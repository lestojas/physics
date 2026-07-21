from docx import Document
from docx.shared import Inches, Pt, Cm, Emu, Twips
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT
from docx.oxml.ns import qn, nsdecls
from docx.oxml import parse_xml, OxmlElement
import copy


def set_cell_border(cell, **kwargs):
    """Set cell border properties."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcBorders = OxmlElement('w:tcBorders')
    for edge in ('start', 'top', 'end', 'bottom', 'insideH', 'insideV'):
        edge_data = kwargs.get(edge)
        if edge_data:
            element = OxmlElement(f'w:{edge}')
            for key in ('sz', 'val', 'color', 'space'):
                if key in edge_data:
                    element.set(qn(f'w:{key}'), str(edge_data[key]))
            tcBorders.append(element)
    tcPr.append(tcBorders)


def set_cell_margins(cell, top=0, bottom=0, left=100, right=100):
    """Set cell margins in twips."""
    tc = cell._tc
    tcPr = tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for side, val in [('top', top), ('bottom', bottom), ('start', left), ('end', right)]:
        node = OxmlElement(f'w:{side}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)


def set_paragraph_spacing(paragraph, before=0, after=0, line=240):
    """Set paragraph spacing."""
    pf = paragraph.paragraph_format
    pf.space_before = Pt(before)
    pf.space_after = Pt(after)
    if line:
        pf.line_spacing = Pt(line * 20 / 240)  # Convert twips-like to points


def add_questionnaire_to_cell(cell, number):
    """Add questionnaire content to a table cell, replicating the original format."""
    # Clear the cell (remove default empty paragraph)
    for paragraph in cell.paragraphs:
        p = paragraph._element
        p.getparent().remove(p)

    # Set cell margins for compact fit
    set_cell_margins(cell, top=80, bottom=80, left=120, right=120)

    # --- Questionnaire No. line (right-aligned) ---
    p_num = cell.add_paragraph()
    p_num.alignment = WD_ALIGN_PARAGRAPH.RIGHT
    run = p_num.add_run(f"Questionnaire No. PHYS1-SC2-{number:02d}")
    run.font.size = Pt(10)
    run.font.name = "Times New Roman"
    pf = p_num.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)

    # --- SKILL CHECK 2 (centered, bold) ---
    p_title = cell.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p_title.add_run("SKILL CHECK 2")
    run.bold = True
    run.font.size = Pt(10)
    run.font.name = "Times New Roman"
    pf = p_title.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)

    # --- Physics 1 (centered) ---
    p_subject = cell.add_paragraph()
    p_subject.alignment = WD_ALIGN_PARAGRAPH.CENTER
    run = p_subject.add_run("Physics 1")
    run.font.size = Pt(10)
    run.font.name = "Times New Roman"
    pf = p_subject.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)

    # --- Empty line ---
    # (skip - tighten layout)

    # --- Instructions ---
    p_instr = cell.add_paragraph()
    run_bold = p_instr.add_run("Instructions:")
    run_bold.bold = True
    run_bold.font.size = Pt(10)
    run_bold.font.name = "Times New Roman"
    run_text = p_instr.add_run(" Do not write anything on this paper. Solve the problems using the Given-Required-Solution format. Show the isolation of the target variable before substituting any numerical values.")
    run_text.font.size = Pt(10)
    run_text.font.name = "Times New Roman"
    pf = p_instr.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)

    # --- Question 1 ---
    p_q1 = cell.add_paragraph()
    run = p_q1.add_run("1) A jet plane is cruising at 280 m/s when suddenly the pilot turns the engines to full throttle. After traveling 4.0 km, the jet moves with a speed of 380 m/s. What is the jet\u2019s acceleration, assuming it to be a constant acceleration? [5 pts]")
    run.font.size = Pt(10)
    run.font.name = "Times New Roman"
    pf = p_q1.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(6)

    # --- Question 2 ---
    p_q2 = cell.add_paragraph()
    run = p_q2.add_run("2) How long, in seconds, does it take for the air in your lungs to accelerate from rest to 150 km/h, assuming a constant acceleration of 83 m/s\u00b2? [5 pts]")
    run.font.size = Pt(10)
    run.font.name = "Times New Roman"
    pf = p_q2.paragraph_format
    pf.space_before = Pt(0)
    pf.space_after = Pt(0)


def create_document():
    doc = Document()

    # Set page size to 8.5 x 13 inches
    for section in doc.sections:
        section.page_width = Inches(8.5)
        section.page_height = Inches(13)
        section.top_margin = Cm(0.5)
        section.bottom_margin = Cm(0.5)
        section.left_margin = Cm(0.5)
        section.right_margin = Cm(0.5)

    # Remove default empty paragraph
    if doc.paragraphs:
        p = doc.paragraphs[0]._element
        p.getparent().remove(p)

    # Layout: 2 columns x N rows per page (true grid, matching the original 2-column layout)
    # Page is 8.5 x 13 in with 0.5cm margins on every side.
    # Usable width  ~ 8.1 in  -> each column ~ 4.0 in wide
    # Usable height ~ 12.0 in -> with 3 rows per page, each row gets ~4.0 in of height,
    # which comfortably fits the questionnaire content at the narrower column width.
    #
    # 2 columns x 3 rows = 6 questionnaires per page
    # 48 questionnaires / 6 per page = 8 pages exactly.

    cols_per_page = 2
    rows_per_page = 3
    per_page = cols_per_page * rows_per_page
    total_questionnaires = 48  # at least 45
    total_pages = (total_questionnaires + per_page - 1) // per_page

    questionnaire_num = 1

    for page in range(total_pages):
        remaining = total_questionnaires - page * per_page
        items_this_page = min(per_page, remaining)
        rows_this_page = (items_this_page + cols_per_page - 1) // cols_per_page

        # Create a table with rows_this_page rows and 2 columns
        table = doc.add_table(rows=rows_this_page, cols=cols_per_page)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Set table width to full page width
        tbl = table._tbl
        tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
        tblW = OxmlElement('w:tblW')
        tblW.set(qn('w:w'), '5000')
        tblW.set(qn('w:type'), 'pct')  # 100% width
        tblPr.append(tblW)

        # Fixed layout so both columns are equal width regardless of content
        tblLayout = OxmlElement('w:tblLayout')
        tblLayout.set(qn('w:type'), 'fixed')
        tblPr.append(tblLayout)

        # Set table borders (visible grid for cutting)
        tblBorders = OxmlElement('w:tblBorders')
        for border_name in ['top', 'left', 'bottom', 'right', 'insideH', 'insideV']:
            border = OxmlElement(f'w:{border_name}')
            border.set(qn('w:val'), 'single')
            border.set(qn('w:sz'), '12')  # 1.5pt border
            border.set(qn('w:space'), '0')
            border.set(qn('w:color'), '000000')
            tblBorders.append(border)
        tblPr.append(tblBorders)

        # Force equal column widths (half the table width each)
        for col in table.columns:
            col.width = Inches(4.0)

        # Fill cells in row-major order: left-to-right, then next row
        for row_idx in range(rows_this_page):
            for col_idx in range(cols_per_page):
                if questionnaire_num > total_questionnaires:
                    break
                cell = table.cell(row_idx, col_idx)
                cell.width = Inches(4.0)
                add_questionnaire_to_cell(cell, questionnaire_num)
                questionnaire_num += 1

        # Add page break after each table (except last)
        if page < total_pages - 1:
            p = doc.add_paragraph()
            pf = p.paragraph_format
            pf.space_before = Pt(0)
            pf.space_after = Pt(0)
            # Add page break via XML
            run = p.add_run()
            br = OxmlElement('w:br')
            br.set(qn('w:type'), 'page')
            run._r.append(br)

    # Save
    output_path = "/projects/sandbox/physics/PHYS1-SC2-Questionnaires.docx"
    doc.save(output_path)
    print(f"Document saved to: {output_path}")
    print(f"Total questionnaires: {total_questionnaires}")
    print(f"Grid layout: {cols_per_page} columns x {rows_per_page} rows = {per_page} per page")
    print(f"Total pages: {total_pages}")


if __name__ == "__main__":
    create_document()
