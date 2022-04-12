import webbrowser
import os
import sys
import tkinter as tk
import pystray
from pystray import Icon, Menu, MenuItem
from PIL import Image
import comtypes.client
import pathlib
import module.logic as logic
from module.v import *

def thread_st(): #スレッドの開始をする関数
    global icon
    global root
    options_map = {'表示': lambda:[root.after(0,root.deiconify)], '終了': lambda: root.after(1, thread_quit)}
    items = []
    for option, callback in options_map.items():
        items.append(MenuItem(option, callback, default=True if option == 'Show' else False))
    menu = Menu(*items)
    image = Image.open(logic.resource_path("icon.ico"))
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
    aboutapp.geometry("300x100")
    appname = tk.Label(aboutapp, text="VRChat Join通知システム", font=("メイリオ", 12)).pack()
    verlabel = tk.Label(aboutapp, text="Ver:{}".format(appversion), font=("メイリオ", 10)).pack()
    repo = tk.Label(aboutapp, text="リポジトリへのリンク", fg="blue")
    repo.pack()
    repo.bind("<Button-1>", lambda e: webbrowser.open_new("https://github.com/Milix-M/VRC_Join_Notifier"))
    author = tk.Label(aboutapp, text="作者:ReoSteldam", fg="blue")
    author.pack()
    author.bind("<Button-1>", lambda e: webbrowser.open_new("https://twitter.com/ReoSteldam"))
    aboutapp.focus_set()


def createsettingwin(): #設定ウィンドウを作成する関数
    settingwin = tk.Toplevel()
    settingwin.title("環境設定")
    settingwin.geometry("300x230")
    updintervallabel = tk.Label(settingwin, text="更新間隔(ms)").pack()
    updinterval = tk.Entry(settingwin, width=10)
    updinterval.insert(0, logic.config["updinterval"])
    updinterval.pack()

    bl = tk.BooleanVar()
    bl.set(logic.config["sendxsoverlay"])
    sendxsovelaychkbox = tk.Checkbutton(settingwin, variable=bl, text="XSOverlayに送信する").pack()

    bl2 = tk.BooleanVar()
    bl2.set(logic.config["writelog"])
    writelogchkbox = tk.Checkbutton(settingwin, variable=bl2, text="Joinログを.txt形式で書き出す").pack()

    bl3 = tk.BooleanVar()
    bl3.set(logic.config["restorelogs"])
    restorelogschkbox = tk.Checkbutton(settingwin, variable=bl3, text="Joinログを.txtファイルから読み込み復元する").pack()

    bl4 = tk.BooleanVar()
    bl4.set(logic.config["separateworld"])
    separateworldchkbox = tk.Checkbutton(settingwin, variable=bl4, text="ワールド移動時にJoinログに区切りを挿入する").pack()

    bl5 = tk.BooleanVar()
    bl5.set(logic.config["tasktray"])
    tasktraychkbox = tk.Checkbutton(settingwin, variable=bl5, text="タスクトレイに最小化").pack()

    bl6 = tk.BooleanVar()
    bl6.set(logic.config["startnowindow"])
    startnowindowchkbox = tk.Checkbutton(settingwin, variable=bl6, text="最小化した状態で起動").pack()

    complatebuttom = tk.Button(settingwin, text="保存", command=lambda:logic.savesettings(updinterval.get(), bl.get(), bl2.get(), bl3.get(), bl4.get(), bl5.get(), bl6.get())).pack()
    settingwin.focus_set()

def createblacklistwin(): #ブラックリストを編集するウィンドウを作成する関数
    blacklistwin = tk.Toplevel()
    blacklistwin.title("通知しないユーザーを編集")
    blacklistwin.geometry("400x100")
    blacklistwin.resizable(False, False)
    nonotifyusrlabel = tk.Label(blacklistwin, text="XSOvelayで通知しないユーザー名をカンマ区切りで入力").pack()
    nonotifyusr = tk.Entry(blacklistwin, width=50)
    logic.loadsettings()
    nonotifyusr.insert(0, logic.config["no_notifysusr"])
    nonotifyusr.pack()
    editcompletebtn = tk.Button(blacklistwin, text="保存", command=lambda:logic.savenonofityusr(nonotifyusr.get())).pack()
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