import tkinter as tk
from tkinter import ttk
import time as tm
import threading as th

pop = None
the_t = None
pb = None

def the_proc() -> None:
    global pop
    global pb
    # pb.start()
    for i in range(10):
        print(f"i={i}")
        tm.sleep(1)
        pb['value'] = i+1
        pop.update()
    # pb.stop()
    tm.sleep(1)
    pop.destroy()

def popup() -> None:
    global pop
    global the_t
    global pb
    x = root.winfo_rootx()
    y = root.winfo_rooty()
    pop = tk.Toplevel(root, borderwidth=2, background='lightblue')
    pop.geometry(f"300x200+{x+50}+{y+50}")
    pop.overrideredirect(True)
    pb = ttk.Progressbar(pop, orient="horizontal", length=100, mode='determinate', maximum=10)
    pb.pack(pady=10)
    the_t = th.Thread(target=the_proc)
    the_t.start()

root = tk.Tk()
root.geometry("500x400")
btn = tk.Button(root,text="Pop up", command=popup)
btn.pack(pady=10)
root.mainloop()
if the_t:
    the_t.join()
    print("Thread finished!")