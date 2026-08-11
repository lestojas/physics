"""
Faithful rebuild of the DepEd SHS E-Class Record with modified entry counts.

Source template: E-Class-Record-Senior-High-6-17-26.xlsx
  Original 'E-Class' layout : WW=6, PT=6, Summative=4, Term Exam=2
  Grading logic (per learner row r):
     T  = SUM(entries)
     PS = IFERROR(ROUND((T/HPS_total)*100,2),"0")
     WS = IFERROR(ROUND((PS*weight),2),"0")
  Exam block: WS(ST&TE) = (WS_ST + WS_TE) * exam_weight('Input Details'!K14)
  Initial Grade = WS_WW + WS_PT + WS(ST&TE)
  Final Grade   = VLOOKUP(Initial, Reference!A:C, 2)   (transmutation table)
  Descriptive / Remarks = VLOOKUP(Final, D206:J307, 2 / 5)

This script keeps 'Input Details', 'Reference', 'Instruction' intact and
rebuilds 'E-Class' (rows 1-92 + descriptor block 206-307) with:
     WW=12, PT=12, Summative=2, Term Exam=1
It also adds a 'Consolidated' sheet:
     WW=6, PT=6 (each entry = sum of a consecutive pair on E-Class),
     Summative=2 & Term Exam=1 copied straight from E-Class.
The layout-coupled 'Result' report-card sheet is dropped (its 134 formulas
target the original column positions); it can be re-linked separately.
"""

import copy
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL

SRC = "E-Class-Record-Senior-High-6-17-26.xlsx"
OUT = "E-Class-Record-Senior-High.xlsx"

FIRST_ROW, LAST_ROW, HPS_ROW = 13, 92, 12
G9, G10, SUB = 9, 10, 11   # group header rows / sub-header row

# ---- styles ----------------------------------------------------------------
thin = Side(style="thin", color="808080")
med = Side(style="medium", color="000000")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center")
BOLD = Font(bold=True, size=9)
SMALL = Font(size=9)
TITLE = Font(bold=True, size=14, color="1F4E78")
WW_F = PatternFill("solid", fgColor="DDEBF7")
PT_F = PatternFill("solid", fgColor="E2EFDA")
ST_F = PatternFill("solid", fgColor="FFF2CC")
TE_F = PatternFill("solid", fgColor="FCE4D6")
GR_F = PatternFill("solid", fgColor="D9D9D9")
NM_F = PatternFill("solid", fgColor="F2F2F2")
HD_F = PatternFill("solid", fgColor="BDD7EE")


def col_letters(a, b):
    return CL(a), CL(b)


def build_layout(nww, npt, nst, nte):
    """Return dict of column indices mirroring the template's structure."""
    c = 5  # A No, B Family, C First, D M.I.
    L = {"name": {"No": 1, "Family": 2, "First": 3, "MI": 4}}
    def block(n, combined=False):
        nonlocal c
        entries = list(range(c, c + n)); c += n
        T = c; c += 1
        PS = c; c += 1
        WS = c; c += 1
        return {"entries": entries, "T": T, "PS": PS, "WS": WS}
    L["WW"] = block(nww)
    L["PT"] = block(npt)
    L["ST"] = block(nst)
    # TE block plus combined PS/WS(ST&TE)
    te_entries = list(range(c, c + nte)); c += nte
    L["TE"] = {"entries": te_entries, "T": c, "PS": c + 1, "WS": c + 2}
    c += 3
    L["EX"] = {"PS": c, "WS": c + 1}   # PS(ST&TE), WS(ST&TE)
    c += 2
    L["INIT"] = c; c += 1
    L["FINAL"] = c; c += 1
    L["DESC"] = c; c += 1
    L["REMARK"] = c; c += 1
    L["END"] = c - 1
    return L


def style_region(ws, r1, c1, r2, c2, border=True):
    for r in range(r1, r2 + 1):
        for cc in range(c1, c2 + 1):
            cell = ws.cell(r, cc)
            if border:
                cell.border = BORDER
            if cell.alignment is None or cell.alignment.horizontal is None:
                cell.alignment = CENTER


def info_block(ws, title):
    ws.cell(1, 1, title).font = TITLE
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=12)
    ws.cell(1, 1).alignment = Alignment(horizontal="center", vertical="center")
    info = [
        ("Region:", "='Input Details'!C2", "School:", "='Input Details'!C4"),
        ("Division:", "='Input Details'!C3", "School ID:", "='Input Details'!C5"),
        ("District:", "='Input Details'!C6", "Grade & Section:",
         "=CONCATENATE('Input Details'!C13,\" - \",'Input Details'!C14)"),
        ("Term:", "='Input Details'!C10", "Subject:", "='Input Details'!C12"),
        ("School Year:", "='Input Details'!C11", "Teacher:", "='Input Details'!K2"),
        ("Male:", "='Input Details'!C15", "Female:", "='Input Details'!C16"),
    ]
    for i, (l1, v1, l2, v2) in enumerate(info):
        r = 3 + i
        ws.cell(r, 1, l1).font = BOLD
        ws.cell(r, 3, v1).font = SMALL
        ws.cell(r, 6, l2).font = BOLD
        ws.cell(r, 9, v2).font = SMALL


def write_headers(ws, L, exam_hdr=("Summative Test (60%)", "Term Examination (40%)")):
    # group header row 9
    def merge_label(r_from, r_to, c_from, c_to, text, fill, font=BOLD):
        ws.merge_cells(start_row=r_from, start_column=c_from,
                       end_row=r_to, end_column=c_to)
        cell = ws.cell(r_from, c_from, text)
        cell.font, cell.alignment, cell.fill = font, CENTER, fill
    # Learner name group
    merge_label(G9, G10, 1, 4, "LEARNER'S NAME", HD_F)
    merge_label(G9, G10, L["WW"]["entries"][0], L["WW"]["WS"], "Written / Oral Works", WW_F)
    merge_label(G9, G10, L["PT"]["entries"][0], L["PT"]["WS"], "Performance Tasks", PT_F)
    merge_label(G9, G9, L["ST"]["entries"][0], L["EX"]["WS"], "Examinations", ST_F)
    merge_label(G10, G10, L["ST"]["entries"][0], L["ST"]["WS"], exam_hdr[0], ST_F)
    merge_label(G10, G10, L["TE"]["entries"][0], L["EX"]["WS"], exam_hdr[1], TE_F)
    for col, txt in ((L["INIT"], "Initial\nGrade"), (L["FINAL"], "Final\nGrade"),
                     (L["DESC"], "Descriptive"), (L["REMARK"], "Remarks")):
        merge_label(G9, SUB, col, col, txt, GR_F)

    # sub-header row 11 (and merge name headers down to row12)
    for col, txt in ((1, "No."), (2, "Family"), (3, "First Name"), (4, "M.I.")):
        ws.merge_cells(start_row=SUB, start_column=col, end_row=HPS_ROW, end_column=col)
        c = ws.cell(SUB, col, txt); c.font, c.alignment, c.fill = BOLD, CENTER, NM_F

    def cat_headers(key, fill, ps_lbl, ws_lbl, t_lbl="T"):
        b = L[key]
        for i, ec in enumerate(b["entries"], 1):
            c = ws.cell(SUB, ec, i); c.font, c.alignment, c.fill = BOLD, CENTER, fill
        for col, lbl in ((b["T"], t_lbl), (b["PS"], ps_lbl), (b["WS"], ws_lbl)):
            c = ws.cell(SUB, col, lbl); c.font, c.alignment, c.fill = BOLD, CENTER, GR_F

    cat_headers("WW", WW_F, "PS", "WS")
    cat_headers("PT", PT_F, "PS", "WS")
    cat_headers("ST", ST_F, "PS\n(ST)", "WS\n(ST)")
    # TE block
    b = L["TE"]
    for i, ec in enumerate(b["entries"], 1):
        c = ws.cell(SUB, ec, i); c.font, c.alignment, c.fill = BOLD, CENTER, TE_F
    ws.cell(SUB, b["T"], "T").font = BOLD
    ws.cell(SUB, b["PS"], "PS\n(TE)").font = BOLD
    ws.cell(SUB, b["WS"], "TE").font = BOLD
    ws.cell(SUB, L["EX"]["PS"], "PS\n(ST & TE)").font = BOLD
    ws.cell(SUB, L["EX"]["WS"], "WS\n(ST & TE)").font = BOLD
    for col in (b["T"], b["PS"], b["WS"], L["EX"]["PS"], L["EX"]["WS"]):
        ws.cell(SUB, col).alignment = CENTER
        ws.cell(SUB, col).fill = GR_F


def hps_weight_row(ws, L, ww_w, pt_w, st_w, te_w, exam_w_formula):
    """Row 12: per-item HPS entry cells, category HPS totals, PS base 100, weights."""
    def sum(b):
        f, l = col_letters(b["entries"][0], b["entries"][-1])
        return f"=SUM({f}{HPS_ROW}:{l}{HPS_ROW})"
    ws.cell(HPS_ROW, L["WW"]["T"], sum(L["WW"]))
    ws.cell(HPS_ROW, L["WW"]["PS"], 100)
    ws.cell(HPS_ROW, L["WW"]["WS"], ww_w)
    ws.cell(HPS_ROW, L["PT"]["T"], sum(L["PT"]))
    ws.cell(HPS_ROW, L["PT"]["PS"], 100)
    ws.cell(HPS_ROW, L["PT"]["WS"], pt_w)
    ws.cell(HPS_ROW, L["ST"]["T"], sum(L["ST"]))
    ws.cell(HPS_ROW, L["ST"]["PS"], 100)
    ws.cell(HPS_ROW, L["ST"]["WS"], st_w)
    ws.cell(HPS_ROW, L["TE"]["T"], sum(L["TE"]))
    ws.cell(HPS_ROW, L["TE"]["WS"], te_w)
    ws.cell(HPS_ROW, L["EX"]["WS"], exam_w_formula)
    for col in (L["WW"]["T"], L["WW"]["PS"], L["WW"]["WS"], L["PT"]["T"], L["PT"]["PS"],
                L["PT"]["WS"], L["ST"]["T"], L["ST"]["PS"], L["ST"]["WS"], L["TE"]["T"],
                L["TE"]["WS"], L["EX"]["WS"]):
        ws.cell(HPS_ROW, col).font = BOLD
        ws.cell(HPS_ROW, col).alignment = CENTER
        ws.cell(HPS_ROW, col).fill = GR_F


def student_formulas(ws, L, r, entry_writer):
    """entry_writer(key, entry_cols, r) fills the raw entry cells (blank or formula)."""
    def C(col):
        return f"{CL(col)}{r}"
    # raw entries
    for key in ("WW", "PT", "ST", "TE"):
        entry_writer(key, L[key]["entries"], r)
    # WW / PT / ST : T, PS, WS
    for key in ("WW", "PT", "ST"):
        b = L[key]
        f, l = col_letters(b["entries"][0], b["entries"][-1])
        ws.cell(r, b["T"], f"=SUM({f}{r}:{l}{r})")
        ws.cell(r, b["PS"],
                f'=IFERROR(ROUND(({C(b["T"])}/${CL(b["T"])}${HPS_ROW})*100,2),"0")')
        ws.cell(r, b["WS"],
                f'=IFERROR(ROUND(({C(b["PS"])}*${CL(b["WS"])}${HPS_ROW}),2),"0")')
    # TE block
    b = L["TE"]
    f, l = col_letters(b["entries"][0], b["entries"][-1])
    ws.cell(r, b["T"], f"=SUM({f}{r}:{l}{r})")
    ws.cell(r, b["PS"],
            f'=IFERROR(ROUND(({C(b["T"])}/${CL(b["T"])}${HPS_ROW})*100,2),"0")')
    ws.cell(r, b["WS"],
            f'=IFERROR(ROUND(({C(b["PS"])}*${CL(b["WS"])}${HPS_ROW}),2),"0")')
    # Exam combined
    ex = L["EX"]
    ws.cell(r, ex["PS"], f'={C(L["ST"]["WS"])}+{C(L["TE"]["WS"])}')
    ws.cell(r, ex["WS"],
            f'=IFERROR(ROUND(({C(ex["PS"])}*${CL(ex["WS"])}${HPS_ROW}),2),"0")')
    # Initial / Final / Descriptive / Remarks
    ws.cell(r, L["INIT"], f'={C(L["WW"]["WS"])}+{C(L["PT"]["WS"])}+{C(ex["WS"])}')
    ws.cell(r, L["FINAL"],
            f'=IFERROR(VLOOKUP({C(L["INIT"])},Reference!$A$4:$C$15065,2)," ")')
    fin = f'${CL(L["FINAL"])}{r}'
    ws.cell(r, L["DESC"], f'=IFERROR(VLOOKUP({fin},{DESC_REF},2),"0")')
    ws.cell(r, L["REMARK"], f'=IFERROR(VLOOKUP({fin},{DESC_REF},5),"0")')
    # numbering + alignment
    ws.cell(r, 1, r - FIRST_ROW + 1).alignment = CENTER
    ws.cell(r, 2).alignment = LEFT
    ws.cell(r, 3).alignment = LEFT


# ============================================================================
wb = load_workbook(SRC, data_only=False)

# capture descriptor lookup block (cols A..J rows 205..308) from original E-Class
orig = wb["E-Class"]
desc_block = [[orig.cell(r, c).value for c in range(1, 11)] for r in range(205, 309)]

# drop layout-coupled sheets and rebuild E-Class
idx = wb.sheetnames.index("E-Class")
del wb["E-Class"]
if "Result" in wb.sheetnames:
    del wb["Result"]

ws = wb.create_sheet("E-Class", idx)
DESC_REF = "$D$206:$J$307"   # descriptor block lives on this sheet
L1 = build_layout(12, 12, 2, 1)

info_block(ws, "ELECTRONIC CLASS RECORD")
write_headers(ws, L1)
hps_weight_row(ws, L1, 0.2, 0.5, 0.6, 0.4, "='Input Details'!K14")


def blank_entries(key, cols, r):
    for c in cols:
        ws.cell(r, c).alignment = CENTER


for r in range(FIRST_ROW, LAST_ROW + 1):
    student_formulas(ws, L1, r, blank_entries)

# restore descriptor block at rows 205..308
for i, rowvals in enumerate(desc_block):
    rr = 205 + i
    for c, v in enumerate(rowvals, start=1):
        if v is not None:
            ws.cell(rr, c, v)

# borders + widths
style_region(ws, G9, 1, LAST_ROW, L1["END"])
ws.column_dimensions["A"].width = 4.5
ws.column_dimensions["B"].width = 12
ws.column_dimensions["C"].width = 13
ws.column_dimensions["D"].width = 4.5
for key in ("WW", "PT", "ST", "TE"):
    for ec in L1[key]["entries"]:
        ws.column_dimensions[CL(ec)].width = 4.3
    ws.column_dimensions[CL(L1[key]["T"])].width = 5.5
    ws.column_dimensions[CL(L1[key]["PS"])].width = 6
    ws.column_dimensions[CL(L1[key]["WS"])].width = 6
for col in (L1["EX"]["PS"], L1["EX"]["WS"], L1["INIT"], L1["FINAL"]):
    ws.column_dimensions[CL(col)].width = 7
ws.column_dimensions[CL(L1["DESC"])].width = 12
ws.column_dimensions[CL(L1["REMARK"])].width = 9
ws.freeze_panes = ws.cell(FIRST_ROW, 5)

# ============================================================================
# Consolidated sheet : WW6 / PT6 (pair sums) / ST2 / TE1 (copies)
# ============================================================================
ws2 = wb.create_sheet("Consolidated")
L2 = build_layout(6, 6, 2, 1)
S1 = "'E-Class'"
DESC_REF = f"{S1}!$D$206:$J$307"   # consolidated pulls descriptor from E-Class

info_block(ws2, "ELECTRONIC CLASS RECORD - CONSOLIDATED")
write_headers(ws2, L2)

# HPS/weight row 12 : WW/PT entries = pair sums of E-Class row12; ST/TE copied
def s1c(col, row):
    return f"={S1}!{CL(col)}{row}"

for key in ("WW", "PT"):
    for j, ec in enumerate(L2[key]["entries"]):
        a = L1[key]["entries"][2 * j]; b = L1[key]["entries"][2 * j + 1]
        ws2.cell(HPS_ROW, ec, f"={S1}!{CL(a)}{HPS_ROW}+{S1}!{CL(b)}{HPS_ROW}")
for ec2, ec1 in zip(L2["ST"]["entries"], L1["ST"]["entries"]):
    ws2.cell(HPS_ROW, ec2, s1c(ec1, HPS_ROW))
for ec2, ec1 in zip(L2["TE"]["entries"], L1["TE"]["entries"]):
    ws2.cell(HPS_ROW, ec2, s1c(ec1, HPS_ROW))
hps_weight_row(ws2, L2, 0.2, 0.5, 0.6, 0.4, "='Input Details'!K14")
# re-apply the pair-sum/copy HPS entries (hps_weight_row only wrote T/PS/WS cols)


def consolidated_entries(key, cols, r):
    if key in ("WW", "PT"):
        for j, ec in enumerate(cols):
            a = L1[key]["entries"][2 * j]; b = L1[key]["entries"][2 * j + 1]
            ws2.cell(r, ec, f"={S1}!{CL(a)}{r}+{S1}!{CL(b)}{r}").alignment = CENTER
    else:  # ST / TE copied straight from E-Class
        src = L1[key]["entries"]
        for ec, sc in zip(cols, src):
            ws2.cell(r, ec, s1c(sc, r)).alignment = CENTER


for r in range(FIRST_ROW, LAST_ROW + 1):
    # No/Name reference E-Class
    ws2.cell(r, 1, s1c(1, r)).alignment = CENTER
    ws2.cell(r, 2, s1c(2, r)).alignment = LEFT
    ws2.cell(r, 3, s1c(3, r)).alignment = LEFT
    ws2.cell(r, 4, s1c(4, r)).alignment = CENTER
    student_formulas(ws2, L2, r, consolidated_entries)
    # student_formulas overwrites No/Name numbering -> restore references
    ws2.cell(r, 1, s1c(1, r)).alignment = CENTER
    ws2.cell(r, 2, s1c(2, r)).alignment = LEFT
    ws2.cell(r, 3, s1c(3, r)).alignment = LEFT

style_region(ws2, G9, 1, LAST_ROW, L2["END"])
for col, w in [("A", 4.5), ("B", 12), ("C", 13), ("D", 4.5)]:
    ws2.column_dimensions[col].width = w
for key in ("WW", "PT", "ST", "TE"):
    for ec in L2[key]["entries"]:
        ws2.column_dimensions[CL(ec)].width = 4.6
    ws2.column_dimensions[CL(L2[key]["T"])].width = 5.5
    ws2.column_dimensions[CL(L2[key]["PS"])].width = 6
    ws2.column_dimensions[CL(L2[key]["WS"])].width = 6
for col in (L2["EX"]["PS"], L2["EX"]["WS"], L2["INIT"], L2["FINAL"]):
    ws2.column_dimensions[CL(col)].width = 7
ws2.column_dimensions[CL(L2["DESC"])].width = 12
ws2.column_dimensions[CL(L2["REMARK"])].width = 9
ws2.freeze_panes = ws2.cell(FIRST_ROW, 5)

wb.save(OUT)
print("Saved", OUT)
print("Final sheets:", wb.sheetnames)
print("E-Class layout:", {k: v for k, v in L1.items()})
print("Consolidated layout:", {k: v for k, v in L2.items()})
