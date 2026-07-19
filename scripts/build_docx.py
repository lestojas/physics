#!/usr/bin/env python3
"""
Builds "Problem Set 3 - Solution Key - Uniformly Accelerated Motion (Horizontal)"
as a .docx file matching the reference image format exactly:
  - Problem heading with underline
  - Shaded problem-statement box (italic)
  - Given: bold label, indented bullet equations with annotations
  - Required: bold label, indented list
  - Solution: bold label, left-justified derivations with aligned equals signs
  - Bold red final answers

Uses native OMML equations (python-docx has no built-in equation support,
so OMML is generated directly -- see omml.py).

Run:  python3 build_docx.py
Output: ../Problem Set 3 - Solution Key.docx
"""
import sys
import os
sys.path.insert(0, os.path.dirname(__file__))

import docx
from docx.shared import Pt, RGBColor, Inches, Cm, Emu
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

from omml import (
    mrun, frac, sup, sub, sqrt, paren, boxed, oMath, oMathPara,
    add_inline_math, add_display_math, new_math_paragraph,
    V, N, PW, FRAC, PAREN, SQRT, BOX, cat, UPW, SUBX,
)
from style_helpers import (
    NAVY, GRAY_HEAD, GRAY_TEXT, RED, BLUE_ACCENT,
    SHADE_STATEMENT, SHADE_CALLOUT,
    set_cell_shading, set_cell_margins, remove_table_borders, set_table_borders,
    add_bottom_border, shade_paragraph, set_run, parse_var_text, add_rich_text,
    _paint_math_red_bold,
)

OUT_PATH = os.path.join(os.path.dirname(__file__), "..",
                         "Problem Set 3 - Solution Key.docx")


# ===========================================================================
# Document setup
# ===========================================================================

doc = docx.Document()

style = doc.styles["Normal"]
style.font.name = "Calibri"
style.font.size = Pt(11)

sec = doc.sections[0]
sec.left_margin = Inches(1.0)
sec.right_margin = Inches(1.0)
sec.top_margin = Inches(0.8)
sec.bottom_margin = Inches(0.8)

INDENT = Pt(28)  # standard indentation for equation lines


# ===========================================================================
# Helper functions matching the reference image format
# ===========================================================================

def add_problem_heading(number):
    """Bold 'Problem N' with bottom border line."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(18)
    p.paragraph_format.space_after = Pt(6)
    r = p.add_run("Problem %d" % number)
    set_run(r, bold=True, size=14)
    add_bottom_border(p, color="000000", sz=6)
    return p


def add_statement_box(text):
    """Light gray shaded problem statement in italic."""
    table = doc.add_table(rows=1, cols=1)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    cell = table.rows[0].cells[0]
    set_cell_shading(cell, SHADE_STATEMENT)
    set_cell_margins(cell, top=100, bottom=100, left=150, right=150)
    set_table_borders(table, color="BFBFBF", sz=4)
    p = cell.paragraphs[0]
    p.paragraph_format.space_after = Pt(0)
    add_rich_text(p, parse_var_text(text), italic=True, size=10.5, color=GRAY_TEXT)
    return table


def add_label(text):
    """Bold section label like 'Given:', 'Required:', 'Solution:'."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(10)
    p.paragraph_format.space_after = Pt(4)
    r = p.add_run(text)
    set_run(r, bold=True, size=11)
    return p


def add_indented_text(text, indent=INDENT, italic=False, size=11, color=None,
                       bold=False, space_after=4):
    """Indented plain text line (for annotations, notes)."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = indent
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(0)
    add_rich_text(p, parse_var_text(text), italic=italic, size=size,
                   color=color, bold=bold)
    return p


def add_indented_math(om_items, indent=INDENT, space_after=4, space_before=0):
    """Left-justified, indented OMML equation line."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = indent
    p.paragraph_format.space_after = Pt(space_after)
    p.paragraph_format.space_before = Pt(space_before)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    add_inline_math(p, oMath(*om_items))
    return p


def add_aligned_eq(rows, indent=INDENT, space_after=2):
    """Left-justified equals-sign-aligned derivation block.

    rows: list of (lhs_items, rhs_items) or (lhs_items, rhs_items, annotation_str)
          lhs_items=None means continuation line (no LHS, no '=').

    Uses a borderless 3-column table (or 4 with annotation):
      [right-aligned LHS] [=] [left-aligned RHS] [annotation?]
    The table is left-justified with indent margin.
    """
    has_annot = any(len(r) > 2 and r[2] for r in rows)
    ncols = 4 if has_annot else 3
    table = doc.add_table(rows=len(rows), cols=ncols)
    table.alignment = WD_TABLE_ALIGNMENT.LEFT
    # Remove all borders
    remove_table_borders(table)

    # Set left indent on the table
    tblPr = table._tbl.tblPr
    tblInd = OxmlElement("w:tblInd")
    tblInd.set(qn("w:w"), str(int(indent)))
    tblInd.set(qn("w:type"), "dxa")
    tblPr.append(tblInd)

    for i, row_data in enumerate(rows):
        lhs = row_data[0]
        rhs = row_data[1]
        annot = row_data[2] if len(row_data) > 2 else None
        cells = table.rows[i].cells

        # LHS cell (right aligned)
        p_l = cells[0].paragraphs[0]
        p_l.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p_l.paragraph_format.space_after = Pt(space_after)
        p_l.paragraph_format.space_before = Pt(0)
        if lhs is not None:
            add_inline_math(p_l, oMath(*lhs))

        # "=" cell (centered, narrow)
        p_m = cells[1].paragraphs[0]
        p_m.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_m.paragraph_format.space_after = Pt(space_after)
        p_m.paragraph_format.space_before = Pt(0)
        if lhs is not None:
            add_inline_math(p_m, oMath(*N("=")))
        else:
            add_inline_math(p_m, oMath(*N("=")))

        # RHS cell (left aligned)
        p_r = cells[2].paragraphs[0]
        p_r.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_r.paragraph_format.space_after = Pt(space_after)
        p_r.paragraph_format.space_before = Pt(0)
        add_inline_math(p_r, oMath(*rhs))

        # Annotation cell
        if has_annot and annot:
            p_a = cells[3].paragraphs[0]
            p_a.alignment = WD_ALIGN_PARAGRAPH.LEFT
            p_a.paragraph_format.space_after = Pt(space_after)
            p_a.paragraph_format.space_before = Pt(0)
            add_rich_text(p_a, parse_var_text(annot), italic=True,
                          size=9, color=GRAY_TEXT)

    return table


def add_final_answer(om_items):
    """Bold red final answer line, left-justified with indent."""
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = INDENT
    p.paragraph_format.space_after = Pt(8)
    p.paragraph_format.space_before = Pt(2)
    p.alignment = WD_ALIGN_PARAGRAPH.LEFT
    om = oMath(*om_items)
    _paint_math_red_bold(om)
    add_inline_math(p, om)
    return p


def add_sub_label(text):
    """Sub-part label like '(a) t = 1 s:' in bold."""
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(4)
    add_rich_text(p, parse_var_text(text), bold=True, size=11, italic=False)
    return p


def add_note(text, indent=INDENT, italic=True, size=10, color=None):
    """Italic annotation/note line."""
    if color is None:
        color = GRAY_TEXT
    return add_indented_text(text, indent=indent, italic=italic,
                              size=size, color=color)


# ===========================================================================
# COVER / TITLE PAGE
# ===========================================================================

for _ in range(4):
    doc.add_paragraph()

p = doc.add_paragraph()
p.alignment = WD_ALIGN_PARAGRAPH.CENTER
pPr = p._p.get_or_add_pPr()
pBdr = OxmlElement("w:pBdr")
left_el = OxmlElement("w:left")
left_el.set(qn("w:val"), "single")
left_el.set(qn("w:sz"), "18")
left_el.set(qn("w:space"), "8")
left_el.set(qn("w:color"), "1F4E79")
pBdr.append(left_el)
pPr.append(pBdr)
r = p.add_run("PROBLEM SET 3")
set_run(r, bold=True, size=26, color=NAVY)

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
# PROBLEM 1: The Fastest Tennis Serve
# ===========================================================================

add_problem_heading(1)

add_statement_box(
    "In the fastest measured tennis serve, the ball left the racquet at "
    "73.14 m/s. A served tennis ball is typically in contact with the "
    "racquet for 30.0 ms and starts from rest. Assume constant "
    "acceleration. (a) What was the ball\u2019s acceleration during this serve? "
    "(b) How far did the ball travel during the serve?"
)

add_label("Given:")
add_indented_math(cat(V('v', 'o'), N(' = 0 m/s')))
add_note("\u201cStarts from rest\u201d means initial velocity is zero", indent=INDENT*2)
add_indented_math(cat(V('v'), N(' = 73.14 m/s')))
add_note("Final speed as it leaves the racquet", indent=INDENT*2)
add_indented_math(cat(V('t'), N(' = 30.0 ms = 0.0300 s')))
add_note("Convert ms \u2192 s (\u00f71000) for SI units", indent=INDENT*2)

add_label("Required:")
add_indented_text("(a) a = ?")
add_indented_text("(b) x \u2212 x\u2092 = ?  (distance traveled)")

add_label("Solution:")
add_note("Substitute each known into the appropriate kinematic equation.",
          indent=INDENT, italic=True, size=10.5, color=None)

add_sub_label("(a) Finding acceleration:")
add_note("We have v\u2092, v, and t but not displacement \u2192 use Eq. 1: v = v\u2092 + at")

add_aligned_eq([
    (cat(V('v')), cat(V('v', 'o'), N(' + '), V('a'), V('t'))),
    (cat(V('v'), N(' \u2212 '), V('v', 'o')), cat(V('a'), V('t'))),
    (cat(V('a')), cat(FRAC(cat(V('v'), N(' \u2212 '), V('v', 'o')), cat(V('t'))))),
    (cat(V('a')), cat(FRAC(cat(N('73.14 m/s \u2212 0 m/s')), cat(N('0.0300 s'))))),
])

add_final_answer(cat(V('a'), N(' = 2.44 \u00d7 '), PW(N('10'), '3'), N(' m/'), UPW('s', '2')))

add_sub_label("(b) Finding distance traveled:")
add_note("Avoid reusing rounded a \u2192 use Eq. 4 (missing a): x = x\u2092 + \u00bd(v\u2092 + v)t")

add_aligned_eq([
    (cat(V('x'), N(' \u2212 '), V('x', 'o')),
     cat(FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t'))),
    (None,
     cat(FRAC(N('1'), N('2')), PAREN(cat(N('0 + 73.14 m/s'))), N('(0.0300 s)'))),
])

add_final_answer(cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 1.10 m')))

doc.add_page_break()
print("Problem 1 built.")


# ===========================================================================
# PROBLEM 2: The Fastest Pitched Baseball
# ===========================================================================

add_problem_heading(2)

add_statement_box(
    "The fastest measured pitched baseball left the pitcher\u2019s hand at a "
    "speed of 45.0 m/s. If the pitcher was in contact with the ball over a "
    "distance of 1.50 m and produced constant acceleration, (a) what "
    "acceleration did he give the ball, and (b) how much time did it take "
    "him to pitch it?"
)

add_label("Given:")
add_indented_math(cat(V('v', 'o'), N(' = 0 m/s')))
add_note("Ball starts at rest in the pitcher\u2019s hand", indent=INDENT*2)
add_indented_math(cat(V('v'), N(' = 45.0 m/s')))
add_indented_math(cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 1.50 m')))

add_label("Required:")
add_indented_text("(a) a = ?")
add_indented_text("(b) t = ?")

add_label("Solution:")

add_sub_label("(a) Finding acceleration:")
add_note("We have v\u2092, v, and (x \u2212 x\u2092) but not t \u2192 use Eq. 3: v\u00b2 = v\u2092\u00b2 + 2a(x \u2212 x\u2092)")

add_aligned_eq([
    (cat(PW(V('v'), '2')), cat(PW(V('v', 'o'), '2'), N(' + 2'), V('a'),
                                PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))))),
    (cat(V('a')), cat(FRAC(cat(PW(V('v'), '2'), N(' \u2212 '), PW(V('v', 'o'), '2')),
                            cat(N('2'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))))))),
    (None, cat(FRAC(cat(PW(PAREN(N('45.0 m/s')), '2'), N(' \u2212 '), PW(N('0'), '2')),
                     cat(N('2(1.50 m)'))))),
    (None, cat(FRAC(cat(N('2025 '), UPW('m', '2'), N('/'), UPW('s', '2')),
                     cat(N('3.00 m'))))),
])

add_final_answer(cat(V('a'), N(' = 675 m/'), UPW('s', '2')))

add_sub_label("(b) Finding time:")
add_note("Avoid reusing rounded a \u2192 use Eq. 4 (missing a): x = x\u2092 + \u00bd(v\u2092 + v)t")

add_aligned_eq([
    (cat(V('x'), N(' \u2212 '), V('x', 'o')),
     cat(FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t'))),
    (cat(V('t')), cat(FRAC(cat(N('2'), PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o')))),
                            cat(V('v', 'o'), N(' + '), V('v'))))),
    (None, cat(FRAC(cat(N('2(1.50 m)')), cat(N('0 + 45.0 m/s'))))),
])

add_final_answer(cat(V('t'), N(' = 0.0667 s (66.7 ms)')))

doc.add_page_break()
print("Problem 2 built.")


# ===========================================================================
# PROBLEM 3: Airbag Survival Distance
# ===========================================================================

add_problem_heading(3)

add_statement_box(
    "The human body can survive an acceleration trauma incident if the "
    "magnitude of the acceleration is less than 250 m/s\u00b2. If you are in "
    "an automobile accident with an initial speed of 105 km/h and are "
    "stopped by an airbag, over what minimum distance must the airbag stop "
    "you to survive?"
)

add_label("Given:")
add_indented_math(cat(V('v', 'o'), N(' = 105 km/h')))
add_note("Must convert to m/s (SI unit)", indent=INDENT*2)
add_indented_math(cat(V('v'), N(' = 0 m/s')))
add_note("Come to a complete stop", indent=INDENT*2)
add_indented_math(cat(V('a'), N(' = \u2212250 m/'), UPW('s', '2')))
add_note("Maximum survivable deceleration (negative = opposing motion)", indent=INDENT*2)

add_label("Unit conversion:")
add_aligned_eq([
    (cat(V('v', 'o')),
     cat(N('105 '), FRAC(N('km'), N('h')), N(' \u00d7 '),
         FRAC(N('1000 m'), N('1 km')), N(' \u00d7 '), FRAC(N('1 h'), N('3600 s')))),
    (None, cat(N('29.17 m/s'))),
])

add_label("Required:")
add_indented_text("x \u2212 x\u2092 = ?  (minimum stopping distance)")

add_label("Solution:")
add_note("We have v\u2092, v, and a but not t \u2192 use Eq. 3: v\u00b2 = v\u2092\u00b2 + 2a(x \u2212 x\u2092)")

add_aligned_eq([
    (cat(V('x'), N(' \u2212 '), V('x', 'o')),
     cat(FRAC(cat(PW(V('v'), '2'), N(' \u2212 '), PW(V('v', 'o'), '2')),
              cat(N('2'), V('a'))))),
    (None,
     cat(FRAC(cat(PW(N('0'), '2'), N(' \u2212 '), PW(PAREN(N('29.17 m/s')), '2')),
              cat(N('2(\u2212250 m/'), UPW('s', '2'), N(')'))))),
    (None, cat(FRAC(cat(N('\u2212850.7 '), UPW('m', '2'), N('/'), UPW('s', '2')),
                     cat(N('\u2212500 m/'), UPW('s', '2'))))),
])

add_final_answer(cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 1.70 m')))

doc.add_page_break()
print("Problem 3 built.")


# ===========================================================================
# PROBLEM 4: Block Sliding Down a Frictionless Incline
# ===========================================================================

add_problem_heading(4)

add_statement_box(
    "A small block has constant acceleration as it slides down a "
    "frictionless incline, released from rest. Its speed after traveling "
    "6.80 m is 3.80 m/s. What is its speed after traveling only 3.40 m "
    "(halfway down)?"
)

disp1 = SUBX(PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))), '1')
disp2 = SUBX(PAREN(cat(V('x'), N(' \u2212 '), V('x', 'o'))), '2')
v1 = SUBX(cat(V('v')), '1')
v2 = SUBX(cat(V('v')), '2')

add_label("Given:")
add_indented_math(cat(V('v', 'o'), N(' = 0 m/s')))
add_note("Released from rest", indent=INDENT*2)
add_indented_math(cat(disp1, N(' = 6.80 m')))
add_indented_math(cat(v1, N(' = 3.80 m/s')))
add_note("Speed at the bottom (end of full distance)", indent=INDENT*2)
add_indented_math(cat(disp2, N(' = 3.40 m')))
add_note("The shorter distance (exactly half of 6.80 m)", indent=INDENT*2)

add_label("Required:")
add_indented_text("v\u2082 = ?  (speed at 3.40 m)")

add_label("Solution:")

add_sub_label("Stage 1: Find acceleration using the full 6.80 m trip")
add_note("We have v\u2092, v\u2081, and (x \u2212 x\u2092)\u2081 but not t \u2192 use Eq. 3")

add_aligned_eq([
    (cat(V('a')), cat(FRAC(cat(PW(v1, '2'), N(' \u2212 '), PW(V('v', 'o'), '2')),
                            cat(N('2'), disp1)))),
    (None, cat(FRAC(cat(PW(PAREN(N('3.80 m/s')), '2'), N(' \u2212 0')),
                     cat(N('2(6.80 m)'))))),
    (None, cat(FRAC(cat(N('14.44 '), UPW('m', '2'), N('/'), UPW('s', '2')),
                     cat(N('13.6 m'))))),
    (None, cat(N('1.06 m/'), UPW('s', '2'))),
])

add_sub_label("Stage 2: Find speed at 3.40 m")
add_note("Same equation (Eq. 3), solving for v\u2082")

add_aligned_eq([
    (cat(v2), cat(SQRT(cat(PW(V('v', 'o'), '2'), N(' + 2'), V('a'), disp2)))),
    (None, cat(SQRT(cat(N('0 + 2(1.0618 m/'), UPW('s', '2'), N(')(3.40 m)'))))),
    (None, cat(SQRT(cat(N('7.22 '), UPW('m', '2'), N('/'), UPW('s', '2'))))),
])

add_final_answer(cat(v2, N(' = 2.69 m/s')))

doc.add_page_break()
print("Problem 4 built.")


# ===========================================================================
# PROBLEM 5: Lamborghini Aventador S Acceleration
# ===========================================================================

add_problem_heading(5)

add_statement_box(
    "A Lamborghini Aventador S can go from 0 to 60 mph in 2.7 s. Assume "
    "constant acceleration. (a) What is the magnitude of the acceleration? "
    "(b) How far has the car traveled when it reaches 60 mph?"
)

add_label("Given:")
add_indented_math(cat(V('v', 'o'), N(' = 0 m/s')))
add_note("Starts from rest", indent=INDENT*2)
add_indented_math(cat(V('v'), N(' = 60 mph')))
add_note("Must convert to m/s", indent=INDENT*2)
add_indented_math(cat(V('t'), N(' = 2.7 s')))

add_label("Unit conversion:")
add_aligned_eq([
    (cat(V('v')), cat(N('60 '), FRAC(N('mi'), N('h')), N(' \u00d7 '),
                       FRAC(N('1609 m'), N('1 mi')), N(' \u00d7 '),
                       FRAC(N('1 h'), N('3600 s')))),
    (None, cat(N('26.82 m/s'))),
])

add_label("Required:")
add_indented_text("(a) a = ?")
add_indented_text("(b) x \u2212 x\u2092 = ?")

add_label("Solution:")

add_sub_label("(a) Finding acceleration:")
add_note("We have v\u2092, v, and t but not displacement \u2192 use Eq. 1: v = v\u2092 + at")

add_aligned_eq([
    (cat(V('a')), cat(FRAC(cat(V('v'), N(' \u2212 '), V('v', 'o')), cat(V('t'))))),
    (None, cat(FRAC(cat(N('26.82 m/s \u2212 0')), cat(N('2.7 s'))))),
])

add_final_answer(cat(V('a'), N(' = 9.93 m/'), UPW('s', '2')))

add_sub_label("(b) Finding distance traveled:")
add_note("Avoid reusing rounded a \u2192 use Eq. 4 (missing a): x = x\u2092 + \u00bd(v\u2092 + v)t")

add_aligned_eq([
    (cat(V('x'), N(' \u2212 '), V('x', 'o')),
     cat(FRAC(N('1'), N('2')), PAREN(cat(V('v', 'o'), N(' + '), V('v'))), V('t'))),
    (None, cat(FRAC(N('1'), N('2')), PAREN(cat(N('0 + 26.82 m/s'))), N('(2.7 s)'))),
])

add_final_answer(cat(V('x'), N(' \u2212 '), V('x', 'o'), N(' = 36.2 m')))

print("Problem 5 built.")


# ===========================================================================
# Save
# ===========================================================================

doc.save(OUT_PATH)
print("Saved ->", OUT_PATH)
