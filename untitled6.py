import numpy as np
import pylab as plt
import pandas as pd
import matplotlib.gridspec as gridspec
from tslearn.metrics import dtw_path
from scipy.io.wavfile import read, write
from scipy import signal
import time
import zipfile

# 処理時間計測開始
start = time.time()

lang=["E","J"]
costAll = []
ans = []
ans_down= []
PATH_LIST = "/content/drive/MyDrive/sample_Q/Jwav_list.txt"

def partial_dtw(x, y):
    Tx = len(x)
    Ty = len(y)

    C = np.zeros((Tx, Ty))
    B = np.zeros((Tx, Ty, 2), int)

    C[0, 0] = dist(x[0], y[0])
    
    #for i in range(Tx):
    #   C[i, 0] = dist(x[i], y[0])
    #   B[i, 0] = [0, 0]

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
    #print(int(cost))
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
 

def kinzi():

    with open(PATH_LIST) as f:
        name = [line.strip() for line in f.readlines()] # 改行削除
    
    #音声の読み込み
    for j in lang:
        for i in range(1,45):
            fs,data = read("C:/Users/shojushota/Documents/procon33/JKspeech/ + j + str(i).zfill(2) + ".wav")
            ans.append(data)
    
    #入力データの読み込み
    #fs6,datadd= read("/content/drive/MyDrive/sample_answer/sample_answer_Q_E04/A01-1.wav")
    fs6,datadd= read("/content/drive/MyDrive/pbunri6_Noise Gate (1).wav")
    
    #音声データの圧縮
    d = datadd
    
    #magnification = 70*(len(d)/48000) / len(d)
    magnification =  100 *(len(d)/48000) / len(d)
    #print(70*(len(d)/48000))
    
    print("データ倍率:{}".format(magnification))
    #magnification = 0.002
    print("データ秒:{}".format(len(d)/48000))
    
    for i in ans:
        ans_down.append(signal.resample(i,int(len(i)*magnification)))
    
    input_data = signal.resample(d,int(len(d)*magnification))
    #input_data = datadd
     
    nj = 1
    for j in ans_down:
        #print("\n")
        #print("E0{}.wav".format(nj))
        #nj+=1
        path, cost = partial_dtw(j, input_data)
    
    sort = sorted(costAll)
    print(costAll)
    print(sort)
    
    
    for i in range(5):
        print("{} スコア {}".format(name[costAll.index(sort[i])], int(sort[i])))
    
    
    
    print("スコア差;{}".format(int(sort[1]-sort[0])))
    print("スコア差の倍率;{}".format(sort[1]/sort[0]))
    
    end = time.time()
    # 処理時間表示
    print("Total elapsed time : {}[sec]".format(round(end - start, 4)))