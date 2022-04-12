import glob
import os
import sys
import json
from socket import socket, AF_INET, SOCK_DGRAM

def resource_path(relative): #リソースのパスを取得する関数
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative)
    return os.path.join(os.path.abspath('.'), relative)

def findnewvrclog(): #最新のVRCログファイルを取得する関数
    files = glob.glob(os.getenv('LOCALAPPDATA') + 'Low\\VRChat\\VRChat\\*.txt')
    logs = {}
    for file in files:
        logs[file] = os.stat(file)
    logs = sorted(logs.items(), key=lambda x: x[1].st_mtime, reverse=True)
    return logs[0][0]

def sendtoxsoverlay(content): #XSOverlayに通知を送信する関数
    s = socket(AF_INET, SOCK_DGRAM)
    msg = {
        "messageType": 1,
        "index": 0,
        "timeout": 3.0,
        "height": 100,
        "opacity": 1,
        "volume": 0.5,
        "audioPath": "default",
        "title": "Join",
        "content": content,
        "useBase64Icon": False,
        "icon": "",
        "sourceApp": "",
    }
    msg_str = json.dumps(msg)
    s.sendto(msg_str.encode("utf-8"), ("127.0.0.1", 42069))
    s.close()

def writejoinlog(writedata): #Joinログを.txtファイルに書き出す関数
    if os.path.exists('.\\vrcjoinlog.txt'):
        with open(".\\vrcjoinlog.txt", "a", encoding="utf-8") as f:
            f.write(writedata)
    else:
        with open(".\\vrcjoinlog.txt", "x", encoding="utf-8") as f:
            f.write(writedata)

def savesettings(updinterval, sendxsoverlay, writelog, restorelogs, separateworld, tasktray, startnowindow): #設定をファイルに書き込む関数
    config["updinterval"] = updinterval
    config["sendxsoverlay"] = sendxsoverlay
    config["writelog"] = writelog
    if restorelogs:
        if not writelog:
            config["writelog"] = True
    config["restorelogs"] = restorelogs
    config["separateworld"] = separateworld
    config["tasktray"] = tasktray
    if startnowindow:
        if not tasktray:
            config["tasktray"] = True
    config["startnowindow"] = startnowindow
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    loadsettings() #設定を再読み込み

def savenonofityusr(nonotifyusr): #通知を行わないユーザをファイルに保存する関数
    with open("config.json", "w") as f:
        config["no_notifysusr"] = nonotifyusr
        json.dump(config, f, indent=2)
    loadsettings()

def loadsettings(): #設定を読み込む関数
    global config
    if os.path.exists('.\\config.json'):
        f = open('.\\config.json', 'r')
        config = json.load(f)
        f.close()
    else:
        config = {"updinterval": "1500", "sendxsoverlay": True, "writelog": True, "restorelogs": True, "separateworld": True, "tasktray": True, "startnowindow": False, "no_notifysusr": ""}
        f = open('.\\config.json', 'w')
        json.dump(config, f, indent=2) #json形式で書き込み
        f.close()

