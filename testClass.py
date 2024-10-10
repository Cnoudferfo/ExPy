import tkinter as tk
from tkinter import ttk
import tkinterDnD as tkdnd
import time as tm
import threading as th

class button(tk.Button):
    def __init__(self, parent, text, command):
        super().__init__(parent, text=text, command=command)

class progressbar(ttk.Progressbar):
    def __init__(self, parent, ori, lnth, md, max):
        super().__init__(master=parent, orient=ori, length=lnth, mode=md, maximum=max)

class popup(tk.Toplevel):
    def __init__(self, parent, geom):
        super().__init__(parent, borderwidth=2, background='lightblue')
        self.geometry(geom)
        self.overrideredirect(True)
        self.progbar=progressbar(self, ori="horizontal", lnth=100, md='determinate', max=10)
        self.progbar.pack(expand=True, fill='x', pady=10)

class root(tkdnd.Tk):
    def __init__(self, title, geom):
        super().__init__()
        self.title(title)
        self.geometry(geom)
        self.btn1 = button(self, text="To Popup", command=self.popup)
        self.btn1.pack(pady=10)
        self.pop = None
        self.the_t = None
        self.mainloop()

    def popup(self):
        x = self.winfo_rootx()
        y = self.winfo_rooty()
        self.pop = popup(self,f"300x200+{x+50}+{y+50}")
        self.the_t = th.Thread(target=self.the_proc)
        self.the_t.start()
    def the_proc(self):
        for i in range(10):
            print(f"i={i}")
            tm.sleep(1)
            self.pop.progbar['value'] = i+1
            self.pop.update()
        # pb.stop()
        tm.sleep(1)
        self.pop.destroy()

app = root(title="Class", geom="300x200")
