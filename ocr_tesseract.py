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

def ReadImage(image):
    # Convert input image to numpy array image
    np_img = np.array(image)

    # Preprocess the image
    processed_img = preprocess_image(np_img)

    # Rotation logic
    best_text = ""
    best_ave = 0.0
    best_rotation = 0
    best_image = processed_img

    vocabulary = ['模具付款申請廠商確認書', '估價單', '電子發票證明聯']

    # while ave < 90:
    for rotation_count in range(4): # 0, 90, 180, 270 deggress ccw
        data = ts.image_to_data(processed_img, lang='chi_tra', output_type=ts.Output.DICT)

        # Extract text and confidence levels
        results = [(data['left'][i], data['text'][i], int(data['conf'][i])) for i in range(len(data['text'])) if int(data['conf'][i]) > 0 and data['text'][i].strip()]
        # Calculate the average confidence level of this page
        conf_list = [conf for _, _, conf in results if _.strip()]
        ave = np.average(conf_list) if conf_list else 0

        print(f"Rotation={rotation_count}, ave={ave}")
        for i in range(len(data['text'])):
            if data['text'][i].strip() and data['conf'][i]>-1:
                print(f"{data['text'][i]} , {data['conf'][i]}")

        # To make the OCR string of this page
        text = ''
        for _, s, c in results:
            if c > 50 and s.strip():
                text += f"{s}\n"

        # # Merge fragments based on the predefined vocabulary
        # merged_text = merge_fragments(text, vocabulary)

        if ave > best_ave:
            best_text = text
            best_ave = ave
            best_rotation = rotation_count
            best_image = processed_img.copy()

        processed_img = np.rot90(processed_img)

    print(f"Best rotation={best_rotation}, best_ave={best_ave}")
    pil_img = Image.fromarray(best_image)
    pil_img.show()


    # return page string and average confidence level
    return best_text, best_ave
