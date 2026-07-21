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

    # Layout: 1 column, multiple rows per page (grid = rows x 1 col with borders)
    # On 8.5x13 paper with tight margins, each questionnaire takes about ~3.2 inches height
    # So we can fit 4 rows per page in a single column
    # OR 2 columns x 2 rows = 4 per page but text would be too small
    # Let's do 1 column x 4 rows per page to keep original font size

    # Actually, re-reading user request: "grid type" and "maximize space"
    # The original is a half-page questionnaire. On 8.5x13 we can fit:
    # - 2 columns x 3 rows = 6 per page (with smaller margins), or
    # - 1 column x 4 rows = 4 per page
    # Let's try 2 columns x 3 rows = 6 per page for true grid

    # With 2 columns on 8.5in paper (minus margins), each column ~ 3.6 inches wide
    # That's tight for the text. Let's check: original text is 10pt in ~7.3in width
    # At half width (3.6in), 10pt would wrap a lot. Let's use 9pt and see.
    # 
    # Actually, looking at the original document content - it's meant to be a half-page slip.
    # "Grid type" likely means a table with visible borders (grid lines) for cutting.
    # Let me do 1 column with visible grid borders, fitting as many rows as possible.
    # On 8.5x13 with 0.5cm margins top/bottom, usable height ~ 12 in = ~864pt
    # Each questionnaire at 10pt with the content ~ about 2.8-3.2 inches
    # So 4 per page is safe. 4 x 12 pages = 48 questionnaires.

    # Let's try to maximize: use compact spacing to fit more per page
    # Testing shows we can likely fit 4 per page comfortably

    rows_per_page = 4
    total_questionnaires = 48  # at least 45
    total_pages = (total_questionnaires + rows_per_page - 1) // rows_per_page

    questionnaire_num = 1

    for page in range(total_pages):
        # Create a table with rows_per_page rows and 1 column
        rows_this_page = min(rows_per_page, total_questionnaires - page * rows_per_page)
        table = doc.add_table(rows=rows_this_page, cols=1)
        table.alignment = WD_TABLE_ALIGNMENT.CENTER

        # Set table width to full page width
        tbl = table._tbl
        tblPr = tbl.tblPr if tbl.tblPr is not None else OxmlElement('w:tblPr')
        tblW = OxmlElement('w:tblW')
        tblW.set(qn('w:w'), '5000')
        tblW.set(qn('w:type'), 'pct')  # 100% width
        tblPr.append(tblW)

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

        for row_idx in range(rows_this_page):
            cell = table.cell(row_idx, 0)
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
    print(f"Questionnaires per page: {rows_per_page}")
    print(f"Total pages: {total_pages}")


if __name__ == "__main__":
    create_document()
