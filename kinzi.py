import numpy as np
from scipy.io.wavfile import read
from scipy import signal
import time
import fftonly 



lang=["E","J"]
costAll = []
ans = []
ans_down= []
PATH_LIST = "wav_list.txt"

def partial_dtw(x, y):
    Tx = len(x)
    Ty = len(y)

    C = np.zeros((Tx, Ty))
    B = np.zeros((Tx, Ty, 2), int)

    C[0, 0] = dist(x[0], y[0])

    for j in range(1, Ty):
        C[0, j] = C[0, j - 1] + dist(x[0], y[j])
        B[0, j] = [0, j - 1]

    for i in range(1, Tx):
        for j in range(1, Ty):
            pi, pj, m = get_min(C[i - 1, j],
                                C[i, j - 1],
                                C[i - 1, j - 1],
                                i, j)
            C[i, j] = dist(x[i], y[j]) + m
            B[i, j] = [pi, pj]
    t_end = np.argmin(C[:,-1])
    cost = C[t_end, -1]
    
    path = [[t_end, Ty - 1]]
    i = t_end
    j = Ty - 1
    
    while (B[i, j][0] != 0 or B[i, j][1] != 0):
        path.append(B[i, j])
        i, j = B[i, j].astype(int)
        
    costAll.append(round(cost,1))
    return np.array(path), cost

def dist(x, y):
    return (x - y)**2

def get_min(m0, m1, m2, i, j):
    if m0 < m1:
        if m0 < m2:
            return i - 1, j, m0
        else:
            return i - 1, j - 1, m2
    else:
        if m1 < m2:
            return i, j - 1, m1
        else:
            return i - 1, j - 1, m2
 

def kinzi(input_name):
    
    with open(PATH_LIST) as f:
        name = [line.strip() for line in f.readlines()] # 改行削除
    
    #音声の読み込み
    for j in lang:
        for i in range(1,45):
            fs,data = read("./JKspeech/"+ j + str(i).zfill(2) + ".wav")
            ans.append(data)
    
    #入力データの読み込み
    #fs6,datadd= read("/content/drive/MyDrive/sample_answer/sample_answer_Q_E04/A01-1.wav")
    fs,data= read(input_name)
 
    #magnification = 70*(len(d)/48000) / len(d)
    magnification =  50 * (len(data)/48000) / len(data)
    
    for i in ans:
        ans_down.append(signal.resample(i,int(len(i)*magnification)))
    
    input_data = signal.resample(data,int(len(data)*magnification))
     
    for j in ans_down:
        path, cost = partial_dtw(j, input_data)
    
    sort = sorted(costAll)
    
    return name[costAll.index(sort[0])][1:3]