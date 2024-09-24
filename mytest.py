import os
# a transaction
dic_trns = {
    'vendor name': '',
    'quotation number': 0,
    '模具付款申請廠商確認書': [],
    '電子發票證明聯': [],
    '統一發票': [],
    '檢查結果連絡書': [],
    '模具修繕申請表': [],
    '金型修正指示書': [],
    '設計變更連絡書': [],
    '會議記錄': [],
    '模具資產管理卡': [],
    '模具重量照片': []
}

def main():
    print("main() Hello world!")
    for key in dic_trns.keys():
        print(f"key={key}")

if __name__ == "__main__":
    main()
