import easyocr
import numpy as np
import torch
from PIL import Image, ImageEnhance, ImageFilter
import cv2

reader = None

def Init():
    global reader
    if torch.cuda.is_available():
        Gpu = True
    else:
        Gpu = False
    print(f"Gpu = {Gpu}")
    reader = easyocr.Reader(['ch_tra', 'en'], gpu=Gpu)

def preprocess_image(image, zoom=1.0):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

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

def ReadImage(image, vocabulary=None, ccw=0, zoom=1.0):
    global reader
    # Convert input image to numpy array
    np_img = np.array(image)

    # Preprocess the image
    processed_img = preprocess_image(image=np_img, zoom=zoom)

    # Rotate to designated direction
    ccw_count =0
    while ccw_count < ccw:
        processed_img = np.rot90(processed_img)
        ccw_count += 90

    results = reader.readtext(image=processed_img)
    # Calculate the average confidence level of this page
    conf_list = [cf for _, _, cf in results if _.strip()]
    ave = np.average(conf_list) if conf_list else 0

    # TODO : REMOVE THIS BEFORE RELEASE
    # To show the image for confirmation
    pil_img = Image.fromarray(processed_img)
    pil_img.show()

    # To make the OCR string of this page
    text = ''
    for _, s, c in results:
        if c > 0.1:
            text += s

    # return page string and average confidence level
    return ave, text

def main():
    Init()
    results = reader.readtext('./test_data/test.jpg')
    text = ''
    for _, s, _ in results:
        text += f"{s}\n"
    conf_list = []
    for _, _, cf in results:
        conf_list.append(cf)

    print(f"text={text}")
    print(f"conf_list={conf_list}")

    the_list = [ 1.0, 0.9, 0.8, 0.2]
    arr = np.array(conf_list)
    print(f"AVE = {np.average(arr)}")

if __name__ == "__main__":
    main()