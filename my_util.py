# mylib.py
# Chiaming's handy python library
import re
import json

def load_config(fpth):
    with open(fpth, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def parse_config(config):
    attr = config.get('Attributes',{})
    result = {
        'titles' : attr.get('titles',[]),
        'vendor names' : attr.get('vendor names',[]),
        'quotation number' : attr.get('quotation number',[])
    }
    return result

def loadPageAttrFromJson():
    try:
        ocr_cfg = load_config('config_ocr.json')
        dic_config = parse_config(ocr_cfg)

        # print("Attributes:")
        # for t in dic_config['titles']:
        #     print(f"{t}")
        # for vn in dic_config['vendor names']:
        #     print(f"{vn}")
        # for qn in dic_config['quotation number']:
        #     print(f"{qn}")

        return dic_config
    except Exception as e:
        print(f"makeAttrDic() Error! {e}")
        return None

def remove_all_whitespaces(s):
    return re.sub(r'\s+', '', s)

def matchTokenAndTest(tokenStr, testStr):
    # First test string_similarity
    max_len = max((len(tokenStr), len(testStr)))
    tokenNorm = tokenStr + ' '*(max_len - len(tokenStr))
    testNorm = testStr + ' '*(max_len - len(testStr))
    the_ss = sum(1 if i == j else 0 for i, j in zip(tokenNorm, testNorm)) / float(max_len)
    # TODO : Overcome the string match logic
    # TODO : Overcome the string match threashold value
    # if the_ss > 0.6:
    #     return the_ss
    # # Next, test str in str
    # elif tokenStr in testStr:
    #     return 1.0
    # else:
    #     # Finally, return 0, No hit!
    #     return 0.0
    return the_ss

def extract_quotation_number(text, prefix):
    pattern = re.escape(prefix) + r':(\d+)'
    match = re.search(pattern, text)
    if match:
        return str(match.group(1))
    return None

def ya_extract_qn(text, yy):
    pattern = fr'{yy}\d{{4}}'
    # print(f"pattern={pattern}")
    match = re.search(pattern, text)
    if match:
        return str(match.group())
    else:
        return ''

# To test the occurences of all attribution tokens in this page
def testAttrTokens(attr_dic, page_strings):
    Titles = attr_dic['titles']
    VendorNames = attr_dic['vendor names']
    QuotationNumber = attr_dic['quotation number']
    TitleInPage = ''
    VnInPage = ''
    QnInPage = ''
    theHit = False
    # To iterate every string in this page
    for str in page_strings:
        theHit = False
        clean_str = remove_all_whitespaces(str)
        msg_text = f"Dbg:testAttrTokens() To test clean_str={clean_str}"
        if TitleInPage == '':
            for t in Titles:
                ss = matchTokenAndTest(tokenStr=t, testStr=clean_str)
                if(ss > 0.6):
                    TitleInPage = t
                    theHit = True
                    msg_text += f" Hit! t={t}, ss={ss}"
                    break
        if VnInPage == '' and theHit == False:
            for v in VendorNames:
                clean_str.replace(":","").replace(" ", "")
                # To match the whole token with the whole test
                ss = matchTokenAndTest(tokenStr=v, testStr=clean_str)
                # print(f"token={v}, test={clean_str}, ss={ss}")
                if(ss > 0.9) or (v in clean_str):
                    VnInPage = v
                    theHit = True
                    msg_text += f" Hit! v={v}, ss={ss}"
                    break
                else:
                    # To match part of token and part of test
                    sub_vn = v[2:5]
                    test_len = len(clean_str)
                    if sub_vn in clean_str:
                        i = 0
                        while i < (test_len - 1):
                            sub_vn = v[:5]
                            sub_test = clean_str[i:]
                            i += 1
                            ss = matchTokenAndTest(tokenStr=sub_vn, testStr=sub_test)
                            # print(f"token={sub_vn}, test={sub_test}, ss={ss}")
                            if(ss > 0.45) or (v in clean_str):
                                VnInPage = v
                                theHit = True
                                msg_text += f" Hit! v={v}, ss={ss}"
                                break
                    if theHit == True:
                        break
        if QnInPage == '' and theHit == False:
            for q in QuotationNumber:
                if q in clean_str:
                    QnInPage = ya_extract_qn(text = clean_str, yy = "24")
                    if QnInPage != None and QnInPage.isnumeric():
                        theHit = True
                        msg_text += f" Hit! qn={QnInPage}"
                        break
        # # To print debug message
        # print(msg_text)
    if TitleInPage == '' and VnInPage == '' and QnInPage == '':
        return None
    else:
        return {'title':TitleInPage, 'vendor name':VnInPage, 'quotation number':QnInPage}

def main():
    token = "估價單"
    test = "(估價單N0:240360)"

    print(f"{test[2:4]}")
    exit(0)

    if token in test:
        qn = ya_extract_qn(text=test, yy="24")
    print(f"qn = {qn}")
    exit(0)

    noisystr = "AWS1201H01A0-0H019903,909|240348"
    theQn = ya_extract_qn(text=noisystr, yy="24")
    print(f"theQn={theQn}")
    exit(0)

    pages = []
    pages.append(["模具付款申請廠商確認書", "翔鎰精密科技工業有限公司", "公司印", "估價單NO:240257"])
    pages.append(["電子發票證明聯", "翔鎰精密科技工", "240257"])
    pages.append(["檢查結果連絡書", "廠商 翔鎰精密科技工業有限公司", "頁數："])
    pages.append(["xxxx", "oopopp", "noise"])
    pages.append(["模具付款申請廠商確認書", "元譽精業有限公司", "公司印", "估價單NO:240258"])
    pages.append(["電子發票證明聯", "元譽精業有限公", "240258"])
    pages.append(["檢查結果連絡書", "廠商：元譽", "頁數："])
    pages.append([",,,", "...", "==="])
    pages.append(["模具付款申請廠商確認書", "元譽精業有限公司", "公司印", "估價單NO:240259"])
    pages.append(["電子發票證明聯", "元譽精業有限公", "240259"])
    pages.append(["檢查結果連絡書", "廠商：元譽", "頁數："])
    pages.append(["333", "853", "00"])
    pages.append(["模具付款申請廠商確認書", "威盈工業股份有限公司", "公司印", "估價單NO:240260"])
    pages.append(["電子發票證明聯", "威盈工業股份有", "240260"])
    pages.append(["檢查結果連絡書", "廠商：威盈", "頁數："])
    pages.append(["XXJJ", "Z ZPU", "NOISE", "xxc", "yuyu"])

    a_dic = loadPageAttrFromJson()
    if a_dic == None:
        exit(-1)

    i=0
    for page in pages:
        i += 1
        the_dic = testAttrTokens(attr_dic=a_dic, page_strings=page)
        if the_dic == None:
            print(f"page[{i}] No hit!")
        else:
            print(f"page[{i}] Hit! title={the_dic['title']}, vendor name={the_dic['vendor name']}, quotation number={the_dic['quotation number']}")

if __name__ == "__main__":
    main()