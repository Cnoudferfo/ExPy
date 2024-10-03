import os
import tkinter as tk
from tkinter import font
from tkinter import ttk
import tkinterDnD
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import do_ocr as Doo

root = None
progressBar = None
textWidget = None
textInTw = None

# Dsiplay a string in text widget
def tw_set_string(str):
    global textWidget
    textWidget.config(state=tk.NORMAL)
    textWidget.delete(1.0, tk.END)
    textWidget.insert(tk.END, str)
    textWidget.config(state=tk.DISABLED)

def tw_insert_string(str):
    global textWidget
    textWidget.config(state=tk.NORMAL)
    textWidget.insert(tk.END, str)
    textWidget.config(state=tk.DISABLED)

def progress_callback(maximum = None, value = None, text = None):
    global progressBar, textWidget, root, textInTw
    if maximum != None:
        # Before process a valid event
        progressBar.config(mode='determinate', maximum=maximum)  # To set a progress bar
        progressBar.start()
        tw_set_string("processing...")  # Update display message
    if value != None:
        # To update progress bar
        progressBar['value'] = value
        root.update_idletasks()
    if text != None:
        if text == "init ocr":
            tw_insert_string(str=f"init ocr...\n")
        else:
            textInTw = text

def main():
    global root, progressBar, textWidget, textInTw

    if len(sys.argv) == 2 and sys.argv[1] == 'use_tess':
        pass
    elif len(sys.argv) == 2 and sys.argv[1] == 'use_easy':
        pass
    else:
        print(f"Usage: python {os.path.basename(__file__)} ocr_option")
        print(f"    ocr_option: [use_tess] tesseract, [use_easy] EasyOCR")
        exit(-1)

    root = tkinterDnD.Tk()
    root.title("綜合PDF整理器")
    root.geometry("1000x750")  # Adjust the size as needed

    def drop(event):  # This function is called, when stuff is dropped into a widget

        try:
            if not os.path.isfile(event.data) or 'pdf' not in event.data:
                tw_set_string(str=f"Wrong! {event.data} is NOT a pdf file!")
                return

            # call Do_ocr
            Doo.Do_ocr(pdfFilePath = event.data, pgCommand = progress_callback)

            # To display OCR result
            tw_set_string(str=textInTw)

        except Exception as e:
            # Display error message
            tw_set_string(str=f"Error: {e}")

        finally:
            # Stop the progress bar
            progressBar.stop()

    # Define font size and calculate padding
    label_font = font.Font(family="Helvetica", size=12)
    line_height = label_font.metrics("linespace")
    padding = line_height // 8

    # Create a progress bar
    progressBar = ttk.Progressbar(root, mode='determinate')
    progressBar.pack(fill="x", padx=10, pady=(0, padding))

    # Create a frame for the text widget and scrollbar
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a scrollbar to the display area of stringvar2
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    # Use a Text widget instead of Label for scrollable content
    disp_font = font.Font(family="Meiryo UI", size=10)
    textWidget = tk.Text(frame, wrap="word", relief="solid", yscrollcommand=scrollbar.set, font=disp_font)
    textWidget.pack(fill="both", expand=True)

    tw_set_string(str=f"OCR = {sys.argv[1]}\n")

    if sys.argv[1] == 'use_tess':
        Doo.use_tess()
    else:
        Doo.use_easyocr()

    tw_insert_string(str="Drop a PDF here.")
    # Bind drop event to text widget
    textWidget.register_drop_target("*")
    textWidget.bind("<<Drop>>", drop)

    # Configure the scrollbar
    scrollbar.config(command=textWidget.yview)

    root.mainloop()

if __name__ == "__main__":
    main()