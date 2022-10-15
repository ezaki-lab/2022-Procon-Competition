import numpy as np
from scipy.io.wavfile import read, write




name="a1"
wavlist =["./problem/problem1.wav","./problem/problem2.wav","./problem/problem3.wav"]#,"./problem/problem4.wav"]
wavdata = []

sortWav = sorted(wavlist)

for i in sortWav:
    fs,data = read(i)
    wavdata.extend(data)
    
wavdata = np.array(wavdata,dtype = "int16")
name = "./processing/" + name + "/" + name
write(name + ".wav", rate=fs, data = wavdata)
