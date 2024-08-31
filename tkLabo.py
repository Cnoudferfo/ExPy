import tkinter as tk
from tkinter import font

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
texts = [f"Text {i}" for i in range(100)]
for text in texts:
    label = tk.Label(main_frame, text=text, font=label_font)
    label.pack(pady=(padding, 0))

# Configure the canvas and frame to work with the scrollbar
main_frame.update_idletasks()
canvas.config(scrollregion=canvas.bbox("all"), yscrollcommand=scrollbar.set)

# Update the scroll region when the frame size changes
def on_frame_configure(event):
    canvas.config(scrollregion=canvas.bbox("all"))

main_frame.bind("<Configure>", on_frame_configure)

root.mainloop()
