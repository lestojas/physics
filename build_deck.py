#!/usr/bin/env python3
"""
Generate a modern, visually appealing PowerPoint deck from the lecture PDF:
"Ethical & Effective Use of AI in Literature Review" (Milestone 2.1).

Design goals:
- 16:9 widescreen, clean light theme with a navy/teal/amber accent system
- Body text kept in the ~24-28pt range for readability
- Reusable layout helpers: title slides, section dividers, bullet lists,
  numbered lists, cards, callouts, do/don't columns, tables, and prompt boxes.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.oxml.ns import qn

# ----------------------------------------------------------------------------
# Theme
# ----------------------------------------------------------------------------
INK      = RGBColor(0x0F, 0x2A, 0x43)   # deep navy
INK2     = RGBColor(0x14, 0x39, 0x5C)   # navy 2
TEAL     = RGBColor(0x16, 0xB8, 0xA6)   # accent teal
TEAL_DK  = RGBColor(0x0E, 0x8C, 0x7E)
AMBER    = RGBColor(0xF5, 0xA6, 0x23)   # warning / callout
CORAL    = RGBColor(0xE4, 0x57, 0x2E)   # don't
GREEN    = RGBColor(0x2F, 0x9E, 0x6E)   # do
BG       = RGBColor(0xF4, 0xF7, 0xFA)   # light page background
CARD     = RGBColor(0xFF, 0xFF, 0xFF)
CARD_ALT = RGBColor(0xEC, 0xF2, 0xF7)
TEXT     = RGBColor(0x22, 0x2E, 0x3C)   # main body text
MUTED    = RGBColor(0x5C, 0x6B, 0x7A)
WHITE    = RGBColor(0xFF, 0xFF, 0xFF)
CODEBG   = RGBColor(0x0C, 0x22, 0x38)   # dark prompt box
CODEFG   = RGBColor(0xCF, 0xE9, 0xE4)   # light mono text

HEAD_FONT = "Segoe UI Semibold"
BODY_FONT = "Segoe UI"
MONO_FONT = "Consolas"

EMU = 914400
SW, SH = 13.333, 7.5

prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]

TOTAL_PLACEHOLDER = "TOTAL"  # replaced after all slides built
slide_count = 0


# ----------------------------------------------------------------------------
# Low-level helpers
# ----------------------------------------------------------------------------
def _set_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color
    shape.line.fill.background()


def _no_shadow(shape):
    # remove the default preset shadow python-pptx applies to autoshapes
    sp = shape._element.spPr
    existing = sp.find(qn('a:effectLst'))
    if existing is None:
        sp.append(sp.makeelement(qn('a:effectLst'), {}))


def rect(slide, x, y, w, h, color, rounded=False, line=None, line_w=None):
    shp_type = MSO_SHAPE.ROUNDED_RECTANGLE if rounded else MSO_SHAPE.RECTANGLE
    shp = slide.shapes.add_shape(shp_type, Inches(x), Inches(y), Inches(w), Inches(h))
    if color is None:
        shp.fill.background()
    else:
        shp.fill.solid()
        shp.fill.fore_color.rgb = color
    if line is None:
        shp.line.fill.background()
    else:
        shp.line.color.rgb = line
        shp.line.width = Pt(line_w or 1)
    _no_shadow(shp)
    if rounded:
        try:
            shp.adjustments[0] = 0.06
        except Exception:
            pass
    return shp


def bg(slide, color=BG):
    rect(slide, -0.06, -0.06, SW + 0.12, SH + 0.12, color)


def txt(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, align=PP_ALIGN.LEFT, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    tf.paragraphs[0].alignment = align
    return tf


def run(p, text, size, color=TEXT, bold=False, italic=False, font=BODY_FONT):
    r = p.add_run()
    r.text = text
    r.font.size = Pt(size)
    r.font.color.rgb = color
    r.font.bold = bold
    r.font.italic = italic
    r.font.name = font
    return r


def para(tf, first=False):
    if first and not tf.paragraphs[0].runs:
        return tf.paragraphs[0]
    return tf.add_paragraph()


def new_slide():
    global slide_count
    s = prs.slides.add_slide(BLANK)
    slide_count += 1
    bg(s)
    return s


# ----------------------------------------------------------------------------
# Shared chrome (title header + footer)
# ----------------------------------------------------------------------------
def footer(slide):
    rect(slide, 0, SH - 0.34, SW, 0.34, INK)
    tf = txt(slide, 0.55, SH - 0.37, 8.5, 0.34, anchor=MSO_ANCHOR.MIDDLE)
    p = tf.paragraphs[0]
    run(p, "Milestone 2.1", 10.5, TEAL, bold=True)
    run(p, "   ·   Ethical & Effective Use of AI in Literature Review", 10.5, RGBColor(0xC7, 0xD3, 0xDE))
    tf2 = txt(slide, SW - 2.05, SH - 0.37, 1.5, 0.34, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
    run(tf2.paragraphs[0], f"{slide_count} / {TOTAL_PLACEHOLDER}", 10.5,
        RGBColor(0xC7, 0xD3, 0xDE))


def header(slide, kicker, title, title_size=32):
    # left accent bar
    rect(slide, 0, 0, 0.22, SH, TEAL)
    # kicker / eyebrow
    tf = txt(slide, 0.7, 0.42, 11.8, 0.4)
    run(tf.paragraphs[0], kicker.upper(), 13, TEAL_DK, bold=True)
    # title
    tf2 = txt(slide, 0.7, 0.78, 12.0, 1.0)
    run(tf2.paragraphs[0], title, title_size, INK, bold=True, font=HEAD_FONT)
    # underline accent
    rect(slide, 0.72, 1.62, 1.5, 0.06, AMBER)
    footer(slide)


# ----------------------------------------------------------------------------
# Slide builders
# ----------------------------------------------------------------------------
def title_slide():
    s = new_slide()
    rect(s, -0.06, -0.06, SW + 0.12, SH + 0.12, INK)
    # decorative bands
    rect(s, 0, 0, SW, 0.18, TEAL)
    rect(s, 0, SH - 0.18, SW, 0.18, AMBER)
    # big soft circles
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(9.6), Inches(-1.6), Inches(5.2), Inches(5.2))
    _set_fill(c, INK2); _no_shadow(c)
    c2 = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(11.2), Inches(3.6), Inches(3.6), Inches(3.6))
    _set_fill(c2, RGBColor(0x10, 0x30, 0x4C)); _no_shadow(c2)

    # eyebrow chip
    chip = rect(s, 0.9, 1.15, 3.5, 0.5, TEAL, rounded=True)
    ctf = chip.text_frame; ctf.word_wrap = True
    ctf.paragraphs[0].alignment = PP_ALIGN.CENTER
    run(ctf.paragraphs[0], "MILESTONE 2.1  ·  LECTURE", 12.5, INK, bold=True)

    tf = txt(s, 0.9, 1.95, 9.6, 2.4)
    p = tf.paragraphs[0]
    run(p, "Ethical & Effective Use of AI", 44, WHITE, bold=True, font=HEAD_FONT)
    p2 = tf.add_paragraph()
    run(p2, "in Literature Review", 44, TEAL, bold=True, font=HEAD_FONT)

    tf2 = txt(s, 0.92, 4.35, 9.4, 0.6)
    run(tf2.paragraphs[0], "Using Gemini Notebook (NotebookLM) for Milestone 2.1",
        20, RGBColor(0xD7, 0xE2, 0xEC), bold=True)

    # tagline callout
    bar = rect(s, 0.9, 5.25, 9.5, 0.95, INK2, rounded=True)
    rect(s, 0.9, 5.25, 0.12, 0.95, AMBER)
    ttf = txt(s, 1.25, 5.36, 8.9, 0.75, anchor=MSO_ANCHOR.MIDDLE)
    run(ttf.paragraphs[0], "AI as your synthesis partner \u2014 never your source finder.",
        20, WHITE, italic=True)


def section_divider(number, title, subtitle=None):
    s = new_slide()
    rect(s, -0.06, -0.06, SW + 0.12, SH + 0.12, INK)
    rect(s, 0, 0, 0.28, SH, TEAL)
    rect(s, 0, SH - 0.18, SW, 0.18, AMBER)
    # big ghost number
    tfn = txt(s, 8.7, 0.6, 4.4, 4.0, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.RIGHT)
    run(tfn.paragraphs[0], number, 200, INK2, bold=True, font=HEAD_FONT)

    tf = txt(s, 1.0, 2.28, 8.2, 0.5)
    run(tf.paragraphs[0], "SECTION", 15, TEAL, bold=True)
    rect(s, 1.02, 2.74, 1.4, 0.06, AMBER)  # accent bar above the title
    tf2 = txt(s, 1.0, 2.94, 8.4, 1.9)
    run(tf2.paragraphs[0], title, 40, WHITE, bold=True, font=HEAD_FONT)
    if subtitle:
        tf3 = txt(s, 1.02, 4.85, 8.0, 1.2)
        run(tf3.paragraphs[0], subtitle, 19, RGBColor(0xC7, 0xD3, 0xDE), italic=True)
    footer(s)


def bullets_slide(kicker, title, items, cols=1, size=24, icon="\u2022", icon_color=TEAL):
    """items: list of (text, bold_bool) or strings. Supports optional sub bullets via
    tuples of ('sub', text)."""
    s = new_slide()
    header(s, kicker, title)
    top = 2.0
    if cols == 1:
        _bullet_block(s, items, 0.9, top, 11.6, size, icon, icon_color)
    else:
        half = (len(items) + 1) // 2
        _bullet_block(s, items[:half], 0.9, top, 5.7, size, icon, icon_color)
        _bullet_block(s, items[half:], 6.85, top, 5.7, size, icon, icon_color)
    return s


def _bullet_block(slide, items, x, y, w, size, icon, icon_color):
    tf = txt(slide, x, y, w, SH - y - 0.6)
    first = True
    for it in items:
        p = para(tf, first); first = False
        p.space_after = Pt(11)
        p.line_spacing = 1.05
        if isinstance(it, tuple) and it[0] == 'sub':
            p.level = 1
            run(p, "\u2013   ", size - 3, MUTED, bold=True)
            run(p, it[1], size - 3, MUTED)
        else:
            text, bold = (it if isinstance(it, tuple) else (it, False))
            run(p, icon + "   ", size, icon_color, bold=True)
            run(p, text, size, TEXT, bold=bold)


def numbered_slide(kicker, title, items, cols=1, size=24, note=None):
    s = new_slide()
    header(s, kicker, title)
    top = 2.0
    avail_h = (SH - top - (0.7 if note else 0.55))
    if cols == 1:
        _numbered_block(s, items, 0.9, top, 11.6, size, start=1)
    else:
        half = (len(items) + 1) // 2
        _numbered_block(s, items[:half], 0.9, top, 5.7, size, start=1)
        _numbered_block(s, items[half:], 6.85, top, 5.7, size, start=half + 1)
    if note:
        nb = rect(s, 0.9, SH - 1.05, 11.6, 0.6, CARD_ALT, rounded=True)
        rect(s, 0.9, SH - 1.05, 0.1, 0.6, AMBER)
        ntf = txt(s, 1.2, SH - 1.02, 11.1, 0.55, anchor=MSO_ANCHOR.MIDDLE)
        run(ntf.paragraphs[0], note, 15.5, INK2, italic=True)
    return s


def _numbered_block(slide, items, x, y, w, size, start=1):
    tf = txt(slide, x, y, w, SH - y - 0.6)
    first = True
    for i, it in enumerate(items):
        text = it if isinstance(it, str) else it[0]
        italic = isinstance(it, tuple) and len(it) > 1 and it[1] == 'i'
        p = para(tf, first); first = False
        p.space_after = Pt(10)
        p.line_spacing = 1.05
        run(p, f"{start + i}   ", size, TEAL_DK, bold=True)
        run(p, text, size, TEXT, italic=italic)


def cards_slide(kicker, title, cards, size=18, accent_cycle=(TEAL, AMBER, INK2)):
    """cards: list of (heading, body, big_label)"""
    s = new_slide()
    header(s, kicker, title)
    n = len(cards)
    gap = 0.4
    total_w = 11.9
    cw = (total_w - gap * (n - 1)) / n
    x = 0.75
    y = 2.15
    ch = 4.4
    for i, (head, body, big) in enumerate(cards):
        acc = accent_cycle[i % len(accent_cycle)]
        card = rect(s, x, y, cw, ch, CARD, rounded=True, line=RGBColor(0xE0,0xE7,0xEE), line_w=1)
        rect(s, x, y, cw, 0.14, acc)
        # big label circle
        circ = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(x + 0.3), Inches(y + 0.4),
                                  Inches(0.95), Inches(0.95))
        _set_fill(circ, acc); _no_shadow(circ)
        ctf = circ.text_frame; ctf.word_wrap = True
        ctf.paragraphs[0].alignment = PP_ALIGN.CENTER
        run(ctf.paragraphs[0], big, 22, WHITE, bold=True, font=HEAD_FONT)
        htf = txt(s, x + 0.3, y + 1.55, cw - 0.6, 0.9)
        run(htf.paragraphs[0], head, 20, INK, bold=True, font=HEAD_FONT)
        btf = txt(s, x + 0.3, y + 2.45, cw - 0.6, ch - 2.6)
        run(btf.paragraphs[0], body, size, MUTED)
        x += cw + gap
    return s


def callout_slide(kicker, title, big_text, sub_items=None, accent=AMBER):
    s = new_slide()
    header(s, kicker, title)
    box = rect(s, 0.9, 2.25, 11.6, 2.15, INK, rounded=True)
    rect(s, 0.9, 2.25, 0.16, 2.15, accent)
    tf = txt(s, 1.35, 2.4, 10.9, 1.85, anchor=MSO_ANCHOR.MIDDLE)
    run(tf.paragraphs[0], big_text, 28, WHITE, bold=True, font=HEAD_FONT)
    if sub_items:
        yy = 4.75
        tf2 = txt(s, 1.0, yy, 11.4, SH - yy - 0.55)
        first = True
        for it in sub_items:
            p = para(tf2, first); first = False
            p.space_after = Pt(10)
            run(p, "\u2022   ", 24, accent, bold=True)
            run(p, it, 24, TEXT)
    return s


def do_dont_slide():
    s = new_slide()
    header(s, "Ethical Ground Rules", "Do's and Don'ts")
    dos = [
        "Upload only sources you personally found and read",
        "Ask AI to summarize, organize, and spot patterns",
        "Click every citation and verify it against the original PDF",
        "Rewrite AI output in your own words before submitting",
        "Tell your teacher when and how you used AI, if required",
    ]
    donts = [
        "Ask AI to \u201cfind,\u201d \u201crecommend,\u201d or \u201csuggest\u201d new sources",
        "Paste raw AI output straight into your final paper",
        "Trust a synthesis without opening the original source",
        "Let AI decide your final research gap for you",
        "Upload full texts you don't have the right to share",
    ]
    _dd_col(s, 0.75, GREEN, "DO", "check", dos)
    _dd_col(s, 6.9, CORAL, "DON'T", "cross", donts)
    return s


def _line(slide, x1, y1, x2, y2, color, width=3.0):
    from pptx.enum.shapes import MSO_CONNECTOR
    c = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT, Inches(x1), Inches(y1),
                                   Inches(x2), Inches(y2))
    c.line.color.rgb = color
    c.line.width = Pt(width)
    return c


def _dd_col(slide, x, color, head, mark, items):
    w = 5.65
    card = rect(slide, x, 2.1, w, 4.6, CARD, rounded=True, line=RGBColor(0xE0,0xE7,0xEE), line_w=1)
    hb = rect(slide, x, 2.1, w, 0.7, color, rounded=True)
    rect(slide, x, 2.45, w, 0.35, color)  # square off bottom of header
    # draw the check / cross mark in vector lines (guaranteed to render)
    cx, cy = x + 0.42, 2.45
    if mark == "check":
        _line(slide, cx - 0.13, cy, cx - 0.02, cy + 0.13, WHITE, 3.5)
        _line(slide, cx - 0.02, cy + 0.13, cx + 0.2, cy - 0.14, WHITE, 3.5)
    else:
        _line(slide, cx - 0.13, cy - 0.13, cx + 0.15, cy + 0.15, WHITE, 3.5)
        _line(slide, cx + 0.15, cy - 0.13, cx - 0.13, cy + 0.15, WHITE, 3.5)
    htf = txt(slide, x + 0.78, 2.12, w - 0.9, 0.68, anchor=MSO_ANCHOR.MIDDLE)
    run(htf.paragraphs[0], head, 22, WHITE, bold=True, font=HEAD_FONT)
    tf = txt(slide, x + 0.35, 3.0, w - 0.7, 3.55)
    first = True
    for it in items:
        p = para(tf, first); first = False
        p.space_after = Pt(11)
        p.line_spacing = 1.03
        run(p, "\u2022  ", 18, color, bold=True)
        run(p, it, 18, TEXT)


def table_slide():
    s = new_slide()
    header(s, "Roles at a Glance", "Who Does What?")
    rows = [
        ("Task", "AI (NotebookLM)", "You"),
        ("Finding sources", "Never", "Always"),
        ("Reading full sources", "Can't replace this", "Always"),
        ("Summarizing an uploaded source", "First draft", "Verify & rewrite"),
        ("Spotting themes / patterns", "First draft", "Confirm & finalize"),
        ("Deciding the final research gap", "Suggests only", "Final call"),
        ("Drafting review paragraphs", "First draft", "Rewrite in own words"),
        ("Checking citation accuracy", "Flags issues", "Confirms against PDF"),
        ("Formatting APA references", "Format only", "Supplies all data"),
        ("Final wording submitted", "Never as-is", "Always"),
    ]
    left, top, width = 0.75, 2.0, 11.85
    height = 4.9
    tbl_shape = s.shapes.add_table(len(rows), 3, Inches(left), Inches(top),
                                   Inches(width), Inches(height))
    table = tbl_shape.table
    table.columns[0].width = Inches(5.85)
    table.columns[1].width = Inches(3.0)
    table.columns[2].width = Inches(3.0)
    # disable banded styling defaults; we set colors manually
    for r, rowdata in enumerate(rows):
        for c, val in enumerate(rowdata):
            cell = table.cell(r, c)
            cell.margin_left = Inches(0.15)
            cell.margin_right = Inches(0.1)
            cell.margin_top = Inches(0.03)
            cell.margin_bottom = Inches(0.03)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if c == 0 else PP_ALIGN.CENTER
            if r == 0:
                cell.fill.solid(); cell.fill.fore_color.rgb = INK
                run(p, val, 15.5, WHITE, bold=True, font=HEAD_FONT)
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = CARD if r % 2 else CARD_ALT
                if c == 0:
                    run(p, val, 14.5, TEXT, bold=True)
                elif c == 1:
                    col = CORAL if val.lower().startswith(("never","can't")) else MUTED
                    run(p, val, 14, col, bold=("never" in val.lower()))
                else:
                    run(p, val, 14, TEAL_DK, bold=True)
    return s


def prompt_slide(kicker, title, subtitle, prompt_lines, caution=None):
    s = new_slide()
    header(s, kicker, title)
    # subtitle italic
    tf = txt(s, 0.9, 1.78, 11.6, 0.4)
    run(tf.paragraphs[0], subtitle, 17, TEAL_DK, italic=True, bold=True)
    box_top = 2.28
    box_h = SH - box_top - (1.0 if caution else 0.6)
    box = rect(s, 0.9, box_top, 11.6, box_h, CODEBG, rounded=True)
    # little prompt label
    tag = rect(s, 1.15, box_top - 0.0 + 0.18, 1.5, 0.42, TEAL, rounded=True)
    ttf = txt(s, 1.15, box_top + 0.18, 1.5, 0.42, anchor=MSO_ANCHOR.MIDDLE, align=PP_ALIGN.CENTER)
    run(ttf.paragraphs[0], "PROMPT", 12, INK, bold=True)
    # prompt text
    n = len(prompt_lines)
    fsize = 15 if n <= 11 else (13.5 if n <= 15 else 12)
    ptf = txt(s, 1.2, box_top + 0.75, 11.0, box_h - 0.95)
    first = True
    for line in prompt_lines:
        p = para(ptf, first); first = False
        p.line_spacing = 1.08
        run(p, line if line else " ", fsize, CODEFG, font=MONO_FONT)
    if caution:
        cb = rect(s, 0.9, SH - 0.95, 11.6, 0.55, RGBColor(0xFD,0xF1,0xDD), rounded=True)
        rect(s, 0.9, SH - 0.95, 0.1, 0.55, AMBER)
        ctf = txt(s, 1.2, SH - 0.93, 11.1, 0.5, anchor=MSO_ANCHOR.MIDDLE)
        run(ctf.paragraphs[0], "\u26A0  " + caution, 15, RGBColor(0x8A,0x5A,0x08), bold=True)
    return s


def checklist_slide(kicker, title, items):
    s = new_slide()
    header(s, kicker, title)
    top = 2.15
    row_h = (SH - top - 0.6) / len(items)
    box = 0.34
    for i, it in enumerate(items):
        ry = top + i * row_h
        cy = ry + (row_h - box) / 2
        # drawn checkbox (guaranteed to render, no font glyph needed)
        sq = rect(s, 0.95, cy, box, box, WHITE, rounded=True,
                  line=TEAL_DK, line_w=2)
        tf = txt(s, 1.55, ry, 10.9, row_h, anchor=MSO_ANCHOR.MIDDLE)
        run(tf.paragraphs[0], it, 24, TEXT)
    return s


def closing_slide():
    s = new_slide()
    rect(s, -0.06, -0.06, SW + 0.12, SH + 0.12, INK)
    rect(s, 0, 0, SW, 0.18, TEAL)
    rect(s, 0, SH - 0.18, SW, 0.18, AMBER)
    c = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(-1.8), Inches(3.5), Inches(5.0), Inches(5.0))
    _set_fill(c, INK2); _no_shadow(c)
    tf = txt(s, 0.9, 1.7, 11.5, 1.4)
    run(tf.paragraphs[0], "Questions?", 54, WHITE, bold=True, font=HEAD_FONT)
    tf2 = txt(s, 0.92, 3.05, 11.4, 0.6)
    run(tf2.paragraphs[0], "Bring your matrix and review drafts to consultation / office hours.",
        20, RGBColor(0xD7, 0xE2, 0xEC))
    bar = rect(s, 0.9, 4.1, 11.5, 1.15, INK2, rounded=True)
    rect(s, 0.9, 4.1, 0.14, 1.15, AMBER)
    btf = txt(s, 1.3, 4.2, 10.9, 0.95, anchor=MSO_ANCHOR.MIDDLE)
    p = btf.paragraphs[0]
    run(p, "Remember:  ", 26, RGBColor(0xC7,0xD3,0xDE))
    run(p, "You read. You decide. AI organizes.", 26, TEAL, bold=True, font=HEAD_FONT)


# ----------------------------------------------------------------------------
# Build the deck
# ----------------------------------------------------------------------------
title_slide()

numbered_slide("Overview", "Today's Roadmap", [
    "The One Rule for AI + Research",
    "Milestone 2.1 at a glance \u2014 where AI fits",
    "Finding your own literature",
    "Discovery tools: Research Rabbit & Consensus",
    "Meet Gemini Notebook (NotebookLM)",
    "Ethical do's and don'ts",
    "Prompts for building your matrix",
    "Prompts for writing your literature review",
    "Prompts for references & problem statement",
    "Full workflow, pitfalls, and practice",
], cols=2, size=22)

bullets_slide("Learning Objectives", "By the End, You Will Be Able To", [
    "Explain why AI must never find sources for you",
    "Use real databases to locate credible sources",
    "Use Research Rabbit & Consensus to expand a search",
    "Set up a Gemini Notebook for Milestone 2.1",
    "Use ready-made prompts to build your matrix AND draft your review",
    "Verify, revise, and take ownership of every AI-assisted paragraph",
    "Recognize and avoid common AI misuse in research",
], size=23)

callout_slide("The One Rule to Remember", "The One Rule",
              "AI finds patterns in sources YOU already found and read. "
              "AI does NOT find, choose, or invent your sources.",
              ["You = the researcher and reader",
               "AI = the synthesis assistant",
               "A source you haven't personally read doesn't exist for your paper yet"],
              accent=AMBER)

bullets_slide("Your Responsibility", "Why You Must Search Yourself", [
    "It's the actual research skill you're being trained in",
    "AI chat tools can invent fake studies, authors, even DOIs",
    "Only you can judge if a source is credible and fits your IV/DV",
    "Your panel or judges will ask about your sources \u2014 know them firsthand",
], size=25)

numbered_slide("The Big Picture", "Milestone 2.1 at a Glance", [
    "Recap your Title & Variables (100% you)",
    "Build 3 Literature Matrices \u2192 Themes \u2192 Gaps",
    "Combine into ONE Final Research Gap",
    "Write your 5-Part Literature Review",
    "Build your APA Reference List",
    "Draft your Problem Statement",
], cols=2, size=24,
   note="AI can assist in Phases 2, 4, and 5 \u2014 never Phase 1, and never without your verification.")

cards_slide("Recap", "What Are You Searching For?", [
    ("Independent Variable", "At least 10 sources on your IV.", "10+"),
    ("Dependent Variable", "At least 10 sources on your DV.", "10+"),
    ("Both Variables", "At least 5 sources studying both variables together.", "5+"),
])

bullets_slide("Real Databases  ·  1 of 2", "Where to Find Real Research Articles", [
    ("Google Scholar \u2014 scholar.google.com", True),
    ("Semantic Scholar \u2014 semanticscholar.org", True),
    ("ERIC (education topics) \u2014 eric.ed.gov", True),
    ("PubMed / PMC (health & life sciences) \u2014 pubmed.ncbi.nlm.nih.gov", True),
    ("DOAJ (open-access journals) \u2014 doaj.org", True),
], size=24)

bullets_slide("Real Databases  ·  2 of 2", "Where to Find Real Research Articles", [
    ("CORE \u2014 core.ac.uk", True),
    ("BASE \u2014 base-search.net", True),
    ("ResearchGate \u2014 researchgate.net (author-uploaded copies)", True),
    ("SSRN (social science) \u2014 ssrn.com", True),
    ("Philippine E-Journals (PH topics) \u2014 ejournals.ph", True),
], size=24)

bullets_slide("Search Skills", "Smart Search Tips", [
    "Search keywords, not full sentences (e.g., \u201csleep deprivation academic performance\u201d)",
    "Use quotation marks for exact phrases",
    "Filter by year \u2014 last 5\u201310 years, unless it's a classic study",
    "Check the \u201cCited by\u201d count for influence",
    "Confirm it's peer-reviewed, not a blog or opinion piece",
], size=23)

bullets_slide("Discovery Tool", "Expand Your Search: Research Rabbit", [
    "researchrabbit.ai \u2014 free citation-mapping tool",
    "Drop in a \u201cseed\u201d paper you already found and trust",
    "Explore Similar Work, Earlier Work, and Later Work",
    "Save promising results into a Collection to revisit later",
    "You still must open, read, and evaluate everything it suggests",
], size=23)

bullets_slide("Discovery Tool", "Expand Your Search: Consensus", [
    "consensus.app \u2014 AI-powered academic search engine",
    "Ask a yes/no research question \u2192 get a \u201cconsensus meter\u201d from real studies",
    "Use filters (study type, sample size, year) to narrow results",
    "Every result links to the original paper \u2014 always click through and read it",
    "Useful for sanity-checking what the field currently shows",
], size=23)

bullets_slide("Quality Control", "Screen Before You Add a Source", [
    "Is it actually about my IV or DV \u2014 not just adjacent?",
    "Is it recent enough, or a foundational classic?",
    "Is it peer-reviewed or from a credible publisher?",
    "Have I actually opened and read it \u2014 not just the abstract?",
], size=25, icon="?", icon_color=AMBER)

callout_slide("Reality Check", "Still Just Discovery Tools",
              "Research Rabbit and Consensus help you FIND sources faster \u2014 "
              "they do not replace reading the full source.",
              ["Never cite a source using only its AI-generated summary",
               "Download the actual PDF before it goes in your matrix"],
              accent=CORAL)

numbered_slide("Preparation", "Before You Touch Any AI Tool", [
    "Download PDFs of every source you'll use",
    "Sort them into 3 folders: Independent Variable / Dependent Variable / Both",
    "Skim each one yourself \u2014 you should recognize it later",
    "Now you're ready for synthesis",
], size=25)

# ---- Section 2: Synthesis / NotebookLM ----
section_divider("01", "Meet Gemini Notebook (NotebookLM)",
                "Google's AI notebook, built to work only with YOUR sources.")

bullets_slide("The Difference", "What Makes Gemini Notebook Different?", [
    "It only reads the documents you upload \u2014 nothing else",
    "Every answer comes with a clickable citation back to your source",
    "Reduces (but does not eliminate) the risk of made-up information",
    "Built for study and research, not open-ended chat",
], size=24)

bullets_slide("Feature Tour", "Quick Feature Tour", [
    ("Sources panel \u2014 your uploaded PDFs", True),
    ("Chat \u2014 ask questions grounded in those sources", True),
    ("Citations \u2014 click to jump to the exact passage", True),
    ("Notebook guide / FAQ / Briefing doc \u2014 auto-generated overviews", True),
    ("Audio Overview & Mind map \u2014 alternate ways to review your sources", True),
], size=23)

bullets_slide("Privacy", "A Note on Privacy & Files", [
    "Only upload files you have the right to use for schoolwork",
    "Don't upload personal or sensitive information into any source",
    "Follow your school's data & AI-tool policy for what can be uploaded",
    "When unsure, ask your teacher before uploading",
], size=24, icon="!", icon_color=AMBER)

numbered_slide("Setup", "Setting Up Your Notebook for 2.1", [
    "Create a notebook: \u201cMilestone 2.1 \u2013 [Your Topic]\u201d",
    "Upload your Independent Variable PDFs",
    "Upload your Dependent Variable PDFs",
    "Upload your Both-Variables PDFs",
    "Rename each source clearly: Author, Year",
], size=24)

do_dont_slide()
table_slide()

# ---- Section 3: Building the matrix ----
section_divider("02", "Building Your Literature Matrix",
                "Phase 2 prompts \u2014 one row at a time, then themes, then gaps.")

prompt_slide("Template Prompt 1", "Build One Matrix Row",
             "Use after uploading ONE source at a time",
             [
                 'Using ONLY the source I uploaded titled "[source title],"',
                 'extract in my own simple words, based on this source alone:',
                 '',
                 '1. Key Objectives (1\u20132 short paragraphs)',
                 '2. Key Methodology (1\u20132 short paragraphs)',
                 '3. Key Findings (1\u20132 short paragraphs)',
                 '4. Relevance to my study on [Independent Variable]',
                 '   and [Dependent Variable] (1 paragraph)',
                 '',
                 'Give me the exact page or section for each point',
                 'so I can verify it.',
             ])

prompt_slide("Template Prompt 2", "Group Sources Into Themes",
             "Use after uploading all sources for one topic",
             [
                 'Using only the sources I uploaded under [Independent /',
                 'Dependent / Both Variables], look across their Key',
                 'Findings and Key Objectives. Group them into 2\u20134 THEMES',
                 '\u2014 patterns that repeat across multiple sources.',
                 '',
                 'For each theme give me:',
                 '- A short Theme Name',
                 '- The source numbers/titles that support it',
                 '- ONE synthesis sentence on what they say TOGETHER',
                 '- Whether the sources agree or disagree',
                 '',
                 'Show me exactly where in each source you found this.',
             ])

prompt_slide("Template Prompt 3", "Spot the Gap",
             "Use after your themes are grouped for one topic",
             [
                 'Using the themes we identified for [Topic name], answer',
                 'using only my uploaded sources:',
                 '',
                 '1. DISAGREEMENT GAP \u2014 Which theme shows sources with',
                 '   different or opposite results? How do they disagree?',
                 '2. MISSING PIECE GAP \u2014 What population, place, method,',
                 '   or condition is NOT covered by any source?',
                 '3. THEY SAID SO GAP \u2014 Did any source say more research',
                 '   is needed? Quote where it says this.',
                 '',
                 'Point me to the exact source and page for each answer.',
             ])

# ---- Section 4: Writing the review ----
section_divider("03", "Writing Your Literature Review",
                "Phase 4 \u2014 draft theme by theme, then verify every line.")

bullets_slide("Rules Before You Prompt", "Ground Rules for the Review", [
    "Write theme by theme, never source by source",
    "One theme = at least one full paragraph (5\u20138 sentences)",
    "Every (Author, Year) you cite must be in your Reference List",
    "Everything AI drafts here is a starting point, not final text",
], size=25)

prompt_slide("Template Prompt 4", "Introduction Section",
             "Previews the review \u2014 no findings yet",
             [
                 'Write a 2\u20133 sentence Introduction for my literature',
                 'review. It should:',
                 '',
                 '1. State my general topic: [your general topic/title]',
                 '2. Preview what each section covers \u2014 Introduction,',
                 '   literature on [IV], literature on [DV], studies',
                 '   combining both variables, and a closing Summary',
                 '',
                 'Do NOT include findings, themes, or results \u2014 this is',
                 'a map of the review, not an argument. Base it only on',
                 'the topics and themes already in this notebook.',
             ])

prompt_slide("Template Prompt 5", "Topic 1 or Topic 2 Section",
             "Reuse for both your IV and DV sections",
             [
                 'Using my Theme Table for [Independent / Dependent',
                 'Variable], turn EACH theme into its own paragraph:',
                 '',
                 '"Several studies on [variable] have found that [theme]',
                 '(Author, Year; Author, Year). For example, [detail].',
                 'However, [Author, Year] found something different.',
                 'Overall, these studies suggest that [synthesis]."',
                 '',
                 'Rules: one paragraph per theme, 5\u20138 sentences, cite',
                 'at least 2 sources; state agree/disagree; group by',
                 'theme (not by source); use only my uploaded sources.',
                 'This is a DRAFT I will revise before submitting.',
             ])

prompt_slide("Template Prompt 6", "Topic 3 Section (Both Variables)",
             "Focus on the relationship, not either variable alone",
             [
                 'Using my Theme Table for sources that study [IV] and',
                 '[DV] together, write at least one paragraph per theme',
                 '(5\u20138 sentences) using the same sentence frame.',
                 '',
                 'Focus each paragraph on HOW the two variables relate',
                 'to each other. Note any disagreement between the',
                 'combined studies. End the section with 1\u20132 sentences',
                 'on what is still missing \u2014 this should connect to my',
                 'research gap.',
                 '',
                 'Use only my uploaded sources. This is a DRAFT to revise.',
             ])

prompt_slide("Template Prompt 7", "Summary Section",
             "Ties the whole review back to your Final Research Gap",
             [
                 'Using the Theme Names across my IV, DV, and Both-',
                 'Variables sections, and my Final Research Gap',
                 'Statement: "[paste it]" \u2014 draft a Summary that:',
                 '',
                 '1. Names the 2\u20133 themes that matter most across topics',
                 '2. Explains why the field still needs more research,',
                 '   using my Final Research Gap Statement',
                 '3. Explains how my study will specifically fill it',
                 '',
                 'Base this only on my uploaded sources and the theme',
                 'tables already built. This is a DRAFT for me to revise.',
             ])

prompt_slide("Template Prompt 8", "Whole-Review Coherence Check",
             "Run this once all five sections are drafted",
             [
                 'Here is my full literature review draft: [paste].',
                 'Do NOT rewrite my content or add new claims. Just flag:',
                 '',
                 '1. Any ideas repeated across sections',
                 '2. Any paragraph that reads source-by-source instead',
                 '   of theme-by-theme',
                 '3. Any transition that feels abrupt between sections',
                 '',
                 'List the issues by section so I can fix them myself.',
             ])

prompt_slide("Template Prompt 9", "Full-Review Citation Audit",
             "Your last check before submitting the review",
             [
                 'Go through my full literature review draft: [paste].',
                 'For every (Author, Year) citation, confirm:',
                 '',
                 '(a) it appears in a source I uploaded to this notebook',
                 '(b) the claim next to it is actually supported by that',
                 '    source',
                 '',
                 'Flag any citation you cannot verify from my uploaded',
                 'sources \u2014 do not guess or fill in a citation that',
                 "isn't there.",
             ])

# ---- Section 5: References & Problem Statement ----
section_divider("04", "References & Problem Statement",
                "Phases 5\u20136 \u2014 formatting help and building your problem statement.")

prompt_slide("Template Prompt 10", "Reference List Formatting Check",
             "Formatting help only \u2014 never a source of new data",
             [
                 'Here is my reference list draft with Author, Year,',
                 'Title, Source, and page/URL for each entry: [paste].',
                 '',
                 'Using APA 7th edition, check the FORMAT of each entry',
                 'only \u2014 do not add, remove, or change any author, year,',
                 'title, or URL I did not provide.',
                 '',
                 'Flag any entry missing a required APA element (e.g.,',
                 'DOI, issue number, page range) so I can look it up.',
             ],
             caution="Never let AI invent a DOI, page number, or URL it wasn't given.")

prompt_slide("Template Prompt 11", "Problem Statement Components",
             "Draft each component from your own finalized gap",
             [
                 'Using my Final Research Gap Statement: "[paste it]" \u2014',
                 'draft one sentence each for:',
                 '',
                 '1. Background Context \u2014 the broader setting of my topic',
                 '2. Specific Problem or Gap \u2014 based only on my Final',
                 '   Research Gap Statement, not a new gap',
                 '3. Implications \u2014 who is affected if this stays unresolved',
                 '4. Objectives or Aims \u2014 what my study will do about it',
                 '',
                 'Base this only on my research gap and topic \u2014 do not',
                 'introduce new sources or claims.',
             ])

prompt_slide("Template Prompt 12", "Combine Into One Paragraph",
             "Smooth your four sentences into a single paragraph",
             [
                 'Here are my four Problem Statement sentences:',
                 'Background Context: [paste]',
                 'Specific Problem/Gap: [paste]',
                 'Implications: [paste]',
                 'Objectives/Aims: [paste]',
                 '',
                 'Combine them into one smooth paragraph using connecting',
                 'words like "However," "This means that," or "Therefore."',
                 'Do not add new claims or sources \u2014 only combine and',
                 'smooth the sentences I wrote.',
             ])

# ---- Section 6: Workflow, pitfalls, practice ----
section_divider("05", "Workflow, Pitfalls & Practice",
                "Putting it all together \u2014 from search to submission.")

numbered_slide("The Human Step", "After Every Prompt", [
    "Open the cited source \u2014 confirm it says what the AI claims",
    "Rewrite the output in your own voice",
    "Check the tone matches an academic literature review",
    "Only then paste it into your matrix or paper",
], size=25)

bullets_slide("Stay Alert", "Common AI Pitfalls to Watch For", [
    "Fabricated citations, authors, or DOIs that don't exist",
    "Overgeneralized \u201cthemes\u201d that flatten real disagreement",
    "Paragraphs that quietly slip back into source-by-source listing",
    "Confident-sounding claims not actually in your sources",
    "A polished tone that implies more consensus than your sources show",
    "Reference entries AI \u201ccompletes\u201d with wrong page numbers",
], size=22, icon="!", icon_color=CORAL)

numbered_slide("End-to-End", "Full Workflow: Search to Submission", [
    "Search: Google Scholar, ERIC, PubMed, Semantic Scholar, DOAJ",
    "Expand: Research Rabbit & Consensus \u2014 then screen every result",
    "Download & sort PDFs by topic (IV / DV / Both)",
    "Upload to Gemini Notebook (NotebookLM)",
    "Prompts 1\u20133: build your matrix, themes, and topic gaps",
    "Combine into your Final Research Gap Statement (your step)",
    "Prompts 4\u20139: draft, check, and audit your review",
    "Prompt 10: format-check your APA reference list",
    "Prompts 11\u201312: draft and combine your Problem Statement",
    "Final read-through in your own voice before submitting",
], cols=2, size=19)

checklist_slide("Before You Submit", "Revision Checklist", [
    "Every source in my matrix is one I personally found and read",
    "Every theme paragraph is written theme-by-theme, not source-by-source",
    "Every (Author, Year) citation traces to a real, verified source",
    "Every AI-drafted sentence has been rewritten in my own words",
    "My reference list entries match my in-text citations exactly",
    "I disclosed my AI use, if my teacher requires it",
])

bullets_slide("Integrity", "Academic Integrity & Disclosure", [
    "AI-assisted is NOT AI-written: the final words must be yours",
    "Disclose your AI use if your teacher or school requires it",
    "When in doubt about a rule, ask before you submit",
    "Integrity protects the credibility of your research, not just a grade",
], size=24)

numbered_slide("Practice  ·  Activity 1", "Matrix Row", [
    "Pick ONE source you've already found for Topic 1",
    "Upload it to a test Gemini Notebook",
    "Run Template Prompt 1",
    "Compare the AI's summary to the actual PDF \u2014 what's right? What needs fixing?",
], size=24)

numbered_slide("Practice  ·  Activity 2", "Theme Paragraph", [
    "Using your Topic 1 Theme Table, pick ONE theme",
    "Run Template Prompt 5 for that single theme",
    "Rewrite the AI's paragraph in your own words",
    "Trade with a partner: can they verify every citation you used?",
], size=24)

bullets_slide("Discuss", "Discussion Questions", [
    "What's one moment you'd be tempted to just copy AI output as-is?",
    "How would you explain your research gap without reading it off a slide?",
    "If NotebookLM gave you a citation you couldn't find in your source, what would you do next?",
], size=24, icon="?", icon_color=AMBER)

closing_slide()

# ----------------------------------------------------------------------------
# Replace TOTAL placeholder in footers
# ----------------------------------------------------------------------------
total = len(prs.slides._sldIdLst)
for slide in prs.slides:
    for shape in slide.shapes:
        if not shape.has_text_frame:
            continue
        for p in shape.text_frame.paragraphs:
            for r in p.runs:
                if TOTAL_PLACEHOLDER in r.text:
                    r.text = r.text.replace(TOTAL_PLACEHOLDER, str(total))

out = "Ethical_AI_Literature_Review_Milestone_2.1.pptx"
prs.save(out)
print(f"Saved {out} with {total} slides.")
