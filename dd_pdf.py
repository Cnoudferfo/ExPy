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
def disp_text_widget(txt_wdgt, str):
    txt_wdgt.config(state=tk.NORMAL)
    txt_wdgt.delete(1.0, tk.END)
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
    page_str = ot.ReadImage(img)
    return page_str.split('\n')

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
    elif len(sys.argv) == 2 and sys.argv[1] == 'use_easyocr':
        import ocr_easyocr as ot  # Warning! Not comply with python convention
    else:
        print(f"Usage: python {os.path.basename(__file__)} ocr_option")
        print(f"    ocr_option: [use_tess] tesseract, [use_easyocr] EasyOCR")
        exit(-1)

    ot.Init()  # To initialize ocr engine

    attr_dic_from_json = MyU.loadPageAttrFromJson()
    if attr_dic_from_json == None:
        exit(-1)

    root = tkinterDnD.Tk()
    root.title("綜合PDF整理器")
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
            fpath = ''

            # Define test specifications, zoom and cw rotation in degrees
            # TODO : modify testSpecs according to the real pdf's page directions
            testSpecs = [{'zoom': 1.5, 'cw': 0},
                         {'zoom': 1.5, 'cw': 270},
                         {'zoom': 1.8, 'cw': 270},
                         {'zoom': 1.8, 'cw': 0}]

            # To prepare one page pdf's filepath
            # reset leading quotation number & vendor name
            lead_qn = ''
            lead_vn = ''

            def IS_PASS_THIS_SPEC(page_number, test_count):
                if (page_number % 4) == 0:
                    use_spec = 1 # testSpecs[0] = cw0
                elif (page_number % 3) == 0:
                    use_spec = 2 # testSpecs[1] = cw270
                elif (page_number % 2) == 0:
                    use_spec = 2 # testSpecs[1] = cw270
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

                    # TODO : Remove this temp operation
                    # Rotate the page according to test file's page placement
                    if IS_PASS_THIS_SPEC(page_number=(i+1), test_count=j) == True:
                        continue

                    zoomV = ts['zoom']
                    cwV = ts['cw']
                    print(f"drop():parse page{i+1} at zoom={zoomV}, cw={cwV}")
                    pp_strs = parse_a_page(page=pp, zoom=zoomV, cw=cwV)  # To parse this page to strings

                    # TEMP !
                    save_one_page(filename=f"./test_data/real_uncover_p{i+1}.pdf", page=pp)
                    # TEMP !

                    tested_dic = MyU.testAttrTokens(attr_dic=attr_dic_from_json, page_strings=pp_strs)
                    if tested_dic != None:  # One of the age strings hit
                        t_qn = tested_dic['quotation number']
                        t_vn = tested_dic['vendor name']
                        t_ti = tested_dic['title']

                        # TODO : To refine attribution registration logic
                        # if t_qn != '' and lead_qn == '':
                        #     lead_qn = t_qn
                        # if t_vn != '' and lead_vn == '':
                        #     lead_vn = t_vn
                        if lead_qn=='' and lead_vn=='':
                            if t_qn!='' and t_vn!='':
                                lead_qn = t_qn
                                lead_vn = t_vn
                        if lead_qn!='' and lead_vn!='':
                            if t_qn!='' and t_vn!='':
                                if t_qn != lead_qn and t_vn != lead_vn:
                                    lead_qn = t_qn
                                    lead_vn = t_vn

                        print(f"drop() page{i+1} hit! title={t_ti}, vendor name={t_vn}, quotation number={t_qn}")
                        break

                # TODO : Overcome NO HIT logic
                # FOR NOW, LET "if tested_dic == None" BE THE NO HIT! CONDITION
                # if j == len(testSpecs) and tested_dic == None: # No hit
                if tested_dic == None:
                    if lead_qn != '' and lead_vn != '':
                        # To save one page file
                        fpath = f"./test_data/{lead_qn}_{lead_vn}_會議記錄.pdf"
                        # ret = save_one_page(filename = fpath, page = pp)
                        # print(f"save_one_page({fpath},pp) returned {ret}")

                        # Reset the leading quotation number & vendor name
                        # DOING : Overcome the reset condition of leading qn & vn
                        # lead_qn = ''
                        # lead_vn = ''
                    else:
                        print("FATAL ERROR! NO HIT PAGE WITHOUT LEADING QN or VN!")
                else:
                    # TODO : Add transaction page disorder logic

                    # FOR NOW, TEST FILEIS WELL ORDERED!
                    if lead_qn != '' and lead_vn != '' and t_ti != '':
                        # To save the one page file
                        fpath = f"./test_data/{lead_qn}_{lead_vn}_{t_ti}.pdf"
                        # ret = save_one_page(filename = fpath, page = pp)
                        # print(f"save_one_page({fpath},pp) returned {ret}")
                    else:
                        print("FATAL ERROR! HIT PAGE WITHOUT LEADING QN or VN!")

                text += f"Dbg: page{i+1} was parsed {j} times, file={fpath} will be saved.\n"
                # for s in pp_strs:
                #     if s != '':
                #         clean_str = MyU.remove_all_whitespaces(s)
                #         print(f"Dbg: page{i} : {clean_str}")

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