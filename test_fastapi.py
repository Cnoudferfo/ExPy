# Server
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import fitz  # pymupdf
import struct
from PIL import Image
import io

app = FastAPI()

def packPix(fitzPage, zoom):
    mtrx = fitz.Matrix(zoom, zoom)
    pix = fitzPage.get_pixmap(matrix=mtrx)
    img_bytes = pix.tobytes()
    packedData = struct.pack(f"!III{len(img_bytes)}s", pix.width, pix.height, len(img_bytes), img_bytes)
    return packedData

def unpackData(packedData):
    width, height, length = struct.unpack("!III", packedData[:12])
    img_bytes = struct.unpack(f"!{length}s", packedData[12:])[0]
    img = Image.frombytes("RGB", (width, height), img_bytes)
    return img

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    img_data = await file.read()
    packed_data = struct.pack(f"!{len(img_data)}s", img_data)
    img = unpackData(packed_data)

    # Perform OCR here (using EasyOCR or any preferred library)

    # Returning a dummy response for simplicity
    response = {'text': 'dummy OCR text'}
    return JSONResponse(content=response)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8000)


# Client
import requests

def send_image_to_server(image_path):
    with open(image_path, 'rb') as img_file:
        files = {'file': img_file}
        response = requests.post("http://<SERVER_IP>:8000/process", files=files)

    if response.status_code == 200:
        print(response.json())

send_image_to_server("path_to_your_image.jpg")
