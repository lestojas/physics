"""
Generate ProblemSet3-SolutionKey.docx with proper formatting.
Key formatting feature: aligned equal signs in derivation/substitution steps
using 4-column tables with invisible borders.
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, Emu, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml
import copy


def set_cell_border(cell, **kwargs):
    """Set cell border properties."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'  <w:top w:val="nil"/>'
        f'  <w:left w:val="nil"/>'
        f'  <w:bottom w:val="nil"/>'
        f'  <w:right w:val="nil"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)


def remove_table_borders(table):
    """Remove all borders from a table."""
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="nil"/>'
        f'  <w:left w:val="nil"/>'
        f'  <w:bottom w:val="nil"/>'
        f'  <w:right w:val="nil"/>'
        f'  <w:insideH w:val="nil"/>'
        f'  <w:insideV w:val="nil"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)
    if tbl.tblPr is None:
        tbl.append(tblPr)
    for row in table.rows:
        for cell in row.cells:
            set_cell_border(cell)


def set_cell_width(cell, width):
    """Set exact cell width."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcW = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{width}" w:type="dxa"/>')
    tcPr.append(tcW)


def set_cell_margins(cell, top=0, bottom=0, start=0, end=0):
    """Set cell margins (in twips)."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'  <w:top w:w="{top}" w:type="dxa"/>'
        f'  <w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'  <w:start w:w="{start}" w:type="dxa"/>'
        f'  <w:end w:w="{end}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def set_paragraph_spacing(paragraph, before=0, after=0, line=240):
    """Set paragraph spacing."""
    pPr = paragraph._p.get_or_add_pPr()
    spacing = parse_xml(
        f'<w:spacing {nsdecls("w")} w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
    )
    pPr.append(spacing)


def add_run(paragraph, text, bold=False, italic=False, size=Pt(11), font_name='Calibri'):
    """Add a run with specified formatting."""
    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = size
    run.font.name = font_name
    return run


def add_heading_custom(doc, text, level=1):
    """Add a heading paragraph."""
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=240, after=120)
    run = p.add_run(text)
    run.bold = True
    if level == 1:
        run.font.size = Pt(16)
    elif level == 2:
        run.font.size = Pt(13)
    elif level == 3:
        run.font.size = Pt(11)
    run.font.name = 'Calibri'
    return p


def add_problem_heading(doc, text):
    """Add a problem heading (Problem 1, Problem 2, etc.)."""
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=360, after=120)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(14)
    run.font.name = 'Calibri'
    return p


def add_problem_text(doc, text, indent=Cm(1)):
    """Add problem statement text (indented)."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = indent
    set_paragraph_spacing(p, before=60, after=60)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    return p


def add_section_label(doc, text):
    """Add a section label (Given, Required, Solution)."""
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=200, after=80)
    run = p.add_run(text)
    run.bold = True
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    return p


def add_bullet(doc, text, indent=Cm(1)):
    """Add a bullet point."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = indent
    p.paragraph_format.first_line_indent = Cm(-0.5)
    set_paragraph_spacing(p, before=20, after=20)
    run = p.add_run('\u2022  ' + text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    return p


def add_normal_para(doc, text, indent=None, bold=False, italic=False):
    """Add a normal paragraph."""
    p = doc.add_paragraph()
    if indent:
        p.paragraph_format.left_indent = indent
    set_paragraph_spacing(p, before=60, after=60)
    run = p.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    return p


def add_equation_line(doc, text, indent=Cm(1)):
    """Add a standalone equation line."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = indent
    set_paragraph_spacing(p, before=60, after=60)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    run.italic = True
    return p


def add_aligned_table(doc, rows, col_widths=None, indent=Cm(1)):
    """
    Add a borderless table with aligned equal signs.
    Each row is a list of strings for each column.
    Typically 4 columns: [left_side, '=', right_side, annotation]
    """
    if not rows:
        return
    num_cols = max(len(r) for r in rows)
    table = doc.add_table(rows=len(rows), cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    remove_table_borders(table)

    # Default column widths (in twips: 1 inch = 1440 twips)
    if col_widths is None:
        col_widths = [2200, 360, 3200, 3600]  # LHS, =, RHS, annotation

    for i, row_data in enumerate(rows):
        row = table.rows[i]
        for j in range(num_cols):
            cell = row.cells[j]
            set_cell_width(cell, col_widths[j] if j < len(col_widths) else 2000)
            set_cell_margins(cell, top=20, bottom=20, start=72, end=72)
            # Clear default paragraph and add content
            p = cell.paragraphs[0]
            set_paragraph_spacing(p, before=0, after=0, line=260)
            text = row_data[j] if j < len(row_data) else ''
            run = p.add_run(text)
            run.font.size = Pt(11)
            run.font.name = 'Calibri'
            if j == num_cols - 1 and text:  # annotation column
                run.italic = True
                run.font.color.rgb = RGBColor(80, 80, 80)

    # Set table indent
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblInd = parse_xml(f'<w:tblInd {nsdecls("w")} w:w="720" w:type="dxa"/>')
    tblPr.append(tblInd)

    return table


def add_given_table(doc, rows):
    """
    Add a Given table with columns: Symbol, Value, Annotation.
    Each row is [symbol, value, annotation].
    """
    num_cols = 3
    table = doc.add_table(rows=len(rows) + 1, cols=num_cols)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    remove_table_borders(table)

    col_widths = [1440, 2160, 5400]
    headers = ['Symbol', 'Value', 'Annotation']

    # Header row
    for j, header in enumerate(headers):
        cell = table.rows[0].cells[j]
        set_cell_width(cell, col_widths[j])
        set_cell_margins(cell, top=40, bottom=40, start=72, end=72)
        p = cell.paragraphs[0]
        set_paragraph_spacing(p, before=0, after=0)
        run = p.add_run(header)
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Calibri'

    # Data rows
    for i, row_data in enumerate(rows):
        for j in range(num_cols):
            cell = table.rows[i + 1].cells[j]
            set_cell_width(cell, col_widths[j])
            set_cell_margins(cell, top=20, bottom=20, start=72, end=72)
            p = cell.paragraphs[0]
            set_paragraph_spacing(p, before=0, after=0)
            text = row_data[j] if j < len(row_data) else ''
            run = p.add_run(text)
            run.font.size = Pt(11)
            run.font.name = 'Calibri'
            if j == 2:  # annotation
                run.italic = True

    # Table indent
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblInd = parse_xml(f'<w:tblInd {nsdecls("w")} w:w="720" w:type="dxa"/>')
    tblPr.append(tblInd)

    return table


def build_document():
    doc = Document()

    # Set default font
    style = doc.styles['Normal']
    font = style.font
    font.name = 'Calibri'
    font.size = Pt(11)

    # Set margins
    for section in doc.sections:
        section.top_margin = Cm(2.54)
        section.bottom_margin = Cm(2.54)
        section.left_margin = Cm(2.54)
        section.right_margin = Cm(2.54)

    # =========================================================================
    # PROBLEM 1
    # =========================================================================
    add_problem_heading(doc, 'Problem 1')
    add_problem_text(doc,
        'In the fastest measured tennis serve, the ball left the racquet at 73.14 m/s. '
        'A served tennis ball is typically in contact with the racquet for 30.0 ms and starts from rest. '
        'Assume constant acceleration. (a) What was the ball\u2019s acceleration during this serve? '
        '(b) How far did the ball travel during the serve?'
    )

    # Given
    add_section_label(doc, 'Given')
    add_bullet(doc, 'v\u2080 = 0 m/s \u2014 "Starts from rest" means initial velocity is zero')
    add_bullet(doc, 'v = 73.14 m/s \u2014 Final speed as it leaves the racquet')
    add_bullet(doc, 't = 30.0 ms = 0.0300 s \u2014 Convert ms \u2192 s by dividing by 1000, since equations need SI units')

    # Required
    add_section_label(doc, 'Required')
    add_normal_para(doc, '(a)  a = ?', indent=Cm(1))
    add_normal_para(doc, '(b)  (x \u2212 x\u2080) = ?   (distance traveled)', indent=Cm(1))

    # Solution (a)
    add_section_label(doc, 'Solution')
    add_normal_para(doc, '(a) Finding acceleration', indent=Cm(0.5), bold=True)
    add_normal_para(doc, 'Which equation?  We are given v\u2080, v, and t. We are not given \u2014 and don\u2019t need \u2014 displacement (x \u2212 x\u2080). Hence, Eq. 1 is our match.', indent=Cm(1))
    add_equation_line(doc, 'v = v\u2080 + at')

    add_normal_para(doc, 'Isolate a:', indent=Cm(1))
    add_aligned_table(doc, [
        ['v', '=', 'v\u2080 + at', ''],
        ['v \u2212 v\u2080', '=', 'at', ''],
        ['(v \u2212 v\u2080) / t', '=', 'a', ''],
        ['a', '=', '(v \u2212 v\u2080) / t', ''],
    ])

    add_normal_para(doc, 'Substitute values:', indent=Cm(1))
    add_aligned_table(doc, [
        ['a', '=', '(73.14 \u2212 0) / 0.0300', ''],
        ['a', '=', '2.44 \u00d7 10\u00b3 m/s\u00b2', ''],
    ])

    add_normal_para(doc, 'This is roughly 249 times the acceleration due to gravity (g = 9.8 m/s\u00b2) \u2014 that\u2019s how violent a tennis serve impact really is!', indent=Cm(1), italic=True)

    # Solution (b)
    add_normal_para(doc, '(b) Finding distance traveled', indent=Cm(0.5), bold=True)
    add_normal_para(doc, 'Which equation?  We now know v\u2080, v, t, and a from part (a). We could use Eq. 2, but since a was a rounded answer, reusing it could introduce rounding error. It is safer to use the equation that doesn\u2019t need acceleration at all \u2014 Eq. 4, which is missing a.', indent=Cm(1))
    add_equation_line(doc, '(x \u2212 x\u2080) = \u00bd(v\u2080 + v)t')

    add_normal_para(doc, 'Derivation by transposition \u2014 isolate (x \u2212 x\u2080), the distance traveled:', indent=Cm(1))
    add_aligned_table(doc, [
        ['(x \u2212 x\u2080)', '=', '\u00bd(v\u2080 + v)t', ''],
        ['(x \u2212 x\u2080)', '=', '\u00bd(v\u2080 + v)t', 'transpose x\u2080: added on the right, becomes subtracted on the left'],
    ])

    add_normal_para(doc, 'Substitute values:', indent=Cm(1))
    add_aligned_table(doc, [
        ['(x \u2212 x\u2080)', '=', '\u00bd(0 + 73.14)(0.0300)', ''],
        ['(x \u2212 x\u2080)', '=', '1.10 m', ''],
    ])

    # =========================================================================
    # PROBLEM 2
    # =========================================================================
    add_problem_heading(doc, 'Problem 2')
    add_problem_text(doc,
        'The fastest measured pitched baseball left the pitcher\u2019s hand at a speed of 45.0 m/s. '
        'If the pitcher was in contact with the ball over a distance of 1.50 m and produced constant acceleration, '
        '(a) what acceleration did he give the ball, and (b) how much time did it take him to pitch it?'
    )

    # Given
    add_section_label(doc, 'Given')
    add_given_table(doc, [
        ['v\u2080', '0 m/s', 'Ball starts at rest in the pitcher\u2019s hand before the throwing motion begins'],
        ['v', '45.0 m/s', 'Speed as the ball leaves the hand'],
        ['(x \u2212 x\u2080)', '1.50 m', 'Distance over which the hand accelerates the ball'],
    ])

    # Required
    add_section_label(doc, 'Required')
    add_normal_para(doc, '(a)  a = ?', indent=Cm(1))
    add_normal_para(doc, '(b)  t = ?', indent=Cm(1))

    # Solution (a)
    add_section_label(doc, 'Solution')
    add_normal_para(doc, '(a) Finding acceleration', indent=Cm(0.5), bold=True)
    add_normal_para(doc, 'Which equation?  We are given v\u2080, v, and (x \u2212 x\u2080). We are not given, and do not yet need, time t. Eq. 3 is the one missing t, so that\u2019s our match.', indent=Cm(1))
    add_equation_line(doc, 'v\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)')

    add_normal_para(doc, 'Derivation by transposition \u2014 isolate a:', indent=Cm(1))
    add_aligned_table(doc, [
        ['v\u00b2', '=', 'v\u2080\u00b2 + 2a(x \u2212 x\u2080)', ''],
        ['v\u00b2 \u2212 v\u2080\u00b2', '=', '2a(x \u2212 x\u2080)', 'transpose v\u2080\u00b2: added on the right, becomes subtracted on the left'],
        ['(v\u00b2 \u2212 v\u2080\u00b2) / 2(x \u2212 x\u2080)', '=', 'a', 'transpose 2(x \u2212 x\u2080): multiplying a, becomes a divisor'],
        ['a', '=', '(v\u00b2 \u2212 v\u2080\u00b2) / 2(x \u2212 x\u2080)', ''],
    ])

    add_normal_para(doc, 'Substitute values:', indent=Cm(1))
    add_aligned_table(doc, [
        ['a', '=', '(45.0\u00b2 \u2212 0\u00b2) / 2(1.50)', 'm\u00b2/s\u00b2 \u00f7 m'],
        ['a', '=', '2025 / 3.00', ''],
        ['a', '=', '675 m/s\u00b2', ''],
    ])

    # Solution (b)
    add_normal_para(doc, '(b) Finding time', indent=Cm(0.5), bold=True)
    add_normal_para(doc, 'Which equation?  We now know v\u2080, v, (x \u2212 x\u2080), and a (rounded). To avoid propagating rounding error from part (a), use the equation that doesn\u2019t need a \u2014 Eq. 4, missing acceleration.', indent=Cm(1))
    add_equation_line(doc, '(x \u2212 x\u2080) = \u00bd(v\u2080 + v)t')

    add_normal_para(doc, 'Derivation by transposition \u2014 isolate t:', indent=Cm(1))
    add_aligned_table(doc, [
        ['(x \u2212 x\u2080)', '=', '\u00bd(v\u2080 + v)t', 'transpose x\u2080 (as in Problem 1)'],
        ['2(x \u2212 x\u2080)', '=', '(v\u2080 + v)t', 'transpose \u00bd: multiply both sides by 2 to clear the fraction'],
        ['2(x \u2212 x\u2080) / (v\u2080 + v)', '=', 't', 'transpose (v\u2080 + v): multiplying t, becomes a divisor'],
        ['t', '=', '2(x \u2212 x\u2080) / (v\u2080 + v)', ''],
    ])

    add_normal_para(doc, 'Substitute values:', indent=Cm(1))
    add_aligned_table(doc, [
        ['t', '=', '2(1.50) / (0 + 45.0)', 'm \u00f7 (m/s)'],
        ['t', '=', '3.00 / 45.0', ''],
        ['t', '=', '0.0667 s  (66.7 ms)', ''],
    ])

    # =========================================================================
    # PROBLEM 3
    # =========================================================================
    add_problem_heading(doc, 'Problem 3')
    add_problem_text(doc,
        'The human body can survive an acceleration trauma incident if the magnitude of the acceleration '
        'is less than 250 m/s\u00b2. If you are in an automobile accident with an initial speed of 105 km/h '
        'and are stopped by an airbag, over what minimum distance must the airbag stop you to survive?'
    )

    # Given
    add_section_label(doc, 'Given')
    add_given_table(doc, [
        ['v\u2080', '105 km/h', 'Must convert to m/s (SI unit) before using the equations'],
        ['v', '0 m/s', 'The car (and you) come to a complete stop'],
        ['a', '\u2212250 m/s\u00b2', 'Use the maximum allowed magnitude of deceleration \u2014 this gives the minimum possible stopping distance. The negative sign shows it is a deceleration, opposite to the direction of motion.'],
    ])

    add_normal_para(doc, 'Unit conversion:', indent=Cm(1))
    add_normal_para(doc, 'v\u2080 = 105 km/h \u00d7 (1000 m / 1 km) \u00d7 (1 h / 3600 s) = 29.17 m/s', indent=Cm(1))

    # Required
    add_section_label(doc, 'Required')
    add_normal_para(doc, '(x \u2212 x\u2080) = ?   (minimum stopping distance)', indent=Cm(1))

    # Solution
    add_section_label(doc, 'Solution')
    add_normal_para(doc, 'Which equation?  We are given v\u2080, v, and a. We are not given, and don\u2019t need, time t. Eq. 3 is missing t, so that\u2019s our match.', indent=Cm(1))
    add_equation_line(doc, 'v\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)')

    add_normal_para(doc, 'Derivation by transposition \u2014 isolate (x \u2212 x\u2080):', indent=Cm(1))
    add_aligned_table(doc, [
        ['v\u00b2', '=', 'v\u2080\u00b2 + 2a(x \u2212 x\u2080)', ''],
        ['v\u00b2 \u2212 v\u2080\u00b2', '=', '2a(x \u2212 x\u2080)', 'transpose v\u2080\u00b2: added on the right, becomes subtracted on the left'],
        ['(v\u00b2 \u2212 v\u2080\u00b2) / 2a', '=', '(x \u2212 x\u2080)', 'transpose 2a: multiplying, becomes a divisor'],
        ['(x \u2212 x\u2080)', '=', '(v\u00b2 \u2212 v\u2080\u00b2) / 2a', ''],
    ])

    add_normal_para(doc, 'Substitute values:', indent=Cm(1))
    add_aligned_table(doc, [
        ['(x \u2212 x\u2080)', '=', '(0\u00b2 \u2212 29.17\u00b2) / 2(\u2212250)', 'm\u00b2/s\u00b2 \u00f7 m/s\u00b2'],
        ['(x \u2212 x\u2080)', '=', '(\u2212850.9) / (\u2212500)', ''],
        ['(x \u2212 x\u2080)', '=', '1.70 m', ''],
    ])

    add_normal_para(doc, 'The negative signs on top and bottom cancel \u2014 that makes sense, since a distance must be positive! The airbag (plus crumple zone) must stop you within at least 1.70 m, or the deceleration will exceed the survivable limit of 250 m/s\u00b2.', indent=Cm(1), italic=True)

    # =========================================================================
    # PROBLEM 4
    # =========================================================================
    add_problem_heading(doc, 'Problem 4')
    add_problem_text(doc,
        'A small block has constant acceleration as it slides down a frictionless incline, released from rest. '
        'Its speed after traveling 6.80 m is 3.80 m/s. What is its speed after traveling only 3.40 m (halfway down)?'
    )
    add_normal_para(doc, 'Strategy.  This problem needs two stages. First, use the full trip (0 to 6.80 m) to find the constant acceleration a. Then apply that same a to the shorter trip (0 to 3.40 m) to find the speed at that point.', indent=Cm(1), italic=True)

    # Given
    add_section_label(doc, 'Given')
    add_given_table(doc, [
        ['v\u2080', '0 m/s', 'Released from rest at the top'],
        ['(x \u2212 x\u2080)\u2081', '6.80 m', 'Full distance to the bottom'],
        ['v\u2081', '3.80 m/s', 'Speed at the bottom (end of the full distance)'],
        ['(x \u2212 x\u2080)\u2082', '3.40 m', 'The shorter distance we care about (exactly half of 6.80 m)'],
    ])

    # Required
    add_section_label(doc, 'Required')
    add_normal_para(doc, 'v\u2082 = ?   \u2014 the speed when the block has traveled 3.40 m', indent=Cm(1))

    # Solution - Stage 1
    add_section_label(doc, 'Solution')
    add_normal_para(doc, 'Stage 1 \u2014 find the acceleration using the full 6.80 m trip', indent=Cm(0.5), bold=True)
    add_normal_para(doc, 'Which equation?  We know v\u2080, v\u2081, and (x \u2212 x\u2080)\u2081. We don\u2019t have or need t. Eq. 3 is missing t.', indent=Cm(1))
    add_equation_line(doc, 'v\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)')

    add_normal_para(doc, 'Derivation by transposition \u2014 isolate a:', indent=Cm(1))
    add_aligned_table(doc, [
        ['v\u2081\u00b2', '=', 'v\u2080\u00b2 + 2a(x \u2212 x\u2080)\u2081', ''],
        ['v\u2081\u00b2 \u2212 v\u2080\u00b2', '=', '2a(x \u2212 x\u2080)\u2081', 'transpose v\u2080\u00b2'],
        ['(v\u2081\u00b2 \u2212 v\u2080\u00b2) / 2(x \u2212 x\u2080)\u2081', '=', 'a', 'transpose 2(x \u2212 x\u2080)\u2081: multiplying, becomes a divisor'],
        ['a', '=', '(v\u2081\u00b2 \u2212 v\u2080\u00b2) / 2(x \u2212 x\u2080)\u2081', ''],
    ])

    add_normal_para(doc, 'Substitute values:', indent=Cm(1))
    add_aligned_table(doc, [
        ['a', '=', '(3.80\u00b2 \u2212 0\u00b2) / 2(6.80)', 'm\u00b2/s\u00b2 \u00f7 m'],
        ['a', '=', '14.44 / 13.60', ''],
        ['a', '=', '1.06 m/s\u00b2  (unrounded: 1.0618 m/s\u00b2)', ''],
    ])

    # Solution - Stage 2
    add_normal_para(doc, 'Stage 2 \u2014 use this acceleration to find the speed at 3.40 m', indent=Cm(0.5), bold=True)
    add_normal_para(doc, 'Same equation, same reasoning.  We still don\u2019t know or need t, so Eq. 3 applies again \u2014 but now we solve for v\u2082 instead of a.', indent=Cm(1))
    add_equation_line(doc, 'v\u2082\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)\u2082')

    add_normal_para(doc, 'This is already solved for v\u2082\u00b2 \u2014 one more transposition step (the square root) isolates v\u2082:', indent=Cm(1))
    add_aligned_table(doc, [
        ['v\u2082', '=', '\u221a[v\u2080\u00b2 + 2a(x \u2212 x\u2080)\u2082]', 'apply \u221a to both sides'],
    ])

    add_normal_para(doc, 'Substitute values (use the un-rounded a = 1.0618 m/s\u00b2 to avoid rounding error):', indent=Cm(1))
    add_aligned_table(doc, [
        ['v\u2082', '=', '\u221a[0\u00b2 + 2(1.0618)(3.40)]', ''],
        ['v\u2082', '=', '\u221a[7.220]', ''],
        ['v\u2082', '=', '2.69 m/s', ''],
    ])

    add_normal_para(doc, 'Since v\u2080 = 0, speed is proportional to the square root of distance traveled. Half the distance does not give half the speed \u2014 it gives speed divided by \u221a2 \u2248 1.414. Check: 3.80 / 1.414 = 2.69 m/s \u2713. Kinematics with acceleration is not "linear" in the intuitive sense!', indent=Cm(1), italic=True)

    # =========================================================================
    # PROBLEM 5
    # =========================================================================
    add_problem_heading(doc, 'Problem 5')
    add_problem_text(doc,
        'A Lamborghini Aventador S can go from 0 to 60 mph in 2.7 s. Assume constant acceleration. '
        '(a) What is the magnitude of the acceleration? (b) How far has the car traveled when it reaches 60 mph?'
    )

    # Given
    add_section_label(doc, 'Given')
    add_given_table(doc, [
        ['v\u2080', '0 mph = 0 m/s', 'Starts from rest'],
        ['v', '60 mph', 'Must convert to m/s'],
        ['t', '2.7 s', 'Time to reach 60 mph'],
    ])

    add_normal_para(doc, 'Unit conversion:', indent=Cm(1))
    add_normal_para(doc, 'v = 60 mph \u00d7 (1609 m / 1 mi) \u00d7 (1 h / 3600 s) = 26.8 m/s', indent=Cm(1))

    # Required
    add_section_label(doc, 'Required')
    add_normal_para(doc, '(a)  a = ?', indent=Cm(1))
    add_normal_para(doc, '(b)  (x \u2212 x\u2080) = ?', indent=Cm(1))

    # Solution (a)
    add_section_label(doc, 'Solution')
    add_normal_para(doc, '(a) Finding acceleration', indent=Cm(0.5), bold=True)
    add_normal_para(doc, 'Which equation?  We are given v\u2080, v, and t. We are not given, and don\u2019t need, displacement. Eq. 1 is missing (x \u2212 x\u2080), so that\u2019s our match.', indent=Cm(1))
    add_equation_line(doc, 'v = v\u2080 + at')

    add_normal_para(doc, 'Derivation by transposition \u2014 isolate a (same steps as Problem 1):', indent=Cm(1))
    add_aligned_table(doc, [
        ['v', '=', 'v\u2080 + at', ''],
        ['v \u2212 v\u2080', '=', 'at', 'transpose v\u2080'],
        ['(v \u2212 v\u2080) / t', '=', 'a', 'transpose t'],
        ['a', '=', '(v \u2212 v\u2080) / t', ''],
    ])

    add_normal_para(doc, 'Substitute values:', indent=Cm(1))
    add_aligned_table(doc, [
        ['a', '=', '(26.8 \u2212 0) / 2.7', 'm/s \u00f7 s'],
        ['a', '=', '9.93 m/s\u00b2', ''],
    ])

    add_normal_para(doc, 'That\u2019s about 1.01 g \u2014 you\u2019d feel about your own body weight pushing you back into the seat!', indent=Cm(1), italic=True)

    # Solution (b)
    add_normal_para(doc, '(b) Finding distance traveled', indent=Cm(0.5), bold=True)
    add_normal_para(doc, 'Which equation?  We know v\u2080, v, t, and a (rounded). To avoid rounding error, use the equation missing a \u2014 Eq. 4.', indent=Cm(1))
    add_equation_line(doc, '(x \u2212 x\u2080) = \u00bd(v\u2080 + v)t')

    add_normal_para(doc, 'Derivation by transposition \u2014 isolate (x \u2212 x\u2080) (same steps as Problem 1):', indent=Cm(1))
    add_aligned_table(doc, [
        ['(x \u2212 x\u2080)', '=', '\u00bd(v\u2080 + v)t', ''],
    ])

    add_normal_para(doc, 'Substitute values:', indent=Cm(1))
    add_aligned_table(doc, [
        ['(x \u2212 x\u2080)', '=', '\u00bd(0 + 26.8)(2.7)', ''],
        ['(x \u2212 x\u2080)', '=', '36.2 m', ''],
    ])

    add_normal_para(doc, 'For comparison, that\u2019s roughly the length of two and a half basketball courts, covered in under 3 seconds!', indent=Cm(1), italic=True)

    # =========================================================================
    # SUMMARY TABLE
    # =========================================================================
    add_problem_heading(doc, 'Summary of Final Answers')

    summary_table = doc.add_table(rows=6, cols=3)
    summary_table.alignment = WD_TABLE_ALIGNMENT.LEFT

    # Set up summary table with visible borders
    tbl = summary_table._tbl
    tblPr = tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="000000"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)

    # Table indent
    tblInd = parse_xml(f'<w:tblInd {nsdecls("w")} w:w="720" w:type="dxa"/>')
    tblPr.append(tblInd)

    summary_data = [
        ['Problem', 'Part (a)', 'Part (b)'],
        ['1. Tennis serve', 'a = 2.44 \u00d7 10\u00b3 m/s\u00b2', '(x \u2212 x\u2080) = 1.10 m'],
        ['2. Baseball pitch', 'a = 675 m/s\u00b2', 't = 0.0667 s'],
        ['3. Airbag', '(x \u2212 x\u2080) = 1.70 m (minimum)', '\u2014'],
        ['4. Incline block', 'v\u2082 = 2.69 m/s at 3.40 m', '\u2014'],
        ['5. Lamborghini', 'a = 9.93 m/s\u00b2', '(x \u2212 x\u2080) = 36.2 m'],
    ]

    for i, row_data in enumerate(summary_data):
        row = summary_table.rows[i]
        for j, cell_text in enumerate(row_data):
            cell = row.cells[j]
            p = cell.paragraphs[0]
            set_paragraph_spacing(p, before=40, after=40)
            run = p.add_run(cell_text)
            run.font.size = Pt(11)
            run.font.name = 'Calibri'
            if i == 0:
                run.bold = True

    # Footer
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=360, after=0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Problem Set 3 \u2014 Uniformly Accelerated Motion (Horizontal)   |   Page ')
    run.font.size = Pt(9)
    run.font.name = 'Calibri'

    return doc


if __name__ == '__main__':
    doc = build_document()
    output_path = '/projects/sandbox/physics/ProblemSet3-SolutionKey.docx'
    doc.save(output_path)
    print(f'Document saved to: {output_path}')
