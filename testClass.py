import os
import sys
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinterDnD as tkdnd
import time as tm
import threading as th

class app(tkdnd.Tk):
    text=''
    integer = 5150
    def __init__(self, title, geom):
        cwd = os.path.dirname(os.path.abspath(__file__))
        print(f"cwd={cwd}")
        super().__init__()
        self.title(title)
        self.geometry(geom)
        self.lbl = ui_label(parent=self)
        self.btn1 = ui_button(self, text="To Popup", command=self.to_popup)
        self.pop = None
        self.the_t = None
        self.text = title
        self.mainloop()

    def to_popup(self):
        self.pop = ui_popup(self)

class ui_button(tk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent, text=f"{parent}:{text}", command=command)
        self.pack(pady=10, padx=10)

class ui_label(ttk.Label):
    def __init__(self, parent):
        self.strVar = tk.StringVar(value='LABEL')
        super().__init__(master=parent,\
                         textvariable=self.strVar)
        self.pack(pady=10, padx=10, fill='both', expand=True)
        self.register_drop_target("*")
        self.bind("<<Drop>>", self.on_drop)
    def on_drop(self, event):
        self.strVar.set(value=f"{self.master.integer}:{event.data}")

class ui_popup(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent, border=1, borderwidth=2)
        x = parent.winfo_rootx()
        y = parent.winfo_rooty()
        self.geometry(f"300x200+{x+50}+{y+50}")
        # self.overrideredirect(True)
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.frame = tk.Frame(self, border=1, borderwidth=10, padx=5, pady=5)
        self.frame.pack(fill='both', expand=True)
        self.text = parent.text
        self.progbar=ui_progressbar(self.frame, ori="horizontal", lnth=100, md='determinate', max=10)
        self.progbar.pack(expand=True, fill='x', pady=10)
        self.strVar = tk.StringVar(self.frame, value=f"Progress 0/{self.progbar.cget(key='maximum')}")
        self.lbl = tk.Label(self.frame, textvariable=self.strVar)
        self.lbl.pack(fill='both', expand=True, padx=10, pady=10)
        self.btn = tk.Button(self.frame,text="Abort", command=self.to_stop_t)
        self.btn.pack()
        self.the_t = th.Thread(target=lambda: self.the_proc(text='ARGS'))
        self.let_t_go = True
        self.the_t.start()
    def the_proc(self, text):
        for i in range(10):
            print(f"i={i}")
            tm.sleep(1.0)
            self.progbar.config(value = i+1)
            self.strVar.set(value=f"{self.text}:{text}: Progress: {i+1}/{self.progbar.cget(key='maximum')}.")
            self.update()
            if not self.let_t_go:
                self.strVar.set(value=f"{text}: Abort, breaking...")
                tm.sleep(1.0)
                break
        # pb.stop()
        self.strVar.set(value=f"{text}: Finished.")
        tm.sleep(1)
        self.destroy()
    def to_stop_t(self):
        self.let_t_go = False
        # self.the_t.join()
        print("Thread finished.")

    def on_closing(self):
        if messagebox.askokcancel("Abort", "Confirm again!"):
            self.to_stop_t()

class ui_progressbar(ttk.Progressbar):
    def __init__(self, parent, ori, lnth, md, max):
        super().__init__(master=parent, orient=ori, length=lnth, mode=md, maximum=max)

app = app(title="Class", geom="300x200")