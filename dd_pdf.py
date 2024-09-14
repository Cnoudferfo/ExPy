import os
import tkinter as tk
from tkinter import font
from tkinter import ttk
import tkinterDnD
from PIL import Image
import pymupdf as pmpdf
import re  # To use regular expression
import json
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU

ot = None  # OCR object (tesseract or easyocr)

# Dsiplay a string in text widget
def tw_set_string(txt_wdgt, str):
    txt_wdgt.config(state=tk.NORMAL)
    txt_wdgt.delete(1.0, tk.END)
    txt_wdgt.insert(tk.END, str)
    txt_wdgt.config(state=tk.DISABLED)

def tw_insert_string(txt_wdgt, str):
    txt_wdgt.config(state=tk.NORMAL)
    txt_wdgt.insert(tk.END, str)
    txt_wdgt.config(state=tk.DISABLED)

# Parse a pdf page's text strings
def parse_a_page(page, zoom=1.2, cw = 0):  # cw : counter-clockwise rotation in 0-90-270-degree
    global ot
    if not isinstance(page, pmpdf.Page):
        raise ValueError("parse_a_page() must receive a PyMuPDF page object")
    page.set_rotation(cw)
    mtrx = pmpdf.Matrix(zoom, zoom)  # To set a zoomed matrix
    page_pix = page.get_pixmap(matrix=mtrx)  # To get pixmap of page
    img = Image.frombytes("RGB", [page_pix.width, page_pix.height], page_pix.samples)  # Convert pixmap to image
    page_str, page_cf = ot.ReadImage(img)

    return page_str.split('\n'), page_cf

# Save the page
def save_one_page(filename='', page=None):
    if filename == '' or page == None:
        return -1

    new_pdf = pmpdf.open()
    new_pdf.insert_pdf(page.parent, from_page=page.number, to_page=page.number)
    new_pdf.save(filename)
    new_pdf.close()
    return 0

def ya_save_one_page(vendor_name, quo_number, title, page):
    if page == None:
        return -1
    if title != '':
        fpath = f"./test_data/{quo_number}_{vendor_name}_{title}.pdf"
    else:
        fpath = f"./test_data/{quo_number}_{vendor_name}_會議記錄.pdf"

    return save_one_page(filename=fpath, page=page)

def main():
    global ot
    if len(sys.argv) == 2 and sys.argv[1] == 'use_tess':
        import ocr_tesseract as ot  # Warning! Not comply with python convention
    elif len(sys.argv) == 2 and sys.argv[1] == 'use_easy':
        import ocr_easyocr as ot  # Warning! Not comply with python convention
    else:
        print(f"Usage: python {os.path.basename(__file__)} ocr_option")
        print(f"    ocr_option: [use_tess] tesseract, [use_easy] EasyOCR")
        exit(-1)

    ot.Init()  # To initialize ocr engine

    attr_dic_from_json = MyU.loadPageAttrFromJson()
    if attr_dic_from_json == None:
        exit(-1)

    root = tkinterDnD.Tk()
    root.title("綜合PDF整理器")
    root.geometry("1000x750")  # Adjust the size as needed

    def drop(event):  # This function is called, when stuff is dropped into a widget
        try:
            # Validate the dropped object
            if not os.path.isfile(event.data) or 'pdf' not in event.data:
                tw_set_string(text_widget, f"Wrong! {event.data} is NOT a pdf file!")
                return

            pdf = pmpdf.open(event.data)  # To open pdf file

            # Before process a valid event
            progress_bar.config(mode='determinate', maximum=pdf.page_count)  # To set a progress bar
            progress_bar.start()
            tw_set_string(text_widget, f"{event.data}    processing...")  # Update display message

            text = 'OCR result ' + '\n'
            fpath = ''

            # Define test specifications, zoom and cw rotation in degrees
            # TODO : modify testSpecs according to the real pdf's page directions
            testSpecs = [{'zoom': 2.5, 'cw': 0},
                         {'zoom': 2.5, 'cw': 90},
                         {'zoom': 2.5, 'cw': 180},
                         {'zoom': 2.5, 'cw': 270}]

            # To prepare one page pdf's filepath
            # reset leading quotation number & vendor name
            lead_qn = ''
            lead_vn = ''

            def IS_PASS_THIS_SPEC(page_number, test_count):
                if (page_number % 4) == 2 or (page_number % 4) == 3:
                    use_spec = 4 # testSpecs[1] = cw270
                else:
                    use_spec = 1 # testSpecs[0] = cw0

                if test_count != use_spec:
                    return True
                else:
                    return False

            # For each page in pdf
            for i in range(pdf.page_count):  # Use PyMuPdf
                # Perform OCR
                pp = pdf.load_page(i)  # To load the i-th page

                j = 0     # test count
                for ts in testSpecs:   # To test a page in different specs if needed
                    j += 1

                    # # TODO : Remove this temp operation
                    # # Rotate the page according to test file's page placement
                    # if IS_PASS_THIS_SPEC(page_number=(i+1), test_count=j) == True:
                    #     continue

                    # Doubt about is multiple rotation damage the page image?
                    ppcopy = pp

                    zoomV = ts['zoom']
                    cwV = ts['cw']
                    # pp_strs = parse_a_page(page=pp, zoom=zoomV, cw=cwV)  # To parse this page to strings
                    pp_strs, pp_cf = parse_a_page(page=ppcopy, zoom=zoomV, cw=cwV)  # To parse this page to strings
                    print(f"drop(): page{i+1} parsed at zoom={zoomV}, cw={cwV}, strs_len={len(pp_strs)}, cf={pp_cf:.4f}")
                    if pp_cf < 0.3:
                        continue
                    tested_dic = MyU.testAttrTokens(attr_dic=attr_dic_from_json, page_strings=pp_strs)
                    if tested_dic != None:  # One of the age strings hit
                        t_qn = tested_dic['quotation number']
                        t_vn = tested_dic['vendor name']
                        t_ti = tested_dic['title']

                        # TODO : To refine attribution registration logic
                        if lead_qn=='' and lead_vn=='':
                            if t_qn!='' and t_vn!='':
                                lead_qn = t_qn
                                lead_vn = t_vn
                        if lead_qn!='' and lead_vn!='':
                            if t_qn!='' and t_vn!='':
                                if t_qn != lead_qn:
                                    lead_qn = t_qn
                                    lead_vn = t_vn

                        # To prevent useless rotation
                        if t_ti != '':
                            print(f"drop() page{i+1} hit! title={t_ti}, vendor name={t_vn}, quotation number={t_qn}")
                            break
                        else:
                            tested_dic = None

                # TODO : Overcome NO HIT logic
                # FOR NOW, LET "if tested_dic == None" BE THE NO HIT! CONDITION
                # if j == len(testSpecs) and tested_dic == None: # No hit
                if tested_dic == None:
                    if lead_qn != '' and lead_vn != '':
                        # To save one page file
                        fpath = f"./test_data/{lead_qn}_{lead_vn}_會議記錄.pdf"
                        # ret = save_one_page(filename = fpath, page = ppcopy)
                        # print(f"save_one_page({fpath},ppcopy) returned {ret}")

                    else:
                        print("FATAL ERROR! NO HIT PAGE WITHOUT LEADING QN or VN!")
                else:
                    # TODO : Add transaction page disorder logic

                    # FOR NOW, TEST FILEIS WELL ORDERED!
                    if lead_qn != '' and lead_vn != '' and t_ti != '':
                        # To save the one page file
                        fpath = f"./test_data/{lead_qn}_{lead_vn}_{t_ti}.pdf"
                        # ret = save_one_page(filename = fpath, page = ppcopy)
                        # print(f"save_one_page({fpath},ppcopy) returned {ret}")
                    else:
                        print("FATAL ERROR! HIT PAGE WITHOUT LEADING QN or VN!")

                text += f"Dbg: page{i+1} was parsed {j} times, file={fpath} will be saved.\n"

                # To update progress bar
                progress_bar['value'] = i+1
                root.update_idletasks()

            # To display OCR result
            tw_set_string(text_widget, text)

        except Exception as e:
            # Display error message
            tw_set_string(text_widget, f"Error: {e}")

        finally:
            # Stop the progress bar
            progress_bar.stop()

    # Define font size and calculate padding
    label_font = font.Font(family="Helvetica", size=12)
    line_height = label_font.metrics("linespace")
    padding = line_height // 8

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
    # text_widget.insert(tk.END, 'Drop a PDF file here.')
    # text_widget.config(state=tk.DISABLED)
    tw_insert_string(txt_wdgt=text_widget, str="Drop a PDF here.")
    # Bind drop event to text widget
    text_widget.register_drop_target("*")
    text_widget.bind("<<Drop>>", drop)

    # Configure the scrollbar
    scrollbar.config(command=text_widget.yview)

    root.mainloop()

if __name__ == "__main__":
    main()