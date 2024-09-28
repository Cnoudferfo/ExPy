import os
from random import randrange

transaction = {
    'quotation number': 'null',
    'vendor name': 'null',
    'titles to have': {
        "模具付款申請廠商確認書": False,
        "電子發票證明聯": False,
        "統一發票": False,
        "檢查結果連絡書": False,
        "檢查結果聯絡書": False,
        "模具修繕申請表": False,
        "金型修正指示書": False,
        "設計變更連絡書": False,
        "設計變更聯絡書": False,
        "會議記錄": False,
        "模具資產管理卡": False,
        "模具重量照片": False
    }
}

def process_transaction(page_data):
    # An un-ocrable page came in
    if page_data['page conf'] == 0:
        if transaction['titles to have']['會議記錄'] == False:
            page_data['title'] = '會議記錄'
            transaction['titles to have']['會議記錄'] == True
        else:
            page_data['title'] = '模具重量照片'
            transaction['titles to have']['模具重量照片'] == True
        page_data['vendor name'] = transaction['vendor name']
        page_data['quotation number'] = transaction['quotation number']
    else:
        # This page is ocrable
        if page_data['vendor name'] and page_data['quotation number']:
            # New transaction
            #    When quotation number changed, a new transaction came in
            if transaction['quotation number'] != page_data['quotation number']:
                transaction['vendor name'] = page_data['vendor name']
                transaction['quotation number'] =page_data['quotation number']
                # Reset titles' appearances
                for key in transaction['titles to have']:
                    transaction['titles to have'][key] = False
        # WARNING! FILL IN VALUES IN CASE OF UN-OCRABLE VALUES HAPPENED
        if not page_data['vendor name']:
            page_data['vendor name'] = transaction['vendor name']
        if not page_data['quotation number']:
            page_data['quotation number'] = transaction['quotation number']
        # Register title appearance
        if page_data['title']:
            if page_data['title'] in transaction['titles to have'].keys():
                transaction['titles to have'][page_data['title']] = True
    return f"{page_data['quotation number']}_{page_data['vendor name']}_{page_data['title']}.pdf"


def main():
    result_dic = {
        'title': '',
        'vendor name': '',
        'quotation number': '',
        'page conf': 0
    }
    for i in range(12):
        result_dic

if __name__ == "__main__":
    main()
