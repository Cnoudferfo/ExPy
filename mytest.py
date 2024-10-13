import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import do_ocr as Doo

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
r= Doo.postProcessPageInfos(strs=test_pat)
print(f"r={r}")