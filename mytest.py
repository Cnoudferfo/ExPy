import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU
import do_ocr as Doo
from random import randrange
import tkinter as tk
from tkinter import ttk
from tkinter import *
import tkinterDnD as tkdnd
import pymupdf as fitz
from PIL import Image, ImageTk
import re

# Globale variables
theConfig = None
theFilepath = ''

def createRoot() -> tkdnd.Tk:
    global theConfig
    # Read config file, load ocr setting: ocr_type, log / plain flags & pages
    theConfig = MyU.load_config('config_ocr.json')
    # gui settings
    gui_stts = theConfig.get('gui settings',{})
    root_aspect = gui_stts['root aspect']
    root_width = gui_stts['root width']
    # thbn_zoom = gui_stts['thumbnail zoom']
    # Create root window
    root = tkdnd.Tk()
    root.title(f"{os.path.basename(__file__)}")
    # root_width = 800
    # root_aspect = "4:3"
    root_height = int(root_width*int(root_aspect.split(':')[1])/int(root_aspect.split(':')[0]))
    root.geometry(f"{root_width}x{root_height}")
    return root
def createOcrSettingUI(parent) -> ttk.Frame:
    global theConfig
    # Create message frame
    fram_rt = ttk.Frame(parent, borderwidth=2, relief='solid')
    # Call back function
    def on_clickRadioButton():
        print(f"ocr type={ocrType.get()}")
        for i, key in enumerate(options.keys()):
            options[key]= True if strVars[i].get()=='True' else False
    # Call do_ocr.py.iterateInPdf() when Do OCR button pressed
    def on_clickButton():
        global theFilepath
        print(f"ocr_type={ocrType.get()}")
        print(f"log={options['log']}")
        print(f"plain={options['plain']}")
        pps = pages.get().replace(' ','')
        if not pps:
            print(f"Empty pages, set batch to None.")
            batch_list=None
        else:
            print(f"pps={pps}")
            punc = re.findall(r'[^\w\w]', pps)
            print(f"punc={punc}")
            if len(punc) > 0:
                the_list = pps.split(punc[0])
            else:
                the_list = pps.split(' ')
            print(f"the_list={the_list}")
            if len(the_list) == 2:
                batch_list = list(range(int(the_list[0]), (int(the_list[1])+1)))
            else:
                batch_list = [int(c) for c in the_list]
        print(f"batch={batch_list}")
        print(f"filenmae={theFilepath}")
        print(f"Those settings will be used.")
        print((f"Call iterateInPdf()"))
        try:
            Doo.iterateInPdf(pdffn=theFilepath, ocr_type=ocrType.get(), batch=batch_list, do_log=options['log'], do_plain=options['plain'])
        except Exception as e:
            print(f"Exception={e}")
    # ocr settings
    ocr_stts = theConfig.get('ocr settings',{})
    # Create OCR type UI
    lf_ocrType = tk.LabelFrame(fram_rt, text="OCR type:", padx=5, pady=5)
    lf_ocrType.pack()
    ocrType = tk.StringVar(value='use_easy')
    radioButtons=[]
    for i, ele in enumerate(ocr_stts.get('ocr types',[])):
        radioButtons.append(tk.Radiobutton(lf_ocrType, anchor='w', text=ele, variable=ocrType, value=ele, command=on_clickRadioButton))
        radioButtons[i].pack()
    # Create Option (log / plain) UI
    lf_ocrOption = tk.LabelFrame(fram_rt, text="Option:", padx=5, pady=5)
    lf_ocrOption.pack()
    checkButtons=[]
    options={}
    strVars=[]
    for i, ele in enumerate(ocr_stts.get('ocr options',[])):
        options[ele] = False
        strVars.append(tk.StringVar(value='False'))
        checkButtons.append(tk.Checkbutton(lf_ocrOption, anchor='w', text=ele, variable=strVars[i], onvalue='True', offvalue='False', command=on_clickRadioButton))
        checkButtons[i].pack()
    # Create Pages UI
    lf_pages = tk.LabelFrame(fram_rt, text='Pages:', padx=5, pady=5)
    lf_pages.pack()
    pages = tk.StringVar(value='')
    pages_pages = tk.Entry(lf_pages, textvariable=pages)
    pages_pages.pack()
    pages_label = tk.Label(lf_pages, text='null(all)  1,2,3  1-3 ')
    pages_label.pack()
    # Create "do ocr" button
    button_doOcr = tk.Button(fram_rt,text="Do OCR", command=on_clickButton)
    button_doOcr.pack(pady = 10, padx = 10)
    return fram_rt

def createPdfDisplayUI(parent) -> ttk.Frame:
    # Display PDF
    #  Create image label
    def make_labels(img=None, ppno=0):
        ppno_lbl = tk.Label(fram_scrbar)
        img_tk = ImageTk.PhotoImage(img)
        img_lbl = tk.Label(fram_scrbar, image=img_tk)
        img_lbl.image = img_tk
        img_lbl.bind("<Button-1>", on_leftClick)
        return img_lbl, ppno_lbl
    #  Iterate all pages in pdf
    def show_pdf_images(doc=None, zoom=1.0)->int:
        mtrx = fitz.Matrix(zoom, zoom)
        for i in range(doc.page_count):
            pp = doc.load_page(i)
            pix = pp.get_pixmap(matrix=mtrx)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            iL, pL = make_labels(img=img,ppno=(i+1))
            img_labels.append(iL)
            pno_labels.append(pL)
            page_infos.append(tk.StringVar(value=f"Page {i+1}"))
            pno_labels[i].config(textvar=page_infos[i])
            img_labels[i].grid(column=0, row=i)
            pno_labels[i].grid(column=1, row=i)
        fram_scrbar.update_idletasks()
        cnvs.config(scrollregion=cnvs.bbox("all"))
        return i+1
    # To receive a dropped pdf file
    def on_drop(event):
        global theConfig, theFilepath
        try:
            theFilepath = event.data
            theDoc = fitz.open(theFilepath)
            if len(img_labels):
                for im in img_labels:
                    im.destroy()
                del(img_labels[:])
            if len(pno_labels):
                for n in pno_labels:
                    n.destroy()
                del(pno_labels[:])
            if len(page_infos):
                for p in page_infos:
                    p.set('')
                del(page_infos[:])
            thbn_zoom = theConfig.get('gui settings',{})['thumbnail zoom']
            n = show_pdf_images(doc=theDoc, zoom=thbn_zoom)
            print(f"pdffn={theFilepath}")
            print(f"doc.page_count={theDoc.page_count}")
            print(f"{n}-page processed.")
        except Exception as e:
            print(f"drop()() Error={e}")
        finally:
            theDoc.close()
    #  Mouse wheel scroll
    def on_mouseWheel(event):
        cnvs.yview_scroll(number=int((-1 * event.delta)/120), what=tk.UNITS)
    # Mouse left click
    def on_leftClick(event):
       print(f"{page_infos[img_labels.index(event.widget)].get()}")

    # Create thumbnail UI
    fram_lft = ttk.Frame(parent, borderwidth=2, relief='solid')
    # fram_lft.pack(side='left', fill='both', expand=True, padx=5, pady=5, )
    cnvs = tk.Canvas(fram_lft, borderwidth=0, relief='solid')
    scrbar = tk.Scrollbar(fram_lft, orient="vertical", command=cnvs.yview)
    fram_scrbar = tk.Frame(cnvs, borderwidth=0, relief='solid', padx=10, pady=10)
    fram_scrbar.bind("<Configure>", lambda e: cnvs.configure(scrollregion=cnvs.bbox("all")))
    cnvs.create_window((0,0), window=fram_scrbar, anchor="nw")
    cnvs.configure(yscrollcommand=scrbar.set)
    scrbar.config(command=cnvs.yview)
    cnvs.register_drop_target("*")
    cnvs.bind("<<Drop>>", on_drop)
    cnvs.pack(side="left", fill="both", expand=True)
    scrbar.pack(side="right", fill="y")
    cnvs.bind("<MouseWheel>", on_mouseWheel)
    # Create empty list
    img_labels=[]  # images
    pno_labels=[]  # page numbers
    page_infos=[]  # page infos
    return fram_lft

def main() -> None:
    theRoot = createRoot()
    theRoot.columnconfigure(0, weight=1)
    theRoot.columnconfigure(1, weight=1)
    theRoot.rowconfigure(0,weight=1)
    fm1 = createOcrSettingUI(parent=theRoot)
    fm1.grid(column=1, row=0, sticky="nsew")
    fm2 = createPdfDisplayUI(parent=theRoot)
    fm2.grid(column=0, row=0, sticky="nsew")
    theRoot.mainloop()

if __name__ == "__main__":
    main()
