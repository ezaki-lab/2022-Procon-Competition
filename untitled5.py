import numpy as np
import pylab as plt
import pandas as pd
import matplotlib.gridspec as gridspec
from scipy.io.wavfile import read, write
from scipy import signal
import time

pas = "C:/Users/shojushota/Downloads/JKspeech-v_1_0/JKspeech/problems/"
a = ["AE01-2.wav","AE01-1.wav"]

def WavSort(wavlist):
    wavdata = []
    
    sortWav = sorted(wavlist)
    print(sortWav)
    
    for i in sortWav:
        fs,data = read(pas+i)
        wavdata.extend(data)
        
    wavdata = np.array(wavdata,dtype = "int16")
    
    write("problem.wav", rate=fs, data=wavdata)