import os
import urllib.parse
import json
import sys
import requests
import re
import wav_coupling
import datetime
import kinzi
import bandopasu
import filter_high_low
import os
import noisecancel
import boin

#url = "https://procon33-practice.kosen.work"
url = "http://172.28.1.1:80"
filepath = "./problem"  
token = open("token.txt").read()
    
def match() -> None:
    endpoint = urllib.parse.urljoin(url,"match")
    res = requests.get(endpoint,  headers={"procon-token": token})
    
    if res.status_code!=200:
        sys.exit(res.text)
        
    else:
        print(res.text)

def problem() -> None:
    endpoint =urllib.parse.urljoin(url,"problem")
    res = requests.get(endpoint, headers = {"procon-token": token})
    
    if res.status_code!=200:
        sys.exit(res.text)
        
    else:
        res = json.loads(res.text)

        start = datetime.datetime.fromtimestamp(res["start_at"])
        print("id:{}\n 分割数:{}\n 開始時間:{}:{}:{}\n 制限時間:{}\n データ数:{}".format(res["id"], res["chunks"], start.hour,start.minute,start.second, res["time_limit"], res["data"]))
        return res["id"]

def chunks(chunks) -> None:
    endpoint = urllib.parse.urljoin(url,"problem/chunks?n=" + chunks)
    res = requests.post(endpoint, headers={"procon-token": token})
    if res.status_code==200:
        loads = json.loads(res.text)  
        filename = loads.get("chunks")
        wavfile = []
    
        for count in range(len(filename)):
            endpoint =urllib.parse.urljoin(url, "problem/chunks/" + filename[count])
            res = requests.get(endpoint,  headers={"procon-token": token})
            file = open(os.path.join(filepath,os.path.basename(endpoint)),"wb")
            for chunks in res.iter_content(100000):
                file.write(chunks)
            wavfile.append(file.name)
            file.close()
        return wavfile
    else:
        sys.exit(res.content) 
    
def answer() -> None:
    ansin = input("answer:")
    ansin = "".join(set(ansin))
    answers = ""
    ans = "あいうえおかきくけこさしすせそたちつてとなにぬねのはひふへほまみむめもやゆよらりるれろわ"
    endpoint = urllib.parse.urljoin(url,"problem")
    
    for i in range(44):
        for j in ansin:
            if j == ans[i]: 
                answers += str(i+1).zfill(2)
                
    answers = re.split('(..)',answers)[1::2]
    
    res = requests.get(endpoint, headers = {"procon-token": token})
    res = json.loads(res.text)
    jsondata ={
        "problem_id": res["id"],
        "answers": answers
        }
   
    j = json.dumps(jsondata)
    res = requests.post(endpoint, headers={"procon-token": token,
                                           "Content-Type": "application/json"}, data = j)
    print(res.text)

if __name__ == "__main__":
    match()    
    filename = problem()
    chunk = input("分割数:")
    wavfile = chunks(chunk)
    if not os.path.exists("./processing/" + filename):
        os.mkdir("./processing/" + filename)
    wavpath = wav_coupling.WavSort(wavfile,filename)
    writename = bandopasu.band(wavpath,filename)
    filter_high_low.highlow(wavpath,filename)
    noisecancel.noise_cancel(wavpath,writename)
    boin.boinband(wavpath,filename)
    #result = kinzi.kinzi(filename + ".wav")
    answer()
    
    