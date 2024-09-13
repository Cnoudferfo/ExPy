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
    if the_ss > 0.05:
        return 1.0
    # Next, test str in str
    elif tokenStr in testStr:
        return 1.0
    else:
        # Finally, return 0, No hit!
        return 0.0

def extract_quotation_number(text, prefix):
    pattern = re.escape(prefix) + r':(\d+)'
    match = re.search(pattern, text)
    if match:
        return str(match.group(1))
    return None

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
        # clean_str = str.strip().replace(' ','')
        clean_str = remove_all_whitespaces(str)
        if TitleInPage == '':
            for t in Titles:
                ss = matchTokenAndTest(tokenStr=t, testStr=clean_str)                
                if(ss > 0.0):
                    TitleInPage = t
                    theHit = True
                    # print(f"Dbg:testAttrTokens() Hit! t={t}, clean_str={clean_str}")
                    break
        if VnInPage == '':
            for v in VendorNames:
                ss = matchTokenAndTest(tokenStr=v, testStr=clean_str)
                if(ss > 0.0):
                    VnInPage = v
                    theHit = True
                    # print(f"Dbg:testAttrTokens() Hit! v={v}, clean_str={clean_str}")
                    break
        
        if QnInPage == '':
            for q in QuotationNumber:
                ss = matchTokenAndTest(tokenStr=q, testStr=clean_str)
                if(ss > 0.0):
                    QnInPage = extract_quotation_number(clean_str, q)
                    if QnInPage != None and QnInPage.isnumeric():
                        theHit = True
                        # print(f"Dbg:testAttrTokens() Hit! qn={QnInPage}, clean_str={clean_str}, ss={ss}")                
                        break
    if theHit == False:
        return None
    else:
        return {'title':TitleInPage, 'vendor name':VnInPage, 'quotation number':QnInPage}

def main():

    # testSpecs = [{'zoom': 1.2, 'cw': 0},
    #              {'zoom': 1.2, 'cw': 90},
    #              {'zoom': 1.8, 'cw': 0},
    #              {'zoom': 1.8, 'cw': 90}]
    
    # for testSpec in testSpecs:
    #     print(f"zoom={testSpec['zoom']}, cw={testSpec['cw']}")

    # exit(0)
    
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