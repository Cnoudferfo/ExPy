來寫程式。
由 Copilot 傳送:
當然可以！你想寫什麼樣的程式呢？是有特定的語言或項目嗎？例如，Python、JavaScript，還是其他的？或者你有一個具體的問題或功能需要幫助嗎？讓我知道，我會盡力幫助你！ 😊

由 您 傳送:
Please modify the following tkdnd's example code to an applet having these functions: 1) receive a drag-and-droped email from microsoft outlook, 2) copy the attached files (if there is any) of the email to a specified save path, 3) having a browse button to let user choose the save path, 4) use json file to save the save path for next usage of this applet.   Below is the original code
```python
import tkinter as tk
from tkinter import ttk
import tkinterDnD  # Importing the tkinterDnD module

# You have to use the tkinterDnD.Tk object for super easy initialization,
# and to be able to use the main window as a dnd widget
root = tkinterDnD.Tk()  
root.title("tkinterDnD example")

stringvar = tk.StringVar()
stringvar.set('Drop here or drag from here!')


def drop(event):
    # This function is called, when stuff is dropped into a widget
    stringvar.set(event.data)

def drag_command(event):
    # This function is called at the start of the drag,
    # it returns the drag type, the content type, and the actual content
    return (tkinterDnD.COPY, "DND_Text", "Some nice dropped text!")


# Without DnD hook you need to register the widget for every purpose,
# and bind it to the function you want to call
label_1 = tk.Label(root, textvar=stringvar, relief="solid")
label_1.pack(fill="both", expand=True, padx=10, pady=10)

label_1.register_drop_target("*")
label_1.bind("<<Drop>>", drop)

label_1.register_drag_source("*")
label_1.bind("<<DragInitCmd>>", drag_command)


# With DnD hook you just pass the command to the proper argument,
# and tkinterDnD will take care of the rest
# NOTE: You need a ttk widget to use these arguments
label_2 = ttk.Label(root, ondrop=drop, ondragstart=drag_command,
                    textvar=stringvar, padding=50, relief="solid")
label_2.pack(fill="both", expand=True, padx=10, pady=10)


root.mainloop()
```
正在為您產生解答…

由 Copilot 傳送:
Here’s a modified version of the code to create an applet with the specified functions:

Receive a drag-and-dropped email from Microsoft Outlook.
Copy the attached files (if any) of the email to a specified save path.
Include a browse button to let the user choose the save path.
Use a JSON file to save the save path for the next usage of this applet.
```Python
import tkinter as tk
from tkinter import ttk, filedialog
import tkinterDnD
import json
import os
import win32com.client  # Make sure to install pywin32

# Initialize the main window
root = tkinterDnD.Tk()
root.title("Email Attachment Saver")

# Load the save path from a JSON file
save_path = ""
config_file = "config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        save_path = config.get("save_path", "")

stringvar = tk.StringVar()
stringvar.set('Drop an email here!')

def drop(event):
    global save_path
    if not save_path:
        stringvar.set("Please select a save path first!")
        return

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    msg = outlook.OpenSharedItem(event.data)
    
    if msg.Attachments.Count > 0:
        for attachment in msg.Attachments:
            attachment.SaveAsFile(os.path.join(save_path, attachment.FileName))
        stringvar.set(f"Attachments saved to {save_path}")
    else:
        stringvar.set("No attachments found in the email.")

def browse_path():
    global save_path
    save_path = filedialog.askdirectory()
    if save_path:
        with open(config_file, 'w') as f:
            json.dump({"save_path": save_path}, f)
        stringvar.set(f"Save path set to: {save_path}")

# Create the UI elements
label = ttk.Label(root, textvar=stringvar, padding=50, relief="solid")
label.pack(fill="both", expand=True, padx=10, pady=10)
label.register_drop_target("*")
label.bind("<<Drop>>", drop)

browse_button = ttk.Button(root, text="Browse", command=browse_path)
browse_button.pack(pady=10)

# Start the main loop
root.mainloop()
```

AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Key Changes:
Drag-and-Drop Email Handling: The drop function now uses win32com.client to handle the dropped email and save its attachments.
Save Path Selection: Added a browse_path function and a button to let the user choose the save path.
Configuration Management: The save path is stored in a JSON file (config.json) and loaded on startup.
Make sure you have the pywin32 package installed to interact with Outlook:

```bash
pip install pywin32
```

Feel free to ask if you need any further modifications or explanations! 😊

1
github.com
2
pypi.org
3
stackoverflow.com
4
visualstudio.microsoft.com
由 您 傳送:
Thanks, but please make more modifications based on the above modified code. 1) print the "Save path set to..." string to somewhere outside the drop area, 2) print the ful path of the saved attached file in the drop area.
正在為您產生解答…

由 Copilot 傳送:
Sure, I’ve made the requested modifications to the code. Now, the “Save path set to…” message will be displayed outside the drop area, and the full path of the saved attached file will be printed in the drop area.

Here’s the updated code:

```Python
import tkinter as tk
from tkinter import ttk, filedialog
import tkinterDnD
import json
import os
import win32com.client  # Make sure to install pywin32

# Initialize the main window
root = tkinterDnD.Tk()
root.title("Email Attachment Saver")

# Load the save path from a JSON file
save_path = ""
config_file = "config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        save_path = config.get("save_path", "")

stringvar = tk.StringVar()
stringvar.set('Drop an email here!')

save_path_var = tk.StringVar()
save_path_var.set(f"Save path: {save_path}" if save_path else "No save path set")

def drop(event):
    global save_path
    if not save_path:
        stringvar.set("Please select a save path first!")
        return

    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    msg = outlook.OpenSharedItem(event.data)
    
    if msg.Attachments.Count > 0:
        saved_files = []
        for attachment in msg.Attachments:
            file_path = os.path.join(save_path, attachment.FileName)
            attachment.SaveAsFile(file_path)
            saved_files.append(file_path)
        stringvar.set(f"Attachments saved:\n" + "\n".join(saved_files))
    else:
        stringvar.set("No attachments found in the email.")

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

# Start the main loop
root.mainloop()
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Key Changes:
Save Path Message: Added a save_path_var to display the save path message outside the drop area.
Full Path of Saved Files: Modified the drop function to print the full path of each saved attached file in the drop area.
This should meet your requirements. Let me know if you need any further adjustments! 😊

由 您 傳送:
I droped an email in the drop area, but nothing happen. Why is that?
正在為您產生解答…

由 Copilot 傳送:
Let’s troubleshoot this together. Here are a few things to check:

Outlook Integration: Ensure that Microsoft Outlook is installed and configured correctly on your system. The script uses win32com.client to interact with Outlook, so Outlook must be running.
Permissions: Make sure the script has the necessary permissions to access Outlook and save files to the specified directory.
Event Data: Verify that the event.data contains the correct information. You can add a print statement in the drop function to see what data is being received:
```Python
def drop(event):
    print(event.data)  # Add this line to see the event data
    # Rest of the code...
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Error Handling: Add error handling to catch any exceptions that might occur during the process. This will help identify any issues:
```Python
def drop(event):
    global save_path
    if not save_path:
        stringvar.set("Please select a save path first!")
        return

    try:
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        msg = outlook.OpenSharedItem(event.data)
        
        if msg.Attachments.Count > 0:
            saved_files = []
            for attachment in msg.Attachments:
                file_path = os.path.join(save_path, attachment.FileName)
                attachment.SaveAsFile(file_path)
                saved_files.append(file_path)
            stringvar.set(f"Attachments saved:\n" + "\n".join(saved_files))
        else:
            stringvar.set("No attachments found in the email.")
    except Exception as e:
        stringvar.set(f"Error: {e}")
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Drag-and-Drop Compatibility: Ensure that the drag-and-drop functionality is compatible with the version of Outlook and the operating system you are using.
Try these steps and let me know if you see any error messages or if the issue persists. This will help us narrow down the problem. 😊

由 您 傳送:
How to make sure this python script has the permission to access outlook?
正在為您產生解答…

由 Copilot 傳送:
To ensure your Python script has the necessary permissions to access Outlook, follow these steps:

Install Required Packages: Make sure you have the pywin32 package installed, which allows Python to interact with Windows COM objects, including Outlook.
pip install pywin32

Run Outlook as Administrator: Sometimes, running both Outlook and your Python script with administrative privileges can help resolve permission issues.
Check Outlook Security Settings: Outlook may block programmatic access to its data for security reasons. You can adjust these settings:
Open Outlook.
Go to File > Options > Trust Center > Trust Center Settings.
Under Programmatic Access, select the option that allows access (e.g., “Never warn me about suspicious activity”).
Use Microsoft Graph API: For a more robust and secure approach, consider using the Microsoft Graph API. This requires setting up an Azure AD application and granting it the necessary permissions to access Outlook data. Here’s a brief overview:
Register an Application: Go to the Azure Portal, navigate to Azure Active Directory > App registrations, and register a new application.
Grant Permissions: In the app’s settings, grant the necessary API permissions (e.g., Mail.Read, Mail.ReadWrite).
Authenticate: Use the Microsoft Authentication Library (MSAL) to authenticate and obtain an access token.
Here’s a simple example using the Microsoft Graph API with the msal library:

```Python
import msal
import requests

# Replace with your app's client ID and tenant ID
client_id = 'YOUR_CLIENT_ID'
tenant_id = 'YOUR_TENANT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
result = app.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    access_token = result["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me/messages", headers=headers)
    print(response.json())
else:
    print("Error obtaining access token")
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
This example demonstrates how to authenticate and make a simple request to the Microsoft Graph API to read emails. You can expand this to handle attachments and other functionalities.

By following these steps, you should be able to ensure your script has the necessary permissions to access Outlook. Let me know if you need further assistance! 😊

1
github.com
2
pypi.org
3
kontext.tech
4
learn.microsoft.com
5
learn.microsoft.com
6
github.com
由 您 傳送:
The last "...nothing happen" was because of I used new outlook. After changed to classic outlook and dropped again, something happened, but it was an error message "File "C:\...\tkdnd_copyattch.py", line 33, in drop
    msg = outlook.OpenSharedItem(event.data)
  File "<COMObject GetNamespace>", line 2, in OpenSharedItem
pywintypes.com_error: (-2147352567, '發生例外狀況。', (4096, 'Microsoft Outlook', '路徑或 URL 無效。', None, 0, -2147352567), None)"
正在為您產生解答…

由 Copilot 傳送:
The error message indicates that the path or URL provided to OpenSharedItem is invalid. This can happen if the event.data does not contain a valid path or URL that Outlook can recognize. Here are a few steps to troubleshoot and resolve this issue:

Check the Event Data: Add a print statement to see what event.data contains when you drop an email. This will help you understand if the data is in the expected format.
```Python
def drop(event):
    print(event.data)  # Add this line to see the event data
    # Rest of the code...
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Verify the Dragged Data: Ensure that the data being dragged and dropped is indeed an email item from Outlook. Sometimes, the data might not be in the correct format.
Use the Correct Outlook Item: The OpenSharedItem method expects a valid file path or URL. If event.data is not providing this, you might need to adjust how you handle the dropped data.
Error Handling: Add error handling to provide more informative messages and prevent the app from crashing.
```Python
def drop(event):
    global save_path
    if not save_path:
        stringvar.set("Please select a save path first!")
        return

    try:
        print(event.data)  # Check the event data
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        msg = outlook.OpenSharedItem(event.data)
        
        if msg.Attachments.Count > 0:
            saved_files = []
            for attachment in msg.Attachments:
                file_path = os.path.join(save_path, attachment.FileName)
                attachment.SaveAsFile(file_path)
                saved_files.append(file_path)
            stringvar.set(f"Attachments saved:\n" + "\n".join(saved_files))
        else:
            stringvar.set("No attachments found in the email.")
    except Exception as e:
        stringvar.set(f"Error: {e}")
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Alternative Approach: If the above steps do not resolve the issue, consider using the Microsoft Graph API for a more robust solution. This approach involves setting up an Azure AD application and using the API to access Outlook data.
Here’s a brief example of how you might use the Microsoft Graph API to read emails and save attachments:

```Python
import msal
import requests
import os
import json

# Replace with your app's client ID, tenant ID, and client secret
client_id = 'YOUR_CLIENT_ID'
tenant_id = 'YOUR_TENANT_ID'
client_secret = 'YOUR_CLIENT_SECRET'

authority = f"https://login.microsoftonline.com/{tenant_id}"
scopes = ["https://graph.microsoft.com/.default"]

app = msal.ConfidentialClientApplication(client_id, authority=authority, client_credential=client_secret)
result = app.acquire_token_for_client(scopes=scopes)

if "access_token" in result:
    access_token = result["access_token"]
    headers = {"Authorization": f"Bearer {access_token}"}
    response = requests.get("https://graph.microsoft.com/v1.0/me/messages", headers=headers)
    emails = response.json()
    print(emails)
else:
    print("Error obtaining access token")
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
This example demonstrates how to authenticate and make a simple request to the Microsoft Graph API to read emails. You can expand this to handle attachments and other functionalities.

Let me know if you need further assistance or if you encounter any other issues! 😊

1
github.com
2
pypi.org
3
kontext.tech
4
learn.microsoft.com
5
learn.microsoft.com
6
github.com
由 您 傳送:
I used print(event.data) to check and it printed the Sender, Title, Receive Time..., I think that was not a legal URL .
正在為您產生解答…

由 Copilot 傳送:
It looks like the data being dragged and dropped is not in the format that OpenSharedItem expects. Instead of using OpenSharedItem, we can try a different approach to handle the dropped email data.

Here’s an updated version of the code that uses the win32com.client to access the Outlook inbox and find the email based on the subject or other properties. This approach assumes that the dropped data contains enough information to identify the email in the inbox.

```Python
import tkinter as tk
from tkinter import ttk, filedialog
import tkinterDnD
import json
import os
import win32com.client  # Make sure to install pywin32

# Initialize the main window
root = tkinterDnD.Tk()
root.title("Email Attachment Saver")

# Load the save path from a JSON file
save_path = ""
config_file = "config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        save_path = config.get("save_path", "")

stringvar = tk.StringVar()
stringvar.set('Drop an email here!')

save_path_var = tk.StringVar()
save_path_var.set(f"Save path: {save_path}" if save_path else "No save path set")

def drop(event):
    global save_path
    if not save_path:
        stringvar.set("Please select a save path first!")
        return

    try:
        print(event.data)  # Check the event data
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        # Find the email based on the subject or other properties
        for msg in messages:
            if event.data in msg.Subject:
                if msg.Attachments.Count > 0:
                    saved_files = []
                    for attachment in msg.Attachments:
                        file_path = os.path.join(save_path, attachment.FileName)
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

# Start the main loop
root.mainloop()
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Key Changes:
Email Identification: Instead of using OpenSharedItem, the script now searches the inbox for an email that matches the dropped data (e.g., subject).
Error Handling: Improved error handling to provide more informative messages.
This approach should help in identifying and processing the dropped email correctly. Let me know if this works or if you need further adjustments! 😊

由 您 傳送:
Wow! much longer and seems more robust. Let me try it.
正在為您產生解答…

由 Copilot 傳送:
Great! I’m glad you find it promising. Give it a try and let me know how it goes. If you encounter any issues or need further adjustments, feel free to reach out. I’m here to help! 😊

Good luck with your applet! 🚀

由 您 傳送:
It gave me "Email not found" string in the drop area. But I did dragged the mail from inbox which is GetDefaultFolder(6), and only one email account in that classic outlook.
正在為您產生解答…

由 Copilot 傳送:
It sounds like the script isn’t correctly identifying the email based on the dropped data. Let’s refine the approach to ensure we can accurately match the email. We can add more detailed logging and try to match the email based on multiple properties like subject, sender, and received time.

Here’s an updated version of the script with enhanced logging and matching criteria:

```python
import tkinter as tk
from tkinter import ttk, filedialog
import tkinterDnD
import json
import os
import win32com.client  # Make sure to install pywin32

# Initialize the main window
root = tkinterDnD.Tk()
root.title("Email Attachment Saver")

# Load the save path from a JSON file
save_path = ""
config_file = "config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        save_path = config.get("save_path", "")

stringvar = tk.StringVar()
stringvar.set('Drop an email here!')

save_path_var = tk.StringVar()
save_path_var.set(f"Save path: {save_path}" if save_path else "No save path set")

def drop(event):
    global save_path
    if not save_path:
        stringvar.set("Please select a save path first!")
        return

    try:
        print("Dropped data:", event.data)  # Check the event data
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        # Extract relevant information from the dropped data
        dropped_data = event.data.split("\n")
        subject = next((line for line in dropped_data if line.startswith("Subject:")), "").replace("Subject:", "").strip()
        sender = next((line for line in dropped_data if line.startswith("From:")), "").replace("From:", "").strip()
        received_time = next((line for line in dropped_data if line.startswith("Received:")), "").replace("Received:", "").strip()

        print(f"Searching for email with Subject: {subject}, From: {sender}, Received: {received_time}")

        # Find the email based on the extracted properties
        for msg in messages:
            if (subject in msg.Subject and sender in msg.SenderName and received_time in str(msg.ReceivedTime)):
                if msg.Attachments.Count > 0:
                    saved_files = []
                    for attachment in msg.Attachments:
                        file_path = os.path.join(save_path, attachment.FileName)
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

# Start the main loop
root.mainloop()
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Key Changes:
Detailed Logging: Added print statements to log the dropped data and the search criteria.
Enhanced Matching: Extracted subject, sender, and received time from the dropped data and used these properties to find the email.
Try this updated script and see if it helps in identifying the email correctly. Let me know how it goes or if you need further adjustments! 😊

由 您 傳送:
This time it gave me "No attachments found in the email.". I tried multiple times, I did dropped an test email with one attached json file. Can you please help to find the problem?
正在為您產生解答…

由 Copilot 傳送:
It seems like the script isn’t correctly identifying the attachments in the email. Let’s add more detailed logging to understand what’s happening and ensure that the email and its attachments are being accessed correctly.

Here’s an updated version of the script with additional logging to help diagnose the issue:

```Python
import tkinter as tk
from tkinter import ttk, filedialog
import tkinterDnD
import json
import os
import win32com.client  # Make sure to install pywin32

# Initialize the main window
root = tkinterDnD.Tk()
root.title("Email Attachment Saver")

# Load the save path from a JSON file
save_path = ""
config_file = "config.json"
if os.path.exists(config_file):
    with open(config_file, 'r') as f:
        config = json.load(f)
        save_path = config.get("save_path", "")

stringvar = tk.StringVar()
stringvar.set('Drop an email here!')

save_path_var = tk.StringVar()
save_path_var.set(f"Save path: {save_path}" if save_path else "No save path set")

def drop(event):
    global save_path
    if not save_path:
        stringvar.set("Please select a save path first!")
        return

    try:
        print("Dropped data:", event.data)  # Check the event data
        outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
        inbox = outlook.GetDefaultFolder(6)  # 6 refers to the inbox
        messages = inbox.Items
        messages.Sort("[ReceivedTime]", True)

        # Extract relevant information from the dropped data
        dropped_data = event.data.split("\n")
        subject = next((line for line in dropped_data if line.startswith("Subject:")), "").replace("Subject:", "").strip()
        sender = next((line for line in dropped_data if line.startswith("From:")), "").replace("From:", "").strip()
        received_time = next((line for line in dropped_data if line.startswith("Received:")), "").replace("Received:", "").strip()

        print(f"Searching for email with Subject: {subject}, From: {sender}, Received: {received_time}")

        # Find the email based on the extracted properties
        for msg in messages:
            print(f"Checking email: Subject: {msg.Subject}, From: {msg.SenderName}, Received: {msg.ReceivedTime}")
            if (subject in msg.Subject and sender in msg.SenderName and received_time in str(msg.ReceivedTime)):
                print("Email found")
                if msg.Attachments.Count > 0:
                    saved_files = []
                    for attachment in msg.Attachments:
                        print(f"Found attachment: {attachment.FileName}")
                        file_path = os.path.join(save_path, attachment.FileName)
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

# Start the main loop
root.mainloop()
```
AI 產生的代碼。請仔細檢視及使用。 深入了解常見問題集。
Key Changes:
Detailed Logging: Added print statements to log the dropped data, the search criteria, and the details of each email being checked.
Attachment Logging: Added print statements to log the details of each attachment found.
This should help us understand why the attachments are not being detected. Run the updated script and check the console output for any clues. Let me know what you find, and we can further refine the script based on the results! 😊

1
learn.microsoft.com
2
learn.microsoft.com
3
answers.microsoft.com
4
learn.microsoft.com
由 您 傳送:
Great! it worked.
正在為您產生解答…

由 Copilot 傳送:
That’s fantastic to hear! 🎉 I’m glad we could get it working. If you have any more questions or need further assistance with your applet or anything else, feel free to ask. Happy coding! 😊

由 您 傳送:
Thank you so much. For this applet, I can make it better ny myself. Next time let's work on other type of program.
正在為您產生解答…

由 Copilot 傳送:
You’re very welcome! I’m glad I could help. It’s great to hear that you’re confident in improving the applet further on your own. Whenever you’re ready to work on another type of program, just let me know. I’m here to assist with anything you need. Happy coding, and see you next time! 😊

由 您 傳送:
Good night!
正在為您產生解答…

由 Copilot 傳送:
Good night! Sleep well and see you next time! 😊🌙