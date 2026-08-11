"""
Generate an E-Class Record workbook with two sheets.

Sheet 1 ("E-Class Record"):
    - Written/Oral Works : 12 entries
    - Performance Tasks   : 12 entries
    - Summative Test      :  2 entries
    - Term Exam           :  1 entry
    Each category has a per-row Total formula. Table spans to row 92.

Sheet 2 ("Consolidated"):
    - Written/Oral Works : 6 entries  -> entry k = Sheet1 WW(2k-1) + WW(2k)
    - Performance Tasks   : 6 entries  -> entry k = Sheet1 PT(2k-1) + PT(2k)
    - Summative Test      : 2 entries  -> copied straight from Sheet 1
    - Term Exam           : 1 entry    -> copied straight from Sheet 1
    Each category has a per-row Total formula.
"""

from openpyxl import Workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.utils import get_column_letter

# ----------------------------------------------------------------------------
# Layout constants
# ----------------------------------------------------------------------------
INFO_ROWS = 4          # rows 1..4 : title + school info
GROUP_ROW = 6          # merged category header row
NUM_ROW = 7            # numbered sub-header row (1,2,3, ... , Total)
HPS_ROW = 8            # Highest Possible Score row
FIRST_STUDENT_ROW = 9
LAST_ROW = 92          # table spans down to row 92
N_STUDENTS = LAST_ROW - FIRST_STUDENT_ROW + 1  # rows 9..92

# ----------------------------------------------------------------------------
# Styles
# ----------------------------------------------------------------------------
thin = Side(style="thin", color="000000")
BORDER = Border(left=thin, right=thin, top=thin, bottom=thin)
CENTER = Alignment(horizontal="center", vertical="center", wrap_text=True)
LEFT = Alignment(horizontal="left", vertical="center")
BOLD = Font(bold=True)
TITLE_FONT = Font(bold=True, size=14)

WW_FILL = PatternFill("solid", fgColor="DDEBF7")   # light blue
PT_FILL = PatternFill("solid", fgColor="E2EFDA")   # light green
ST_FILL = PatternFill("solid", fgColor="FFF2CC")   # light yellow
TE_FILL = PatternFill("solid", fgColor="FCE4D6")   # light orange
NAME_FILL = PatternFill("solid", fgColor="F2F2F2")
TOTAL_FILL = PatternFill("solid", fgColor="D9D9D9")

# category name, number of entries, fill
CATEGORIES = {
    "WW": ("WRITTEN / ORAL WORKS", WW_FILL),
    "PT": ("PERFORMANCE TASKS", PT_FILL),
    "ST": ("SUMMATIVE TEST", ST_FILL),
    "TE": ("TERM EXAM", TE_FILL),
}


def build_column_map(counts):
    """Return list of (key, kind, index) columns starting after No.+Name.

    kind is 'entry' or 'total'. Returns dict with per-category entry columns
    and total column, plus the next free column.
    """
    col = 3  # A=No, B=Name
    layout = {}
    for key in ("WW", "PT", "ST", "TE"):
        n = counts[key]
        entry_cols = list(range(col, col + n))
        col += n
        total_col = col
        col += 1
        layout[key] = {"entries": entry_cols, "total": total_col}
    layout["_end"] = col - 1
    return layout


def style_header(ws, layout):
    """Draw the No./Name headers + category group headers + numbered row + HPS."""
    # No. and Name headers (merge across group+num rows)
    ws.merge_cells(start_row=GROUP_ROW, start_column=1, end_row=NUM_ROW, end_column=1)
    ws.merge_cells(start_row=GROUP_ROW, start_column=2, end_row=NUM_ROW, end_column=2)
    c = ws.cell(GROUP_ROW, 1, "No.")
    c.font, c.alignment, c.fill = BOLD, CENTER, NAME_FILL
    c = ws.cell(GROUP_ROW, 2, "LEARNER'S NAME")
    c.font, c.alignment, c.fill = BOLD, CENTER, NAME_FILL

    # HPS label under Name
    hc = ws.cell(HPS_ROW, 2, "Highest Possible Score")
    hc.font, hc.alignment, hc.fill = BOLD, LEFT, TOTAL_FILL

    for key in ("WW", "PT", "ST", "TE"):
        label, fill = CATEGORIES[key]
        entries = layout[key]["entries"]
        total = layout[key]["total"]
        first, last = entries[0], total
        # merged group header spans entries + total
        ws.merge_cells(start_row=GROUP_ROW, start_column=first,
                       end_row=GROUP_ROW, end_column=last)
        g = ws.cell(GROUP_ROW, first, label)
        g.font, g.alignment, g.fill = BOLD, CENTER, fill
        # numbered sub-headers
        for i, ecol in enumerate(entries, start=1):
            sc = ws.cell(NUM_ROW, ecol, i)
            sc.font, sc.alignment, sc.fill = BOLD, CENTER, fill
        tc = ws.cell(NUM_ROW, total, "TOTAL")
        tc.font, tc.alignment, tc.fill = BOLD, CENTER, TOTAL_FILL
        # HPS row entry cells (blank, to be filled by teacher) + total formula
        for ecol in entries:
            hc = ws.cell(HPS_ROW, ecol)
            hc.alignment, hc.fill = CENTER, TOTAL_FILL
        first_letter = get_column_letter(entries[0])
        last_letter = get_column_letter(entries[-1])
        htot = ws.cell(HPS_ROW, total,
                       f"=SUM({first_letter}{HPS_ROW}:{last_letter}{HPS_ROW})")
        htot.font, htot.alignment, htot.fill = BOLD, CENTER, TOTAL_FILL


def apply_borders(ws, layout):
    for r in range(GROUP_ROW, LAST_ROW + 1):
        for col in range(1, layout["_end"] + 1):
            ws.cell(r, col).border = BORDER


def set_widths(ws, layout):
    ws.column_dimensions["A"].width = 5
    ws.column_dimensions["B"].width = 28
    for key in ("WW", "PT", "ST", "TE"):
        for ecol in layout[key]["entries"]:
            ws.column_dimensions[get_column_letter(ecol)].width = 6
        ws.column_dimensions[get_column_letter(layout[key]["total"])].width = 8


def write_info_block(ws, title, subject_line, section_line, end_col):
    ws.merge_cells(start_row=1, start_column=1, end_row=1, end_column=min(end_col, 12))
    t = ws.cell(1, 1, title)
    t.font, t.alignment = TITLE_FONT, CENTER
    ws.cell(2, 1, "Subject:").font = BOLD
    ws.cell(2, 3, subject_line)
    ws.cell(3, 1, "Grade & Section:").font = BOLD
    ws.cell(3, 3, section_line)
    ws.cell(4, 1, "Teacher:").font = BOLD


# ----------------------------------------------------------------------------
# Sheet 1
# ----------------------------------------------------------------------------
wb = Workbook()
ws1 = wb.active
ws1.title = "E-Class Record"

counts1 = {"WW": 12, "PT": 12, "ST": 2, "TE": 1}
layout1 = build_column_map(counts1)

write_info_block(ws1, "ELECTRONIC CLASS RECORD", "________________________",
                 "________________________", layout1["_end"])
style_header(ws1, layout1)

for idx, row in enumerate(range(FIRST_STUDENT_ROW, LAST_ROW + 1), start=1):
    n = ws1.cell(row, 1, idx)
    n.alignment = CENTER
    ws1.cell(row, 2).alignment = LEFT
    for key in ("WW", "PT", "ST", "TE"):
        entries = layout1[key]["entries"]
        total = layout1[key]["total"]
        for ecol in entries:
            ws1.cell(row, ecol).alignment = CENTER
        fl = get_column_letter(entries[0])
        ll = get_column_letter(entries[-1])
        tcell = ws1.cell(row, total, f"=SUM({fl}{row}:{ll}{row})")
        tcell.alignment = CENTER
        tcell.fill = TOTAL_FILL

apply_borders(ws1, layout1)
set_widths(ws1, layout1)
ws1.freeze_panes = "C9"

# ----------------------------------------------------------------------------
# Sheet 2
# ----------------------------------------------------------------------------
ws2 = wb.create_sheet("Consolidated")
counts2 = {"WW": 6, "PT": 6, "ST": 2, "TE": 1}
layout2 = build_column_map(counts2)

write_info_block(ws2, "ELECTRONIC CLASS RECORD - CONSOLIDATED",
                 "________________________", "________________________",
                 layout2["_end"])
style_header(ws2, layout2)

S1 = "'E-Class Record'"

for row in range(FIRST_STUDENT_ROW, LAST_ROW + 1):
    # No. and Name reference sheet 1
    n = ws2.cell(row, 1, f"={S1}!A{row}")
    n.alignment = CENTER
    nm = ws2.cell(row, 2, f"={S1}!B{row}")
    nm.alignment = LEFT

    # HPS row references sheet1 pairing too (do only once, handled below)
    for key in ("WW", "PT"):
        entries2 = layout2[key]["entries"]          # 6 columns on sheet 2
        s1_entries = layout1[key]["entries"]        # 12 columns on sheet 1
        for k, ecol in enumerate(entries2):         # k = 0..5
            a = get_column_letter(s1_entries[2 * k])
            b = get_column_letter(s1_entries[2 * k + 1])
            cell = ws2.cell(row, ecol, f"={S1}!{a}{row}+{S1}!{b}{row}")
            cell.alignment = CENTER
        total = layout2[key]["total"]
        fl = get_column_letter(entries2[0])
        ll = get_column_letter(entries2[-1])
        tcell = ws2.cell(row, total, f"=SUM({fl}{row}:{ll}{row})")
        tcell.alignment = CENTER
        tcell.fill = TOTAL_FILL

    # Summative Test + Term Exam : copy straight from sheet 1
    for key in ("ST", "TE"):
        entries2 = layout2[key]["entries"]
        s1_entries = layout1[key]["entries"]
        for ecol2, ecol1 in zip(entries2, s1_entries):
            a = get_column_letter(ecol1)
            cell = ws2.cell(row, ecol2, f"={S1}!{a}{row}")
            cell.alignment = CENTER
        total = layout2[key]["total"]
        fl = get_column_letter(entries2[0])
        ll = get_column_letter(entries2[-1])
        tcell = ws2.cell(row, total, f"=SUM({fl}{row}:{ll}{row})")
        tcell.alignment = CENTER
        tcell.fill = TOTAL_FILL

# HPS row on sheet 2 (pair sums / copies from sheet1 HPS)
for key in ("WW", "PT"):
    entries2 = layout2[key]["entries"]
    s1_entries = layout1[key]["entries"]
    for k, ecol in enumerate(entries2):
        a = get_column_letter(s1_entries[2 * k])
        b = get_column_letter(s1_entries[2 * k + 1])
        ws2.cell(HPS_ROW, ecol, f"={S1}!{a}{HPS_ROW}+{S1}!{b}{HPS_ROW}").alignment = CENTER
for key in ("ST", "TE"):
    entries2 = layout2[key]["entries"]
    s1_entries = layout1[key]["entries"]
    for ecol2, ecol1 in zip(entries2, s1_entries):
        a = get_column_letter(ecol1)
        ws2.cell(HPS_ROW, ecol2, f"={S1}!{a}{HPS_ROW}").alignment = CENTER

apply_borders(ws2, layout2)
set_widths(ws2, layout2)
ws2.freeze_panes = "C9"

OUT = "E-Class-Record-Senior-High.xlsx"
wb.save(OUT)
print("Saved", OUT)
print("Sheet1 layout:", {k: v for k, v in layout1.items()})
print("Sheet2 layout:", {k: v for k, v in layout2.items()})
