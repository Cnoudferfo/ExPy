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

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    # # Apply Guassian blur to reduce noise
    # blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    # # Binarization
    # _, binary = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    # Sharpen
    # pil_img = Image.fromarray(binary)
    pil_img = Image.fromarray(gray)
    enhancer = ImageEnhance.Sharpness(pil_img)
    sharpened = enhancer.enhance(2.0)
    # Convert back to numpy array
    processed_img = np.array(sharpened)
    return processed_img

def ReadImage(image, vocabulary=None):
    global reader
    # Convert input image to numpy array
    np_img = np.array(image)

    # Preprocess the image
    np_img = preprocess_image(np_img)

    # Rotation logic
    ## Initialize variables
    ave = 0
    rotation_count = 0
    max_rotations = 3 # 0, 90, 180, 270

    while ave < 0.3 and rotation_count < max_rotations:
        results = reader.readtext(np_img)
        # Calculate the average confidence level of this page
        conf_list = [cf for _, _, cf in results]
        ave = np.average(conf_list) if conf_list else 0

        if ave > 0.3:
            break

        np_img = np.rot90(np_img)
        rotation_count += 1

    # # TODO : REMOVE THIS BEFORE RELEASE
    # # To show the image for confirmation
    # pil_img = Image.fromarray(array_img)
    # pil_img.show()

    # To make the OCR string of this page
    # text = '\n'.join([s for _, s, _ in results])
    # text = '\n'.join([s if c > 0.1 else '\n' for _, s, c in results])
    text = ''
    for _, s, c in results:
        if c < 0.1:
            # Skip the strings with confidence lower than 0.1
            continue
        text += f"{s}\n"

    # return page string and average confidence level
    return text, ave


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