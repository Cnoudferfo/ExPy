import tkinter as tk
from tkinter import Menu, PhotoImage
from tkinterdnd2 import DND_FILES, TkinterDnD
import easyocr
from PIL import Image, ImageTk, ImageGrab
import io

class App(TkinterDnD.Tk):
    def __init__(self):
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

    def show_popup_menu(self, event):
        self.popup_menu.post(event.x_root, event.y_root)

    def paste_image(self):
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                self.display_image(image)
        except Exception as e:
            print(f"Error pasting image: {e}")

    def display_image(self, image):
        self.image = ImageTk.PhotoImage(image)
        self.image_label.config(image=self.image)
        self.image_label.image = self.image

    def perform_ocr(self):
        try:
            image = ImageGrab.grabclipboard()
            if isinstance(image, Image.Image):
                reader = easyocr.Reader(['en'])
                result = reader.readtext(image)
                text = "\n".join([res[1] for res in result])
                print("OCR Result:", text)
        except Exception as e:
            print(f"Error performing OCR: {e}")

if __name__ == "__main__":
    app = App()
    app.mainloop()
