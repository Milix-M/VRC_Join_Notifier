import webbrowser
import glob
import os
import sys
import json
import tkinter as tk
from socket import socket, AF_INET, SOCK_DGRAM
import queue
import threading
import pystray
from pystray import Icon, Menu, MenuItem
from PIL import Image
import comtypes.client
import pathlib

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

def savesettings(updinterval, sendxsoverlay, writelog, restorelogs, separateworld, tasktray, startnowindow, leave): #設定をファイルに書き込む関数
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
    config["leave"] = leave
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
        config = {"updinterval": "1500", "sendxsoverlay": True, "writelog": True, "restorelogs": True, "separateworld": True, "tasktray": True, "startnowindow": False, "leave":True, "no_notifysusr": ""}
        f = open('.\\config.json', 'w')
        json.dump(config, f, indent=2) #json形式で書き込み
        f.close()

def thread_st(): #スレッドの開始をする関数
    global icon
    global root
    options_map = {'表示': lambda:[root.after(0,root.deiconify)], '終了': lambda: root.after(1, thread_quit)}
    items = []
    for option, callback in options_map.items():
        items.append(MenuItem(option, callback, default=True if option == 'Show' else False))
    menu = Menu(*items)
    image = Image.open(resource_path("icon.ico"))
    icon=pystray.Icon("name", image, "VRChat Join通知システム", menu)
    icon.run()

def thread_quit(): #スレッドの終了処理をする関数
    global icon
    global root
    icon.stop()
    root.destroy()

def createaboutapp(): #このアプリについてのウィンドウを作成する関数
    global appversion
    aboutapp = tk.Toplevel()
    aboutapp.title("このアプリについて")
    aboutapp.geometry("300x140")
    appname = tk.Label(aboutapp, text="VRChat Join通知システム", font=("メイリオ", 12)).pack()
    verlabel = tk.Label(aboutapp, text="Ver:{}".format(appversion), font=("メイリオ", 10)).pack()
    repo = tk.Label(aboutapp, text="リポジトリへのリンク", fg="blue")
    repo.pack()
    repo.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Milix-M/VRC_Join_Notifier"))
    author = tk.Label(aboutapp, text="作者:ReoSteldam", fg="blue")
    author.pack()
    author.bind("<Button-1>", lambda e: webbrowser.open_new("https://twitter.com/ReoSteldam"))
    updbtn = tk.Button(aboutapp, text="アップデートを確認", width=13, command=lambda : webbrowser.open_new("https://github.com/Milix-M/VRC_Join_Notifier/releases"))
    updbtn.pack(fill = 'x', padx=20, side = 'left')
    okbtn = tk.Button(aboutapp, text="OK", width=13, command=aboutapp.destroy)
    okbtn.pack(fill = 'x', padx=20, side = 'right')
    aboutapp.focus_set()


def createsettingwin(): #設定ウィンドウを作成する関数
    settingwin = tk.Toplevel()
    settingwin.title("環境設定")
    settingwin.geometry("300x250")
    settingwin.resizable(False, False)
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
    separateworldchkbox = tk.Checkbutton(settingwin, variable=bl4, text="ワールド移動時にJoinログに区切りを挿入する").pack()

    bl5 = tk.BooleanVar()
    bl5.set(config["tasktray"])
    tasktraychkbox = tk.Checkbutton(settingwin, variable=bl5, text="タスクトレイに最小化").pack()

    bl6 = tk.BooleanVar()
    bl6.set(config["startnowindow"])
    startnowindowchkbox = tk.Checkbutton(settingwin, variable=bl6, text="最小化した状態で起動").pack()

    bl7 = tk.BooleanVar()
    bl7.set(config["leave"])
    leavelogshowwinchkbox = tk.Checkbutton(settingwin, variable=bl7, text="Leaveログを表示する").pack()

    complatebuttom = tk.Button(settingwin, text="保存", command=lambda:[savesettings(updinterval.get(), bl.get(), bl2.get(), bl3.get(), bl4.get(), bl5.get(), bl6.get(), bl7.get()), settingwin.destroy()]).pack()
    settingwin.focus_set()

def createblacklistwin(): #ブラックリストを編集するウィンドウを作成する関数
    blacklistwin = tk.Toplevel()
    blacklistwin.title("通知しないユーザーを編集")
    blacklistwin.geometry("400x100")
    blacklistwin.resizable(False, False)
    nonotifyusrlabel = tk.Label(blacklistwin, text="XSOvelayで通知しないユーザー名をカンマ区切りで入力").pack()
    nonotifyusr = tk.Entry(blacklistwin, width=50)
    loadsettings()
    nonotifyusr.insert(0, config["no_notifysusr"])
    nonotifyusr.pack()
    editcompletebtn = tk.Button(blacklistwin, text="保存", command=lambda:[savenonofityusr(nonotifyusr.get()), blacklistwin.destroy()]).pack()
    blacklistwin.focus_set()

def autoexecwin(): #自動実行ウィンドウを作成する関数
    #リンク先のファイル名
    target_file=os.path.join(sys.argv[0])
    #ショートカットを作成するパス
    save_path=os.path.join(str(pathlib.Path.home()) + "\AppData\Roaming\Microsoft\Windows\Start Menu\Programs\Startup\\","VJN.lnk")
    #WSHを生成
    wsh=comtypes.client.CreateObject("wScript.Shell",dynamic=True)
    #ショートカットの作成先を指定して、ショートカットファイルを開く。作成先のファイルが存在しない場合は、自動作成される。
    short=wsh.CreateShortcut(save_path)
    #以下、ショートカットにリンク先やコメントといった情報を指定する。
    #リンク先を指定
    short.TargetPath=target_file
    #コメントを指定する
    short.Description="VRChat Join通知システム"
    #作業ディレクトリ指定
    short.workingDirectory=os.getcwd()
    #ショートカットファイルを作成する
    short.Save()

    autoexecwin = tk.Toplevel()
    autoexecwin.title("自動実行設定")
    autoexecwin.geometry("400x100")
    autoexecwin.resizable(False, False)
    autoexeclabel = tk.Label(autoexecwin, text="Windows起動時に自動起動するよう設定しました。\n自動起動を止めたい場合はWindowsのスタートアップフォルダから\n「VJN」ファイルを削除して下さい。").pack()
    acceptbtn = tk.Button(autoexecwin, text="OK", command=autoexecwin.destroy).pack()
    autoexecwin.focus_set()

def main(lastline): #メイン関数
    senddatas = queue.Queue()
    xsdata = []
    joindata = ""
    if config["no_notifysusr"]:
        deleteusrs = config["no_notifysusr"].split(",")
    with open(findnewvrclog(), encoding="utf-8") as f: #ログファイルをリストで読み込み
        lines = f.readlines()
    endlines = len(lines) - 1 #最新の行までの行数
    newlines = lines[lastline:]
    for line in newlines:
        count = line.find("[Behaviour] OnPlayerJoined")
        worldcheck = line.find("[Behaviour] Entering Room")
        if config["separateworld"] and worldcheck != -1:
            logview.configure(state='normal')
            logview.insert('end', "ワールド移動:" + line[61:])
            logview.see("end")
            logview.configure(state='disabled')
            writejoinlog("ワールド移動:" + line[61:])
        if count != -1:
            qdata = (line[60:] + ",").replace("\n", "")
            xsdata.append((line[60:]).replace("\n", "")) #XSOverlayに送信するデータをリストに追加
            senddatas.put(qdata)
            joindata = line[:19] + " Join"
        if line.find("[Behaviour] OnPlayerLeft") != -1:
            logview.configure(state='normal')
            logview.insert('end', line[:19] + " Leave:" + line[59:])
            logview.see("end")
            logview.configure(state='disabled')
            writejoinlog(line[:19] + " Leave:" + line[59:])
    if joindata:
        joinlog = ""
        while not senddatas.empty():
            joinlog = joinlog + senddatas.get()
        final_string = joindata + joinlog.rstrip(",") + "\n"
        if config["sendxsoverlay"]:
            for i in deleteusrs: #ブラックリストにあるユーザーを削除
                if " " + i in xsdata:
                    xsdata.remove(" " + i)
            xsoverlaysenddata = ",".join(xsdata)
            xsoverlaysenddata = xsoverlaysenddata.strip()
            if xsoverlaysenddata:
                sendtoxsoverlay(xsoverlaysenddata)
        logview.configure(state='normal')
        logview.insert('end', final_string)
        logview.see("end")
        logview.configure(state='disabled')
        if config["writelog"]:
            writejoinlog(final_string)
    root.after(config["updinterval"], main, endlines) #メイン関数を再帰的に呼び出し


appversion = "1.0.2" #アプリのバージョンを設定する

loadsettings()

#GUI設定
root = tk.Tk()
if config["startnowindow"]:
    root.withdraw()
root.title("VRChat Join通知システム Ver{}".format(appversion))
root.geometry("800x500")
root.iconbitmap(resource_path("icon.ico"))
if config["tasktray"]:
    root.protocol('WM_DELETE_WINDOW', lambda:root.withdraw()) #ウィンドウを閉じた際ウィンドウを非表示にする
    threading.Thread(target=thread_st).start()

#メニューバー
menubar = tk.Menu(root)
root.config(menu=menubar)
menucfg = tk.Menu(root, tearoff=0)
menubar.add_cascade(label="設定", menu=menucfg)
menubar.add_cascade(label="このアプリについて", command=createaboutapp)
menucfg.add_command(label="環境設定", command=createsettingwin)
menucfg.add_command(label="通知除外設定", command=createblacklistwin)
menucfg.add_command(label="自動起動設定", command=autoexecwin)
menucfg.add_separator()
menucfg.add_command(label="終了", command=lambda: root.after(1, thread_quit))


#上部ロゴテキスト
logolabel = tk.Label(root, text="VRChat Join通知システム", font=("メイリオ", "20")).grid(row=0, column=0)

#テキストエリア
scrollbar_text = tk.Scrollbar(orient="vertical") #スクロールバー
logview = tk.Text(root, yscrollcommand=scrollbar_text.set, font=("メイリオ", "13")) #Joinログ表示用テキスト
logview.grid(column=0, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))
scrollbar_text.config(command=logview.yview)
scrollbar_text.grid(column=1, row=1, sticky=(tk.N, tk.S, tk.E, tk.W))

#ウィンドウのgrid設定
root.columnconfigure(0, weight=1)
root.rowconfigure(1, weight=1)

with open(findnewvrclog(), encoding="utf-8") as f: #ログファイルをリストで読み込み
    lines = f.readlines()

if config["restorelogs"] and os.path.exists(".\\vrcjoinlog.txt"): #Joinログを.txtファイルから読み込み、テキストエリアに表示
    with open(".\\vrcjoinlog.txt", "r", encoding="utf-8") as f:
        oldlog = f.read()
        logview.configure(state='normal')
        logview.insert('end', oldlog)
        logview.see("end")
        logview.configure(state='disabled')

main(len(lines) - 1)

root.mainloop()