from scipy import signal
from scipy.fftpack import fft
import librosa
import numpy as np
from pydub import AudioSegment
import math
from scipy.io.wavfile import read,write
import scipy
from scipy.ndimage import maximum_filter1d

def wav_read(path): # 音声ファイルを読み込む
    wave, fs = librosa.core.load(path, mono=True)
    return wave, fs

def calc_fft(data, fs): # FFTする
    frq = np.linspace(0, fs, len(data))
    yf = fft(data)/(len(data)/2)
    return np.abs(yf), frq

def envelope(y, rate, threshold):
    """
    Args:
        - y: 信号データ
        - rate: サンプリング周波数
        - threshold: 雑音判断するしきい値
    Returns:
        - mask: 振幅がしきい値以上か否か
        - y_mean: Sound Envelop
    """
    y_mean = maximum_filter1d(np.abs(y), mode="constant", size=rate//20)
    mask = [mean > threshold for mean in y_mean]
    return mask, y_mean
def _db_to_amp(x,):
    return librosa.core.db_to_amplitude(x, ref=1.0)
n_fft=2048  # STFTカラム間の音声フレーム数
hop_length=512  # STFTカラム間の音声フレーム数
win_length=2048  # ウィンドウサイズ
n_std_thresh=1.0  # 信号とみなされるために、ノイズの平均値よりも大きい標準偏差（各周波数レベルでの平均値のdB）が何個あるかのしきい値
sample_rate= 22050
fs = 22050
def _stft(y, n_fft, hop_length, win_length):
    return librosa.stft(y=y, n_fft=n_fft, hop_length=hop_length, win_length=win_length)

def _amp_to_db(x):
    return librosa.core.amplitude_to_db(x, ref=1.0, amin=1e-20, top_db=80.0)
def _istft(y, hop_length, win_length):
    return librosa.istft(y, hop_length, win_length)
#sourceAudio = "sample.wav"

#noise_source = "zproblemM5zzz.wav"
#noise_source = "zatuon.wav"
# 音声ファイルの読み込み
# audio_clip, _ = librosa.load(path=noise_source, sr=sample_rate)

# # # ノイズデータ取得
# mask, noise_clip = envelope(audio_clip, sample_rate, threshold=0.03)
# plt.axis([0, len(noise_clip), -max(noise_clip), max(noise_clip)])
# plt.plot(audio_clip)
# plt.plot(noise_clip)
def noise_cancel(sourceAudio,noise):
    sourceAudio1 =sourceAudio+ ".wav"
    noise1 = "./snd/"+noise+".wav"
    audio_clip,fs = wav_read(sourceAudio1)
#noise_clip,fs = wav_read(noise_source)
    noise_clip,fs = wav_read(noise1)
# noise_clip /=44


    noise_stft = _stft(noise_clip, n_fft, hop_length, win_length)
    noise_stft_db = _amp_to_db(np.abs(noise_stft))  # dBに変換する
   
    mean_freq_noise = np.mean(noise_stft_db, axis=1)
    std_freq_noise = np.std(noise_stft_db, axis=1)
    noise_thresh = mean_freq_noise + std_freq_noise * n_std_thresh

    n_grad_freq = 2  # マスクで平滑化する周波数チャンネルの数
    n_grad_time = 4  # マスクを使って滑らかにする時間チャンネル数
    prop_decrease = 1  # ノイズをどの程度減らすか
    
    # 音源もSTFTで特徴量抽出する
    sig_stft = _stft(audio_clip, n_fft, hop_length, win_length)
    sig_stft_db = _amp_to_db(np.abs(sig_stft))
    
    # 時間と頻度でマスクの平滑化フィルターを作成
    smoothing_filter = np.outer(
            np.concatenate(
                [
                    np.linspace(0, 1, n_grad_freq + 1, endpoint=False),
                    np.linspace(1, 0, n_grad_freq + 2),
                ]
            )[1:-1],
            np.concatenate(
                [
                    np.linspace(0, 1, n_grad_time + 1, endpoint=False),
                    np.linspace(1, 0, n_grad_time + 2),
                ]
            )[1:-1],
        )
    smoothing_filter = smoothing_filter / np.sum(smoothing_filter)
    
    # 時間と周波数のしきい値の計算
    db_thresh = np.repeat(
            np.reshape(noise_thresh, [1, len(mean_freq_noise)]),
            np.shape(sig_stft_db)[1],
            axis=0,
        ).T
    sig_mask = sig_stft_db < db_thresh
    sig_mask = scipy.signal.fftconvolve(sig_mask, smoothing_filter, mode="same")
    sig_mask = sig_mask * prop_decrease
    
    mask_gain_dB = np.min(_amp_to_db(np.abs(sig_stft)))
    
    
    
    sig_stft_db_masked = (
            sig_stft_db * (1 - sig_mask)
            + np.ones(np.shape(mask_gain_dB)) * mask_gain_dB * sig_mask
    )
    
    sig_imag_masked = np.imag(sig_stft) * (1 - sig_mask)
    sig_stft_amp = (_db_to_amp(sig_stft_db_masked) * np.sign(sig_stft)) + (1j * sig_imag_masked)
    
    recovered_signal = _istft(sig_stft_amp, hop_length, win_length)
    recovered_signal = recovered_signal.astype(np.float32)
    write("{problem}-{noise}.wav".format(problem=sourceAudio,noise=noise),rate = fs, data = recovered_signal)

noise_cancel("zproblemM5zzzg","J01")