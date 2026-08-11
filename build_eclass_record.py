"""
E-Class Record generator (modern styling + blank-until-data).

Sheets produced:
  * 'E-Class'      : WW=12, PT=12, Summative=2, Term Exam=1  (rows 1-92)
  * 'Consolidated' : WW=6, PT=6 (each = sum of a consecutive pair on E-Class),
                     Summative & Term Exam copied from E-Class.
Kept from the reference template: 'Instruction', 'Input Details', 'Reference'
(+ the descriptor block on E-Class rows 205-308 for Descriptive/Remarks).

Design goals from feedback:
  - minimal / modern look with clear contrast (entries vs totals vs grades)
  - NO pre-filled "0": every computed cell stays blank until real data exists
  - weights displayed as percentages (20%, 50%, 30%, 60%, 40%)
"""

from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter as CL
from openpyxl.cell.cell import MergedCell

SRC = "E-Class-Record-Senior-High-6-17-26.xlsx"
OUT = "E-Class-Record-Senior-High.xlsx"

FIRST_ROW, LAST_ROW, HPS_ROW = 13, 92, 12
G9, G10, SUB = 9, 10, 11

# ---------------------------------------------------------------- palette ---
FONT = "Calibri"
INK = "1F2937"          # near-black text
DARK = "1F3864"         # group header background (deep blue)
MID = "2E5496"          # exam sub-band
SUBHD = "D9E1F2"        # sub-header background (soft blue)
HPSBG = "F3F4F6"        # config/HPS row (light gray)
TOTAL = "BDD7EE"        # TOTAL columns (accent blue)  -> high contrast
PSWS = "EEF2F7"         # PS / WS columns (subtle)
INITBG = "FFF2CC"       # Initial grade (light amber)
FINALBG = "FFD966"      # Final grade (amber)  -> hero contrast
GRPGRAY = "F2F2F2"      # descriptive/remarks
ZEBRA = "F7FAFD"        # alternating student row tint
WHITE = "FFFFFF"

hair = Side(style="thin", color="DDE3EA")
medg = Side(style="medium", color="9AA7B8")
darkg = Side(style="medium", color=DARK)

def border(left=hair, right=hair, top=hair, bottom=hair):
    return Border(left=left, right=right, top=top, bottom=bottom)

CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center", indent=1)

def font(bold=False, color=INK, size=9, italic=False):
    return Font(name=FONT, bold=bold, color=color, size=size, italic=italic)

def fill(hexc):
    return PatternFill("solid", fgColor=hexc)


# --------------------------------------------------------------- layout -----
def build_layout(nww, npt, nst, nte):
    c = 5
    L = {"name": {"No": 1, "Family": 2, "First": 3, "MI": 4}}
    def block(n):
        nonlocal c
        e = list(range(c, c + n)); c += n
        d = {"entries": e, "T": c, "PS": c + 1, "WS": c + 2}; c += 3
        return d
    L["WW"], L["PT"], L["ST"] = block(nww), block(npt), block(nst)
    te = list(range(c, c + nte)); c += nte
    L["TE"] = {"entries": te, "T": c, "PS": c + 1, "WS": c + 2}; c += 3
    L["EX"] = {"PS": c, "WS": c + 1}; c += 2
    L["INIT"], L["FINAL"], L["DESC"], L["REMARK"] = c, c + 1, c + 2, c + 3
    L["END"] = c + 3
    return L


# ----------------------------------------------------- formula fragments ----
def f_T(b, r):
    a, z = CL(b["entries"][0]), CL(b["entries"][-1])
    return f'=IF(COUNT({a}{r}:{z}{r})=0,"",SUM({a}{r}:{z}{r}))'

def f_PS(b, r):
    Tc = f"{CL(b['T'])}{r}"; H = f"${CL(b['T'])}${HPS_ROW}"
    return f'=IF({Tc}="","",IFERROR(ROUND(({Tc}/{H})*100,2),""))'

def f_WS(b, r):
    PSc = f"{CL(b['PS'])}{r}"; W = f"${CL(b['WS'])}${HPS_ROW}"
    return f'=IF({PSc}="","",IFERROR(ROUND(({PSc}*{W}),2),""))'


def write_grades(ws, L, r):
    """T/PS/WS + exam + initial/final/descriptive/remarks (blank-until-data)."""
    for key in ("WW", "PT", "ST", "TE"):
        b = L[key]
        ws.cell(r, b["T"], f_T(b, r))
        ws.cell(r, b["PS"], f_PS(b, r))
        ws.cell(r, b["WS"], f_WS(b, r))
    stws, tews = f"{CL(L['ST']['WS'])}{r}", f"{CL(L['TE']['WS'])}{r}"
    exps, exws = L["EX"]["PS"], L["EX"]["WS"]
    ws.cell(r, exps, f'=IF(AND({stws}="",{tews}=""),"",SUM({stws},{tews}))')
    ec = f"{CL(exps)}{r}"; ew = f"${CL(exws)}${HPS_ROW}"
    ws.cell(r, exws, f'=IF({ec}="","",IFERROR(ROUND(({ec}*{ew}),2),""))')
    wwws, ptws = f"{CL(L['WW']['WS'])}{r}", f"{CL(L['PT']['WS'])}{r}"
    exwsc = f"{CL(exws)}{r}"
    init = f"{CL(L['INIT'])}{r}"
    ws.cell(r, L["INIT"],
            f'=IF(AND({wwws}="",{ptws}="",{exwsc}=""),"",SUM({wwws},{ptws},{exwsc}))')
    ws.cell(r, L["FINAL"],
            f'=IF({init}="","",IFERROR(VLOOKUP({init},Reference!$A$4:$C$15065,2),""))')
    fin = f"${CL(L['FINAL'])}{r}"
    finq = f"{CL(L['FINAL'])}{r}"
    ws.cell(r, L["DESC"], f'=IF({finq}="","",IFERROR(VLOOKUP({fin},{DESC_REF},2),""))')
    ws.cell(r, L["REMARK"], f'=IF({finq}="","",IFERROR(VLOOKUP({fin},{DESC_REF},5),""))')


def hps_row(ws, L, ww, pt, st, te, exam_formula, entry_writer=None):
    for key, w in (("WW", ww), ("PT", pt), ("ST", st), ("TE", te)):
        b = L[key]
        if entry_writer:
            entry_writer(key, b["entries"], HPS_ROW)
        a, z = CL(b["entries"][0]), CL(b["entries"][-1])
        ws.cell(HPS_ROW, b["T"], f'=IF(COUNT({a}{HPS_ROW}:{z}{HPS_ROW})=0,"",SUM({a}{HPS_ROW}:{z}{HPS_ROW}))')
        if key in ("WW", "PT", "ST"):
            ws.cell(HPS_ROW, b["PS"], 100)
        ws.cell(HPS_ROW, b["WS"], w)                 # weight value (decimal)
    ws.cell(HPS_ROW, L["EX"]["WS"], exam_formula)


# ---------------------------------------------------------------- headers ---
def headers(ws, L, exam=("Summative Test (60%)", "Term Examination (40%)")):
    def m(r1, r2, c1, c2, text, bg, fg=INK, bold=True, size=9):
        ws.merge_cells(start_row=r1, start_column=c1, end_row=r2, end_column=c2)
        cell = ws.cell(r1, c1, text)
        cell.font = font(bold=bold, color=fg, size=size)
        cell.alignment = CENTER
        cell.fill = fill(bg)
    m(G9, G10, 1, 4, "LEARNER'S NAME", DARK, WHITE)
    m(G9, G10, L["WW"]["entries"][0], L["WW"]["WS"], "WRITTEN / ORAL WORKS", DARK, WHITE)
    m(G9, G10, L["PT"]["entries"][0], L["PT"]["WS"], "PERFORMANCE TASKS", DARK, WHITE)
    m(G9, G9, L["ST"]["entries"][0], L["EX"]["WS"], "EXAMINATIONS", DARK, WHITE)
    m(G10, G10, L["ST"]["entries"][0], L["ST"]["WS"], exam[0], MID, WHITE)
    m(G10, G10, L["TE"]["entries"][0], L["EX"]["WS"], exam[1], MID, WHITE)
    for col, txt in ((L["INIT"], "INITIAL\nGRADE"), (L["FINAL"], "FINAL\nGRADE"),
                     (L["DESC"], "DESCRIPTIVE"), (L["REMARK"], "REMARKS")):
        m(G9, SUB, col, col, txt, DARK, WHITE)

    for col, txt in ((1, "No."), (2, "Family Name"), (3, "First Name"), (4, "M.I.")):
        ws.merge_cells(start_row=SUB, start_column=col, end_row=HPS_ROW, end_column=col)
        c = ws.cell(SUB, col, txt)
        c.font, c.alignment, c.fill = font(bold=True), CENTER, fill(SUBHD)

    def cat(key, ps, wsx):
        b = L[key]
        for i, ec in enumerate(b["entries"], 1):
            c = ws.cell(SUB, ec, i); c.font, c.alignment, c.fill = font(bold=True), CENTER, fill(SUBHD)
        for col, lbl in ((b["T"], "T"), (b["PS"], ps), (b["WS"], wsx)):
            c = ws.cell(SUB, col, lbl); c.font, c.alignment, c.fill = font(bold=True), CENTER, fill(SUBHD)
    cat("WW", "PS", "WS"); cat("PT", "PS", "WS"); cat("ST", "PS\n(ST)", "WS\n(ST)")
    b = L["TE"]
    for i, ec in enumerate(b["entries"], 1):
        c = ws.cell(SUB, ec, i); c.font, c.alignment, c.fill = font(bold=True), CENTER, fill(SUBHD)
    for col, lbl in ((b["T"], "T"), (b["PS"], "PS\n(TE)"), (b["WS"], "TE"),
                     (L["EX"]["PS"], "PS\n(ST&TE)"), (L["EX"]["WS"], "WS\n(ST&TE)")):
        c = ws.cell(SUB, col, lbl); c.font, c.alignment, c.fill = font(bold=True), CENTER, fill(SUBHD)


def info_block(ws, title, end_col):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=min(end_col, 16))
    t = ws.cell(1, 1, title)
    t.font = Font(name=FONT, bold=True, size=15, color=DARK)
    t.alignment = Alignment(horizontal="left", vertical="center", indent=1)
    ws.row_dimensions[1].height = 26
    rows = [
        ("Region", "='Input Details'!C2", "School", "='Input Details'!C4"),
        ("Division", "='Input Details'!C3", "School ID", "='Input Details'!C5"),
        ("Term", "='Input Details'!C10", "Grade & Section",
         "=CONCATENATE('Input Details'!C13,\" - \",'Input Details'!C14)"),
        ("School Year", "='Input Details'!C11", "Subject", "='Input Details'!C12"),
        ("Teacher", "='Input Details'!K2", "Male / Female",
         "=CONCATENATE('Input Details'!C15,\" / \",'Input Details'!C16)"),
    ]
    for i, (l1, v1, l2, v2) in enumerate(rows):
        r = 3 + i
        a = ws.cell(r, 1, l1.upper()); a.font = font(bold=True, color="6B7280", size=8)
        ws.cell(r, 3, v1).font = font(size=9)
        b = ws.cell(r, 6, l2.upper()); b.font = font(bold=True, color="6B7280", size=8)
        ws.cell(r, 9, v2).font = font(size=9)


# ----------------------------------------------------------- role styling ---
def role_map(L):
    R = {1: "no", 2: "name", 3: "name", 4: "name"}
    for key in ("WW", "PT", "ST", "TE"):
        for ec in L[key]["entries"]:
            R[ec] = "entry"
        R[L[key]["T"]] = "total"; R[L[key]["PS"]] = "ps"; R[L[key]["WS"]] = "ws"
    R[L["EX"]["PS"]] = "ps"; R[L["EX"]["WS"]] = "ws"
    R[L["INIT"]] = "init"; R[L["FINAL"]] = "final"
    R[L["DESC"]] = "desc"; R[L["REMARK"]] = "remark"
    return R


def block_starts(L):
    """columns that begin a visual block -> medium separator on their left."""
    s = {L["WW"]["entries"][0], L["PT"]["entries"][0], L["ST"]["entries"][0],
         L["TE"]["entries"][0], L["INIT"]}
    # also start of each T (total) group for a subtle separation
    for key in ("WW", "PT", "ST", "TE"):
        s.add(L[key]["T"])
    s.add(L["EX"]["PS"])
    return s


def style_body(ws, L):
    R = role_map(L)
    starts = block_starts(L)
    end = L["END"]
    for r in range(FIRST_ROW, LAST_ROW + 1):
        zebra = (r - FIRST_ROW) % 2 == 1
        ws.row_dimensions[r].height = 15
        for c in range(1, end + 1):
            role = R.get(c, "entry")
            cell = ws.cell(r, c)
            if isinstance(cell, MergedCell):
                continue
            left = medg if c in starts else hair
            cell.border = border(left=left)
            if role == "no":
                cell.font = font(color="6B7280"); cell.alignment = CENTER
                cell.fill = fill(ZEBRA if zebra else WHITE)
            elif role == "name":
                cell.font = font(); cell.alignment = LEFT
                cell.fill = fill(ZEBRA if zebra else WHITE)
            elif role == "entry":
                cell.font = font(); cell.alignment = CENTER
                cell.fill = fill(ZEBRA if zebra else WHITE)
            elif role == "total":
                cell.font = font(bold=True); cell.alignment = CENTER
                cell.fill = fill(TOTAL)
            elif role in ("ps", "ws"):
                cell.font = font(); cell.alignment = CENTER
                cell.fill = fill(PSWS)
            elif role == "init":
                cell.font = font(bold=True); cell.alignment = CENTER
                cell.fill = fill(INITBG)
            elif role == "final":
                cell.font = font(bold=True, size=11); cell.alignment = CENTER
                cell.fill = fill(FINALBG)
            elif role == "desc":
                cell.font = font(size=8); cell.alignment = CENTER
                cell.fill = fill(ZEBRA if zebra else WHITE)
            elif role == "remark":
                cell.font = font(bold=True, size=8); cell.alignment = CENTER
                cell.fill = fill(ZEBRA if zebra else WHITE)
    # HPS / weights row (config) - skip merged name columns 1..4
    for c in range(5, end + 1):
        cell = ws.cell(HPS_ROW, c)
        if isinstance(cell, MergedCell):
            continue
        left = medg if c in starts else hair
        cell.border = border(left=left, bottom=medg)
        cell.fill = fill(HPSBG)
        if cell.font is None or not cell.font.bold:
            cell.font = font(bold=True, size=8)
        cell.alignment = CENTER
    # bottom frame
    for c in range(1, end + 1):
        bot = ws.cell(LAST_ROW, c)
        if isinstance(bot, MergedCell):
            continue
        bot.border = border(bottom=darkg, left=medg if c in starts else hair,
                            top=hair, right=hair)


def weight_percent(ws, L):
    for key in ("WW", "PT", "ST", "TE"):
        ws.cell(HPS_ROW, L[key]["WS"]).number_format = "0%"
    ws.cell(HPS_ROW, L["EX"]["WS"]).number_format = "0%"


def col_widths(ws, L):
    ws.column_dimensions["A"].width = 4.2
    ws.column_dimensions["B"].width = 13
    ws.column_dimensions["C"].width = 13
    ws.column_dimensions["D"].width = 4.5
    for key in ("WW", "PT", "ST", "TE"):
        for ec in L[key]["entries"]:
            ws.column_dimensions[CL(ec)].width = 4.2
        ws.column_dimensions[CL(L[key]["T"])].width = 5.2
        ws.column_dimensions[CL(L[key]["PS"])].width = 5.6
        ws.column_dimensions[CL(L[key]["WS"])].width = 5.6
    for col in (L["EX"]["PS"], L["EX"]["WS"], L["INIT"], L["FINAL"]):
        ws.column_dimensions[CL(col)].width = 7
    ws.column_dimensions[CL(L["DESC"])].width = 13
    ws.column_dimensions[CL(L["REMARK"])].width = 8
    for r in (G9, G10, SUB):
        ws.row_dimensions[r].height = {G9: 16, G10: 18, SUB: 26}[r]


# ============================================================================
wb = load_workbook(SRC, data_only=False)
orig = wb["E-Class"]
desc_block = [[orig.cell(r, c).value for c in range(1, 11)] for r in range(205, 309)]
idx = wb.sheetnames.index("E-Class")
del wb["E-Class"]
if "Result" in wb.sheetnames:
    del wb["Result"]

# ---- E-Class -----------------------------------------------------------
ws = wb.create_sheet("E-Class", idx)
ws.sheet_view.showGridLines = False
DESC_REF = "$D$206:$J$307"
L1 = build_layout(12, 12, 2, 1)
info_block(ws, "ELECTRONIC CLASS RECORD", L1["END"])
headers(ws, L1)
hps_row(ws, L1, 0.2, 0.5, 0.6, 0.4, "='Input Details'!K14")
for r in range(FIRST_ROW, LAST_ROW + 1):
    ws.cell(r, 1, r - FIRST_ROW + 1)          # No.
    write_grades(ws, L1, r)
for i, rowvals in enumerate(desc_block):      # descriptor lookup block
    for c, v in enumerate(rowvals, start=1):
        if v is not None:
            ws.cell(205 + i, c, v)
style_body(ws, L1); weight_percent(ws, L1); col_widths(ws, L1)
ws.freeze_panes = ws.cell(FIRST_ROW, 5)

# ---- Consolidated ------------------------------------------------------
ws2 = wb.create_sheet("Consolidated")
ws2.sheet_view.showGridLines = False
S1 = "'E-Class'"
DESC_REF = f"{S1}!$D$206:$J$307"
L2 = build_layout(6, 6, 2, 1)
info_block(ws2, "ELECTRONIC CLASS RECORD  \u00b7  CONSOLIDATED", L2["END"])
headers(ws2, L2)

def pair(key, cols, r):
    """WW/PT -> pair sum (blank until data); ST/TE -> copy (blank until data)."""
    if key in ("WW", "PT"):
        for j, ec in enumerate(cols):
            a, b = CL(L1[key]["entries"][2 * j]), CL(L1[key]["entries"][2 * j + 1])
            ws2.cell(r, ec, f'=IF(AND({S1}!{a}{r}="",{S1}!{b}{r}=""),"",'
                            f'SUM({S1}!{a}{r},{S1}!{b}{r}))')
    else:
        for ec, sc in zip(cols, L1[key]["entries"]):
            s = CL(sc)
            ws2.cell(r, ec, f'=IF({S1}!{s}{r}="","",{S1}!{s}{r})')

hps_row(ws2, L2, 0.2, 0.5, 0.6, 0.4, "='Input Details'!K14", entry_writer=pair)
for r in range(FIRST_ROW, LAST_ROW + 1):
    # No. copies E-Class number; names blank until present
    ws2.cell(r, 1, f'={S1}!A{r}')
    ws2.cell(r, 2, f'=IF({S1}!B{r}="","",{S1}!B{r})')
    ws2.cell(r, 3, f'=IF({S1}!C{r}="","",{S1}!C{r})')
    ws2.cell(r, 4, f'=IF({S1}!D{r}="","",{S1}!D{r})')
    pair("WW", L2["WW"]["entries"], r)
    pair("PT", L2["PT"]["entries"], r)
    pair("ST", L2["ST"]["entries"], r)
    pair("TE", L2["TE"]["entries"], r)
    write_grades(ws2, L2, r)
style_body(ws2, L2); weight_percent(ws2, L2); col_widths(ws2, L2)
ws2.freeze_panes = ws2.cell(FIRST_ROW, 5)

# ---- also show Input Details assessment weights as % -------------------
idet = wb["Input Details"]
for cell in ("K11", "K12", "K13", "K14"):
    if isinstance(idet[cell].value, (int, float)):
        idet[cell].number_format = "0%"

wb.save(OUT)
print("Saved", OUT, "| sheets:", wb.sheetnames)
