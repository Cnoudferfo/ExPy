import tkinter as tk
from tkinter import ttk, filedialog
import tkinterDnD
import json
import os
import win32com.client  # Make sure to install pywin32
from datetime import datetime

# Global veriables
_savePath = ""
_configFile = "config.json"
_timeThreshold = 30  # default value
_textWidget = None
_msgVar = None

def setTextWidget(str):
    global _textWidget
    _textWidget.config(state=tk.NORMAL)
    _textWidget.delete(1.0, tk.END)
    _textWidget.insert(tk.END, str)
    _textWidget.config(state=tk.DISABLED)

def insertTextWidget(str):
    global _textWidget
    _textWidget.config(state=tk.NORMAL)
    _textWidget.insert(tk.END, str)
    _textWidget.config(state=tk.DISABLED)

def save_savepath(path=''):
    global _configFile
    with open(_configFile, 'w') as f:
        json.dump({"save_path": path}, f)

def show_msgVar(text=''):
    global _msgVar
    _msgVar.set(text)

def do_dropped_path(path):
    global _savePath
    _savePath = path
    show_msgVar(f"Save path set to: {_savePath}")
    save_savepath(path=_savePath)
    list_files(path=path)

def do_dropped_email(dropped_data,path):
    if not path:
        setTextWidget("Please select a save path first!\n")
        return -1
    dropped_data = dropped_data.split('\n')  # Split to an array of two strings
    if len(dropped_data) < 2:
        setTextWidget("Invalid email data dropped.\n")
        return -1
    dict_head = dropped_data[0].strip().split('\t')
    dict_data = dropped_data[1].strip().split('\t')
    if len(dict_head) != len(dict_data):
        setTextWidget("Mismatch in email data fields.\n")
        return -1
    dd_dict = dict(zip(dict_head, dict_data))
    dd_sender = dd_dict['寄件者']
    dd_subject = dd_dict['主旨']
    dd_locrxt = dd_dict['收到日期'].replace("下午", "PM").replace("上午", "AM")

    loc_parse = datetime.strptime(dd_locrxt, "%Y/%m/%d %p %I:%M")
    dd_date = loc_parse.strftime("%Y-%m-%d")
    dd_time = loc_parse.strftime("%H:%M:%S")
    print(f"Searching for email with Subject: {dd_subject}, From: {dd_sender}, Received: {dd_date} {dd_time}")

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
    messages = inbox.Items
    messages.Sort("[ReceivedTime]", True)

    def time_to_seconds(tm_str):  # Calculate HH*60*60 + MM*60 + SS
        h, m, s = map(int, tm_str.split(':'))
        return h*3600 + m*60 + s

    def str_similarity(str1, str2):
        str1 = str1 + ' '*(len(str2) - len(str1))
        str2 = str2 + ' '*(len(str1) - len(str2))
        return sum(1 if i == j else 0 for i, j in zip(str1, str2)) / float(len(str1))

    i = 0
    for msg in messages:  # Find the email based on the extracted properties
        msg_rxt = msg.ReceivedTime
        msg_date = msg_rxt.strftime("%Y-%m-%d")
        msg_time = msg_rxt.strftime("%H:%M:%S")
        print(f"Checking email: Subject: {msg.Subject}, From: {msg.SenderName}, Received: {msg_date} {msg_time}, Attachment: {msg.Attachments}")
        if(dd_date != msg_date):
            print(f"pass this email, dd_date={dd_date}, msg_date={msg_date}")
            continue
        time_diff = abs(time_to_seconds(dd_time) - time_to_seconds(msg_time))
        if(time_diff > _timeThreshold):
            if i < 500:
                print(f"pass this email, time_diff={time_diff} > threshold:{_timeThreshold}")
                i = i + 1
            else:
                setTextWidget(f"Quit for quick debug! search only in {i} items.")
                break
            continue
        ss_subj = str_similarity(dd_subject, msg.Subject)
        ss_sndr = str_similarity(dd_sender, msg.SenderName)
        if (ss_subj > 0.2 and ss_sndr > 0.2):
            print("Email found")
            if msg.Attachments.Count > 0:
                saved_files = []
                for attachment in msg.Attachments:
                    print(f"Found attachment: {attachment.FileName}")
                    file_path = os.path.join(path, attachment.FileName)

                    # Check file existence
                    base, ext = os.path.splitext(file_path)
                    f_counter = 1
                    while os.path.exists(file_path):
                        p_str1 = f"{file_path} exists,"
                        file_path = f"{base}_{f_counter}{ext}"
                        print(f"{p_str1} try {file_path}")
                        f_counter += 1
                    attachment.SaveAsFile(file_path)
                    saved_files.append(file_path)
                show_msgVar(f"Attachments saved:\n" + "\n".join(saved_files) + "\n")
            else:
                show_msgVar("No attachments found in the email.")
            break
    else:
        setTextWidget("Email not found.")
    list_files(path=_savePath)

def drop(event):  # On dnd's drop event
    global _savePath
    global _configFile
    global _textWidget

    data = event.data.strip()
    if os.path.isdir(data):
        do_dropped_path(path=data)
    else:
        try:
            do_dropped_email(dropped_data=data, path=_savePath)
        except Exception as e:
            setTextWidget(f"Error: {e}")

def browse_path():
    path = filedialog.askdirectory()
    if path:
        save_savepath(path=path)
        show_msgVar(f"Save path set to: {path}")
        list_files(path=path)
    else:
        path = '.\\'
    return path

def list_files(path):
    if not path:
        setTextWidget(str="No save path set.")
        return
    try:
        files = os.listdir(path)
        files.insert(0, '..')  # Add parent directory
        file_list = "\n".join(files)
        setTextWidget(str=f"Files in {path}:\n{file_list}\n")
    except Exception as e:
        setTextWidget(str=f"Error listing files: {e}\n")

def main():
    global _savePath
    global _configFile
    global _timeThreshold
    global _textWidget
    global _msgVar

    # Initialize the main window
    root = tkinterDnD.Tk()
    root.title("Drag & drop emails from outlook to save attachments.")
    root.geometry('600x400')

    if os.path.exists(_configFile):
        with open(_configFile, 'r') as f:
            config = json.load(f)
            _savePath = config.get("save_path", "")
            if not os.path.isdir(_savePath):
                _savePath = '.\\'
            _timeThreshold = config.get("time_threshold_seconds", 30)

    _msgVar = tk.StringVar()
    _msgVar.set(f"Save path: {_savePath}" if _savePath else "No save path set")

    thrhld_var = tk.StringVar()
    thrhld_var.set(f"Time threshold: {_timeThreshold} seconds")

    # Create the UI elements
    upper_frame = ttk.Frame(root)
    upper_frame.pack(fill="both", expand=True, padx=10, pady=10)

    lower_frame = ttk.Frame(root)
    lower_frame.pack(fill="x", padx=10, pady=10)

    _textWidget = tk.Text(upper_frame, wrap="word", height=15)
    _textWidget.pack(side="left", fill="both", expand=True)

    scrollbar = ttk.Scrollbar(upper_frame, orient="vertical", command=_textWidget.yview)
    scrollbar.pack(side="right", fill="y")

    _textWidget.config(yscrollcommand=scrollbar.set)
    # _textWidget.insert(tk.END, "Hello world!")

    # Register the text widget as a drop target
    _textWidget.register_drop_target("*")
    _textWidget.bind("<<Drop>>", drop)

    list_files(path=_savePath)

    browse_button = ttk.Button(lower_frame, text="Browse", command=browse_path)
    browse_button.pack(pady=10)

    _msg_label = ttk.Label(lower_frame, textvar=_msgVar, padding=10)
    _msg_label.pack(pady=10)

    thrhld_label = ttk.Label(lower_frame, textvar=thrhld_var, padding=10)
    thrhld_label.pack(pady=0)

    # Start the main loop
    root.mainloop()

if __name__ == "__main__":
    main()