"""
Generates kinematics_worksheet.docx
Layout: Landscape, 13in x 8.5in, narrow margins.
One row of FOUR VERTICAL COLUMNS (side by side).
Each column = one independent guided derivation activity (Part A–D).

Pedagogy: Instruction → blank response line → instruction → blank → ...
until the student arrives at the goal equation.
Font: Calibri, size 9pt.
Equations: OMML (Office Math Markup Language).
Monochrome grayscale only.
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement, parse_xml

BLACK = RGBColor(0, 0, 0)
GRAY = RGBColor(0x55, 0x55, 0x55)
LIGHT_GRAY_FILL = "EDEDED"

MATH_NS = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W_NS = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"

# ============================================================================
# OMML Equation builders
# ============================================================================

def omml_run(text):
    """Simple math run: m:r > m:t"""
    return f'<m:r><m:rPr><m:sty m:val="p"/></m:rPr><m:t>{text}</m:t></m:r>'

def omml_run_italic(text):
    """Italic math run (default math font style)"""
    return f'<m:r><m:t>{text}</m:t></m:r>'

def omml_frac(num, den):
    """Fraction: m:f"""
    return f'<m:f><m:num>{num}</m:num><m:den>{den}</m:den></m:f>'

def omml_sub(base, sub):
    """Subscript"""
    return f'<m:sSub><m:e>{base}</m:e><m:sub>{sub}</m:sub></m:sSub>'

def omml_sup(base, sup):
    """Superscript"""
    return f'<m:sSup><m:e>{base}</m:e><m:sup>{sup}</m:sup></m:sSup>'

def omml_subsup(base, sub, sup):
    """Subscript + superscript"""
    return f'<m:sSubSup><m:e>{base}</m:e><m:sub>{sub}</m:sub><m:sup>{sup}</m:sup></m:sSubSup>'

def omml_d(content, left="(", right=")"):
    """Delimiter (parentheses, brackets, etc.)"""
    beg = f'<m:dPr><m:begChr m:val="{left}"/><m:endChr m:val="{right}"/></m:dPr>' if left != "(" or right != ")" else ""
    return f'<m:d>{beg}<m:e>{content}</m:e></m:d>'

def omml_d_bracket(content):
    return omml_d(content, left="[", right="]")

def wrap_omath(content):
    """Wrap content in oMathPara > oMath for display (centered) equation."""
    return f'<m:oMathPara xmlns:m="{MATH_NS}"><m:oMath>{content}</m:oMath></m:oMathPara>'

def wrap_omath_inline(content):
    """Wrap content in oMath only (inline equation)."""
    return f'<m:oMath xmlns:m="{MATH_NS}">{content}</m:oMath>'


def insert_display_equation(cell, omml_content, space_before=2, space_after=2):
    """Insert a centered OMML equation paragraph into a cell."""
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    # If omml_content is a callable (function), call it
    if callable(omml_content):
        omml_content = omml_content()
    xml_str = f'<m:oMathPara xmlns:m="{MATH_NS}" xmlns:w="{W_NS}"><m:oMath>{omml_content}</m:oMath></m:oMathPara>'
    el = parse_xml(xml_str)
    p._p.append(el)
    return p


def insert_inline_equation(paragraph, omml_content):
    """Insert an inline OMML equation into an existing paragraph."""
    # If omml_content is a callable (function), call it
    if callable(omml_content):
        omml_content = omml_content()
    xml_str = f'<m:oMath xmlns:m="{MATH_NS}" xmlns:w="{W_NS}">{omml_content}</m:oMath>'
    el = parse_xml(xml_str)
    paragraph._p.append(el)


# ============================================================================
# OMML equation definitions for each kinematic equation
# ============================================================================

# v = v₀ + at
def eq_v_v0_at():
    v = omml_run_italic("v")
    eq_sign = omml_run(" = ")
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    plus = omml_run(" + ")
    at = omml_run_italic("at")
    return v + eq_sign + v0 + plus + at

# a = Δv / Δt
def eq_a_def():
    num = omml_run_italic("Δv")
    den = omml_run_italic("Δt")
    a = omml_run_italic("a")
    eq_sign = omml_run(" = ")
    return a + eq_sign + omml_frac(num, den)

# Δv = v - v₀
def eq_delta_v():
    dv = omml_run_italic("Δv")
    eq_sign = omml_run(" = ")
    v = omml_run_italic("v")
    minus = omml_run(" \u2212 ")
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    return dv + eq_sign + v + minus + v0

# Δt = t - 0 = t
def eq_delta_t():
    dt = omml_run_italic("Δt")
    eq_sign = omml_run(" = ")
    t = omml_run_italic("t")
    minus = omml_run(" \u2212 0 = ")
    return dt + eq_sign + t + minus + t

# a = (v - v₀) / t
def eq_a_expanded():
    a = omml_run_italic("a")
    eq_sign = omml_run(" = ")
    v = omml_run_italic("v")
    minus = omml_run(" \u2212 ")
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    num = v + minus + v0
    den = omml_run_italic("t")
    return a + eq_sign + omml_frac(num, den)

# x = x₀ + v_avg · t
def eq_x_vavg_t():
    x = omml_run_italic("x")
    eq_sign = omml_run(" = ")
    x0 = omml_sub(omml_run_italic("x"), omml_run("0"))
    plus = omml_run(" + ")
    vavg = omml_sub(omml_run_italic("v"), omml_run("avg"))
    dot_t = omml_run(" \u00b7 ")
    t = omml_run_italic("t")
    return x + eq_sign + x0 + plus + vavg + dot_t + t

# v_avg = (x - x₀) / t
def eq_vavg_def():
    vavg = omml_sub(omml_run_italic("v"), omml_run("avg"))
    eq_sign = omml_run(" = ")
    x = omml_run_italic("x")
    minus = omml_run(" \u2212 ")
    x0 = omml_sub(omml_run_italic("x"), omml_run("0"))
    num = x + minus + x0
    den = omml_run_italic("t")
    return vavg + eq_sign + omml_frac(num, den)

# v_avg = (v₀ + v) / 2
def eq_vavg_mean():
    vavg = omml_sub(omml_run_italic("v"), omml_run("avg"))
    eq_sign = omml_run(" = ")
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    plus = omml_run(" + ")
    v = omml_run_italic("v")
    num = v0 + plus + v
    den = omml_run("2")
    return vavg + eq_sign + omml_frac(num, den)

# x = x₀ + ½(v₀ + v)t
def eq_x_half_vv0_t():
    x = omml_run_italic("x")
    eq_sign = omml_run(" = ")
    x0 = omml_sub(omml_run_italic("x"), omml_run("0"))
    plus = omml_run(" + ")
    half = omml_frac(omml_run("1"), omml_run("2"))
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    plus2 = omml_run(" + ")
    v = omml_run_italic("v")
    inner = v0 + plus2 + v
    paren = omml_d(inner)
    t = omml_run_italic("t")
    return x + eq_sign + x0 + plus + half + paren + t

# x = x₀ + ½[v₀ + (v₀ + at)]t
def eq_x_substituted():
    x = omml_run_italic("x")
    eq_sign = omml_run(" = ")
    x0 = omml_sub(omml_run_italic("x"), omml_run("0"))
    plus = omml_run(" + ")
    half = omml_frac(omml_run("1"), omml_run("2"))
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    plus2 = omml_run(" + ")
    v0_2 = omml_sub(omml_run_italic("v"), omml_run("0"))
    plus3 = omml_run(" + ")
    at = omml_run_italic("at")
    inner_paren = omml_d(v0_2 + plus3 + at)
    bracket_content = v0 + plus2 + inner_paren
    bracket = omml_d_bracket(bracket_content)
    t = omml_run_italic("t")
    return x + eq_sign + x0 + plus + half + bracket + t

# x = x₀ + v₀t + ½at²
def eq_x_v0t_half_at2():
    x = omml_run_italic("x")
    eq_sign = omml_run(" = ")
    x0 = omml_sub(omml_run_italic("x"), omml_run("0"))
    plus = omml_run(" + ")
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    t = omml_run_italic("t")
    plus2 = omml_run(" + ")
    half = omml_frac(omml_run("1"), omml_run("2"))
    a = omml_run_italic("a")
    t2 = omml_sup(omml_run_italic("t"), omml_run("2"))
    return x + eq_sign + x0 + plus + v0 + t + plus2 + half + a + t2

# t = (v - v₀) / a
def eq_t_from_v():
    t = omml_run_italic("t")
    eq_sign = omml_run(" = ")
    v = omml_run_italic("v")
    minus = omml_run(" \u2212 ")
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    num = v + minus + v0
    den = omml_run_italic("a")
    return t + eq_sign + omml_frac(num, den)

# x - x₀ = ½(v₀ + v) · (v - v₀)/a
def eq_displacement_substituted():
    x = omml_run_italic("x")
    minus = omml_run(" \u2212 ")
    x0 = omml_sub(omml_run_italic("x"), omml_run("0"))
    eq_sign = omml_run(" = ")
    half = omml_frac(omml_run("1"), omml_run("2"))
    v0 = omml_sub(omml_run_italic("v"), omml_run("0"))
    plus = omml_run(" + ")
    v = omml_run_italic("v")
    paren = omml_d(v0 + plus + v)
    dot = omml_run(" \u00b7 ")
    v2 = omml_run_italic("v")
    minus2 = omml_run(" \u2212 ")
    v0_2 = omml_sub(omml_run_italic("v"), omml_run("0"))
    frac_part = omml_frac(v2 + minus2 + v0_2, omml_run_italic("a"))
    return x + minus + x0 + eq_sign + half + paren + dot + frac_part

# v² = v₀² + 2a(x - x₀)
def eq_v2_final():
    v2 = omml_sup(omml_run_italic("v"), omml_run("2"))
    eq_sign = omml_run(" = ")
    v0_2 = omml_subsup(omml_run_italic("v"), omml_run("0"), omml_run("2"))
    plus = omml_run(" + 2")
    a = omml_run_italic("a")
    x = omml_run_italic("x")
    minus = omml_run(" \u2212 ")
    x0 = omml_sub(omml_run_italic("x"), omml_run("0"))
    paren = omml_d(x + minus + x0)
    return v2 + eq_sign + v0_2 + plus + a + paren


# ============================================================================
# Low level OXML helpers for table/cell formatting
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


def add_instruction(cell, text, space_before=3, space_after=0):
    """Add an instruction paragraph."""
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    add_run(p, text, size=FONT_SIZE)
    return p


def add_blank_line(cell, count=1, space_before=2, space_after=1):
    """Add blank response line(s) with bottom border for student to write on."""
    for _ in range(count):
        p = cell.add_paragraph()
        p.paragraph_format.space_before = Pt(space_before)
        p.paragraph_format.space_after = Pt(space_after)
        set_paragraph_border_bottom(p, sz=4, color="999999")
        add_run(p, " ", size=Pt(11))  # height spacer
    return p


def add_blank_lines(cell, count=2):
    """Add multiple blank lines for a multi-line response."""
    for i in range(count):
        add_blank_line(cell, space_before=1 if i > 0 else 3, space_after=0)


# ============================================================================
# Header block for each column
# ============================================================================

def add_header(cell, part_letter, eq_number):
    # Name line
    p = cell.paragraphs[0]  # reuse default empty paragraph
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    add_run(p, "Name: ___________________________________", size=FONT_SIZE_SM)

    # Grade & Section + Date
    p2 = cell.add_paragraph()
    p2.paragraph_format.space_before = Pt(2)
    p2.paragraph_format.space_after = Pt(0)
    add_run(p2, "Grade & Section: _____________  Date: __________", size=FONT_SIZE_SM)

    # Part label
    p3 = cell.add_paragraph()
    p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p3.paragraph_format.space_before = Pt(5)
    p3.paragraph_format.space_after = Pt(1)
    set_paragraph_borders_all(p3, sz=8, color="000000")
    set_paragraph_shading(p3, LIGHT_GRAY_FILL)
    add_run(p3, f"PART {part_letter}: ", bold=True, size=FONT_SIZE)
    add_run(p3, f"Deriving Kinematic Equation {eq_number}", bold=True, size=FONT_SIZE)


def add_goal(cell, equation_builder):
    """Add the goal box with the target equation."""
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(4)
    p.paragraph_format.space_after = Pt(4)
    add_run(p, "GOAL: Derive  ", bold=True, size=FONT_SIZE_SM)
    insert_inline_equation(p, equation_builder())


# ============================================================================
# Content for each Part
# ============================================================================

def build_part_a(cell):
    """Part A: Derive v = v₀ + at"""
    add_header(cell, "A", "1")
    add_goal(cell, eq_v_v0_at)

    # Step 1
    add_instruction(cell, "1. Acceleration is defined as the rate of change of velocity over time. "
                          "Write the general definition of acceleration using delta notation (a = ?):")
    add_blank_lines(cell, 1)

    # Step 2
    add_instruction(cell, "2. The change in velocity is Δv = v \u2212 v\u2080, and if timing starts at "
                          "t = 0, then Δt = t. Substitute these into the definition you wrote above:")
    add_blank_lines(cell, 1)

    # Step 3
    add_instruction(cell, "3. Using the equation you arrived at, multiply both sides by t "
                          "to eliminate the fraction. Write the result:")
    add_blank_lines(cell, 1)

    # Step 4
    add_instruction(cell, "4. Now add v\u2080 to both sides of your equation to isolate v. "
                          "Write the final equation:")
    add_blank_lines(cell, 1)

    # Final
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    set_paragraph_borders_all(p, sz=6, color="000000")
    add_run(p, " \u2713  Final Equation 1:  ", bold=True, size=FONT_SIZE_SM)
    insert_inline_equation(p, eq_v_v0_at)


def build_part_b(cell):
    """Part B: Derive x = x₀ + ½(v₀ + v)t"""
    add_header(cell, "B", "4")
    add_goal(cell, eq_x_half_vv0_t)

    # Step 1
    add_instruction(cell, "1. Average velocity is defined as total displacement over total time. "
                          "Write this definition as a formula (v_avg = ?):")
    add_blank_lines(cell, 1)

    # Step 2
    add_instruction(cell, "2. Using the equation above, multiply both sides by t and then "
                          "isolate the final position x on one side. Write the result:")
    add_blank_lines(cell, 1)

    # Step 3
    add_instruction(cell, "3. Under constant acceleration, velocity changes linearly. The average "
                          "of any linear quantity is simply the mean of its start and end values. "
                          "Write v_avg in terms of v\u2080 and v:")
    add_blank_lines(cell, 1)

    # Step 4
    add_instruction(cell, "4. Using the position equation from Step 2, replace v_avg with the "
                          "expression you found in Step 3. Write the final equation:")
    add_blank_lines(cell, 1)

    # Final
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    set_paragraph_borders_all(p, sz=6, color="000000")
    add_run(p, " \u2713  Final Equation 4:  ", bold=True, size=FONT_SIZE_SM)
    insert_inline_equation(p, eq_x_half_vv0_t)


def build_part_c(cell):
    """Part C: Derive x = x₀ + v₀t + ½at²"""
    add_header(cell, "C", "2")
    add_goal(cell, eq_x_v0t_half_at2)

    # Step 1
    add_instruction(cell, "1. Write down the two source equations you will combine:\n"
                          "    Equation 1 (velocity):  v = v\u2080 + at\n"
                          "    Equation 4 (position):  x = x\u2080 + \u00bd(v\u2080 + v)t")

    # Step 2
    add_instruction(cell, "2. In Equation 4, locate the variable v. Replace it entirely with "
                          "the right-hand side of Equation 1 (v\u2080 + at). Write the substitution:")
    add_blank_lines(cell, 1)

    # Step 3
    add_instruction(cell, "3. Inside the brackets, combine the two v\u2080 terms "
                          "(v\u2080 + v\u2080 = 2v\u2080). Write the simplified expression:")
    add_blank_lines(cell, 1)

    # Step 4
    add_instruction(cell, "4. Distribute t into the bracket, then distribute the \u00bd to each "
                          "term. Simplify the coefficients. Write the final equation:")
    add_blank_lines(cell, 1)

    # Final
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    set_paragraph_borders_all(p, sz=6, color="000000")
    add_run(p, " \u2713  Final Equation 2:  ", bold=True, size=FONT_SIZE_SM)
    insert_inline_equation(p, eq_x_v0t_half_at2)


def build_part_d(cell):
    """Part D: Derive v² = v₀² + 2a(x − x₀)"""
    add_header(cell, "D", "3")
    add_goal(cell, eq_v2_final)

    # Step 1
    add_instruction(cell, "1. Start with Equation 1: v = v\u2080 + at. "
                          "Isolate t by first subtracting v\u2080, then dividing by a. Write t = :")
    add_blank_lines(cell, 1)

    # Step 2
    add_instruction(cell, "2. Write the displacement equation: x \u2212 x\u2080 = \u00bd(v\u2080 + v)\u00b7t. "
                          "Using the expression for t from Step 1, substitute it into this equation:")
    add_blank_lines(cell, 1)

    # Step 3
    add_instruction(cell, "3. Combine the fractions into one. Recognize that the numerator "
                          "(v + v\u2080)(v \u2212 v\u2080) follows the difference of squares pattern: "
                          "(a+b)(a\u2212b) = a\u00b2 \u2212 b\u00b2. Simplify the numerator:")
    add_blank_lines(cell, 1)

    # Step 4
    add_instruction(cell, "4. Multiply both sides by 2a to clear the denominator. "
                          "Then add v\u2080\u00b2 to both sides. Write the final equation:")
    add_blank_lines(cell, 1)

    # Final
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(2)
    set_paragraph_borders_all(p, sz=6, color="000000")
    add_run(p, " \u2713  Final Equation 3:  ", bold=True, size=FONT_SIZE_SM)
    insert_inline_equation(p, eq_v2_final)


# ============================================================================
# Main build function
# ============================================================================

def build():
    doc = Document()

    # Default style → Calibri 9pt
    style = doc.styles['Normal']
    style.font.name = FONT_NAME
    style.font.size = FONT_SIZE
    style.paragraph_format.space_before = Pt(0)
    style.paragraph_format.space_after = Pt(0)
    style.paragraph_format.line_spacing = 1.0

    # Page setup: landscape 13in × 8.5in, narrow margins
    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Inches(13)
    section.page_height = Inches(8.5)
    section.top_margin = Inches(0.3)
    section.bottom_margin = Inches(0.3)
    section.left_margin = Inches(0.3)
    section.right_margin = Inches(0.3)
    section.gutter = Inches(0)

    # Usable width in twips (1 inch = 1440 twips)
    usable_twips = int((13 - 0.6) * 1440)  # 12.4 inches
    col_twips = usable_twips // 4

    # Create table: 1 row, 4 cols
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    disable_autofit(table)
    table.autofit = False

    # Remove table spacing/padding at table level
    tblPr = table._tbl.tblPr
    tblCellSpacing = OxmlElement('w:tblCellSpacing')
    tblCellSpacing.set(qn('w:w'), '0')
    tblCellSpacing.set(qn('w:type'), 'dxa')
    tblPr.append(tblCellSpacing)

    row = table.rows[0]
    # Set row height to fill the page
    page_height_twips = int(8.5 * 1440)
    margins_twips = int(0.6 * 1440)
    row_twips = page_height_twips - margins_twips
    set_row_height(row, row_twips, exact=True)

    cells = row.cells
    builders = [build_part_a, build_part_b, build_part_c, build_part_d]

    for idx, cell in enumerate(cells):
        set_col_width(cell, col_twips)
        set_cell_margins(cell, top=40, bottom=30, left=60, right=60)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP

        # Borders: solid outer, dashed between columns (cut lines)
        solid = {'val': 'single', 'sz': 10, 'color': '000000'}
        dashed = {'val': 'dashed', 'sz': 8, 'color': '555555'}
        left_b = solid
        right_b = dashed if idx < 3 else solid
        set_cell_border(cell, top=solid, bottom=solid, left=left_b, right=right_b)

        # Build content
        builders[idx](cell)

    # Remove trailing empty paragraph that Word adds
    body = doc._body._body
    last_p = body.findall(qn('w:p'))
    if last_p:
        # Remove the extra paragraph after the table if it exists
        after_tbl = body.findall(qn('w:p'))
        for extra_p in after_tbl:
            if body.index(extra_p) > body.index(table._tbl):
                pPr = extra_p.get_or_add_pPr() if hasattr(extra_p, 'get_or_add_pPr') else None
                # Just minimize it
                pass

    doc.save('/projects/sandbox/physics/kinematics_worksheet.docx')
    print("Saved kinematics_worksheet.docx")


if __name__ == '__main__':
    build()
