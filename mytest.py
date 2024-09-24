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

def ReadImage(image=None, vocabulary=None, ccw=0):
    ccw_count = 0
    while ccw_count < ccw:
        print("Rotate once")
        ccw_count += 90
    print(f"{__name__}, {ccw_count} times rotated")
    return ccw_count

def main():
    print("main() Hello world!")
    for key in dic_trns.keys():
        print(f"key={key}")
    print(f"ReadImage={ReadImage(ccw=0)}")
    print(f"ReadImage={ReadImage(ccw=90)}")
    print(f"ReadImage={ReadImage(ccw=180)}")
    print(f"ReadImage={ReadImage(ccw=270)}")

if __name__ == "__main__":
    main()
