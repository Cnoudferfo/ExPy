import os
import sys
from PIL import Image
import pymupdf as pmpdf
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU

ocr_engine = None

def use_tess():
    global ocr_engine
    print("Use tesseract")
    import ocr_tesseract as ocr_engine  # Warning! Not comply with python convention

def use_easyocr():
    global ocr_engine
    print("Use EasyOCR")
    import ocr_easyocr as ocr_engine  # Warning! Not comply with python convention

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

    # Parse a pdf page's text strings
def parse_a_page(page, zoom=1.2, cw = 0, attr_dic = None):  # cw : counter-clockwise rotation in 0-90-270-degree
    global ocr_engine
    if not isinstance(page, pmpdf.Page):
        raise ValueError("parse_a_page() must receive a PyMuPDF page object")
    page.set_rotation(cw)
    mtrx = pmpdf.Matrix(zoom, zoom)  # To set a zoomed matrix
    page_pix = page.get_pixmap(matrix=mtrx)  # To get pixmap of page
    img = Image.frombytes("RGB", [page_pix.width, page_pix.height], page_pix.samples)  # Convert pixmap to image

    vocabulary = MyU.makeVocabulary(attr_dic=attr_dic)
    page_str, page_cf = ocr_engine.ReadImage(image=img, vocabulary=vocabulary)

    return page_str.split('\n'), page_cf

# An entry point of ocr processing
def Do_ocr(pdfFilePath='', pgCommand = None):
    global ocr_engine

    if ocr_engine == None:
        print(f"Do_ocr() Error: OCR object=None")
        return -1

    ocr_engine.Init()

    # Load page attributions from json
    attr_dic_from_json = MyU.loadPageAttrFromJson()
    if attr_dic_from_json == None:
        return -1

    # Validate the PDF file
    pdf = pmpdf.open(pdfFilePath)  # To open pdf file

    if pgCommand != None:
        pgCommand(maximum=pdf.page_count)

    text = 'OCR result ' + '\n'
    op_fpath = '' # One page (output) file name

    # Define test specifications, zoom and cw rotation in degrees
    # TODO : modify testSpecs according to the real pdf's page directions
    testSpecs = [{'zoom': 2.5, 'cw': 0}, {'zoom': 2.5, 'cw': 90}, {'zoom': 2.5, 'cw': 180}, {'zoom': 2.5, 'cw': 270}]

    # To prepare one page pdf's filepath
    # reset leading quotation number & vendor name
    lead_qn = ''
    lead_vn = ''

    def IS_PASS_THIS_SPEC(page_number, test_count):
        # WARNING! THIS IS A HARD CODING LOGIC ACCORDING TO CERTAIN TEST PDF
        if (page_number % 4) == 2 or (page_number % 4) == 3:
            use_spec = 4 # testSpecs[1] = cw270
        else:
            use_spec = 1 # testSpecs[0] = cw0
        # skip or not
        if test_count != use_spec:
            return True # SKIP
        else:
            return False # DON'T SKIP

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
            tested_dic = MyU.testTokensInOnePage(attr_dic=attr_dic_from_json, page_strings=pp_strs)
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
                op_fpath = f"./test_data/{lead_qn}_{lead_vn}_會議記錄.pdf"
                # ret = save_one_page(filename = fpath, page = ppcopy)
                # print(f"save_one_page({fpath},ppcopy) returned {ret}")

            else:
                print("FATAL ERROR! NO HIT PAGE WITHOUT LEADING QN or VN!")
        else:
            # TODO : Add transaction page disorder logic

            # FOR NOW, TEST FILEIS WELL ORDERED!
            if lead_qn != '' and lead_vn != '' and t_ti != '':
                # To save the one page file
                op_fpath = f"./test_data/{lead_qn}_{lead_vn}_{t_ti}.pdf"
                # ret = save_one_page(filename = fpath, page = ppcopy)
                # print(f"save_one_page({fpath},ppcopy) returned {ret}")
            else:
                print("FATAL ERROR! HIT PAGE WITHOUT LEADING QN or VN!")

        text += f"Dbg: page{i+1} was parsed {j} times, file=\"{op_fpath}\"   will be saved.\n"

        # To update progress bar
        if pgCommand != None:
            pgCommand(value = i+1)

    if pgCommand != None:
        pgCommand(text = text)

def openPDF(fn=''):
    if not os.path.isfile(fn) or 'pdf' not in fn:
        print(f"Wrong! {fn} is NOT a pdf file!")
        return None
    pdf = pmpdf.open(filename=fn)
    print(f"openPDF() open : {fn}.")
    return pdf

def saveMyOnePage(index=0,page=None):
    if (index % 4) == 2 or (index % 4) == 3:
        # cw = 270
        cw = 90
    else:
        cw = 0
    page.set_rotation(cw)
    print(f"index={index}, cw={cw}")

    fn = f".\\test_data\\page_{index}.pdf"
    print(f"processPage() to save : {fn}.")
    return save_one_page(filename=fn, page=page)
    # return 0

# Yet, another entry point of ocr process
def doMyOnePage(index=0, page=None, attr_dic=None):
    pp_strs, pp_cf = parse_a_page(page=page, zoom=2.0, cw=0, attr_dic=attr_dic) # Set only zoom factor, 2.0 should be the best
    print(f"pp_strs={pp_strs}")
    print(f"pp_cf={pp_cf}")
    page_dic = MyU.testTokensInOnePage(attr_dic=attr_dic, page_strings=pp_strs)
    if page_dic != None:
        print(f"ti={page_dic['title']}, vn={page_dic['vendor name']}, qn={page_dic['quotation number']} ")
    else:
        print("Page didn't hit!")
    return 0


def iterateInOnePdf(pdf=None, command=None):
    if pdf==None:
        return None
    attr_dic = MyU.loadPageAttrFromJson()
    for i in range(pdf.page_count):
        page = pdf.load_page(i)
        if command==None:
            return None
        command(index=(i+1), page=page, attr_dic=attr_dic)
    return 0

def main():
    global ocr_engine

    if len(sys.argv) == 3 and sys.argv[2] == 'use_tess':
        use_tess()
    elif len(sys.argv) == 3 and sys.argv[2] == 'use_easy':
        use_easyocr()
    else:
        print(f"Usage: python {os.path.basename(__file__)} pdf_filenpath ocr_option")
        print(f"    ocr_option: [use_tess] tesseract, [use_easy] EasyOCR")
        exit(-1)

    pdf = openPDF(fn=sys.argv[1])
    if pdf==None:
        exit(-1)


    ocr_engine.Init()
    iterateInOnePdf(pdf=pdf, command=doMyOnePage)
    return 0

if __name__ == "__main__":
    main()