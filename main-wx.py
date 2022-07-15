import webbrowser
import glob
import os
import sys
import json
import tkinter as tk
from socket import socket, AF_INET, SOCK_DGRAM
import queue
import threading
from numpy import save
import pystray
from pystray import Icon, Menu, MenuItem
from PIL import Image
import comtypes.client
import pathlib
#wxpython
import wx
import wx.adv

class MyFrame(wx.Frame):
    def __init__(self, *args, **kwds):
        loadsettings()
        # begin wxGlade: MyFrame.__init__
        kwds["style"] = kwds.get("style", 0) | wx.DEFAULT_FRAME_STYLE
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((865, 548))
        self.SetTitle(u"VRChat Join通知システム")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))


        # Menu Bar
        self.frame_menubar = wx.MenuBar()
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(1, u"環境設定", "")
        wxglade_tmp_menu.Append(2, u"通知除外設定", "")
        wxglade_tmp_menu.Append(3, u"自動起動設定", "")
        wxglade_tmp_menu.AppendSeparator()
        wxglade_tmp_menu.Append(4, u"終了", "")
        self.frame_menubar.Append(wxglade_tmp_menu, u"設定")
        wxglade_tmp_menu = wx.Menu()
        wxglade_tmp_menu.Append(5, u"バージョン情報", "")
        wxglade_tmp_menu.Append(6, "Booth", "")
        wxglade_tmp_menu.Append(7, u"作者Twitter", "")
        self.frame_menubar.Append(wxglade_tmp_menu, u"このアプリについて")
        self.SetMenuBar(self.frame_menubar)
        self.Bind(wx.EVT_MENU, self.on_menu_click)
        # Menu Bar end

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_3, 1, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, u"VRChat Join通知システム", style=wx.ST_ELLIPSIZE_END)
        label_1.SetMinSize((-1, 45))
        label_1.SetFont(wx.Font(20, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "", style=wx.BORDER_NONE | wx.TE_MULTILINE | wx.TE_READONLY)
        self.text_ctrl_1.SetFont(wx.Font(13, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(self.text_ctrl_1, 1, wx.EXPAND, 0)

        if config["restorelogs"] and os.path.exists(".\\vrcjoinlog.txt"): #Joinログを.txtファイルから読み込み、テキストエリアに表示
            with open(".\\vrcjoinlog.txt", "r", encoding="utf-8") as f:
                oldlog = f.read()
                self.text_ctrl_1.SetValue(oldlog)
                self.text_ctrl_1.SetInsertionPointEnd()
                self.text_ctrl_1.ShowPosition(self.text_ctrl_1.GetLastPosition())

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        # end wxGlade

        self.timer = wx.Timer(self)
        self.Bind(wx.EVT_TIMER, lambda x: main(endlines))
        self.timer.Start(int(config["updinterval"]))

    def on_menu_click(self, event): #メニュークリック時の処理
        if event.GetId() == 1:
            settings_window = MyFrame1(None, wx.ID_ANY, "")
            settings_window.Show(True)
        elif event.GetId() == 2:
            no_notify_window = MyFrame3(None, wx.ID_ANY, "")
            no_notify_window.Show(True)
        elif event.GetId() == 3:
            pass
        elif event.GetId() == 4:
            exit()
        elif event.GetId() == 5:
            about_app = MyFrame2(None, wx.ID_ANY, "")
            about_app.Show(True)
        elif event.GetId() == 6:
            webbrowser.open_new("https://reoshop.booth.pm/items/3757293")
        elif event.GetId() == 7:
            webbrowser.open_new("https://twitter.com/ReoSteldam")

# end of class MyFrame

class MyFrame1(wx.Frame):
    def __init__(self, *args, **kwds):
        loadsettings()
        # begin wxGlade: MyFrame1.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((575, 364))
        self.SetTitle(u"環境設定")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        grid_sizer_1 = wx.GridSizer(8, 2, 0, 0)
        sizer_1.Add(grid_sizer_1, 1, wx.EXPAND, 0)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        grid_sizer_1.Add(self.text_ctrl_1, 0, wx.ALL, 5)
        self.text_ctrl_1.SetValue(str(config["updinterval"]))

        label_11 = wx.StaticText(self.panel_1, wx.ID_ANY, u"ログ更新間隔(ms)")
        grid_sizer_1.Add(label_11, 0, wx.ALL, 5)

        self.checkbox_7 = wx.CheckBox(self.panel_1, wx.ID_ANY, u"XSOvelayでログを表示")
        grid_sizer_1.Add(self.checkbox_7, 0, wx.ALL, 5)
        self.checkbox_7.SetValue(config["sendxsoverlay"])

        label_8 = wx.StaticText(self.panel_1, wx.ID_ANY, u"XSOverlayの機能を使用して\nログをオーバーレイ表示します")
        grid_sizer_1.Add(label_8, 0, wx.ALL, 5)

        self.checkbox_8 = wx.CheckBox(self.panel_1, wx.ID_ANY, u"ログをバックアップ")
        grid_sizer_1.Add(self.checkbox_8, 0, wx.ALL, 5)
        self.checkbox_8.SetValue(config["writelog"])

        label_9 = wx.StaticText(self.panel_1, wx.ID_ANY, u".txt形式でログをバックアップします")
        grid_sizer_1.Add(label_9, 0, wx.ALL, 5)

        self.checkbox_9 = wx.CheckBox(self.panel_1, wx.ID_ANY, u"起動時にログを復元する")
        grid_sizer_1.Add(self.checkbox_9, 0, wx.ALL, 5)
        self.checkbox_9.SetValue(config["restorelogs"])

        label_10 = wx.StaticText(self.panel_1, wx.ID_ANY, u"起動時にバックアップファイルを使用してログを復元します\nログバックアップの有効化が必要です")
        grid_sizer_1.Add(label_10, 0, wx.ALL, 5)

        self.checkbox_10 = wx.CheckBox(self.panel_1, wx.ID_ANY, u"ワールド移動時にログを区切る")
        grid_sizer_1.Add(self.checkbox_10, 0, wx.ALL, 5)
        self.checkbox_10.SetValue(config["separateworld"])

        label_12 = wx.StaticText(self.panel_1, wx.ID_ANY, u"ワールド移動時にログに区切りを挿入します。")
        grid_sizer_1.Add(label_12, 0, wx.ALL, 5)

        self.checkbox_11 = wx.CheckBox(self.panel_1, wx.ID_ANY, u"タスクトレイに最小化")
        grid_sizer_1.Add(self.checkbox_11, 0, wx.ALL, 5)
        self.checkbox_11.SetValue(config["tasktray"])

        label_13 = wx.StaticText(self.panel_1, wx.ID_ANY, u"ウィンドウを閉じた時にタスクトレイに最小化します")
        grid_sizer_1.Add(label_13, 0, wx.ALL, 5)

        self.checkbox_12 = wx.CheckBox(self.panel_1, wx.ID_ANY, u"最小化した状態で起動")
        grid_sizer_1.Add(self.checkbox_12, 0, wx.ALL, 5)
        self.checkbox_12.SetValue(config["startnowindow"])

        label_14 = wx.StaticText(self.panel_1, wx.ID_ANY, u"タスクトレイに最小化した状態でアプリを起動します")
        grid_sizer_1.Add(label_14, 0, wx.ALL, 5)

        self.checkbox_13 = wx.CheckBox(self.panel_1, wx.ID_ANY, u"Leaveログを表示する")
        grid_sizer_1.Add(self.checkbox_13, 0, wx.ALL, 5)
        self.checkbox_13.SetValue(config["leave"])

        label_15 = wx.StaticText(self.panel_1, wx.ID_ANY, u"Leaveログを表示します。")
        grid_sizer_1.Add(label_15, 0, wx.ALL, 5)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, u"保存")
        sizer_1.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM | wx.LEFT | wx.RIGHT, 5)
        self.button_1.Bind(wx.EVT_BUTTON, lambda x:[self.writesettings(self.text_ctrl_1.GetValue(), self.checkbox_7.GetValue(), self.checkbox_8.GetValue(), self.checkbox_9.GetValue(), self.checkbox_10.GetValue(), self.checkbox_11.GetValue(), self.checkbox_12.GetValue(), self.checkbox_13.GetValue()), self.Destroy()])

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        # end wxGlade

    def writesettings(self, text_ctrl_1, checkbox_7, checkbox_8, checkbox_9, checkbox_10, checkbox_11, checkbox_12, checkbox_13): #設定を書き込む関数
        config["updinterval"] = text_ctrl_1
        config["sendxsoverlay"] = checkbox_7
        config["writelog"] = checkbox_8
        config["restorelogs"] = checkbox_9
        config["separateworld"] = checkbox_10
        config["tasktray"] = checkbox_11
        config["startnowindow"] = checkbox_12
        config["leave"] = checkbox_13
        with open("config.json", "w") as f:
            json.dump(config, f, indent=2)
        loadsettings() #設定を再読み込み

# end of class MyFrame1

class MyFrame2(wx.Frame):
    def __init__(self, *args, **kwds):
        # begin wxGlade: MyFrame2.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLOSE_BOX
        wx.Frame.__init__(self, *args, **kwds)
        self.SetSize((250, 130))
        self.SetTitle(u"このアプリについて")
        self.SetBackgroundColour(wx.Colour(255, 255, 255))

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 0, wx.EXPAND, 0)

        sizer_3 = wx.BoxSizer(wx.VERTICAL)
        sizer_2.Add(sizer_3, 0, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, u"VRChat Join通知システム")
        label_1.SetFont(wx.Font(14, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        label_2 = wx.StaticText(self.panel_1, wx.ID_ANY, "Ver: " + appversion)
        label_2.SetFont(wx.Font(10, wx.FONTFAMILY_DEFAULT, wx.FONTSTYLE_NORMAL, wx.FONTWEIGHT_NORMAL, 0, "Yu Gothic UI"))
        sizer_3.Add(label_2, 0, wx.ALIGN_CENTER_HORIZONTAL, 0)

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, "OK")
        sizer_3.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 10)
        self.button_1.Bind(wx.EVT_BUTTON, self.close_about_window)

        self.panel_1.SetSizer(sizer_1)

        self.Layout()
        # end wxGlade

    def close_about_window(self, event):
        self.Destroy()

# end of class MyFrame2

class MyFrame3(wx.Frame):
    def __init__(self, *args, **kwds):
        loadsettings()
        # begin wxGlade: MyFrame3.__init__
        kwds["style"] = kwds.get("style", 0) | wx.CAPTION | wx.CLIP_CHILDREN | wx.CLOSE_BOX | wx.SYSTEM_MENU
        wx.Frame.__init__(self, *args, **kwds)
        self.SetTitle("frame_3")

        self.panel_1 = wx.Panel(self, wx.ID_ANY)

        sizer_1 = wx.BoxSizer(wx.VERTICAL)

        sizer_2 = wx.BoxSizer(wx.VERTICAL)
        sizer_1.Add(sizer_2, 1, wx.EXPAND, 0)

        label_1 = wx.StaticText(self.panel_1, wx.ID_ANY, u"XSOverlayで通知しないユーザーをカンマ区切りで入力")
        sizer_2.Add(label_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)

        self.text_ctrl_1 = wx.TextCtrl(self.panel_1, wx.ID_ANY, "")
        sizer_2.Add(self.text_ctrl_1, 0, wx.ALL | wx.EXPAND, 5)
        self.text_ctrl_1.SetValue(config["no_notifysusr"])

        self.button_1 = wx.Button(self.panel_1, wx.ID_ANY, u"保存")
        sizer_2.Add(self.button_1, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.ALL, 5)
        self.button_1.Bind(wx.EVT_BUTTON, lambda x:[self.savenonofityusr(self.text_ctrl_1.GetValue()), self.Destroy()])

        self.panel_1.SetSizer(sizer_1)

        sizer_1.Fit(self)
        self.Layout()
        # end wxGlade
    def savenonofityusr(self, nonotifyusr): #通知を行わないユーザをファイルに保存する関数
        with open("config.json", "w") as f:
            config["no_notifysusr"] = nonotifyusr
            json.dump(config, f, indent=2)
        loadsettings()

# end of class MyFrame3


class MyApp(wx.App):
    def OnInit(self):
        self.frame = MyFrame(None, wx.ID_ANY, "")
        self.SetTopWindow(self.frame)
        self.frame.Show()
        return True

# end of class MyApp

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

def findnewvrclog(): #最新のVRCログファイルを取得する関数
    files = glob.glob(os.getenv('LOCALAPPDATA') + 'Low\\VRChat\\VRChat\\*.txt')
    logs = {}
    for file in files:
        logs[file] = os.stat(file)
    logs = sorted(logs.items(), key=lambda x: x[1].st_mtime, reverse=True)
    return logs[0][0]

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

def writejoinlog(writedata): #Joinログを.txtファイルに書き出す関数
    if os.path.exists('.\\vrcjoinlog.txt'):
        with open(".\\vrcjoinlog.txt", "a", encoding="utf-8") as f:
            f.write(writedata)
    else:
        with open(".\\vrcjoinlog.txt", "x", encoding="utf-8") as f:
            f.write(writedata)

appversion = "1.2" #アプリのバージョンを設定する

if __name__ == "__main__":
    app = MyApp(0)
    logview = MyFrame(None, wx.ID_ANY, "")
    def main(lastline): #メイン関数
        global endlines
        senddatas = queue.Queue()
        lsenddatas = queue.Queue()
        xsdata = []
        joindata = ""
        leavedata = ""
        if config["no_notifysusr"]:
            deleteusrs = config["no_notifysusr"].split(",")
        else:
            deleteusrs = []
        with open(findnewvrclog(), encoding="utf-8") as f: #ログファイルをリストで読み込み
            lines = f.readlines()
        endlines = len(lines) - 1 #最新の行までの行数
        newlines = lines[lastline:]
        for line in newlines:
            count = line.find("[Behaviour] OnPlayerJoined")
            worldcheck = line.find("[Behaviour] Entering Room")
            if config["separateworld"] and worldcheck != -1:
                logview.text_ctrl_1.AppendText("ワールド移動:" + line[61:])
                writejoinlog("ワールド移動:" + line[61:])
                pass
            if count != -1:
                qdata = (line[60:] + ",").replace("\n", "")
                xsdata.append((line[60:]).replace("\n", "")) #XSOverlayに送信するデータをリストに追加
                senddatas.put(qdata)
                joindata = line[:19] + " Join"
            if config["leave"] and line.find("[Behaviour] OnPlayerLeft ") != -1:
                qldata = (line[58:] + ",").replace("\n", "")
                leavedata = line[:19] + " Leave"
                lsenddatas.put(qldata)
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
            logview.text_ctrl_1.AppendText(final_string)
            if config["writelog"]:
                writejoinlog(final_string)
        if leavedata:
            leavelog = ""
            while not lsenddatas.empty():
                leavelog = leavelog + lsenddatas.get()
            lfinal_string = leavedata + leavelog.rstrip(",") + "\n"
            logview.text_ctrl_1.AppendText(lfinal_string)
            if config["writelog"]:
                writejoinlog(lfinal_string)

    loadsettings()

    with open(findnewvrclog(), encoding="utf-8") as f: #ログファイルをリストで読み込み
        lines = f.readlines()

    main(len(lines) - 1)

    app.MainLoop()
    logview.Destroy()