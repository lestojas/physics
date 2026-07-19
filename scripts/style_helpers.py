"""
Word document styling helpers (colors, shading, borders, boxed callouts)
used to replicate the "Problem Set" solution-key visual style:
  - Navy title / section headings
  - Gray subtitle / annotation text
  - Light-gray shaded problem-statement boxes
  - Light-blue shaded reasoning callouts
  - Bold red boxed final answers
"""
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

NAVY = RGBColor(0x1F, 0x4E, 0x79)
GRAY_HEAD = RGBColor(0x59, 0x59, 0x59)
GRAY_TEXT = RGBColor(0x40, 0x40, 0x40)
RED = RGBColor(0xC0, 0x00, 0x00)
BLUE_ACCENT = RGBColor(0x2E, 0x74, 0xB5)

SHADE_STATEMENT = "EDEDED"   # light gray - problem statement box
SHADE_CALLOUT = "DEEAF6"     # light blue - reasoning callouts
SHADE_TABLE_HEAD = "1F4E79"  # navy header row for tables


def set_cell_shading(cell, hex_color):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for tag, val in (("top", top), ("bottom", bottom), ("start", left), ("end", right)):
        el = OxmlElement("w:%s" % tag)
        el.set(qn("w:w"), str(val))
        el.set(qn("w:type"), "dxa")
        mar.append(el)
    tcPr.append(mar)


def remove_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "none")
        el.set(qn("w:sz"), "0")
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), "auto")
        borders.append(el)
    tblPr.append(borders)


def set_table_borders(table, color="BFBFBF", sz=4):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for edge in ("top", "left", "bottom", "right", "insideH", "insideV"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), str(sz))
        el.set(qn("w:space"), "0")
        el.set(qn("w:color"), color)
        borders.append(el)
    tblPr.append(borders)


def add_bottom_border(paragraph, color="1F4E79", sz=12):
    """Adds a single bottom border/rule under a paragraph (used beneath
    'Problem N' headings, like the horizontal line in the reference image)."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(sz))
    bottom.set(qn("w:space"), "4")
    bottom.set(qn("w:color"), color)
    pBdr.append(bottom)
    pPr.append(pBdr)


def add_left_border(paragraph, color="2E74B5", sz=18):
    """Adds a left accent border (used for callout / tip boxes)."""
    pPr = paragraph._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    left = OxmlElement("w:left")
    left.set(qn("w:val"), "single")
    left.set(qn("w:sz"), str(sz))
    left.set(qn("w:space"), "8")
    left.set(qn("w:color"), color)
    pBdr.append(left)
    pPr.append(pBdr)


def shade_paragraph(paragraph, hex_color):
    pPr = paragraph._p.get_or_add_pPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hex_color)
    pPr.append(shd)


def set_run(run, text=None, bold=False, italic=False, size=11, color=None,
            font="Calibri", caps=False):
    if text is not None:
        run.text = text
    run.bold = bold
    run.italic = italic
    run.font.size = Pt(size)
    run.font.name = font
    if color is not None:
        run.font.color.rgb = color
    if caps:
        run.font.all_caps = True
    return run


# ---------------------------------------------------------------------------
# Variable-name helper for PLAIN (non-OMML) narrative text such as callouts,
# notes, and problem statements.
#
# The Unicode "subscript small letter o" (U+2092) used for v-sub-o etc. is
# unreliably rendered by common fonts (it can fall back to a glyph that
# looks like a degree sign). To guarantee correct, font-independent
# rendering of variable names like "v\u2092" or "x\u2092" inside ordinary
# text runs, this helper writes the base letter as a normal run and the
# subscript letter as a *true* Word subscript run (w:vertAlign="subscript")
# instead of relying on a fragile Unicode code point.
# ---------------------------------------------------------------------------

def add_var_runs(paragraph, base, sub=None, italic=True, bold=False, size=None,
                  color=None, font="Calibri"):
    """Append a variable name (e.g. v, or v with subscript o/1/2) to an
    existing paragraph using real run-level subscript formatting."""
    r1 = paragraph.add_run(base)
    r1.italic = italic
    r1.bold = bold
    r1.font.name = font
    if size is not None:
        r1.font.size = Pt(size)
    if color is not None:
        r1.font.color.rgb = color
    if sub is not None:
        r2 = paragraph.add_run(str(sub))
        r2.italic = italic
        r2.bold = bold
        r2.font.name = font
        if size is not None:
            r2.font.size = Pt(size)
        if color is not None:
            r2.font.color.rgb = color
        r2.font.subscript = True
    return paragraph


_SUBSCRIPT_MAP = {
    "\u2080": "0", "\u2081": "1", "\u2082": "2", "\u2083": "3", "\u2084": "4",
    "\u2085": "5", "\u2086": "6", "\u2087": "7", "\u2088": "8", "\u2089": "9",
    "\u2092": "o",
}


def parse_var_text(text):
    """
    Scans plain narrative text for <letter><unicode-subscript-char> pairs
    (e.g. 'v\u2092', 'x\u2081') and converts them into ('var', base, sub)
    parts, leaving all other text as plain string parts. The returned list
    is ready to pass to add_rich_text(), guaranteeing that subscripted
    variable names render correctly (as true Word subscripts) rather than
    relying on the fragile Unicode subscript glyphs directly in a run.
    """
    parts = []
    buf = ""
    i = 0
    n = len(text)
    while i < n:
        ch = text[i]
        nxt = text[i + 1] if i + 1 < n else ""
        if nxt in _SUBSCRIPT_MAP and (ch.isalpha()):
            if buf:
                parts.append(buf)
                buf = ""
            parts.append(("var", ch, _SUBSCRIPT_MAP[nxt]))
            i += 2
            continue
        buf += ch
        i += 1
    if buf:
        parts.append(buf)
    return parts


def add_rich_text(paragraph, parts, italic=True, size=None, color=None,
                   font="Calibri", bold=False):
    """
    Append a sequence of narrative-text parts to a paragraph, where each
    part is either:
      - a plain string (appended as normal text), or
      - ('var', 'v') / ('var', 'v', 'o')  -> a variable name, optionally with
        a true-subscript letter/number, rendered safely (see add_var_runs).
    This lets callouts/notes mix ordinary prose with inline variable
    references (v, v\u2092, x\u2081, ...) without relying on fragile Unicode
    subscript glyphs.
    """
    for part in parts:
        if isinstance(part, tuple) and part[0] == "var":
            base = part[1]
            sub = part[2] if len(part) > 2 else None
            add_var_runs(paragraph, base, sub, italic=italic, bold=bold,
                         size=size, color=color, font=font)
        else:
            r = paragraph.add_run(part)
            r.italic = italic
            r.bold = bold
            r.font.name = font
            if size is not None:
                r.font.size = Pt(size)
            if color is not None:
                r.font.color.rgb = color
    return paragraph


def add_heading_text(doc, text, size=20, bold=True, color=NAVY, italic=False,
                      alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, space_before=0):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    r = p.add_run(text)
    set_run(r, bold=bold, italic=italic, size=size, color=color)
    return p


def add_plain_text(doc, text, size=11, bold=False, italic=False, color=None,
                    alignment=WD_ALIGN_PARAGRAPH.LEFT, space_after=6, space_before=0):
    p = doc.add_paragraph()
    p.alignment = alignment
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    r = p.add_run(text)
    set_run(r, bold=bold, italic=italic, size=size, color=color)
    return p


def add_shaded_box(doc, paragraphs_builder, bg=SHADE_STATEMENT, border_color="BFBFBF"):
    """
    Creates a single-cell borderless-outside / thin-bordered table that acts
    as a shaded 'card' box (problem statements, callouts). paragraphs_builder
    is a callable that receives the cell and populates it with content.
    """
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, bg)
    set_cell_margins(cell, top=120, bottom=120, left=200, right=200)
    set_table_borders(table, color=border_color, sz=4)
    # remove the default empty paragraph's spacing before adding content
    cell.paragraphs[0].paragraph_format.space_after = Pt(0)
    paragraphs_builder(cell)
    return table


def add_problem_heading(doc, number, title=None):
    text = "Problem %s" % number
    if title:
        text += " \u2014 %s" % title
    p = add_heading_text(doc, text, size=16, bold=True, color=NAVY,
                          space_after=4, space_before=14)
    add_bottom_border(p, color="1F4E79", sz=10)
    return p


def add_section_label(doc, text, color=NAVY, size=12.5):
    return add_heading_text(doc, text, size=size, bold=True, color=color,
                             space_after=4, space_before=10)


def add_callout(doc, lines):
    """A light-blue, left-accented italic callout box for reasoning /
    'Which equation?' notes. `lines` is a list of (prefix_bold, rest_text)
    tuples, or plain strings. Subscript variable references like 'v\u2092'
    in the text are automatically converted to true Word subscripts via
    parse_var_text() for reliable font-independent rendering."""
    def builder(cell):
        p0 = cell.paragraphs[0]
        first = True
        for line in lines:
            p = p0 if first else cell.add_paragraph()
            first = False
            p.paragraph_format.space_after = Pt(2)
            if isinstance(line, tuple):
                bold_part, rest = line
                add_rich_text(p, parse_var_text(bold_part), italic=True,
                              bold=True, size=10.5, color=BLUE_ACCENT)
                add_rich_text(p, parse_var_text(rest), italic=True,
                              size=10.5, color=GRAY_TEXT)
            else:
                add_rich_text(p, parse_var_text(line), italic=True,
                              size=10.5, color=GRAY_TEXT)
    return add_shaded_box(doc, builder, bg=SHADE_CALLOUT, border_color="9DC3E6")



def add_statement_box(doc, text):
    """Light-gray shaded problem-statement box (matches the reference image)."""
    def builder(cell):
        p = cell.paragraphs[0]
        add_rich_text(p, parse_var_text(text), italic=False, size=10.5, color=GRAY_TEXT)
    return add_shaded_box(doc, builder, bg=SHADE_STATEMENT, border_color="BFBFBF")


def add_given_table(doc, rows):
    """rows: list of (symbol_omml_items, value_text, annotation_text)."""
    from omml import oMath, add_inline_math
    n = len(rows)
    table = doc.add_table(rows=n + 1, cols=3)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(table, color="BFBFBF", sz=4)
    hdr = table.rows[0].cells
    for c, htext in zip(hdr, ["Symbol", "Value", "Annotation"]):
        set_cell_shading(c, "1F4E79")
        set_cell_margins(c)
        p = c.paragraphs[0]
        p.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r = p.add_run(htext)
        set_run(r, bold=True, size=10.5, color=RGBColor(0xFF, 0xFF, 0xFF))
    for i, (sym_items, value_text, annot_text) in enumerate(rows, start=1):
        cells = table.rows[i].cells
        for c in cells:
            set_cell_margins(c)
        p0 = cells[0].paragraphs[0]
        p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
        add_inline_math(p0, oMath(*sym_items))
        p1 = cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
        r1 = p1.add_run(value_text)
        set_run(r1, size=10.5)
        p2 = cells[2].paragraphs[0]
        p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
        add_rich_text(p2, parse_var_text(annot_text), italic=False, size=10, color=GRAY_TEXT)
    return table


def add_required_line(doc, parts):
    """parts: list of strings / ('math', omml_items) tuples, one per required
    quantity, rendered as a bulleted-ish stacked list."""
    from omml import oMath, add_inline_math
    for part in parts:
        p = doc.add_paragraph(style=None)
        p.paragraph_format.space_after = Pt(2)
        p.paragraph_format.left_indent = Pt(14)
        if isinstance(part, tuple) and part[0] == "math":
            r = p.add_run("\u2022  ")
            set_run(r, size=11)
            add_inline_math(p, oMath(*part[1]))
        else:
            r = p.add_run("\u2022  ")
            set_run(r, size=11)
            add_rich_text(p, parse_var_text(part), italic=False, size=11)



def add_centered_display_eq(doc, om_items, space_before=4, space_after=4):
    from omml import oMath, add_display_math
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    add_display_math(p, oMath(*om_items))
    return p


def _paint_math_red_bold(om_element):
    """Recursively force every <m:r> math run inside om_element to render
    bold and red, matching the reference solution key's highlighted final
    -answer style (e.g. '= 0 m' shown in bold red)."""
    from omml import _m, _w
    M_R = "{http://schemas.openxmlformats.org/officeDocument/2006/math}r"
    W_RPR = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}rPr"
    W_COLOR = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}color"
    W_B = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}b"
    M_RPR = "{http://schemas.openxmlformats.org/officeDocument/2006/math}rPr"
    for r in om_element.iter(M_R):
        wrpr = r.find(W_RPR)
        if wrpr is None:
            wrpr = OxmlElement("w:rPr")
            # Per spec, if a math <m:rPr> exists it must occur first, and
            # <w:rPr> must come immediately after it (both before <m:t>).
            mrpr = r.find(M_RPR)
            insert_at = 1 if mrpr is not None else 0
            r.insert(insert_at, wrpr)
        # remove any pre-existing color/bold so we don't duplicate
        for tag in (W_COLOR, W_B):
            existing = wrpr.find(tag)
            if existing is not None:
                wrpr.remove(existing)
        b = OxmlElement("w:b")
        wrpr.append(b)
        color = OxmlElement("w:color")
        color.set(qn("w:val"), "C00000")
        wrpr.append(color)
    return om_element


def add_boxed_answer(doc, om_items, space_before=6, space_after=10):
    """Centered final-answer equation highlighted in a red-bordered,
    light-red-shaded box (matches the reference solution key's emphasized
    final-answer style). Implemented as a paragraph border/shading rather
    than relying on per-run color inside the OMML runs, since several
    renderers (including LibreOffice) do not honor w:rPr color/bold set
    inside <m:r> math runs -- the paragraph-level border+shading renders
    reliably everywhere while the equation itself is still real OMML."""
    from omml import oMath, add_display_math
    p = doc.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)

    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    for edge in ("top", "left", "bottom", "right"):
        el = OxmlElement("w:%s" % edge)
        el.set(qn("w:val"), "single")
        el.set(qn("w:sz"), "6")
        el.set(qn("w:space"), "6")
        el.set(qn("w:color"), "C00000")
        pBdr.append(el)
    pPr.append(pBdr)
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), "FDF2F2")
    pPr.append(shd)

    om = oMath(*om_items)
    _paint_math_red_bold(om)  # best-effort: also honored by Word itself
    add_display_math(p, om)
    return p


def add_note(doc, text, size=10, color=None, italic=True, space_after=8):
    if color is None:
        color = GRAY_TEXT
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(space_after)
    add_rich_text(p, parse_var_text(text), italic=italic, size=size, color=color)
    return p
