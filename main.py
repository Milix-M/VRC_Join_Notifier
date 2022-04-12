import os
import tkinter as tk
import queue
import threading

import module.logic as logic #内部処理の関数が定義されたモジュール
import module.gui as gui #GUIの為の関数が定義されたモジュール
from module.v import *

def main(lastline): #メイン関数
    senddatas = queue.Queue()
    xsdata = []
    joindata = ""
    if logic.config["no_notifysusr"]:
        deleteusrs = logic.config["no_notifysusr"].split(",")
    with open(logic.findnewvrclog(), encoding="utf-8") as f: #ログファイルをリストで読み込み
        lines = f.readlines()
    endlines = len(lines) - 1 #最新の行までの行数
    newlines = lines[lastline:]
    for line in newlines:
        count = line.find("[Behaviour] OnPlayerJoined")
        worldcheck = line.find("[Behaviour] Entering Room")
        if logic.config["separateworld"] and worldcheck != -1:
            logview.configure(state='normal')
            logview.insert('end', "ワールド移動:" + line[61:])
            logview.see("end")
            logview.configure(state='disabled')
            logic.writejoinlog("ワールド移動:" + line[61:])
        if count != -1:
            qdata = (line[60:] + ",").replace("\n", "")
            xsdata.append((line[60:]).replace("\n", "")) #XSOverlayに送信するデータをリストに追加
            senddatas.put(qdata)
            joindata = line[:19] + " Join"
    if joindata:
        joinlog = ""
        while not senddatas.empty():
            joinlog = joinlog + senddatas.get()
        final_string = joindata + joinlog.rstrip(",") + "\n"
        if logic.config["sendxsoverlay"]:
            for i in deleteusrs: #ブラックリストにあるユーザーを削除
                if " " + i in xsdata:
                    xsdata.remove(" " + i)
            xsoverlaysenddata = ",".join(xsdata)
            xsoverlaysenddata = xsoverlaysenddata.strip()
            if xsoverlaysenddata:
                logic.sendtoxsoverlay(xsoverlaysenddata)
        logview.configure(state='normal')
        logview.insert('end', final_string)
        logview.see("end")
        logview.configure(state='disabled')
        if logic.config["writelog"]:
            logic.writejoinlog(final_string)
    root.after(logic.config["updinterval"], main, endlines) #メイン関数を再帰的に呼び出し

logic.loadsettings() #設定を読み込む

#GUI設定
root = tk.Tk()
if logic.config["startnowindow"]:
    root.withdraw()
root.title("VRChat Join通知システム Ver{}".format(appversion))
root.geometry("800x500")
root.iconbitmap(logic.resource_path("icon.ico"))
if logic.config["tasktray"]:
    root.protocol('WM_DELETE_WINDOW', lambda:root.withdraw()) #ウィンドウを閉じた際ウィンドウを非表示にする
    threading.Thread(target=gui.thread_st).start()

#メニューバー
menubar = tk.Menu(root)
root.config(menu=menubar)
menucfg = tk.Menu(root, tearoff=0)
menubar.add_cascade(label="設定", menu=menucfg)
menubar.add_cascade(label="このアプリについて", command=gui.createaboutapp)
menucfg.add_command(label="環境設定", command=gui.createsettingwin)
menucfg.add_command(label="通知除外設定", command=gui.createblacklistwin)
menucfg.add_command(label="自動起動設定", command=gui.autoexecwin)
menucfg.add_separator()
menucfg.add_command(label="終了", command=lambda: root.after(1, gui.thread_quit))


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

with open(logic.findnewvrclog(), encoding="utf-8") as f: #ログファイルをリストで読み込み
    lines = f.readlines()

if logic.config["restorelogs"] and os.path.exists(".\\vrcjoinlog.txt"): #Joinログを.txtファイルから読み込み、テキストエリアに表示
    with open(".\\vrcjoinlog.txt", "r", encoding="utf-8") as f:
        oldlog = f.read()
        logview.configure(state='normal')
        logview.insert('end', oldlog)
        logview.see("end")
        logview.configure(state='disabled')

main(len(lines) - 1)

root.mainloop()