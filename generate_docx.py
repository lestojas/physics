"""
Generate ProblemSet3-SolutionKey.docx with OMML equations and proper formatting.
Matches the original document structure exactly:
- Problem headings, indented statements
- Given (bullets with · or tables), Required, Solution sections
- OMML display equations
- 4-column borderless aligned tables for derivation steps (with OMML in cells)
- Commentary in italic
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, Emu, RGBColor, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, OxmlElement
import lxml.etree as ET
import copy

# Namespaces
MATH_NS = 'http://schemas.openxmlformats.org/officeDocument/2006/math'
WORD_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
M = '{%s}' % MATH_NS
W = '{%s}' % WORD_NS

NSMAP = {'m': MATH_NS, 'w': WORD_NS}


# ===========================================================================
# OMML EQUATION BUILDERS
# ===========================================================================

def make_math_run(text, italic=True, font='Cambria Math'):
    """Create an OMML math run <m:r> with text."""
    r = ET.SubElement(ET.Element('dummy'), f'{M}r')
    # Math run properties
    if not italic:
        rPr = ET.SubElement(r, f'{M}rPr')
        sty = ET.SubElement(rPr, f'{M}sty')
        sty.set(f'{M}val', 'p')  # plain (non-italic)
    # Word run properties for font
    wRPr = ET.SubElement(r, f'{W}rPr')
    rFonts = ET.SubElement(wRPr, f'{W}rFonts')
    rFonts.set(f'{W}ascii', font)
    rFonts.set(f'{W}hAnsi', font)
    # The text
    t = ET.SubElement(r, f'{M}t')
    t.text = text
    # Handle spaces
    if text.startswith(' ') or text.endswith(' '):
        t.set('{http://www.w3.org/XML/1998/namespace}space', 'preserve')
    return r


def make_subscript(base_text, sub_text):
    """Create <m:sSub> for subscript like v₀."""
    sSub = ET.Element(f'{M}sSub')
    sSubPr = ET.SubElement(sSub, f'{M}sSubPr')
    ET.SubElement(sSubPr, f'{M}ctrlPr')
    e = ET.SubElement(sSub, f'{M}e')
    e.append(make_math_run(base_text))
    sub = ET.SubElement(sSub, f'{M}sub')
    sub.append(make_math_run(sub_text))
    return sSub


def make_superscript(base_text, sup_text):
    """Create <m:sSup> for superscript like v²."""
    sSup = ET.Element(f'{M}sSup')
    sSupPr = ET.SubElement(sSup, f'{M}sSupPr')
    ET.SubElement(sSupPr, f'{M}ctrlPr')
    e = ET.SubElement(sSup, f'{M}e')
    e.append(make_math_run(base_text))
    sup = ET.SubElement(sSup, f'{M}sup')
    sup.append(make_math_run(sup_text))
    return sSup


def make_sub_sup(base_text, sub_text, sup_text):
    """Create <m:sSubSup> for subscript+superscript like v₀²."""
    sSubSup = ET.Element(f'{M}sSubSup')
    sSubSupPr = ET.SubElement(sSubSup, f'{M}sSubSupPr')
    ET.SubElement(sSubSupPr, f'{M}ctrlPr')
    e = ET.SubElement(sSubSup, f'{M}e')
    e.append(make_math_run(base_text))
    sub = ET.SubElement(sSubSup, f'{M}sub')
    sub.append(make_math_run(sub_text))
    sup = ET.SubElement(sSubSup, f'{M}sup')
    sup.append(make_math_run(sup_text))
    return sSubSup


def make_fraction(num_elements, den_elements):
    """Create <m:f> fraction. num_elements and den_elements are lists of OMML elements."""
    f = ET.Element(f'{M}f')
    fPr = ET.SubElement(f, f'{M}fPr')
    ET.SubElement(fPr, f'{M}ctrlPr')
    num = ET.SubElement(f, f'{M}num')
    for el in num_elements:
        num.append(el)
    den = ET.SubElement(f, f'{M}den')
    for el in den_elements:
        den.append(el)
    return f


def make_radical(elements, show_deg=False):
    """Create <m:rad> square root. elements is list of OMML elements under the radical."""
    rad = ET.Element(f'{M}rad')
    radPr = ET.SubElement(rad, f'{M}radPr')
    if not show_deg:
        degHide = ET.SubElement(radPr, f'{M}degHide')
        degHide.set(f'{M}val', '1')
    ET.SubElement(radPr, f'{M}ctrlPr')
    deg = ET.SubElement(rad, f'{M}deg')
    e = ET.SubElement(rad, f'{M}e')
    for el in elements:
        e.append(el)
    return rad


def make_delimited(elements, beg_char='(', end_char=')'):
    """Create <m:d> delimited (parenthesized) group."""
    d = ET.Element(f'{M}d')
    dPr = ET.SubElement(d, f'{M}dPr')
    begChr = ET.SubElement(dPr, f'{M}begChr')
    begChr.set(f'{M}val', beg_char)
    endChr = ET.SubElement(dPr, f'{M}endChr')
    endChr.set(f'{M}val', end_char)
    ET.SubElement(dPr, f'{M}ctrlPr')
    e = ET.SubElement(d, f'{M}e')
    for el in elements:
        e.append(el)
    return d


def make_omath(elements):
    """Create <m:oMath> inline math containing the given elements."""
    oMath = ET.Element(f'{M}oMath')
    for el in elements:
        oMath.append(el)
    return oMath


def make_omath_para(elements):
    """Create <m:oMathPara> display (centered) math paragraph."""
    oMathPara = ET.Element(f'{M}oMathPara')
    oMath = ET.SubElement(oMathPara, f'{M}oMath')
    for el in elements:
        oMath.append(el)
    return oMathPara


# ===========================================================================
# HIGHER-LEVEL EQUATION BUILDERS (specific to this problem set)
# ===========================================================================

def eq_v_sub(var, subscript):
    """Variable with subscript: v₀, x₀, v₁, v₂, etc."""
    return make_subscript(var, subscript)


def eq_v_sup(var, superscript):
    """Variable with superscript: v², etc."""
    return make_superscript(var, superscript)


def eq_v_sub_sup(var, subscript, superscript):
    """Variable with both: v₀²"""
    return make_sub_sup(var, subscript, superscript)


def eq_displacement():
    """(x - x₀) as a delimited expression."""
    return make_delimited([
        make_math_run('x'),
        make_math_run('\u2212'),
        make_subscript('x', '0'),
    ])


def eq_displacement_sub(subscript):
    """(x - x₀)₁ or (x - x₀)₂"""
    sSub = ET.Element(f'{M}sSub')
    sSubPr = ET.SubElement(sSub, f'{M}sSubPr')
    ET.SubElement(sSubPr, f'{M}ctrlPr')
    e = ET.SubElement(sSub, f'{M}e')
    # The base is the delimited (x - x₀)
    d = make_delimited([
        make_math_run('x'),
        make_math_run('\u2212'),
        make_subscript('x', '0'),
    ])
    e.append(d)
    sub = ET.SubElement(sSub, f'{M}sub')
    sub.append(make_math_run(subscript))
    return sSub


# Build complete equations used in the document:

def build_eq1():
    """v = v₀ + at"""
    return [
        make_math_run('v'),
        make_math_run('='),
        make_subscript('v', '0'),
        make_math_run('+'),
        make_math_run('at'),
    ]


def build_eq3():
    """v² = v₀² + 2a(x − x₀)"""
    return [
        make_superscript('v', '2'),
        make_math_run('='),
        make_sub_sup('v', '0', '2'),
        make_math_run('+'),
        make_math_run('2a'),
        make_delimited([
            make_math_run('x'),
            make_math_run('\u2212'),
            make_subscript('x', '0'),
        ]),
    ]


def build_eq4():
    """(x − x₀) = ½(v₀ + v)t"""
    return [
        make_delimited([
            make_math_run('x'),
            make_math_run('\u2212'),
            make_subscript('x', '0'),
        ]),
        make_math_run('='),
        make_fraction([make_math_run('1')], [make_math_run('2')]),
        make_delimited([
            make_subscript('v', '0'),
            make_math_run('+'),
            make_math_run('v'),
        ]),
        make_math_run('t'),
    ]


# Derivation step builders for aligned tables:

def build_isolate_a_step1():
    """v = v₀ + at"""
    return build_eq1()


def build_isolate_a_step2():
    """v − v₀ = at"""
    return [
        make_math_run('v'),
        make_math_run('\u2212'),
        make_subscript('v', '0'),
    ], [
        make_math_run('at'),
    ]


def build_isolate_a_step3():
    """(v − v₀)/t = a  as fraction"""
    return [
        make_fraction(
            [make_math_run('v'), make_math_run('\u2212'), make_subscript('v', '0')],
            [make_math_run('t')]
        ),
    ], [
        make_math_run('a'),
    ]


def build_isolate_a_step4():
    """a = (v − v₀)/t"""
    return [
        make_math_run('a'),
    ], [
        make_fraction(
            [make_math_run('v'), make_math_run('\u2212'), make_subscript('v', '0')],
            [make_math_run('t')]
        ),
    ]


# ===========================================================================
# DOCUMENT FORMATTING HELPERS
# ===========================================================================

def set_cell_border_none(cell):
    """Remove all borders from a cell."""
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
            set_cell_border_none(cell)


def set_cell_width(cell, width_twips):
    """Set cell width in twips."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcW = parse_xml(f'<w:tcW {nsdecls("w")} w:w="{width_twips}" w:type="dxa"/>')
    tcPr.append(tcW)


def set_cell_margins(cell, top=0, bottom=0, start=72, end=72):
    """Set cell margins in twips."""
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
    """Set paragraph spacing (in twips for before/after, 240=single line)."""
    pPr = paragraph._p.get_or_add_pPr()
    spacing = parse_xml(
        f'<w:spacing {nsdecls("w")} w:before="{before}" w:after="{after}" w:line="{line}" w:lineRule="auto"/>'
    )
    pPr.append(spacing)


def set_table_indent(table, indent_twips=720):
    """Set left indent for a table."""
    tbl = table._tbl
    tblPr = tbl.tblPr
    tblInd = parse_xml(f'<w:tblInd {nsdecls("w")} w:w="{indent_twips}" w:type="dxa"/>')
    tblPr.append(tblInd)


def add_omml_to_paragraph(paragraph, omml_elements):
    """Add OMML inline math elements to a paragraph."""
    oMath = OxmlElement('m:oMath')
    for el in omml_elements:
        # Convert lxml element to OxmlElement by serializing/parsing
        xml_str = ET.tostring(el)
        oxel = parse_xml(xml_str)
        oMath.append(oxel)
    paragraph._p.append(oMath)


def add_omml_display_to_body(doc, omml_elements, indent=Cm(1)):
    """Add a display (centered) OMML equation paragraph to the document body."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = indent
    set_paragraph_spacing(p, before=120, after=120)

    # Build oMathPara > oMath
    oMathPara = OxmlElement('m:oMathPara')
    oMathParaPr = OxmlElement('m:oMathParaPr')
    jc = OxmlElement('m:jc')
    jc.set(qn('m:val'), 'left')
    oMathParaPr.append(jc)
    oMathPara.append(oMathParaPr)

    oMath = OxmlElement('m:oMath')
    for el in omml_elements:
        xml_str = ET.tostring(el)
        oxel = parse_xml(xml_str)
        oMath.append(oxel)
    oMathPara.append(oMath)

    p._p.append(oMathPara)
    return p


def add_omml_to_cell(cell, omml_elements):
    """Add OMML inline math to a table cell's paragraph."""
    p = cell.paragraphs[0]
    oMath = OxmlElement('m:oMath')
    for el in omml_elements:
        xml_str = ET.tostring(el)
        oxel = parse_xml(xml_str)
        oMath.append(oxel)
    p._p.append(oMath)


# ===========================================================================
# DOCUMENT CONTENT HELPERS
# ===========================================================================

def add_problem_heading(doc, text):
    """Add Problem N heading using Heading 1 style (dark blue #365F91, 14pt, bold)."""
    p = doc.add_heading(text, level=1)
    # Override spacing
    set_paragraph_spacing(p, before=360, after=120)
    return p


def add_problem_text(doc, text):
    """Add indented problem statement."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Cm(1.27)
    set_paragraph_spacing(p, before=60, after=120)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    return p


def add_section_heading(doc, text):
    """Add Given/Required/Solution heading using Heading 2 style (blue #4F81BD, bold)."""
    p = doc.add_heading(text, level=2)
    # Override size to 11pt (keep the blue color from the style)
    for run in p.runs:
        run.font.size = Pt(12)
    set_paragraph_spacing(p, before=200, after=80)
    return p


def add_sub_heading(doc, text, indent=Cm(0.63)):
    """Add (a) Finding acceleration style sub-heading using Heading 3 (blue, bold)."""
    p = doc.add_heading(text, level=3)
    p.paragraph_format.left_indent = indent
    for run in p.runs:
        run.font.size = Pt(11)
    set_paragraph_spacing(p, before=160, after=60)
    return p


def add_body_text(doc, text, indent=Cm(1.27), italic=False, bold=False):
    """Add normal body text."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = indent
    set_paragraph_spacing(p, before=60, after=60)
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    run.italic = italic
    run.bold = bold
    return p


def add_bullet(doc, text, indent=Cm(1.27)):
    """Add a bullet point with middle dot (·)."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = indent
    p.paragraph_format.first_line_indent = Cm(-0.4)
    set_paragraph_spacing(p, before=40, after=40)
    run = p.add_run('\u00b7 ')
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    run = p.add_run(text)
    run.font.size = Pt(11)
    run.font.name = 'Calibri'
    return p


def add_given_table(doc, rows, indent=720):
    """
    Add a Given table: Symbol | Value | Annotation.
    rows is list of [symbol, value, annotation].
    Header row has bottom border and light blue shading.
    """
    table = doc.add_table(rows=len(rows) + 1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    remove_table_borders(table)

    col_widths = [1200, 2000, 5800]
    headers = ['Symbol', 'Value', 'Annotation']

    # Header row with styling
    for j, header in enumerate(headers):
        cell = table.rows[0].cells[j]
        set_cell_width(cell, col_widths[j])
        set_cell_margins(cell, top=40, bottom=40, start=72, end=72)
        # Add bottom border to header cells
        tc = cell._tc
        tcPr = tc.get_or_add_tcPr()
        tcBorders = parse_xml(
            f'<w:tcBorders {nsdecls("w")}>'
            f'  <w:top w:val="nil"/>'
            f'  <w:left w:val="nil"/>'
            f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="4F81BD"/>'
            f'  <w:right w:val="nil"/>'
            f'</w:tcBorders>'
        )
        tcPr.append(tcBorders)
        # Light blue shading for header
        shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="DBE5F1" w:val="clear" w:color="auto"/>')
        tcPr.append(shd)

        p = cell.paragraphs[0]
        set_paragraph_spacing(p, before=0, after=0)
        run = p.add_run(header)
        run.bold = True
        run.font.size = Pt(11)
        run.font.name = 'Calibri'
        run.font.color.rgb = RGBColor(0x36, 0x5F, 0x91)  # Dark blue matching Heading 1

    # Data rows
    for i, row_data in enumerate(rows):
        for j in range(3):
            cell = table.rows[i + 1].cells[j]
            set_cell_width(cell, col_widths[j])
            set_cell_margins(cell, top=20, bottom=20, start=72, end=72)
            p = cell.paragraphs[0]
            set_paragraph_spacing(p, before=0, after=0)
            text = row_data[j] if j < len(row_data) else ''
            run = p.add_run(text)
            run.font.size = Pt(11)
            run.font.name = 'Calibri'
            if j == 2:
                run.italic = True

    set_table_indent(table, indent)
    return table


def add_aligned_equations(doc, rows, col_widths=None, indent=720):
    """
    Add a borderless 4-column table for aligned equation steps.
    Each row is a dict with keys: 'lhs', 'eq', 'rhs', 'note'
    where lhs and rhs can be either strings or lists of OMML elements.
    'eq' is always '=' sign.
    'note' is annotation text (string, italic).
    """
    if col_widths is None:
        col_widths = [2400, 360, 3600, 3200]

    table = doc.add_table(rows=len(rows), cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    remove_table_borders(table)

    for i, row_data in enumerate(rows):
        row = table.rows[i]
        for j in range(4):
            cell = row.cells[j]
            set_cell_width(cell, col_widths[j])
            set_cell_margins(cell, top=30, bottom=30, start=50, end=50)
            p = cell.paragraphs[0]
            set_paragraph_spacing(p, before=0, after=0)

            if j == 0:  # LHS
                content = row_data.get('lhs', '')
                if isinstance(content, list):
                    add_omml_to_cell(cell, content)
                else:
                    run = p.add_run(content)
                    run.font.size = Pt(11)
                    run.font.name = 'Cambria Math'
            elif j == 1:  # = sign
                run = p.add_run('=')
                run.font.size = Pt(11)
                run.font.name = 'Cambria Math'
            elif j == 2:  # RHS
                content = row_data.get('rhs', '')
                if isinstance(content, list):
                    add_omml_to_cell(cell, content)
                else:
                    run = p.add_run(content)
                    run.font.size = Pt(11)
                    run.font.name = 'Cambria Math'
            elif j == 3:  # annotation
                note = row_data.get('note', '')
                if note:
                    run = p.add_run(note)
                    run.font.size = Pt(10)
                    run.font.name = 'Calibri'
                    run.italic = True
                    run.font.color.rgb = RGBColor(80, 80, 80)

    set_table_indent(table, indent)
    return table


# ===========================================================================
# MAIN DOCUMENT BUILDER
# ===========================================================================

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
    add_section_heading(doc, 'Given')
    add_bullet(doc, 'v\u2080 = 0 m/s  \u2014  \u201cStarts from rest\u201d means initial velocity is zero')
    add_bullet(doc, 'v = 73.14 m/s  \u2014  Final speed as it leaves the racquet')
    add_bullet(doc, 't = 30.0 ms = 0.0300 s  \u2014  Convert ms \u2192 s by dividing by 1000, since equations need SI units')

    # Required
    add_section_heading(doc, 'Required')
    add_body_text(doc, '(a)  a = ?')
    add_body_text(doc, '(b)  (x \u2212 x\u2080) = ?   (distance traveled)')

    # Solution
    add_section_heading(doc, 'Solution')

    # (a) Finding acceleration
    add_sub_heading(doc, '(a) Finding acceleration')
    add_body_text(doc,
        'Which equation?  We are given v\u2080, v, and t. We are not given \u2014 and don\u2019t need \u2014 '
        'displacement (x \u2212 x\u2080). Hence, Eq. 1 is our match.'
    )

    # Display equation: v = v₀ + at
    add_omml_display_to_body(doc, build_eq1())

    add_body_text(doc, 'Isolate a:')

    # Aligned derivation steps
    add_aligned_equations(doc, [
        {'lhs': [make_math_run('v')],
         'rhs': [make_subscript('v', '0'), make_math_run('+'), make_math_run('at')],
         'note': ''},
        {'lhs': [make_math_run('v'), make_math_run('\u2212'), make_subscript('v', '0')],
         'rhs': [make_math_run('at')],
         'note': ''},
        {'lhs': [make_fraction(
                    [make_math_run('v'), make_math_run('\u2212'), make_subscript('v', '0')],
                    [make_math_run('t')])],
         'rhs': [make_math_run('a')],
         'note': ''},
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction(
                    [make_math_run('v'), make_math_run('\u2212'), make_subscript('v', '0')],
                    [make_math_run('t')])],
         'note': ''},
    ])

    add_body_text(doc, 'Substitute values:')

    add_aligned_equations(doc, [
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction(
                    [make_math_run('73.14'), make_math_run('\u2212'), make_math_run('0')],
                    [make_math_run('0.0300')])],
         'note': ''},
        {'lhs': [make_math_run('a')],
         'rhs': [make_math_run('2.44\u00d710\u00b3 m/s\u00b2')],
         'note': ''},
    ])

    add_body_text(doc,
        'This is roughly 249 times the acceleration due to gravity (g = 9.8 m/s\u00b2) '
        '\u2014 that\u2019s how violent a tennis serve impact really is!',
        italic=True
    )

    # (b) Finding distance traveled
    add_sub_heading(doc, '(b) Finding distance traveled')
    add_body_text(doc,
        'Which equation?  We now know v\u2080, v, t, and a from part (a). We could use Eq. 2, but since '
        'a was a rounded answer, reusing it could introduce rounding error. It is safer to use the '
        'equation that doesn\u2019t need acceleration at all \u2014 Eq. 4, which is missing a.'
    )

    # Display equation: (x − x₀) = ½(v₀ + v)t
    add_omml_display_to_body(doc, build_eq4())

    add_body_text(doc, 'Derivation by transposition \u2014 isolate (x \u2212 x\u2080), the distance traveled:')

    add_aligned_equations(doc, [
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction([make_math_run('1')], [make_math_run('2')]),
                 make_delimited([make_subscript('v', '0'), make_math_run('+'), make_math_run('v')]),
                 make_math_run('t')],
         'note': ''},
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction([make_math_run('1')], [make_math_run('2')]),
                 make_delimited([make_subscript('v', '0'), make_math_run('+'), make_math_run('v')]),
                 make_math_run('t')],
         'note': 'transpose x\u2080: added on the right, becomes subtracted on the left'},
    ])

    add_body_text(doc, 'Substitute values:')

    add_aligned_equations(doc, [
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction([make_math_run('1')], [make_math_run('2')]),
                 make_delimited([make_math_run('0'), make_math_run('+'), make_math_run('73.14')]),
                 make_delimited([make_math_run('0.0300')], '(', ')')],
         'note': ''},
        {'lhs': [eq_displacement()],
         'rhs': [make_math_run('1.10 m')],
         'note': ''},
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
    add_section_heading(doc, 'Given')
    add_given_table(doc, [
        ['v\u2080', '0 m/s', 'Ball starts at rest in the pitcher\u2019s hand before the throwing motion begins'],
        ['v', '45.0 m/s', 'Speed as the ball leaves the hand'],
        ['(x \u2212 x\u2080)', '1.50 m', 'Distance over which the hand accelerates the ball'],
    ])

    # Required
    add_section_heading(doc, 'Required')
    add_body_text(doc, '(a)  a = ?')
    add_body_text(doc, '(b)  t = ?')

    # Solution
    add_section_heading(doc, 'Solution')

    # (a)
    add_sub_heading(doc, '(a) Finding acceleration')
    add_body_text(doc,
        'Which equation?  We are given v\u2080, v, and (x \u2212 x\u2080). We are not given, and do not yet need, '
        'time t. Eq. 3 is the one missing t, so that\u2019s our match.'
    )

    add_omml_display_to_body(doc, build_eq3())

    add_body_text(doc, 'Derivation by transposition \u2014 isolate a:')

    add_aligned_equations(doc, [
        {'lhs': [make_superscript('v', '2')],
         'rhs': [make_sub_sup('v', '0', '2'), make_math_run('+'), make_math_run('2a'),
                 eq_displacement()],
         'note': ''},
        {'lhs': [make_superscript('v', '2'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
         'rhs': [make_math_run('2a'), eq_displacement()],
         'note': 'transpose v\u2080\u00b2: added on the right, becomes subtracted on the left'},
        {'lhs': [make_fraction(
                    [make_superscript('v', '2'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
                    [make_math_run('2'), eq_displacement()])],
         'rhs': [make_math_run('a')],
         'note': 'transpose 2(x \u2212 x\u2080): multiplying a, becomes a divisor'},
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction(
                    [make_superscript('v', '2'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
                    [make_math_run('2'), eq_displacement()])],
         'note': ''},
    ])

    add_body_text(doc, 'Substitute values:')

    add_aligned_equations(doc, [
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction(
                    [make_superscript('45.0', '2'), make_math_run('\u2212'), make_superscript('0', '2')],
                    [make_math_run('2'), make_delimited([make_math_run('1.50')])])],
         'note': 'm\u00b2/s\u00b2 \u00f7 m'},
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction([make_math_run('2025')], [make_math_run('3.00')])],
         'note': ''},
        {'lhs': [make_math_run('a')],
         'rhs': [make_math_run('675 m/s\u00b2')],
         'note': ''},
    ])

    # (b)
    add_sub_heading(doc, '(b) Finding time')
    add_body_text(doc,
        'Which equation?  We now know v\u2080, v, (x \u2212 x\u2080), and a (rounded). To avoid propagating '
        'rounding error from part (a), use the equation that doesn\u2019t need a \u2014 Eq. 4, missing acceleration.'
    )

    add_omml_display_to_body(doc, build_eq4())

    add_body_text(doc, 'Derivation by transposition \u2014 isolate t:')

    add_aligned_equations(doc, [
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction([make_math_run('1')], [make_math_run('2')]),
                 make_delimited([make_subscript('v', '0'), make_math_run('+'), make_math_run('v')]),
                 make_math_run('t')],
         'note': 'transpose x\u2080 (as in Problem 1)'},
        {'lhs': [make_math_run('2'), eq_displacement()],
         'rhs': [make_delimited([make_subscript('v', '0'), make_math_run('+'), make_math_run('v')]),
                 make_math_run('t')],
         'note': 'transpose \u00bd: multiply both sides by 2 to clear the fraction'},
        {'lhs': [make_fraction(
                    [make_math_run('2'), eq_displacement()],
                    [make_delimited([make_subscript('v', '0'), make_math_run('+'), make_math_run('v')])])],
         'rhs': [make_math_run('t')],
         'note': 'transpose (v\u2080 + v): multiplying t, becomes a divisor'},
        {'lhs': [make_math_run('t')],
         'rhs': [make_fraction(
                    [make_math_run('2'), eq_displacement()],
                    [make_delimited([make_subscript('v', '0'), make_math_run('+'), make_math_run('v')])])],
         'note': ''},
    ])

    add_body_text(doc, 'Substitute values:')

    add_aligned_equations(doc, [
        {'lhs': [make_math_run('t')],
         'rhs': [make_fraction(
                    [make_math_run('2'), make_delimited([make_math_run('1.50')])],
                    [make_delimited([make_math_run('0'), make_math_run('+'), make_math_run('45.0')])])],
         'note': 'm \u00f7 (m/s)'},
        {'lhs': [make_math_run('t')],
         'rhs': [make_fraction([make_math_run('3.00')], [make_math_run('45.0')])],
         'note': ''},
        {'lhs': [make_math_run('t')],
         'rhs': [make_math_run('0.0667 s  (66.7 ms)')],
         'note': ''},
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
    add_section_heading(doc, 'Given')
    add_given_table(doc, [
        ['v\u2080', '105 km/h', 'Must convert to m/s (SI unit) before using the equations'],
        ['v', '0 m/s', 'The car (and you) come to a complete stop'],
        ['a', '\u2212250 m/s\u00b2', 'Use the maximum allowed magnitude of deceleration \u2014 this gives the minimum possible stopping distance. The negative sign shows it is a deceleration, opposite to the direction of motion.'],
    ])

    add_body_text(doc, 'Unit conversion:')
    add_body_text(doc, 'v\u2080 = 105 km/h \u00d7 (1000 m / 1 km) \u00d7 (1 h / 3600 s) = 29.17 m/s')

    # Required
    add_section_heading(doc, 'Required')
    add_body_text(doc, '(x \u2212 x\u2080) = ?   (minimum stopping distance)')

    # Solution
    add_section_heading(doc, 'Solution')
    add_body_text(doc,
        'Which equation?  We are given v\u2080, v, and a. We are not given, and don\u2019t need, time t. '
        'Eq. 3 is missing t, so that\u2019s our match.'
    )

    add_omml_display_to_body(doc, build_eq3())

    add_body_text(doc, 'Derivation by transposition \u2014 isolate (x \u2212 x\u2080):')

    add_aligned_equations(doc, [
        {'lhs': [make_superscript('v', '2')],
         'rhs': [make_sub_sup('v', '0', '2'), make_math_run('+'), make_math_run('2a'),
                 eq_displacement()],
         'note': ''},
        {'lhs': [make_superscript('v', '2'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
         'rhs': [make_math_run('2a'), eq_displacement()],
         'note': 'transpose v\u2080\u00b2: added on the right, becomes subtracted on the left'},
        {'lhs': [make_fraction(
                    [make_superscript('v', '2'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
                    [make_math_run('2a')])],
         'rhs': [eq_displacement()],
         'note': 'transpose 2a: multiplying, becomes a divisor'},
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction(
                    [make_superscript('v', '2'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
                    [make_math_run('2a')])],
         'note': ''},
    ])

    add_body_text(doc, 'Substitute values:')

    add_aligned_equations(doc, [
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction(
                    [make_superscript('0', '2'), make_math_run('\u2212'), make_superscript('29.17', '2')],
                    [make_math_run('2'), make_delimited([make_math_run('\u2212250')])])],
         'note': 'm\u00b2/s\u00b2 \u00f7 m/s\u00b2'},
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction([make_math_run('\u2212850.9')], [make_math_run('\u2212500')])],
         'note': ''},
        {'lhs': [eq_displacement()],
         'rhs': [make_math_run('1.70 m')],
         'note': ''},
    ])

    add_body_text(doc,
        'The negative signs on top and bottom cancel \u2014 that makes sense, since a distance must be positive! '
        'The airbag (plus crumple zone) must stop you within at least 1.70 m, or the deceleration will exceed '
        'the survivable limit of 250 m/s\u00b2.',
        italic=True
    )

    # =========================================================================
    # PROBLEM 4
    # =========================================================================
    add_problem_heading(doc, 'Problem 4')
    add_problem_text(doc,
        'A small block has constant acceleration as it slides down a frictionless incline, released from rest. '
        'Its speed after traveling 6.80 m is 3.80 m/s. What is its speed after traveling only 3.40 m (halfway down)?'
    )
    add_body_text(doc,
        'Strategy.  This problem needs two stages. First, use the full trip (0 to 6.80 m) to find the '
        'constant acceleration a. Then apply that same a to the shorter trip (0 to 3.40 m) to find the speed at that point.',
        italic=True
    )

    # Given
    add_section_heading(doc, 'Given')
    add_given_table(doc, [
        ['v\u2080', '0 m/s', 'Released from rest at the top'],
        ['(x \u2212 x\u2080)\u2081', '6.80 m', 'Full distance to the bottom'],
        ['v\u2081', '3.80 m/s', 'Speed at the bottom (end of the full distance)'],
        ['(x \u2212 x\u2080)\u2082', '3.40 m', 'The shorter distance we care about (exactly half of 6.80 m)'],
    ])

    # Required
    add_section_heading(doc, 'Required')
    add_body_text(doc, 'v\u2082 = ?   \u2014 the speed when the block has traveled 3.40 m')

    # Solution - Stage 1
    add_section_heading(doc, 'Solution')
    add_sub_heading(doc, 'Stage 1 \u2014 find the acceleration using the full 6.80 m trip')
    add_body_text(doc,
        'Which equation?  We know v\u2080, v\u2081, and (x \u2212 x\u2080)\u2081. We don\u2019t have or need t. Eq. 3 is missing t.'
    )

    add_omml_display_to_body(doc, build_eq3())

    add_body_text(doc, 'Derivation by transposition \u2014 isolate a:')

    add_aligned_equations(doc, [
        {'lhs': [make_superscript('v', '2'), make_math_run('\u2081')],
         'rhs': [make_sub_sup('v', '0', '2'), make_math_run('+'), make_math_run('2a'),
                 eq_displacement_sub('1')],
         'note': ''},
        {'lhs': [make_superscript('v', '2'), make_math_run('\u2081'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
         'rhs': [make_math_run('2a'), eq_displacement_sub('1')],
         'note': 'transpose v\u2080\u00b2'},
        {'lhs': [make_fraction(
                    [make_superscript('v', '2'), make_math_run('\u2081'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
                    [make_math_run('2'), eq_displacement_sub('1')])],
         'rhs': [make_math_run('a')],
         'note': 'transpose 2(x \u2212 x\u2080)\u2081: multiplying, becomes a divisor'},
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction(
                    [make_superscript('v', '2'), make_math_run('\u2081'), make_math_run('\u2212'), make_sub_sup('v', '0', '2')],
                    [make_math_run('2'), eq_displacement_sub('1')])],
         'note': ''},
    ])

    add_body_text(doc, 'Substitute values:')

    add_aligned_equations(doc, [
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction(
                    [make_superscript('3.80', '2'), make_math_run('\u2212'), make_superscript('0', '2')],
                    [make_math_run('2'), make_delimited([make_math_run('6.80')])])],
         'note': 'm\u00b2/s\u00b2 \u00f7 m'},
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction([make_math_run('14.44')], [make_math_run('13.60')])],
         'note': ''},
        {'lhs': [make_math_run('a')],
         'rhs': [make_math_run('1.06 m/s\u00b2  (unrounded: 1.0618 m/s\u00b2)')],
         'note': ''},
    ])

    # Stage 2
    add_sub_heading(doc, 'Stage 2 \u2014 use this acceleration to find the speed at 3.40 m')
    add_body_text(doc,
        'Same equation, same reasoning.  We still don\u2019t know or need t, so Eq. 3 applies again \u2014 '
        'but now we solve for v\u2082 instead of a.'
    )

    # Display: v₂² = v₀² + 2a(x − x₀)₂
    add_omml_display_to_body(doc, [
        make_sub_sup('v', '2', '2'),
        make_math_run('='),
        make_sub_sup('v', '0', '2'),
        make_math_run('+'),
        make_math_run('2a'),
        eq_displacement_sub('2'),
    ])

    add_body_text(doc, 'This is already solved for v\u2082\u00b2 \u2014 one more transposition step (the square root) isolates v\u2082:')

    add_aligned_equations(doc, [
        {'lhs': [make_subscript('v', '2')],
         'rhs': [make_radical([
                    make_sub_sup('v', '0', '2'),
                    make_math_run('+'),
                    make_math_run('2a'),
                    eq_displacement_sub('2'),
                 ])],
         'note': 'apply \u221a to both sides'},
    ])

    add_body_text(doc, 'Substitute values (use the un-rounded a = 1.0618 m/s\u00b2 to avoid rounding error):')

    add_aligned_equations(doc, [
        {'lhs': [make_subscript('v', '2')],
         'rhs': [make_radical([
                    make_superscript('0', '2'),
                    make_math_run('+'),
                    make_math_run('2'),
                    make_delimited([make_math_run('1.0618')]),
                    make_delimited([make_math_run('3.40')]),
                 ])],
         'note': ''},
        {'lhs': [make_subscript('v', '2')],
         'rhs': [make_radical([make_math_run('7.220')])],
         'note': ''},
        {'lhs': [make_subscript('v', '2')],
         'rhs': [make_math_run('2.69 m/s')],
         'note': ''},
    ])

    add_body_text(doc,
        'Since v\u2080 = 0, speed is proportional to the square root of distance traveled. Half the distance '
        'does not give half the speed \u2014 it gives speed divided by \u221a2 \u2248 1.414. '
        'Check: 3.80 / 1.414 = 2.69 m/s \u2713. Kinematics with acceleration is not \u201clinear\u201d in the intuitive sense!',
        italic=True
    )

    # =========================================================================
    # PROBLEM 5
    # =========================================================================
    add_problem_heading(doc, 'Problem 5')
    add_problem_text(doc,
        'A Lamborghini Aventador S can go from 0 to 60 mph in 2.7 s. Assume constant acceleration. '
        '(a) What is the magnitude of the acceleration? (b) How far has the car traveled when it reaches 60 mph?'
    )

    # Given
    add_section_heading(doc, 'Given')
    add_given_table(doc, [
        ['v\u2080', '0 mph = 0 m/s', 'Starts from rest'],
        ['v', '60 mph', 'Must convert to m/s'],
        ['t', '2.7 s', 'Time to reach 60 mph'],
    ])

    add_body_text(doc, 'Unit conversion:')
    add_body_text(doc, 'v = 60 mph \u00d7 (1609 m / 1 mi) \u00d7 (1 h / 3600 s) = 26.8 m/s')

    # Required
    add_section_heading(doc, 'Required')
    add_body_text(doc, '(a)  a = ?')
    add_body_text(doc, '(b)  (x \u2212 x\u2080) = ?')

    # Solution
    add_section_heading(doc, 'Solution')

    # (a)
    add_sub_heading(doc, '(a) Finding acceleration')
    add_body_text(doc,
        'Which equation?  We are given v\u2080, v, and t. We are not given, and don\u2019t need, displacement. '
        'Eq. 1 is missing (x \u2212 x\u2080), so that\u2019s our match.'
    )

    add_omml_display_to_body(doc, build_eq1())

    add_body_text(doc, 'Derivation by transposition \u2014 isolate a (same steps as Problem 1):')

    add_aligned_equations(doc, [
        {'lhs': [make_math_run('v')],
         'rhs': [make_subscript('v', '0'), make_math_run('+'), make_math_run('at')],
         'note': ''},
        {'lhs': [make_math_run('v'), make_math_run('\u2212'), make_subscript('v', '0')],
         'rhs': [make_math_run('at')],
         'note': 'transpose v\u2080'},
        {'lhs': [make_fraction(
                    [make_math_run('v'), make_math_run('\u2212'), make_subscript('v', '0')],
                    [make_math_run('t')])],
         'rhs': [make_math_run('a')],
         'note': 'transpose t'},
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction(
                    [make_math_run('v'), make_math_run('\u2212'), make_subscript('v', '0')],
                    [make_math_run('t')])],
         'note': ''},
    ])

    add_body_text(doc, 'Substitute values:')

    add_aligned_equations(doc, [
        {'lhs': [make_math_run('a')],
         'rhs': [make_fraction(
                    [make_math_run('26.8'), make_math_run('\u2212'), make_math_run('0')],
                    [make_math_run('2.7')])],
         'note': 'm/s \u00f7 s'},
        {'lhs': [make_math_run('a')],
         'rhs': [make_math_run('9.93 m/s\u00b2')],
         'note': ''},
    ])

    add_body_text(doc,
        'That\u2019s about 1.01 g \u2014 you\u2019d feel about your own body weight pushing you back into the seat!',
        italic=True
    )

    # (b)
    add_sub_heading(doc, '(b) Finding distance traveled')
    add_body_text(doc,
        'Which equation?  We know v\u2080, v, t, and a (rounded). To avoid rounding error, use the equation '
        'missing a \u2014 Eq. 4.'
    )

    add_omml_display_to_body(doc, build_eq4())

    add_body_text(doc, 'Derivation by transposition \u2014 isolate (x \u2212 x\u2080) (same steps as Problem 1):')

    add_aligned_equations(doc, [
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction([make_math_run('1')], [make_math_run('2')]),
                 make_delimited([make_subscript('v', '0'), make_math_run('+'), make_math_run('v')]),
                 make_math_run('t')],
         'note': ''},
    ])

    add_body_text(doc, 'Substitute values:')

    add_aligned_equations(doc, [
        {'lhs': [eq_displacement()],
         'rhs': [make_fraction([make_math_run('1')], [make_math_run('2')]),
                 make_delimited([make_math_run('0'), make_math_run('+'), make_math_run('26.8')]),
                 make_delimited([make_math_run('2.7')], '(', ')')],
         'note': ''},
        {'lhs': [eq_displacement()],
         'rhs': [make_math_run('36.2 m')],
         'note': ''},
    ])

    add_body_text(doc,
        'For comparison, that\u2019s roughly the length of two and a half basketball courts, covered in under 3 seconds!',
        italic=True
    )

    # =========================================================================
    # SUMMARY TABLE
    # =========================================================================
    add_problem_heading(doc, 'Summary of Final Answers')

    summary_table = doc.add_table(rows=6, cols=3)
    summary_table.alignment = WD_TABLE_ALIGNMENT.LEFT

    # Set up borders with blue accent color
    tbl = summary_table._tbl
    tblPr = tbl.tblPr
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'  <w:top w:val="single" w:sz="4" w:space="0" w:color="4F81BD"/>'
        f'  <w:left w:val="single" w:sz="4" w:space="0" w:color="4F81BD"/>'
        f'  <w:bottom w:val="single" w:sz="4" w:space="0" w:color="4F81BD"/>'
        f'  <w:right w:val="single" w:sz="4" w:space="0" w:color="4F81BD"/>'
        f'  <w:insideH w:val="single" w:sz="4" w:space="0" w:color="4F81BD"/>'
        f'  <w:insideV w:val="single" w:sz="4" w:space="0" w:color="4F81BD"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)
    set_table_indent(summary_table, 720)

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
                run.font.color.rgb = RGBColor(0xFF, 0xFF, 0xFF)  # White text on blue header
                # Add blue shading to header cells
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="4F81BD" w:val="clear" w:color="auto"/>')
                tcPr.append(shd)
            elif i % 2 == 0:
                # Alternating row shading (light blue)
                tc = cell._tc
                tcPr = tc.get_or_add_tcPr()
                shd = parse_xml(f'<w:shd {nsdecls("w")} w:fill="DBE5F1" w:val="clear" w:color="auto"/>')
                tcPr.append(shd)

    # Footer
    p = doc.add_paragraph()
    set_paragraph_spacing(p, before=360, after=0)
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p.add_run('Problem Set 3 \u2014 Uniformly Accelerated Motion (Horizontal)   |   Page 2 of 3')
    run.font.size = Pt(9)
    run.font.name = 'Calibri'

    return doc


if __name__ == '__main__':
    doc = build_document()
    output_path = '/projects/sandbox/physics/ProblemSet3-SolutionKey.docx'
    doc.save(output_path)
    print(f'Document saved to: {output_path}')
