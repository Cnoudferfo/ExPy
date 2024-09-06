import pytesseract as ts

def Init():
    ts.pytesseract.tesseract_cmd = r'D:\Tools\tesseract540\tesseract.exe'

def ReadImage(image):
    return ts.image_to_string(image, lang='chi_tra')