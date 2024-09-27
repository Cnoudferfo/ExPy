import os
import sys
import pymupdf as fitz

arrange_table = [
    {'original_page_no': 2, 'to_rotate': 0},
    {'original_page_no': 3, 'to_rotate': 270},
    {'original_page_no': 1, 'to_rotate': 270},
    {'original_page_no': 4, 'to_rotate': 0},

    {'original_page_no': 6, 'to_rotate': 0},
    {'original_page_no': 7, 'to_rotate': 270},
    {'original_page_no': 5, 'to_rotate': 0},
    {'original_page_no': 8, 'to_rotate': 270},

    {'original_page_no': 10, 'to_rotate': 0},
    {'original_page_no': 11, 'to_rotate': 270},
    {'original_page_no': 9, 'to_rotate': 270},
    {'original_page_no': 12, 'to_rotate': 0},

    {'original_page_no': 13, 'to_rotate': 0},
    {'original_page_no': 15, 'to_rotate': 270},
    {'original_page_no': 14, 'to_rotate': 270},
    {'original_page_no': 16, 'to_rotate': 0},

    {'original_page_no': 18, 'to_rotate': 0},
    {'original_page_no': 19, 'to_rotate': 270},
    {'original_page_no': 17, 'to_rotate': 270},
    {'original_page_no': 20, 'to_rotate': 0},

    {'original_page_no': 23, 'to_rotate': 0},
    {'original_page_no': 21, 'to_rotate': 270},
    {'original_page_no': 22, 'to_rotate': 270},
    {'original_page_no': 24, 'to_rotate': 0},

    {'original_page_no': 26, 'to_rotate': 0},
    {'original_page_no': 27, 'to_rotate': 270},
    {'original_page_no': 25, 'to_rotate': 0},
    {'original_page_no': 28, 'to_rotate': 270},

    {'original_page_no': 30, 'to_rotate': 0},
    {'original_page_no': 31, 'to_rotate': 270},
    {'original_page_no': 29, 'to_rotate': 270},
    {'original_page_no': 32, 'to_rotate': 270},

    {'original_page_no': 34, 'to_rotate': 0},
    {'original_page_no': 35, 'to_rotate': 270},
    {'original_page_no': 33, 'to_rotate': 270},
    {'original_page_no': 36, 'to_rotate': 0},

    {'original_page_no': 38, 'to_rotate': 0},
    {'original_page_no': 39, 'to_rotate': 0},
    {'original_page_no': 37, 'to_rotate': 270},
    {'original_page_no': 40, 'to_rotate': 270},
    {'original_page_no': 41, 'to_rotate': 0},
    {'original_page_no': 42, 'to_rotate': 0},

    {'original_page_no': 43, 'to_rotate': 0},
    {'original_page_no': 45, 'to_rotate': 270},
    {'original_page_no': 44, 'to_rotate': 270},
    {'original_page_no': 46, 'to_rotate': 0},

    {'original_page_no': 48, 'to_rotate': 0},
    {'original_page_no': 49, 'to_rotate': 270},
    {'original_page_no': 47, 'to_rotate': 270},
    {'original_page_no': 50, 'to_rotate': 0},

    {'original_page_no': 52, 'to_rotate': 0},
    {'original_page_no': 53, 'to_rotate': 270},
    {'original_page_no': 51, 'to_rotate': 270},
    {'original_page_no': 54, 'to_rotate': 0},

    {'original_page_no': 56, 'to_rotate': 0},
    {'original_page_no': 57, 'to_rotate': 270},
    {'original_page_no': 55, 'to_rotate': 0},
    {'original_page_no': 58, 'to_rotate': 270},

    {'original_page_no': 60, 'to_rotate': 0},
    {'original_page_no': 61, 'to_rotate': 270},
    {'original_page_no': 59, 'to_rotate': 0},
    {'original_page_no': 62, 'to_rotate': 270},

    {'original_page_no': 64, 'to_rotate': 0},
    {'original_page_no': 65, 'to_rotate': 270},
    {'original_page_no': 63, 'to_rotate': 270},
    {'original_page_no': 66, 'to_rotate': 270},
    {'original_page_no': 67, 'to_rotate': 0},
    {'original_page_no': 68, 'to_rotate': 270},

    {'original_page_no': 70, 'to_rotate': 0},
    {'original_page_no': 71, 'to_rotate': 270},
    {'original_page_no': 69, 'to_rotate': 270},
    {'original_page_no': 72, 'to_rotate': 270},
    {'original_page_no': 73, 'to_rotate': 0},
    {'original_page_no': 74, 'to_rotate': 270},

    {'original_page_no': 76, 'to_rotate': 0},
    {'original_page_no': 77, 'to_rotate': 270},
    {'original_page_no': 75, 'to_rotate': 270},
    {'original_page_no': 78, 'to_rotate': 270},
    {'original_page_no': 79, 'to_rotate': 0},
    {'original_page_no': 80, 'to_rotate': 270},

    {'original_page_no': 83, 'to_rotate': 0},
    {'original_page_no': 84, 'to_rotate': 270},
    {'original_page_no': 81, 'to_rotate': 270},
    {'original_page_no': 85, 'to_rotate': 270},
    {'original_page_no': 86, 'to_rotate': 0},
    {'original_page_no': 87, 'to_rotate': 270},

    {'original_page_no': 89, 'to_rotate': 0},
    {'original_page_no': 90, 'to_rotate': 270},
    {'original_page_no': 88, 'to_rotate': 270},
    {'original_page_no': 91, 'to_rotate': 270},
    {'original_page_no': 92, 'to_rotate': 0},
    {'original_page_no': 93, 'to_rotate': 270},

    {'original_page_no': 95, 'to_rotate': 0},
    {'original_page_no': 96, 'to_rotate': 270},
    {'original_page_no': 94, 'to_rotate': 270},
    {'original_page_no': 97, 'to_rotate': 270},
    {'original_page_no': 98, 'to_rotate': 270},
    {'original_page_no': 99, 'to_rotate': 0},
    {'original_page_no': 100, 'to_rotate': 270},

    {'original_page_no': 103, 'to_rotate': 0},
    {'original_page_no': 104, 'to_rotate': 270},
    {'original_page_no': 102, 'to_rotate': 270},
    {'original_page_no': 105, 'to_rotate': 270},
    {'original_page_no': 106, 'to_rotate': 0},
    {'original_page_no': 107, 'to_rotate': 270},

    {'original_page_no': 109, 'to_rotate': 0},
    {'original_page_no': 110, 'to_rotate': 270},
    {'original_page_no': 108, 'to_rotate': 270},
    {'original_page_no': 112, 'to_rotate': 270},
    {'original_page_no': 113, 'to_rotate': 0},
    {'original_page_no': 114, 'to_rotate': 270},

    {'original_page_no': 116, 'to_rotate': 0},
    {'original_page_no': 117, 'to_rotate': 270},
    {'original_page_no': 115, 'to_rotate': 270},
    {'original_page_no': 118, 'to_rotate': 270},
    {'original_page_no': 119, 'to_rotate': 0},
    {'original_page_no': 120, 'to_rotate': 270},

    {'original_page_no': 121, 'to_rotate': 0},
    {'original_page_no': 123, 'to_rotate': 270},
    {'original_page_no': 122, 'to_rotate': 270},
    {'original_page_no': 124, 'to_rotate': 270},
    {'original_page_no': 125, 'to_rotate': 0},
    {'original_page_no': 126, 'to_rotate': 270},

    {'original_page_no': 128, 'to_rotate': 0},
    {'original_page_no': 129, 'to_rotate': 270},
    {'original_page_no': 127, 'to_rotate': 270},
    {'original_page_no': 130, 'to_rotate': 270},
    {'original_page_no': 131, 'to_rotate': 0},
    {'original_page_no': 132, 'to_rotate': 270},

    {'original_page_no': 134, 'to_rotate': 0},
    {'original_page_no': 135, 'to_rotate': 270},
    {'original_page_no': 133, 'to_rotate': 270},
    {'original_page_no': 136, 'to_rotate': 270},
    {'original_page_no': 137, 'to_rotate': 0},
    {'original_page_no': 138, 'to_rotate': 270},

    {'original_page_no': 140, 'to_rotate': 0},
    {'original_page_no': 141, 'to_rotate': 270},
    {'original_page_no': 139, 'to_rotate': 270},
    {'original_page_no': 142, 'to_rotate': 270},
    {'original_page_no': 143, 'to_rotate': 0},
    {'original_page_no': 144, 'to_rotate': 270},

    {'original_page_no': 146, 'to_rotate': 0},
    {'original_page_no': 147, 'to_rotate': 270},
    {'original_page_no': 145, 'to_rotate': 270},
    {'original_page_no': 148, 'to_rotate': 270},
    {'original_page_no': 149, 'to_rotate': 0},
    {'original_page_no': 150, 'to_rotate': 270},

    {'original_page_no': 152, 'to_rotate': 0},
    {'original_page_no': 153, 'to_rotate': 270},
    {'original_page_no': 151, 'to_rotate': 270},
    {'original_page_no': 154, 'to_rotate': 270},
    {'original_page_no': 155, 'to_rotate': 0},
    {'original_page_no': 156, 'to_rotate': 270},

    {'original_page_no': 162, 'to_rotate': 0},
    {'original_page_no': 158, 'to_rotate': 270},
    {'original_page_no': 157, 'to_rotate': 270},
    {'original_page_no': 159, 'to_rotate': 270},
    {'original_page_no': 160, 'to_rotate': 0},
    {'original_page_no': 161, 'to_rotate': 270},

    {'original_page_no': 164, 'to_rotate': 0},
    {'original_page_no': 165, 'to_rotate': 270},
    {'original_page_no': 163, 'to_rotate': 270},
    {'original_page_no': 166, 'to_rotate': 270},
    {'original_page_no': 167, 'to_rotate': 0},
    {'original_page_no': 168, 'to_rotate': 270},
]

def main():
    if len(sys.argv) < 2:
        print(f"Usage:{__name__} source_pdf_filepath")
        exit(0)

    doc = fitz.open(sys.argv[1])
    new_doc = fitz.open()

    # Rearrange and rotate pages
    i = 0
    for item in arrange_table:
        ori_ppno = item['original_page_no']-1
        rot = item['to_rotate']
        ori_page = doc.load_page(ori_ppno)

        if rot == 0:
            new_width = ori_page.rect.width
            new_height = ori_page.rect.height
        else:
            new_width = ori_page.rect.height
            new_height = ori_page.rect.width

        new_page = new_doc.new_page(width=new_width, height=new_height)
        new_page.show_pdf_page(new_page.rect, doc, pno=ori_ppno, rotate=rot, keep_proportion=True)
        i += 1
        print(f"page{i} ori_pp={item['original_page_no']}, rot={rot}")

    # Save the new PDF
    new_doc.save(".\\test_data\\rearranged.pdf")

if __name__ == "__main__":
    main()