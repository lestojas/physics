"""Rendering engine: helpers to build styled slides on the template."""
import copy
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn
from PIL import Image

# ---- palette ----
ORANGE = RGBColor(0xF9, 0x77, 0x0B)
ORANGE_D = RGBColor(0xC8, 0x5A, 0x00)
DARK = RGBColor(0x26, 0x26, 0x26)
TITLE_CLR = RGBColor(0x1A, 0x1A, 0x1A)
GREY = RGBColor(0x6E, 0x6E, 0x6E)
WHITE = RGBColor(0xFF, 0xFF, 0xFF)
LIGHT = RGBColor(0xFD, 0xF1, 0xE6)   # very light orange for callouts / bands
LIGHTER = RGBColor(0xFB, 0xEA, 0xD9)
ROW_ALT = RGBColor(0xFB, 0xF3, 0xEC)

FONT = "TT Hoves"
FONT_BOLD = "TT Hoves ExtraBold"

# content region (inches)
CL = 0.76
CW = 11.80
CT = 1.85
CB = 6.75

EMU_IN = 914400


# ------------------------------------------------------------------ #
#  Slide duplication / cleanup
# ------------------------------------------------------------------ #
def duplicate_slide(prs, src_slide):
    layout = src_slide.slide_layout
    new_slide = prs.slides.add_slide(layout)
    for shp in list(new_slide.shapes):
        shp._element.getparent().remove(shp._element)
    for shp in src_slide.shapes:
        new_slide.shapes._spTree.append(copy.deepcopy(shp._element))
    return new_slide


def find_shape(slide, name):
    for s in slide.shapes:
        if s.name == name:
            return s
    return None


def delete_sldIds(prs, sldId_elements):
    lst = prs.slides._sldIdLst
    for el in sldId_elements:
        lst.remove(el)


# ------------------------------------------------------------------ #
#  Run / paragraph helpers
# ------------------------------------------------------------------ #
def _baseline(run, val):
    rPr = run._r.get_or_add_rPr()
    rPr.set("baseline", str(val))


def add_seg(paragraph, seg, size, color, font=FONT):
    """seg = (kind, text). kind: t,b,i,bi,var,sub,sup,subi,supi,bt(bold)"""
    kind, text = seg
    r = paragraph.add_run()
    r.text = text
    f = r.font
    f.name = font
    f.size = Pt(size)
    f.color.rgb = color
    if kind in ("b", "bt", "bi"):
        f.bold = True
    if kind in ("i", "bi", "var", "subi", "supi"):
        f.italic = True
    if kind in ("sub", "subi"):
        _baseline(r, -25000)
        f.size = Pt(size * 0.92)
    if kind in ("sup", "supi"):
        _baseline(r, 30000)
        f.size = Pt(size * 0.92)
    return r


def parse_inline(text):
    """Return list of (bold, italic, chunk) parsing ***, **, *."""
    runs = []
    buf = ""
    bold = ital = False
    i, n = 0, len(text)

    def flush():
        nonlocal buf
        if buf:
            runs.append((bold, ital, buf))
            buf = ""

    while i < n:
        if text[i:i+3] == "***":
            flush(); bold = not bold; ital = not ital; i += 3
        elif text[i:i+2] == "**":
            flush(); bold = not bold; i += 2
        elif text[i] == "*":
            flush(); ital = not ital; i += 1
        else:
            buf += text[i]; i += 1
    flush()
    return runs


def set_bullet(paragraph, color=ORANGE, char="\u2022"):
    pPr = paragraph._p.get_or_add_pPr()
    pPr.set("marL", "320040")
    pPr.set("indent", "-320040")
    buClr = pPr.makeelement(qn("a:buClr"), {})
    srgb = pPr.makeelement(qn("a:srgbClr"), {"val": "%02X%02X%02X" % (color[0], color[1], color[2])})
    buClr.append(srgb)
    buFont = pPr.makeelement(qn("a:buFont"), {"typeface": "Arial"})
    buChar = pPr.makeelement(qn("a:buChar"), {"char": char})
    pPr.append(buClr); pPr.append(buFont); pPr.append(buChar)


def no_bullet(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    pPr.append(pPr.makeelement(qn("a:buNone"), {}))


# ------------------------------------------------------------------ #
#  Title
# ------------------------------------------------------------------ #
def set_title(slide, text):
    tb = find_shape(slide, "TextBox 9")
    tb.left = Inches(CL); tb.top = Inches(0.46)
    tb.width = Inches(CW); tb.height = Inches(1.12)
    tf = tb.text_frame
    tf.word_wrap = True
    # clear existing paragraphs
    for p in list(tf.paragraphs)[1:]:
        p._p.getparent().remove(p._p)
    p = tf.paragraphs[0]
    for r in list(p.runs):
        r._r.getparent().remove(r._r)
    size = 30 if len(text) <= 46 else 25
    r = p.add_run(); r.text = text
    r.font.name = FONT_BOLD; r.font.size = Pt(size); r.font.color.rgb = TITLE_CLR
    r.font.bold = True
    # accent bar under title
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(CL+0.02), Inches(1.62),
                                 Inches(1.05), Inches(0.075))
    bar.fill.solid(); bar.fill.fore_color.rgb = ORANGE
    bar.line.fill.background()
    bar.shadow.inherit = False
    return tb


def remove_body(slide):
    b = find_shape(slide, "TextBox 8")
    if b is not None:
        b._element.getparent().remove(b._element)


# ------------------------------------------------------------------ #
#  Bulleted text block
# ------------------------------------------------------------------ #
def add_bullets(slide, items, left, top, width, height, size=18, gap=8,
                line_spacing=1.03):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(height))
    tf = tb.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.TOP
    first = True
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.LEFT
        p.line_spacing = line_spacing
        p.space_after = Pt(gap)
        p.space_before = Pt(0)
        set_bullet(p)
        for (b, it, chunk) in parse_inline(item):
            kind = "bi" if (b and it) else "b" if b else "i" if it else "t"
            add_seg(p, (kind, chunk), size, DARK)
    return tb


# ------------------------------------------------------------------ #
#  Equation band
# ------------------------------------------------------------------ #
def add_equation(slide, seg_lines, top, size=25, width=8.6, height=None,
                 left=None):
    if height is None:
        height = 0.62 + 0.55 * len(seg_lines)
    if left is None:
        left = CL + (CW - width) / 2.0
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left),
                                 Inches(top), Inches(width), Inches(height))
    box.fill.solid(); box.fill.fore_color.rgb = LIGHT
    box.line.color.rgb = ORANGE; box.line.width = Pt(1.25)
    box.shadow.inherit = False
    # round corner smaller
    try:
        box.adjustments[0] = 0.10
    except Exception:
        pass
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_top = Pt(4); tf.margin_bottom = Pt(4)
    first = True
    for line in seg_lines:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.alignment = PP_ALIGN.CENTER
        no_bullet(p)
        for seg in line:
            add_seg(p, seg, size, ORANGE_D)
    return box


# ------------------------------------------------------------------ #
#  Callout box (quote / boundary / workaround)
# ------------------------------------------------------------------ #
def add_callout(slide, items, top, left=CL, width=CW, size=17, height=None,
                accent=ORANGE):
    if height is None:
        height = 0.55 + 0.42 * sum(max(1, len(i)//95 + 1) for i in items)
    box = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, Inches(left),
                                 Inches(top), Inches(width), Inches(height))
    box.fill.solid(); box.fill.fore_color.rgb = LIGHTER
    box.line.fill.background()
    box.shadow.inherit = False
    try:
        box.adjustments[0] = 0.06
    except Exception:
        pass
    # left accent bar
    bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(left), Inches(top),
                                 Inches(0.09), Inches(height))
    bar.fill.solid(); bar.fill.fore_color.rgb = accent
    bar.line.fill.background(); bar.shadow.inherit = False
    tf = box.text_frame
    tf.word_wrap = True
    tf.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf.margin_left = Pt(16); tf.margin_right = Pt(12)
    tf.margin_top = Pt(6); tf.margin_bottom = Pt(6)
    first = True
    for item in items:
        p = tf.paragraphs[0] if first else tf.add_paragraph()
        first = False
        p.line_spacing = 1.03
        p.space_after = Pt(4)
        no_bullet(p)
        for (b, it, chunk) in parse_inline(item):
            kind = "bi" if (b and it) else "b" if b else "i" if it else "t"
            add_seg(p, (kind, chunk), size, DARK)
    return box


# ------------------------------------------------------------------ #
#  Table
# ------------------------------------------------------------------ #
def _fill_cell(cell, content, size, color, bold=False, align=PP_ALIGN.LEFT):
    cell.margin_left = Pt(9); cell.margin_right = Pt(9)
    cell.margin_top = Pt(5); cell.margin_bottom = Pt(5)
    cell.vertical_anchor = MSO_ANCHOR.MIDDLE
    tf = cell.text_frame
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.alignment = align
    if isinstance(content, list):   # list of segments (equations)
        for seg in content:
            add_seg(p, seg, size, color)
    else:
        for (b, it, chunk) in parse_inline(content):
            kind = "bi" if (b and (it or bold)) else "b" if (b or bold) else "i" if it else "t"
            add_seg(p, (kind, chunk), size, color)


def add_table(slide, header, rows, left, top, width, col_widths, size=16,
              header_size=17, row_height=0.5, first_col_bold=True):
    ncols = len(col_widths)
    nrows = len(rows) + (1 if header else 0)
    gf = slide.shapes.add_table(nrows, ncols, Inches(left), Inches(top),
                                Inches(width), Inches(row_height * nrows))
    tbl = gf.table
    # disable default banded style
    tbl.first_row = bool(header)
    tbl.horz_banding = False
    for ci, w in enumerate(col_widths):
        tbl.columns[ci].width = Inches(w)
    r0 = 0
    if header:
        for ci, h in enumerate(header):
            c = tbl.cell(0, ci)
            c.fill.solid(); c.fill.fore_color.rgb = ORANGE
            _fill_cell(c, h, header_size, WHITE, bold=True,
                       align=PP_ALIGN.LEFT if ci == 0 else PP_ALIGN.LEFT)
        r0 = 1
    for ri, row in enumerate(rows):
        bg = WHITE if ri % 2 == 0 else ROW_ALT
        for ci, val in enumerate(row):
            c = tbl.cell(ri + r0, ci)
            c.fill.solid(); c.fill.fore_color.rgb = bg
            bold = first_col_bold and ci == 0
            clr = ORANGE_D if bold else DARK
            _fill_cell(c, val, size, clr, bold=bold)
    return gf


# ------------------------------------------------------------------ #
#  Image fit
# ------------------------------------------------------------------ #
def add_image_fit(slide, path, left, top, box_w, box_h, align="center", valign="middle"):
    with Image.open(path) as im:
        iw, ih = im.size
    ar = iw / ih
    box_ar = box_w / box_h
    if ar > box_ar:
        w = box_w; h = box_w / ar
    else:
        h = box_h; w = box_h * ar
    if align == "center":
        x = left + (box_w - w) / 2
    elif align == "left":
        x = left
    else:
        x = left + (box_w - w)
    if valign == "middle":
        y = top + (box_h - h) / 2
    elif valign == "top":
        y = top
    else:
        y = top + (box_h - h)
    return slide.shapes.add_picture(path, Inches(x), Inches(y), Inches(w), Inches(h))


def add_caption(slide, text, left, top, width, size=12):
    tb = slide.shapes.add_textbox(Inches(left), Inches(top), Inches(width), Inches(0.3))
    tf = tb.text_frame; tf.word_wrap = True
    p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER
    no_bullet(p)
    r = p.add_run(); r.text = text
    r.font.name = FONT; r.font.size = Pt(size); r.font.italic = True
    r.font.color.rgb = GREY
    return tb


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text
