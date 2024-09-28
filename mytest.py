import os
from random import randrange

db = {
    'vendors': [
        "翔鎰精密科技工業有限公司",
        "元譽精業有限公司",
        "威盈工業股份有限公司",
        "欣創工業股份有限公司",
        "金原金屬有限公司",
        "新榮緯股份有限公司",
        "星齊科技有限公司",
        "聯和橡膠股份有限公司",
        "立群鋼模企業股份有限公司",
        "永益精密工業有限公司",
        "慶沂企業有限公司",
        "精銘塑膠股份有限公司"
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

def CalcStringSimilarity(tokenStr, testStr):
    # First test string_similarity
    max_len = max((len(tokenStr), len(testStr)))
    tokenNorm = tokenStr + ' '*(max_len - len(tokenStr))
    testNorm = testStr + ' '*(max_len - len(testStr))
    the_ss = sum(1 if i == j else 0 for i, j in zip(tokenNorm, testNorm)) / float(max_len)
    return the_ss

def testTokenInPage(token='', page=''):
    ss = 0
    pageLen = len(page)
    tokenLen = len(token)
    pos_start = 0
    threshold = 1 - (3 / tokenLen)
    print(f"at testTokenInPage() &page={hex(id(page))}, th={threshold}")
    while pos_start < pageLen:
        # Get a clean string according to token length
        testStr = page[pos_start:(pos_start+tokenLen)]

        ss = CalcStringSimilarity(tokenStr=token, testStr=testStr)

        print(f"token={token}, testStr={testStr}, ss={ss}")

        if ss >= threshold:
            # Cut and cascade page text
            sub1 = page[0:pos_start]
            # sub2 = page[(pos_start+tokenLen-1):pageLen]
            sub2 = page[(pos_start+tokenLen):pageLen]
            page = sub1 + sub2
            pageLen = len(page)
            break

        # Increment start position index
        pos_start += 1
    return page, ss
    # return ss

def main():
    token = '翔鎰精密科技工業有限公司'
    # token = '精銘塑膠股份有限公司'

    ppStr = 'Domain:T30文件編號:3005034404\
        「瑟新品塑膠製品模購入年月保有年數;\
        5年[打品圖[]修金屬製品模日期:2024/9/9(估價單NO:240347)\
        加rm回點購次戰|國存放地點(不含稅)瞄1點時商總入則製|一人金aa\
        上生[扣除額(A預付款、B其他)|統一發票轉還區生8|全預付|金|一\
        「3||還國加了製造廠商使用廠商負責人印鑑|\
        公司印:翔鐺精密科技工業有限公司精銘塑膠股人國圖圖國轉點1六加圖讓圖計(器'
    print(f"at main() &ppStr={hex(id(ppStr))}")

    ppStr, ss = testTokenInPage(token=token, page=ppStr)
    # ss = testTokenInPage(token=token, page=ppStr)
    print(f"{token} from {ppStr}, with ss={ss} ")
    print(f"yet at main() &ppStr={hex(id(ppStr))}")


if __name__ == "__main__":
    main()
