import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU
import do_ocr as Doo
import tkinter as tk
from tkinter import ttk
import tkinterDnD as tkdnd
import pymupdf as fitz
from PIL import Image, ImageTk
import re
import threading as th
import time as tm

# App root window
class UI_app(tkdnd.Tk):
    pdfPath = ''
    pageNumber = 0
    pageAttrs = {
        'page no': None,
        'quotation number': None,
        'vendor name': None,
        'paper title': None
    }
    def __init__(self):
        # Read config json
        cwd = os.path.dirname(os.path.abspath(__file__))
        self.configJson = MyU.load_config(f"{cwd}\\config_ocr.json")
        dic = self.configJson.get('gui settings',{})
        aspect = dic['root aspect']
        width = dic['root width']
        height = int(width*int(aspect.split(':')[1])/int(aspect.split(':')[0]))
        # Create root window
        super().__init__()
        self.title('Class DD Pdf')
        self.geometry(f"{width}x{height}")
        # Setup grid
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)
        self.rowconfigure(0,weight=1)
        self.rowconfigure(1,weight=1)
        # Create panels
        self.pn1 = UI_ocrSetting(parent=self)
        self.pn1.grid(column=1, row=0, sticky="nsew")
        self.pn2 = UI_pdfPreview(parent=self)
        self.pn2.grid(column=0, row=0, rowspan=3, sticky="nsew")
        self.pn3 = UI_pageEdit(parent=self)
        self.pn3.grid(column=1, row=1, sticky="nsew")
        self.pn4 = UI_actions(parent=self)
        self.pn4.grid(column=1, row=2, sticky="nsew")
        # Enter app main loop
        self.mainloop()
    # This callback is an inter-panel data exchange method
    def callback(self, command: dict):
        # Once a panel call parent's callback, poll all panels to do command
        self.pn1.on_parentCall(command)
        self.pn2.on_parentCall(command)
        self.pn3.on_parentCall(command)
        self.pn4.on_parentCall(command)

# CREATE OCR SETTINGS PANEL
class UI_ocrSetting(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent, borderwidth=2, relief='solid')
        self.ocrSettings = parent.configJson.get('ocr settings',{})
        # Create OCR type UI
        lf_ocrType = tk.LabelFrame(self, text="OCR type:", padx=5, pady=5)
        lf_ocrType.pack(pady=10, padx=10, expand=True, fill='both')
        self.ocrType = tk.StringVar(value='use_easy')
        radioButtons=[]
        for i, ele in enumerate(self.ocrSettings.get('ocr types',[])):
            radioButtons.append(tk.Radiobutton(lf_ocrType,\
                                               anchor='w',\
                                               text=ele,\
                                               variable=self.ocrType,\
                                               value=ele,\
                                               command=self.on_clickRadioButton)\
                                                )
            radioButtons[i].pack(pady=10, padx=10, expand=True, fill='both')
        # Create Option (log / plain) UI
        lf_ocrOption = tk.LabelFrame(self, text="Option:", padx=5, pady=5)
        lf_ocrOption.pack(pady=10, padx=10, expand=True, fill='both')
        checkButtons=[]
        self.options={}
        self.strVars=[]
        for i, ele in enumerate(self.ocrSettings.get('ocr options',[])):
            self.options[ele] = False
            self.strVars.append(tk.StringVar(value='False'))
            checkButtons.append(tk.Checkbutton(lf_ocrOption,\
                                               anchor='w',\
                                               text=ele,\
                                               variable=self.strVars[i],\
                                               onvalue='True',\
                                               offvalue='False',\
                                               command=self.on_clickRadioButton)\
                                                )
            checkButtons[i].pack(pady=10, padx=10, expand=True, fill='both')
        # Create Pages UI
        lf_pages = tk.LabelFrame(self, text='Pages:', padx=5, pady=5)
        lf_pages.pack(pady=10, padx=10, expand=True, fill='both')
        self.pages = tk.StringVar(value='')
        pages_pages = tk.Entry(lf_pages, textvariable=self.pages)
        pages_pages.pack(pady=10, padx=10, expand=True, fill='both')
        pages_label = tk.Label(lf_pages, text='null(all)  1,2,3  1-3 ')
        pages_label.pack(pady=10, padx=10, expand=True, fill='both')
        # Create "do ocr" button
        self.doOcrBtn = tk.Button(self,text="Do OCR",\
                                   command=self.on_doOcr,\
                                   foreground="black",\
                                   background="lightblue")
        self.doOcrBtn.pack(pady=10, padx=10, expand=True, fill='both')
        self.doOcrBtn.config(state='disabled')

    def on_clickRadioButton(self):
        for i, key in enumerate(self.options.keys()):
            self.options[key]= True if self.strVars[i].get()=='True' else False

    # Call do_ocr.py.iterateInPdf() when Do OCR button pressed
    def on_doOcr(self):
        pps = self.pages.get().replace(' ','')
        if not pps:
            batch_list=list(range(1,(self.master.pageNumber+1)))
            print(f"Do all pages")
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
            'pdf path': self.master.pdfPath,
            'ocr_type': self.ocrType.get(),
            'batch': batch_list,
            'do_log': self.options['log'],
            'do_plain': self.options['plain'],
            'num of pages': len(batch_list)
        }
        # DO OCR!
        pop = ui_popup(parent=self.master, ocr_args=ocr_args)
    def on_parentCall(self, msg: dict):
        if 'enableDoOcrBtn' in msg['command']:
            self.doOcrBtn.config(state='active')
        if 'disableDoOcrBtn' in msg['command']:
            self.doOcrBtn.config(state='disabled')

class ui_progressbar(ttk.Progressbar):
    def __init__(self, parent, ori, lnth, md, max):
        super().__init__(master=parent, orient=ori, length=lnth, mode=md, maximum=max)

class ui_popup(tk.Toplevel):
    def __init__(self, parent, ocr_args):
        super().__init__(parent, border=1, borderwidth=2)
        x = parent.winfo_rootx()
        y = parent.winfo_rooty()
        self.geometry(f"300x200+{x+50}+{y+50}")
        self.protocol("WM_DELETE_WINDOW", self.on_closeWindow)
        self.frame = tk.Frame(self, border=1, borderwidth=10, padx=5, pady=5)
        self.frame.pack(fill='both', expand=True)
        self.progbar=ui_progressbar(self.frame,\
                                    ori="horizontal",\
                                    lnth=100,\
                                    md='determinate',\
                                    max=ocr_args['num of pages']\
                                    )
        self.progbar.pack(expand=True, fill='x', pady=10)
        self.strVar = tk.StringVar(self.frame,\
                                   value=f"Progress: 0/{self.progbar.cget(key='maximum')}"\
                                   )
        self.lbl = tk.Label(self.frame, textvariable=self.strVar)
        self.lbl.pack(fill='both', expand=True, padx=10, pady=10)
        self.btn = tk.Button(self.frame,text="Abort", command=self.to_stop_t)
        self.btn.pack()
        self.the_t = th.Thread(target=lambda: self.proc_ocr(ocr_args))
        self.let_t_go = True
        self.the_t.start()

    def proc_ocr(self, ocr_args):
        # Call generator coroutine at Doo
        r = Doo.gen_iterateInPdf(pdffn=ocr_args['pdf path'],\
                                ocr_type=ocr_args['ocr_type'],\
                                batch=ocr_args['batch'],\
                                do_log=ocr_args['do_log'],\
                                do_plain=ocr_args['do_plain'])
        # Initialize page index (counting from zero)
        i = 0
        num_of_pages = self.progbar.cget(key='maximum')
        while True:
            # Get ocr result sequentially page by page
            p = next(r)
            # Null (or None) means ocr finished
            if not p:
                break
            else:
                pno = int(p.split('\n')[0].split('.')[1])
                self.master.callback({'command': 'setPageInfoStrs',\
                                      'index': (pno-1), 'value': p})
                self.progbar.config(value=i+1)
                self.strVar.set(value=f"Progress: {i+1}/{num_of_pages}")
                self.update()
            i += 1
            # Just in case
            if i > 1000:
                break
            # Aborted from UI
            if not self.let_t_go:
                self.strVar.set(value="Abort, breaking...")
                break
        self.strVar.set(value="Finished.")
        tm.sleep(1)
        self.destroy()

    def to_stop_t(self):
        self.let_t_go = False

    def on_closeWindow(self):
        self.to_stop_t()

# CREATE PDF PREVIEW PANEL
class UI_pdfPreview(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent, borderwidth=2, relief='solid')
        self.cnvs = tk.Canvas(self, borderwidth=0, relief='solid')
        scrbar = tk.Scrollbar(self, orient="vertical", command=self.cnvs.yview)
        self.fram_scrbar = tk.Frame(self.cnvs,\
                               borderwidth=0,\
                               relief='solid',\
                               padx=10,\
                               pady=10)
        self.fram_scrbar.bind("<Configure>",\
                         lambda e: self.cnvs.configure(scrollregion=self.cnvs.bbox("all")))
        self.cnvs.create_window((0,0), window=self.fram_scrbar, anchor="nw")
        self.cnvs.configure(yscrollcommand=scrbar.set)
        scrbar.config(command=self.cnvs.yview)
        self.cnvs.register_drop_target("*")
        self.cnvs.bind("<<Drop>>", self.on_drop)
        self.cnvs.pack(side="left", fill="both", expand=True)
        scrbar.pack(side="right", fill="y")
        self.cnvs.bind("<MouseWheel>", self.on_mouseWheel)
        self.pageInfoLbls=[]  # preview attr labels
        self.pageImgLbls=[]   # preview image labels
        self.pageInfoStrs=[]  # page info stringVars

    def make_labels(self, img=None, ppno=0):
        ppno_lbl = tk.Label(self.fram_scrbar)
        img_tk = ImageTk.PhotoImage(img)
        img_lbl = tk.Label(self.fram_scrbar, image=img_tk)
        img_lbl.image = img_tk
        img_lbl.bind("<Button-1>", self.on_leftClick)
        return img_lbl, ppno_lbl
    #  Iterate all pages in pdf
    def show_pdf_images(self, doc=None, zoom=1.0)->int:
        mtrx = fitz.Matrix(zoom, zoom)
        for i in range(doc.page_count):
            pp = doc.load_page(i)
            pix = pp.get_pixmap(matrix=mtrx)
            img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
            iL, pL = self.make_labels(img=img,ppno=(i+1))
            self.pageImgLbls.append(iL)
            self.pageInfoLbls.append(pL)
            sss = f"page.{i+1}\n" + f"unknownQn\n" + f"unknownVn\n" + f"unknownTt"
            self.pageInfoStrs.append(tk.StringVar(value=sss))
            self.pageInfoLbls[i].config(textvar=self.pageInfoStrs[i])
            self.pageImgLbls[i].grid(column=0, row=i)
            self.pageInfoLbls[i].grid(column=1, row=i)
        self.fram_scrbar.update_idletasks()
        self.cnvs.config(scrollregion=self.cnvs.bbox("all"))
        return i+1
    # To receive a dropped pdf file
    def resetPdf(self):
        if len(self.pageImgLbls):
            for im in self.pageImgLbls:
                im.destroy()
            del(self.pageImgLbls[:])
        if len(self.pageInfoLbls):
            for n in self.pageInfoLbls:
                n.destroy()
            del(self.pageInfoLbls[:])
        if len(self.pageInfoStrs):
            for p in self.pageInfoStrs:
                p.set('')
            del(self.pageInfoStrs[:])
        for key in self.master.pageAttrs.keys():
            self.master.pageAttrs[key].set('')
    def on_drop(self, event):
        try:
            self.master.pdfPath = event.data
            theDoc = fitz.open(self.master.pdfPath)
            self.master.pageNumber = theDoc.page_count
            self.resetPdf()
            thbn_zoom = self.master.configJson.get('gui settings',{})['thumbnail zoom']
            n = self.show_pdf_images(doc=theDoc, zoom=thbn_zoom)
            # enableDoOcrButton()
            # enableSaveFilesButton()
            self.master.callback({'command': 'enableDoOcrBtn', 'arg': None})
            self.master.callback({'command': 'enableSaveFilesBtn', 'arg': None})
        except Exception as e:
            print(f"drop() Error={e}")
        finally:
            theDoc.close()
    #  Mouse wheel scroll
    def on_mouseWheel(self, event):
        self.cnvs.yview_scroll(number=int((-1 * event.delta)/120), what=tk.UNITS)
    # Mouse left click
    def on_leftClick(self, event):
        dic = {}
        ls = self.pageInfoStrs[self.pageImgLbls.index(event.widget)].get().split('\n')
        for i, key in enumerate(self.master.pageAttrs.keys()):
            dic[key] = ls[i]
        # to_updatePageEdit(pp_dic=dic)
        self.master.callback({'command': 'updatePageEdit', 'arg': dic})

    def on_parentCall(self, msg: dict):
        if 'setPageInfoStrs' in msg['command']:
            index = msg['index']
            value = msg['value']
            self.pageInfoStrs[index].set(value=value)
        if 'getPageInfoStrs' in msg['command']:
            proc = msg['rx']
            proc(self.pageInfoStrs)

# CREATE PAGE EDIT PANEL
class UI_pageEdit(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent,\
                         borderwidth=2,\
                         relief='solid'\
                            )
        self.lbfrm = tk.LabelFrame(self, text="Page Information:", padx=5, pady=5)
        col_no = 2
        row_no = 5
        for i in range(col_no):
            self.lbfrm.columnconfigure(i, weight=1)
        for i in range(row_no):
            self.lbfrm.rowconfigure(i,weight=1)
        lbls = []
        etys = []
        for i, key in enumerate(self.master.pageAttrs.keys()):
            self.master.pageAttrs[key]=tk.StringVar(value='')
            lbls.append(tk.Label(self.lbfrm, text=f"{key}"))
            lbls[i].grid(column=0, row=i, sticky="nsew", padx=5, pady=5)
            etys.append(tk.Entry(self.lbfrm, textvariable=self.master.pageAttrs[key]))
            etys[i].grid(column=1, row=i, sticky="ew", padx=5, pady=5)
        self.changePpInfoBtn = tk.Button(self.lbfrm,\
                                          text="Change it!",\
                                          command=self.on_clickToChange,\
                                          foreground="black",\
                                          background="pink"\
                                          )
        self.changePpInfoBtn.grid(column=0, columnspan=2, row=4, sticky="nsew")
        self.lbfrm.pack(pady=10, padx=10, expand=True, fill='both')
        self.changePpInfoBtn.config(state='disabled')

    def on_clickToChange(self):
        pn = self.master.pageAttrs['page no']
        pnlst = pn.get().split('.')
        ppno = int(pnlst[1])
        qn = self.master.pageAttrs['quotation number'].get()
        vn = self.master.pageAttrs['vendor name'].get()
        tt = self.master.pageAttrs['paper title'].get()
        ppinfo = f"page.{ppno}\n"+f"{qn}\n"+f"{vn}\n"+f"{tt}"
        # self.master.pageInfoStrs[ppno-1].set(ppinfo)
        self.master.callback({'command': 'setPageInfoStrs',\
                              'index':(ppno-1),\
                              'value': ppinfo})
    def to_updatePageEdit(self, pp_dic=None):
        for key in self.master.pageAttrs.keys():
            self.master.pageAttrs[key].set(pp_dic[key])
        self.changePpInfoBtn.config(state='active')

    def on_parentCall(self, msg: str):
        if 'updatePageEdit' in msg['command']:
            self.to_updatePageEdit(pp_dic=msg['arg'])

# CREATE ACTIONS PANEL
class UI_actions(ttk.Frame):
    def __init__(self, parent):
        super().__init__(master=parent, borderwidth=2, relief='solid')
        self.savePath = tk.StringVar(value=os.path.dirname(os.path.abspath(__file__)))
        lbfrm = ttk.LabelFrame(self, text="Actions:")
        sp_lbfrm = ttk.LabelFrame(lbfrm, text="Save path:")
        sp_lbl = tk.Label(sp_lbfrm, textvariable=self.savePath)
        sp_lbfrm.pack(fill='both', padx=10, pady=10)
        sp_lbl.pack()
        sp_lbl.register_drop_target("*")
        sp_lbl.bind("<<Drop>>", self.on_drop)

        self.saveFilesBtn = ttk.Button(lbfrm,\
                                       text="Save files!",\
                                       command=self.on_saveFiles)
        self.saveFilesBtn.pack()
        lbfrm.pack(fill='both', padx=10, pady=10)
        self.saveFilesBtn.config(state='disabled')

    def on_saveFiles(self):
        # Callback function to receive pageInfoStrs and iterate it
        def rx_proc(v: list):
            retlst=[]
            # Go through all pages and make a list pf all page information
            for strvar in v:
                retlst.append(strvar.get())
            Doo.gen_toSaveFiles(pdffn=self.master.pdfPath,\
                                ppInfoLst=retlst,\
                                savePath=self.savePath.get())
        # Get page info strs from pdfPreview panel
        self.master.callback({'command': 'getPageInfoStrs', 'rx': rx_proc})

    def on_drop(self, event):
        if os.path.isdir(event.data):
            self.savePath.set(event.data)
        else:
            self.savePath.set("Error! Dropped object not a path.")

    def on_parentCall(self, msg: str):
        if 'enableSaveFilesBtn' in msg['command']:
            self.saveFilesBtn.config(state='active')
        if 'disableSaveFilesBtn' in msg['command']:
            self.saveFilesBtn.config(state='disabled')

UI_app=UI_app()