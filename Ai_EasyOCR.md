
# Using EasyOCR
- To install
```
pip install easyocr
```
- Sample code
```python
import easyocr
from PIL import Image
import fitz  # PyMuPDF
import re  # To use regular expression
import json
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import my_util as cu

# Initialize the EasyOCR reader with the desired languages
reader = easyocr.Reader(['ch_tra'])  # 'ch_tra' for traditional Chinese

# Parse a pdf page's text strings
def parse_a_pdf_page_at_zoom(page, zoom=1.2):
    if not isinstance(page, fitz.Page):
        raise ValueError("parse_a_pdf_page_at_zoom() must receive a PyMuPDF page object")
    mtrx = fitz.Matrix(zoom, zoom)  # To set a zoomed matrix
    page_pix = page.get_pixmap(matrix=mtrx)  # To get pixmap of page
    page_img = Image.frombytes("RGB", [page_pix.width, page_pix.height], page_pix.samples)
    
    # Convert the image to a format compatible with EasyOCR
    page_img_np = np.array(page_img)
    
    # Perform OCR using EasyOCR
    results = reader.readtext(page_img_np)
    
    # Extract text from results
    page_strs = [text for _, text, _ in results]
    return page_strs

def main():
    try:
        ...
        def drop(event):  # This function is called, when stuff is dropped into a widget        
            try:
                pdf = fitz.open(event.data)  # To open pdf file

                text = 'OCR result ' + '\n'
                # For each page in pdf
                for i in range(pdf.page_count):  # Use PyMuPDF
                    # Perform OCR
                    pp = pdf.load_page(i)  # To load page
                    pp_strs = parse_a_pdf_page_at_zoom(page=pp, zoom=1.2) 
                    for s in pp_strs:
                        ...
```
- Unpacking the tuple
```python
for _, text, _ in results
```
- This part of the comprehension unpacks each tuple in results into three variables: _, text, and _.
- The underscore _ is often used as a throwaway variable name when the value is not needed.


```python
# Example list of tuples
results = [(1, 'Hello', 0.99), (2, 'World', 0.95), (3, 'Python', 0.98)]

# List comprehension to extract the second element from each tuple
texts = [text for _, text, _ in results]

print(texts)  # Output: ['Hello', 'World', 'Python']
```