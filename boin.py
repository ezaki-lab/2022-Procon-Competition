import numpy as np
from scipy import signal
from scipy import fftpack
from scipy.fftpack import fft
import librosa
from scipy.io.wavfile import write

#バターワースフィルタ（バンドストップ）
def bandstop(x, samplerate, fp, fs, gpass, gstop):
    fn = samplerate / 2                           #ナイキスト周波数
    wp = fp / fn                                  #ナイキスト周波数で通過域端周波数を正規化
    ws = fs / fn                                  #ナイキスト周波数で阻止域端周波数を正規化
    N, Wn = signal.buttord(wp, ws, gpass, gstop)  #オーダーとバターワースの正規化周波数を計算
    b, a = signal.butter(N, Wn, "bandstop")       #フィルタ伝達関数の分子と分母を計算
    y = signal.filtfilt(b, a, x)                  #信号に対してフィルタをかける
    return y                                      #フィルタ後の信号を返す

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


    # forループでデータを抽出
    for i in range(N_ave):
        ps = int(x_ol * i)                                                     # 切り出し位置をループ毎に更新
        array.append(data[ps:ps + Fs:1])                                       # 切り出し位置psからフレームサイズ分抽出して配列に追加
    return array, N_ave                                                        # オーバーラップ抽出されたデータ配列とデータ個数を戻り値にする

def boinband(wavpath,filename):
    # ここからサンプル波形生成とフィルタ処理をする-------------------------------------------
    samplerate = 48000
    q = 48000/22050
        
    problem = wavpath.replace('./processing/'+ filename + "/", '')
    data,f= wav_read(wavpath + ".wav")
    # 波形生成のための時間軸の作成
    
    start = [424.55236449742387, 500]
    end = [ 468.55836523848967, 1700]
    dif = 50                #幅
    plusband = 10            #start,endにプラスする量
    data_filt = [0]*len(end)
    # バンドパスをする関数を実行
    fp = np.array([(plusband + start[0])*q ,q*(plusband + end[0])])                             # 通過域端周波数[Hz]※ベクトル
    fs = np.array([(start[0]-dif-plusband)*q,(end[0]+dif+plusband)*q])                              # 阻止域端周波数[Hz]※ベクトル
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

    write("processing/"+filename+"/n{}band.wav".format(problem), rate=f, data=data_filt[len(end)-1])

    start = [300]
    end = [1700]

    dif = 49
    plusband = 12
    j=0
    # バンドパスをする関数を実行
    fp = np.array([(plusband + start[j])*q ,q*(plusband + end[j])])                             # 通過域端周波数[Hz]※ベクトル
    fs = np.array([(start[j]-dif+plusband)*q,(end[j]+dif+plusband)*q])                              # 阻止域端周波数[Hz]※ベクトル
    gpass = 5                                               # 通過域端最大損失[dB]
    gstop = 6                                             # 阻止域端最小損失[dB]
    data_filt = bandpass(data, samplerate, fp, fs, gpass, gstop)
    data_filt = data_filt.astype(np.float32)
    data_filt *=5
    write(f"processing/"+filename+"/i{}band.wav".format(problem), rate=f, data=data_filt)

    fp = np.array([500, 1500])      #通過域端周波数[Hz]※ベクトル
    fs = np.array([250, 6000])      #阻止域端周波数[Hz]※ベクトル    gpass = 3                                               # 通過域端最大損失[dB]
    gstop = 40                                              # 阻止域端最小損失[dB]
     
    data_filt = bandstop(data, samplerate, fp, fs, gpass, gstop)
    
    data_filt = data_filt.astype(np.float32)
    write(f"processing/"+filename+"/e{}band.wav".format(problem),rate = f, data=data_filt)

    fp = np.array([500, 2000])      #通過域端周波数[Hz]※ベクトル
    fs = np.array([250, 4000])      #阻止域端周波数[Hz]※ベクトル
    gpass = 1                                              # 通過域端最大損失[dB]
    gstop = 41                                              # 阻止域端最小損失[dB]
     
    data_filt = bandstop(data, samplerate, fp, fs, gpass, gstop)
    
    data_filt = data_filt.astype(np.float32)
<<<<<<< HEAD
    write(f"processing/a{problem}band.wav",rate = f, data=data_filt)
=======
    write(f"processing/"+filename+"a{problem}band.wav",rate = f, data=data_filt)

>>>>>>> 1fdf32a9a9451eb759b9500287979636ff34ba7a
