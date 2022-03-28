import glob
import os
import json
import tkinter as tk
from socket import socket, AF_INET, SOCK_DGRAM
import queue
import datetime

def findnewvrclog(): #最新のVRCログファイルのパスを取得する関数
    vrclogdir = os.getenv('LOCALAPPDATA') + 'Low\\VRChat\\VRChat'
    files = glob.glob(vrclogdir + '\\*.txt')
    logs = {}
    for file in files:
        logs[file] = os.stat(file)
    logs = sorted(logs.items(), key=lambda x: x[1].st_mtime, reverse=True)
    return logs[0][0]

def createpastlog(): #出力ログの作成
    dt_now = datetime.datetime.now()
    time = dt_now.strftime('[%Y-%m-%d %H.%M.%S] ')
    file_name = 'VRC_Logs.txt'
    file_path = os.environ['userprofile']
    file_path = file_path + '\\desktop\\' + str(time)+file_name
    with open(file_path,'a') as i:
        i.write("VRC Join Log Output_time = "+time+"\n")
        i.write("==============================================\n")

def writelog():#出力ログの作成ログへの書き込み
    dt_now = datetime.datetime.now()
    time = dt_now.strftime('[%Y-%m-%d %H.%M.%S] ')
    file_name = 'VRC_Logs.txt'
    file_path = os.environ['userprofile']
    file_path = file_path + '\\desktop\\' + str(time)+file_name
    path = findnewvrclog()
    with open(path,encoding="UTF-8") as f:#一行ずつ読み込み
        for line in f:
            count_1 = line.find("[Behaviour] OnPlayerJoined")
            count_2 = line.find("[Behaviour] Entering Room")
            if count_1 != -1:
                qdata = line[:20]+line[60:].replace("\n","")
                with open(file_path,'a') as i:
                    i.write(qdata+"\n")
            else:
                if count_2 != -1:
                    qdata = line[:20]+line[60:].replace("\n","")
                    with open(file_path,'a') as i:
                        i.write("\n\n")
                        i.write(qdata+"\n")
                        i.write("-----------------------------------------\n")
                else:
                    exit

createpastlog()
writelog()