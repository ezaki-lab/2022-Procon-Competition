import os
import urllib.parse
import json
import sys
import requests
import re
import wav_coupling
import datetime
import kinzi
import time

url = "https://procon33-practice.kosen.work"
filepath = "C:/Users/shojushota/Documents/procon33"  
token = open("token.txt").read()
    
def match() -> None:
    endpoint = urllib.parse.urljoin(url,"match")
    res = requests.get(endpoint,  headers={"procon-token": token})
    
    if res.status_code!=200:
        print(res.text)
        
    else:
        print(res.text)

def problem() -> None:
    endpoint =urllib.parse.urljoin(url,"problem")
    res = requests.get(endpoint, headers = {"procon-token": token})
    
    if res.status_code!=200:
        print(res.text)
        
    else:
        res = json.loads(res.text)

        start = datetime.datetime.fromtimestamp(res["starts_at"])
        print("id:{}\n 分割数:{}\n 開始時間:{}:{}:{}\n 制限時間:{}\n データ数:{}".format(res["id"], res["chunks"], start.hour,start.minute,start.second, res["time_limit"], res["data"]))
        return res["id"]

def chunks(chunks) -> None:
    endpoint = urllib.parse.urljoin(url,"problem/chunks?n="+chunks)
    res = requests.post(endpoint, headers={"procon-token": token})
    if res.status_code==200:
        loads = json.loads(res.text)  
        filename = loads.get("chunks")
        wavfile = []
    
        for count in range(len(filename)):
            endpoint =urllib.parse.urljoin(url, "problem/chunks/"+filename[count])
            res = requests.get(endpoint,  headers={"procon-token": token})
            file = open(os.path.join(filepath,os.path.basename(endpoint)),"wb")
            for chunks in res.iter_content(100000):
                file.write(chunks)
            wavfile.append(file.name)
            file.close()
        return wavfile
    else:
        print(res.content) 
    
def answer(answers:str) -> None:
    endpoint = urllib.parse.urljoin(url,"problem")
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
    while True:
        print("1:match  2:problem  3:chunks  4:answer  5:終了")
        mode = int(input())
        
        if mode == 1:
            match()
            
        elif mode == 2:
            filename = problem()
            
        elif mode ==3:
            chunk = input("分割数:")
            wavfile = chunks(chunk)
            wav_coupling.WavSort(wavfile,filename)
            result = kinzi.kinzi(filename + ".wav")
            answer(result)
            
        elif mode == 4:
            result = input("answer:")
            answer(result)
            
        elif mode == 5:
            break
    
    