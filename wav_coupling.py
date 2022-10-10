import numpy as np
from scipy.io.wavfile import read, write



def WavSort(wavlist,name):
    wavdata = []
    
    sortWav = sorted(wavlist)
    
    for i in sortWav:
        fs,data = read(i)
        wavdata.extend(data)
        
    wavdata = np.array(wavdata,dtype = "int16")
    name = "./processing/" + name + "/" + name
    print(name)
    write(name + ".wav", rate=fs, data = wavdata)
    
    return name