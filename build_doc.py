# -*- coding: utf-8 -*-
"""Generate a styled .docx (WordprocessingML + OMML) for the Free-Fall guided examples.

Equations are laid out so every '=' aligns: a borderless 2-column table where
col-0 (left-hand side) is right-justified and col-1 ('=' + right-hand side) is
left-justified. All equations are written in OMML (Office Math Markup Language).
"""
import os, zipfile

# ---------------------------------------------------------------------------
# Colours / geometry
# ---------------------------------------------------------------------------
NAVY      = "1F3B5C"   # header background
EYEBROW   = "9DB2CC"   # header eyebrow small-caps text
GRAY_BOX  = "EDF0F4"   # problem box background
BLUE_ACC  = "2E5C8A"   # problem left accent
MINT      = "E9F3EC"   # given/required background
GREEN     = "2E7D57"   # given/required + solution labels
GRAYLINE  = "C9CDD3"   # rules / dividers
GOLD_BG   = "FBF3D9"   # answer box background
GOLD_BD   = "C9A227"   # answer box border
GOLD_TX   = "9A7B12"   # answer label text
PURPLE_BG = "F1ECF9"   # teacher-tip background
PURPLE    = "6B4E9E"   # teacher-tip accent + label
INK       = "222222"   # body text
GRAYTX    = "6E7680"   # muted annotation text

CONTENT_W = 10080      # usable width in twips (letter, 0.75" margins)

# ---------------------------------------------------------------------------
# XML helpers
# ---------------------------------------------------------------------------
def esc(s):
    return (s.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;"))

# ---------- OMML mini-compiler ---------------------------------------------
# Mini-language:
#   \frac{A}{B}   fraction
#   \sqrt{A}      square root
#   \u{TEXT}      upright roman text (units / words)  -- literal inside braces
#   {...}         group (single atom for sub/sup base)
#   _{...} ^{...} subscript / superscript on preceding atom
#   letters       -> italic math ; digits/operators -> upright math

def _sty(val):
    return '<m:rPr><m:sty m:val="%s"/></m:rPr>' % val

def _run(text, sty):
    return '<m:r>%s<m:t xml:space="preserve">%s</m:t></m:r>' % (_sty(sty), esc(text))

def run_text(buf, bold=False):
    """Split into alpha (italic) vs non-alpha (upright) runs."""
    out = []
    i = 0
    n = len(buf)
    while i < n:
        j = i
        alpha = buf[i].isalpha()
        while j < n and buf[j].isalpha() == alpha:
            j += 1
        seg = buf[i:j]
        if alpha:
            sty = "bi" if bold else "i"
        else:
            sty = "b" if bold else "p"
        out.append(_run(seg, sty))
        i = j
    return "".join(out)

def read_group(s, i):
    """s[i] == '{' ; return (parsed_xml_of_inner, index_after_close)."""
    assert s[i] == '{'
    depth = 1
    j = i + 1
    while j < len(s) and depth:
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                break
        j += 1
    inner = s[i + 1:j]
    return inner, j + 1

def read_raw(s, i):
    assert s[i] == '{'
    depth = 1
    j = i + 1
    while j < len(s) and depth:
        if s[j] == '{':
            depth += 1
        elif s[j] == '}':
            depth -= 1
            if depth == 0:
                break
        j += 1
    return s[i + 1:j], j + 1

def parse(s, bold=False):
    atoms = []
    buf = ""

    def flush():
        nonlocal buf
        if buf:
            atoms.append(run_text(buf, bold))
            buf = ""

    i = 0
    while i < len(s):
        c = s[i]
        if c == '\\':
            flush()
            if s.startswith('\\frac', i):
                num, i = read_group(s, i + 5)
                den, i = read_group(s, i)
                atoms.append('<m:f><m:fPr><m:type m:val="bar"/></m:fPr>'
                             '<m:num>%s</m:num><m:den>%s</m:den></m:f>'
                             % (parse(num, bold), parse(den, bold)))
                continue
            if s.startswith('\\sqrt', i):
                arg, i = read_group(s, i + 5)
                atoms.append('<m:rad><m:radPr><m:degHide m:val="1"/></m:radPr>'
                             '<m:deg/><m:e>%s</m:e></m:rad>' % parse(arg, bold))
                continue
            if s.startswith('\\u', i):
                txt, i = read_raw(s, i + 2)
                atoms.append(_run(txt, "b" if bold else "p"))
                continue
            buf += c
            i += 1
            continue
        if c == '{':
            flush()
            inner, i = read_group(s, i)
            atoms.append(parse(inner, bold))
            continue
        if c in '_^':
            # determine base
            if buf:
                if len(buf) > 1:
                    atoms.append(run_text(buf[:-1], bold))
                base = run_text(buf[-1], bold)
                buf = ""
            else:
                base = atoms.pop() if atoms else ""
            script, i = read_group(s, i + 1)
            script = parse(script, bold)
            if c == '_':
                atoms.append('<m:sSub><m:e>%s</m:e><m:sub>%s</m:sub></m:sSub>'
                             % (base, script))
            else:
                atoms.append('<m:sSup><m:e>%s</m:e><m:sup>%s</m:sup></m:sSup>'
                             % (base, script))
            continue
        buf += c
        i += 1
    flush()
    return "".join(atoms)

def omath(s, bold=False):
    body = parse(s, bold)
    if not body:
        return ""
    return '<m:oMath>%s</m:oMath>' % body

# ---------- run / paragraph helpers ----------------------------------------
def wrun(text, bold=False, italic=False, color=INK, sz=22, caps=False,
         spacing=None, font=None):
    rpr = []
    if font:
        rpr.append('<w:rFonts w:ascii="%s" w:hAnsi="%s"/>' % (font, font))
    if bold:
        rpr.append('<w:b/>')
    if italic:
        rpr.append('<w:i/>')
    if caps:
        rpr.append('<w:smallCaps/>')
    if spacing is not None:
        rpr.append('<w:spacing w:val="%d"/>' % spacing)
    if color:
        rpr.append('<w:color w:val="%s"/>' % color)
    rpr.append('<w:sz w:val="%d"/>' % sz)
    return ('<w:r><w:rPr>%s</w:rPr><w:t xml:space="preserve">%s</w:t></w:r>'
            % ("".join(rpr), esc(text)))

def para(inner, jc=None, before=40, after=40, ind=None, line=None, shd=None,
         keep=False):
    ppr = []
    if keep:
        ppr.append('<w:keepNext/>')
    spc = '<w:spacing w:before="%d" w:after="%d"%s/>' % (
        before, after, (' w:line="%d" w:lineRule="auto"' % line) if line else "")
    ppr.append(spc)
    if ind is not None:
        ppr.append('<w:ind w:left="%d"/>' % ind)
    if shd:
        ppr.append('<w:shd w:val="clear" w:fill="%s"/>' % shd)
    if jc:
        ppr.append('<w:jc w:val="%s"/>' % jc)
    return '<w:p><w:pPr>%s</w:pPr>%s</w:p>' % ("".join(ppr), inner)

def spacer(h=120):
    return ('<w:p><w:pPr><w:spacing w:before="0" w:after="0" '
            'w:line="%d" w:lineRule="exact"/></w:pPr></w:p>' % h)

# ---------- inline sequence (text with `math` segments) --------------------
def inline_seq(s, sz=22, color=INK, bold=False, italic=False):
    parts = s.split('`')
    out = []
    for k, seg in enumerate(parts):
        if k % 2 == 1:
            out.append(omath(seg))
        elif seg:
            out.append(wrun(seg, sz=sz, color=color, bold=bold, italic=italic))
    return "".join(out)

# ---------------------------------------------------------------------------
# Equation alignment table (col-0 LHS right-justified, col-1 '='+RHS left)
# ---------------------------------------------------------------------------
def eq_cell(math_xml, jc):
    ppr = ('<w:pPr><w:spacing w:before="30" w:after="30"/>'
           '<w:jc w:val="%s"/></w:pPr>' % jc)
    body = math_xml if math_xml else ""
    return ('<w:tc><w:tcPr><w:tcW w:w="0" w:type="auto"/>'
            '<w:vAlign w:val="center"/></w:tcPr>'
            '<w:p>%s%s</w:p></w:tc>' % (ppr, body))

def _clean_len(s):
    """Rough visible-width estimate for a mini-language string."""
    import re
    t = s
    t = re.sub(r'\\frac\{([^{}]*)\}\{([^{}]*)\}',
               lambda m: max(m.group(1), m.group(2), key=len), t)
    t = re.sub(r'\\sqrt', 'VVVV', t)
    t = re.sub(r'\\u', '', t)
    t = re.sub(r'[{}_^]', '', t)
    return len(t)

def eq_table(rows, bold=False, indent=650, c0=None, c1=None):
    # Auto-size columns to content so equations sit left-indented (like sample)
    lhs_max = max((_clean_len(l) for l, _ in rows if l), default=1)
    rhs_max = max((_clean_len(r) for _, r in rows if r), default=1)
    if c0 is None:
        c0 = min(max(lhs_max * 130 + 200, 500), 4200)
    if c1 is None:
        c1 = min(max(rhs_max * 130 + 260, 900), 6600)
    no_bd = ('<w:tblBorders>'
             + "".join('<w:%s w:val="none" w:sz="0" w:space="0"/>' % b for b in
                       ("top", "left", "bottom", "right", "insideH", "insideV"))
             + '</w:tblBorders>')
    tblpr = ('<w:tblPr><w:tblW w:w="0" w:type="auto"/>'
             '<w:tblInd w:w="%d" w:type="dxa"/>%s'
             '<w:tblLayout w:type="fixed"/>'
             '<w:tblCellMar>'
             '<w:top w:w="10" w:type="dxa"/><w:bottom w:w="10" w:type="dxa"/>'
             '<w:left w:w="40" w:type="dxa"/><w:right w:w="40" w:type="dxa"/>'
             '</w:tblCellMar></w:tblPr>' % (indent, no_bd))
    grid = '<w:tblGrid><w:gridCol w:w="%d"/><w:gridCol w:w="%d"/></w:tblGrid>' % (c0, c1)
    trs = []
    for lhs, rhs in rows:
        left = eq_cell(omath(lhs, bold) if lhs else "", "right")
        right = eq_cell(omath(rhs, bold) if rhs else "", "left")
        trs.append('<w:tr>%s%s</w:tr>' % (left, right))
    return '<w:tbl>%s%s%s</w:tbl>' % (tblpr, grid, "".join(trs))

# ---------------------------------------------------------------------------
# Boxes (single/twin-cell tables)
# ---------------------------------------------------------------------------
def borders(spec):
    # spec: dict side->(sz,color) ; missing sides = none
    out = ['<w:tcBorders>']
    for side in ("top", "left", "bottom", "right"):
        if side in spec:
            sz, col = spec[side]
            out.append('<w:%s w:val="single" w:sz="%d" w:space="0" w:color="%s"/>'
                       % (side, sz, col))
        else:
            out.append('<w:%s w:val="none" w:sz="0" w:space="0" w:color="auto"/>' % side)
    out.append('</w:tcBorders>')
    return "".join(out)

def box(content, fill=None, bspec=None, width=CONTENT_W, mar=170):
    tblpr = ('<w:tblPr><w:tblW w:w="%d" w:type="dxa"/>'
             '<w:tblLayout w:type="fixed"/>'
             '<w:tblCellMar>'
             '<w:top w:w="%d" w:type="dxa"/><w:bottom w:w="%d" w:type="dxa"/>'
             '<w:left w:w="%d" w:type="dxa"/><w:right w:w="%d" w:type="dxa"/>'
             '</w:tblCellMar></w:tblPr>' % (width, mar, mar, mar + 40, mar))
    grid = '<w:tblGrid><w:gridCol w:w="%d"/></w:tblGrid>' % width
    tcpr = ['<w:tcW w:w="%d" w:type="dxa"/>' % width]
    if fill:
        tcpr.append('<w:shd w:val="clear" w:fill="%s"/>' % fill)
    if bspec:
        tcpr.append(borders(bspec))
    tc = '<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % ("".join(tcpr), content)
    return '<w:tbl>%s%s<w:tr>%s</w:tr></w:tbl>' % (tblpr, grid, tc)

def twin_box(left_content, right_content, fill=MINT):
    w = CONTENT_W
    cw = w // 2
    tblpr = ('<w:tblPr><w:tblW w:w="%d" w:type="dxa"/>'
             '<w:tblLayout w:type="fixed"/>'
             '<w:tblCellMar>'
             '<w:top w:w="150" w:type="dxa"/><w:bottom w:w="150" w:type="dxa"/>'
             '<w:left w:w="200" w:type="dxa"/><w:right w:w="200" w:type="dxa"/>'
             '</w:tblCellMar></w:tblPr>' % w)
    grid = ('<w:tblGrid><w:gridCol w:w="%d"/><w:gridCol w:w="%d"/></w:tblGrid>'
            % (cw, w - cw))
    lcpr = ('<w:tcW w:w="%d" w:type="dxa"/>'
            '<w:shd w:val="clear" w:fill="%s"/>' % (cw, fill)) + borders(
        {"right": (6, "FFFFFF")})
    rcpr = ('<w:tcW w:w="%d" w:type="dxa"/>'
            '<w:shd w:val="clear" w:fill="%s"/>' % (w - cw, fill))
    lc = '<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % (lcpr, left_content)
    rc = '<w:tc><w:tcPr>%s</w:tcPr>%s</w:tc>' % (rcpr, right_content)
    return '<w:tbl>%s%s<w:tr>%s%s</w:tr></w:tbl>' % (tblpr, grid, lc, rc)

# ---------------------------------------------------------------------------
# High-level block builders
# ---------------------------------------------------------------------------
def header_box(eyebrow, title):
    p1 = para(wrun(eyebrow, bold=True, color=EYEBROW, sz=17, caps=True, spacing=60),
              before=20, after=40)
    p2 = para(wrun(title, bold=True, color="FFFFFF", sz=28), before=0, after=20)
    return box(p1 + p2, fill=NAVY, mar=200)

def label_para(text, color, sz=18, extra=None, before=20, after=80):
    inner = wrun(text, bold=True, color=color, sz=sz, caps=True, spacing=60)
    if extra:
        inner += extra
    return para(inner, before=before, after=after)

def problem_box(text):
    lbl = label_para("Problem", NAVY, sz=17, before=10, after=60)
    body = para(inline_seq(text), before=0, after=20)
    return box(lbl + body, fill=GRAY_BOX,
               bspec={"left": (30, BLUE_ACC)}, mar=180)

def bullet(inner, ind=290):
    ppr = ('<w:pPr><w:spacing w:before="30" w:after="30"/>'
           '<w:ind w:left="%d" w:hanging="%d"/></w:pPr>' % (ind, ind))
    dot = wrun("\u2022  ", color=GREEN, sz=22, bold=True)
    return '<w:p>%s%s%s</w:p>' % (ppr, dot, inner)

def given_required(given_items, required_items):
    # given_items: list of (mathstr, annotation)
    g = [label_para("Given", GREEN, sz=17, before=0, after=60)]
    for m, ann in given_items:
        inner = omath(m)
        if ann:
            inner += wrun("   " + ann, italic=True, color=GRAYTX, sz=19)
        g.append(bullet(inner))
    r = [label_para("Required", GREEN, sz=17, before=0, after=60)]
    for it in required_items:
        r.append(bullet(inline_seq(it)))
    return twin_box("".join(g), "".join(r))

def solution_heading():
    inner = (wrun("Solution", bold=True, color=GREEN, sz=22, caps=True, spacing=60)
             + wrun("    step-by-step derivation", italic=True, color=GRAYTX, sz=19))
    p = para(inner, before=160, after=20)
    rule = ('<w:p><w:pPr><w:spacing w:before="0" w:after="80"/>'
            '<w:pBdr><w:bottom w:val="single" w:sz="8" w:space="1" w:color="%s"/>'
            '</w:pBdr></w:pPr></w:p>' % GRAYLINE)
    return p + rule

def step_para(label, text):
    inner = (wrun(label + " ", bold=True, color=INK, sz=22)
             + inline_seq(text))
    return para(inner, before=100, after=30, keep=True)

def text_para(text):
    return para(inline_seq(text), before=40, after=30)

def tip_box(paras):
    lbl = para(wrun("\u25C6 Teacher Tip", bold=True, color=PURPLE, sz=18,
                    caps=True, spacing=40), before=10, after=50)
    body = "".join(para(inline_seq(p), before=0, after=40) for p in paras)
    return box(lbl + body, fill=PURPLE_BG, bspec={"left": (24, PURPLE)}, mar=170)

def answer_box(part_label, rows):
    inner = wrun("Answer", bold=True, color=GOLD_TX, sz=18, caps=True, spacing=60)
    if part_label:
        inner += wrun("    " + part_label, bold=True, color=GOLD_TX, sz=18,
                      caps=True, spacing=40)
    lbl = para(inner, before=6, after=50)
    eq = eq_table(rows, bold=True, indent=120)
    return box(lbl + eq, fill=GOLD_BG,
               bspec={"top": (8, GOLD_BD), "left": (8, GOLD_BD),
                      "bottom": (8, GOLD_BD), "right": (8, GOLD_BD)}, mar=160)

# ---------------------------------------------------------------------------
# Content data
# ---------------------------------------------------------------------------
EXAMPLES = []

# ---------- Example 1 ----------
EXAMPLES.append(dict(
    eyebrow="Guided Example 01", title="A Brick in Free Fall",
    problem=("A brick is dropped (zero initial speed) from the roof of a building. "
             "The brick strikes the ground in 1.90 s. Air resistance is ignored, so the "
             "brick is in free fall. (a) How tall, in meters, is the building? "
             "(b) What is the magnitude of the brick\u2019s velocity just before it reaches "
             "the ground?"),
    given=[("a = \u22129.80 \\u{m/s}^{2}", "free-fall acceleration; up is +y"),
           ("v_{0} = 0", "dropped \u21d2 zero initial speed"),
           ("t = 1.90 \\u{s}", "time to fall roof \u2192 ground"),
           ("y_{0} = 0", "origin placed at the roof")],
    required=["(a) height of the building, in meters",
              "(b) magnitude of the impact velocity"],
    blocks=[
        ("step", "Step 1.", "Choose the equation that connects `y`, `v_{0}`, `a`, and `t` "
                            "(no `v` needed) \u2014 this fits part (a) because we know `t` "
                            "but not the final velocity yet."),
        ("eq", [("y \u2212 y_{0}", "= v_{0}t + \\frac{1}{2}at^{2}")]),
        ("part", "Part (a).", "Isolate `y`, then substitute `v_{0}` = 0, `a` = \u22129.80 m/s\u00b2, "
                             "`t` = 1.90 s:"),
        ("eq", [("y", "= y_{0} + v_{0}t + \\frac{1}{2}at^{2}"),
                ("y", "= 0 + (0)(1.90) + \\frac{1}{2}(\u22129.80){(1.90)}^{2}")]),
        ("tip", ["The answer is negative because the brick ends up below where it started "
                 "\u2014 expected for a dropped object.",
                 "Since \u201cheight\u201d is a distance (always positive), we report the "
                 "size of the number, 17.69 m, and drop the minus sign."]),
        ("answer", "Part (A)", [("\\u{height}", "= 17.69 \\u{m}")]),
        ("step", "Step 2.", "Find the impact velocity with the velocity equation "
                            "`v = v_{0} + at`, which is already solved for `v`."),
        ("eq", [("v", "= v_{0} + at")]),
        ("part", "Part (b).", "Substitute `v_{0}` = 0, `a` = \u22129.80 m/s\u00b2, `t` = 1.90 s:"),
        ("eq", [("v", "= 0 + (\u22129.80)(1.90)")]),
        ("tip", ["The negative sign just means the velocity points downward "
                 "(our negative direction).",
                 "The question asks for the magnitude \u2014 how fast, not which way "
                 "\u2014 so we drop the sign."]),
        ("answer", "Part (B)", [("|v|", "= 18.62 \\u{m/s}")]),
    ]))

# ---------- Example 2 ----------
EXAMPLES.append(dict(
    eyebrow="Guided Example 02", title="Throwing a Stone Downward",
    problem=("You throw a stone straight down from the top of a tall tower; it leaves your "
             "hand at 8.00 m/s. Neglect air resistance. Take up as the positive y-direction "
             "and y = 0 where the stone leaves your hand. (a) Find the stone\u2019s position "
             "and velocity 1.50 s after release. (b) Find its velocity when it is 8.00 m "
             "below your hand."),
    given=[("v_{0} = \u22128.00 \\u{m/s}", "thrown downward \u21d2 negative (up is +)"),
           ("a = \u22129.80 \\u{m/s}^{2}", "free-fall acceleration points down"),
           ("y_{0} = 0", "origin at the hand")],
    required=["`y` and `v` at `t` = 1.50 s",
              "`v` when `y` = \u22128.00 m"],
    blocks=[
        ("tip", ["Even though the stone is thrown \u201cdown,\u201d keep up as positive "
                 "\u2014 so every downward quantity (v\u2080, a, and eventually y) is entered "
                 "as a negative number.",
                 "Mixing up a sign here is the most common mistake in this type of problem."]),
        ("step", "Step 1.", "Part (a) gives `t` directly, so use the position and velocity "
                            "equations that contain `t` \u2014 both are already solved for the "
                            "quantity we want."),
        ("eq", [("y", "= v_{0}t + \\frac{1}{2}at^{2}"),
                ("v", "= v_{0} + at")]),
        ("part", "Part (a).", "Substitute `v_{0}` = \u22128.00 m/s, `a` = \u22129.80 m/s\u00b2, "
                             "`t` = 1.50 s:"),
        ("eq", [("y", "= (\u22128.00)(1.50) + \\frac{1}{2}(\u22129.80){(1.50)}^{2}")]),
        ("eq", [("v", "= \u22128.00 + (\u22129.80)(1.50)")]),
        ("tip", ["Both answers are negative, which makes sense: the stone is below the hand "
                 "(negative y) and still moving downward (negative v).",
                 "Here we keep the signs, unlike Example 1, because the question asks for "
                 "position and velocity \u2014 which include direction."]),
        ("answer", "Part (A)", [("y", "= \u221223.03 \\u{m}"),
                                ("v", "= \u221222.70 \\u{m/s}")]),
        ("step", "Step 2.", "Part (b) gives a position instead of a time, so use the "
                            "equation that skips `t` entirely."),
        ("eq", [("v^{2}", "= v_{0}^{2} + 2a(y \u2212 y_{0})")]),
        ("part", "Part (b).", "Solve for `v` (take the square root), then substitute "
                             "`v_{0}` = \u22128.00 m/s, `a` = \u22129.80 m/s\u00b2, `y` = \u22128.00 m:"),
        ("eq", [("v", "= \u00b1\\sqrt{v_{0}^{2} + 2a(y \u2212 y_{0})}"),
                ("v", "= \u00b1\\sqrt{{(\u22128.00)}^{2} + 2(\u22129.80)(\u22128.00 \u2212 0)}")]),
        ("tip", ["Squaring erases the sign, so this equation always returns two answers, "
                 "+ and \u2212.",
                 "Physically the stone was thrown downward and gravity only speeds it up, so "
                 "it never reverses \u2014 the velocity stays negative: v = \u221214.86 m/s."]),
        ("answer", "Part (B)", [("v", "= \u221214.86 \\u{m/s}")]),
    ]))

# ---------- Example 3 ----------
EXAMPLES.append(dict(
    eyebrow="Guided Example 03", title="Putty Thrown Up Toward a Ceiling",
    problem=("You throw a glob of putty straight up toward a ceiling 3.60 m above your hand. "
             "The initial speed as it leaves your hand is 9.50 m/s. (a) What is the speed of "
             "the putty just before it strikes the ceiling? (b) How much time does it take to "
             "reach the ceiling?"),
    given=[("v_{0} = +9.50 \\u{m/s}", "thrown upward = positive"),
           ("a = \u22129.80 \\u{m/s}^{2}", "free-fall acceleration"),
           ("y_{0} = 0", "ceiling at y = +3.60 m")],
    required=["(a) speed at the ceiling",
              "(b) time to reach the ceiling"],
    blocks=[
        ("step", "Step 1.", "Part (a) gives a position, not a time, so skip `t` with "
                            "`v^{2} = v_{0}^{2} + 2a(y \u2212 y_{0})`."),
        ("eq", [("v^{2}", "= v_{0}^{2} + 2a(y \u2212 y_{0})")]),
        ("part", "Part (a).", "Solve for `v` (take the square root), then substitute "
                             "`v_{0}` = 9.50 m/s, `a` = \u22129.80 m/s\u00b2, `y` = 3.60 m:"),
        ("eq", [("v", "= \u00b1\\sqrt{v_{0}^{2} + 2a(y \u2212 y_{0})}"),
                ("v", "= \u00b1\\sqrt{{(9.50)}^{2} + 2(\u22129.80)(3.60)}")]),
        ("tip", ["Again a \u00b1 answer, so reason about direction. The highest the putty "
                 "could reach unobstructed is y\u2098\u2090\u2093 = v\u2080\u00b2/(2g) = "
                 "90.25/19.6 \u2248 4.60 m.",
                 "The ceiling (3.60 m) is below that maximum, so the putty is still rising "
                 "when it hits. Keep the positive root: v = +4.44 m/s."]),
        ("answer", "Part (A)", [("\\u{speed}", "= 4.44 \\u{m/s}")]),
        ("step", "Step 2.", "Part (b) asks for time and we know the position, so use "
                            "`y = v_{0}t + \\frac{1}{2}at^{2}`. Because `t` is squared, this is "
                            "a quadratic \u2014 rearrange to standard form and isolate `t` first."),
        ("eq", [("y", "= v_{0}t + \\frac{1}{2}at^{2}")]),
        ("text", "Write it as `\\frac{1}{2}at^{2} + v_{0}t \u2212 y = 0` and solve for `t` with the "
                 "quadratic formula:"),
        ("eq", [("\\frac{1}{2}at^{2} + v_{0}t \u2212 y", "= 0"),
                ("t", "= \\frac{\u2212v_{0} \u00b1 \\sqrt{v_{0}^{2} + 2ay}}{a}")]),
        ("text", "Substitute `v_{0}` = 9.50 m/s, `a` = \u22129.80 m/s\u00b2, `y` = 3.60 m:"),
        ("eq", [("t", "= \\frac{\u22129.50 \u00b1 \\sqrt{{(9.50)}^{2} + 2(\u22129.80)(3.60)}}{\u22129.80}")]),
        ("eq", [("t", "= 0.52 \\u{s}     \\u{or}     t = 1.42 \\u{s}")]),
        ("tip", ["A quadratic in t usually gives two roots, because the object passes a given "
                 "height twice \u2014 once going up, once coming down.",
                 "t = 0.52 s is the rising pass and t = 1.42 s the falling pass, but the "
                 "putty sticks on arrival \u2014 so only the smaller time is physical."]),
        ("answer", "Part (B)", [("t", "= 0.52 \\u{s}")]),
    ]))

# ---------- Example 4 ----------
EXAMPLES.append(dict(
    eyebrow="Guided Example 04", title="A Rock Tossed Straight Up",
    problem=("You throw a rock straight up and find it returns to your hand 3.60 s after it "
             "left. Neglect air resistance. What was the maximum height above your hand that "
             "the rock reached?"),
    given=[("\\u{total flight time} = 3.60 \\u{s}", "leaves hand \u2192 returns to hand"),
           ("a = \u22129.80 \\u{m/s}^{2}", "free-fall acceleration"),
           ("y_{start} = y_{end} = 0", "starts and ends at the hand")],
    required=["maximum height above the hand"],
    blocks=[
        ("tip", ["This problem never gives v\u2080 directly, so use symmetry: when an object "
                 "starts and ends at the same height, the trip up takes exactly as long as the "
                 "trip down.",
                 "So the time to reach the very top is half of the total flight time."]),
        ("step", "Step 1.", "Use symmetry to find the time to reach maximum height \u2014 "
                            "isolate `t_{up}` as half the total flight time."),
        ("eq", [("t_{up}", "= \\frac{1}{2}t_{total}"),
                ("t_{up}", "= \\frac{1}{2}(3.60 \\u{s}) = 1.80 \\u{s}")]),
        ("step", "Step 2.", "At maximum height the rock is momentarily at rest (`v` = 0). "
                            "Use `v = v_{0} + at` and solve for `v_{0}`."),
        ("eq", [("v", "= v_{0} + at"),
                ("v_{0}", "= v \u2212 at = \u2212at_{up}"),
                ("v_{0}", "= \u2212(\u22129.80)(1.80) = 17.6 \\u{m/s}")]),
        ("tip", ["We used t = 1.80 s here (time to the top, where v = 0) \u2014 not 3.60 s.",
                 "Plugging in the full 3.60 s would answer a different question: the velocity "
                 "back at the hand, not at the peak."]),
        ("step", "Step 3.", "Find the maximum height with `v^{2} = v_{0}^{2} + 2a(y \u2212 y_{0})`, "
                            "using `v` = 0 and `y \u2212 y_{0}` = `h`. Since `v_{0}` = `\u2212at_{up}`, "
                            "solving for `h` gives a form in `a` and `t_{up}` only:"),
        ("eq", [("0", "= v_{0}^{2} + 2ah"),
                ("h", "= \\frac{\u2212v_{0}^{2}}{2a} = \u2212\\frac{1}{2}at_{up}^{2}")]),
        ("text", "Substitute `a` = \u22129.80 m/s\u00b2 and `t_{up}` = 1.80 s:"),
        ("eq", [("h", "= \u2212\\frac{1}{2}(\u22129.80){(1.80)}^{2}")]),
        ("answer", "", [("\\u{maximum height}", "= 15.88 \\u{m}")]),
    ]))

# ---------------------------------------------------------------------------
# Assemble document body
# ---------------------------------------------------------------------------
def build_body():
    body = []
    # Title + intro
    body.append(para(wrun("Free Fall & Vertical Motion", bold=True, color=NAVY, sz=36),
                     before=0, after=20))
    body.append(para(wrun("Guided Examples", bold=True, color=GREEN, sz=24, caps=True,
                          spacing=40), before=0, after=80))
    body.append(para(inline_seq("Each example uses `g` = 9.80 m/s\u00b2 for the free-fall "
                                 "acceleration and follows the Given \u2192 Required \u2192 "
                                 "Solution method. Purple Teacher Tip boxes explain "
                                 "the reasoning behind the trickiest steps.",
                                 color=GRAYTX, italic=True, sz=20), after=120))

    for ex in EXAMPLES:
        body.append(spacer(160))
        body.append(header_box(ex["eyebrow"], ex["title"]))
        body.append(spacer(120))
        body.append(problem_box(ex["problem"]))
        body.append(spacer(120))
        body.append(given_required(ex["given"], ex["required"]))
        body.append(spacer(60))
        body.append(solution_heading())
        for blk in ex["blocks"]:
            kind = blk[0]
            if kind == "step":
                body.append(step_para(blk[1], blk[2]))
            elif kind == "part":
                body.append(step_para(blk[1], blk[2]))
            elif kind == "text":
                body.append(text_para(blk[1]))
            elif kind == "eq":
                body.append(spacer(40))
                body.append(eq_table(blk[1]))
                body.append(spacer(40))
            elif kind == "tip":
                body.append(spacer(60))
                body.append(tip_box(blk[1]))
                body.append(spacer(60))
            elif kind == "answer":
                body.append(spacer(60))
                body.append(answer_box(blk[1], blk[2]))
                body.append(spacer(40))

    sect = ('<w:sectPr><w:pgSz w:w="12240" w:h="15840"/>'
            '<w:pgMar w:top="1080" w:right="1080" w:bottom="1080" w:left="1080" '
            'w:header="720" w:footer="720" w:gutter="0"/></w:sectPr>')
    return "".join(body) + sect

# ---------------------------------------------------------------------------
# Package parts
# ---------------------------------------------------------------------------
NS = ('xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
      'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math" '
      'xmlns:r="http://schemas.openxmlformats.org/officeDocument/2006/relationships" '
      'xmlns:wp="http://schemas.openxmlformats.org/drawingml/2006/wordprocessingDrawing"')

def document_xml():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:document %s><w:body>%s</w:body></w:document>' % (NS, build_body()))

def styles_xml():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:styles xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main">'
            '<w:docDefaults><w:rPrDefault><w:rPr>'
            '<w:rFonts w:ascii="Calibri" w:hAnsi="Calibri" w:cs="Calibri"/>'
            '<w:color w:val="%s"/><w:sz w:val="22"/><w:szCs w:val="22"/></w:rPr></w:rPrDefault>'
            '<w:pPrDefault><w:pPr><w:spacing w:after="40" w:line="264" w:lineRule="auto"/>'
            '</w:pPr></w:pPrDefault></w:docDefaults>'
            '<w:style w:type="paragraph" w:default="1" w:styleId="Normal">'
            '<w:name w:val="Normal"/></w:style></w:styles>' % INK)

def settings_xml():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<w:settings xmlns:w="http://schemas.openxmlformats.org/wordprocessingml/2006/main" '
            'xmlns:m="http://schemas.openxmlformats.org/officeDocument/2006/math">'
            '<m:mathPr><m:mathFont m:val="Cambria Math"/><m:brkBin m:val="before"/>'
            '<m:brkBinSub m:val="--"/><m:smallFrac m:val="0"/><m:dispDef/>'
            '<m:lMargin m:val="0"/><m:rMargin m:val="0"/><m:defJc m:val="centerGroup"/>'
            '<m:wrapIndent m:val="1440"/><m:intLim m:val="subSup"/>'
            '<m:naryLim m:val="undOvr"/></m:mathPr>'
            '<w:compat/></w:settings>')

def content_types():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Types xmlns="http://schemas.openxmlformats.org/package/2006/content-types">'
            '<Default Extension="rels" ContentType="application/vnd.openxmlformats-package.relationships+xml"/>'
            '<Default Extension="xml" ContentType="application/xml"/>'
            '<Override PartName="/word/document.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.document.main+xml"/>'
            '<Override PartName="/word/styles.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.styles+xml"/>'
            '<Override PartName="/word/settings.xml" ContentType="application/vnd.openxmlformats-officedocument.wordprocessingml.settings+xml"/>'
            '<Override PartName="/docProps/core.xml" ContentType="application/vnd.openxmlformats-package.core-properties+xml"/>'
            '<Override PartName="/docProps/app.xml" ContentType="application/vnd.openxmlformats-officedocument.extended-properties+xml"/>'
            '</Types>')

def root_rels():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/officeDocument" Target="word/document.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/package/2006/relationships/metadata/core-properties" Target="docProps/core.xml"/>'
            '<Relationship Id="rId3" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/extended-properties" Target="docProps/app.xml"/>'
            '</Relationships>')

def doc_rels():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Relationships xmlns="http://schemas.openxmlformats.org/package/2006/relationships">'
            '<Relationship Id="rId1" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/styles" Target="styles.xml"/>'
            '<Relationship Id="rId2" Type="http://schemas.openxmlformats.org/officeDocument/2006/relationships/settings" Target="settings.xml"/>'
            '</Relationships>')

def core_xml():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<cp:coreProperties xmlns:cp="http://schemas.openxmlformats.org/package/2006/metadata/core-properties" '
            'xmlns:dc="http://purl.org/dc/elements/1.1/">'
            '<dc:title>Free Fall &amp; Vertical Motion \u2014 Guided Examples</dc:title>'
            '<dc:creator>Instructional Design</dc:creator></cp:coreProperties>')

def app_xml():
    return ('<?xml version="1.0" encoding="UTF-8" standalone="yes"?>'
            '<Properties xmlns="http://schemas.openxmlformats.org/officeDocument/2006/extended-properties">'
            '<Application>Kiro</Application></Properties>')

def write_docx(path):
    parts = {
        "[Content_Types].xml": content_types(),
        "_rels/.rels": root_rels(),
        "word/document.xml": document_xml(),
        "word/styles.xml": styles_xml(),
        "word/settings.xml": settings_xml(),
        "word/_rels/document.xml.rels": doc_rels(),
        "docProps/core.xml": core_xml(),
        "docProps/app.xml": app_xml(),
    }
    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as z:
        for name, data in parts.items():
            z.writestr(name, data)
    # validate all xml well-formed
    import xml.dom.minidom as md
    for name, data in parts.items():
        if name.endswith(".xml") or name.endswith(".rels"):
            md.parseString(data.encode("utf-8"))
    print("wrote", path, os.path.getsize(path), "bytes; xml OK")

if __name__ == "__main__":
    write_docx("/projects/sandbox/physics/Guided-Examples-Free-Fall.docx")
