from obswebsocket import obsws, requests
import tkinter as tk
from functools import partial
from tkinter import ttk
import json
import sys

class ComboboxSampleVariableOption(ttk.Frame):
    def __init__(self, master,Scene):
        super().__init__(master)
        self.variable = tk.StringVar()
        self.create_widgets(Scene)
        self.pack(fill = 'both')

    def create_widgets(self,Scene):
        valuelist = Scene.ScenesNames
        self.combo = ttk.Combobox(self,values=valuelist,textvariable=self.variable,state="readonly")
        self.combo.pack(padx=20, side = 'left')
        button1 = ttk.Button(self,text="シーン切り替え",command=self.sceneSwitch)
        button1.pack(fill = 'x', padx=20, side = 'left')
    def sceneSwitch(self):
        print(self.variable.get())
        ws.call(requests.SetCurrentScene(self.variable.get()))
    def changeBox(self,Names):
        self.combo.config(values=Names)

class ScenesManager():
    def __init__(self):
        self.getScenes()        
    def getScenes(self):
        self.scenes = ws.call(requests.GetSceneList())
        self.ScenesNames = []
        for s in self.scenes.getScenes():
            name = s["name"]
            self.ScenesNames.append(name)
    def allBoxLoad(self,sceneSwitchWidgets):
        self.getScenes()
        for widget in sceneSwitchWidgets:
            widget.changeBox(self.ScenesNames)

def sceneReload():
    button2 = ttk.Button(master,text="シーン情報更新",command=partial(scene.allBoxLoad,sceneSwitchWidgets))
    button2.pack(fill = 'x', padx=20, side = 'left')

if __name__ == '__main__':

    master = tk.Tk()
    master.title("OBSSceneChanger")
    master.geometry("350x200")
    iconfile = "OBSScene.ico"
    master.iconbitmap(default=iconfile)
    
    config_file = "myconfig.json"
    try:
        with open(config_file, "r") as f:
            tmp = json.load(f)
        host = tmp["host"]
        port = tmp["port"]
        password = tmp["password"]
        sceneSwitchWidgetNum = int(tmp["showSwitch"])
    except:
        lbl_result = tk.Label(master, text="設定ファイルが不正か存在しません。")
        lbl_result.pack()
        master.mainloop()
        sys.exit()

    ws = obsws(host, port, password)

    try:
        ws.connect()
    except:
        lbl_result = tk.Label(master, text="先にOBSを起動してください。")
        lbl_result2 = tk.Label(master, text="またはパスワード、ポート番号、ホストに間違いがあります。")
        lbl_result.pack()
        lbl_result2.pack()
        master.mainloop()
        sys.exit()

    scene = ScenesManager() 
    sceneSwitchWidgets = []
    for num in range(sceneSwitchWidgetNum):
        sceneSwitchWidgets.append(ComboboxSampleVariableOption(master,scene))
    sceneReload()
    master.mainloop()
    ws.disconnect()
    sys.exit()

