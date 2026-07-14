"""
Generates kinematics_worksheet.docx
Page 1: Student Activity Sheet (4 vertical columns, guided derivation)
Page 2: Teacher's Answer Key (same layout, answers in RED)

Layout: Landscape, 13in x 8.5in, narrow margins.
One row of FOUR VERTICAL COLUMNS (side by side).
Each column = one independent guided derivation activity (Part A-D).

Pedagogy: Instruction -> blank response line(s) -> instruction -> blank -> ...
until the student arrives at the goal equation.
Font: Calibri, size 9pt.
Equations: OMML (Office Math Markup Language).
Monochrome grayscale for student sheet; red answers on answer key.
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml

BLACK = RGBColor(0, 0, 0)
RED = RGBColor(0xFF, 0x00, 0x00)
GRAY = RGBColor(0x55, 0x55, 0x55)
LIGHT_GRAY_FILL = "E8E8E8"

MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# ============================================================================
# OMML Equation builders
# ============================================================================

def omml_run(text):
    """Plain (upright) math run."""
    return f'<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>{text}</m:t></m:r>'

def omml_run_italic(text):
    """Italic math run (variable style)."""
    return f'<m:r><m:t>{text}</m:t></m:r>'

def omml_run_red(text):
    """Red upright math run for answer key."""
    return (f'<m:r><m:rPr><m:sty m:val="p"/></m:rPr>'
            f'<w:rPr xmlns:w="{W_NS}"><w:color w:val="FF0000"/></w:rPr>'
            f'<m:t>{text}</m:t></m:r>')

def omml_run_italic_red(text):
    """Red italic math run for answer key."""
    return (f'<m:r>'
            f'<w:rPr xmlns:w="{W_NS}"><w:color w:val="FF0000"/></w:rPr>'
            f'<m:t>{text}</m:t></m:r>')

def omml_frac(num, den):
    return f'<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f>'

def omml_sub(base, sub):
    return f'<m:sSub><m:e>{base}</m:e><m:sub>{sub}</m:sub></m:sSub>'

def omml_sup(base, sup):
    return f'<m:sSup><m:e>{base}</m:e><m:sup>{sup}</m:sup></m:sSup>'

def omml_subsup(base, sub, sup):
    return f'<m:sSubSup><m:e>{base}</m:e><m:sub>{sub}</m:sub><m:sup>{sup}</m:sup></m:sSubSup>'

def omml_d(content, left="(", right=")"):
    beg = f'<m:dPr><m:begChr m:val="{left}"/><m:endChr m:val="{right}"/></m:dPr>' if left != "(" or right != ")" else ""
    return f'<m:d>{beg}<m:e>{content}</m:e></m:d>'

def omml_d_bracket(content):
    return omml_d(content, left="[", right="]")


def insert_display_equation(cell, omml_content, space_before=2, space_after=2):
    """Insert a centered OMML display equation paragraph into a cell."""
    if callable(omml_content):
        omml_content = omml_content()
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    xml_str = f'<m:oMathPara xmlns:m="{MATH_NS}" xmlns:w="{W_NS}"><m:oMath>{omml_content}</m:oMath></m:oMathPara>'
    el = parse_xml(xml_str)
    p._p.append(el)
    return p


def insert_inline_equation(paragraph, omml_content):
    """Insert an inline OMML equation into an existing paragraph."""
    if callable(omml_content):
        omml_content = omml_content()
    xml_str = f'<m:oMath xmlns:m="{MATH_NS}" xmlns:w="{W_NS}">{omml_content}</m:oMath>'
    el = parse_xml(xml_str)
    paragraph._p.append(el)


# ============================================================================
# OMML equation definitions (black, for student sheet & instructions)
# ============================================================================

# a = Δv/Δt
def eq_a_def():
    return (omml_run_italic("a") + omml_run(" = ") +
            omml_frac(omml_run_italic("\u0394v"), omml_run_italic("\u0394t")))

# a = (v - v₀)/t
def eq_a_expanded():
    num = omml_run_italic("v") + omml_run(" \u2212 ") + omml_sub(omml_run_italic("v"), omml_run("0"))
    return (omml_run_italic("a") + omml_run(" = ") +
            omml_frac(num, omml_run_italic("t")))

# at = v - v₀
def eq_at_equals():
    return (omml_run_italic("at") + omml_run(" = ") +
            omml_run_italic("v") + omml_run(" \u2212 ") +
            omml_sub(omml_run_italic("v"), omml_run("0")))

# v = v₀ + at
def eq_v_v0_at():
    return (omml_run_italic("v") + omml_run(" = ") +
            omml_sub(omml_run_italic("v"), omml_run("0")) +
            omml_run(" + ") + omml_run_italic("at"))

# v_avg = Δx/Δt = (x - x₀)/t
def eq_vavg_def():
    num = omml_run_italic("x") + omml_run(" \u2212 ") + omml_sub(omml_run_italic("x"), omml_run("0"))
    return (omml_sub(omml_run_italic("v"), omml_run("avg")) + omml_run(" = ") +
            omml_frac(omml_run_italic("\u0394x"), omml_run_italic("\u0394t")) +
            omml_run(" = ") + omml_frac(num, omml_run_italic("t")))

# x - x₀ = v_avg · t  →  x = x₀ + v_avg · t
def eq_x_vavg():
    return (omml_run_italic("x") + omml_run(" = ") +
            omml_sub(omml_run_italic("x"), omml_run("0")) +
            omml_run(" + ") +
            omml_sub(omml_run_italic("v"), omml_run("avg")) +
            omml_run(" \u00b7 ") + omml_run_italic("t"))

# v_avg = (v₀ + v)/2
def eq_vavg_mean():
    num = omml_sub(omml_run_italic("v"), omml_run("0")) + omml_run(" + ") + omml_run_italic("v")
    return (omml_sub(omml_run_italic("v"), omml_run("avg")) + omml_run(" = ") +
            omml_frac(num, omml_run("2")))

# x = x₀ + ½(v₀ + v)t
def eq_x_half_vv0_t():
    inner = omml_sub(omml_run_italic("v"), omml_run("0")) + omml_run(" + ") + omml_run_italic("v")
    return (omml_run_italic("x") + omml_run(" = ") +
            omml_sub(omml_run_italic("x"), omml_run("0")) + omml_run(" + ") +
            omml_frac(omml_run("1"), omml_run("2")) +
            omml_d(inner) + omml_run_italic("t"))

# Eq1: v = v₀ + at  (for reference)
def eq_eq1_ref():
    return eq_v_v0_at()

# Eq4: x = x₀ + ½(v₀ + v)t  (for reference)
def eq_eq4_ref():
    return eq_x_half_vv0_t()

# x = x₀ + ½[v₀ + (v₀ + at)]t
def eq_x_substituted():
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    v0_2 = omml_sub(omml_run_italic("v"), omml_run("0"))
    inner_paren = omml_d(v0_2 + omml_run(" + ") + omml_run_italic("at"))
    bracket_content = v0 + omml_run(" + ") + inner_paren
    bracket = omml_d_bracket(bracket_content)
    return (omml_run_italic("x") + omml_run(" = ") +
            omml_sub(omml_run_italic("x"), omml_run("0")) + omml_run(" + ") +
            omml_frac(omml_run("1"), omml_run("2")) + bracket + omml_run_italic("t"))

# x = x₀ + ½[2v₀ + at]t
def eq_x_combined():
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    bracket_content = omml_run("2") + v0 + omml_run(" + ") + omml_run_italic("at")
    bracket = omml_d_bracket(bracket_content)
    return (omml_run_italic("x") + omml_run(" = ") +
            omml_sub(omml_run_italic("x"), omml_run("0")) + omml_run(" + ") +
            omml_frac(omml_run("1"), omml_run("2")) + bracket + omml_run_italic("t"))

# x = x₀ + v₀t + ½at²
def eq_x_v0t_half_at2():
    return (omml_run_italic("x") + omml_run(" = ") +
            omml_sub(omml_run_italic("x"), omml_run("0")) + omml_run(" + ") +
            omml_sub(omml_run_italic("v"), omml_run("0")) + omml_run_italic("t") +
            omml_run(" + ") +
            omml_frac(omml_run("1"), omml_run("2")) +
            omml_run_italic("a") + omml_sup(omml_run_italic("t"), omml_run("2")))

# t = (v - v₀)/a
def eq_t_from_v():
    num = omml_run_italic("v") + omml_run(" \u2212 ") + omml_sub(omml_run_italic("v"), omml_run("0"))
    return (omml_run_italic("t") + omml_run(" = ") +
            omml_frac(num, omml_run_italic("a")))

# x - x₀ = ½(v₀ + v)·t   (displacement form)
def eq_disp_vavg():
    inner = omml_sub(omml_run_italic("v"), omml_run("0")) + omml_run(" + ") + omml_run_italic("v")
    return (omml_run_italic("x") + omml_run(" \u2212 ") +
            omml_sub(omml_run_italic("x"), omml_run("0")) + omml_run(" = ") +
            omml_frac(omml_run("1"), omml_run("2")) +
            omml_d(inner) + omml_run_italic("t"))

# x - x₀ = ½(v + v₀)·(v - v₀)/a
def eq_disp_substituted():
    inner = omml_run_italic("v") + omml_run(" + ") + omml_sub(omml_run_italic("v"), omml_run("0"))
    num_frac = omml_run_italic("v") + omml_run(" \u2212 ") + omml_sub(omml_run_italic("v"), omml_run("0"))
    return (omml_run_italic("x") + omml_run(" \u2212 ") +
            omml_sub(omml_run_italic("x"), omml_run("0")) + omml_run(" = ") +
            omml_frac(omml_run("1"), omml_run("2")) +
            omml_d(inner) + omml_run(" \u00b7 ") +
            omml_frac(num_frac, omml_run_italic("a")))

# x - x₀ = (v² - v₀²) / 2a
def eq_disp_diff_squares():
    num = omml_sup(omml_run_italic("v"), omml_run("2")) + omml_run(" \u2212 ") + omml_subsup(omml_run_italic("v"), omml_run("0"), omml_run("2"))
    den = omml_run("2") + omml_run_italic("a")
    return (omml_run_italic("x") + omml_run(" \u2212 ") +
            omml_sub(omml_run_italic("x"), omml_run("0")) + omml_run(" = ") +
            omml_frac(num, den))

# v² = v₀² + 2a(x - x₀)
def eq_v2_final():
    inner = omml_run_italic("x") + omml_run(" \u2212 ") + omml_sub(omml_run_italic("x"), omml_run("0"))
    return (omml_sup(omml_run_italic("v"), omml_run("2")) + omml_run(" = ") +
            omml_subsup(omml_run_italic("v"), omml_run("0"), omml_run("2")) +
            omml_run(" + 2") + omml_run_italic("a") + omml_d(inner))


# ============================================================================
# RED versions of equations (for answer key)
# ============================================================================

def eq_a_def_red():
    return (omml_run_italic_red("a") + omml_run_red(" = ") +
            omml_frac(omml_run_italic_red("\u0394v"), omml_run_italic_red("\u0394t")))

def eq_a_expanded_red():
    num = omml_run_italic_red("v") + omml_run_red(" \u2212 ") + omml_sub(omml_run_italic_red("v"), omml_run_red("0"))
    return (omml_run_italic_red("a") + omml_run_red(" = ") +
            omml_frac(num, omml_run_italic_red("t")))

def eq_at_equals_red():
    return (omml_run_italic_red("at") + omml_run_red(" = ") +
            omml_run_italic_red("v") + omml_run_red(" \u2212 ") +
            omml_sub(omml_run_italic_red("v"), omml_run_red("0")))

def eq_v_v0_at_red():
    return (omml_run_italic_red("v") + omml_run_red(" = ") +
            omml_sub(omml_run_italic_red("v"), omml_run_red("0")) +
            omml_run_red(" + ") + omml_run_italic_red("at"))

def eq_vavg_def_red():
    num = omml_run_italic_red("x") + omml_run_red(" \u2212 ") + omml_sub(omml_run_italic_red("x"), omml_run_red("0"))
    return (omml_sub(omml_run_italic_red("v"), omml_run_red("avg")) + omml_run_red(" = ") +
            omml_frac(num, omml_run_italic_red("t")))

def eq_x_vavg_red():
    return (omml_run_italic_red("x") + omml_run_red(" = ") +
            omml_sub(omml_run_italic_red("x"), omml_run_red("0")) +
            omml_run_red(" + ") +
            omml_sub(omml_run_italic_red("v"), omml_run_red("avg")) +
            omml_run_red(" \u00b7 ") + omml_run_italic_red("t"))

def eq_vavg_mean_red():
    num = omml_sub(omml_run_italic_red("v"), omml_run_red("0")) + omml_run_red(" + ") + omml_run_italic_red("v")
    return (omml_sub(omml_run_italic_red("v"), omml_run_red("avg")) + omml_run_red(" = ") +
            omml_frac(num, omml_run_red("2")))

def eq_x_half_vv0_t_red():
    inner = omml_sub(omml_run_italic_red("v"), omml_run_red("0")) + omml_run_red(" + ") + omml_run_italic_red("v")
    return (omml_run_italic_red("x") + omml_run_red(" = ") +
            omml_sub(omml_run_italic_red("x"), omml_run_red("0")) + omml_run_red(" + ") +
            omml_frac(omml_run_red("1"), omml_run_red("2")) +
            omml_d(inner) + omml_run_italic_red("t"))

def eq_x_substituted_red():
    v0 = omml_sub(omml_run_italic_red("v"), omml_run_red("0"))
    v0_2 = omml_sub(omml_run_italic_red("v"), omml_run_red("0"))
    inner_paren = omml_d(v0_2 + omml_run_red(" + ") + omml_run_italic_red("at"))
    bracket_content = v0 + omml_run_red(" + ") + inner_paren
    bracket = omml_d_bracket(bracket_content)
    return (omml_run_italic_red("x") + omml_run_red(" = ") +
            omml_sub(omml_run_italic_red("x"), omml_run_red("0")) + omml_run_red(" + ") +
            omml_frac(omml_run_red("1"), omml_run_red("2")) + bracket + omml_run_italic_red("t"))

def eq_x_combined_red():
    v0 = omml_sub(omml_run_italic_red("v"), omml_run_red("0"))
    bracket_content = omml_run_red("2") + v0 + omml_run_red(" + ") + omml_run_italic_red("at")
    bracket = omml_d_bracket(bracket_content)
    return (omml_run_italic_red("x") + omml_run_red(" = ") +
            omml_sub(omml_run_italic_red("x"), omml_run_red("0")) + omml_run_red(" + ") +
            omml_frac(omml_run_red("1"), omml_run_red("2")) + bracket + omml_run_italic_red("t"))

def eq_x_v0t_half_at2_red():
    return (omml_run_italic_red("x") + omml_run_red(" = ") +
            omml_sub(omml_run_italic_red("x"), omml_run_red("0")) + omml_run_red(" + ") +
            omml_sub(omml_run_italic_red("v"), omml_run_red("0")) + omml_run_italic_red("t") +
            omml_run_red(" + ") +
            omml_frac(omml_run_red("1"), omml_run_red("2")) +
            omml_run_italic_red("a") + omml_sup(omml_run_italic_red("t"), omml_run_red("2")))

def eq_t_from_v_red():
    num = omml_run_italic_red("v") + omml_run_red(" \u2212 ") + omml_sub(omml_run_italic_red("v"), omml_run_red("0"))
    return (omml_run_italic_red("t") + omml_run_red(" = ") +
            omml_frac(num, omml_run_italic_red("a")))

def eq_disp_substituted_red():
    inner = omml_run_italic_red("v") + omml_run_red(" + ") + omml_sub(omml_run_italic_red("v"), omml_run_red("0"))
    num_frac = omml_run_italic_red("v") + omml_run_red(" \u2212 ") + omml_sub(omml_run_italic_red("v"), omml_run_red("0"))
    return (omml_run_italic_red("x") + omml_run_red(" \u2212 ") +
            omml_sub(omml_run_italic_red("x"), omml_run_red("0")) + omml_run_red(" = ") +
            omml_frac(omml_run_red("1"), omml_run_red("2")) +
            omml_d(inner) + omml_run_red(" \u00b7 ") +
            omml_frac(num_frac, omml_run_italic_red("a")))

def eq_disp_diff_squares_red():
    num = omml_sup(omml_run_italic_red("v"), omml_run_red("2")) + omml_run_red(" \u2212 ") + omml_subsup(omml_run_italic_red("v"), omml_run_red("0"), omml_run_red("2"))
    den = omml_run_red("2") + omml_run_italic_red("a")
    return (omml_run_italic_red("x") + omml_run_red(" \u2212 ") +
            omml_sub(omml_run_italic_red("x"), omml_run_red("0")) + omml_run_red(" = ") +
            omml_frac(num, den))

def eq_v2_final_red():
    inner = omml_run_italic_red("x") + omml_run_red(" \u2212 ") + omml_sub(omml_run_italic_red("x"), omml_run_red("0"))
    return (omml_sup(omml_run_italic_red("v"), omml_run_red("2")) + omml_run_red(" = ") +
            omml_subsup(omml_run_italic_red("v"), omml_run_red("0"), omml_run_red("2")) +
            omml_run_red(" + 2") + omml_run_italic_red("a") + omml_d(inner))


# ============================================================================
# Low level OXML helpers
# ============================================================================

def set_cell_border(cell, **kwargs):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = tcPr.find(qn('w:tcBorders'))
    if tcBorders is None:
        tcBorders = OxmlElement('w:tcBorders')
        tcPr.append(tcBorders)
    for edge in ('top', 'left', 'bottom', 'right'):
        spec = kwargs.get(edge)
        if spec is None:
            continue
        tag = f'w:{edge}'
        el = tcBorders.find(qn(tag))
        if el is None:
            el = OxmlElement(tag)
            tcBorders.append(el)
        el.set(qn('w:val'), spec.get('val', 'single'))
        el.set(qn('w:sz'), str(spec.get('sz', 6)))
        el.set(qn('w:space'), '0')
        el.set(qn('w:color'), spec.get('color', '000000'))


def set_cell_margins(cell, top=30, bottom=30, left=55, right=55):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for edge, val in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        node = OxmlElement(f'w:{edge}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        mar.append(node)
    tcPr.append(mar)


def set_col_width(cell, width):
    cell.width = width
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = OxmlElement('w:tcW')
    tcW.set(qn('w:w'), str(int(width)))
    tcW.set(qn('w:type'), 'dxa')
    tcPr.append(tcW)


def disable_autofit(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)


def set_row_height(row, twips, exact=False):
    trPr = row._tr.get_or_add_trPr()
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), str(twips))
    trHeight.set(qn('w:hRule'), 'exact' if exact else 'atLeast')
    trPr.append(trHeight)


def set_paragraph_border_bottom(paragraph, sz=4, color="AAAAAA"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el = OxmlElement('w:bottom')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), str(sz))
    el.set(qn('w:space'), '1')
    el.set(qn('w:color'), color)
    pBdr.append(el)
    pPr.append(pBdr)


def set_paragraph_shading(paragraph, hex_color):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    pPr.append(shd)


def set_paragraph_borders_all(paragraph, sz=6, color="000000"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for edge in ('top', 'left', 'bottom', 'right'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), 'single')
        el.set(qn('w:sz'), str(sz))
        el.set(qn('w:space'), '2')
        el.set(qn('w:color'), color)
        pBdr.append(el)
    pPr.append(pBdr)


# ============================================================================
# Text helpers
# ============================================================================

FONT_NAME = "Calibri"
FONT_SIZE = Pt(9)
FONT_SIZE_SM = Pt(8)
FONT_SIZE_XS = Pt(7.5)


def add_run(paragraph, text, bold=False, italic=False, underline=False,
            size=FONT_SIZE, color=BLACK):
    r = paragraph.add_run(text)
    r.font.name = FONT_NAME
    r.font.size = size
    r.bold = bold
    r.italic = italic
    r.underline = underline
    r.font.color.rgb = color
    return r


def add_instruction(cell, text, space_before=4, space_after=1, inline_eq=None):
    """Add an instruction paragraph, optionally with an inline OMML equation at the end."""
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    add_run(p, text, size=FONT_SIZE)
    if inline_eq:
        insert_inline_equation(p, inline_eq)
    return p


def add_blank_lines(cell, count=2):
    """Add blank response lines with underline for student to write on."""
    for i in range(count):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(2 if i > 0 else 4)
        p.paragraph_format.space_after = Pt(0)
        set_paragraph_border_bottom(p, sz=4, color="999999")
        add_run(p, " ", size=Pt(13))  # height spacer for writing space


def add_answer_equation(cell, eq_func, space_before=4, space_after=2):
    """Add a red OMML equation as the answer (for answer key page)."""
    insert_display_equation(cell, eq_func, space_before=space_before, space_after=space_after)


# ============================================================================
# Header block for each column
# ============================================================================

def add_header(cell, part_letter, eq_number, is_answer_key=False):
    """Header: Name/Grade/Date fields + Part title."""
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)

    if is_answer_key:
        add_run(p, "TEACHER\u2019S ANSWER KEY", bold=True, size=FONT_SIZE_SM, color=RED)
    else:
        add_run(p, "Name: ________________________________________", size=FONT_SIZE_SM)

    p2 = cell.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(0)
    if is_answer_key:
        add_run(p2, " ", size=FONT_SIZE_SM)
    else:
        add_run(p2, "Grade & Section: ______________  Date: ___________", size=FONT_SIZE_SM)

    # Part label bar
    p3 = cell.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(4)
    p3.paragraph_format.space_after = Pt(2)
    set_paragraph_borders_all(p3, sz=8, color="000000")
    set_paragraph_shading(p3, LIGHT_GRAY_FILL)
    add_run(p3, f"PART {part_letter}: ", bold=True, size=FONT_SIZE)
    add_run(p3, f"Deriving Kinematic Equation {eq_number}", bold=True, size=FONT_SIZE)


def add_goal(cell, equation_builder):
    """GOAL line with inline equation."""
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(5)
    add_run(p, "GOAL:  ", bold=True, size=FONT_SIZE_SM)
    add_run(p, "Derive  ", size=FONT_SIZE_SM)
    insert_inline_equation(p, equation_builder)


# ============================================================================
# STUDENT WORKSHEET content builders (Page 1)
# ============================================================================

def build_part_a_student(cell):
    """Part A: Derive v = v₀ + at (student version with blanks)."""
    add_header(cell, "A", "1")
    add_goal(cell, eq_v_v0_at)

    add_instruction(cell,
        "1. Acceleration is defined as the rate of change of velocity over time. "
        "Write the defining formula for acceleration using delta notation:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "2. The change in velocity is \u0394v = v \u2212 v\u2080, and if timing starts at "
        "t = 0, then \u0394t = t. Substitute these into the definition you wrote above:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "3. Using the equation you arrived at in Step 2, multiply both sides by t "
        "to eliminate the fraction. Write the result:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "4. Now add v\u2080 to both sides of your equation to isolate v. "
        "Write the final equation:")
    add_blank_lines(cell, 2)


def build_part_b_student(cell):
    """Part B: Derive x = x₀ + ½(v₀ + v)t (student version)."""
    add_header(cell, "B", "4")
    add_goal(cell, eq_x_half_vv0_t)

    add_instruction(cell,
        "1. Average velocity is defined as total displacement over total time. "
        "Write the definition as a formula:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "2. Using the equation above, multiply both sides by t then "
        "isolate the final position x on one side. Write the result:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "3. Under constant acceleration, velocity changes linearly. The average "
        "of any linear quantity equals the mean of its start and end values. "
        "Express the average velocity in terms of v\u2080 and v:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "4. Using the position equation from Step 2, replace the average velocity with the "
        "expression you found in Step 3. Write the final equation:")
    add_blank_lines(cell, 2)


def build_part_c_student(cell):
    """Part C: Derive x = x₀ + v₀t + ½at² (student version)."""
    add_header(cell, "C", "2")
    add_goal(cell, eq_x_v0t_half_at2)

    # Step 1 - given equations
    p = add_instruction(cell,
        "1. Write down the two source equations you will combine:")
    p2 = cell.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(0)
    add_run(p2, "     Equation 1:  ", size=FONT_SIZE_SM, italic=True)
    insert_inline_equation(p2, eq_v_v0_at)
    p3 = cell.add_paragraph()
    p3.paragraph_format.space_before = Pt(1)
    p3.paragraph_format.space_after = Pt(2)
    add_run(p3, "     Equation 4:  ", size=FONT_SIZE_SM, italic=True)
    insert_inline_equation(p3, eq_x_half_vv0_t)

    add_instruction(cell,
        "2. In Equation 4, replace v with the right-hand side of Equation 1. "
        "Write the full substitution:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "3. Using the expression from Step 2, combine the like terms inside the "
        "brackets (v\u2080 + v\u2080 = 2v\u2080). Write the simplified expression:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "4. Distribute t into the bracket, then distribute \u00bd to each "
        "term. Simplify the coefficients and write the final equation:")
    add_blank_lines(cell, 2)


def build_part_d_student(cell):
    """Part D: Derive v² = v₀² + 2a(x - x₀) (student version)."""
    add_header(cell, "D", "3")
    add_goal(cell, eq_v2_final)

    add_instruction(cell,
        "1. Start with Equation 1: v = v\u2080 + at. "
        "Isolate t (subtract v\u2080, then divide by a). Write t =")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "2. Write the displacement equation: x \u2212 x\u2080 = \u00bd(v\u2080 + v)\u00b7t. "
        "Replace t with the expression from Step 1. Write the substitution:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "3. Combine into a single fraction. Apply the difference of squares: "
        "(v+v\u2080)(v\u2212v\u2080) = v\u00b2 \u2212 v\u2080\u00b2. Simplify:")
    add_blank_lines(cell, 2)

    add_instruction(cell,
        "4. Multiply both sides by 2a to clear the denominator, then add v\u2080\u00b2 "
        "to both sides. Write the final equation:")
    add_blank_lines(cell, 2)


# ============================================================================
# ANSWER KEY content builders (Page 2)
# ============================================================================

def build_part_a_answer(cell):
    """Part A answers in red."""
    add_header(cell, "A", "1", is_answer_key=True)
    add_goal(cell, eq_v_v0_at)

    add_instruction(cell, "1. Definition of acceleration:")
    add_answer_equation(cell, eq_a_def_red)

    add_instruction(cell, "2. Substitute \u0394v = v \u2212 v\u2080 and \u0394t = t:")
    add_answer_equation(cell, eq_a_expanded_red)

    add_instruction(cell, "3. Multiply both sides by t:")
    add_answer_equation(cell, eq_at_equals_red)

    add_instruction(cell, "4. Add v\u2080 to both sides:")
    add_answer_equation(cell, eq_v_v0_at_red)


def build_part_b_answer(cell):
    """Part B answers in red."""
    add_header(cell, "B", "4", is_answer_key=True)
    add_goal(cell, eq_x_half_vv0_t)

    add_instruction(cell, "1. Definition of average velocity:")
    add_answer_equation(cell, eq_vavg_def_red)

    add_instruction(cell, "2. Multiply by t, isolate x:")
    add_answer_equation(cell, eq_x_vavg_red)

    add_instruction(cell, "3. Average velocity as mean of endpoints:")
    add_answer_equation(cell, eq_vavg_mean_red)

    add_instruction(cell, "4. Substitute into position equation:")
    add_answer_equation(cell, eq_x_half_vv0_t_red)


def build_part_c_answer(cell):
    """Part C answers in red."""
    add_header(cell, "C", "2", is_answer_key=True)
    add_goal(cell, eq_x_v0t_half_at2)

    add_instruction(cell, "1. Source equations: Eq 1 & Eq 4 (given).")

    add_instruction(cell, "2. Substitute Eq 1 into Eq 4:")
    add_answer_equation(cell, eq_x_substituted_red)

    add_instruction(cell, "3. Combine like terms (v\u2080 + v\u2080 = 2v\u2080):")
    add_answer_equation(cell, eq_x_combined_red)

    add_instruction(cell, "4. Distribute t and \u00bd, simplify:")
    add_answer_equation(cell, eq_x_v0t_half_at2_red)


def build_part_d_answer(cell):
    """Part D answers in red."""
    add_header(cell, "D", "3", is_answer_key=True)
    add_goal(cell, eq_v2_final)

    add_instruction(cell, "1. Isolate t from v = v\u2080 + at:")
    add_answer_equation(cell, eq_t_from_v_red)

    add_instruction(cell, "2. Substitute t into displacement equation:")
    add_answer_equation(cell, eq_disp_substituted_red)

    add_instruction(cell, "3. Apply difference of squares:")
    add_answer_equation(cell, eq_disp_diff_squares_red)

    add_instruction(cell, "4. Multiply by 2a, add v\u2080\u00b2:")
    add_answer_equation(cell, eq_v2_final_red)


# ============================================================================
# Table/page builder utility
# ============================================================================

def create_page_table(doc, builders, is_first_page=True):
    """Create a 1-row × 4-col table filling the page for the given builders."""
    usable_twips = int((13 - 0.6) * 1440)
    col_twips = usable_twips // 4

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    disable_autofit(table)
    table.autofit = False

    # Zero cell spacing
    tblPr = table._tbl.tblPr
    tblCellSpacing = OxmlElement('w:tblCellSpacing')
    tblCellSpacing.set(qn('w:w'), '0')
    tblCellSpacing.set(qn('w:type'), 'dxa')
    tblPr.append(tblCellSpacing)

    row = table.rows[0]
    row_twips = int(8.5 * 1440) - int(0.6 * 1440)
    set_row_height(row, row_twips, exact=True)

    cells = row.cells

    for idx, cell in enumerate(cells):
        set_col_width(cell, col_twips)
        set_cell_margins(cell, top=40, bottom=30, left=60, right=60)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP

        solid = {'val': 'single', 'sz': 10, 'color': '000000'}
        dashed = {'val': 'dashed', 'sz': 8, 'color': '555555'}
        right_b = dashed if idx < 3 else solid
        set_cell_border(cell, top=solid, bottom=solid, left=solid, right=right_b)

        builders[idx](cell)

    return table


# ============================================================================
# Main
# ============================================================================

def build():
    doc = Document()

    # Default style
    style = doc.styles['Normal']
    style.font.name = FONT_NAME
    style.font.size = FONT_SIZE
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # --- PAGE 1: Student Activity Sheet ---
    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Inches(13)
    section.page_height = Inches(8.5)
    section.top_margin = Inches(0.3)
    section.bottom_margin = Inches(0.3)
    section.left_margin = Inches(0.3)
    section.right_margin = Inches(0.3)
    section.gutter = Inches(0)

    student_builders = [build_part_a_student, build_part_b_student,
                        build_part_c_student, build_part_d_student]
    create_page_table(doc, student_builders)

    # --- PAGE BREAK ---
    # Add a section break (new page) with same page setup
    doc.add_section()
    section2 = doc.sections[1]
    section2.orientation = WD_ORIENT.LANDSCAPE
    section2.page_width = Inches(13)
    section2.page_height = Inches(8.5)
    section2.top_margin = Inches(0.3)
    section2.bottom_margin = Inches(0.3)
    section2.left_margin = Inches(0.3)
    section2.right_margin = Inches(0.3)
    section2.gutter = Inches(0)

    # --- PAGE 2: Teacher's Answer Key ---
    answer_builders = [build_part_a_answer, build_part_b_answer,
                       build_part_c_answer, build_part_d_answer]
    create_page_table(doc, answer_builders)

    doc.save('/projects/sandbox/physics/kinematics_worksheet.docx')
    print("Saved kinematics_worksheet.docx (2 pages: student + answer key)")


if __name__ == '__main__':
    build()
