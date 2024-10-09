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
import threading as th

# Globale variables
theConfig = None
theFilepath = ''
thePpInfoStrs=[]  # page infos: a list to store all pages' information of drooped pdf
thePpImgLbls=[]   # images
thePpInfoLbls=[]  # page numbers
thePageEdits = {
    'page no': None,
    'quotation number': None,
    'vendor name': None,
    'paper title': None
}
theDoOcrButton=None
theChangePpInfoButton=None
theSaveFilesButton=None

def createRoot() -> tkdnd.Tk:
    global theConfig
    # Read config file, load ocr setting: ocr_type, log / plain flags & pages
    theConfig = MyU.load_config('config_ocr.json')
    # gui settings
    gui_stts = theConfig.get('gui settings',{})
    root_aspect = gui_stts['root aspect']
    root_width = gui_stts['root width']
    # Create root window
    root = tkdnd.Tk()
    root.title(f"{os.path.basename(__file__)}")
    root_height = int(root_width*int(root_aspect.split(':')[1])/int(root_aspect.split(':')[0]))
    root.geometry(f"{root_width}x{root_height}")
    return root

def enableDoOcrButton() -> None:
    theDoOcrButton.config(state='active')

def proc_ocr(ocr_args):
    r = Doo.gen_iterateInPdf(pdffn=ocr_args['pdf path'],\
                             ocr_type=ocr_args['ocr_type'],\
                             batch=ocr_args['batch'],\
                             do_log=ocr_args['do_log'],\
                             do_plain=ocr_args['do_plain'])
    i = 0
    while True:
        p = next(r)
        if not p:
            break
        else:
            thePpInfoStrs[i].set(value=p)
            thePpImgLbls[i].update()
        i += 1
        if i > 1000:
            break

def createOcrSettingUI(parent) -> ttk.Frame:
    global theConfig
    global theDoOcrButton
    # Call back function
    def on_clickRadioButton():
        print(f"ocr type={ocrType.get()}")
        for i, key in enumerate(options.keys()):
            options[key]= True if strVars[i].get()=='True' else False
    # Call do_ocr.py.iterateInPdf() when Do OCR button pressed
    def on_doOcr():
        global theFilepath
        global thePpInfoStrs
        global thePpInfoLbls
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

        ocr_args = {
            'pdf path': theFilepath,
            'ocr_type': ocrType.get(),
            'batch': batch_list,
            'do_log': options['log'],
            'do_plain': options['plain']
        }

        thid = th.Thread(target=lambda: proc_ocr(ocr_args=ocr_args))
        thid.start()

    # ocr settings
    ocr_stts = theConfig.get('ocr settings',{})
    # Create message frame
    fram_rt = ttk.Frame(parent, borderwidth=2, relief='solid')
    # Create OCR type UI
    lf_ocrType = tk.LabelFrame(fram_rt, text="OCR type:", padx=5, pady=5)
    lf_ocrType.pack(pady=10, padx=10, expand=True, fill='both')
    ocrType = tk.StringVar(value='use_easy')
    radioButtons=[]
    for i, ele in enumerate(ocr_stts.get('ocr types',[])):
        radioButtons.append(tk.Radiobutton(lf_ocrType, anchor='w', text=ele, variable=ocrType, value=ele, command=on_clickRadioButton))
        radioButtons[i].pack(pady=10, padx=10, expand=True, fill='both')
    # Create Option (log / plain) UI
    lf_ocrOption = tk.LabelFrame(fram_rt, text="Option:", padx=5, pady=5)
    lf_ocrOption.pack(pady=10, padx=10, expand=True, fill='both')
    checkButtons=[]
    options={}
    strVars=[]
    for i, ele in enumerate(ocr_stts.get('ocr options',[])):
        options[ele] = False
        strVars.append(tk.StringVar(value='False'))
        checkButtons.append(tk.Checkbutton(lf_ocrOption, anchor='w', text=ele, variable=strVars[i], onvalue='True', offvalue='False', command=on_clickRadioButton))
        checkButtons[i].pack(pady=10, padx=10, expand=True, fill='both')
    # Create Pages UI
    lf_pages = tk.LabelFrame(fram_rt, text='Pages:', padx=5, pady=5)
    lf_pages.pack(pady=10, padx=10, expand=True, fill='both')
    pages = tk.StringVar(value='')
    pages_pages = tk.Entry(lf_pages, textvariable=pages)
    pages_pages.pack(pady=10, padx=10, expand=True, fill='both')
    pages_label = tk.Label(lf_pages, text='null(all)  1,2,3  1-3 ')
    pages_label.pack(pady=10, padx=10, expand=True, fill='both')
    # Create "do ocr" button
    theDoOcrButton = tk.Button(fram_rt,text="Do OCR", command=on_doOcr, foreground="black", background="lightblue")
    theDoOcrButton.pack(pady=10, padx=10, expand=True, fill='both')
    theDoOcrButton.config(state='disabled')
    return fram_rt

def createPdfDisplayUI(parent) -> ttk.Frame:
    global theConfig
    global theFilepath
    global thePpInfoStrs
    global thePpImgLbls
    global thePpInfoLbls
    global thePageEdits
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
            thePpImgLbls.append(iL)
            thePpInfoLbls.append(pL)
            sss = f"page.{i+1}\n" + f"unknownQn\n" + f"unknownVn\n" + f"unknownTt"
            thePpInfoStrs.append(tk.StringVar(value=sss))
            thePpInfoLbls[i].config(textvar=thePpInfoStrs[i])
            thePpImgLbls[i].grid(column=0, row=i)
            thePpInfoLbls[i].grid(column=1, row=i)
        fram_scrbar.update_idletasks()
        cnvs.config(scrollregion=cnvs.bbox("all"))
        return i+1
    # To receive a dropped pdf file
    def resetPdf() -> None:
        if len(thePpImgLbls):
            for im in thePpImgLbls:
                im.destroy()
            del(thePpImgLbls[:])
        if len(thePpInfoLbls):
            for n in thePpInfoLbls:
                n.destroy()
            del(thePpInfoLbls[:])
        if len(thePpInfoStrs):
            for p in thePpInfoStrs:
                p.set('')
            del(thePpInfoStrs[:])
        for key in thePageEdits.keys():
            thePageEdits[key].set('')
    def on_drop(event):
        global theFilepath
        try:
            theFilepath = event.data
            theDoc = fitz.open(theFilepath)
            resetPdf()
            thbn_zoom = theConfig.get('gui settings',{})['thumbnail zoom']
            n = show_pdf_images(doc=theDoc, zoom=thbn_zoom)
            enableDoOcrButton()
            enableSaveFilesButton()
        except Exception as e:
            print(f"drop() Error={e}")
        finally:
            theDoc.close()
    #  Mouse wheel scroll
    def on_mouseWheel(event):
        cnvs.yview_scroll(number=int((-1 * event.delta)/120), what=tk.UNITS)
    # Mouse left click
    def on_leftClick(event):
        dic = {}
        ls = thePpInfoStrs[thePpImgLbls.index(event.widget)].get().split('\n')
        for i, key in enumerate(thePageEdits.keys()):
            dic[key] = ls[i]
        to_updatePageEdit(pp_dic=dic)

    # Create thumbnail UI
    fram_lft = ttk.Frame(parent, borderwidth=2, relief='solid')
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
    return fram_lft

def to_updatePageEdit(pp_dic=None) -> None:
    global thePageEdits
    global theChangePpInfoButton
    for key in thePageEdits.keys():
        thePageEdits[key].set(pp_dic[key])
    theChangePpInfoButton.config(state='active')

def createPageEditUI(parent) -> ttk.Frame:
    global thePageEdits
    global thePpInfoStrs
    global theChangePpInfoButton
    def on_clickToChange():
        pn = thePageEdits['page no']
        pnlst = pn.get().split('.')
        ppno = int(pnlst[1])
        qn = thePageEdits['quotation number'].get()
        vn = thePageEdits['vendor name'].get()
        tt = thePageEdits['paper title'].get()
        ppinfo = f"page.{ppno}\n"+f"{qn}\n"+f"{vn}\n"+f"{tt}"
        thePpInfoStrs[ppno-1].set(ppinfo)

    frm = ttk.Frame(parent, borderwidth=2, relief='solid')
    lbfrm = tk.LabelFrame(frm, text="Page Information:", padx=5, pady=5)
    col_no = 2
    row_no = 5
    for i in range(col_no):
        lbfrm.columnconfigure(i, weight=1)
    for i in range(row_no):
        lbfrm.rowconfigure(i,weight=1)
    lbls = []
    etys = []
    for i, key in enumerate(thePageEdits.keys()):
        thePageEdits[key]=tk.StringVar(value='')
        lbls.append(tk.Label(lbfrm, text=f"{key}"))
        lbls[i].grid(column=0, row=i, sticky="nsew", padx=5, pady=5)
        etys.append(tk.Entry(lbfrm, textvariable=thePageEdits[key]))
        etys[i].grid(column=1, row=i, sticky="ew", padx=5, pady=5)

    theChangePpInfoButton = tk.Button(lbfrm, text="Change it!", command=on_clickToChange, foreground="black", background="pink")
    theChangePpInfoButton.grid(column=0, columnspan=2, row=4, sticky="nsew")
    lbfrm.pack(pady=10, padx=10, expand=True, fill='both')
    theChangePpInfoButton.config(state='disabled')
    return frm

def enableSaveFilesButton() -> None:
    global theSaveFilesButton
    theSaveFilesButton.config(state='active')
def createActionsUI(parent) -> ttk.Frame:
    global theSaveFilesButton

    sp_strvar = tk.StringVar(value=os.path.dirname(os.path.abspath(__file__)))
    def on_saveFiles() -> None:
        global theFilepath
        global thePpInfoStrs
        retlst=[]
        # Go through all pages and make a list pf all page information
        for strvar in thePpInfoStrs:
            retlst.append(strvar.get())
        Doo.gen_toSaveFiles(pdffn=theFilepath, ppInfoLst=retlst, savePath=sp_strvar.get())
    def on_drop(event):
        if os.path.isdir(event.data):
            sp_strvar.set(event.data)
        else:
            sp_strvar.set("Error! Dropped object not a path.")
    frm = ttk.Frame(parent, borderwidth=2, relief='solid')
    lbfrm = ttk.LabelFrame(frm, text="Actions:")
    sp_lbfrm = ttk.LabelFrame(lbfrm, text="Save path:")
    sp_lbl = tk.Label(sp_lbfrm, textvariable=sp_strvar)
    sp_lbfrm.pack(fill='both', padx=10, pady=10)
    sp_lbl.pack()
    sp_lbl.register_drop_target("*")
    sp_lbl.bind("<<Drop>>", on_drop)

    theSaveFilesButton = ttk.Button(lbfrm, text="Save files!", command=on_saveFiles)
    theSaveFilesButton.pack()
    lbfrm.pack(fill='both', padx=10, pady=10)
    theSaveFilesButton.config(state='disabled')
    return frm

def main() -> None:
    theRoot = createRoot()
    theRoot.columnconfigure(0, weight=1)
    theRoot.columnconfigure(1, weight=1)
    theRoot.rowconfigure(0,weight=1)
    theRoot.rowconfigure(1,weight=1)
    fm1 = createOcrSettingUI(parent=theRoot)
    fm1.grid(column=1, row=0, sticky="nsew")
    fm2 = createPdfDisplayUI(parent=theRoot)
    fm2.grid(column=0, row=0, rowspan=3, sticky="nsew")
    fm3 = createPageEditUI(parent=theRoot)
    fm3.grid(column=1, row=1, sticky="nsew")
    fm4 = createActionsUI(parent=theRoot)
    fm4.grid(column=1, row=2, sticky="nsew")
    theRoot.mainloop()

if __name__ == "__main__":
    main()
