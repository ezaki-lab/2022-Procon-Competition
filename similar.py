import datetime
import pandas_datareader.data as web
import numpy as np
from scipy.io.wavfile import read, write
import matplotlib.pyplot as plt
from scipy import signal
from scipy.spatial.distance import correlation
from scipy.stats import pearsonr
import pandas as pd
import scipy.stats
import time
# 処理前の時刻
t1 = time.time() 
 


"""聞こえた音声 - 問題音声

例（0.1秒間隔）でずらしていって最も類似度の高い部分を


相関を出す
from scipy.spatial.distance import correlation
1 - correlation(x, y)
x,yそれぞれの波形のリストを入れる

x,yの波形の大きさを間違えないように
どちらかの波形をずらす

最も相関があるところをノイズキャンセリング

ノイズキャンセル"""

def pearson_corr(x, y):
    x_diff = x - np.mean(x)
    y_diff = y - np.mean(y)
    return np.dot(x_diff, y_diff) / (np.sqrt(sum(x_diff ** 2)) * np.sqrt(sum(y_diff ** 2)))

ans = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわ"
fs,problem  = read("C:/Users/学生用/Documents/2022-Procon-Competition/processing/a1/a1.wav")
problem = problem[0:len(problem)//2]
bairitu = 15
problem = signal.resample(problem,len(problem) // bairitu)
problem_size = len(problem)
last =[]
lang = ["E","J"]

for o in lang:
    for l in range(1,45):
        fs,candata = read("./JKspeech/"+ str(o) +str(l).zfill(2)+".wav")

        candata = signal.resample(candata,len(candata) // bairitu)

        sample_size = len(candata)

        n = sample_size - problem_size + 1
        score = []
        #print([n,sample_size,problem_size])
        for i in range(n):
            #score.append(pearsonr(candata[i : i + problem_size],problem))
            score.append(1 - correlation(candata[i : i + problem_size],problem))
            #score.append(pearson_corr(candata[i : i + problem_size],problem))
        makkusu = max(score)
        miin = np.mean(score)
        #print(makkusu - miin)
        last.append(makkusu-miin)

        #plt.plot(score)
        #plt.show()
sort = sorted(last)
answer = ""
print(sort)
for n in range(20):
    answer += (ans[int(last.index(sort[-1-n])%44)])
print(answer)
t2 = time.time()
    
# 経過時間を表示
elapsed_time = t2-t1
print(f"経過時間：{elapsed_time}")
    


