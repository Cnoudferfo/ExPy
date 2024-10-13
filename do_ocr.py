import os
import sys
from PIL import Image
import pymupdf as pmpdf
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as MyU
import re

ocr_engine = None
ocr_type = 'tess'

def use_tess():
    global ocr_engine
    print("Use tesseract")
    import ocr_tesseract as ocr_engine  # Warning! Not comply with python convention

def use_easyocr():
    global ocr_engine
    global ocr_type
    print("Use EasyOCR")
    import ocr_easyocr as ocr_engine  # Warning! Not comply with python convention
    ocr_type = 'easyocr'

# Get page image
def getPageImg(page, zoom):
    mtrx = pmpdf.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mtrx)
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)
    return img

# Save the page
def save_one_page(filename='', page=None, rotate=0) -> int:
    if filename == '' or page == None:
        return -1
    new_pdf = pmpdf.open()
    new_pdf.insert_pdf(page.parent, from_page=page.number, to_page=page.number, rotate=rotate)
    new_pdf.save(filename)
    new_pdf.close()
    return 0
def ya_save_one_page(vendor_name, quo_number, title, page, savePath, ccw=0, group_idx='') -> int:
    if page == None:
        return -1
    fpath = f"{savePath}\\Qn{quo_number}_No{group_idx}_{vendor_name}_{title}.pdf"
    print(f"fpath={fpath}")
    cw = 0
    if ccw==90:
        cw = 270
    elif ccw==270:
        cw = 90
    else:
        pass
    return save_one_page(filename=fpath, page=page, rotate=cw)
def openPDF(fn=''):
    pdf = pmpdf.open(filename=fn)
    print(f"openPDF() open : {fn}.")
    return pdf
def saveMyOnePage(index=0,page=None):
    if (index % 4) == 2 or (index % 4) == 3:
        cw = 90
    else:
        cw = 0
    page.set_rotation(cw)
    fn = f".\\test_data\\page_{index}.pdf"
    return save_one_page(filename=fn, page=page)
def testTokenInPage(tok='', ppStr=''):
    ss = 0
    pageLen = len(ppStr)
    tokenLen = len(tok)
    pos_start = 0
    if tokenLen > 8:
        threshold = 1 - (2 / tokenLen) # Permit for 2 unmatach word
    elif tokenLen > 3:
        threshold = 1 - (1 / tokenLen) # Permit for 1 unmatach word
    else:
        threshold = 1 - (0 / tokenLen) # Permit for 0 unmatach word
    while pos_start < pageLen:
        # Get a clean string according to token length
        testStr = ppStr[pos_start:(pos_start+tokenLen)]
        ss = MyU.CalcStringSimilarity(tokenStr=tok, testStr=testStr)
        if ss >= threshold:
            return ss, pos_start
        # Increment start position index
        pos_start += 1
    return 0, 0

def cutPage(ppStr='', pos_start=0, cutLen=0):
    # Cut and cascade page text
    sub1 = ppStr[0:pos_start]
    sub2 = ppStr[(pos_start+cutLen):len(ppStr)]
    ppStr = sub1 + sub2
    return ppStr

def testAndCut(tok='', ppStr=''):
    ss, pos_start = testTokenInPage(tok=tok, ppStr=ppStr)
    if ss:
        ppStr = cutPage(ppStr=ppStr, pos_start=pos_start, cutLen=len(tok))
    return ppStr, ss

# Yet, another entry point of ocr process
def doMyOnePage(page=None, attr_dic=None, page_no=0):
    global ocr_engine
    global ocr_type
    # Check page
    if not isinstance(page, pmpdf.Page):
        raise ValueError("{__name__}, page NOT PDF!")
    # SET ZOOM FACTOR
    zoomAtPdf = 2.5
    # Get page image
    pp_img = getPageImg(page=page, zoom=zoomAtPdf)
    # Result
    result_dic = {
        'title': '',
        'vendor name': '',
        'quotation number': '',
        'page conf': 0,
        'ccw degree': 360
    }
    # Yet another result
    resultBuffer = {
        'title': {'text': '', 'ss': 0.0},
        'vendor name': {'text': '', 'ss': 0.0},
        'quotation number': {'text': '', 'ss': 0.0}
    }
    qnInPage = ''
    # Define escape titles to try to speed up
    EscapeTitles = [
        "電子發票證明聯",
        "統一發票",
        "檢查結果連絡書",
        "模具修繕申請表",
        "金型修正指示書",
        "設計變更連絡書",
        "設計變更聯絡書",
        "模具資產管理卡"
    ]

    if ocr_type=='tess':
        minconf = 50
        zoomList = [0.4, 0.6, 1.0]    # for Easy OCR
        ccw_list = [0, 90, 180, 270]  # for Easy OCR
    else:
        minconf = 15
        zoomList = [1.0]    # for Easy OCR
        ccw_list = [90, 0, 270]  # for Easy OCR

    for zoomAtCv2 in zoomList:
        for ccw_degree in ccw_list:
            # Do OCR
            page_conf, str = ocr_engine.ReadImage(image=pp_img,\
                                                  ccw=ccw_degree,\
                                                  zoom=zoomAtCv2)
            page_text = MyU.remove_punctuation(MyU.remove_all_whitespaces(s=str))
            if ocr_type == 'easyocr':
                page_conf *= 100

            # DEBUG
            MyU.log_text(f"pp.{page_no},conf={page_conf},zm={zoomAtCv2},ccw={ccw_degree},pptxt={page_text}")

            # SKIP LOW CONFIDENCE ROTATION
            if page_conf < minconf:
                continue
            def update_conf():
                if result_dic['page conf']==0:
                    result_dic['page conf'] = page_conf
            # Loop in titles, vendor names, quotation number
            for key in attr_dic.keys():
                # Loop in all tokens
                for token in attr_dic[key]:
                    if key == 'titles' or key == 'vendor names':
                        # Test each vocabulary to the textWholeInOne
                        ss, pos_st = testTokenInPage(tok=token, ppStr=page_text)
                        # String similarity is large enough to cut the token from page string
                        if ss > 0.9:
                            page_text = cutPage(ppStr=page_text,\
                                                pos_start=pos_st,\
                                                cutLen=len(token))
                        # HIT CONDITION
                        #   TODO : hard coding threashold
                        if ss > 0.65:
                            # update page conf value ONLY when a token hit
                            update_conf()
                            # trim the 's' in key's tail
                            key_singular = key[:(len(key)-1)]
                            if ss > resultBuffer[key_singular]['ss']:
                                resultBuffer[key_singular]['ss'] = ss
                                # solution Title Order, sTO
                                if resultBuffer[key_singular]['text']==attr_dic['titles'][0]:
                                    pass
                                else:
                                    resultBuffer[key_singular]['text'] = token
                    elif key == 'quotation number':
                        ss, pos_s = testTokenInPage(tok=token, ppStr=page_text)
                        if ss > 0.65:
                            # update page conf value ONLY when a token hit
                            update_conf()
                            pos_e = pos_s+len(token)+10
                            qnStr = page_text[pos_s:pos_e]
                            qnInPage = MyU.ya_extract_qn(text=qnStr, yy="24")
                            page_text = cutPage(ppStr=page_text,\
                                                pos_start=pos_s,\
                                                cutLen=(pos_e-pos_s+1))
                            if ss > resultBuffer[key]['ss']:
                                resultBuffer[key]['ss'] = ss
                                resultBuffer[key]['text'] = qnInPage
            # To escape rotate trial
            if ocr_type=='easyocr' and resultBuffer['title']['text'] in EscapeTitles:
                break
            if ocr_type=='easyocr' and\
                    resultBuffer['title']['text'] and\
                    resultBuffer['quotation number']['text'] and\
                    resultBuffer['vendor name']['text']:
                break
        # To escape zoom trial
        if ocr_type=='tess' and resultBuffer['title']['text'] in EscapeTitles:
            break
    result_dic['title'] = resultBuffer['title']['text']
    result_dic['vendor name'] = resultBuffer['vendor name']['text']
    result_dic['quotation number'] = resultBuffer['quotation number']['text']
    result_dic['ccw degree'] = ccw_degree
    return result_dic

# Define a transaction
transaction = {
    'quotation number': 'null',
    'vendor name': 'null',
    'titles to have': {
        '模具付款申請廠商確認書': False,
        '電子發票證明聯': False,
        '統一發票': False,
        '檢查結果連絡書': False,
        '模具修繕申請表': False,
        '金型修正指示書': False,
        '設計變更連絡書': False,
        '設計變更聯絡書': False,
        '模具資產管理卡': False,
        '會議記錄': False,
        '模具重量照片': False
    }
}

def process_transaction(page_data) -> str:
    MyU.log_text(f"transaction={transaction}")
    # An un-ocrable page came in
    if page_data['page conf'] == 0:
        if transaction['titles to have']['會議記錄'] == False:
            page_data['title'] = '會議記錄'
            transaction['titles to have']['會議記錄'] = True
        else:
            page_data['title'] = '模具重量照片'
            transaction['titles to have']['模具重量照片'] = True
        page_data['vendor name'] = transaction['vendor name']
        page_data['quotation number'] = transaction['quotation number']
    else:
        # This page is ocrable
        if page_data['vendor name'] and page_data['quotation number']:
            # New transaction
            #    When quotation number changed, a new transaction came in
            if transaction['quotation number'] != page_data['quotation number']:
                transaction['vendor name'] = page_data['vendor name']
                transaction['quotation number'] =page_data['quotation number']
                # Reset titles' appearances
                for key in transaction['titles to have']:
                    transaction['titles to have'][key] = False
        # WARNING! FILL IN VALUES IN CASE OF UN-OCRABLE VALUES HAPPENED
        if not page_data['vendor name']:
            page_data['vendor name'] = transaction['vendor name']
        if not page_data['quotation number']:
            page_data['quotation number'] = transaction['quotation number']
        # Register title appearance
        if page_data['title']:
            if page_data['title'] in transaction['titles to have'].keys():
                transaction['titles to have'][page_data['title']] = True
    s1 = f"{page_data['quotation number']}\n"
    s2 = f"{page_data['vendor name']}\n"
    s3 = f"{page_data['title']}\n"
    s4 = f"{page_data['ccw degree']}\n"
    s5 = f"{page_data['page conf']:.2f}"
    return s1+s2+s3+s4+s5

# To iterate in a pdf file, generator co-routine
def gen_iterateInPdf(pdffn, ocr_command=None, ocr_type='', do_plain=False, do_log=False, batch=None):
    global ocr_engine

    # Load config_ocr.json
    attr_dic = MyU.loadPageAttrFromJson()

    if not os.path.isfile(pdffn) or 'pdf' not in pdffn:
        raise Exception(f"Wrong! {pdffn} NOT exists or NOT a pdf file!")
    theDoc = openPDF(fn=pdffn)
    if theDoc==None:
        raise Exception(f"FATAL ERROR! failed in open {pdffn}")

    if ocr_command:
        ocr_command()
    elif ocr_type=='use_easy':
        use_easyocr()
    elif ocr_type=='use_tess':
        use_tess()
    else:
        raise Exception(f"Unknown ocr type:{ocr_type}")

    ocr_engine.Init()

    if batch == None or len(batch)==0:
        batch = list(range(1, theDoc.page_count+1))
        MyU.set_log(dolog=False)
        reallyToDoPlain = False
    else:
        MyU.set_log(dolog=do_log)
        reallyToDoPlain = do_plain

    # Loop in all pages in pdf
    for i in batch:
        ppno = i-1
        page = theDoc.load_page(ppno)
        if reallyToDoPlain==False:
            pp_dic = doMyOnePage(page=page, attr_dic=attr_dic, page_no=i)
            ret_str = process_transaction(page_data=pp_dic)
            yield f"Page.{i}\n" + ret_str
        else:
            MyU.set_log(dolog=True)
            img = getPageImg(page=page, zoom=2.0)
            ocr_engine.ReadImage(image=img, do_plain=True)
    theDoc.close()
    # End this processing
    yield ''
def gen_toSaveFiles(pdffn, ppInfoLst, savePath):
    doc = openPDF(fn=pdffn)
    for i in range(len(ppInfoLst)):
        page = doc.load_page(i)
        ss = ppInfoLst[i].split('\n')
        qn = ss[1]  # Quotation no
        vn = ss[2]  # Vendor name
        tt = ss[3]  # Paper title
        ccw = 0
        group_idx = '0'
        if len(ss) > 4:
            ccw = int(ss[4]) # CCW degree
        if len(ss) > 6:
            group_idx = ss[6].split('.')[1]
        ya_save_one_page(vendor_name=vn,\
                         quo_number=qn,\
                         title=tt,\
                         page=page,\
                         savePath=savePath,\
                         ccw=ccw,\
                         group_idx=group_idx)
        # print(f"to save file i={i},{qn},{vn},{tt}")
    doc.close()
# Post processing of page infos, page by page
#  Return format: {PageNo}\n{QuotationNo}\n{VendorName}\n{PaperTitle}\n{ccwDegree}\n{conf}\n{groupIndex}
def postProcessPageInfos(strs: list) -> list:
    pps = list()
    qns = list()
    vns = list()
    tts = list()
    remains = list()
    for s in strs:
        ss = s.split('\n')
        item_num = len(ss)
        pps.append(ss[0])  # Page No ...
        qns.append(ss[1])  # Quotation no.
        vns.append(ss[2])  # Vendor name
        tts.append(ss[3])  # Paper title
        # keep remaining page info
        st = ''
        for i in range(4, item_num):
            st += f"{ss[i]}\n"
        remains.append(st)
    page_num = len(tts)
    head = 0
    tail = 0
    # Iterate all pages to analyze
    while tail<page_num:
        tail += 1
        transact_grouped = False
        # To group a transaction
        if tail >= page_num:
            transact_grouped = True
        elif tts[head]==tts[tail]:
            transact_grouped = True
        # A transaction has been grouped
        if transact_grouped:
            # To add group index at the end of page info
            for i in range(head, tail):
                grp_idx = i-head+1
                remains[i] += f"GroupIdx.{grp_idx}"
            # To check inconsistent vendor name
            group_vns = vns[head:tail]
            voc = list(set(group_vns)) # vocabulary
            if len(voc)==1:
                pass # Group vendor name is consistent
            else:
                # Inconsistent vendor names are found
                #  Use vendor name on invoce as true vendor name
                group_tts = tts[head:tail]
                true_idx = 0
                for s in group_tts:
                    if "發票" in s:
                        true_idx=group_tts.index(s)
                        break
                true_vn = group_vns[true_idx]
                print(f"most_v={true_vn}") # Sort by value
                for i in range(len(group_vns)):
                    if group_vns[i] != true_vn:
                        log = f"Caught inconsist vn at pp{head+1}-{tail}, correct from {group_vns}"
                        group_vns[i] = true_vn
                        print(f"{log} to {group_vns}")
                vns[head:tail] = group_vns
            head = tail
    ret = list()
    for i in range(page_num):
        # TODO: add remaining page info back to the string
        ret.append(f"{pps[i]}\n{qns[i]}\n{vns[i]}\n{tts[i]}\n{remains[i]}")
    return ret
def main():
    # Check the argv
    theArgc = len(sys.argv)
    if theArgc < 3:
        path_strs = __file__.split('\\')
        exename = path_strs[len(path_strs)-1]
        print(f"Usage: python {exename} Filepath ocr_type option")
        print(f"\tFilepath : pdf file")
        print(f"\tocr_type :")
        print(f"\t\tuse_tess : to do mold transaction ocr using tesseract")
        print(f"\t\tuse_easy : to do mold transaction ocr using EasyOCR")
        print(f"\toption :")
        print(f"\t\t<page_numer...> : do mold trans to the designated page(s), count from 1")
        print(f"\t\tlog <page_numer...>: do mold transaction with log output")
        print(f"\t\tplain <page_numer...>: do plain ocr and just print results(lbox, str, conf)")
        exit(-1)
    # Check ocr type
    useWhichOcr = {
        'use_tess': use_tess,
        'use_easy': use_easyocr
    }
    if not sys.argv[2] in useWhichOcr.keys():
        print(f"\tUnknown ocr type, {sys.argv[2]}")
        exit(-1)
    # For checkint flags
    flags = {
        'plain': False,
        'log': False
    }
    # Create an empty batch list
    batch_list = None
    # Check flags and batch's string range
    if theArgc > 3:
        # Valid flags exist
        if sys.argv[3] in flags.keys():
            # Set flag
            flags[sys.argv[3]] = True
            # Batch list string range confirmed
            for_diff = 4
            # A batch list exits
            if theArgc > 4:
                batch_list = []
        else:
            # Batch list string range confirmed
            for_diff = 3
            # A batch list exits
            batch_list = []
        # Make batch list
        the_remain = sys.argv[for_diff:]

        str = ''.join(the_remain)
        # Find out delimiters' existence '-', ','
        punc = re.findall(r'[^\w\w]', str)
        # Delimiter exists
        if len(punc) > 0:
            the_list = str.split(punc[0])
        # No delimiter
        else:
            the_list = the_remain
        # Batch is start~stop type
        if len(the_list) == 2:
            batch_list=list(range(int(the_list[0]),(int(the_list[1])+1)))
        # Batch is discrete page numbers
        else:
            batch_list=[int(c) for c in the_list]
    # To OCR a pdf
    r = gen_iterateInPdf(pdffn=sys.argv[1],\
                        ocr_type=sys.argv[2],\
                        batch=batch_list,\
                        do_log=flags['log'],\
                        do_plain=flags['plain'])
    # Initialize page index (counting from zero)
    i = 0
    while True:
        # Get ocr result sequentially page by page
        p = next(r)
        # Null (or None) means ocr finished
        if not p:
            break
        else:
            print(f"{p}")
        i += 1
        # Just in case
        if i > 1000:
            break
    return 0

if __name__ == "__main__":
    main()