import numpy as np
from scipy import signal
from scipy import fftpack
from scipy.fftpack import fft
import librosa
from scipy.io.wavfile import write


def wav_read(path): # 音声ファイルを読み込む
    wave, fs = librosa.core.load(path, mono=True)
    return wave, fs

def calc_fft(data, fs): # FFTする
    frq = np.linspace(0, fs, len(data))
    yf = fft(data)/(len(data)/2)
    return np.abs(yf), frq
 
#バターワースフィルタ（バンドパス）
def bandpass(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "band")           #フィルタ伝達関数の分子と分母を計算
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

#リニア値からdBへ変換
def db(x, dBref):
    y = 20 * np.log10(x / dBref)     #変換式
    return y      
                   #dB値を返す
def band(wavpath,filename):
    # ここからサンプル波形生成とフィルタ処理をする-------------------------------------------
    samplerate = 48000
    q = 48000/22050
        
    problem = wavpath.replace('./problem/', '')
    data,f= wav_read(wavpath + ".wav")
    yf, frq = calc_fft(data, f)

    # 波形生成のための時間軸の作成
    
    start = [216.56531832921507, 424.55236449742387, 635.4581388555695, 812.3438492483591, 1054.1261835509624,1250]
    end = [233.93855216038023, 468.55836523848967, 702.4031281115167, 936.049399243616, 1176.3345493490413,1350]
    # start = [216.56531832921507, 424.55236449742387, 635.4581388555695, 812.3438492483591, 1054.1261835509624,1250,1450,1650,2750]
    # end = [233.93855216038023, 468.55836523848967, 702.4031281115167, 936.049399243616, 1176.3345493490413,1350,1550,1750,2850]
    
    # start = [216.56531832921507, 424.55236449742387, 635.4581388555695, 812.3438492483591,1000]
    # end = [233.93855216038023, 468.55836523848967, 702.4031281115167, 936.049399243616,1100]
    
    dif = 50
    plusband = 0
    # バンドパスをする関数を実行
    data_filt = [0] * len(end)
    fp = np.array([(plusband + start[0])*q ,q*(plusband + end[0])])                             # 通過域端周波数[Hz]※ベクトル
    fs = np.array([(start[0]-dif+plusband)*q,(end[0]+dif+plusband)*q])                              # 阻止域端周波数[Hz]※ベクトル
    gpass = 5
    gstop = 6
    data_filt[0] = bandpass(data, samplerate, fp, fs, gpass, gstop)
    data_filt[0] = data_filt[0].astype(np.float32)
    
    for j in range(1,len(end)):
        fp = np.array([(plusband + start[j])*q ,q*(plusband + end[j])])                             # 通過域端周波数[Hz]※ベクトル
        fs = np.array([(start[j]-dif+plusband)*q,(end[j]+dif+plusband)*q])                              # 阻止域端周波数[Hz]※ベクトル
        gpass = 5
        gstop = 6
        data_filt[j] = bandpass(data, samplerate, fp, fs, gpass, gstop)
        data_filt[j] = data_filt[j].astype(np.float32)
        data_filt[j] += data_filt[j-1]
    
    write("processing/{}/{}band.wav".format(filename,problem), rate=f, data=data_filt[len(end)-1])