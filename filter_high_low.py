import numpy as np
from scipy import signal
from scipy import fftpack
from scipy.fftpack import fft
import librosa
from scipy.io.wavfile import read,write
import wave
import soundfile as sf

def wav_read(path): # 音声ファイルを読み込む
    wave, fs = librosa.core.load(path, mono=True)
    return wave, fs

def calc_fft(data, fs): # FFTする
    frq = np.linspace(0, fs, len(data))
    yf = fft(data)/(len(data)/2)
    return np.abs(yf), frq
#バターワースフィルタ（ローパス）
def lowpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "low")            #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y                                      #フィルタ後の信号を返す

def highpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "high")            #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y                                      #フィルタ後の信号を返す

# オーバーラップ処理
def ov(data, samplerate, Fs, overlap):
    Ts = len(data) / samplerate                                                # 全データ長
    Fc = Fs / samplerate                                                       # フレーム周期
    x_ol = Fs * (1 - (overlap / 100))                                          # オーバーラップ時のフレームずらし幅
    N_ave = int((Ts - (Fc * (overlap / 100))) / (Fc * (1 - (overlap / 100))))  # 抽出するフレーム数（平均化に使うデータ個数）

    array = []                                                                 # 抽出したデータを入れる空配列の定義

    # forループでデータを抽出
    for i in range(N_ave):
        ps = int(x_ol * i)                                                     # 切り出し位置をループ毎に更新
        array.append(data[ps:ps + Fs:1])                                       # 切り出し位置psからフレームサイズ分抽出して配列に追加
    return array, N_ave                                                        # オーバーラップ抽出されたデータ配列とデータ個数を戻り値にする

# 窓関数処理（ハニング窓）
def hanning(data_array, Fs, N_ave):
    han = signal.hann(Fs)                    # ハニング窓作成
    acf = 1 / (sum(han) / Fs)                # 振幅補正係数(Amplitude Correction Factor)

    # オーバーラップされた複数時間波形全てに窓関数をかける
    for i in range(N_ave):
        data_array[i] = data_array[i] * han  # 窓関数をかける

    return data_array, acf

# FFT処理
def fft_ave(data_array, samplerate, Fs, N_ave, acf):
    fft_array = []
    for i in range(N_ave):
        fft_array.append(acf * np.abs(fftpack.fft(data_array[i]) / (Fs / 2)))  # FFTをして配列に追加、窓関数補正値をかけ、(Fs/2)の正規化を実施。

    fft_axis = np.linspace(0, samplerate, Fs)                                  # 周波数軸を作成
    fft_array = np.array(fft_array)                                            # 型をndarrayに変換
    fft_mean = np.mean(fft_array, axis=0)                                      # 全てのFFT波形の平均を計算

    return fft_array, fft_mean, fft_axis


def highlow(wavpath):
    # ここからサンプル波形生成とフィルタ処理をする-------------------------------------------
    
    samplerate = 22050
    problem = wavpath.replace('./problem/', '')    
    data,f= wav_read(wavpath + ".wav")
    yf, frq = calc_fft(data, f)
    
    fp = 1500                                               # 通過域端周波数[Hz]
    fs = 6000                                               # 阻止域端周波数[Hz]
    gpass = 3                                               # 通過域端最大損失[dB]
    gstop = 40                                              # 阻止域端最小損失[dB]
    
    # ローパスをする関数を実行
    data_filt = lowpass(data, samplerate, fp, fs, gpass, gstop)
    data_filt = data_filt.astype(np.float32)
    path = "./processing/" + problem
    write("{}low.wav".format(path), rate = f,data = data_filt)
    data_high = highpass(data,samplerate,fp,fs,gpass,gstop)
    data_high = data_high.astype(np.float32)
    write("{}high.wav".format(path),rate= f ,data = data_high)
