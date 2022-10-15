import numpy as np
from scipy.io.wavfile import read, write

def minus(JKpath,problem,cutpoint):

    fs,JKlist = read("./JKspeech/" + JKpath + ".wav")
    fs,problemlist = read(problem)
    minusData =  problem - JKlist[cutpoint:cutpoint + len(problemlist) - 1]
    name += JKpath
    write(name  + ".wav",fs = fs, data = minusData)
    return name