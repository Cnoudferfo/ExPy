# Server
from fastapi import FastAPI, File, UploadFile
from fastapi.responses import JSONResponse
import struct
from PIL import Image
import io

app = FastAPI()

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

@app.post("/process")
async def process_image(file: UploadFile = File(...)):
    data = await file.read()
    img = unpackData(packedData=data)

    # Perform OCR here (using EasyOCR or any preferred library)

    # Returning a dummy response for simplicity
    response = {'text': f"imgsize={img.size[0]}x{img.size[1]}"}
    return JSONResponse(content=response)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='127.0.0.1', port=8000)