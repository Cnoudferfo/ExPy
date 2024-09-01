import tkinter as tk
from tkinter import font
import os
import os.path
from pathlib import Path
import json

save_path = "../"
config_file = "config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        save_path = config.get("save_path", "")

paths = Path(save_path).glob('*.*')
# for p in paths:
#     print(f"p={p.name}")

root = tk.Tk()
root.title('tkLabo')
root.geometry('400x400')

# Create a canvas and a scrollbar
canvas = tk.Canvas(root)
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas.yview)
scrollbar.pack(side='right', fill='y')
canvas.pack(side='left', fill='both', expand=True)

# Create a main frame inside the canvas
main_frame = tk.Frame(canvas)
canvas.create_window((0, 0), window=main_frame, anchor='nw')

# Define font size and calculate padding
label_font = font.Font(family="Helvetica", size=10)
line_height = label_font.metrics("linespace")
padding = line_height // 8

# Add labels to the frame
texts = [f"-{p.name}" for p in paths]
labels = [tk.Label(main_frame, text=t, font=label_font, anchor='w') for t in texts]
def lcommand(evnt):
    print(f"Label clicked {evnt}")
    labels.pop(len(labels)-1).destroy()
for label in labels:
    label.pack(pady=(padding, 0), anchor='nw')
    label.bind("<Button-1>", lcommand)

# Configure the canvas and frame to work with the scrollbar
main_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)

# Update the scroll region when the frame size changes
def on_frame_configure(event):
    canvas.config(scrollregion=canvas.bbox("all"))

main_frame.bind("<Configure>", on_frame_configure)

root.mainloop()
