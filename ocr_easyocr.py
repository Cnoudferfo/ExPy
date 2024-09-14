import easyocr
import numpy as np
import torch

reader = None

def Init():
    global reader
    if torch.cuda.is_available():
        Gpu = True
    else:
        Gpu = False
    print(f"Gpu = {Gpu}")
    reader = easyocr.Reader(['ch_tra', 'en'], gpu=Gpu)

def ReadImage(image):
    global reader
    img_np = np.array(image)
    results = reader.readtext(img_np)

    text = ''
    for _, s, _ in results:
        text += f"{s}\n"

    conf_list = []
    for _, _, cf in results:
        conf_list.append(cf)
    arr = np.array(conf_list)
    ave = np.average(arr)
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