#!/usr/bin/env python3
"""
Lecture 2: Research Ethics — 16:9 PowerPoint generator.

Modern, water-themed deck (the recurring "Barangay Water Filter Project"
case study inspires an aqua/teal palette). Content is copied verbatim from
the source script; Visual Suggestions are realized as native PPTX graphics;
Speaker Notes are placed in each slide's Notes pane.
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
from pptx.enum.text import MSO_AUTO_SIZE
from pptx.oxml.ns import qn

# ----------------------------------------------------------------------------
# Palette
# ----------------------------------------------------------------------------
INK       = RGBColor(0x21, 0x2A, 0x33)   # near-black body text
MUTED     = RGBColor(0x5B, 0x6B, 0x73)   # secondary text
PAPER     = RGBColor(0xF5, 0xF8, 0xF9)   # slide background
WHITE     = RGBColor(0xFF, 0xFF, 0xFF)
PANEL     = RGBColor(0xFF, 0xFF, 0xFF)
FAINT     = RGBColor(0xE3, 0xEC, 0xEF)   # light panel / outlines
GREYBOX   = RGBColor(0xD9, 0xE2, 0xE6)   # inactive flowchart fill

TEAL      = RGBColor(0x0F, 0x4C, 0x5C)   # primary deep teal
AQUA      = RGBColor(0x2A, 0x9D, 0x8F)   # accent aqua-green
SAND      = RGBColor(0xE9, 0xC4, 0x6A)   # warm sand
SAND_DK   = RGBColor(0xC9, 0x9A, 0x2E)   # darker sand for text on light
CORAL     = RGBColor(0xE7, 0x6F, 0x51)   # coral
BLUE      = RGBColor(0x3A, 0x7C, 0xA5)   # respect blue
PURPLE    = RGBColor(0x6A, 0x4C, 0x93)   # confidentiality purple

# Four core standard colors (reused Slide 6 & 11)
C_HONESTY = AQUA
C_RESPECT = BLUE
C_CONFID  = PURPLE
C_HARM    = CORAL

FONT_H = "Segoe UI Semibold"
FONT_B = "Segoe UI"
FONT_L = "Segoe UI Light"

# Global font scale — bump all text up for readability / to fill the slide.
FSCALE = 1.2


def sp(pt, scale=True):
    """Scaled point size for fonts (spacing values keep using Pt directly)."""
    return Pt(pt * (FSCALE if scale else 1.0))

EMU_IN = 914400
SW = 13.333
SH = 7.5

prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]


# ----------------------------------------------------------------------------
# Low-level helpers
# ----------------------------------------------------------------------------
def _set_fill(shape, color):
    shape.fill.solid()
    shape.fill.fore_color.rgb = color


def _no_line(shape):
    shape.line.fill.background()


def _line(shape, color, width=1.0):
    shape.line.color.rgb = color
    shape.line.width = Pt(width)


def _shadow_off(shape):
    try:
        shape.shadow.inherit = False
    except Exception:
        pass


def rect(slide, x, y, w, h, fill=None, line=None, line_w=1.0,
         shape=MSO_SHAPE.RECTANGLE):
    s = slide.shapes.add_shape(shape, Inches(x), Inches(y), Inches(w), Inches(h))
    _shadow_off(s)
    if fill is None:
        s.fill.background()
    else:
        _set_fill(s, fill)
    if line is None:
        _no_line(s)
    else:
        _line(s, line, line_w)
    return s


def soft_shadow(shape, blur=0.08, dist=0.05, alpha=72000):
    """Add a subtle drop shadow via raw XML."""
    sp = shape._element.spPr
    effLst = sp.find(qn('a:effectLst'))
    if effLst is None:
        effLst = sp.makeelement(qn('a:effectLst'), {})
        sp.append(effLst)
    sh = effLst.makeelement(qn('a:outerShdw'), {
        'blurRad': str(int(blur * EMU_IN)),
        'dist': str(int(dist * EMU_IN)),
        'dir': '5400000', 'rotWithShape': '0'})
    clr = sh.makeelement(qn('a:srgbClr'), {'val': '1F2A33'})
    a = clr.makeelement(qn('a:alpha'), {'val': str(alpha)})
    clr.append(a)
    sh.append(clr)
    effLst.append(sh)


def textbox(slide, x, y, w, h, anchor=MSO_ANCHOR.TOP, wrap=True):
    tb = slide.shapes.add_textbox(Inches(x), Inches(y), Inches(w), Inches(h))
    tf = tb.text_frame
    tf.word_wrap = wrap
    tf.vertical_anchor = anchor
    tf.margin_left = 0
    tf.margin_right = 0
    tf.margin_top = 0
    tf.margin_bottom = 0
    return tb, tf


def para(tf, runs, size=16, color=INK, bold=False, italic=False,
         align=PP_ALIGN.LEFT, before=0, after=6, line=1.06, font=FONT_B,
         first=False, scale=True):
    """runs: str, or list of (text, dict-overrides)."""
    p = tf.paragraphs[0] if first and not tf.paragraphs[0].runs else tf.add_paragraph()
    p.alignment = align
    p.space_before = Pt(before)
    p.space_after = Pt(after)
    try:
        p.line_spacing = line
    except Exception:
        pass
    if isinstance(runs, str):
        runs = [(runs, {})]
    for text, ov in runs:
        r = p.add_run()
        r.text = text
        r.font.size = sp(ov.get("size", size), scale)
        r.font.bold = ov.get("bold", bold)
        r.font.italic = ov.get("italic", italic)
        r.font.name = ov.get("font", font)
        r.font.color.rgb = ov.get("color", color)
    return p


def set_notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# ----------------------------------------------------------------------------
# Slide scaffolding (background, kicker, title)
# ----------------------------------------------------------------------------
SECTIONS = {
    "foundation":  ("FOUNDATIONS OF RESEARCH ETHICS", TEAL),
    "standards":   ("THE FOUR CORE STANDARDS", AQUA),
    "stages":      ("ETHICS ACROSS EVERY STAGE", SAND_DK),
    "bridge":      ("PLAGIARISM: THE ETHICAL BRIDGE", CORAL),
    "citation":    ("CITING SOURCES (APA)", PURPLE),
    "integrate":   ("PUTTING IT ALL TOGETHER", TEAL),
}


def base_slide(section=None):
    slide = prs.slides.add_slide(BLANK)
    rect(slide, -0.1, -0.1, SW + 0.2, SH + 0.2, fill=PAPER)
    return slide


def header(slide, kicker_key, title, num):
    label, accent = SECTIONS[kicker_key]
    # left accent bar
    rect(slide, 0, 0, 0.22, SH, fill=accent)
    # kicker chip
    chip = rect(slide, 0.7, 0.5, 0.34, 0.34, fill=accent, shape=MSO_SHAPE.OVAL)
    _, ktf = textbox(slide, 1.15, 0.44, 9.5, 0.4, anchor=MSO_ANCHOR.MIDDLE)
    para(ktf, [(label, {})], size=12.5, color=accent, bold=True,
         font=FONT_H, after=0, first=True)
    # title (fixed size — kept large but stable so long titles don't wrap)
    _, ttf = textbox(slide, 0.7, 0.86, 12.1, 1.0, anchor=MSO_ANCHOR.TOP)
    para(ttf, title, size=35, color=INK, bold=True, font=FONT_H,
         after=0, first=True, line=1.0, scale=False)
    # underline accent
    rect(slide, 0.72, 1.72, 1.6, 0.07, fill=accent)
    # slide number
    _, ntf = textbox(slide, SW - 1.2, SH - 0.55, 0.9, 0.35,
                     anchor=MSO_ANCHOR.MIDDLE)
    para(ntf, [(f"{num:02d}", {})], size=12, color=MUTED, bold=True,
         align=PP_ALIGN.RIGHT, after=0, first=True, font=FONT_H)
    # footer label
    _, ftf = textbox(slide, 0.7, SH - 0.55, 8.0, 0.35, anchor=MSO_ANCHOR.MIDDLE)
    para(ftf, [("Lecture 2 · Research Ethics", {})], size=10, color=MUTED,
         after=0, first=True)
    return accent


def example_card(slide, x, y, w, h, label, body_runs, accent):
    """A highlighted 'Example' callout with a colored left rail."""
    card = rect(slide, x, y, w, h, fill=WHITE, line=FAINT, line_w=1.0,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.04
    soft_shadow(card, blur=0.07, dist=0.04, alpha=60000)
    rect(slide, x, y, 0.12, h, fill=accent, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    _, tf = textbox(slide, x + 0.32, y + 0.16, w - 0.55, h - 0.3,
                    anchor=MSO_ANCHOR.MIDDLE)
    para(tf, [(label + "  ", {"color": accent, "bold": True, "size": 12.5,
                              "font": FONT_H})], after=4, first=True)
    for rr in body_runs:
        para(tf, rr, size=14.5, color=INK, after=2)
    return card



# ----------------------------------------------------------------------------
# Reusable graphics
# ----------------------------------------------------------------------------
FLOW_STAGES = ["Planning", "Beginning\nthe Study", "Collecting\nData",
               "Analyzing\nData", "Reporting\nResults"]


def flowchart(slide, y, highlight=None, accent=SAND_DK, cx=None, w_total=11.9,
              h=0.95, size=13.5):
    """Five-stage chevron process. `highlight` matches a stage keyword."""
    n = len(FLOW_STAGES)
    overlap = 0.28
    bw = (w_total + overlap * (n - 1)) / n
    x0 = (SW - w_total) / 2 if cx is None else cx
    for i, name in enumerate(FLOW_STAGES):
        x = x0 + i * (bw - overlap)
        shp = MSO_SHAPE.PENTAGON if i == 0 else MSO_SHAPE.CHEVRON
        is_hi = highlight is not None and highlight.lower() in name.lower().replace("\n", " ")
        box = slide.shapes.add_shape(shp, Inches(x), Inches(y),
                                     Inches(bw), Inches(h))
        _shadow_off(box)
        box.adjustments[0] = 0.32
        if is_hi:
            _set_fill(box, accent)
            _no_line(box)
            soft_shadow(box, blur=0.06, dist=0.04, alpha=55000)
            tcol = WHITE
        else:
            _set_fill(box, GREYBOX)
            _no_line(box)
            tcol = MUTED
        tf = box.text_frame
        tf.word_wrap = True
        p = tf.paragraphs[0]
        p.alignment = PP_ALIGN.CENTER
        for j, ln in enumerate(name.split("\n")):
            pp = p if j == 0 else tf.add_paragraph()
            pp.alignment = PP_ALIGN.CENTER
            pp.space_after = Pt(0)
            pp.line_spacing = 1.0
            r = pp.add_run()
            r.text = ln
            r.font.size = sp(size)
            r.font.bold = True
            r.font.name = FONT_H
            r.font.color.rgb = tcol


def styled_table(slide, data, x, y, w, h, col_w=None, header=True,
                 accent=TEAL, fsize=14, hsize=14.5, header_bold=True,
                 align_first_left=True):
    rows, cols = len(data), len(data[0])
    gtbl = slide.shapes.add_table(rows, cols, Inches(x), Inches(y),
                                  Inches(w), Inches(h))
    tbl = gtbl.table
    tbl.first_row = False
    tbl.horz_banding = False
    # strip default style
    tblPr = tbl._tbl.tblPr
    tblPr.set('firstRow', '0')
    tblPr.set('bandRow', '0')
    if col_w:
        for i, cw in enumerate(col_w):
            tbl.columns[i].width = Inches(cw)
    for r in range(rows):
        tbl.rows[r].height = Inches(h / rows)
        for c in range(cols):
            cell = tbl.cell(r, c)
            cell.margin_left = Inches(0.16)
            cell.margin_right = Inches(0.16)
            cell.margin_top = Inches(0.08)
            cell.margin_bottom = Inches(0.08)
            cell.vertical_anchor = MSO_ANCHOR.MIDDLE
            is_head = header and r == 0
            if is_head:
                cell.fill.solid(); cell.fill.fore_color.rgb = accent
            else:
                cell.fill.solid()
                cell.fill.fore_color.rgb = WHITE if r % 2 == 1 else FAINT
            tf = cell.text_frame
            tf.word_wrap = True
            p = tf.paragraphs[0]
            p.alignment = PP_ALIGN.LEFT if (c == 0 and align_first_left) or is_head else PP_ALIGN.LEFT
            val = data[r][c]
            runs = val if isinstance(val, list) else [(val, {})]
            for text, ov in runs:
                rn = p.add_run()
                rn.text = text
                rn.font.size = sp(ov.get("size", hsize if is_head else fsize))
                rn.font.bold = ov.get("bold", header_bold if is_head else False)
                rn.font.italic = ov.get("italic", False)
                rn.font.name = FONT_H if (is_head or ov.get("bold")) else FONT_B
                rn.font.color.rgb = ov.get("color", WHITE if is_head else INK)
    return tbl


def bullets(tf, items, size=17, color=INK, gap=8, bullet_color=None,
            marker="•", first=True):
    for i, it in enumerate(items):
        runs = it if isinstance(it, list) else [(it, {})]
        p = tf.paragraphs[0] if (first and i == 0 and not tf.paragraphs[0].runs) else tf.add_paragraph()
        p.alignment = PP_ALIGN.LEFT
        p.space_after = Pt(gap)
        p.space_before = Pt(0)
        p.line_spacing = 1.08
        m = p.add_run()
        m.text = marker + "  "
        m.font.size = sp(size)
        m.font.bold = True
        m.font.name = FONT_H
        m.font.color.rgb = bullet_color or color
        for text, ov in runs:
            r = p.add_run()
            r.text = text
            r.font.size = sp(ov.get("size", size))
            r.font.bold = ov.get("bold", False)
            r.font.italic = ov.get("italic", False)
            r.font.name = ov.get("font", FONT_B)
            r.font.color.rgb = ov.get("color", color)


def numbered(tf, items, size=17, color=INK, gap=8, num_color=TEAL, first=True):
    for i, it in enumerate(items):
        runs = it if isinstance(it, list) else [(it, {})]
        p = tf.paragraphs[0] if (first and i == 0 and not tf.paragraphs[0].runs) else tf.add_paragraph()
        p.space_after = Pt(gap)
        p.line_spacing = 1.08
        m = p.add_run()
        m.text = f"{i+1}   "
        m.font.size = sp(size)
        m.font.bold = True
        m.font.name = FONT_H
        m.font.color.rgb = num_color
        for text, ov in runs:
            r = p.add_run()
            r.text = text
            r.font.size = sp(ov.get("size", size))
            r.font.bold = ov.get("bold", False)
            r.font.italic = ov.get("italic", False)
            r.font.name = ov.get("font", FONT_B)
            r.font.color.rgb = ov.get("color", color)


def apply_chip(slide, x, y, accent, text="APPLY IT", width=1.6):
    chip = rect(slide, x, y, width, 0.46, fill=accent,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    chip.adjustments[0] = 0.5
    tf = chip.text_frame
    tf.word_wrap = False
    tf.margin_left = Inches(0.1)
    tf.margin_right = Inches(0.1)
    p = tf.paragraphs[0]
    p.alignment = PP_ALIGN.CENTER
    r = p.add_run(); r.text = text
    r.font.size = sp(12.5); r.font.bold = True
    r.font.name = FONT_H; r.font.color.rgb = WHITE
    return chip



# ============================================================================
# COVER
# ============================================================================
s = base_slide()
# layered background
rect(s, -0.1, -0.1, SW + 0.2, SH + 0.2, fill=TEAL)
rect(s, 0, 0, SW, SH, fill=TEAL)
# decorative concentric "ripples" (water motif)
for i, r_in in enumerate([6.4, 5.2, 4.0, 2.8, 1.6]):
    o = s.shapes.add_shape(MSO_SHAPE.OVAL,
                           Inches(SW - r_in/2 - 0.6), Inches(SH - r_in/2 + 0.2),
                           Inches(r_in), Inches(r_in))
    _shadow_off(o); o.fill.background()
    o.line.color.rgb = AQUA if i % 2 == 0 else SAND
    o.line.width = Pt(1.4)
    _lf = o.line._get_or_add_ln()
    a = _lf.makeelement(qn('a:solidFill'), {})
rect(s, 0, 0, 0.28, SH, fill=SAND)
_, tf = textbox(s, 0.95, 1.55, 9.6, 0.5)
para(tf, [("LECTURE 2", {})], size=16, color=SAND, bold=True, font=FONT_H,
     after=0, first=True)
_, tf = textbox(s, 0.9, 2.05, 10.6, 2.4)
para(tf, [("Research Ethics", {})], size=60, color=WHITE, bold=True,
     font=FONT_H, after=2, first=True, line=1.0)
para(tf, [("Doing science honestly — from planning to citation", {})],
     size=21, color=RGBColor(0xCF, 0xE6, 0xE2), italic=True, font=FONT_L, after=0)
# competency + audience pills
py = 4.75
for i, (t) in enumerate([
        "Competency 9 · Apply ethical standards in all stages of research",
        "Competency 10 · Demonstrate proper citation of sources"]):
    pill = rect(s, 0.95, py + i*0.62, 8.6, 0.5, fill=RGBColor(0x14,0x5A,0x6B),
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    pill.adjustments[0] = 0.5
    _, ptf = textbox(s, 1.2, py + i*0.62, 8.2, 0.5, anchor=MSO_ANCHOR.MIDDLE)
    para(ptf, [(t, {})], size=14, color=WHITE, bold=True, font=FONT_H,
         after=0, first=True)
_, tf = textbox(s, 0.98, 6.35, 10, 0.5)
para(tf, [("Grade 12 STEM · Senior High School", {})], size=14,
     color=RGBColor(0x9F,0xC7,0xC2), font=FONT_B, after=0, first=True)
set_notes(s, "Title slide for Lecture 2: Research Ethics. Target competencies: "
             "(9) apply ethical standards in all stages of the research process, and "
             "(10) demonstrate proper citation of sources. Audience: Grade 12 STEM, "
             "Senior High School. The whole lecture is built around one recurring case "
             "study — the Barangay Water Filter Project — so students experience ethics "
             "and citation as a connected story rather than disconnected rules.")

# ============================================================================
# HOW THIS LECTURE WORKS (from 'A Note on Structure' + recurring case study)
# ============================================================================
s = base_slide()
header(s, "foundation", "How This Lecture Works", 0)
_, tf = textbox(s, 0.7, 2.0, 6.05, 4.6)
para(tf, [("One story, start to finish.", {"bold": True, "size": 19,
           "color": TEAL, "font": FONT_H})], after=6, first=True)
para(tf, [("A single recurring case study runs across the whole lecture, so "
           "research ethics and citation feel like a ", {}),
          ("connected story", {"italic": True, "bold": True}),
          (" — not a list of disconnected rules. Reusing it also lowers "
           "cognitive load: no new scenario to learn every few slides.", {})],
     size=15.5, after=12)
para(tf, [("Sources.", {"bold": True, "size": 19, "color": TEAL, "font": FONT_H})],
     after=6)
para(tf, [("Textbook material is drawn from ", {}),
          ("Creswell & Creswell (2023), Research Design, Ch. 4", {"italic": True}),
          (" — the “Ethical Issues” section and Table 4.1. Examples not from "
           "the textbook are labeled ", {}),
          ("Instructor-Created Example", {"bold": True}), (".", {})],
     size=15.5, after=0)
# case study panel
cs = rect(s, 7.0, 2.0, 5.5, 4.55, fill=WHITE, line=FAINT,
          shape=MSO_SHAPE.ROUNDED_RECTANGLE)
cs.adjustments[0] = 0.03
soft_shadow(cs)
rect(s, 7.0, 2.0, 5.5, 0.7, fill=AQUA, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
_, ctf = textbox(s, 7.28, 2.05, 5.0, 0.62, anchor=MSO_ANCHOR.MIDDLE)
para(ctf, [("RECURRING CASE STUDY", {})], size=13, color=WHITE, bold=True,
     font=FONT_H, after=0, first=True)
_, ctf = textbox(s, 7.3, 2.85, 4.95, 3.55)
para(ctf, [("The Barangay Water Filter Project", {"bold": True, "size": 17,
            "color": TEAL, "font": FONT_H})], after=3, first=True)
para(ctf, [("Instructor-Created Example", {"italic": True, "size": 12,
            "color": MUTED})], after=8)
para(ctf, [("Grade 12 STEM researchers test whether a low-cost filter of "
            "coconut-husk charcoal, sand, and gravel can reduce bacterial "
            "contamination in a rural barangay's shared well. They sample "
            "household water before and after filtering, interview residents "
            "about water habits, and compare results to a filter design "
            "published earlier by another student researcher.", {})],
     size=13.5, after=0, line=1.12)
set_notes(s, "A note on structure before you build: this script uses one recurring "
             "case study across the whole lecture so students experience research "
             "ethics and citation as a connected story, not a list of disconnected "
             "rules. Reusing it repeatedly also reduces cognitive load. All "
             "textbook-sourced material is from Creswell & Creswell (2023), Research "
             "Design, Chapter 4 — the 'Ethical Issues' section and Table 4.1. "
             "Examples not found in the textbook are labeled Instructor-Created Example.")

# ============================================================================
# SLIDE 1
# ============================================================================
s = base_slide()
header(s, "foundation", "A Filter, A Village, A Dilemma", 1)
# narrative panel (full-bleed feel)
panel = rect(s, 0.7, 2.0, 7.7, 4.6, fill=WHITE, line=FAINT,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
panel.adjustments[0] = 0.03
soft_shadow(panel)
_, tf = textbox(s, 1.05, 2.3, 7.05, 4.0, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("Grade 12 researchers want to test a homemade water filter in a "
           "rural barangay. Before they collect a single drop of water, they "
           "face questions no data can answer for them:", {})],
     size=16.5, after=10, first=True)
bullets(tf, [
    "Who gets to decide if the community participates?",
    [("What happens if the filter ", {}), ("doesn't", {"italic": True}),
     (" work — do they still report that?", {})],
    "What if their filter design looks a lot like someone else's?",
], size=16, gap=8, bullet_color=AQUA, first=False)
para(tf, [("This is where research ethics begins — before the “research” "
           "even starts.", {"italic": True})], size=16.5, color=TEAL,
     bold=True, after=0)
# visual: illustrated well + filter
vx = 8.75
vp = rect(s, vx, 2.0, 3.8, 4.6, fill=TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
vp.adjustments[0] = 0.03
soft_shadow(vp)
# well
rect(s, vx+0.55, 4.5, 1.3, 1.7, fill=RGBColor(0x2A,0x66,0x74))
rect(s, vx+0.5, 4.35, 1.4, 0.2, fill=SAND)
# water
rect(s, vx+0.7, 4.85, 1.0, 1.3, fill=AQUA)
# roof over well
tri = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(vx+0.35), Inches(3.7),
                         Inches(1.7), Inches(0.7)); _shadow_off(tri); _set_fill(tri, CORAL); _no_line(tri)
# filter tube beside
rect(s, vx+2.35, 3.55, 0.95, 2.65, fill=RGBColor(0xEE,0xF4,0xF3),
     shape=MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s, vx+2.45, 3.75, 0.75, 0.7, fill=INK)          # charcoal
rect(s, vx+2.45, 4.5, 0.75, 0.7, fill=SAND)          # sand
rect(s, vx+2.45, 5.25, 0.75, 0.75, fill=RGBColor(0x8A,0x9A,0xA0))  # gravel
_, vtf = textbox(s, vx+0.2, 2.25, 3.4, 1.0)
para(vtf, [("The well. The filter.", {})], size=15, color=WHITE, bold=True,
     font=FONT_H, after=0, first=True)
para(vtf, [("A tangible object to picture all lecture long.", {})], size=12,
     color=RGBColor(0xBF, 0xDD, 0xD8), italic=True, after=0)
set_notes(s, "Open with this scenario cold — don't define anything yet. The goal is "
             "to let students feel the tension in the questions before you hand them "
             "vocabulary. Ask the class: \"What could go wrong here, even if the "
             "science is done perfectly?\" Let a few students answer. The point you're "
             "building toward is that good science and ethical science are not "
             "automatically the same thing — you can run a flawless experiment and "
             "still cause harm, deceive people, or take credit unfairly. Do not resolve "
             "any of the three bullet questions yet; tell students you'll return to this "
             "exact scenario throughout the lesson.\n\nVisual: a rural well/water source "
             "with a filter setup beside it — grounds the abstract 'ethics' topic in a "
             "tangible object students can picture throughout the lecture.")



# ============================================================================
# SLIDE 2
# ============================================================================
s = base_slide()
header(s, "foundation", "Ethics Is Not One Checklist Item", 2)
_, tf = textbox(s, 0.7, 2.0, 11.9, 1.3)
bullets(tf, [
    [("Many students think “ethics” is something you check ", {}),
     ("once", {"italic": True}), (", at the start of a study.", {})],
    [("In reality, ", {}), ("research ethics", {"bold": True, "color": TEAL}),
     (" applies ", {}), ("continuously", {"bold": True}),
     (" — at every stage of the research process.", {})],
], size=17, gap=8, bullet_color=SAND_DK, first=True)
flowchart(s, y=3.7, highlight=None, accent=SAND_DK)
_, tf = textbox(s, 0.7, 5.05, 11.9, 0.6)
para(tf, [("Every one of these five stages has its own ethical questions.", {})],
     size=16, color=TEAL, italic=True, bold=True, align=PP_ALIGN.CENTER,
     after=0, first=True)
set_notes(s, "This slide reframes a term students already encountered briefly in "
             "Lecture 1 (when weighing 'ethical, social, and environmental factors' for "
             "a proposal). Here, make clear that ethics isn't a single feasibility "
             "checkbox — it's a standard that has to be re-applied at every single stage "
             "of the process. This flowchart previews the structure you'll return to later "
             "in the lecture (Slides 12-16), so tell students explicitly: 'Keep this "
             "five-stage map in your head — we're going to walk through each one.' This is "
             "a structural anchor, not a topic to dwell on yet.\n\nVisual: a horizontal "
             "five-stage process flowchart, kept minimal; it reappears highlighted "
             "stage-by-stage in Slides 12-16 to reinforce continuity.")

# ============================================================================
# SLIDE 3
# ============================================================================
s = base_slide()
header(s, "foundation", "Defining Research Ethics", 3)
# definition callout
defb = rect(s, 0.7, 2.05, 11.9, 1.35, fill=TEAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
defb.adjustments[0] = 0.06
soft_shadow(defb)
_, tf = textbox(s, 1.1, 2.2, 11.1, 1.05, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("Research ethics", {"bold": True, "size": 21, "color": SAND,
           "font": FONT_H}),
          ("  —  the standards and principles that guide ", {"size": 18, "color": WHITE}),
          ("responsible and trustworthy", {"size": 18, "color": WHITE, "italic": True, "bold": True}),
          (" conduct throughout a research study.", {"size": 18, "color": WHITE})],
     after=0, first=True, line=1.1)
_, tf = textbox(s, 0.7, 3.75, 11.9, 0.5)
para(tf, [("Research ethics exists because research almost always involves:", {})],
     size=17, color=INK, after=6, first=True)
_, tf = textbox(s, 1.0, 4.35, 11.4, 1.5)
bullets(tf, [
    [("Collecting data ", {}), ("from", {"bold": True}), (" or ", {}),
     ("about", {"bold": True}), (" people", {})],
    [("Working within real ", {}), ("communities", {"bold": True}),
     (" and ", {}), ("environments", {"bold": True})],
    [("Producing findings that others will ", {}), ("rely on", {"bold": True})],
], size=16.5, gap=9, bullet_color=AQUA, first=True)
_, tf = textbox(s, 0.7, 6.15, 11.9, 0.5)
para(tf, [("Where there are people and consequences, there are ethical "
           "responsibilities.", {})], size=16.5, color=TEAL, italic=True,
     bold=True, align=PP_ALIGN.CENTER, after=0, first=True)
set_notes(s, "Give students a clean, quotable definition here — this is the term "
             "they'll be tested on, so it should be crisp and memorable. Emphasize the "
             "why embedded in the definition: ethics isn't an abstract philosophical "
             "add-on, it exists specifically because research affects real people and real "
             "outcomes. Tie it back to Slide 1: the water filter researchers are dealing "
             "with real households whose water safety may depend on accurate, honest "
             "results. This is a good moment to explicitly note the connection to Lecture "
             "1's competency on 'basic steps in the research process' — ethics governs how "
             "each of those steps is carried out.\n\nVisual: none necessary — a clean, "
             "high-contrast definition slide is more effective than added imagery.")

# ============================================================================
# SLIDE 4
# ============================================================================
s = base_slide()
header(s, "foundation", "Why Research Ethics Matters", 4)
_, tf = textbox(s, 0.7, 1.95, 11.9, 0.5)
para(tf, [("Research ethics protects three things at once:", {})],
     size=17, color=INK, after=0, first=True)
cards = [
    ("The Participants", "Prevents harm, exploitation, and disrespect toward the people involved in a study", C_RESPECT),
    ("The Findings", "Keeps results honest and trustworthy, not distorted by bias or dishonesty", C_HONESTY),
    ("The Researcher's Credibility", "Protects the researcher's — and their institution's — reputation for integrity", TEAL),
]
cw = 3.75; gap = 0.32; x0 = 0.7; cy = 2.7; ch = 3.6
for i, (t, d, col) in enumerate(cards):
    x = x0 + i * (cw + gap)
    card = rect(s, x, cy, cw, ch, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.04
    soft_shadow(card)
    rect(s, x, cy, cw, 1.05, fill=col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    # number badge
    bdg = rect(s, x + cw/2 - 0.35, cy + 1.4, 0.7, 0.7, fill=col, shape=MSO_SHAPE.OVAL)
    _, btf = textbox(s, x + cw/2 - 0.35, cy + 1.4, 0.7, 0.7, anchor=MSO_ANCHOR.MIDDLE)
    para(btf, [(str(i+1), {})], size=22, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
    _, htf = textbox(s, x + 0.2, cy + 0.18, cw - 0.4, 0.75, anchor=MSO_ANCHOR.MIDDLE)
    para(htf, [(t, {})], size=16.5, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True, line=1.0)
    _, dtf = textbox(s, x + 0.28, cy + 2.25, cw - 0.56, 1.2, anchor=MSO_ANCHOR.TOP)
    para(dtf, [(d, {})], size=14, color=INK, align=PP_ALIGN.CENTER, after=0,
         first=True, line=1.12)
set_notes(s, "Walk through each column using the water filter scenario as a running "
             "example: if researchers mislead a household about how their water data will "
             "be used, they harm a participant; if they only report favorable filter "
             "results, they compromise the findings; if either of those things comes to "
             "light later, it damages the researcher's credibility for any future work. "
             "Emphasize that these three protections are interconnected — a violation in "
             "one almost always damages the others too. This slide answers 'why should I "
             "care?' before moving into the specific standards.\n\nVisual: none necessary "
             "— the three-column layout itself is the visual.")

# ============================================================================
# SLIDE 5
# ============================================================================
s = base_slide()
header(s, "foundation", "Who Could Be Affected?", 5)
apply_chip(s, 0.7, 1.95, AQUA)
_, tf = textbox(s, 2.55, 1.98, 10, 0.5, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("Return to the Barangay Water Filter Project.", {"bold": True,
           "size": 16, "color": TEAL})], after=0, first=True)
_, tf = textbox(s, 0.7, 2.65, 11.9, 0.5)
para(tf, [("For each group below, identify ", {"size": 16}),
          ("one specific way", {"bold": True, "size": 16}),
          (" research ethics protects them:", {"size": 16})],
     after=0, first=True)
groups = [
    "The households whose water is being tested",
    "The barangay as a whole community",
    "The original designer of the earlier filter",
    "Future readers who might rely on this research",
]
gy = 3.35; gw = 5.75; gh = 0.92
for i, g in enumerate(groups):
    col = i % 2; row = i // 2
    x = 0.7 + col * (gw + 0.35); y = gy + row * (gh + 0.32)
    b = rect(s, x, y, gw, gh, fill=WHITE, line=FAINT,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    b.adjustments[0] = 0.12
    soft_shadow(b, blur=0.05, dist=0.03, alpha=45000)
    num = rect(s, x + 0.2, y + gh/2 - 0.3, 0.6, 0.6, fill=AQUA, shape=MSO_SHAPE.OVAL)
    _, ntf = textbox(s, x + 0.2, y + gh/2 - 0.3, 0.6, 0.6, anchor=MSO_ANCHOR.MIDDLE)
    para(ntf, [(str(i+1), {})], size=18, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
    _, gtf = textbox(s, x + 1.0, y, gw - 1.2, gh, anchor=MSO_ANCHOR.MIDDLE)
    para(gtf, [(g, {})], size=15, color=INK, after=0, first=True, line=1.05)
_, tf = textbox(s, 0.7, 6.35, 11.9, 0.5)
para(tf, [("Discuss in pairs, then share with the class.", {})],
     size=15.5, color=MUTED, italic=True, align=PP_ALIGN.CENTER, after=0, first=True)
set_notes(s, "This is the lesson's first 'apply it' moment — resist the urge to give "
             "answers immediately. Let pairs work through all four prompts for 3-4 "
             "minutes. Expect students to intuitively identify participant protection (#1) "
             "and community protection (#2) fairly easily; #3 (crediting the earlier "
             "researcher) and #4 (future readers) are usually harder for them to "
             "articulate this early — that's fine, since citation and honest reporting "
             "haven't been formally introduced yet. Use this gap productively: tell "
             "students 'we'll come back to #3 and #4 later in this lesson' to build "
             "anticipation without previewing content.\n\nVisual: none necessary.")



# ============================================================================
# SLIDE 6 — 2x2 matrix
# ============================================================================
s = base_slide()
header(s, "standards", "Four Core Ethical Standards", 6)
quad = [
    ("Honesty & Integrity", "Reporting data and findings truthfully, without fabrication", C_HONESTY),
    ("Respect for Participants", "Informing people they are part of a study and getting their agreement to participate", C_RESPECT),
    ("Confidentiality & Privacy", "Protecting the identity and personal information of participants", C_CONFID),
    ("Avoiding Harm", "Preventing physical, social, or emotional harm to people, communities, and the environment", C_HARM),
]
qw = 5.75; qh = 2.15; x0 = 0.7; y0 = 2.15; gx = 0.35; gy = 0.32
for i, (t, d, col) in enumerate(quad):
    c = i % 2; r = i // 2
    x = x0 + c * (qw + gx); y = y0 + r * (qh + gy)
    card = rect(s, x, y, qw, qh, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.05
    soft_shadow(card)
    rect(s, x, y, 0.16, qh, fill=col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    _, tf = textbox(s, x + 0.42, y + 0.22, qw - 0.7, qh - 0.4)
    para(tf, [(t, {})], size=19, color=col, bold=True, font=FONT_H, after=6,
         first=True)
    para(tf, [(d, {})], size=14.5, color=INK, after=0, line=1.12)
set_notes(s, "This is the 'table of contents' slide for the next four concept slides — "
             "introduce all four principles briefly here, then go deeper one at a time. "
             "Tell students they don't need to memorize the exact wording yet; they'll see "
             "each principle applied to the water filter case individually. The four "
             "principles map roughly onto what professional research communities across "
             "all fields (health, social science, engineering) treat as baseline ethical "
             "standards — you're teaching the shared core, not any one field's specific "
             "code.\n\nVisual: a 2x2 grid/matrix, color-coded by principle so the same four "
             "colors can be reused later (Slide 11) for quick visual recall.")

# ---- Helper for concept + example slides (7-10, 12-15) ----
def concept_example(num, section, title, kind, concept_runs, list_items,
                    example_runs, accent, flow_hi=None, list_marker="•"):
    s = base_slide()
    ac = header(s, section, title, num)
    top = 2.0
    if flow_hi:
        flowchart(s, y=1.95, highlight=flow_hi, accent=SAND_DK, h=0.8, size=12)
        top = 3.05
    _, tf = textbox(s, 0.7, top, 11.9, 1.0)
    para(tf, concept_runs, size=17, color=INK, after=8, first=True, line=1.12)
    ly = top + 0.95
    _, tf2 = textbox(s, 1.0, ly, 11.4, 1.7)
    bullets(tf2, list_items, size=16, gap=7, bullet_color=ac,
            marker=list_marker, first=True)
    # example card at bottom
    example_card(s, 0.7, 5.55, 11.9, 1.35, "EXAMPLE (Instructor-Created):",
                 example_runs, ac)
    return s

# ============================================================================
# SLIDE 7
# ============================================================================
s = concept_example(
    7, "standards", "Honesty and Integrity in Reporting", "honesty",
    [("Honesty and integrity", {"bold": True, "color": C_HONESTY}),
     (" mean reporting exactly what the data shows — never inventing, "
      "altering, or selectively hiding results. This includes:", {})],
    [
        [("Never ", {}), ("falsifying", {"bold": True}),
         (" data, findings, or conclusions ", {}),
         ("(Creswell & Creswell, 2023)", {"italic": True, "color": MUTED})],
        [("Reporting results ", {}), ("honestly", {"italic": True}),
         (", even when they're disappointing or unexpected", {})],
    ],
    [[("If the water filter only reduces bacteria by 40% instead of the "
       "hoped-for 90%, the honest researcher reports 40% — not a rounded-up, "
       "more impressive number.", {})]],
    C_HONESTY)
set_notes(s, "Honesty is usually the easiest of the four principles for students to "
             "grasp intuitively, so move through the definition quickly and spend more "
             "time on the example. Emphasize that dishonesty in research isn't always "
             "dramatic fabrication — it's often subtler, like rounding numbers favorably, "
             "leaving out an inconvenient data point, or overstating certainty. Ask "
             "students: 'Why might a researcher feel tempted to round up a disappointing "
             "result?' This surfaces the human pressure (wanting your project to "
             "'succeed') that makes this standard necessary in the first place.\n\nVisual: "
             "none necessary — the example is brief enough to sit directly on the concept "
             "slide.")

# ============================================================================
# SLIDE 8
# ============================================================================
s = concept_example(
    8, "standards", "Respecting Participants and Consent", "respect",
    [("Respect for participants", {"bold": True, "color": C_RESPECT}),
     (" means people must:", {})],
    [
        [("Know they are part of a study (its purpose is ", {}),
         ("disclosed", {"italic": True}), (", not hidden)", {})],
        [("Voluntarily", {"bold": True}),
         (" agree to take part — never pressured or misled", {})],
    ],
    [[("Before collecting a single water sample, the researchers explain to "
       "each household what the study is for, what will be done with their "
       "water, and confirm the household agrees to participate.", {})]],
    C_RESPECT)
set_notes(s, "Keep this deliberately simple and plain-language — students do not need "
             "formal consent forms or IRB procedures at this level; they need to "
             "understand the principle of voluntary, informed participation. Contrast the "
             "example with what a violation would look like: quietly testing a household's "
             "water without telling them, or implying that participation is mandatory. Ask "
             "students to notice that 'respect' here is really about honesty toward "
             "participants, which is the same value from Slide 7 — just aimed outward at "
             "the people involved rather than at the data.\n\nVisual: none necessary.")

# ============================================================================
# SLIDE 9
# ============================================================================
s = concept_example(
    9, "standards", "Confidentiality and Privacy", "confid",
    [("Confidentiality and privacy", {"bold": True, "color": C_CONFID}),
     (" mean protecting participants' identities and personal information "
      "when reporting results. Common strategies:", {})],
    [
        [("Using ", {}), ("pseudonyms", {"bold": True}),
         (" or aliases instead of real names", {})],
        [("Separating names from responses when recording data ", {}),
         ("(Creswell & Creswell, 2023)", {"italic": True, "color": MUTED})],
    ],
    [[("Instead of writing “Household of Mrs. Santos reported the water tastes "
       "better,” the report says “Household 3 reported the water tastes "
       "better.”", {})]],
    C_CONFID)
set_notes(s, "This principle often confuses students with 'avoiding harm' (the next "
             "slide) — clarify the distinction directly: confidentiality is specifically "
             "about identity protection, while avoiding harm is broader. Use the example "
             "to show a concrete before/after of how identifying details get removed from "
             "a report. You can ask: 'Why would a household care if their name appears in a "
             "public research report, even if the finding itself is positive?' — this "
             "helps students see that privacy matters regardless of whether the "
             "information seems sensitive.\n\nVisual: none necessary.")

# ============================================================================
# SLIDE 10
# ============================================================================
s = concept_example(
    10, "standards", "Avoiding Harm to People and Place", "harm",
    [("Avoiding harm", {"bold": True, "color": C_HARM}),
     (" means protecting participants, the community, and the environment "
      "from negative effects of the research itself. This includes:", {})],
    [
        [("Not deceiving or exploiting participants ", {}),
         ("(Creswell & Creswell, 2023)", {"italic": True, "color": MUTED})],
        [("Minimizing disruption to the research site", {})],
        [("Considering effects on the surrounding community and environment", {})],
    ],
    [[("If the researchers' water sampling disrupts the community's daily "
       "access to the well, or if a “failed” filter is left installed and "
       "mistakenly trusted by residents, real harm has occurred — separate "
       "from whether the data was reported honestly.", {})]],
    C_HARM)
set_notes(s, "This is the broadest of the four principles, so anchor it firmly with the "
             "example — the 'failed filter left installed' detail is important because it "
             "shows harm can happen even after data collection ends, purely through the "
             "physical consequences of the research existing in a real place. Ask students "
             "to brainstorm one additional way the water filter study could unintentionally "
             "harm the community (e.g., taking up residents' time repeatedly, raising false "
             "hope about water safety). This principle is also where research most visibly "
             "touches the environment, since the community's water source itself is the "
             "site of study.\n\nVisual: none necessary.")

# ============================================================================
# SLIDE 11 — decision-tree matching
# ============================================================================
s = base_slide()
header(s, "standards", "Ethical Standards Decision Tree", 11)
apply_chip(s, 0.7, 1.95, AQUA)
_, tf = textbox(s, 2.55, 1.9, 10.0, 0.8, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("For each mini-scenario, decide ", {"size": 14.5}),
          ("which of the four standards", {"bold": True, "size": 14.5}),
          (" is most directly at risk — Honesty, Respect, Confidentiality, "
           "or Avoiding Harm.", {"size": 14.5})], after=0, first=True, line=1.1)
scen = [
    "A researcher tests water without telling the household.",
    "A report lists a participant's full name and address.",
    "A researcher only publishes the filter's best-performing test result.",
    "Repeated data collection visits leave a household without well access for hours each time.",
]
sy = 2.95; sh_ = 0.82
for i, sc in enumerate(scen):
    y = sy + i * (sh_ + 0.16)
    b = rect(s, 0.7, y, 7.0, sh_, fill=WHITE, line=FAINT,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    b.adjustments[0] = 0.12
    soft_shadow(b, blur=0.05, dist=0.03, alpha=45000)
    num = rect(s, 0.9, y + sh_/2 - 0.27, 0.54, 0.54, fill=TEAL, shape=MSO_SHAPE.OVAL)
    _, ntf = textbox(s, 0.9, y + sh_/2 - 0.27, 0.54, 0.54, anchor=MSO_ANCHOR.MIDDLE)
    para(ntf, [(str(i+1), {})], size=16, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
    _, stf = textbox(s, 1.65, y, 5.9, sh_, anchor=MSO_ANCHOR.MIDDLE)
    para(stf, [(sc, {})], size=13.5, color=INK, after=0, first=True, line=1.05)
# four endpoint nodes (reuse colors)
nodes = [("Honesty", C_HONESTY), ("Respect", C_RESPECT),
         ("Confidentiality", C_CONFID), ("Avoiding Harm", C_HARM)]
nx = 8.35
_, ttf = textbox(s, nx, 2.75, 4.2, 0.4)
para(ttf, [("Which standard is at risk?", {})], size=13, color=MUTED,
     italic=True, align=PP_ALIGN.CENTER, after=0, first=True)
ny = 3.2
for i, (t, col) in enumerate(nodes):
    y = ny + i * (0.72 + 0.16)
    node = rect(s, nx, y, 4.2, 0.72, fill=col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    node.adjustments[0] = 0.35
    soft_shadow(node, blur=0.05, dist=0.03, alpha=45000)
    _, ntf = textbox(s, nx, y, 4.2, 0.72, anchor=MSO_ANCHOR.MIDDLE)
    para(ntf, [(t, {})], size=16, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
_, tf = textbox(s, 0.7, 6.75, 11.9, 0.4)
para(tf, [("Match each number to a standard.", {})], size=14, color=MUTED,
     italic=True, align=PP_ALIGN.CENTER, after=0, first=True)
set_notes(s, "This is the consolidation activity for the four core standards — resist "
             "explaining the answers until students have attempted all four matches. The "
             "intended mapping is: 1 -> Respect for Participants, 2 -> Confidentiality, "
             "3 -> Honesty and Integrity, 4 -> Avoiding Harm. Some students may reasonably "
             "argue overlaps (e.g., #1 could also touch 'avoiding harm') — use that as a "
             "teaching moment: in real research, violations often overlap, but naming the "
             "primary standard at risk builds precision in ethical reasoning. This "
             "activity should take no more than 5 minutes.\n\nVisual: a branching "
             "decision-tree with the four standards as endpoint nodes (reusing the four "
             "colors from Slide 6's matrix).")



# ============================================================================
# SLIDE 12
# ============================================================================
s = concept_example(
    12, "stages", "Ethics During the Planning Stage", "planning",
    [("At the ", {}), ("planning stage", {"bold": True, "color": SAND_DK}),
     (", ethical research means:", {})],
    [
        [("Choosing a research problem responsibly — one that could genuinely ", {}),
         ("benefit", {"bold": True}), (" participants, not just satisfy curiosity ", {}),
         ("(Creswell & Creswell, 2023)", {"italic": True, "color": MUTED})],
        [("Considering, before data collection ever begins, who might be "
          "affected and how", {})],
    ],
    [[("Choosing to test a low-cost filter ", {}),
      ("because the community lacks access to safe water", {"italic": True}),
      (" is a responsibly chosen problem — testing it purely because it's a "
       "“convenient” barangay near the school, with no real community benefit "
       "in mind, is not.", {})]],
    SAND_DK, flow_hi="Planning")
set_notes(s, "This begins the second major arc of the lecture — walking through the "
             "five-stage flowchart from Slide 2 in detail, one stage per slide. "
             "Reintroducing the same flowchart graphic (now with 'Planning' highlighted) "
             "gives students a visual anchor showing exactly where they are in the bigger "
             "picture. The key idea here is intentionality: ethical planning isn't "
             "passive, it requires actively asking 'who benefits from this research, and "
             "could this topic cause harm before I've even started?'\n\nVisual: the same "
             "five-stage flowchart from Slide 2, with the 'Planning' box highlighted. "
             "Reusing this exact graphic across Slides 12-15 lets students track lesson "
             "progress at a glance.")

# ============================================================================
# SLIDE 13
# ============================================================================
s = concept_example(
    13, "stages", "Ethics During Data Collection", "collecting",
    [("At the ", {}), ("data collection stage", {"bold": True, "color": SAND_DK}),
     (", ethical research means:", {})],
    [
        [("Being honest with participants about what is happening and why", {})],
        [("Never pressuring or ", {}), ("coercing", {"bold": True}),
         (" participation ", {}),
         ("(Creswell & Creswell, 2023)", {"italic": True, "color": MUTED})],
        [("Never ", {}), ("fabricating", {"bold": True}),
         (" data that wasn't actually collected", {})],
    ],
    [[("If a household declines to have their well water sampled, the "
       "researchers must respect that decision — inventing a data point for "
       "that household to “complete the set” would be a serious ethical "
       "violation.", {})]],
    SAND_DK, flow_hi="Collecting")
set_notes(s, "Note that this slide revisits 'honesty' and 'respect' from Slides 7-8, "
             "but now applied specifically to the action of collecting data, not the "
             "general principle. This repetition is intentional — it shows students that "
             "the same standards show up again and again across different stages, which is "
             "the core idea of the whole lecture. The fabrication example is worth "
             "dwelling on: ask students why a researcher under time pressure might be "
             "tempted to 'fill in' a missing data point, and why that's fundamentally "
             "different from honestly reporting an incomplete dataset.\n\nVisual: same "
             "flowchart graphic, now with 'Collecting Data' highlighted.")

# ============================================================================
# SLIDE 14
# ============================================================================
s = concept_example(
    14, "stages", "Ethics During Data Analysis", "analyzing",
    [("At the ", {}), ("data analysis stage", {"bold": True, "color": SAND_DK}),
     (", ethical research means:", {})],
    [
        [("Avoiding ", {}), ("taking sides", {"bold": True}),
         (" — not favoring results that make participants or the researcher "
          "look good ", {}),
         ("(Creswell & Creswell, 2023)", {"italic": True, "color": MUTED})],
        [("Reporting the ", {}), ("full range", {"bold": True}),
         (" of results, including unexpected or contrary findings", {})],
    ],
    [[("If 7 out of 10 households show improved water quality but 3 show no "
       "change, the researchers must report all 10 results — not just the 7 "
       "that support their hypothesis.", {})]],
    SAND_DK, flow_hi="Analyzing")
set_notes(s, "This stage is where 'honesty' (Slide 7) becomes most concrete and "
             "testable — students can directly see what selective reporting would look "
             "like using real numbers. Ask the class: 'If you were the researcher and only "
             "3 out of 10 households improved, how would you feel about reporting that?' "
             "This surfaces the emotional pull toward dishonesty (disappointment, fear of "
             "a 'failed' project) and lets you explicitly state that an honestly reported "
             "'mixed' result is not a failure — it's good research.\n\nVisual: same "
             "flowchart graphic, now with 'Analyzing Data' highlighted.")

# ============================================================================
# SLIDE 15 — pivot slide
# ============================================================================
s = base_slide()
ac = header(s, "stages", "Ethics During Reporting and Writing", 15)
flowchart(s, y=1.95, highlight="Reporting", accent=SAND_DK, h=0.8, size=12)
_, tf = textbox(s, 0.7, 3.05, 11.9, 0.6)
para(tf, [("At the ", {}), ("reporting stage", {"bold": True, "color": SAND_DK}),
          (", ethical research means:", {})], size=17, after=8, first=True)
_, tf = textbox(s, 1.0, 3.7, 11.4, 1.2)
bullets(tf, [
    "Communicating findings honestly and clearly",
    [("Giving proper ", {}), ("credit", {"bold": True}),
     (" to the ideas and words of others ", {}),
     ("(Creswell & Creswell, 2023)", {"italic": True, "color": MUTED})],
], size=16.5, gap=8, bullet_color=SAND_DK, first=True)
# pivot callout pointing to citation section
pv = rect(s, 0.7, 5.35, 11.9, 1.35, fill=CORAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
pv.adjustments[0] = 0.06
soft_shadow(pv)
_, ptf = textbox(s, 1.1, 5.5, 9.8, 1.05, anchor=MSO_ANCHOR.MIDDLE)
para(ptf, [("That second point — giving credit — is its own major skill.", {"bold": True, "size": 18, "color": WHITE, "font": FONT_H})], after=3, first=True)
para(ptf, [("It's coming up next.", {"italic": True, "size": 16, "color": RGBColor(0xFF,0xE6,0xDD)})], after=0)
arrow = s.shapes.add_shape(MSO_SHAPE.RIGHT_ARROW, Inches(11.1), Inches(5.75),
                           Inches(1.15), Inches(0.55))
_shadow_off(arrow); _set_fill(arrow, WHITE); _no_line(arrow)
set_notes(s, "This is the pivot slide of the entire lecture — deliver it with a clear "
             "tonal shift to signal that a new (but connected) topic is beginning. Don't "
             "elaborate on 'giving credit' yet beyond this one line; the next section will "
             "unpack it fully. The goal here is continuity: students should feel that "
             "citation isn't an unrelated skill being bolted onto an ethics lesson, but "
             "simply what 'honest reporting' requires when your work builds on someone "
             "else's — which directly echoes the original filter design mentioned in the "
             "Slide 1 scenario.\n\nVisual: same flowchart with 'Reporting' highlighted, "
             "plus an arrow pointing toward the next section's title to foreshadow the "
             "shift without a separate recap slide.")

# ============================================================================
# SLIDE 16 — sorting activity
# ============================================================================
s = base_slide()
header(s, "stages", "Trace the Stages", 16)
apply_chip(s, 0.7, 1.9, SAND_DK)
_, tf = textbox(s, 2.55, 1.87, 10.0, 0.72, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("Sort the following researcher actions into the correct stage — "
           "Planning, Collecting, Analyzing, or Reporting.", {"size": 14.5})],
     after=0, first=True, line=1.1)
flowchart(s, y=2.75, highlight=None, accent=SAND_DK, h=0.85, size=12)
# draggable-style cards
actions = [
    "Deciding to study the barangay because they genuinely lack safe water access",
    "Recording a water sample result exactly as measured, even though it's disappointing",
    "Including both improved and unchanged households in the final results",
    "Properly acknowledging the earlier filter design that inspired their own",
]
ay = 4.05; aw = 5.75; ah = 0.92
for i, a in enumerate(actions):
    c = i % 2; r = i // 2
    x = 0.7 + c * (aw + 0.35); y = ay + r * (ah + 0.3)
    card = rect(s, x, y, aw, ah, fill=WHITE, line=SAND, line_w=1.5,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.1
    soft_shadow(card, blur=0.05, dist=0.03, alpha=45000)
    num = rect(s, x + 0.2, y + ah/2 - 0.27, 0.54, 0.54, fill=SAND_DK, shape=MSO_SHAPE.OVAL)
    _, ntf = textbox(s, x + 0.2, y + ah/2 - 0.27, 0.54, 0.54, anchor=MSO_ANCHOR.MIDDLE)
    para(ntf, [(str(i+1), {})], size=16, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
    _, atf = textbox(s, x + 0.95, y, aw - 1.15, ah, anchor=MSO_ANCHOR.MIDDLE)
    para(atf, [(a, {})], size=13, color=INK, after=0, first=True, line=1.05)
_, tf = textbox(s, 0.7, 6.5, 11.9, 0.4)
para(tf, [("Place each action on the flowchart.", {})], size=14, color=MUTED,
     italic=True, align=PP_ALIGN.CENTER, after=0, first=True)
set_notes(s, "This is the consolidation activity for the entire 'stages' section (Slides "
             "12-15) — students should place each numbered action onto the appropriate "
             "stage of the flowchart (physically, if using printed handouts, or "
             "verbally/digitally otherwise). Correct mapping: 1 -> Planning, 2 -> "
             "Collecting, 3 -> Analyzing, 4 -> Reporting. Item 4 deliberately foreshadows "
             "the citation section without teaching it yet — if students struggle to "
             "explain why it belongs at the reporting stage, that's expected; simply "
             "confirm it's coming up next.\n\nVisual: the recurring five-stage flowchart "
             "used as an interactive sorting surface, with the four numbered actions as "
             "draggable cards (digital) or sticky notes (physical).")



# ============================================================================
# SLIDE 17
# ============================================================================
s = base_slide()
header(s, "bridge", "What Counts as Plagiarism", 17)
defb = rect(s, 0.7, 2.05, 11.9, 1.3, fill=CORAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
defb.adjustments[0] = 0.06
soft_shadow(defb)
_, tf = textbox(s, 1.1, 2.2, 11.1, 1.0, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("Plagiarism", {"bold": True, "size": 21, "color": WHITE, "font": FONT_H}),
          ("  —  presenting someone else's work, ideas, or words as your own, "
           "without giving them credit ", {"size": 17.5, "color": WHITE}),
          ("(Creswell & Creswell, 2023)", {"size": 15, "color": RGBColor(0xFF,0xE6,0xDD), "italic": True}),
          (".", {"size": 17.5, "color": WHITE})],
     after=0, first=True, line=1.12)
_, tf = textbox(s, 0.7, 3.7, 11.9, 1.0)
para(tf, [("Plagiarism is not just a ", {}), ("rule", {"italic": True}),
          (" — it's an ", {}),
          ("ethics violation", {"bold": True, "color": CORAL}),
          (". It breaks the same standard of honesty and integrity introduced "
           "earlier in this lesson.", {})],
     size=17, after=0, first=True, line=1.15)
example_card(s, 0.7, 4.95, 11.9, 1.55, "EXAMPLE (Instructor-Created):",
             [[("If the researchers build their filter using the earlier student's "
                "design but never mention that design in their report, readers are "
                "misled into thinking the design is original — that's plagiarism.", {})]],
             CORAL)
set_notes(s, "The most important move on this slide is framing — students often think "
             "of plagiarism as a school-specific 'rule' about citations, disconnected "
             "from real ethics. Explicitly connect it back to Slide 7's 'Honesty and "
             "Integrity' standard: taking credit for someone else's work is a form of "
             "dishonesty, just directed at ideas instead of data. This reframe is what "
             "makes the citation mechanics that follow feel meaningful rather than "
             "arbitrary.\n\nVisual: none necessary.")

# ============================================================================
# SLIDE 18 — two-column comparison
# ============================================================================
s = base_slide()
header(s, "bridge", "Two Forms of Plagiarism", 18)
cols = [
    ("Direct Plagiarism", "Copying someone else's exact words without credit",
     "Even one sentence, word-for-word, without credit counts.", CORAL),
    ("Uncredited Paraphrasing", "Restating someone else's idea in your own words — but still without giving credit",
     "Changing the wording doesn't remove the need to cite the original idea.", RGBColor(0xC0,0x53,0x38)),
]
cw = 5.75; ch = 3.7; y = 2.4
for i, (t, d, note, col) in enumerate(cols):
    x = 0.7 + i * (cw + 0.4)
    card = rect(s, x, y, cw, ch, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.04
    soft_shadow(card)
    rect(s, x, y, cw, 0.95, fill=col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    _, htf = textbox(s, x + 0.3, y, cw - 0.6, 0.95, anchor=MSO_ANCHOR.MIDDLE)
    para(htf, [(t, {})], size=19, color=WHITE, bold=True, font=FONT_H, after=0,
         first=True)
    _, dtf = textbox(s, x + 0.35, y + 1.2, cw - 0.7, 1.4)
    para(dtf, [(d, {})], size=16, color=INK, after=0, first=True, line=1.15)
    ln = rect(s, x + 0.35, y + 2.55, cw - 0.7, 0.02, fill=FAINT)
    _, ntf = textbox(s, x + 0.35, y + 2.7, cw - 0.7, 0.9)
    para(ntf, [(note, {"italic": True})], size=14, color=col, bold=True, after=0,
         first=True, line=1.12)
set_notes(s, "Most students already recognize direct copy-paste plagiarism as wrong; "
             "the harder concept — and the one worth spending more time on — is uncredited "
             "paraphrasing. Many students genuinely believe that rewording something in "
             "their own words makes citation unnecessary. Correct this directly: the idea "
             "still originated with someone else, so credit is still owed, even if not a "
             "single word is copied. This distinction directly sets up why citation "
             "applies to paraphrased material, not just direct quotes, which matters for "
             "the mechanics slides ahead.\n\nVisual: none necessary — the two-column "
             "layout is the visual.")

# ============================================================================
# SLIDE 19 — concept map
# ============================================================================
s = base_slide()
header(s, "bridge", "Why We Cite Sources", 19)
_, tf = textbox(s, 0.7, 1.95, 11.9, 0.5)
para(tf, [("Citation exists for three connected reasons:", {})], size=17,
     color=INK, after=0, first=True)
# center node
ccx, ccy, cr = 2.65, 4.35, 1.5
center = s.shapes.add_shape(MSO_SHAPE.OVAL, Inches(ccx - cr/2), Inches(ccy - cr/2),
                            Inches(cr), Inches(cr))
_shadow_off(center); _set_fill(center, CORAL); _no_line(center); soft_shadow(center)
_, ctf = textbox(s, ccx - cr/2, ccy - cr/2, cr, cr, anchor=MSO_ANCHOR.MIDDLE)
para(ctf, [("Citation", {})], size=20, color=WHITE, bold=True, font=FONT_H,
     align=PP_ALIGN.CENTER, after=0, first=True)
reasons = [
    ("Giving credit", "acknowledging whose idea or words you used", C_HONESTY),
    ("Enabling verification", "letting readers check your sources for themselves", C_RESPECT),
    ("Joining the conversation", "showing how your work connects to existing knowledge", C_CONFID),
]
bx = 5.2; bw = 7.3; bh = 1.15; by0 = 2.55
for i, (t, d, col) in enumerate(reasons):
    y = by0 + i * (bh + 0.28)
    # connector line
    conn = s.shapes.add_connector(2, Inches(ccx + cr/2 - 0.15), Inches(ccy),
                                  Inches(bx), Inches(y + bh/2))
    conn.line.color.rgb = col; conn.line.width = Pt(2.0)
    _shadow_off(conn)
    b = rect(s, bx, y, bw, bh, fill=WHITE, line=FAINT,
             shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    b.adjustments[0] = 0.12
    soft_shadow(b, blur=0.05, dist=0.03, alpha=45000)
    rect(s, bx, y, 0.14, bh, fill=col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    numb = rect(s, bx + 0.35, y + bh/2 - 0.28, 0.56, 0.56, fill=col, shape=MSO_SHAPE.OVAL)
    _, ntf = textbox(s, bx + 0.35, y + bh/2 - 0.28, 0.56, 0.56, anchor=MSO_ANCHOR.MIDDLE)
    para(ntf, [(str(i+1), {})], size=17, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
    _, btf = textbox(s, bx + 1.1, y + 0.12, bw - 1.3, bh - 0.2, anchor=MSO_ANCHOR.MIDDLE)
    para(btf, [(t, {"bold": True, "color": col, "size": 16, "font": FONT_H}),
               ("  —  " + d, {"size": 14, "color": INK})], after=0, first=True,
         line=1.1)
_, tf = textbox(s, 0.7, 6.65, 11.9, 0.5)
para(tf, [("Citation isn't a punishment for “almost plagiarizing” — it's how "
           "honest research is supposed to work.", {})],
     size=15, color=CORAL, italic=True, bold=True, align=PP_ALIGN.CENTER,
     after=0, first=True)
set_notes(s, "This slide answers the question students are often silently asking: 'Why "
             "does this even matter if I'm not trying to steal anything?' Reframe citation "
             "as a positive practice rather than a defensive one — it's not just about "
             "avoiding punishment, it's a normal and expected part of how all researchers "
             "build on each other's work. Use the water filter example one more time: "
             "citing the earlier student's design doesn't weaken the new researchers' work "
             "— it actually strengthens their credibility by showing their design has a "
             "legitimate foundation.\n\nVisual: a concept map with 'Citation' at the "
             "center and three branches to the three reasons.")

# ============================================================================
# SLIDE 20 — spot the difference
# ============================================================================
s = base_slide()
header(s, "bridge", "Plagiarism or Proper Credit?", 20)
apply_chip(s, 0.7, 1.95, CORAL)
_, tf = textbox(s, 2.55, 1.98, 10, 0.5, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("Which version properly credits the source?", {"bold": True,
           "size": 16, "color": CORAL})], after=0, first=True)
versions = [
    ("Version A", "“Coconut husk charcoal can effectively filter bacteria from contaminated water.”",
     RGBColor(0x9A,0xA5,0xAB), "MISSING A SOURCE"),
    ("Version B", "“According to Reyes (2022), coconut husk charcoal can effectively filter bacteria from contaminated water.”",
     C_HONESTY, "CREDITS THE SOURCE"),
]
vw = 5.75; vh = 3.1; y = 2.7
for i, (label, text, col, tag) in enumerate(versions):
    x = 0.7 + i * (vw + 0.4)
    card = rect(s, x, y, vw, vh, fill=WHITE, line=col, line_w=2.0,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.04
    soft_shadow(card)
    rect(s, x, y, vw, 0.85, fill=col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    _, htf = textbox(s, x + 0.3, y, vw - 0.6, 0.85, anchor=MSO_ANCHOR.MIDDLE)
    para(htf, [(label, {})], size=18, color=WHITE, bold=True, font=FONT_H, after=0,
         first=True)
    _, vtf = textbox(s, x + 0.35, y + 1.05, vw - 0.7, 1.4, anchor=MSO_ANCHOR.MIDDLE)
    para(vtf, [(text, {"italic": True})], size=15, color=INK, after=0, first=True,
         line=1.15)
    tagb = rect(s, x + 0.35, y + vh - 0.65, vw - 0.7, 0.45, fill=col,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    tagb.adjustments[0] = 0.5
    _, ttf = textbox(s, x + 0.35, y + vh - 0.65, vw - 0.7, 0.45, anchor=MSO_ANCHOR.MIDDLE)
    para(ttf, [(tag, {})], size=12, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
_, tf = textbox(s, 0.7, 6.1, 11.9, 0.5)
para(tf, [("Which version avoids plagiarism? What's missing from the other?", {})],
     size=15, color=MUTED, italic=True, align=PP_ALIGN.CENTER, after=0, first=True)
set_notes(s, "This should feel almost too simple by this point — that's intentional, "
             "since it confirms students have internalized the core idea before adding "
             "citation mechanics on top. Version B is correct because it names the source "
             "of the idea; Version A presents the same claim as if it were the "
             "researchers' own original finding. Use this moment to explicitly preview: "
             "'Version B shows an in-text citation — next, we'll learn exactly how to "
             "build one properly.' This is a natural, low-key transition rather than a "
             "formal 'forward bridge' recap.\n\nVisual: none necessary.")



# ============================================================================
# SLIDE 21 — two-part diagram
# ============================================================================
s = base_slide()
header(s, "citation", "Two Parts of Every Citation", 21)
_, tf = textbox(s, 0.7, 1.95, 11.9, 0.5)
para(tf, [("Every complete citation has ", {}),
          ("two connected parts", {"bold": True, "color": PURPLE}),
          (":", {})], size=17, after=0, first=True)
parts = [
    ("In-Text Citation", "A short note within your writing, pointing to a source",
     "(Reyes, 2022)", PURPLE),
    ("Reference List Entry", "A full entry at the end of your paper, giving complete source details",
     "Full publication details for Reyes' 2022 work", BLUE),
]
pw = 5.15; ph = 3.3; y = 2.65
xs = [0.9, 7.28]
for i, (t, d, ex, col) in enumerate(parts):
    x = xs[i]
    card = rect(s, x, y, pw, ph, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.04
    soft_shadow(card)
    rect(s, x, y, pw, 0.9, fill=col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    _, htf = textbox(s, x + 0.3, y, pw - 0.6, 0.9, anchor=MSO_ANCHOR.MIDDLE)
    para(htf, [(t, {})], size=18, color=WHITE, bold=True, font=FONT_H, after=0,
         first=True)
    _, dtf = textbox(s, x + 0.35, y + 1.1, pw - 0.7, 1.05)
    para(dtf, [(d, {})], size=15, color=INK, after=0, first=True, line=1.15)
    exb = rect(s, x + 0.35, y + ph - 1.0, pw - 0.7, 0.7, fill=RGBColor(0xF0,0xEC,0xF6) if i==0 else RGBColor(0xEA,0xF1,0xF6),
               shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    exb.adjustments[0] = 0.18
    _, etf = textbox(s, x + 0.5, y + ph - 1.0, pw - 1.0, 0.7, anchor=MSO_ANCHOR.MIDDLE)
    para(etf, [("Example:  ", {"size": 12, "color": MUTED, "bold": True}),
               (ex, {"size": 13.5, "color": col, "bold": True, "font": FONT_H})],
         after=0, first=True, line=1.05)
# connecting arrow + dotted line
conn = s.shapes.add_shape(MSO_SHAPE.LEFT_RIGHT_ARROW, Inches(6.15), Inches(4.05),
                          Inches(1.03), Inches(0.5))
_shadow_off(conn); _set_fill(conn, SAND_DK); _no_line(conn)
_, tf = textbox(s, 0.7, 6.25, 11.9, 0.5)
para(tf, [("The short note in your text always has a matching full entry at "
           "the end.", {})], size=15.5, color=PURPLE, italic=True, bold=True,
     align=PP_ALIGN.CENTER, after=0, first=True)
set_notes(s, "Establish this two-part structure clearly before diving into either part "
             "individually — students need to understand that in-text citations and "
             "reference list entries are not two separate skills, but two connected halves "
             "of the same citation. A useful analogy: the in-text citation is like a claim "
             "ticket, and the reference list entry is what you get when you redeem it — "
             "full details are only in the reference list, so the in-text note only needs "
             "to be short enough to point there.\n\nVisual: a two-box diagram connected by "
             "an arrow — '(Reyes, 2022)' in the text box linking to the fuller reference "
             "entry box. This visual reappears conceptually in Slides 22 and 24.")

# ============================================================================
# SLIDE 22 — in-text table
# ============================================================================
s = base_slide()
header(s, "citation", "APA In-Text Citations", 22)
_, tf = textbox(s, 0.7, 1.95, 11.9, 0.5)
para(tf, [("This course uses ", {}),
          ("APA (American Psychological Association) style", {"bold": True, "color": PURPLE}),
          (" for all citations.", {})], size=17, after=0, first=True)
# format callout
fb = rect(s, 0.7, 2.6, 11.9, 0.85, fill=RGBColor(0xF0,0xEC,0xF6),
          shape=MSO_SHAPE.ROUNDED_RECTANGLE)
fb.adjustments[0] = 0.12
_, ftf = textbox(s, 1.0, 2.6, 11.3, 0.85, anchor=MSO_ANCHOR.MIDDLE)
para(ftf, [("APA in-text citation format:   ", {"size": 15, "color": INK, "bold": True}),
           ("(Author's Last Name, Year)", {"size": 17, "color": PURPLE, "bold": True, "italic": True, "font": FONT_H})],
     after=0, first=True)
styled_table(s, [
    ["Use Case", "Example"],
    ["Paraphrased idea", "Coconut husk charcoal has shown filtering potential in prior designs (Reyes, 2022)."],
    [[("Direct quote ", {}), ("(add page number)", {"italic": True, "size": 13})],
     [("Reyes (2022) found the design ", {}),
      ("“reduced bacterial presence by over 60%”", {"italic": True}),
      (" (p. 14).", {})]],
], x=0.7, y=3.75, w=11.9, h=2.4, col_w=[3.4, 8.5], accent=PURPLE,
   fsize=15, hsize=15.5)
set_notes(s, "Keep the focus tightly on the author-date format — this is the one pattern "
             "students need to master, and introducing multiple citation styles at this "
             "stage would only create confusion (that comparison is intentionally left for "
             "later, more advanced coursework). Point out the small but important "
             "difference between the two example rows: a paraphrase only needs (Author, "
             "Year), while a direct quote also requires a page number, since you're "
             "pointing to the source's exact wording. Have students identify which format "
             "the earlier Slide 20 'Version B' used (a paraphrase, so no page number was "
             "needed).\n\nVisual: none necessary — the table format is the clearest visual "
             "here.")

# ============================================================================
# SLIDE 23 — practice
# ============================================================================
s = base_slide()
header(s, "citation", "Practice In-Text Citations", 23)
apply_chip(s, 0.7, 1.95, PURPLE)
_, tf = textbox(s, 2.55, 1.98, 10.0, 0.5, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("Add a properly formatted APA in-text citation to each sentence.", {"bold": True, "size": 15.5, "color": PURPLE})],
     after=0, first=True)
items = [
    ([("A 2021 study by Dela Cruz found that sand filtration removes 80% of "
       "sediment.", {})], "Paraphrase — write the citation."),
    ([("Dela Cruz's 2021 report stated the filter ", {}),
      ("“significantly improved water clarity within 48 hours.”", {"italic": True})],
     "Direct quote, page 9 — write the citation."),
]
y = 2.85; ih = 1.75
for i, (sent, hint) in enumerate(items):
    yy = y + i * (ih + 0.3)
    card = rect(s, 0.7, yy, 11.9, ih, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.05
    soft_shadow(card, blur=0.06, dist=0.03, alpha=45000)
    num = rect(s, 1.0, yy + 0.35, 0.6, 0.6, fill=PURPLE, shape=MSO_SHAPE.OVAL)
    _, ntf = textbox(s, 1.0, yy + 0.35, 0.6, 0.6, anchor=MSO_ANCHOR.MIDDLE)
    para(ntf, [(str(i+1), {})], size=18, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
    _, stf = textbox(s, 1.85, yy + 0.25, 10.4, 1.3, anchor=MSO_ANCHOR.MIDDLE)
    para(stf, sent, size=16, color=INK, after=6, first=True, line=1.1)
    para(stf, [("( " + hint + " )", {"italic": True, "color": PURPLE, "size": 13.5})],
         after=0)
set_notes(s, "Give students two or three minutes to write both citations independently "
             "before reviewing as a class. Expected answers: (1) '...removes 80% of "
             "sediment (Dela Cruz, 2021).' and (2) '...within 48 hours' (Dela Cruz, 2021, "
             "p. 9).' Common student errors to watch for: forgetting the comma between "
             "author and year, forgetting 'p.' before the page number, or adding a page "
             "number to the paraphrase (unnecessary, since only direct quotes require "
             "one). Correct these live as a class.\n\nVisual: none necessary.")

# ============================================================================
# SLIDE 24 — three template cards
# ============================================================================
s = base_slide()
header(s, "citation", "APA Reference List Basics", 24)
_, tf = textbox(s, 0.7, 1.95, 11.9, 0.5)
para(tf, [("Every source type has a specific ", {}),
          ("reference list", {"bold": True, "color": PURPLE}),
          (" format. Three common types:", {})], size=17, after=0, first=True)
templates = [
    ("Book", MSO_SHAPE.RECTANGLE,
     "Author, A. A. (Year). Title of the work. Publisher.", C_HONESTY),
    ("Journal Article", MSO_SHAPE.FOLDED_CORNER,
     "Author, A. A. (Year). Title of the article. Journal Name, Volume(Issue), page range.", C_RESPECT),
    ("Website", MSO_SHAPE.ROUNDED_RECTANGLE,
     "Author, A. A. (Year, Month Day). Title of the page. Site Name. URL", C_CONFID),
]
cw = 3.85; ch = 3.85; y = 2.65
for i, (t, icon, tmpl, col) in enumerate(templates):
    x = 0.7 + i * (cw + 0.28)
    card = rect(s, x, y, cw, ch, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.045
    soft_shadow(card)
    rect(s, x, y, cw, 0.16, fill=col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    # icon
    ic = s.shapes.add_shape(icon, Inches(x + cw/2 - 0.45), Inches(y + 0.5),
                            Inches(0.9), Inches(0.72))
    _shadow_off(ic); _set_fill(ic, col); _no_line(ic)
    if icon == MSO_SHAPE.RECTANGLE:  # book spine detail
        rect(s, x + cw/2 - 0.45, y + 0.5, 0.16, 0.72, fill=WHITE)
    _, htf = textbox(s, x + 0.2, y + 1.45, cw - 0.4, 0.5, anchor=MSO_ANCHOR.MIDDLE)
    para(htf, [(t, {})], size=18, color=col, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
    codeb = rect(s, x + 0.25, y + 2.05, cw - 0.5, 1.55, fill=RGBColor(0xF3,0xF6,0xF7),
                 shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    codeb.adjustments[0] = 0.06
    _, ctf = textbox(s, x + 0.42, y + 2.15, cw - 0.85, 1.35, anchor=MSO_ANCHOR.MIDDLE)
    para(ctf, [(tmpl, {})], size=12.5, color=INK, font="Consolas", after=0,
         first=True, line=1.2)
set_notes(s, "Present these three templates as patterns to recognize, not to memorize by "
             "rote — students will look these up when writing real papers, so the goal is "
             "familiarity with the structure, not flawless recall under pressure. Point "
             "out what stays consistent across all three: author and year always come "
             "first, matching the in-text citation students just practiced. What changes "
             "is only the middle — title formatting and source-specific details like "
             "journal name or URL.\n\nVisual: three side-by-side template cards, visually "
             "distinct by source type (book, journal, website icons) so students can "
             "quickly identify which format applies to their own source.")



# ============================================================================
# SLIDE 25 — sample entries
# ============================================================================
s = base_slide()
header(s, "citation", "Sample APA Reference Entries", 25)
_, tf = textbox(s, 0.7, 1.9, 11.9, 0.45)
para(tf, [("Instructor-Created Examples, formatted for illustration", {"italic": True})],
     size=13.5, color=MUTED, after=0, first=True)
samples = [
    ("Book", C_HONESTY, [
        ("Santos, M. R. (2020). ", {}),
        ("Water and community: Local solutions to global problems.", {"italic": True}),
        (" Manila Press.", {})]),
    ("Journal Article", C_RESPECT, [
        ("Reyes, J. P. (2022). Low-cost filtration using coconut husk charcoal. ", {}),
        ("Philippine Journal of Environmental Engineering, 15", {"italic": True}),
        ("(2), 45–58.", {})]),
    ("Website", C_CONFID, [
        ("Department of Science and Technology. (2023, March 4). ", {}),
        ("Community water testing guidelines.", {"italic": True}),
        (" DOST Philippines. https://www.dost.gov.ph", {})]),
]
y = 2.5; rh = 1.35
for i, (label, col, runs) in enumerate(samples):
    yy = y + i * (rh + 0.2)
    card = rect(s, 0.7, yy, 11.9, rh, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.05
    soft_shadow(card, blur=0.06, dist=0.03, alpha=45000)
    tab = rect(s, 0.7, yy, 2.3, rh, fill=col, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
    _, ltf = textbox(s, 0.8, yy, 2.1, rh, anchor=MSO_ANCHOR.MIDDLE)
    para(ltf, [(label, {})], size=16, color=WHITE, bold=True, font=FONT_H,
         align=PP_ALIGN.CENTER, after=0, first=True)
    _, etf = textbox(s, 3.2, yy + 0.15, 9.15, rh - 0.3, anchor=MSO_ANCHOR.MIDDLE)
    para(etf, runs, size=14.5, color=INK, after=0, first=True, line=1.15)
set_notes(s, "This slide exists specifically so students can see a complete, realistic "
             "reference list — not just an abstract template. Walk through each entry and "
             "have students point out which part of the template (from Slide 24) each "
             "piece corresponds to: author, year, title, and publisher/journal/site "
             "details. This is a good moment to note the italics convention (book and "
             "journal titles are italicized; article and webpage titles are not) since "
             "it's a common formatting slip.\n\nVisual: none necessary — the three fully "
             "formatted entries are themselves the instructional content.")

# ============================================================================
# SLIDE 26 — build a reference list
# ============================================================================
s = base_slide()
header(s, "citation", "Build a Reference List", 26)
apply_chip(s, 0.7, 1.95, PURPLE)
_, tf = textbox(s, 2.55, 1.98, 10.0, 0.5, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("Turn this source information into a properly formatted APA "
           "reference entry.", {"bold": True, "size": 15, "color": PURPLE})],
     after=0, first=True)
# source-detail panel
srcpanel = rect(s, 0.7, 2.65, 6.1, 4.0, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
srcpanel.adjustments[0] = 0.03
soft_shadow(srcpanel)
rect(s, 0.7, 2.65, 6.1, 0.6, fill=PURPLE, shape=MSO_SHAPE.ROUND_2_SAME_RECTANGLE)
_, htf = textbox(s, 0.95, 2.65, 5.6, 0.6, anchor=MSO_ANCHOR.MIDDLE)
para(htf, [("SOURCE DETAILS", {})], size=13.5, color=WHITE, bold=True,
     font=FONT_H, after=0, first=True)
details = [
    ("Author:", "Dela Cruz, A."),
    ("Year:", "2021"),
    ("Article title:", "Sand filtration effectiveness in rural water systems"),
    ("Journal:", "Journal of Applied Environmental Science", True),
    ("Volume/Issue:", "9(3)"),
    ("Pages:", "112–120"),
]
_, dtf = textbox(s, 1.0, 3.45, 5.55, 3.0)
for i, d in enumerate(details):
    lab, val = d[0], d[1]
    ital = len(d) > 2 and d[2]
    para(dtf, [(lab + "  ", {"bold": True, "color": PURPLE, "size": 14.5, "font": FONT_H}),
               (val, {"size": 14.5, "color": INK, "italic": bool(ital)})],
         after=8, first=(i == 0), line=1.05)
# answer/work area
wp = rect(s, 7.1, 2.65, 5.5, 4.0, fill=RGBColor(0xF3,0xEF,0xF8),
          shape=MSO_SHAPE.ROUNDED_RECTANGLE)
wp.adjustments[0] = 0.03
_, wtf = textbox(s, 7.4, 3.0, 4.9, 3.4, anchor=MSO_ANCHOR.TOP)
para(wtf, [("Write the full reference list entry:", {"bold": True, "color": PURPLE,
            "size": 15, "font": FONT_H})], after=12, first=True)
for _ in range(4):
    para(wtf, [("_______________________________", {"color": RGBColor(0xB9,0xA8,0xD0), "size": 15})],
         after=12)
set_notes(s, "This is the culminating skills-practice slide for citation mechanics — "
             "students now assemble a complete entry from raw, unordered information "
             "rather than filling in a partial template. Expected answer: 'Dela Cruz, A. "
             "(2021). Sand filtration effectiveness in rural water systems. Journal of "
             "Applied Environmental Science, 9(3), 112-120.' Have a few students share "
             "their answers aloud or on the board, and use any discrepancies (missing "
             "italics, wrong punctuation, misplaced year) as quick, low-stakes correction "
             "opportunities before moving to the final application.\n\nVisual: none "
             "necessary.")

# ============================================================================
# SLIDE 27 — audit checklist
# ============================================================================
s = base_slide()
header(s, "integrate", "Full Ethics and Citation Audit", 27)
apply_chip(s, 0.7, 1.9, TEAL, text="APPLY IT — ONE LAST TIME", width=3.15)
_, tf = textbox(s, 4.05, 1.87, 8.5, 0.66, anchor=MSO_ANCHOR.MIDDLE)
para(tf, [("The Barangay Water Filter researchers are ready to submit their "
           "final report. Audit their draft against everything covered today:", {"size": 13.5})],
     after=0, first=True, line=1.1)
checks = [
    [("Did they honestly report ", {}), ("all", {"bold": True}),
     (" results, not just favorable ones?", {})],
    [("Did participating households know about and agree to the study?", {})],
    [("Are household identities protected in the report?", {})],
    [("Was the research conducted without unnecessary harm to people or place?", {})],
    [("Is the earlier filter design properly ", {}), ("cited", {"bold": True}),
     (" — both in-text and in the reference list?", {})],
]
cy = 2.75; chh = 0.68
for i, c in enumerate(checks):
    yy = cy + i * (chh + 0.14)
    card = rect(s, 0.7, yy, 11.9, chh, fill=WHITE, line=FAINT,
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    card.adjustments[0] = 0.15
    soft_shadow(card, blur=0.05, dist=0.03, alpha=40000)
    box = rect(s, 1.0, yy + chh/2 - 0.22, 0.44, 0.44, fill=PAPER, line=TEAL,
               line_w=2.0, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    box.adjustments[0] = 0.2
    _, ctf = textbox(s, 1.7, yy, 10.6, chh, anchor=MSO_ANCHOR.MIDDLE)
    para(ctf, c, size=15, color=INK, after=0, first=True, line=1.05)
_, tf = textbox(s, 0.7, 6.65, 11.9, 0.5)
para(tf, [("If every box can be checked, the research is both scientifically "
           "sound and ethically sound.", {})], size=15.5, color=TEAL, italic=True,
     bold=True, align=PP_ALIGN.CENTER, after=0, first=True)
set_notes(s, "Close the lecture by returning to the exact scenario from Slide 1, now "
             "fully resolved through everything students have learned — this bookends the "
             "lesson without introducing new content or previewing future lessons. Work "
             "through the checklist as a class, calling back to the specific slide where "
             "each item was covered (Honesty -> Slide 7, Consent -> Slide 8, "
             "Confidentiality -> Slide 9, Harm -> Slide 10, Citation -> Slides 17-26). End "
             "by emphasizing the throughline of the entire lesson: ethical research and "
             "well-cited research are not two separate obligations — both come from the "
             "same underlying commitment to honesty and respect for other people's "
             "contributions.\n\nVisual: a checklist graphic with checkable boxes beside "
             "each item — a practical audit tool students can reuse for their own future "
             "research reports.")

# ============================================================================
# APPENDIX — competency alignment map
# ============================================================================
s = base_slide()
header(s, "integrate", "Appendix: Slide-to-Competency Map", 28)
styled_table(s, [
    ["Slides", "Competency Focus"],
    ["1–5", "Foundation: what research ethics is and why it matters (Comp. 9)"],
    ["6–11", "The four core ethical standards (Comp. 9)"],
    ["12–16", "Applying ethics across all stages of the research process (Comp. 9)"],
    ["17–20", "Plagiarism as the ethical bridge into citation (Comp. 9 → 10)"],
    ["21–26", "APA citation mechanics — in-text and reference list (Comp. 10)"],
    ["27", "Integrated ethics + citation application (Comp. 9 & 10)"],
], x=0.7, y=2.15, w=11.9, h=4.2, col_w=[2.2, 9.7], accent=TEAL, fsize=15,
   hsize=16)
set_notes(s, "Appendix: Slide-to-Competency Alignment Map. Slides 1-5 build the "
             "foundation (Comp. 9); Slides 6-11 cover the four core ethical standards "
             "(Comp. 9); Slides 12-16 apply ethics across all stages of the research "
             "process (Comp. 9); Slides 17-20 use plagiarism as the ethical bridge into "
             "citation (Comp. 9 to 10); Slides 21-26 teach APA citation mechanics, in-text "
             "and reference list (Comp. 10); Slide 27 is integrated ethics + citation "
             "application (Comp. 9 & 10).")

# ----------------------------------------------------------------------------
out = "/projects/sandbox/physics/Lecture2-Research-Ethics.pptx"
prs.save(out)
print("Saved", out, "with", len(prs.slides._sldIdLst), "slides")
