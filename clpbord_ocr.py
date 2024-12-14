import tkinter as tk
from tkinter import Menu, PhotoImage
from tkinterdnd2 import DND_FILES, TkinterDnD
import easyocr
from PIL import Image, ImageTk, ImageGrab, ImageDraw
import numpy as np

class App(TkinterDnD.Tk):
    def __init__(self):
        print('Create app...')
        super().__init__()
        self.title("Image OCR App")
        self.geometry("600x400")
        self.frame = tk.Frame(self, width=600, height=400, bg="white")
        self.frame.pack(fill=tk.BOTH, expand=True)
        self.frame.bind("<Button-3>", self.show_popup_menu)
        self.popup_menu = Menu(self, tearoff=0)
        self.popup_menu.add_command(label="Paste", command=self.paste_image)
        self.popup_menu.add_command(label="OCR", command=self.perform_ocr)
        self.image_label = tk.Label(self.frame)
        self.image_label.pack()
        print('Create Ocr reader...')
        self.ocrReader = easyocr.Reader(['ch_tra', 'en'], gpu=True)

    def show_popup_menu(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def paste_image(self):
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                self.image = image
                self.display_image()
        except Exception as e:
            print(f"Error pasting image: {e}")

    def display_image(self):
        dsp_img = ImageTk.PhotoImage(self.image)
        self.image_label.config(image=dsp_img)
        self.image_label.image = dsp_img

    def perform_ocr(self):
        try:
            # Convert the PIL Image to a NumPy array
            img_np = np.array(self.image)

            # Use EasyOCR to read the image
            result = self.ocrReader.readtext(img_np)

            # Draw the results on the image
            draw = ImageDraw.Draw(self.image)
            for res in result:
                bbox, text = res[0], res[1]
                # Extract the top-left and bottom-right coordinates from the bounding box
                top_left = (int(bbox[0][0]), int(bbox[0][1]))
                bottom_right = (int(bbox[2][0]), int(bbox[2][1]))
                draw.rectangle([top_left, bottom_right], outline="red", width=2)
                draw.text((top_left[0], top_left[1] - 10), text, fill="red")

            # Display the image with OCR results
            self.display_image()

            # Print the OCR result text
            text = "\n".join([res[1] for res in result])
            print("OCR Result:", text)
        except Exception as e:
            print(f"Error performing OCR: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
