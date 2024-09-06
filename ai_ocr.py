import fitz  # PyMuPDF
from PIL import Image
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
import pytesseract

# Open the PDF file
doc = fitz.open("yourfile.pdf")

for page_num in range(len(doc)):
    # Load the page
    page = doc.load_page(page_num)

    # Define the zoom factor (e.g., 2.0 for 200% zoom)
    zoom = 2.0
    mat = fitz.Matrix(zoom, zoom)

    # Get the pixmap with the zoom factor applied
    pix = page.get_pixmap(matrix=mat)

    # Convert the pixmap to an image
    img = Image.frombytes("RGB", [pix.width, pix.height], pix.samples)

    # Perform OCR using Tesseract
    text = pytesseract.image_to_string(img)

    # Define the file name based on OCR text or page number
    file_name = f"page_{page_num + 1}.pdf"

    # Create a PDF file
    c = canvas.Canvas(file_name, pagesize=letter)

    # Draw the image on the PDF
    img_path = f"temp_page_{page_num + 1}.jpg"
    img.save(img_path, "JPEG")
    c.drawImage(img_path, 0, 0, width=letter[0], height=letter[1])

    # Save the PDF
    c.save()

    # Optionally, delete the temporary image file
    import os
    os.remove(img_path)

    print(f"Saved {file_name}")

print("All pages processed and saved as individual PDFs.")
