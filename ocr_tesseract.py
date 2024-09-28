import pytesseract as ts
from PIL import Image, ImageEnhance
import numpy as np
import cv2

def Init():
    ts.pytesseract.tesseract_cmd = r'D:\\Tools\\tesseract540\\tesseract.exe'

def preprocess_image(image, zoom=1.0):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)

    # Zoom
    height, width = gray.shape[:2]
    new_height = int(height * zoom)
    new_width = int(width * zoom)
    zoomed = cv2.resize(gray, (new_width, new_height), interpolation=cv2.INTER_NEAREST_EXACT)

    pil_img = Image.fromarray(zoomed)
    enhancer = ImageEnhance.Sharpness(pil_img)
    sharpened = enhancer.enhance(2.0)
    # Convert back to numpy array
    processed_img = np.array(sharpened)
    return processed_img

def calcStringSimilarity(tokenStr, testStr):
    # First test string_similarity
    max_len = max((len(tokenStr), len(testStr)))
    tokenNorm = tokenStr + ' '*(max_len - len(tokenStr))
    testNorm = testStr + ' '*(max_len - len(testStr))
    the_ss = sum(1 if i == j else 0 for i, j in zip(tokenNorm, testNorm)) / float(max_len)
    return the_ss

def ya_testInPage(strInPage, vocabulary):
    # Test each vocabulary to the textWholeInOne
    hitList = []
    ppStr = strInPage
    ppLen = len(ppStr)
    for token in vocabulary:
        # Test in vocaStr exists in test whole in one
        tokenLen = len(token)
        pos_start = 0
        while pos_start < ppLen:
            testStr = ppStr[pos_start:(pos_start+tokenLen)]
            ss = calcStringSimilarity(tokenStr=token, testStr=testStr)
            print(f"token={token}, testStr={testStr}, ss={ss}")
            # TODO : hard coding threashold
            if ss > 0.65:
                hitList.append(token)
                sub1 = ppStr[0:pos_start]
                sub2 = ppStr[(pos_start+tokenLen-1):ppLen]
                ppStr = sub1 + sub2
                ppLen = len(ppStr)
                break
            pos_start += 1
    return hitList

def ReadImage(image, vocabulary=None, ccw=0, zoom=1.0):
    # Convert input image to numpy array image
    np_img = np.array(image)

    # Preprocess the image
    processed_img = preprocess_image(np_img, zoom=zoom)

    # Rotate to designated direction
    ccw_count =0
    while ccw_count < ccw:
        processed_img = np.rot90(processed_img)
        ccw_count += 90

    data = ts.image_to_data(image=processed_img, lang='chi_tra', output_type=ts.Output.DICT)
    # Extract text and confidence levels
    results = [(data['left'][i], data['text'][i], int(data['conf'][i])) for i in range(len(data['text'])) if int(data['conf'][i]) > 0 and data['text'][i].strip()]
    # Calculate the average confidence level of this page
    conf_list = [conf for _, _, conf in results if _.strip()]
    thisAveConf = np.average(conf_list) if conf_list else 0

    # To make the OCR string of this page
    thisText = ''
    for _, s, c in results:
        if c >= 0 and s.strip():
            thisText += s

    return thisAveConf, thisText


def main():
    pageText = "SEC_ONE摩摩喳喳模具付款申請廠商確認書柒柒摳翔鎰精密科技工業有限公司啪啪啪噗噗估價單NO:240568娓娓到到到SEC_TWO元元始電子發飄證明聯結娓娓"
    vocabulry = ["模具付款申請廠商確認書",
            "電子發票證明聯",
            "統一發票",
            "檢查結果連絡書",
            "模具修繕申請表",
            "金型修正指示書",
            "設計變更連絡書",
            "模具資產管理卡",
            "翔鎰精密科技工業有限公司",
            "元譽精業有限公司",
            "威盈工業股份有限公司",
            "欣創工業股份有限公司",
            "金原金屬有限公司",
            "估價單"
            ]
    hitList = ya_testInPage(strInPage=pageText, vocabulary=vocabulry)
    print(f"hit len={len(hitList)}, hit={hitList}")



if __name__ == "__main__":
    main()