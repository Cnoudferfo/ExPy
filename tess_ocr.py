import os
import tkinter as tk
from tkinter import font
from tkinter import ttk
import tkinterDnD
from PIL import Image
import pytesseract as ts
import pymupdf as pmpdf
import re  # To use regular expression
import json
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU

def load_config(fpth):
    with open(fpth, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def parse_config(cnfg):
    attr = cnfg.get('Attributes',{})
    titles = attr.get('titles',[])
    vnames = attr.get('vendor names',[])
    quonum = attr.get('quotation number',[])
    return titles, vnames, quonum

def extract_quotation_number(text):
    match = re.search(r'估價單編號:(\d+)', text)
    if match:
        return match.group(1)
    return None

# Dsiplay a string in text widget
def disp_text_widget(txt_wdgt, str):
    txt_wdgt.config(state=tk.NORMAL)
    txt_wdgt.delete(1.0, tk.END)
    txt_wdgt.insert(tk.END, str)
    txt_wdgt.config(state=tk.DISABLED)

# Parse a pdf page's text strings
def parse_a_pdf_page_at_zoom(page, zoom=1.2):
    if not isinstance(page, pmpdf.Page):
        raise ValueError("parse_a_pdf_page_at_zoom() must receive a PyMuPDF page object")
    mtrx = pmpdf.Matrix(zoom, zoom)  # To set a zoomed matrix
    page_pix = page.get_pixmap(matrix=mtrx)  # To get pixmap of page
    page_img = Image.frombytes("RGB", [page_pix.width, page_pix.height], page_pix.samples)  # Convert pixmap to image
    page_str = ts.image_to_string(page_img, lang='chi_tra')  # To perform OCR
    return page_str.split('\n')

def main():
    print(f"Dbg: cwd={os.getcwd()}")
    try:
        ocr_cfg = load_config('config_ocr.json')
        titles, vendor_names, quotation_number = parse_config(ocr_cfg)
        print("Attributes:")
        for t in titles:
            print(f"{t}")
        for vn in vendor_names:
            print(f"{vn}")
        for qn in quotation_number:
            print(f"{qn}")
    except Exception as e:
        print(f"Error: {e}")
        exit(-1)

    ts.pytesseract.tesseract_cmd = r'D:\Tools\tesseract540\tesseract.exe'

    root = tkinterDnD.Tk()  
    root.title("tkinterDnD example")
    root.geometry("1000x750")  # Adjust the size as needed

    stringvar1 = tk.StringVar()
    stringvar1.set('Drop here or drag from here!')

    def drop(event):  # This function is called, when stuff is dropped into a widget        
        stringvar1.set(f"Dropped object={event.data}")
        try:
            # Validate the dropped object
            if not os.path.isfile(event.data) or 'pdf' not in event.data:
                disp_text_widget(text_widget, f"Wrong! {event.data} is NOT a pdf file!")
                return

            pdf = pmpdf.open(event.data)  # To open pdf file

            # Before process a valid event
            progress_bar.config(mode='determinate', maximum=pdf.page_count)  # To set a progress bar
            progress_bar.start()
            disp_text_widget(text_widget, 'Processing...')  # Update display message

            text = 'OCR result ' + '\n'
            # For each page in pdf
            for i in range(pdf.page_count):  # Use PyMuPdf
                # Perform OCR
                pp = pdf.load_page(i)  # To load page
                pp_strs = parse_a_pdf_page_at_zoom(page=pp, zoom=1.2)  # To parse this page to strings
                text += f"Dbg: page{i} : {len(pp_strs)} strings \n"
                for s in pp_strs:
                    if s != '':
                        # clean_str = s.strip().replace(' ','').replace('\t','')
                        clean_str = MyU.remove_all_whitespaces(s)
                        # print(f"Page{i} : {clean_str}, quo_num={extract_quotation_number(clean_str)}")
                        print(f"Dbg: page{i} : {clean_str}")
                
                # To update progress bar
                progress_bar['value'] = i+1
                root.update_idletasks()

            # To display OCR result
            disp_text_widget(text_widget, text)

        except Exception as e:
            # Display error message
            disp_text_widget(text_widget, f"Error: {e}")
            
        finally:
            # Stop the progress bar
            progress_bar.stop()

    # Define font size and calculate padding
    label_font = font.Font(family="Helvetica", size=12)
    line_height = label_font.metrics("linespace")
    padding = line_height // 8

    # Create label 1
    label_1 = tk.Label(root, textvar=stringvar1, relief="solid", font=label_font)
    label_1.pack(fill="x", expand=False, padx=10, pady=(padding, 0))

    # Register drop event
    label_1.register_drop_target("*")
    label_1.bind("<<Drop>>", drop)

    # Create a progress bar
    progress_bar = ttk.Progressbar(root, mode='determinate')
    progress_bar.pack(fill="x", padx=10, pady=(0, padding))

    # Create a frame for the text widget and scrollbar
    frame = tk.Frame(root)
    frame.pack(fill="both", expand=True, padx=10, pady=10)

    # Add a scrollbar to the display area of stringvar2
    scrollbar = tk.Scrollbar(frame)
    scrollbar.pack(side="right", fill="y")

    # Use a Text widget instead of Label for scrollable content
    disp_font = font.Font(family="Meiryo UI", size=10)
    text_widget = tk.Text(frame, wrap="word", relief="solid", yscrollcommand=scrollbar.set, font=disp_font)
    text_widget.pack(fill="both", expand=True)
    text_widget.insert(tk.END, 'Drop a PDF file to above box')
    text_widget.config(state=tk.DISABLED)

    # Configure the scrollbar
    scrollbar.config(command=text_widget.yview)

    root.mainloop()

if __name__ == "__main__":
    main()