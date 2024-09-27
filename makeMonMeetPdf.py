import os
import sys
import pymupdf as fitz

dest_filename = '2024_Sep_main.pdf'
dest = None
src_list = {
    'raw_main.pdf': None,
    '1_TOP_MSG.pdf': None,
    '2_B2B_AC.pdf': None,
    '3_RESIDENTIAL.pdf': None,
    '4_CC_MAINTAIN.pdf': None,
    '5_ENERGY.pdf': None,
    'HR.pdf': None,
    '1.TWBD PTWG.pdf': None,
    '5.AP.pdf': None
}
arrange_table = [
    {'page_count': 3, 'srcPfilename': 'raw_main.pdf', 'src_begin': 1},
    {'page_count': 6, 'srcPfilename': '1_TOP_MSG.pdf', 'src_begin': 2},
    {'page_count': 2, 'srcPfilename': 'raw_main.pdf', 'src_begin': 4},
    {'page_count': 1, 'srcPfilename': '2_B2B_AC.pdf', 'src_begin': 3},
    {'page_count': 1, 'srcPfilename': 'raw_main.pdf', 'src_begin': 6},
    {'page_count': 5, 'srcPfilename': '3_RESIDENTIAL.pdf', 'src_begin': 2},
    {'page_count': 1, 'srcPfilename': 'raw_main.pdf', 'src_begin': 7},
    {'page_count': 1, 'srcPfilename': '4_CC_MAINTAIN.pdf', 'src_begin': 3},
    {'page_count': 1, 'srcPfilename': 'raw_main.pdf', 'src_begin': 8},
    {'page_count': 1, 'srcPfilename': '5_ENERGY.pdf', 'src_begin': 2},
    {'page_count': 1, 'srcPfilename': '5_ENERGY.pdf', 'src_begin': 4},
    {'page_count': 1, 'srcPfilename': 'raw_main.pdf', 'src_begin': 9},
    {'page_count': 5, 'srcPfilename': 'HR.pdf', 'src_begin': 1},
    {'page_count': 1, 'srcPfilename': 'raw_main.pdf', 'src_begin': 10},
    {'page_count': 1, 'srcPfilename': '1.TWBD PTWG.pdf', 'src_begin': 6},
    {'page_count': 1, 'srcPfilename': '1.TWBD PTWG.pdf', 'src_begin': 11},
    {'page_count': 7, 'srcPfilename': '1.TWBD PTWG.pdf', 'src_begin': 13},
    {'page_count': 1, 'srcPfilename': 'raw_main.pdf', 'src_begin': 11},
    {'page_count': 12, 'srcPfilename': '5.AP.pdf', 'src_begin': 1},
    {'page_count': 1, 'srcPfilename': 'raw_main.pdf', 'src_begin': 12}
]

def main():
    if len(sys.argv) < 2:
        print(f"Usage:{__name__} work_path")
        exit(0)

    work_path = sys.argv[1]
    print(f"work_path={work_path}")

    for key in src_list.keys():
        src_path = work_path + key
        if os.path.isfile(src_path):
            src_list[key] = fitz.open(filename=src_path)
            print(f"{src_path} opened.")
        else:
            print(f"ERROR! failed in open {src_path}, abort!")
            exit(0)
    dest_doc = fitz.open()

    for i in range(len(arrange_table)):
        the_dic = arrange_table[i]
        page_count = the_dic['page_count']
        src_doc = src_list[the_dic['srcPfilename']]
        src_begin_pp = the_dic['src_begin'] - 1
        # print(f"dst_pp={dest_begin_pp}, pp_cnt={page_count}, src_doc={src_doc}, src_b_pp={src_begin_pp}")

        # Rearrange and rotate pages
        for go_cnt in range(page_count):
            src_pp = go_cnt + src_begin_pp
            original_page = src_doc.load_page(src_pp)
            new_page = dest_doc.new_page(width=original_page.rect.width, height=original_page.rect.height)
            new_page.show_pdf_page(new_page.rect, src_doc, src_pp, rotate=0)

    # Save the new PDF
    dest_path = work_path + dest_filename
    dest_doc.save(dest_path)
    print(f"{dest_path} saved.")

if __name__ == "__main__":
    main()