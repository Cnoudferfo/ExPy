# mylib.py
# Chiaming's handy python library
import re

def remove_all_whitespaces(s):
    return re.sub(r'\s+', '', s)

def string_similarity(str1, str2):
    the_len = max((len(str1), len(str2)))
    str1 = str1 + ' '*(the_len - len(str1))
    str2 = str2 + ' '*(the_len - len(str2))
    return sum(1 if i == j else 0 for i, j in zip(str1, str2)) / float(the_len)

def extract_quotation_number(text, prefix):
    # match = re.search(r'估價單編號:(\d+)', text)
    # match = re.search(r'QN:(\d+)', text)
    pattern = re.escape(prefix) + r':(\d+)'
    match = re.search(pattern, text)
    if match:
        return match.group(1)
    return None


def extract_page_attributes(attr_dic, page_strings):
    Titles = attr_dic['titles']
    print(f"Dbg: Titles={Titles}")
    VendorNames = attr_dic['vendor names']
    print(f"Dbg: VendorNames={VendorNames}")
    QuotationNumber = attr_dic['quotation number']
    print(f"Dbg: QuotationNumber={QuotationNumber}")
    TitleInPage = ''            
    VnInPage = ''
    QnInPage = ''
    for str in page_strings:
        # clean_str = str.strip().replace(' ','')
        clean_str = remove_all_whitespaces(str)
        print(f"Dbg: clean_str={clean_str}")
        if TitleInPage == '':
            for t in Titles:
                ss = string_similarity(t, clean_str)
                print(f"Dbg: t={t}, clean_str={clean_str}, ss={ss}")
                if(ss > 0.2):
                    TitleInPage = t
                    break
        if VnInPage == '':
            for v in VendorNames:
                ss = string_similarity(v, clean_str)
                print(f"Dbg: v={v}, clean_str={clean_str}, ss={ss}")
                if(ss > 0.2):
                    VnInPage = v
                    break
        
        if QnInPage == '':
            for q in QuotationNumber:
                ss = string_similarity(q, clean_str)
                print(f"Dbg: q={q}, clean_str={clean_str}, ss={ss}")
                if(ss > 0.2):
                    QnInPage = extract_quotation_number(clean_str, q)
                    break
    return {'title':TitleInPage, 'vendor name':VnInPage, 'quotation number':QnInPage}

def main():
    p1_strs = ['Line1', ' companyA', 'Line2', 'Test report ', 'QN:506331']
    p2_strs = ['Line1', 'companyA', 'Line2', 'Line3', ' Invoice', 'QN:506331']
    p3_strs = ['Line1', ' companyB', 'Line2', 'Test report ', 'QN:506332']
    p4_strs = ['Line1', 'companyB', 'Line2', 'Line3', ' Invoice', 'QN:506332']
    a_dic = {
        "titles": ["Test report", "Invoice", "Meeting minutes"],
        "vendor names": ['companyA', 'companyB', 'companyC', 'companyD'],
        "quotation number": ['QN']
    }
    dic_att = extract_page_attributes(a_dic, p1_strs)
    print(f"title={dic_att['title']}, vendor name={dic_att['vendor name']}, quotation number={dic_att['quotation number']}")

if __name__ == "__main__":
    main()