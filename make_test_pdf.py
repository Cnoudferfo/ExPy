from fpdf import FPDF

def generate_pdf(page_count, output_file="test_pdf.pdf"):
    pdf = FPDF()
    for i in range(page_count):
        pdf.add_page()
        pdf.set_font("Arial", size=12)
        pdf.cell(200, 10, txt=f"Page {i + 1}", ln=True, align='C')
    pdf.output(output_file)
    print(f"PDF with {page_count} pages created as {output_file}")

if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description="Generate a PDF with a specified number of pages.")
    parser.add_argument("page_count", type=int, help="Number of pages in the PDF")
    parser.add_argument("--output", type=str, default="test_pdf.pdf", help="Output PDF file name")

    args = parser.parse_args()
    generate_pdf(args.page_count, args.output)

