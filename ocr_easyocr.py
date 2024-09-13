import easyocr
import numpy as np

reader = None

def Init():
    global reader
    reader = easyocr.Reader(['ch_tra', 'en'], gpu=False)

def ReadImage(image):
    global reader
    img_np = np.array(image)
    results = reader.readtext(img_np)
    # return [text for _, text, _ in results]
    text = ''
    for _, s, _ in results:
        text += f"{s}\n"
    return text
