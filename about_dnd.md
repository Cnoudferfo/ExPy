```The above code had a problem. A draged email turn to a forbidden sign above the drop area. How to resolve?
Copilot
正在為您產生解答…

由 Copilot 傳送:
It looks like the issue might be related to the way the drag-and-drop event is being handled. Let’s make sure the tkinterdnd2 library is correctly set up to accept the dragged email. Here are a few adjustments to help resolve the issue:```

- Step 1: Ensure Correct Import and Initialization
Make sure you are importing and initializing tkinterdnd2 correctly:

```Python
import os
import tkinter as tk
from tkinterdnd2 import TkinterDnD, DND_FILES
import win32com.client
import pickle
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
- Step 2: Update the Drop Area Configuration
Ensure the drop area is correctly configured to accept files:

```Python

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
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
- Step 3: Verify Drag-and-Drop Handling
Ensure the drag-and-drop event is correctly handled:

```Python

def drop(self, event):
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    data = event.data.strip('{}')  # This will contain the dragged email data
    msg = outlook.OpenSharedItem(data)

    for attachment in msg.Attachments:
        attachment.SaveAsFile(os.path.join(self.save_path.get(), attachment.FileName))
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
- Additional Tips
Check File Permissions: Ensure the directory where you are saving the attachments has the correct permissions.
Debugging: Add print statements to debug and ensure the drop event is being triggered correctly.
If the issue persists, it might be helpful to check the documentation or examples provided by the tkinterdnd2 library12. Let me know if you need further assistance!

1: https://github.com/pmgagne/tkinterdnd2 2: https://github.com/TomSchimansky/CustomTkinter/discussions/470
