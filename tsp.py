# tsp.py : Test Struct Pair
import fitz  # pymupdf
import struct
from PIL import Image
import io
import sys
import typer

def packPix(fitzPage, zoom):
    mtrx = fitz.Matrix(zoom, zoom)
    pix = fitzPage.get_pixmap(matrix=mtrx)

    # Save pixmap as PNG to a bytes buffer
    buf = io.BytesIO(pix.tobytes(output="png"))
    img_bytes = buf.getvalue()

    print(f"PackPix(): width={pix.width}, height={pix.height}, bytes_len={len(img_bytes)}")

    packedData = struct.pack(f"!III{len(img_bytes)}s", pix.width, pix.height, len(img_bytes), img_bytes)
    return packedData

def unpackData(packedData):
    try:
        width, height, length = struct.unpack("!III", packedData[:12])
        img_bytes = struct.unpack(f"!{length}s", packedData[12:])[0]

        print(f"UnpackData(): width={width}, height={height}, length={length}, len(img_bytes)={len(img_bytes)}")

        # Load the image from the bytes buffer
        img = Image.open(io.BytesIO(img_bytes))

        return img
    except Exception as e:
        print(f"Error during unpacking: {e}")
        return None

def main(fn: str):
    doc = fitz.open(fn)
    page = doc.load_page(0)
    packed_data = packPix(fitzPage=page, zoom=2.5)
    upkImg = unpackData(packed_data)

    if upkImg:
        print(f"img_size={upkImg.size[0]}x{upkImg.size[1]}")
        upkImg.show()
    else:
        print("Failed to unpack and display image.")

if __name__ == "__main__":
    typer.run(main)
