import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU
from random import randrange
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinterDnD as tkdnd
import pymupdf as fitz
from PIL import Image, ImageTk

def main():
    try:
        cfg_ocr = MyU.load_config('config_ocr.json')
        settings = cfg_ocr.get('ocr settings',{})
    except Exception as e:
        print(f"Error! {e}")

    # root = tk.Tk()
    root = tkdnd.Tk()
    root.title(f"{__name__}")
    root_width = 800
    root_aspect = "4:3"
    root_height = int(root_width*int(root_aspect.split(':')[1])/int(root_aspect.split(':')[0]))
    root.geometry(f"{root_width}x{root_height}")

    fram_rt = ttk.Frame(root, borderwidth=2, relief='solid')
    fram_rt.pack(side='right', fill='both', expand=True, padx=5, pady=5)

    lf_ocrType = tk.LabelFrame(fram_rt, text="OCR type:", padx=5, pady=5)
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

    lf_ocrOption = tk.LabelFrame(fram_rt, text="Option:", padx=5, pady=5)
    lf_ocrOption.pack()
    checkButtons=[]
    options={}
    strVars=[]
    for i, ele in enumerate(settings.get('ocr options',[])):
        options[ele] = False
        strVars.append(tk.StringVar(value='False'))
        checkButtons.append(tk.Checkbutton(lf_ocrOption, anchor='w', text=ele, variable=strVars[i], onvalue='True', offvalue='False', command=foo))
        checkButtons[i].pack()

    lf_pages = tk.LabelFrame(fram_rt, text='Pages:', padx=5, pady=5)
    lf_pages.pack()
    pages = tk.StringVar(value='')
    pages_pages = tk.Entry(lf_pages, textvariable=pages)
    pages_pages.pack()
    pages_label = tk.Label(lf_pages, text='null(all)  1,2,3  1-3 ')
    pages_label.pack()

    def show_img_label(img=None, ppno=0)->None:
        ppno_lbl = tk.Label(fram_scrbar, text=f"pp.{ppno}")
        ppno_lbl.pack()
        img_tk = ImageTk.PhotoImage(img)
        img_lbl = tk.Label(fram_scrbar, image=img_tk)
        img_lbl.image = img_tk
        img_lbl.pack()
    def show_pdf_images(doc=None, zoom=1.0)->int:
        mtrx = fitz.Matrix(zoom, zoom)
        for i in range(doc.page_count):
            pp = doc.load_page(i)
            pix = pp.get_pixmap(matrix=mtrx)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            show_img_label(img=img,ppno=(i+1))
        fram_scrbar.update_idletasks()
        cnvs.config(scrollregion=cnvs.bbox("all"))
        return i+1
    def drop(event):
        try:
            pdffn = event.data
            doc = fitz.open(pdffn)
            n = show_pdf_images(doc=doc, zoom=0.5)
            # cnvs.pack(side="left", fill="both", expand=True)
            # scrbar.pack(side="right", fill="y")
        except Exception as e:
            print(f"drop()() Error={e}")
        finally:
            print(f"pdffn={pdffn}")
            print(f"doc.page_count={doc.page_count}")
            print(f"{n}-page processed.")
            print(f"last i={i}")
            doc.close()

    fram_lft = ttk.Frame(root, borderwidth=1, relief='solid', height=int(root_height), width=int(root_width/2))
    fram_lft.pack(side='left', fill='both', expand=True, padx=5, pady=5, )
    cnvs = tk.Canvas(fram_lft)
    scrbar = tk.Scrollbar(fram_lft, orient="vertical", command=cnvs.yview)
    fram_scrbar = tk.Frame(cnvs)
    fram_scrbar.bind("<Configure>", lambda e: cnvs.configure(scrollregion=cnvs.bbox("all")))
    cnvs.create_window((0,0), window=fram_scrbar, anchor="nw")
    cnvs.configure(yscrollcommand=scrbar.set)
    scrbar.config(command=cnvs.yview)
    cnvs.register_drop_target("*")
    cnvs.bind("<<Drop>>", drop)
    cnvs.pack(side="left", fill="both", expand=True)
    scrbar.pack(side="right", fill="y")

    root.mainloop()

if __name__ == "__main__":
    main()
