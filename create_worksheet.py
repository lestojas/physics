"""
Kinematics Guided Derivation Worksheet
- Landscape 13" x 8.5" bond paper, narrow margins
- 4 parts side by side in columns
- Each part has its own: Activity Name, Name, Grade & Section, Date
- Dashed cut lines between columns
- Each step = one algebraic action, students write fully
- Monochrome grayscale aesthetic
- Answer Key = same layout but with answers filled in red
"""

from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor, Emu, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_CELL_VERTICAL_ALIGNMENT
from docx.enum.section import WD_ORIENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml


def set_cell_margins(cell, top=0, bottom=0, left=72, right=72):
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = parse_xml(
        f'<w:tcMar {nsdecls("w")}>'
        f'<w:top w:w="{top}" w:type="dxa"/>'
        f'<w:bottom w:w="{bottom}" w:type="dxa"/>'
        f'<w:left w:w="{left}" w:type="dxa"/>'
        f'<w:right w:w="{right}" w:type="dxa"/>'
        f'</w:tcMar>'
    )
    tcPr.append(tcMar)


def add_run(paragraph, text, bold=False, italic=False, size=Pt(9), color=None, font_name='Calibri'):
    run = paragraph.add_run(text)
    run.bold = bold
    run.italic = italic
    run.font.size = size
    run.font.name = font_name
    if color:
        run.font.color.rgb = RGBColor(*color)
    return run


def set_paragraph_spacing(paragraph, before=0, after=0, line=None):
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing = line


def set_paragraph_shading(paragraph, color):
    pPr = paragraph._p.get_or_add_pPr()
    shd = parse_xml(f'<w:shd {nsdecls("w")} w:val="clear" w:color="auto" w:fill="{color}"/>')
    pPr.append(shd)


def set_table_borders_none(table):
    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else parse_xml(f'<w:tblPr {nsdecls("w")}/>')
    borders = parse_xml(
        f'<w:tblBorders {nsdecls("w")}>'
        f'<w:top w:val="nil"/>'
        f'<w:left w:val="nil"/>'
        f'<w:bottom w:val="nil"/>'
        f'<w:right w:val="nil"/>'
        f'<w:insideH w:val="nil"/>'
        f'<w:insideV w:val="nil"/>'
        f'</w:tblBorders>'
    )
    tblPr.append(borders)


def set_dashed_right_border(cell):
    """Set a dashed right border on a cell (cut line)."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = parse_xml(
        f'<w:tcBorders {nsdecls("w")}>'
        f'<w:right w:val="dashed" w:sz="6" w:color="888888" w:space="0"/>'
        f'</w:tcBorders>'
    )
    tcPr.append(tcBorders)


def build_part_content(cell, part, is_answer_key=False):
    """Build the content for one part (one column) inside a table cell."""
    cell.vertical_alignment = WD_CELL_VERTICAL_ALIGNMENT.TOP
    set_cell_margins(cell, top=50, bottom=30, left=90, right=90)

    # Clear default paragraph
    cell.paragraphs[0].clear()

    # --- PART HEADER BANNER ---
    header_para = cell.paragraphs[0]
    header_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(header_para, before=0, after=1)
    set_paragraph_shading(header_para, "3D3D3D")
    add_run(header_para, f"  PART {part['letter']}: {part['title']}  ", bold=True, size=Pt(8.5), color=(255, 255, 255))

    # --- ACTIVITY NAME ---
    act_para = cell.add_paragraph()
    set_paragraph_spacing(act_para, before=4, after=1)
    add_run(act_para, "Activity: ", bold=True, size=Pt(7.5), color=(80, 80, 80))
    add_run(act_para, "Guided Derivation of Kinematic Equations", size=Pt(7.5), color=(60, 60, 60))

    # --- NAME ---
    name_para = cell.add_paragraph()
    set_paragraph_spacing(name_para, before=1, after=1)
    add_run(name_para, "Name: ", bold=True, size=Pt(7.5), color=(80, 80, 80))
    add_run(name_para, "______________________________________", size=Pt(7.5), color=(170, 170, 170))

    # --- GRADE & SECTION / DATE on one line ---
    gs_para = cell.add_paragraph()
    set_paragraph_spacing(gs_para, before=1, after=3)
    add_run(gs_para, "Grade & Section: ", bold=True, size=Pt(7.5), color=(80, 80, 80))
    add_run(gs_para, "_____________  ", size=Pt(7.5), color=(170, 170, 170))
    add_run(gs_para, "Date: ", bold=True, size=Pt(7.5), color=(80, 80, 80))
    add_run(gs_para, "___________", size=Pt(7.5), color=(170, 170, 170))

    # --- THIN SEPARATOR LINE ---
    sep_para = cell.add_paragraph()
    set_paragraph_spacing(sep_para, before=0, after=3)
    sep_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    add_run(sep_para, "\u2500" * 42, size=Pt(6), color=(190, 190, 190))

    # --- GOAL BOX ---
    goal_para = cell.add_paragraph()
    goal_para.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(goal_para, before=1, after=4)
    set_paragraph_shading(goal_para, "F0F0F0")
    add_run(goal_para, " GOAL:  ", bold=True, size=Pt(7.5), color=(100, 100, 100))
    add_run(goal_para, "Derive  ", size=Pt(7.5), color=(100, 100, 100))
    add_run(goal_para, part["goal"], bold=True, italic=True, size=Pt(9), color=(40, 40, 40))
    add_run(goal_para, " ", size=Pt(7.5))

    # --- STEPS ---
    for i, step_text in enumerate(part["steps"], 1):
        # Step instruction
        step_p = cell.add_paragraph()
        set_paragraph_spacing(step_p, before=2, after=1)
        add_run(step_p, f"{i}. ", bold=True, size=Pt(7.5), color=(60, 60, 60))
        add_run(step_p, step_text, size=Pt(7.5), color=(50, 50, 50))

        # Answer space or actual answer
        if is_answer_key:
            ans_p = cell.add_paragraph()
            set_paragraph_spacing(ans_p, before=1, after=2)
            add_run(ans_p, "    ")  # indent
            add_run(ans_p, part["answers"][i - 1], bold=True, italic=True, size=Pt(8.5), color=(200, 0, 0))
        else:
            # Blank writing space
            space_p = cell.add_paragraph()
            set_paragraph_spacing(space_p, before=0, after=4)
            add_run(space_p, "", size=Pt(14))


def create_worksheet():
    doc = Document()

    # --- Define all parts ---
    parts = [
        {
            "letter": "A",
            "title": "Deriving Kinematic Equation 1",
            "goal": "v = v\u2080 + at",
            "steps": [
                "Acceleration is defined as the rate of change of velocity over time. Write the defining formula for acceleration using delta notation.",
                "The change in velocity is \u0394v = v \u2212 v\u2080, and if timing starts at t = 0, then \u0394t = t. Substitute these into the definition you wrote above.",
                "Multiply both sides of your equation by t to eliminate the fraction. Write the result.",
                "Add v\u2080 to both sides of your equation to isolate v. Write the final equation.",
            ],
            "answers": [
                "a = \u0394v / \u0394t",
                "a = (v \u2212 v\u2080) / t",
                "at = v \u2212 v\u2080",
                "v = v\u2080 + at",
            ]
        },
        {
            "letter": "B",
            "title": "Deriving Kinematic Equation 4",
            "goal": "x = x\u2080 + \u00bd(v\u2080 + v)t",
            "steps": [
                "Average velocity is defined as total displacement over total time. Write the definition as a formula using v\u0304, \u0394x, and \u0394t.",
                "Displacement is \u0394x = x \u2212 x\u2080 and \u0394t = t. Substitute these into the formula you wrote above.",
                "Multiply both sides of your equation by t to clear the denominator. Write the result.",
                "Add x\u2080 to both sides to isolate x on one side. Write the result.",
                "Under constant acceleration, velocity changes linearly. The average of a linearly changing quantity equals the mean of its start and end values. Express v\u0304 as the mean of v\u2080 and v.",
                "In your equation from Step 4, replace v\u0304 with the expression you found in Step 5. Write the final equation.",
            ],
            "answers": [
                "v\u0304 = \u0394x / \u0394t",
                "v\u0304 = (x \u2212 x\u2080) / t",
                "v\u0304 \u00b7 t = x \u2212 x\u2080",
                "x = x\u2080 + v\u0304 \u00b7 t",
                "v\u0304 = (v\u2080 + v) / 2",
                "x = x\u2080 + \u00bd(v\u2080 + v)t",
            ]
        },
        {
            "letter": "C",
            "title": "Deriving Kinematic Equation 2",
            "goal": "x = x\u2080 + v\u2080t + \u00bdat\u00b2",
            "steps": [
                "Write down Equation 1: v = v\u2080 + at.",
                "Write down Equation 4: x = x\u2080 + \u00bd(v\u2080 + v)t.",
                "In Equation 4, replace v with the right-hand side of Equation 1. Write the full substitution without simplifying.",
                "Inside the brackets, combine the like terms v\u2080 + v\u2080 into a single term. Write the simplified expression.",
                "Distribute t into the bracket. Write the result.",
                "Distribute \u00bd to each term. Simplify the coefficients and write the final equation.",
            ],
            "answers": [
                "v = v\u2080 + at",
                "x = x\u2080 + \u00bd(v\u2080 + v)t",
                "x = x\u2080 + \u00bd(v\u2080 + v\u2080 + at)\u00b7t",
                "x = x\u2080 + \u00bd(2v\u2080 + at)\u00b7t",
                "x = x\u2080 + \u00bd(2v\u2080t + at\u00b2)",
                "x = x\u2080 + v\u2080t + \u00bdat\u00b2",
            ]
        },
        {
            "letter": "D",
            "title": "Deriving Kinematic Equation 3",
            "goal": "v\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)",
            "steps": [
                "Start with Equation 1: v = v\u2080 + at. Subtract v\u2080 from both sides. Write the result.",
                "Divide both sides of your equation by a to isolate t. Write t = ...",
                "Write the displacement equation from Equation 4: x \u2212 x\u2080 = \u00bd(v\u2080 + v)\u00b7t.",
                "Replace t with the expression you found in Step 2. Write the full substitution.",
                "Multiply the two factors in the numerator using the difference-of-squares identity: (v\u2080 + v)(v \u2212 v\u2080) = v\u00b2 \u2212 v\u2080\u00b2. Simplify.",
                "Multiply both sides by 2a to clear the denominator. Write the result.",
                "Add v\u2080\u00b2 to both sides to isolate v\u00b2. Write the final equation.",
            ],
            "answers": [
                "v \u2212 v\u2080 = at",
                "t = (v \u2212 v\u2080) / a",
                "x \u2212 x\u2080 = \u00bd(v\u2080 + v)\u00b7t",
                "x \u2212 x\u2080 = \u00bd(v\u2080 + v)(v \u2212 v\u2080) / a",
                "x \u2212 x\u2080 = (v\u00b2 \u2212 v\u2080\u00b2) / 2a",
                "2a(x \u2212 x\u2080) = v\u00b2 \u2212 v\u2080\u00b2",
                "v\u00b2 = v\u2080\u00b2 + 2a(x \u2212 x\u2080)",
            ]
        },
    ]

    # ============================================
    # PAGE 1: STUDENT WORKSHEET (BLANK)
    # ============================================
    section = doc.sections[0]
    section.orientation = WD_ORIENT.LANDSCAPE
    section.page_width = Inches(13)
    section.page_height = Inches(8.5)
    section.left_margin = Inches(0.3)
    section.right_margin = Inches(0.3)
    section.top_margin = Inches(0.3)
    section.bottom_margin = Inches(0.3)

    # Main table: 1 row x 4 columns
    table = doc.add_table(rows=1, cols=4)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders_none(table)

    # Set column widths
    col_width = Inches(3.1)
    for col in table.columns:
        for cell in col.cells:
            cell.width = col_width

    row = table.rows[0]
    for col_idx, part in enumerate(parts):
        cell = row.cells[col_idx]
        build_part_content(cell, part, is_answer_key=False)

        # Add dashed cut line between columns (not after the last one)
        if col_idx < 3:
            set_dashed_right_border(cell)

    # ============================================
    # PAGE 2: ANSWER KEY (same layout, answers in red)
    # ============================================
    doc.add_page_break()

    # Add a small "ANSWER KEY" label at top
    ak_label = doc.add_paragraph()
    ak_label.alignment = WD_ALIGN_PARAGRAPH.CENTER
    set_paragraph_spacing(ak_label, before=0, after=2)
    add_run(ak_label, "TEACHER\u2019S ANSWER KEY", bold=True, size=Pt(10), color=(150, 0, 0))

    # Answer key table: same 4-column layout
    ak_table = doc.add_table(rows=1, cols=4)
    ak_table.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders_none(ak_table)

    for col in ak_table.columns:
        for cell in col.cells:
            cell.width = col_width

    ak_row = ak_table.rows[0]
    for col_idx, part in enumerate(parts):
        cell = ak_row.cells[col_idx]
        build_part_content(cell, part, is_answer_key=True)

        if col_idx < 3:
            set_dashed_right_border(cell)

    # Save
    doc.save('/projects/sandbox/physics/kinematics-worksheet-4.docx')
    print("Worksheet saved: kinematics-worksheet-4.docx")


if __name__ == "__main__":
    create_worksheet()
