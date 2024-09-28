# mylib.py
# Chiaming's handy python library
import re
import json
from PIL import Image

do_log = False

def set_log(dolog=False):
    global do_log
    do_log = dolog

def log_text(msgstr='peace!'):
    global do_log
    if do_log==True:
        print(f"DEBUG:{msgstr}")

def log_img(img=None):
    global do_log
    if do_log==True:
        pil_img = Image.fromarray(img)
        pil_img.show()

def load_config(fpth):
    with open(fpth, 'r', encoding='utf-8') as f:
        config = json.load(f)
    return config

def parse_attributes(config):
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
        dic_config = parse_attributes(ocr_cfg)
        return dic_config
    except Exception as e:
        print(f"loadPageAttrFromJson() Error! {e}")
        return None

def remove_all_whitespaces(s):
    return re.sub(r'\s+', '', s)

def remove_punctuation(text):
    # Define the pattern to match all punctuation marks
    pattern = r'[^\w\s]'
    # Substitute all punctuation marks with an empty string
    cleaned_text = re.sub(pattern, '', text)
    return cleaned_text

def CalcStringSimilarity(tokenStr, testStr):
    # First test string_similarity
    max_len = max((len(tokenStr), len(testStr)))
    tokenNorm = tokenStr + ' '*(max_len - len(tokenStr))
    testNorm = testStr + ' '*(max_len - len(testStr))
    the_ss = sum(1 if i == j else 0 for i, j in zip(tokenNorm, testNorm)) / float(max_len)
    return the_ss

def ya_extract_qn(text, yy):
    pattern = fr'{yy}\d{{4}}'
    # print(f"pattern={pattern}")
    match = re.search(pattern, text)
    if match:
        return str(match.group())
    else:
        return ''

def main():
    return 0

if __name__ == "__main__":
    main()