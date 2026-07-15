# -*- coding: utf-8 -*-
"""Build the redesigned Kinematics Guided Examples Solution Key (.docx)."""
from docx import Document
from docx.shared import Pt, Twips, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement
import engine as E

# ---- palette -------------------------------------------------------------
NAVY        = "1B365D"
NAVY_SOFT   = "34547D"
INK         = "1F2933"
MUTED       = "5A6472"
GIVEN_FILL  = "EEF3F9"; GIVEN_ACC  = "2E5E8C"
REQ_FILL    = "FBF4E7"; REQ_ACC    = "B0791F"
ANS_FILL    = "E9F5EE"; ANS_ACC    = "2E6F40"
INS_FILL    = "EFF0FB"; INS_ACC    = "3B4CA0"
PROB_FILL   = "F4F6FA"; PROB_ACC   = "1B365D"
ROW_A       = "FFFFFF"; ROW_B      = "F3F6FA"
RULE        = "D9DEE7"

CONTENT_W = 10080
BODY_FONT = "Calibri"
HEAD_FONT = "Calibri"

doc = Document()

# ---- page setup + defaults ------------------------------------------------
sec = doc.sections[0]
sec.page_width  = Twips(12240)
sec.page_height = Twips(15840)
for m in ("top_margin", "bottom_margin"):
    setattr(sec, m, Twips(1080))
sec.left_margin = Twips(1080)
sec.right_margin = Twips(1080)

normal = doc.styles["Normal"]
normal.font.name = BODY_FONT
normal.font.size = Pt(10.5)
normal.font.color.rgb = RGBColor.from_string(INK)
rpr = normal.element.get_or_add_rPr()
rf = rpr.find(qn("w:rFonts"))
if rf is None:
    rf = OxmlElement("w:rFonts"); rpr.append(rf)
rf.set(qn("w:ascii"), BODY_FONT); rf.set(qn("w:hAnsi"), BODY_FONT); rf.set(qn("w:cs"), BODY_FONT)
normal.paragraph_format.space_after = Pt(4)
normal.paragraph_format.line_spacing = 1.12


# ---- generic block helpers ------------------------------------------------
def spacer(after=6, before=0):
    p = doc.add_paragraph()
    E.p_spacing(p, before=before, after=0)
    p.paragraph_format.space_after = Pt(after)
    return p


def full_bar(fill, height_before=140, height_after=140):
    """Return the single cell of a full-width one-cell table."""
    t = doc.add_table(rows=1, cols=1)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    E.set_table_layout_fixed(t, CONTENT_W)
    E.no_table_borders(t)
    E.set_col_widths(t, [CONTENT_W])
    cell = t.rows[0].cells[0]
    E.set_cell_bg(cell, fill)
    E.set_cell_margins(cell, top=height_before, start=200, bottom=height_after, end=200)
    cell.paragraphs[0].text = ""
    return t, cell


def cell_para(cell, first=True):
    if first and cell.paragraphs and not cell.paragraphs[0].runs:
        return cell.paragraphs[0]
    return cell.add_paragraph()


# ---- document-specific blocks --------------------------------------------
def banner():
    t, cell = full_bar(NAVY, 170, 60)
    p = cell.paragraphs[0]
    E.p_spacing(p, after=20)
    E.add_run(p, "PHYSICS LEC 2", bold=True, color="9FC0E8", size=19, font=HEAD_FONT)
    p2 = cell.add_paragraph(); E.p_spacing(p2, after=30)
    E.add_run(p2, "Uniformly Accelerated Motion", bold=True, color="FFFFFF", size=34, font=HEAD_FONT)
    E.add_run(p2, "  (Horizontal)", bold=False, color="C9D8EC", size=22, font=HEAD_FONT)
    p3 = cell.add_paragraph(); E.p_spacing(p3, after=40)
    E.add_run(p3, "GUIDED EXAMPLES  \u00b7  SOLUTION KEY", bold=True, color="8FB2DC", size=15, font=HEAD_FONT)
    p4 = cell.add_paragraph(); E.p_spacing(p4, after=0)
    E.add_run(p4, "Prepared by Philip Jayson L. Lestojas, ECE, ECT", color="D7E2F0", size=15)
    spacer(8)


def strategy_note():
    t, cell = full_bar(PROB_FILL, 130, 130)
    E.set_cell_borders(cell, left=(30, PROB_ACC))
    p = cell.paragraphs[0]; E.p_spacing(p, after=30)
    E.add_run(p, "THE FOUR KINEMATIC EQUATIONS", bold=True, color=NAVY, size=17, font=HEAD_FONT)
    p2 = cell.add_paragraph(); E.p_spacing(p2, after=0)
    E.add_run(p2, "These equations describe motion under constant acceleration. The most efficient "
                  "strategy is to spot the ", color=INK)
    E.add_run(p2, "missing variable", bold=True, color=NAVY)
    E.add_run(p2, " \u2014 the quantity that is neither given nor required \u2014 and then choose the "
                  "equation that omits it.", color=INK)
    spacer(6)


def reference_table():
    rows = [
        ("Equation 1", "v = v_0 + at", "Position ", "(x - x_0)"),
        ("Equation 2", r"x = x_0 + v_0\,t + \tfrac{1}{2}\,a\,t^{2}", "Final velocity ", "(v)"),
        ("Equation 3", r"v^{2} = v_0^{\,2} + 2a\,(x - x_0)", "Time ", "(t)"),
        ("Equation 4", r"x = x_0 + \tfrac{1}{2}\,(v_0 + v)\,t", "Acceleration ", "(a)"),
    ]
    t = doc.add_table(rows=1, cols=3)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    E.set_table_layout_fixed(t, CONTENT_W)
    E.no_table_borders(t)
    widths = [1900, 4600, 3580]
    # header
    hdr = t.rows[0].cells
    heads = ["EQUATION", "FORMULA", "MISSING VARIABLE"]
    for i, h in enumerate(heads):
        E.set_cell_bg(hdr[i], NAVY)
        E.set_cell_margins(hdr[i], top=90, bottom=90, start=150, end=150)
        E.cell_valign(hdr[i], "center")
        p = hdr[i].paragraphs[0]; E.p_spacing(p, after=0)
        E.add_run(p, h, bold=True, color="FFFFFF", size=17, font=HEAD_FONT)
    # body
    for ri, (name, formula, mtxt, mvar) in enumerate(rows):
        cells = t.add_row().cells
        fill = ROW_A if ri % 2 == 0 else ROW_B
        for c in cells:
            E.set_cell_bg(c, fill)
            E.set_cell_margins(c, top=90, bottom=90, start=150, end=150)
            E.cell_valign(c, "center")
            E.set_cell_borders(c, bottom=(4, RULE))
        p0 = cells[0].paragraphs[0]; E.p_spacing(p0, after=0)
        E.add_run(p0, name, bold=True, color=NAVY, size=16)
        p1 = cells[1].paragraphs[0]; E.p_spacing(p1, after=0)
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        E.add_inline_math(p1, formula)
        p2 = cells[2].paragraphs[0]; E.p_spacing(p2, after=0)
        E.add_run(p2, mtxt, color=INK, size=16)
        E.add_inline_math(p2, mvar)
    E.set_col_widths(t, widths)
    spacer(10)


def section_header(num, title):
    t, cell = full_bar(NAVY, 120, 120)
    p = cell.paragraphs[0]; E.p_spacing(p, after=0)
    E.add_run(p, "GUIDED EXAMPLE %d" % num, bold=True, color="9FC0E8", size=15, font=HEAD_FONT)
    E.add_run(p, "     ", size=15)
    E.add_run(p, title, bold=True, color="FFFFFF", size=20, font=HEAD_FONT)
    E.p_keep_next(p)


def problem(text):
    t, cell = full_bar(PROB_FILL, 110, 110)
    E.set_cell_borders(cell, left=(24, PROB_ACC))
    p = cell.paragraphs[0]; E.p_spacing(p, after=0)
    E.add_run(p, "PROBLEM   ", bold=True, color=NAVY, size=14, font=HEAD_FONT)
    E.add_run(p, text, color=INK)
    spacer(6)


def _bullet(cell, first, segments, acc):
    p = cell_para(cell, first)
    E.p_spacing(p, after=40, before=0)
    pf = p.paragraph_format
    p.paragraph_format.left_indent = Twips(180)
    p.paragraph_format.first_line_indent = Twips(-180)
    E.add_run(p, "\u2022  ", bold=True, color=acc)
    for seg in segments:
        kind = seg[0]
        if kind == "t":
            E.add_run(p, seg[1], bold=seg[2] if len(seg) > 2 else False, color=INK)
        elif kind == "b":
            E.add_run(p, seg[1], bold=True, color=NAVY)
        elif kind == "m":
            E.add_inline_math(p, seg[1])
    return p


def given_required(given_items, required_items):
    t = doc.add_table(rows=1, cols=2)
    t.alignment = WD_TABLE_ALIGNMENT.CENTER
    E.set_table_layout_fixed(t, CONTENT_W)
    E.no_table_borders(t)
    gcell, rcell = t.rows[0].cells
    # GIVEN
    E.set_cell_bg(gcell, GIVEN_FILL)
    E.set_cell_borders(gcell, left=(24, GIVEN_ACC))
    E.set_cell_margins(gcell, top=120, bottom=120, start=170, end=170)
    hp = gcell.paragraphs[0]; E.p_spacing(hp, after=50)
    E.add_run(hp, "GIVEN", bold=True, color=GIVEN_ACC, size=15, font=HEAD_FONT)
    for i, item in enumerate(given_items):
        _bullet(gcell, False, item, GIVEN_ACC)
    # REQUIRED
    E.set_cell_bg(rcell, REQ_FILL)
    E.set_cell_borders(rcell, left=(24, REQ_ACC))
    E.set_cell_margins(rcell, top=120, bottom=120, start=170, end=170)
    hp2 = rcell.paragraphs[0]; E.p_spacing(hp2, after=50)
    E.add_run(hp2, "REQUIRED", bold=True, color=REQ_ACC, size=15, font=HEAD_FONT)
    for i, item in enumerate(required_items):
        _bullet(rcell, False, item, REQ_ACC)
    E.set_col_widths(t, [5040, 5040])
    spacer(8)


def solution_header():
    p = doc.add_paragraph(); E.p_spacing(p, before=40, after=30)
    E.add_run(p, "SOLUTION", bold=True, color=NAVY, size=16, font=HEAD_FONT)
    E.add_run(p, "   \u2014   step-by-step derivation", color=MUTED, size=15)
    E.p_keep_next(p)


def step(label, text_segments):
    p = doc.add_paragraph(); E.p_spacing(p, before=30, after=20)
    if label:
        E.add_run(p, label + "   ", bold=True, color=NAVY_SOFT)
    for seg in text_segments:
        kind = seg[0]
        if kind == "t":
            E.add_run(p, seg[1], color=INK)
        elif kind == "b":
            E.add_run(p, seg[1], bold=True, color=NAVY)
        elif kind == "i":
            E.add_run(p, seg[1], italic=True, color=INK)
        elif kind == "m":
            E.add_inline_math(p, seg[1])
    E.p_keep_next(p)
    return p


def derive(aligned_latex):
    p = doc.add_paragraph(); E.p_spacing(p, before=20, after=20)
    E.add_display_math(p, r"\begin{aligned}" + aligned_latex + r"\end{aligned}")
    return p


def answer_box(label, math_latex, note=None):
    t, cell = full_bar(ANS_FILL, 90, 90)
    E.set_cell_borders(cell, left=(34, ANS_ACC), top=(6, ANS_ACC),
                       right=(6, ANS_ACC), bottom=(6, ANS_ACC))
    p = cell.paragraphs[0]; E.p_spacing(p, after=0)
    E.add_run(p, "ANSWER", bold=True, color=ANS_ACC, size=13, font=HEAD_FONT)
    if label:
        E.add_run(p, "  \u00b7  " + label, bold=True, color=ANS_ACC, size=13)
    E.add_run(p, "     ")
    E.add_inline_math(p, math_latex)
    if note:
        E.add_run(p, "   " + note, italic=True, color=MUTED, size=15)
    spacer(6)


def conclusion_box(label, text):
    t, cell = full_bar(ANS_FILL, 90, 90)
    E.set_cell_borders(cell, left=(34, ANS_ACC), top=(6, ANS_ACC),
                       right=(6, ANS_ACC), bottom=(6, ANS_ACC))
    p = cell.paragraphs[0]; E.p_spacing(p, after=0)
    E.add_run(p, "CONCLUSION", bold=True, color=ANS_ACC, size=13, font=HEAD_FONT)
    if label:
        E.add_run(p, "  \u00b7  " + label, bold=True, color=ANS_ACC, size=13)
    p2 = cell.add_paragraph(); E.p_spacing(p2, after=0)
    E.add_run(p2, text, color=INK)
    spacer(6)


def insight(text_runs):
    t, cell = full_bar(INS_FILL, 120, 120)
    E.set_cell_borders(cell, left=(30, INS_ACC))
    p = cell.paragraphs[0]; E.p_spacing(p, after=30)
    E.add_run(p, "PEDAGOGICAL INSIGHT", bold=True, color=INS_ACC, size=15, font=HEAD_FONT)
    p2 = cell.add_paragraph(); E.p_spacing(p2, after=0)
    for seg in text_runs:
        if seg[0] == "t":
            E.add_run(p2, seg[1], color=INK)
        elif seg[0] == "b":
            E.add_run(p2, seg[1], bold=True, color=INS_ACC)
        elif seg[0] == "m":
            E.add_inline_math(p2, seg[1])
    spacer(12)


# ===========================================================================
#  CONTENT
# ===========================================================================
import content
content.build(globals())

doc.save("/projects/sandbox/Kinematics-Guided-Examples-Solution-Key.docx")
print("Document saved.")
