# Client
import requests
import fitz  # pymupdf
import struct
from PIL import Image
import io
import sys

def packPix(page, zoom):
    mtrx = fitz.Matrix(zoom, zoom)
    pix = page.get_pixmap(matrix=mtrx)

    # Save pixmap as PNG to a bytes buffer
    buf = io.BytesIO(pix.tobytes(output="png"))
    img_bytes = buf.getvalue()
    pkData = struct.pack(f"!III{len(img_bytes)}s", pix.width, pix.height, len(img_bytes), img_bytes)
    return pkData

def send_image_to_server(data):
    files = {'file': data}
    response = requests.post("http://127.0.0.1:8000/process", files=files)

    if response.status_code == 200:
        print(response.json())

def main():
    doc = fitz.open(sys.argv[1])
    page = doc.load_page(0)
    pkdat = packPix(page=page, zoom=2.5)
    send_image_to_server(data=pkdat)


if __name__ == "__main__":
    main()
