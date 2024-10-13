
def demo_sort_a_list(strs: list) -> list:
    pps = list()
    qns = list()
    vns = list()
    tts = list()
    remains = list()
    for s in strs:
        ss = s.split('\n')
        item_num = len(ss)
        pps.append(ss[0])  # Page No ...
        qns.append(ss[1])  # Quotation no.
        vns.append(ss[2])  # Vendor name
        tts.append(ss[3])  # Paper title
        # keep remaining page info
        st = ''
        for i in range(4, item_num):
            st += f"{ss[i]}\n"
        remains.append(st)
    page_num = len(tts)
    head = 0
    tail = 0
    # Iterate all pages to analyze
    while tail<page_num:
        tail += 1
        transact_grouped = False
        # To group a transaction
        if tail >= page_num:
            transact_grouped = True
        elif tts[head]==tts[tail]:
            transact_grouped = True
        # A transaction has been grouped
        if transact_grouped:
            # To add group index at the end of page info
            for i in range(head, tail):
                grp_idx = i-head+1
                remains[i] += f"GroupIdx.{grp_idx}"
            # To check inconsistent vendor name
            group_vns = vns[head:tail]
            voc = list(set(group_vns)) # vocabulary
            if len(voc)==1:
                pass # Checked ok
            else:
                # NOT ok
                # Find true vendor name
                #  THIS IS WRONG! sort list to find majority, use majority vn as true vn
                cnts = dict()
                for v in voc:
                    cnts[v]=sum(1 if v==s else 0 for s in group_vns)
                cnts = dict(sorted(cnts.items(), key=lambda item: item[1], reverse=True))
                true_vn = list(cnts.keys())[0]
                #  Use vendor name on invoce as true vendor name
                group_tts = tts[head:tail]
                true_idx = 0
                for s in group_tts:
                    if "發票" in s:
                        true_idx=group_tts.index(s)
                        break
                true_vn = group_vns[true_idx]
                print(f"most_v={true_vn}") # Sort by value
                for i in range(len(group_vns)):
                    if group_vns[i] != true_vn:
                        log = f"Caught inconsist vn at pp{head+1}-{tail}, correct from {group_vns}"
                        group_vns[i] = true_vn
                        print(f"{log} to {group_vns}")
                vns[head:tail] = group_vns
            head = tail
    ret = list()
    for i in range(page_num):
        # TODO: add remaining page info back to the string
        ret.append(f"{pps[i]}\n{qns[i]}\n{vns[i]}\n{tts[i]}\n{remains[i]}")
    return ret

test_pat = [
    f"page.1\n24001\nB Comp\nA Pap\n0\n60.22",
    f"page.2\n24001\nA Comp\n統一發票\n270\n68.52",
    f"page.3\n24001\nA Comp\nC Pap\n0\n95.24",
    f"page.4\n24001\nA Comp\nD Pap\n90\n63.85",

    f"page.5\n24002\nL Comp\nA Pap\n0\n75.48",
    f"page.6\n24002\nB Comp\n統一發票\n270\n90.34",
    f"page.7\n24002\nL Comp\nC Pap\n90\n61.09",
    f"page.8\n24002\nL Comp\nD Pap\n0\n99.03",

    f"page.9\n24003\nT Comp\nA Pap\n0\n79.86",
    f"page.10\n24003\nC Comp\n統一發票\n270\n59.63",
    f"page.11\n24003\nC Comp\n\n0\n93.02",
    f"page.12\n24003\nC Comp\nD Pap\n90\n71.23",

    f"page.13\n24004\nZ Comp\nA Pap\n90\n59.85",
    f"page.14\n24004\nD Comp\n電子發票證明聯\n0\n62.58",
    f"page.15\n24004\nZ Comp\nC Pap\n270\n89.31",
    f"page.16\n24004\nZ Comp\nD Pap\n90\n78.65"
]
print(f"t={test_pat}")
r= demo_sort_a_list(strs=test_pat)
print(f"r={r}")