#!/usr/bin/python
"""Script to fetch email from outlook."""
import win32com.client
import datetime
import pytz

def extract(count):
    """Get emails from outlook."""
    items = []
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")
    inbox = outlook.GetDefaultFolder(5)  # "6" refers to the inbox
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


def show_message(items, filter_string, exclude_string, date_limit):
    """Show the messages."""
    # items.sort(key=lambda tdn: tdn["SentOn"])
    date_limit = datetime.datetime.strptime(date_limit, "%Y-%m-%d")
    date_limit = date_limit.replace(tzinfo=pytz.UTC)
    filtered_items = [
        item for item in items if filter_string in item["Subject"] and item["SentOn"] >= date_limit and exclude_string not in item["Subject"] and "FW" not in item["Subject"] and "RE" not in item["Subject"] ]
    filtered_items.sort(key=lambda tdn: tdn["SentOn"])
    for i in filtered_items:
        print(i["SentOn"], i["Subject"], i["Body"])


def main():
    """Fetch and display top message."""
    items = extract(3000)
    filter_string = "會議MEMO"
    exclude_string = "颱風影響"
    datetime_limit = "2024-07-22"
    show_message(items, filter_string, exclude_string, datetime_limit)


if __name__ == "__main__":
    main()