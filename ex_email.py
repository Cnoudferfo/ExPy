#!/usr/bin/python
"""Script to fetch email from outlook."""
import win32com.client


def extract(count):
    """Get emails from outlook."""
    items = []
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(6)  # "6" refers to the inbox
    messages = inbox.Items
    message = messages.GetFirst()
    i = 0
    while message:
        try:
            msg = dict()
            msg["Subject"] = getattr(message, "Subject", "<UNKNOWN>")
            msg["SentOn"] = getattr(message, "SentOn", "<UNKNOWN>")
            msg["EntryID"] = getattr(message, "EntryID", "<UNKNOWN>")
            msg["Sender"] = getattr(message, "Sender", "<UNKNOWN>")
            msg["Size"] = getattr(message, "Size", "<UNKNOWN>")
            msg["Body"] = getattr(message, "Body", "<UNKNOWN>")
            items.append(msg)
        except Exception as ex:
            print("Error processing mail", ex)
        i += 1
        if i < count:
            message = messages.GetNext()
        else:
            return items

    return items


def show_message(items):
    """Show the messages."""
    items.sort(key=lambda tdn: tdn["SentOn"])
    for i in items:
        print(i["SentOn"], i["Subject"], i["Body"])


def main():
    """Fetch and display top message."""
    items = extract(30)
    show_message(items)


if __name__ == "__main__":
    main()