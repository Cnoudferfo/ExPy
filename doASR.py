import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU
import pyaudio as pa
import tkinter as tk
from tkinter import ttk
import tkinterDnD as tkdnd

class UI_app(tkdnd.Tk):
    def config(self):
        cwd = os.path.dirname(os.path.abspath(__file__))
        jsonpath = f"{cwd}\\config_asr.json"
        myconfig = MyU.load_config(jsonpath)
        dic = myconfig.get('audio', {})
        self.samplRate = int(dic['sampling rate'])
        self.chunkSize = int(dic['chunk size'])
        dic = myconfig.get('mic', {})
        self.micThresh = int(dic['threshold in dB'])
        self.savePath = myconfig.get('save path')

    def __init__(self, title):
        super().__init__()
        self.title(title)
        self.config()
        s = ttk.Style()
        s.configure('.', font=('Helvetica', 12))
        s.configure('TMenubutton', padx=10, pady=10)
        nb = ttk.Notebook(self)
        f1 = ttk.Frame(nb)
        f2 = ttk.Frame(nb)
        nb.add(f1, text='Mic')
        nb.add(f2, text='File')
        nb.pack(anchor='nw')
        btn = tk.Button(f1, text='Quit', command=self.onQuit)
        btn.pack()
        self.mainloop()

    def onQuit(self):
        pass

if __name__ == '__main__':
    app = UI_app(title='ASR')