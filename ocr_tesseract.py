import pytesseract as ts
from PIL import Image, ImageEnhance
import numpy as np
import cv2

def Init():
    ts.pytesseract.tesseract_cmd = r'D:\Tools\tesseract540\tesseract.exe'

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(np.array(image), cv2.COLOR_RGB2GRAY)
    # Sharpen
    pil_img = Image.fromarray(gray)
    enhancer = ImageEnhance.Sharpness(pil_img)
    sharpened = enhancer.enhance(2.0)
    # Convert back to numpy array
    processed_img = np.array(sharpened)
    return processed_img

def merge_fragments(text_fragments, vocabulary):
    merged_text = ""
    buffer = ""
    for fragment in text_fragments:
        buffer += fragment
        if buffer in vocabulary:
            merged_text += buffer + "\n"
            buffer = ""
        elif any(word.startswith(buffer) for word in vocabulary):
            continue
        else:
            merged_text += buffer + "\n"
            buffer = ""
    if buffer:
        merged_text += buffer + "\n"
    return merged_text

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

def ReadImage(image, vocabulary=None):
    # Convert input image to numpy array image
    np_img = np.array(image)

    # Preprocess the image
    processed_img = preprocess_image(np_img)

    # Rotation logic
    best_text = ""
    best_ave = 0.0
    best_rotation = 0
    best_image = processed_img

    # while ave < 90:
    for rotation_count in range(4): # 0, 90, 180, 270 deggress ccw
        data = ts.image_to_data(processed_img, lang='chi_tra', output_type=ts.Output.DICT)

        # Extract text and confidence levels
        results = [(data['left'][i], data['text'][i], int(data['conf'][i])) for i in range(len(data['text'])) if int(data['conf'][i]) > 0 and data['text'][i].strip()]
        # Calculate the average confidence level of this page
        conf_list = [conf for _, _, conf in results if _.strip()]
        ave = np.average(conf_list) if conf_list else 0

        print(f"Rotation={rotation_count}, ave={ave}")
        # for i in range(len(data['text'])):
        #     if data['text'][i].strip() and data['conf'][i]>-1:
        #         print(f"{data['text'][i]} , {data['conf'][i]}")

        # To make the OCR string of this page
        txtNLSep = ''
        txtInOne = ''
        for _, s, c in results:
            if c >= 0 and s.strip():
                txtNLSep += f"{s}\n"
                txtInOne += s

        # Test each vocabulary to the textWholeInOne
        hitList = ya_testInPage(strInPage=txtInOne, vocabulary=vocabulary)
        print(f"hitList={hitList}")

        # # Merge fragments based on the predefined vocabulary
        # merged_text = merge_fragments(text, vocabulary)

        if ave > best_ave:
            best_text = txtNLSep
            best_ave = ave
            best_rotation = rotation_count
            best_image = processed_img.copy()

        # Rotate the page image
        processed_img = np.rot90(processed_img)

    print(f"Best rotation={best_rotation}, best_ave={best_ave}")
    pil_img = Image.fromarray(best_image)
    pil_img.show()


    # return page string and average confidence level
    return best_text, best_ave

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