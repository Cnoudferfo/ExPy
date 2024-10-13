def checkPageInfosAgain(strs: list) -> list:
    pps = []
    qns = []
    vns = []
    tts = []
    for s in strs:
        ss = s.split('\n')
        pps.append(ss[0])
        qns.append(ss[1])
        vns.append(ss[2])
        tts.append(ss[3])
    page_num = len(tts)
    head = 0
    tail = 0
    while tail<page_num:
        tail += 1
        transact_grouped = False
        if tail >= page_num:
            transact_grouped = True
        elif tts[head]==tts[tail]:
            transact_grouped = True
        if transact_grouped:
            seg = vns[head:tail] # Check vendor name
            voc = list(set(seg)) # vocabulary
            if len(voc)==1:
                pass # Checked ok
            else:
                # NOT ok
                cnts = dict()
                for v in voc:
                    cnts[v]=sum(1 if v==s else 0 for s in seg)
                cnts = dict(sorted(cnts.items(), key=lambda item: item[1], reverse=True))
                most_v = list(cnts.keys())[0]
                print(f"most_v={most_v}") # Sort by value
                for i in range(len(seg)):
                    if seg[i] != most_v:
                        log = f"Caught inconsist vn, from {seg[i]}"
                        seg[i] = most_v
                        print(f"{log} to {seg[i]}")
                vns[head:tail] = seg
            head = tail
    ret = list()
    for i in range(page_num):
        ret.append(f"{pps[i]}\n{qns[i]}\n{vns[i]}\n{tts[i]}")
    return ret

test_pat = [
    f"page.1\n24001\nA Comp\nA Pap",
    f"page.2\n24001\nB Comp\nB Pap",
    f"page.3\n24001\nA Comp\nC Pap",
    f"page.4\n24001\nA Comp\nD Pap",

    f"page.5\n24002\nB Comp\nA Pap",
    f"page.6\n24002\nB Comp\nB Pap",
    f"page.7\n24002\nB Comp\nC Pap",
    f"page.8\n24002\nB Comp\nD Pap",

    f"page.9\n24003\nC Comp\nA Pap",
    f"page.10\n24003\nC Comp\nB Pap",
    f"page.11\n24003\nC Comp\nC Pap",
    f"page.12\n24003\nC Comp\nD Pap",

    f"page.13\n24004\nD Comp\nA Pap",
    f"page.14\n24004\nD Comp\nB Pap",
    f"page.15\n24004\nD Comp\nC Pap",
    f"page.16\n24004\nD Comp\nD Pap"
]
print(f"t={test_pat}")
r= checkPageInfosAgain(strs=test_pat)
print(f"r={r}")