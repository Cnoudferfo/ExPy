import tkinter as tk
from tkinter import ttk, filedialog
import tkinterDnD
import json
import os
import win32com.client  # Make sure to install pywin32
from datetime import datetime

# Initialize the main window
root = tkinterDnD.Tk()
root.title("Drag & drop emails from outlook to save attachments.")
root.geometry('600x300')

# Load the save path from a JSON file
save_path = ""
config_file = "config.json"
time_threashold_seconds = 30 # default value
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        save_path = config.get("save_path", "")
        time_threashold_seconds = config.get("time_threashold_seconds", 30)

stringvar = tk.StringVar()
stringvar.set('Drop an email here!')

save_path_var = tk.StringVar()
save_path_var.set(f"Save path: {save_path}" if save_path else "No save path set")

thrhld_var = tk.StringVar()
thrhld_var.set(f"Time threshold : {time_threashold_seconds} seconds")

def drop(event):  # On dnd's drop event
    global save_path
    if not save_path:
        stringvar.set("Please select a save path first!")
        return
    try:
        dropped_data = event.data.split('\n')    # Split to an array of two strings
        dict_head = dropped_data[0].strip().split('\t')
        dict_data = dropped_data[1].strip().split('\t')
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
            if(time_diff > time_threashold_seconds):
                if i < 500:
                    print(f"pass this email, time_diff={time_diff} > threshold:{time_threashold_seconds}")
                    i = i + 1
                else:
                    stringvar.set(f"Quit for quick debug! search only in {i} items.")
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
                        file_path = os.path.join(save_path, attachment.FileName)

                        # Check file existence
                        base, ext = os.path.splitext(file_path)
                        f_counter = 1
                        while os.path.exists(file_path):
                            p_str1 = f"{file_path} exists,"
                            file_path =f"{base}_{f_counter}{ext}"
                            print(f"{p_str1} try {file_path}")
                            f_counter += 1

                        attachment.SaveAsFile(file_path)
                        saved_files.append(file_path)
                    stringvar.set(f"Attachments saved:\n" + "\n".join(saved_files))
                else:
                    stringvar.set("No attachments found in the email.")
                break
        else:
            stringvar.set("Email not found.")
    except Exception as e:
        stringvar.set(f"Error: {e}")

def browse_path():
    global save_path
    save_path = filedialog.askdirectory()
    if save_path:
        with open(config_file, 'w') as f:
            json.dump({"save_path": save_path}, f)
        save_path_var.set(f"Save path set to: {save_path}")

# Create the UI elements
label = ttk.Label(root, textvar=stringvar, padding=50, relief="solid")
label.pack(fill="both", expand=True, padx=10, pady=10)
label.register_drop_target("*")
label.bind("<<Drop>>", drop)

browse_button = ttk.Button(root, text="Browse", command=browse_path)
browse_button.pack(pady=10)

save_path_label = ttk.Label(root, textvar=save_path_var, padding=10)
save_path_label.pack(pady=10)

thrhld_label = ttk.Label(root, textvar=thrhld_var, padding=10)
thrhld_label.pack(pady=0)

# Start the main loop
root.mainloop()