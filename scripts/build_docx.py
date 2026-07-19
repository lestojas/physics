#!/usr/bin/env python3
"""
Builds "Problem Set 3 - Solution Key - Uniformly Accelerated Motion (Horizontal)"
as a .docx file, using native OMML equations (python-docx has no built-in
equation support, so OMML is generated directly -- see omml.py).

Run:  python3 build_docx.py
Output: ../Problem Set 3 - Solution Key.docx
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import docx
from docx.shared import Pt, RGBColor, Inches, Cm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from omml import (
    mrun, frac, sup, sub, sqrt, paren, boxed, oMath, oMathPara,
    add_inline_math, add_display_math, new_math_paragraph,
    V, N, PW, FRAC, PAREN, SQRT, BOX, cat, add_aligned_derivation, UPW, SUBX,
)
from style_helpers import (
    NAVY, GRAY_HEAD, GRAY_TEXT, RED, BLUE_ACCENT,
    SHADE_STATEMENT, SHADE_CALLOUT,
    set_cell_shading, set_cell_margins, remove_table_borders, set_table_borders,
    add_bottom_border, add_left_border, shade_paragraph, set_run,
    add_heading_text, add_plain_text, add_shaded_box, add_problem_heading,
    add_section_label, add_callout,
    add_statement_box, add_given_table, add_required_line,
    add_centered_display_eq, add_boxed_answer, add_note,
)

OUT_PATH = os.path.join(os.path.dirname(__file__), "..",
                         "Problem Set 3 - Solution Key.docx")


# ===========================================================================
# Document setup
# ===========================================================================

doc = docx.Document()

# Base style
style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

sec = doc.sections[0]
sec.left_margin = Inches(1.0)
sec.right_margin = Inches(1.0)
sec.top_margin = Inches(0.8)
sec.bottom_margin = Inches(0.8)


def add_spacer(h=6):
    p = doc.add_paragraph()
    p.paragraph_format.space_after = Pt(0)
    p.paragraph_format.space_before = Pt(0)
    p.runs  # no-op
    pf = p.paragraph_format
    pf.line_spacing = Pt(h)
    return p


def hr(color="BFBFBF", sz=6, space_before=4, space_after=10):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(space_before)
    p.paragraph_format.space_after = Pt(space_after)
    pPr = p._p.get_or_add_pPr()
    pBdr = OxmlElement("w:pBdr")
    bottom = OxmlElement("w:bottom")
    bottom.set(qn("w:val"), "single")
    bottom.set(qn("w:sz"), str(sz))
    bottom.set(qn("w:space"), "1")
    bottom.set(qn("w:color"), color)
    pBdr.append(bottom)
    pPr.append(pBdr)
    return p


# ===========================================================================
# COVER / TITLE PAGE  (mirrors the "PROBLEM SET 2 / Solution Key" sample)
# ===========================================================================

for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pPr = p._p.get_or_add_pPr()
pBdr = OxmlElement("w:pBdr")
left = OxmlElement("w:left")
left.set(qn("w:val"), "single")
left.set(qn("w:sz"), "18")
left.set(qn("w:space"), "8")
left.set(qn("w:color"), str(NAVY))
pBdr.append(left)
pPr.append(pBdr)
r = p.add_run("PROBLEM SET 3")
set_run(r, bold=True, size=26, color=NAVY, font="Calibri")

p2 = doc.add_paragraph()
p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
r2 = p2.add_run("Solution Key")
set_run(r2, bold=True, size=15, color=GRAY_HEAD)
p2.paragraph_format.space_after = Pt(26)

p3 = doc.add_paragraph()
p3.alignment = WD_ALIGN_PARAGRAPH.CENTER
r3 = p3.add_run("UNIFORMLY ACCELERATED MOTION (HORIZONTAL)")
set_run(r3, bold=True, italic=True, size=13, color=GRAY_HEAD)

p4 = doc.add_paragraph()
p4.alignment = WD_ALIGN_PARAGRAPH.CENTER
r4 = p4.add_run("Prepared by Philip Jayson Lestojas, ECE, ECT")
set_run(r4, italic=True, size=11, color=GRAY_TEXT)

doc.add_page_break()

print("Cover page built.")


# ===========================================================================
# QUICK REFERENCE: The Four Equations of Motion
# ===========================================================================

add_heading_text(doc, "Quick Reference: The Four Equations of Motion",
                  size=16, bold=True, color=NAVY, space_after=6)

add_plain_text(
    doc,
    "Each equation \u201chides\u201d one variable. To choose which equation to use, "
    "list what you are given and what you need, then pick the equation that "
    "leaves out the variable you neither have nor need.",
    size=10.5, italic=True, color=GRAY_TEXT, space_after=10,
)

# --- Table of the four equations ------------------------------------------

eq_table = doc.add_table(rows=5, cols=3)
eq_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(eq_table, color="BFBFBF", sz=4)

hdr = eq_table.rows[0].cells
headers = ["#", "Equation", "Variable NOT present"]
for c, htext in zip(hdr, headers):
    set_cell_shading(c, "1F4E79")
    set_cell_margins(c)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(htext)
    set_run(r, bold=True, size=10.5, color=RGBColor(0xFF, 0xFF, 0xFF))

def eq_row(idx, label, om_items, absent_desc):
    cells = eq_table.rows[idx].cells
    set_cell_margins(cells[0]); set_cell_margins(cells[1]); set_cell_margins(cells[2])
    p0 = cells[0].paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r0 = p0.add_run(label)
    set_run(r0, bold=True, size=10.5, color=NAVY)

    p1 = cells[1].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_inline_math(p1, oMath(*om_items))

    p2 = cells[2].paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.LEFT
    from style_helpers import add_rich_text, parse_var_text
    add_rich_text(p2, parse_var_text(absent_desc), italic=False, size=10, color=GRAY_TEXT)

# Eq.1  v = v_o + a t     -- absent: (x - x_o)
eq_row(1, "Eq. 1",
       cat(V('v'), N(' = '), V('v', 'o'), N(' + '), V('a'), V('t')),
       "(x \u2212 x\u2092)  \u2014  no displacement")

# Eq.2  x = x_o + v_o t + 1/2 a t^2   -- absent: v
eq_row(2, "Eq. 2",
       cat(V('x'), N(' = '), V('x', 'o'), N(' + '), V('v', 'o'), V('t'),
           N(' + '), FRAC(N('1'), N('2')), V('a'), PW(V('t'), '2')),
       "v  \u2014  no final velocity")

# Eq.3  v^2 = v_o^2 + 2 a (x - x_o)   -- absent: t
eq_row(3, "Eq. 3",
       cat(PW(V('v'), '2'), N(' = '), PW(V('v', 'o'), '2'), N(' + 2'), V('a'),
           PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o')))),
       "t  \u2014  no time")

# Eq.4  x = x_o + 1/2 (v_o + v) t   -- absent: a
eq_row(4, "Eq. 4",
       cat(V('x'), N(' = '), V('x', 'o'), N(' + '), FRAC(N('1'), N('2')),
           PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t')),
       "a  \u2014  no acceleration")

doc.add_paragraph().paragraph_format.space_after = Pt(4)

add_callout(doc, [
    ("How to use this table:  ",
     "List the variables the problem gives you and the variable it asks for. "
     "If a variable is missing from your list (neither given nor asked), find "
     "the equation that also doesn't contain it \u2014 that equation is your best "
     "(and often only) choice."),
])

add_callout(doc, [
    ("Transposition reminder:  ",
     "When solving for a variable, a term moves across the equal sign by "
     "\u201cflipping\u201d its operation \u2014 an added term becomes subtracted on "
     "the other side; a multiplying factor becomes a divisor; a squared term "
     "becomes affected by a square root."),
])

doc.add_page_break()

print("Quick reference section built.")


# ===========================================================================
# PROBLEM 1: The Fastest Tennis Serve
# ===========================================================================

add_problem_heading(doc, 1, "The Fastest Tennis Serve")

add_statement_box(
    doc,
    "In the fastest measured tennis serve, the ball left the racquet at "
    "73.14 m/s. A served tennis ball is typically in contact with the "
    "racquet for 30.0 ms and starts from rest. Assume constant "
    "acceleration. (a) What was the ball's acceleration during this serve? "
    "(b) How far did the ball travel during the serve?"
)

add_section_label(doc, "Given")
add_given_table(doc, [
    (cat(V('v', 'o')), "0 m/s", "\u201cStarts from rest\u201d means initial velocity is zero"),
    (cat(V('v')), "73.14 m/s", "Final speed as it leaves the racquet"),
    (cat(V('t')), "30.0 ms = 0.0300 s", "Convert ms \u2192 s (\u00f71000) for SI units"),
])

add_section_label(doc, "Required")
add_required_line(doc, [
    ("math", cat(V('a'), N(' = ?'))),
    ("math", cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = ? '), N("(distance traveled)"))),
])

add_section_label(doc, "Solution")

add_section_label(doc, "(a) Finding acceleration", color=GRAY_HEAD, size=11.5)
add_callout(doc, [
    ("Which equation?  ",
     "We are given v\u2092, v, and t. We are not given (and don't need) "
     "displacement (x \u2212 x\u2092). Eq. 1 is the one missing (x \u2212 x\u2092) \u2014 "
     "that's our match."),
])
add_centered_display_eq(doc, cat(V('v'), N(' = '), V('v', 'o'), N(' + '), V('a'), V('t')))
add_note(doc, "Derivation by transposition \u2014 isolate a:")

rows_1a = [
    (cat(V('v')), cat(V('v', 'o'), N(' + '), V('a'), V('t'))),
    (cat(V('v'), N(' \u2212 '), V('v', 'o')), cat(V('a'), V('t'))),
    (FRAC(cat(V('v'), N(' \u2212 '), V('v', 'o')), cat(V('t'))), cat(V('a'))),
]
annot_1a = [
    None,
    "transpose v\u2092: added on the right \u2192 subtracted on the left",
    "transpose t: multiplying a \u2192 becomes a divisor",
]
add_aligned_derivation(doc, rows_1a, annotations=annot_1a)

add_note(doc, "Substitute values:")
add_centered_display_eq(doc, cat(
    V('a'), N(' = '),
    FRAC(cat(N('73.14 m/s'), N(' \u2212 '), N('0 m/s')), cat(N('0.0300 s')))
))
add_boxed_answer(doc, cat(V('a'), N(' = 2.44 \u00d7 '), PW(N('10'), '3'), N('  m/'), UPW('s', '2')))
add_note(doc, "This is roughly 249 times the acceleration due to gravity "
              "(g = 9.8 m/s\u00b2) \u2014 that's how violent a tennis serve impact really is!")

add_section_label(doc, "(b) Finding distance traveled", color=GRAY_HEAD, size=11.5)
add_callout(doc, [
    ("Which equation?  ",
     "We now know v\u2092, v, t, and a from part (a). Since a was a rounded "
     "answer, reusing it could introduce rounding error, so it's safer to "
     "use the equation that does not need acceleration at all \u2014 Eq. 4, "
     "which is missing a."),
])
add_centered_display_eq(doc, cat(V('x'), N(' = '), V('x', 'o'), N(' + '),
                                  FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t')))
add_note(doc, "Here (x \u2212 x\u2092) is simply the distance traveled, so we solve directly.")
add_note(doc, "Derivation by transposition \u2014 isolate (x \u2212 x\u2092):")

rows_1b = [
    (cat(V('x')), cat(V('x', 'o'), N(' + '), FRAC(N('1'), N('2')),
                       PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t'))),
    (cat(V('x'), N(' \u2212 '), V('x', 'o')),
     cat(FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t'))),
]
annot_1b = [None, "transpose x\u2092: added on the right \u2192 subtracted on the left"]
add_aligned_derivation(doc, rows_1b, annotations=annot_1b)

add_note(doc, "Substitute values:")
add_centered_display_eq(doc, cat(
    V('x'), N(' \u2212 '), V('x', 'o'), N(' = '), FRAC(N('1'), N('2')),
    PAREN(cat(N('0 m/s'), N(' + '), N('73.14 m/s'))), N('(0.0300 s)')
))
add_boxed_answer(doc, cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 1.10 m')))

doc.add_page_break()

print("Problem 1 built.")


# ===========================================================================
# PROBLEM 2: The Fastest Pitched Baseball
# ===========================================================================

add_problem_heading(doc, 2, "The Fastest Pitched Baseball")

add_statement_box(
    doc,
    "The fastest measured pitched baseball left the pitcher's hand at a "
    "speed of 45.0 m/s. If the pitcher was in contact with the ball over a "
    "distance of 1.50 m and produced constant acceleration, (a) what "
    "acceleration did he give the ball, and (b) how much time did it take "
    "him to pitch it?"
)

add_section_label(doc, "Given")
add_given_table(doc, [
    (cat(V('v', 'o')), "0 m/s", "Ball starts at rest in the pitcher's hand before the throw"),
    (cat(V('v')), "45.0 m/s", "Speed as the ball leaves the hand"),
    (cat(V('x'), N(' \u2212 '), V('x', 'o')), "1.50 m", "Distance over which the hand accelerates the ball"),
])

add_section_label(doc, "Required")
add_required_line(doc, [
    ("math", cat(V('a'), N(' = ?'))),
    ("math", cat(V('t'), N(' = ?'))),
])

add_section_label(doc, "Solution")

add_section_label(doc, "(a) Finding acceleration", color=GRAY_HEAD, size=11.5)
add_callout(doc, [
    ("Which equation?  ",
     "We are given v\u2092, v, and (x \u2212 x\u2092). We are not given, and don't yet "
     "need, time t. Eq. 3 is the one missing t \u2014 that's our match."),
])
add_centered_display_eq(doc, cat(PW(V('v'), '2'), N(' = '), PW(V('v', 'o'), '2'),
                                  N(' + 2'), V('a'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o')))))
add_note(doc, "Derivation by transposition \u2014 isolate a:")

rows_2a = [
    (cat(PW(V('v'), '2')), cat(PW(V('v', 'o'), '2'), N(' + 2'), V('a'),
                                PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))))),
    (cat(PW(V('v'), '2'), N(' \u2212 '), PW(V('v', 'o'), '2')),
     cat(N('2'), V('a'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))))),
    (FRAC(cat(PW(V('v'), '2'), N(' \u2212 '), PW(V('v', 'o'), '2')),
          cat(N('2'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))))),
     cat(V('a'))),
]
annot_2a = [
    None,
    "transpose v\u2092\u00b2: added on the right \u2192 subtracted on the left",
    "transpose 2(x \u2212 x\u2092): multiplying a \u2192 becomes a divisor",
]
add_aligned_derivation(doc, rows_2a, annotations=annot_2a)

add_note(doc, "Substitute values:")
add_centered_display_eq(doc, cat(
    V('a'), N(' = '),
    FRAC(cat(PW(PAREN(N('45.0 m/s')), '2'), N(' \u2212 '), PW(N('0'), '2')), cat(N('2(1.50 m)')))
))
add_centered_display_eq(doc, cat(
    V('a'), N(' = '), FRAC(cat(N('2025 '), UPW('m', '2'), N('/'), UPW('s', '2')), cat(N('3.00 m')))
))
add_boxed_answer(doc, cat(V('a'), N(' = 675 m/'), UPW('s', '2')))

add_section_label(doc, "(b) Finding time", color=GRAY_HEAD, size=11.5)
add_callout(doc, [
    ("Which equation?  ",
     "We now know v\u2092, v, (x \u2212 x\u2092), and a (rounded). To avoid propagating "
     "rounding error from part (a), use the equation that does not need a "
     "\u2014 Eq. 4, missing acceleration."),
])
add_centered_display_eq(doc, cat(V('x'), N(' = '), V('x', 'o'), N(' + '),
                                  FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t')))
add_note(doc, "Derivation by transposition \u2014 isolate t:")

rows_2b = [
    (cat(V('x'), N(' \u2212 '), V('x', 'o')),
     cat(FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t'))),
    (cat(N('2'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o')))),
     cat(PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t'))),
    (FRAC(cat(N('2'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o')))),
          cat(V('v', 'o'), N(' + '), V('v'))),
     cat(V('t'))),
]
annot_2b = [
    "transpose x\u2092 (as before)",
    "transpose \u00bd: multiply both sides by 2 to clear the fraction",
    "transpose (v\u2092 + v): multiplying t \u2192 becomes a divisor",
]
add_aligned_derivation(doc, rows_2b, annotations=annot_2b)

add_note(doc, "Substitute values:")
add_centered_display_eq(doc, cat(
    V('t'), N(' = '),
    FRAC(cat(N('2(1.50 m)')), cat(N('0 m/s + 45.0 m/s')))
))
add_boxed_answer(doc, cat(V('t'), N(' = 0.0667 s  (66.7 ms)')))

doc.add_page_break()

print("Problem 2 built.")


# ===========================================================================
# PROBLEM 3: Airbag Survival Distance
# ===========================================================================

add_problem_heading(doc, 3, "Airbag Survival Distance")

add_statement_box(
    doc,
    "The human body can survive an acceleration trauma incident if the "
    "magnitude of the acceleration is less than 250 m/s\u00b2. If you are in an "
    "automobile accident with an initial speed of 105 km/h and are stopped "
    "by an airbag, over what minimum distance must the airbag stop you to "
    "survive?"
)

add_section_label(doc, "Given")
add_given_table(doc, [
    (cat(V('v', 'o')), "105 km/h", "Must convert to m/s (SI unit) before using our equations"),
    (cat(V('v')), "0 m/s", "The car (and you) come to a complete stop"),
    (cat(V('a')), "\u2212250 m/s\u00b2",
     "Use the maximum allowed deceleration magnitude \u2014 this gives the "
     "minimum stopping distance. The negative sign shows it opposes the "
     "direction of motion."),
])

add_note(doc, "Unit conversion:")
add_centered_display_eq(doc, cat(
    V('v', 'o'), N(' = 105 '), FRAC(N('km'), N('h')), N(' \u00d7 '),
    FRAC(N('1000 m'), N('1 km')), N(' \u00d7 '), FRAC(N('1 h'), N('3600 s')),
    N(' = 29.17 m/s')
))

add_section_label(doc, "Required")
add_required_line(doc, [
    ("math", cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = ? '), N("(minimum stopping distance)"))),
])

add_section_label(doc, "Solution")
add_callout(doc, [
    ("Which equation?  ",
     "We are given v\u2092, v, and a. We are not given, and don't need, time t. "
     "Eq. 3 is missing t \u2014 that's our match."),
])
add_centered_display_eq(doc, cat(PW(V('v'), '2'), N(' = '), PW(V('v', 'o'), '2'),
                                  N(' + 2'), V('a'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o')))))
add_note(doc, "Derivation by transposition \u2014 isolate (x \u2212 x\u2092):")

rows_3 = [
    (cat(PW(V('v'), '2'), N(' \u2212 '), PW(V('v', 'o'), '2')),
     cat(N('2'), V('a'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))))),
    (FRAC(cat(PW(V('v'), '2'), N(' \u2212 '), PW(V('v', 'o'), '2')), cat(N('2'), V('a'))),
     cat(V('x'), N(' \u2212 '), V('x', 'o'))),
]
annot_3 = ["transpose v\u2092\u00b2", "transpose 2a: multiplying \u2192 becomes a divisor"]
add_aligned_derivation(doc, rows_3, annotations=annot_3)

add_note(doc, "Substitute values (using the unrounded v\u2092 = 29.1667 m/s to avoid "
              "rounding error, consistent with the convention used in the other "
              "problems):")
add_centered_display_eq(doc, cat(
    V('x'), N(' \u2212 '), V('x', 'o'), N(' = '),
    FRAC(cat(PW(N('0'), '2'), N(' \u2212 '), PW(PAREN(N('29.17 m/s')), '2')),
         cat(N('2(\u2212250 m/'), UPW('s', '2'), N(')')))
))
add_centered_display_eq(doc, cat(
    V('x'), N(' \u2212 '), V('x', 'o'), N(' = '),
    FRAC(cat(N('\u2212850.7 '), UPW('m', '2'), N('/'), UPW('s', '2')),
         cat(N('\u2212500 m/'), UPW('s', '2')))
))
add_boxed_answer(doc, cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 1.70 m')))
add_note(doc, "Interpretation: The negative signs on top and bottom cancel \u2014 "
              "which makes sense, since a distance must be positive! The airbag "
              "(plus crumple zone) must stop you within at least 1.70 m, or the "
              "deceleration will exceed the survivable limit of 250 m/s\u00b2.")

doc.add_page_break()

print("Problem 3 built.")


# ===========================================================================
# PROBLEM 4: Block Sliding Down a Frictionless Incline
# ===========================================================================

add_problem_heading(doc, 4, "Block Sliding Down a Frictionless Incline")

add_statement_box(
    doc,
    "A small block has constant acceleration as it slides down a "
    "frictionless incline, released from rest. Its speed after traveling "
    "6.80 m is 3.80 m/s. What is its speed after traveling only 3.40 m "
    "(halfway down)?"
)

add_note(doc, "Strategy: this problem needs two stages. First, use the full "
              "trip (0 to 6.80 m) to find the constant acceleration a. Then "
              "apply that same a to the shorter trip (0 to 3.40 m) to find "
              "the speed at that point.", italic=True, color=BLUE_ACCENT)

disp1 = SUBX(PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))), '1')
disp2 = SUBX(PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))), '2')
v1 = SUBX(cat(V('v')), '1')
v2 = SUBX(cat(V('v')), '2')

add_section_label(doc, "Given")
add_given_table(doc, [
    (cat(V('v', 'o')), "0 m/s", "Released from rest at the top"),
    (cat(disp1), "6.80 m", "Full distance to the bottom"),
    (cat(v1), "3.80 m/s", "Speed at the bottom (end of full distance)"),
    (cat(disp2), "3.40 m", "The shorter distance we care about (exactly half of 6.80 m)"),
])

add_section_label(doc, "Required")
add_required_line(doc, [
    ("math", cat(v2, N(" = ?  \u2014 the speed when the block has traveled 3.40 m"))),
])

add_section_label(doc, "Solution")

add_section_label(doc, "Stage 1: Find the acceleration using the full 6.80 m trip",
                   color=GRAY_HEAD, size=11.5)
add_callout(doc, [
    ("Which equation?  ",
     "We know v\u2092, v\u2081, and (x \u2212 x\u2092)\u2081. We don't have or need t. Eq. 3 is "
     "missing t."),
])
add_centered_display_eq(doc, cat(PW(v1, '2'), N(' = '), PW(V('v', 'o'), '2'), N(' + 2'),
                                  V('a'), disp1))
add_note(doc, "Derivation by transposition \u2014 isolate a:")

rows_4s1 = [
    (cat(PW(v1, '2'), N(' \u2212 '), PW(V('v', 'o'), '2')),
     cat(N('2'), V('a'), disp1)),
    (FRAC(cat(PW(v1, '2'), N(' \u2212 '), PW(V('v', 'o'), '2')),
          cat(N('2'), disp1)),
     cat(V('a'))),
]
annot_4s1 = ["transpose v\u2092\u00b2", "transpose 2(x \u2212 x\u2092)\u2081: multiplying \u2192 becomes a divisor"]
add_aligned_derivation(doc, rows_4s1, annotations=annot_4s1)

add_note(doc, "Substitute values:")
add_centered_display_eq(doc, cat(
    V('a'), N(' = '),
    FRAC(cat(PW(PAREN(N('3.80 m/s')), '2'), N(' \u2212 0')), cat(N('2(6.80 m)')))
))
add_centered_display_eq(doc, cat(
    V('a'), N(' = '),
    FRAC(cat(N('14.44 '), UPW('m', '2'), N('/'), UPW('s', '2')), cat(N('13.6 m')))
))
add_centered_display_eq(doc, cat(V('a'), N(' = 1.06 m/'), UPW('s', '2')))

add_section_label(doc, "Stage 2: Use this acceleration to find the speed at 3.40 m",
                   color=GRAY_HEAD, size=11.5)
add_callout(doc, [
    ("Same equation, same reasoning  ",
     "we still don't know or need t, so Eq. 3 applies again, but now "
     "solving for v\u2082 instead of a."),
])
add_centered_display_eq(doc, cat(PW(v2, '2'), N(' = '), PW(V('v', 'o'), '2'), N(' + 2'),
                                  V('a'), disp2))
add_note(doc, "This is already solved for v\u2082\u00b2 \u2014 only one more transposition "
              "step remains: taking the square root to isolate v\u2082 itself.")
add_centered_display_eq(doc, cat(
    v2, N(' = '),
    SQRT(cat(PW(V('v', 'o'), '2'), N(' + 2'), V('a'), disp2))
))
add_note(doc, "Substitute values (use the unrounded a = 1.0618 m/s\u00b2 to avoid "
              "rounding error):")
add_centered_display_eq(doc, cat(
    v2, N(' = '),
    SQRT(cat(N('0 + 2(1.0618 m/'), UPW('s', '2'), N(')(3.40 m)')))
))
add_centered_display_eq(doc, cat(
    v2, N(' = '),
    SQRT(cat(N('7.22 '), UPW('m', '2'), N('/'), UPW('s', '2')))
))
add_boxed_answer(doc, cat(v2, N(' = 2.69 m/s')))

add_note(doc, "Sanity check: since v\u2092 = 0, speed is proportional to the square "
              "root of distance traveled. Half the distance does not give half "
              "the speed \u2014 it gives speed divided by \u221a2 \u2248 1.414. "
              "Check: 3.80 / 1.414 = 2.69 m/s \u2713.")

doc.add_page_break()

print("Problem 4 built.")


# ===========================================================================
# PROBLEM 5: Lamborghini Aventador S Acceleration
# ===========================================================================

add_problem_heading(doc, 5, "Lamborghini Aventador S Acceleration")

add_statement_box(
    doc,
    "A Lamborghini Aventador S can go from 0 to 60 mph in 2.7 s. Assume "
    "constant acceleration. (a) What is the magnitude of the acceleration? "
    "(b) How far has the car traveled when it reaches 60 mph?"
)

add_section_label(doc, "Given")
add_given_table(doc, [
    (cat(V('v', 'o')), "0 mph = 0 m/s", "Starts from rest"),
    (cat(V('v')), "60 mph", "Must convert to m/s"),
    (cat(V('t')), "2.7 s", "Time to reach 60 mph"),
])

add_note(doc, "Unit conversion:")
add_centered_display_eq(doc, cat(
    V('v'), N(' = 60 '), FRAC(N('mi'), N('h')), N(' \u00d7 '),
    FRAC(N('1609 m'), N('1 mi')), N(' \u00d7 '), FRAC(N('1 h'), N('3600 s')),
    N(' = 26.82 m/s')
))

add_section_label(doc, "Required")
add_required_line(doc, [
    ("math", cat(V('a'), N(' = ?'))),
    ("math", cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = ?'))),
])

add_section_label(doc, "Solution")

add_section_label(doc, "(a) Finding acceleration", color=GRAY_HEAD, size=11.5)
add_callout(doc, [
    ("Which equation?  ",
     "We are given v\u2092, v, and t. We are not given, and don't need, "
     "displacement. Eq. 1 is missing (x \u2212 x\u2092) \u2014 that's our match."),
])
add_centered_display_eq(doc, cat(V('v'), N(' = '), V('v', 'o'), N(' + '), V('a'), V('t')))
add_note(doc, "Derivation by transposition \u2014 isolate a (same steps as Problem 1):")

rows_5a = [
    (cat(V('v'), N(' \u2212 '), V('v', 'o')), cat(V('a'), V('t'))),
    (FRAC(cat(V('v'), N(' \u2212 '), V('v', 'o')), cat(V('t'))), cat(V('a'))),
]
annot_5a = ["transpose v\u2092", "transpose t"]
add_aligned_derivation(doc, rows_5a, annotations=annot_5a)

add_note(doc, "Substitute values:")
add_centered_display_eq(doc, cat(
    V('a'), N(' = '),
    FRAC(cat(N('26.82 m/s \u2212 0')), cat(N('2.7 s')))
))
add_boxed_answer(doc, cat(V('a'), N(' = 9.93 m/'), UPW('s', '2')))
add_note(doc, "That's about 1.01 g \u2014 you'd feel about your own body weight "
              "pushing you back into the seat!")

add_section_label(doc, "(b) Finding distance traveled", color=GRAY_HEAD, size=11.5)
add_callout(doc, [
    ("Which equation?  ",
     "We know v\u2092, v, t, and a (rounded). To avoid rounding error, use the "
     "equation missing a \u2014 Eq. 4."),
])
add_centered_display_eq(doc, cat(V('x'), N(' = '), V('x', 'o'), N(' + '),
                                  FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t')))
add_note(doc, "Derivation by transposition \u2014 isolate (x \u2212 x\u2092) (same steps as Problem 1):")

rows_5b = [
    (cat(V('x'), N(' \u2212 '), V('x', 'o')),
     cat(FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t'))),
]
add_aligned_derivation(doc, rows_5b, annotations=[None])

add_note(doc, "Substitute values:")
add_centered_display_eq(doc, cat(
    V('x'), N(' \u2212 '), V('x', 'o'), N(' = '),
    FRAC(N('1'), N('2')), PAREN(cat(N('0 + 26.82 m/s'))), N('(2.7 s)')
))
add_boxed_answer(doc, cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 36.2 m')))
add_note(doc, "For comparison, that's roughly the length of two and a half "
              "basketball courts, covered in under 3 seconds!")

doc.add_page_break()

print("Problem 5 built.")


# ===========================================================================
# SUMMARY TABLE OF FINAL ANSWERS
# ===========================================================================

add_heading_text(doc, "Summary Table of Final Answers", size=16, bold=True,
                  color=NAVY, space_after=8)

sum_table = doc.add_table(rows=6, cols=3)
sum_table.alignment = WD_TABLE_ALIGNMENT.CENTER
set_table_borders(sum_table, color="BFBFBF", sz=4)

hdr = sum_table.rows[0].cells
for c, htext in zip(hdr, ["Problem", "Part (a)", "Part (b)"]):
    set_cell_shading(c, "1F4E79")
    set_cell_margins(c)
    p = c.paragraphs[0]
    p.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p.add_run(htext)
    set_run(r, bold=True, size=10.5, color=RGBColor(0xFF, 0xFF, 0xFF))


def sum_row(idx, label, a_items, b_items):
    cells = sum_table.rows[idx].cells
    for c in cells:
        set_cell_margins(c)
    p0 = cells[0].paragraphs[0]
    p0.alignment = WD_ALIGN_PARAGRAPH.LEFT
    r0 = p0.add_run(label)
    set_run(r0, size=10.5)

    p1 = cells[1].paragraphs[0]
    p1.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if a_items:
        add_inline_math(p1, oMath(*a_items))
    else:
        r1 = p1.add_run("\u2014")
        set_run(r1, size=10.5)

    p2 = cells[2].paragraphs[0]
    p2.alignment = WD_ALIGN_PARAGRAPH.CENTER
    if b_items:
        add_inline_math(p2, oMath(*b_items))
    else:
        r2 = p2.add_run("\u2014")
        set_run(r2, size=10.5)


sum_row(1, "1. Tennis serve",
        cat(V('a'), N(' = 2.44 \u00d7 '), PW(N('10'), '3'), N(' m/'), UPW('s', '2')),
        cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 1.10 m')))
sum_row(2, "2. Baseball pitch",
        cat(V('a'), N(' = 675 m/'), UPW('s', '2')),
        cat(V('t'), N(' = 0.0667 s')))
sum_row(3, "3. Airbag",
        cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 1.70 m (minimum)')),
        None)
sum_row(4, "4. Incline block",
        cat(v2, N(' = 2.69 m/s at 3.40 m')),
        None)
sum_row(5, "5. Lamborghini",
        cat(V('a'), N(' = 9.93 m/'), UPW('s', '2')),
        cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 36.2 m')))

print("Summary table built.")

doc.save(OUT_PATH)
print("Saved final ->", OUT_PATH)
