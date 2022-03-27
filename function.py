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
    print(time)
    with open(file_path, mode='w') as f:
        f.write("VRC Join Log")

createpastlog()
