import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU
from random import randrange
import tkinter as tk
from tkinter import ttk
from tkinter import *
import pymupdf as fitz
from PIL import Image, ImageTk

def gui_main():
    try:
        cfg_ocr = MyU.load_config('config_ocr.json')
        settings = cfg_ocr.get('ocr settings',{})
    except Exception as e:
        print(f"Error! {e}")

    root = tk.Tk()
    root.title(f"{__name__}")
    root_width = 800
    root_aspect = "4:3"
    root_height = int(root_width*int(root_aspect.split(':')[1])/int(root_aspect.split(':')[0]))
    root.geometry(f"{root_width}x{root_height}")

    frame_right = ttk.Frame(root, borderwidth=2, relief='solid')
    frame_right.pack(side='right', fill='both', expand=True, padx=5, pady=5)

    lf_ocrType = tk.LabelFrame(frame_right, text="OCR type:", padx=5, pady=5)
    lf_ocrType.pack()
    ocrType = tk.StringVar(value='use_easy')
    def foo():
        print(f"cot type={ocrType.get()}")
        for i, key in enumerate(options.keys()):
            options[key]= True if strVars[i].get()=='True' else False
    radioButtons=[]
    for i, ele in enumerate(settings.get('ocr types',[])):
        radioButtons.append(tk.Radiobutton(lf_ocrType, anchor='w', text=ele, variable=ocrType, value=ele, command=foo))
        radioButtons[i].pack()

    lf_ocrOption = tk.LabelFrame(frame_right, text="Option:", padx=5, pady=5)
    lf_ocrOption.pack()
    checkButtons=[]
    options={}
    strVars=[]
    for i, ele in enumerate(settings.get('ocr options',[])):
        options[ele] = False
        strVars.append(tk.StringVar(value='False'))
        checkButtons.append(tk.Checkbutton(lf_ocrOption, anchor='w', text=ele, variable=strVars[i], onvalue='True', offvalue='False', command=foo))
        checkButtons[i].pack()

    lf_pages = tk.LabelFrame(frame_right, text='Pages:', padx=5, pady=5)
    lf_pages.pack()
    pages = tk.StringVar(value='')
    pages_pages = tk.Entry(lf_pages, textvariable=pages)
    pages_pages.pack()
    pages_label = tk.Label(lf_pages, text='null(all)  1,2,3  1-3 ')
    pages_label.pack()

    frame_left = ttk.Frame(root, borderwidth=1, relief='solid', height=int(root_height), width=int(root_width/2))
    frame_left.pack(side='left', fill='both', expand=True, padx=5, pady=5, )
    scrollbar = tk.Scrollbar(frame_left)
    scrollbar.pack(side='right', fill='y')

    canvas = tk.Canvas(frame_left, bg='lightblue', yscrollcommand=scrollbar.set)
    canvas.pack(side='left', fill='both', expand=True)

    zoom = 0.5
    mtx = fitz.Matrix(zoom, zoom)
    def pdf_to_img(ppno):
        pp = doc.load_page(ppno)
        pix = pp.get_pixmap(matrix=mtx)
        return Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    def show_image(ppno):
        img = pdf_to_img(ppno=ppno)
        img_tk = ImageTk.PhotoImage(img)
        frame = tk.Frame(canvas)
        panel = tk.Label(frame, image=img_tk, text=f"page{i+1}")
        panel.pack(side='bottom', fill="both", expand=True)
        frame.image = img_tk
        canvas.create_window(0,int(i*img_tk.height()),anchor='nw',window=frame)
        frame.update_idletasks()
        canvas.config(scrollregion=canvas.bbox("all"))
    try:
        pdffn = ".\\test_data\\rearranged.pdf"
        doc = fitz.open(pdffn)
        for i in range(doc.page_count):
            show_image(i)
        scrollbar.config(command=canvas.yview)
    except Exception as e:
        print(f"gui_main() error={e}")
        doc.close()

    root.mainloop()
    doc.close()

def main():
    pdffn = ".\\test_data\\rearranged.pdf"
    doc = fitz.open(pdffn)
    try:
        for i in range(doc.page_count):
            pass
    except Exception as e:
        print(f"main() error={e}")
    finally:
        doc.close()

if __name__ == "__main__":
    gui_main()
    # main()
