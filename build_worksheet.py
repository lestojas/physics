"""
Generates kinematics_worksheet.docx
Landscape, 13in x 8.5in (Legal/Long, landscape), narrow margins.
Layout: ONE ROW divided into FOUR VERTICAL COLUMNS (side by side),
each column = one independent activity sheet (Part A-D).
Monochrome / grayscale only (no colour, black text, light gray shading only).
"""

from docx import Document
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.section import WD_ORIENT
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

BLACK = RGBColor(0, 0, 0)
GRAY_FILL = "E8E8E8"   # light gray for goal box shading
LINE_FILL = "F2F2F2"   # very light gray for ruled work area

# ----------------------------------------------------------------------------
# Low level OXML helpers
# ----------------------------------------------------------------------------

def set_cell_border(cell, **kwargs):
    """
    kwargs: top, bottom, left, right -> dict(sz, val, color) or None to skip
    val: 'single', 'dashed', 'nil'
    """
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


def set_cell_shading(cell, hex_color):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    shd = OxmlElement('w:shd')
    shd.set(qn('w:val'), 'clear')
    shd.set(qn('w:color'), 'auto')
    shd.set(qn('w:fill'), hex_color)
    tcPr.append(shd)


def set_cell_margins(cell, top=40, bottom=40, left=60, right=60):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    mar = OxmlElement('w:tcMar')
    for edge, val in (('top', top), ('bottom', bottom), ('left', left), ('right', right)):
        node = OxmlElement(f'w:{edge}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        mar.append(node)
    tcPr.append(mar)


def set_paragraph_border(paragraph, sz=8, color="000000", val="single", shading=None):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    for edge in ('top', 'left', 'bottom', 'right'):
        el = OxmlElement(f'w:{edge}')
        el.set(qn('w:val'), val)
        el.set(qn('w:sz'), str(sz))
        el.set(qn('w:space'), '4')
        el.set(qn('w:color'), color)
        pBdr.append(el)
    pPr.append(pBdr)
    if shading:
        shd = OxmlElement('w:shd')
        shd.set(qn('w:val'), 'clear')
        shd.set(qn('w:color'), 'auto')
        shd.set(qn('w:fill'), shading)
        pPr.append(shd)


def set_paragraph_bottom_border_only(paragraph, sz=4, color="999999"):
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement('w:pBdr')
    el = OxmlElement('w:bottom')
    el.set(qn('w:val'), 'single')
    el.set(qn('w:sz'), str(sz))
    el.set(qn('w:space'), '1')
    el.set(qn('w:color'), color)
    pBdr.append(el)
    pPr.append(pBdr)


def set_row_height(row, height_pts, exact=True):
    trPr = row._tr.get_or_add_trPr()
    trHeight = OxmlElement('w:trHeight')
    trHeight.set(qn('w:val'), str(int(height_pts * 20)))
    trHeight.set(qn('w:hRule'), 'exact' if exact else 'atLeast')
    trPr.append(trHeight)


def set_col_width(cell, width):
    cell.width = width
    tcPr = cell._tc.get_or_add_tcPr()
    tcW = OxmlElement('w:tcW')
    tcW.set(qn('w:w'), str(int(width.twips)))
    tcW.set(qn('w:type'), 'dxa')
    tcPr.append(tcW)


def disable_autofit(table):
    tbl = table._tbl
    tblPr = tbl.tblPr
    layout = OxmlElement('w:tblLayout')
    layout.set(qn('w:type'), 'fixed')
    tblPr.append(layout)


# ----------------------------------------------------------------------------
# Text / run helpers  (subscript & superscript used to render equations
# without needing an embedded equation object -> keeps the .docx lightweight
# and universally compatible)
# ----------------------------------------------------------------------------

def add_run(paragraph, text, bold=False, italic=False, underline=False,
            size=9, sub=False, sup=False, font="Times New Roman", color=BLACK):
    r = paragraph.add_run(text)
    r.font.name = font
    r.font.size = Pt(size)
    r.bold = bold
    r.italic = italic
    r.underline = underline
    r.font.subscript = sub
    r.font.superscript = sup
    r.font.color.rgb = color
    return r


def eq(paragraph, parts, size=9.5, bold=False):
    """
    parts: list of tuples (text, kind) where kind in
           {'n','sub','sup'}  n = normal
    Example: [('v','n'), ('0','sub'), (' = v','n'), ('0','sub'), (' + at','n')]
    """
    for text, kind in parts:
        add_run(paragraph, text, size=size, bold=bold,
                sub=(kind == 'sub'), sup=(kind == 'sup'))


def blank_line(cell, pt_before=0, pt_after=2):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(pt_before)
    p.paragraph_format.space_after = Pt(pt_after)
    return p


# ----------------------------------------------------------------------------
# Content builders
# ----------------------------------------------------------------------------

def add_header_block(cell, part_letter):
    # Name line
    p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(1)
    add_run(p, "Name: ", bold=True, size=8)
    add_run(p, "\t\t\t\t\t\t\t", size=8)

    p2 = cell.add_paragraph()
    p2.paragraph_format.space_after = Pt(1)
    set_paragraph_bottom_border_only(p2, sz=4, color="000000")
    add_run(p2, " ", size=8)

    # Grade & Section / Date line
    p3 = cell.add_paragraph()
    p3.paragraph_format.space_after = Pt(1)
    p3.paragraph_format.space_before = Pt(3)
    add_run(p3, "Grade & Section: ", bold=True, size=8)

    p4 = cell.add_paragraph()
    p4.paragraph_format.space_after = Pt(1)
    set_paragraph_bottom_border_only(p4, sz=4, color="000000")
    add_run(p4, " ", size=8)

    p5 = cell.add_paragraph()
    p5.paragraph_format.space_after = Pt(1)
    p5.paragraph_format.space_before = Pt(3)
    add_run(p5, "Date: ", bold=True, size=8)

    p6 = cell.add_paragraph()
    p6.paragraph_format.space_after = Pt(4)
    set_paragraph_bottom_border_only(p6, sz=4, color="000000")
    add_run(p6, " ", size=8)

    # Part tag
    p7 = cell.add_paragraph()
    p7.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p7.paragraph_format.space_before = Pt(2)
    p7.paragraph_format.space_after = Pt(0)
    set_paragraph_border(p7, sz=10, color="000000")
    add_run(p7, f"PART {part_letter}", bold=True, size=11)

    p8 = cell.add_paragraph()
    p8.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p8.paragraph_format.space_after = Pt(6)
    add_run(p8, "Kinematics Activity Sheet", italic=True, size=7.5)


def add_title(cell, text):
    p = cell.add_paragraph()
    p.paragraph_format.space_after = Pt(3)
    set_paragraph_bottom_border_only(p, sz=6, color="555555")
    add_run(p, text.upper(), bold=True, size=9.5)


def add_goal_box(cell, label_parts):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(2)
    p.paragraph_format.space_after = Pt(6)
    set_paragraph_border(p, sz=8, color="000000", shading=GRAY_FILL)
    add_run(p, "Goal:  ", bold=True, size=8.5)
    add_run(p, "Derive the equation  ", size=8.5)
    eq(p, label_parts, size=9, bold=True)


def add_step(cell, number, title, body_parts):
    """
    body_parts: list of segments; each segment is either
        ('text', "plain sentence ")
        ('eq', [ (text,kind), ... ])   inline equation
        ('displayeq', [ (text,kind), ... ])  equation on its own centered line
    """
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(5)
    p.paragraph_format.space_after = Pt(1)
    add_run(p, f"{number}.  ", bold=True, size=9.5)
    add_run(p, title, bold=True, underline=True, size=9)

    for kind, payload in body_parts:
        if kind == 'text':
            bp = cell.add_paragraph()
            bp.paragraph_format.space_after = Pt(2)
            bp.paragraph_format.left_indent = Inches(0.14)
            add_run(bp, payload, size=8.7)
        elif kind == 'eq':
            bp = cell.add_paragraph()
            bp.paragraph_format.space_after = Pt(2)
            bp.paragraph_format.left_indent = Inches(0.14)
            eq(bp, payload, size=8.7)
        elif kind == 'displayeq':
            bp = cell.add_paragraph()
            bp.alignment = WD_ALIGN_PARAGRAPH.CENTER
            bp.paragraph_format.space_before = Pt(2)
            bp.paragraph_format.space_after = Pt(3)
            eq(bp, payload, size=10, bold=False)


def add_work_area(cell, lines=5):
    p = cell.add_paragraph()
    p.paragraph_format.space_before = Pt(6)
    p.paragraph_format.space_after = Pt(1)
    add_run(p, "Work Area", italic=True, size=7.3, color=RGBColor(0x55, 0x55, 0x55))
    for _ in range(lines):
        lp = cell.add_paragraph()
        lp.paragraph_format.space_after = Pt(9)
        set_paragraph_bottom_border_only(lp, sz=3, color="AAAAAA")
        add_run(lp, " ", size=7)


# ----------------------------------------------------------------------------
# Build document
# ----------------------------------------------------------------------------

def build():
    doc = Document()

    # default style
    style = doc.styles['Normal']
    style.font.name = 'Times New Roman'
    style.font.size = Pt(9)

    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Inches(13)
    section.page_height = Inches(8.5)
    # narrow margins
    section.top_margin = Inches(0.35)
    section.bottom_margin = Inches(0.35)
    section.left_margin = Inches(0.35)
    section.right_margin = Inches(0.35)
    section.gutter = Inches(0)

    usable_width = Inches(13 - 0.35 - 0.35)
    col_width = Inches((13 - 0.35 - 0.35) / 4)

    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    disable_autofit(table)
    table.autofit = False

    row = table.rows[0]
    set_row_height(row, height_pts=int(8.5 * 72 - 0.35 * 72 * 2 - 4), exact=False)

    cells = row.cells
    for idx, cell in enumerate(cells):
        set_col_width(cell, col_width)
        set_cell_margins(cell, top=50, bottom=50, left=70, right=70)
        cell.vertical_alignment = WD_ALIGN_VERTICAL.TOP
        # outer box border solid, but dashed on the "cut line" side (right side,
        # except last column) so the sheet can be cut into 4 vertical strips
        left_spec = {'val': 'single', 'sz': 10, 'color': '000000'}
        right_spec = {'val': 'dashed', 'sz': 8, 'color': '555555'} if idx < 3 else {'val': 'single', 'sz': 10, 'color': '000000'}
        top_spec = {'val': 'single', 'sz': 10, 'color': '000000'}
        bottom_spec = {'val': 'single', 'sz': 10, 'color': '000000'}
        set_cell_border(cell, top=top_spec, bottom=bottom_spec, left=left_spec, right=right_spec)
        # remove existing empty default paragraph text later; we just build on it
        cell.paragraphs[0].text = ""

    # Clear the automatically-created empty first paragraph in each cell before adding content
    # (python-docx tables come with one empty paragraph per cell already; we reuse cell.paragraphs[0])

    def first_p(cell):
        return cell.paragraphs[0]

    # ---------------- PART A ----------------
    cellA = cells[0]
    # replace default blank paragraph with header content by using it as the first line
    p0 = first_p(cellA)
    p0.text = ""
    add_header_block(cellA, "A")
    add_title(cellA, "Deriving Kinematic Equation 1")
    add_goal_box(cellA, [('v', 'n'), (' = v', 'n'), ('0', 'sub'), (' + at', 'n')])

    add_step(cellA, 1, "State the Definition of Acceleration", [
        ('text', "Recall that acceleration is defined as the rate of change of velocity over time. "
                 "Write the defining formula for average acceleration using delta notation:"),
        ('displayeq', [('a = ', 'n'), ('\u0394v', 'n'), (' / ', 'n'), ('\u0394t', 'n')]),
        ('text', "Identify what each symbol represents: \u0394v is the change in velocity, and "
                 "\u0394t is the elapsed time interval."),
    ])
    add_step(cellA, 2, "Expand the Delta Notation", [
        ('text', "Using the definitions from Step 1, replace \u0394v with (v \u2212 v\u2080) and "
                 "replace \u0394t with t, assuming motion starts at t = 0. Rewrite the formula "
                 "with these substitutions clearly shown:"),
        ('displayeq', [('a = (v \u2212 v', 'n'), ('0', 'sub'), (') / t', 'n')]),
    ])
    add_step(cellA, 3, "Isolate the Final Velocity", [
        ('text', "Using the equation from Step 2, eliminate the fraction by multiplying both sides "
                 "by t. Then isolate v by moving v0 to the other side. Show each algebraic step "
                 "in the work area below until you arrive at:"),
        ('displayeq', [('v = v', 'n'), ('0', 'sub'), (' + at', 'n')]),
    ])
    add_work_area(cellA, lines=4)

    # ---------------- PART B ----------------
    cellB = cells[1]
    first_p(cellB).text = ""
    add_header_block(cellB, "B")
    add_title(cellB, "Deriving Kinematic Equation 4")
    add_goal_box(cellB, [('x = x', 'n'), ('0', 'sub'), (' + \u00bd(v', 'n'), ('0', 'sub'), (' + v)t', 'n')])

    add_step(cellB, 1, "State the Definition of Average Velocity", [
        ('text', "Write the defining formula for average velocity as total displacement divided "
                 "by total elapsed time:"),
        ('displayeq', [('v', 'n'), ('avg', 'sub'), (' = (x \u2212 x', 'n'), ('0', 'sub'), (') / t', 'n')]),
        ('text', "Using this definition, multiply both sides by t and isolate the final position x "
                 "on one side."),
    ])
    add_step(cellB, 2, "Find the Average Velocity Under Constant Acceleration", [
        ('text', "Under constant acceleration, velocity changes at a uniform (linear) rate. For any "
                 "quantity that changes linearly, its average value equals the arithmetic mean of its "
                 "starting and ending values. Apply this to write:"),
        ('displayeq', [('v', 'n'), ('avg', 'sub'), (' = (v', 'n'), ('0', 'sub'), (' + v) / 2', 'n')]),
    ])
    add_step(cellB, 3, "Substitute and Simplify", [
        ('text', "Using the position equation from Step 1, replace vavg with the expression you "
                 "derived in Step 2. Substitute and simplify to obtain:"),
        ('displayeq', [('x = x', 'n'), ('0', 'sub'), (' + \u00bd(v', 'n'), ('0', 'sub'), (' + v)t', 'n')]),
    ])
    add_work_area(cellB, lines=4)

    # ---------------- PART C ----------------
    cellC = cells[2]
    first_p(cellC).text = ""
    add_header_block(cellC, "C")
    add_title(cellC, "Deriving Kinematic Equation 2")
    add_goal_box(cellC, [('x = x', 'n'), ('0', 'sub'), (' + v', 'n'), ('0', 'sub'), ('t + \u00bdat', 'n'), ('2', 'sup')])

    add_step(cellC, 1, "Identify the Two Source Equations", [
        ('text', "Write out both equations you will combine. The first gives velocity as a function "
                 "of time; the second gives position from average velocity:"),
        ('displayeq', [('v = v', 'n'), ('0', 'sub'), (' + at', 'n')]),
        ('displayeq', [('x = x', 'n'), ('0', 'sub'), (' + \u00bd(v', 'n'), ('0', 'sub'), (' + v)t', 'n')]),
    ])
    add_step(cellC, 2, "Substitute the Velocity Equation", [
        ('text', "In the position equation, locate the variable v. Replace it entirely with the "
                 "right-hand side of the velocity equation, writing the full substitution explicitly:"),
        ('displayeq', [('x = x', 'n'), ('0', 'sub'), (' + \u00bd[v', 'n'), ('0', 'sub'), (' + (v', 'n'), ('0', 'sub'), (' + at)]t', 'n')]),
    ])
    add_step(cellC, 3, "Expand and Simplify", [
        ('text', "Using the expression from Step 2, combine the like terms inside the brackets "
                 "(v0 + v0 = 2v0), distribute t into the bracket, and then distribute the factor of "
                 "\u00bd to each term. Simplify the coefficients until you reach:"),
        ('displayeq', [('x = x', 'n'), ('0', 'sub'), (' + v', 'n'), ('0', 'sub'), ('t + \u00bdat', 'n'), ('2', 'sup')]),
    ])
    add_work_area(cellC, lines=4)

    # ---------------- PART D ----------------
    cellD = cells[3]
    first_p(cellD).text = ""
    add_header_block(cellD, "D")
    add_title(cellD, "Deriving Kinematic Equation 3")
    add_goal_box(cellD, [('v', 'n'), ('2', 'sup'), (' = v', 'n'), ('0', 'sub'), ('2', 'sup'), (' + 2a(x \u2212 x', 'n'), ('0', 'sub'), (')', 'n')])

    add_step(cellD, 1, "Solve the Velocity Equation for Time", [
        ('text', "Begin with v = v0 + at. To eliminate time from the derivation, isolate t by "
                 "subtracting v0 from both sides and then dividing by a. Write the resulting "
                 "expression for t before moving to the next step."),
    ])
    add_step(cellD, 2, "Substitute into the Displacement Equation", [
        ('text', "Write the displacement-average velocity equation:"),
        ('displayeq', [('x \u2212 x', 'n'), ('0', 'sub'), (' = \u00bd(v', 'n'), ('0', 'sub'), (' + v)t', 'n')]),
        ('text', "Using the expression for t from Step 1, replace t in this equation with that "
                 "expression. Write out the substitution in full."),
    ])
    add_step(cellD, 3, "Apply the Difference of Squares", [
        ('text', "Combine the two fractions from Step 2 into a single fraction. Recognize that the "
                 "numerator follows the pattern (a+b)(a\u2212b) = a\u00b2 \u2212 b\u00b2. Apply that identity to "
                 "simplify the numerator, yielding v\u00b2 \u2212 v0\u00b2."),
    ])
    add_step(cellD, 4, "Isolate the Final Velocity Squared", [
        ('text', "Multiply both sides by 2a to clear the denominator. Then move v0\u00b2 to the "
                 "right-hand side. Show each operation explicitly until you arrive at the final form:"),
        ('displayeq', [('v', 'n'), ('2', 'sup'), (' = v', 'n'), ('0', 'sub'), ('2', 'sup'), (' + 2a(x \u2212 x', 'n'), ('0', 'sub'), (')', 'n')]),
    ])
    add_work_area(cellD, lines=3)

    doc.save('/projects/sandbox/physics/kinematics_worksheet.docx')
    print("Saved kinematics_worksheet.docx")


if __name__ == '__main__':
    build()
