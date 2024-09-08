import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import win32com.client
import pickle

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Email Attachment Saver")

        self.save_path = tk.StringVar()
        self.load_save_path()

        self.path_label = tk.Label(root, text="Save Path:")
        self.path_label.pack()

        self.path_entry = tk.Entry(root, textvariable=self.save_path, width=50)
        self.path_entry.pack()

        self.save_button = tk.Button(root, text="Save Path", command=self.save_save_path)
        self.save_button.pack()

        self.drop_area = tk.Label(root, text="Drag and Drop Email Here", width=50, height=10, bg="lightgrey")
        self.drop_area.pack()
        self.drop_area.drop_target_register(DND_FILES)
        self.drop_area.dnd_bind('<<Drop>>', self.drop)

    def save_save_path(self):
        with open("save_path.pkl", "wb") as f:
            pickle.dump(self.save_path.get(), f)

    def load_save_path(self):
        try:
            with open("save_path.pkl", "rb") as f:
                self.save_path.set(pickle.load(f))
        except FileNotFoundError:
            self.save_path.set("")

    def drop(self, event):
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        data = event.data.strip('{}')  # This will contain the dragged email data
        msg = outlook.OpenSharedItem(data)

        for attachment in msg.Attachments:
            attachment.SaveAsFile(os.path.join(self.save_path.get(), attachment.FileName))

if __name__ == "__main__":
    root = TkinterDnD.Tk()
    app = App(root)
    root.mainloop()
