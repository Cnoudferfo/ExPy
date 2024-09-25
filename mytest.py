import os
from random import randrange


def test_transaction_process():
    db = {
        'vendors': [
            "翔鎰精密科技工業有限公司",
            "元譽精業有限公司",
            "威盈工業股份有限公司",
            "欣創工業股份有限公司",
            "金原金屬有限公司"
        ],
        'titles must have': [
            "模具付款申請廠商確認書",
            "電子發票證明聯",
            "檢查結果連絡書"
        ],
        'optional titles': [
            "模具修繕申請表",
            "金型修正指示書",
            "設計變更連絡書",
            "會議記錄"
        ],
        'new trans titles': [
            "模具資產管理卡",
            "模具重量照片"
        ]
    }

    test_pattern = []
    trans_count = 0
    page_count = 0
    while trans_count < 5:
        qn = ''
        vn = db['vendors'][int(randrange(6) % 5)]
        for key in db['titles must have']:
            if key == db['titles must have'][0]:
                qn = "24{sn:04}".format(sn=trans_count)
            test_pattern.append({'title': key, 'vendor name': vn, 'quotation number': qn})
            page_count += 1
        for i in range(int(randrange(10) % 3)):
            test_pattern.append({'title': key, 'vendor name': vn, 'quotation number': qn})
            page_count += 1
        qn = ''
        opt = db['optional titles'][int(randrange(5) % 4)]
        test_pattern.append({'title': opt, 'vendor name': vn, 'quotation number': qn})
        page_count += 1
        if trans_count == 2 or trans_count == 4:
            for key in db['new trans titles']:
                test_pattern.append({'title': key, 'vendor name': vn, 'quotation number': qn})
                page_count += 1
        trans_count += 1

    print(f"page_count={page_count}, test_pattern={test_pattern}")

    transaction = {
        'quotation number': 'null',
        'vendor name': 'null',
        'titles to have': {
            "模具付款申請廠商確認書": False,
            "電子發票證明聯": False,
            "統一發票": False,
            "檢查結果連絡書": False,
            "模具修繕申請表": False,
            "金型修正指示書": False,
            "設計變更連絡書": False,
            "會議記錄": False,
            "模具資產管理卡": False,
            "模具重量照片": False
        }
    }

    def process_transaction(pp_dic):
        # transaction process
        if pp_dic['vendor name'] and pp_dic['quotation number']:
            # New transaction
            #    When quotation number changed, a new transaction came in
            if transaction['quotation number'] != pp_dic['quotation number']:
                transaction['vendor name'] = pp_dic['vendor name']
                transaction['quotation number'] =pp_dic['quotation number']
                for key in transaction['titles to have']:
                    transaction['titles to have'][key] = False
        if not pp_dic['quotation number']:
            pp_dic['quotation number'] = transaction['quotation number']
        if pp_dic['title']:
            if pp_dic['title'] in transaction['titles to have'].keys():
                transaction['titles to have'][pp_dic['title']] = True

        if pp_dic['title'] == '' and pp_dic['vendor name'] == '' and pp_dic['quotation number'] == '':
            if transaction['titles to have']['會議記錄'] == False:
                pp_dic['title'] = '會議記錄'
                transaction['titles to have']['會議記錄'] == True
            else:
                pp_dic['title'] = '模具重量照片'
                transaction['titles to have']['模具重量照片'] == True

        return f"{pp_dic['quotation number']}_{pp_dic['vendor name']}_{pp_dic['title']}.pdf"

    # Loop in all pages in pdf
    for i in range(page_count):

        pp_dic = test_pattern[i]

        print(f"filepath {i+1} ={process_transaction(pp_dic=pp_dic)}")


def main():
    test_transaction_process()

if __name__ == "__main__":
    main()
