import tkinter as tk

root = tk.Tk()
root.title('Two Canvases Example')
root.geometry('600x400')

# Create the first canvas with a scrollbar
canvas1 = tk.Canvas(root, bg='lightblue')
scrollbar = tk.Scrollbar(root, orient="vertical", command=canvas1.yview)
scrollbar.pack(side='right', fill='y')
canvas1.pack(side='right', fill='both', expand=True)
canvas1.config(yscrollcommand=scrollbar.set)

# Create a frame inside the first canvas
frame1 = tk.Frame(canvas1)
canvas1.create_window((0, 0), window=frame1, anchor='nw')

# Add some content to the first frame
for i in range(20):
    label = tk.Label(frame1, text=f"Label {i}")
    label.pack(pady=5)

# Update the scroll region when the frame size changes
def on_frame1_configure(event):
    canvas1.config(scrollregion=canvas1.bbox("all"))

frame1.bind("<Configure>", on_frame1_configure)

# Create the second canvas without a scrollbar
canvas2 = tk.Canvas(root, bg='lightgreen')
canvas2.pack(side='left', fill='both', expand=True)

# Add some content to the second canvas
for i in range(10):
    canvas2.create_text(10, 20 + i*20, anchor='nw', text=f"Text {i}")

root.mainloop()
