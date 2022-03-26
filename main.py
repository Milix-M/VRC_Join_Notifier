import glob
import os
import json
import tkinter as tk
from socket import socket, AF_INET, SOCK_DGRAM
import queue

def findnewvrclog(): #最新のVRCログファイルを取得する関数
    vrclogdir = os.getenv('LOCALAPPDATA') + 'Low\\VRChat\\VRChat'
    files = glob.glob(vrclogdir + '\\*.txt')
    logs = {}
    for file in files:
        logs[file] = os.stat(file)
    logs = sorted(logs.items(), key=lambda x: x[1].st_mtime, reverse=True)
    return logs[0][0]

def sendtoxsoverlay(content): #XSOverlayに通知を送信する関数
    PORT = 42069
    ADDRESS = "127.0.0.1" # 自分に送信
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
    s.sendto(msg_str.encode("utf-8"), (ADDRESS, PORT))
    s.close()

def writejoinlog(writedata): #Joinログを.txtファイルに書き出す関数
    if os.path.exists('.\\vrcjoinlog.txt'):
        with open(".\\vrcjoinlog.txt", "a", encoding="utf-8") as f:
            f.write(writedata)
    else:
        with open(".\\vrcjoinlog.txt", "x", encoding="utf-8") as f:
            f.write(writedata)

def savesettings(updinterval, sendxsoverlay, writelog, restorelogs, separateworld): #設定をファイルに書き込む関数
    config["updinterval"] = updinterval
    config["sendxsoverlay"] = sendxsoverlay
    config["writelog"] = writelog
    if restorelogs:
        if not writelog:
            config["writelog"] = True
    config["restorelogs"] = restorelogs
    config["separateworld"] = separateworld
    with open("config.json", "w") as f:
        json.dump(config, f, indent=2)
    loadsettings() #設定を再読み込み

def savenonofityusr(nonotifyusr): #通知を行わないユーザをファイルに保存する関数
    if os.path.exists('.\\no_notifyusr.txt'):
        with open(".\\no_notifyusr.txt", "w", encoding="utf-8") as f:
            f.write(nonotifyusr)
    else:
        with open(".\\no_notifyusr.txt", "x", encoding="utf-8") as f:
            f.write(nonotifyusr)
    loadblacklist()

def loadsettings(): #設定を読み込む関数
    global config
    #設定ファイルを読み込み開始
    if os.path.exists('.\\config.json'):
        f = open('.\\config.json', 'r')
        config = json.load(f)
        f.close()
    else:
        config = {"updinterval": "1500", "sendxsoverlay": True, "writelog": True, "restorelogs": True, "separateworld": True}
        f = open('.\\config.json', 'w')
        json.dump(config, f, indent=2) #json形式で書き込み
        f.close()
    #設定ファイル読み込み終了

def loadblacklist(): #ブラックリストを読み込む関数
    global nonotifyusers
    #ブラックリストを読み込み開始
    if os.path.exists('.\\no_notifyusr.txt'):
        f = open('.\\no_notifyusr.txt', 'r', encoding="utf-8")
        nonotifyusers = f.read()
        f.close()
    #ブラックリスト読み込み終了

def createsettingwin(): #設定ウィンドウを作成する関数
    settingwin = tk.Toplevel()
    settingwin.title("環境設定")
    settingwin.geometry("300x200")
    updintervallabel = tk.Label(settingwin, text="更新間隔(ms)").pack()
    updinterval = tk.Entry(settingwin, width=10)
    updinterval.insert(0, config["updinterval"])
    updinterval.pack()

    bl = tk.BooleanVar()
    bl.set(config["sendxsoverlay"])
    sendxsovelaychkbox = tk.Checkbutton(settingwin, variable=bl, text="XSOverlayに送信する").pack()

    bl2 = tk.BooleanVar()
    bl2.set(config["writelog"])
    writelogchkbox = tk.Checkbutton(settingwin, variable=bl2, text="Joinログを.txt形式で書き出す").pack()

    bl3 = tk.BooleanVar()
    bl3.set(config["restorelogs"])
    restorelogschkbox = tk.Checkbutton(settingwin, variable=bl3, text="Joinログを.txtファイルから読み込み復元する").pack()

    bl4 = tk.BooleanVar()
    bl4.set(config["separateworld"])
    separateworldchkbox = tk.Checkbutton(settingwin, text="ワールド移動時にJoinログに区切りを挿入する").pack()

    complatebuttom = tk.Button(settingwin, text="保存", command=lambda:savesettings(updinterval.get(), bl.get(), bl2.get(), bl3.get(), bl4.get())).pack()

def createblacklistwin(): #ブラックリストを編集するウィンドウを作成する関数
    blacklistwin = tk.Toplevel()
    blacklistwin.title("通知しないユーザーを編集")
    blacklistwin.geometry("400x100")
    blacklistwin.resizable(False, False)
    nonotifyusrlabel = tk.Label(blacklistwin, text="XSOvelayで通知しないユーザー名をカンマ区切りで入力").pack()
    nonotifyusr = tk.Entry(blacklistwin, width=50)
    loadblacklist()
    nonotifyusr.insert(0, nonotifyusers)
    nonotifyusr.pack()
    editcompletebtn = tk.Button(blacklistwin, text="保存", command=lambda:savenonofityusr(nonotifyusr.get())).pack()

def main(lastline): #メイン関数
    senddatas = queue.Queue()
    xsdata = []
    joindata = ""
    deleteusrs = nonotifyusers.split(",")
    path = findnewvrclog() #最新のVRCログファイルを取得
    with open(path, encoding="utf-8") as f: #ログファイルをリストで読み込み
        lines = f.readlines()
    endlines = len(lines) - 1 #最新の行までの行数
    newlines = lines[lastline:]
    for line in newlines:
        count = line.find("[Behaviour] OnPlayerJoined") #指定文字列がある行を探す
        if count != -1: #OnPlayerJoinedが見つかったら
            qdata = (line[60:] + ",").replace("\n", "")
            xsdata.append((line[60:]).replace("\n", "")) #XSOverlayに送信するデータをリストに追加
            senddatas.put(qdata)
            joindata = line[:19] + " Join"
    if joindata:
        joinlog = ""
        while not senddatas.empty(): #senddatasがある間
            joinlog = joinlog + senddatas.get() #senddatasからデータを取り出しjoinlogに追加
        final_string = joindata + joinlog.rstrip(",") + "\n"
        if config["sendxsoverlay"]:
            for i in deleteusrs: #ブラックリストにあるユーザーを削除
                if " " + i in xsdata:
                    xsdata.remove(" " + i)
            xsoverlaysenddata = ",".join(xsdata) #ユーザーごとにカンマを入れて代入
            xsoverlaysenddata = xsoverlaysenddata.lstrip().rstrip() #空白を削除
            #xsoverlaysenddata = joinlog.rstrip(",").lstrip(" ") #XSOverlayに送るデータ
            if xsoverlaysenddata:
                sendtoxsoverlay(xsoverlaysenddata) #XSOverlayに送信
        logview.configure(state='normal')
        logview.insert('end', final_string)
        logview.see("end")
        logview.configure(state='disabled')
        if config["writelog"]:
            writejoinlog(final_string)
    root.after(config["updinterval"], main, endlines) #メイン関数を呼び出し

#GUI設定
root = tk.Tk()
root.title("VRChat Join Notifier")
root.geometry("800x500")

#メニューバー
menubar = tk.Menu(root)
root.config(menu=menubar)
menucfg = tk.Menu(root, tearoff=0)
menubar.add_cascade(label="設定", menu=menucfg)
menucfg.add_command(label="環境設定", command=createsettingwin)
menucfg.add_separator()
menucfg.add_command(label="通知除外設定", command=createblacklistwin)

#上部ロゴテキスト
logolabel = tk.Label(root, text="VRChat Join Notifier", font=("MSゴシック", "20", "bold")).grid(row=0, column=0)

#テキストエリア
scrollbar_text = tk.Scrollbar(orient="vertical") #スクロールバー
logview = tk.Text(root, yscrollcommand=scrollbar_text.set, font=("メイリオ", "13")) #Joinログ表示用テキスト
logview.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
scrollbar_text.config(command=logview.yview)
scrollbar_text.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

#ウィンドウのgrid設定
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

path = findnewvrclog() #最新のVRCログファイルを取得
with open(path, encoding="utf-8") as f: #ログファイルをリストで読み込み
    lines = f.readlines()

loadsettings() #設定ファイルを読み込む
loadblacklist() #ブラックリストを読み込む

if config["restorelogs"] and os.path.exists(".\\vrcjoinlog.txt"): #Joinログを.txtファイルから読み込み、テキストエリアに表示
    with open(".\\vrcjoinlog.txt", "r", encoding="utf-8") as f:
        oldlog = f.read()
        logview.configure(state='normal')
        logview.insert('end', oldlog)
        logview.see("end")
        logview.configure(state='disabled')

main(len(lines) - 1) #メイン関数を呼び出す

root.mainloop()