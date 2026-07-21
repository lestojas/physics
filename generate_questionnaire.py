from docx import Document
from docx.shared import Inches, Pt, Cm, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH, WD_TAB_ALIGNMENT
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

# Light gray used for the questionnaire number and the "[x pts]" tags,
# matching the reference image.
GRAY = RGBColor(0x99, 0x99, 0x99)
FONT_NAME = "Calibri"


def set_cell_margins(cell, top=60, bottom=60, left=140, right=140):
    """Set cell margins in twips (1/20 pt)."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for side, val in [('top', top), ('bottom', bottom), ('start', left), ('end', right)]:
        node = OxmlElement(f'w:{side}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_row_cant_split(row):
    """Prevent a table row from being split across two pages."""
    trPr = row._tr.get_or_add_trPr()
    cant_split = OxmlElement('w:cantSplit')
    trPr.append(cant_split)


def add_run(paragraph, text, size=10.5, bold=False, italic=False, color=None):
    run = paragraph.add_run(text)
    run.font.size = Pt(size)
    run.font.name = FONT_NAME
    run.bold = bold
    run.italic = italic
    if color:
        run.font.color.rgb = color
    return run


def add_question_paragraph(cell, number_label, text_before_pts, pts_text):
    """Add a numbered question paragraph with a hanging indent, matching the
    reference layout: '1)' followed by a tab, then justified wrapped text,
    with the point value shown in gray at the end."""
    p = cell.add_paragraph()
    p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p.paragraph_format
    pf.left_indent = Inches(0.22)
    pf.first_line_indent = Inches(-0.22)
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    pf.tab_stops.add_tab_stop(Inches(0.22), WD_TAB_ALIGNMENT.LEFT)

    add_run(p, f"{number_label}\t")
    add_run(p, text_before_pts)
    add_run(p, " ")
    add_run(p, pts_text, color=GRAY)
    return p


def add_spacer(cell, height_pt=6):
    """Add a small blank paragraph used purely for vertical spacing."""
    p = cell.add_paragraph()
    pf = p.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    run = p.add_run("")
    run.font.size = Pt(height_pt * 0.5)
    return p


def add_questionnaire_to_cell(cell, number):
    """Add questionnaire content to a table cell, replicating the reference
    layout: gray italic questionnaire number top-right, bold title, subject,
    justified instructions with 'not' bolded, and two hanging-indent
    numbered questions with gray point values."""
    # Clear the cell's default empty paragraph
    for paragraph in cell.paragraphs:
        p_el = paragraph._element
        p_el.getparent().remove(p_el)

    set_cell_margins(cell)

    # --- Questionnaire No. PHYS1-SC2-XX (right-aligned, italic, gray) ---
    p_num = cell.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    pf = p_num.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(2)
    add_run(p_num, "Questionnaire No. ", size=10, italic=True, color=GRAY)
    add_run(p_num, f"PHYS1-SC2-{number:02d}", size=10, italic=True, color=GRAY)

    # --- SKILL CHECK 2 (left-aligned, bold, black) ---
    p_title = cell.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p_title.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    add_run(p_title, "SKILL CHECK 2", size=14, bold=True)

    # --- Physics 1 (left-aligned, regular, black) ---
    p_subject = cell.add_paragraph()
    p_subject.alignment = WD_ALIGN_PARAGRAPH.LEFT
    pf = p_subject.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    add_run(p_subject, "Physics 1", size=11)

    # --- Blank line ---
    add_spacer(cell, height_pt=8)

    # --- Instructions (justified, "Instructions:" and "not" bold) ---
    p_instr = cell.add_paragraph()
    p_instr.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    pf = p_instr.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)
    add_run(p_instr, "Instructions: ", size=10.5, bold=True)
    add_run(p_instr, "Do ", size=10.5)
    add_run(p_instr, "not", size=10.5, bold=True)
    add_run(
        p_instr,
        " write anything on this paper. Solve the problems using the "
        "Given-Required-Solution format. Show the isolation of the target "
        "variable before substituting any numerical values.",
        size=10.5,
    )

    # --- Blank line ---
    add_spacer(cell, height_pt=8)

    # --- Question 1 ---
    add_question_paragraph(
        cell,
        "1)",
        "A jet plane is cruising at 280 m/s when suddenly the pilot turns the "
        "engines to full throttle. After traveling 4.0 km, the jet moves with a "
        "speed of 380 m/s. What is the jet\u2019s acceleration, assuming it to be a "
        "constant acceleration?",
        "[5 pts]",
    )

    # --- Blank line ---
    add_spacer(cell, height_pt=8)

    # --- Question 2 ---
    add_question_paragraph(
        cell,
        "2)",
        "How long, in seconds, does it take for the air in your lungs to "
        "accelerate from rest to 150 km/h, assuming a constant acceleration of "
        "83 m/s\u00b2?",
        "[5 pts]",
    )


def create_document():
    doc = Document()

    # Set page size to 8.5 x 13 inches with comfortable margins so the grid
    # border does not sit flush against the paper edge.
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(13)
        section.top_margin = Inches(0.5)
        section.bottom_margin = Inches(0.5)
        section.left_margin = Inches(0.5)
        section.right_margin = Inches(0.5)

    # Remove the default empty paragraph
    if doc.paragraphs:
        p = doc.paragraphs[0]._element
        p.getparent().remove(p)

    total_questionnaires = 48  # at least 45
    cols_per_page = 2
    total_rows = (total_questionnaires + cols_per_page - 1) // cols_per_page  # 24

    # Build ONE continuous table for the whole document. Word paginates a
    # single table automatically, flowing as many full rows as fit onto each
    # page -- this maximizes the use of the 8.5x13 page without guessing a
    # fixed row count, while `cantSplit` guarantees a row (and therefore a
    # questionnaire) is never cut across a page break.
    table = doc.add_table(rows=total_rows, cols=cols_per_page)
    table.alignment = WD_TABLE_ALIGNMENT.CENTER

    tbl = table._tbl
    tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')

    tblW = OxmlElement('w:tblW')
    tblW.set(qn('w:w'), '5000')
    tblW.set(qn('w:type'), 'pct')  # 100% of the available width
    tblPr.append(tblW)

    tblLayout = OxmlElement('w:tblLayout')
    tblLayout.set(qn('w:type'), 'fixed')
    tblPr.append(tblLayout)

    # Visible grid borders (cutting guides)
    tblBorders = OxmlElement('w:tblBorders')
    for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
        border = OxmlElement(f'w:{border_name}')
        border.set(qn('w:val'), 'single')
        border.set(qn('w:sz'), '12')  # 1.5pt
        border.set(qn('w:space'), '0')
        border.set(qn('w:color'), '000000')
        tblBorders.append(border)
    tblPr.append(tblBorders)

    col_width = Inches(3.75)  # (8.5in - 1in margins) / 2 columns
    for col in table.columns:
        col.width = col_width

    questionnaire_num = 1
    for row_idx in range(total_rows):
        row = table.rows[row_idx]
        set_row_cant_split(row)
        for col_idx in range(cols_per_page):
            if questionnaire_num > total_questionnaires:
                break
            cell = table.cell(row_idx, col_idx)
            cell.width = col_width
            add_questionnaire_to_cell(cell, questionnaire_num)
            questionnaire_num += 1

    output_path = "/projects/sandbox/physics/PHYS1-SC2-Questionnaires.docx"
    doc.save(output_path)
    print(f"Document saved to: {output_path}")
    print(f"Total questionnaires: {total_questionnaires}")
    print(f"Grid: {cols_per_page} columns x {total_rows} rows (single continuous table)")
    print("Word will auto-paginate this table, packing as many full rows as fit per page.")


if __name__ == "__main__":
    create_document()
