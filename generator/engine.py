# -*- coding: utf-8 -*-
"""Engine: OMML conversion (via pandoc) + python-docx low-level styling helpers."""
import copy
import hashlib
import subprocess
import os
from lxml import etree

from docx.oxml.ns import qn, nsmap
from docx.oxml import OxmlElement

PANDOC = "/projects/sandbox/tools/pandoc-3.1.11/bin/pandoc"

M = "http://schemas.openxmlformats.org/officeDocument/2006/math"
W = "http://schemas.openxmlformats.org/officeDocument/2006/wordprocessingml/2006/main"
NS = {"m": M, "w": W}

# ---------------------------------------------------------------------------
# OMML generation
# ---------------------------------------------------------------------------
_omml_cache = {}
_tmp = "/projects/sandbox/_omml_tmp"
os.makedirs(_tmp, exist_ok=True)


def _pandoc_to_docxxml(latex, display):
    wrapped = ("$$" + latex + "$$") if display else ("$" + latex + "$")
    key = hashlib.md5((("D" if display else "I") + latex).encode()).hexdigest()
    md = os.path.join(_tmp, key + ".md")
    dx = os.path.join(_tmp, key + ".docx")
    with open(md, "w", encoding="utf-8") as f:
        f.write(wrapped + "\n")
    subprocess.run([PANDOC, md, "-o", dx], check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.PIPE)
    import zipfile
    with zipfile.ZipFile(dx) as z:
        return z.read("word/document.xml")


def omath(latex, display=False, align_left=False):
    """Return a deep-copied lxml element: m:oMathPara (display) or m:oMath (inline)."""
    cache_key = (latex, display, align_left)
    if cache_key in _omml_cache:
        return copy.deepcopy(_omml_cache[cache_key])
    xml = _pandoc_to_docxxml(latex, display)
    root = etree.fromstring(xml)
    if display:
        el = root.find(".//m:oMathPara", NS)
        if el is None:  # fallback: wrap oMath
            el = root.find(".//m:oMath", NS)
        if align_left and el.tag == qn("m:oMathPara"):
            pr = el.find("m:oMathParaPr", NS)
            if pr is None:
                pr = etree.SubElement(el, qn("m:oMathParaPr"))
                el.insert(0, pr)
            jc = pr.find("m:jc", NS)
            if jc is None:
                jc = etree.SubElement(pr, qn("m:jc"))
            jc.set(qn("m:val"), "left")
    else:
        el = root.find(".//m:oMath", NS)
    _fill_empty_cells(el)
    el = copy.deepcopy(el)
    _omml_cache[cache_key] = el
    return copy.deepcopy(el)


def _fill_empty_cells(el):
    """Pandoc renders aligned continuation lines with empty <m:e/> alignment cells.
    Word hides these (plcHide), but LibreOffice/Google Docs draw a placeholder box.
    Inject an invisible zero-width run so the cell is non-empty and no box appears,
    while keeping the equal-sign alignment intact."""
    for e in el.iter(qn("m:e")):
        if len(e) == 0:
            r = etree.SubElement(e, qn("m:r"))
            t = etree.SubElement(r, qn("m:t"))
            t.set(qn("xml:space"), "preserve")
            t.text = "\u200b"  # zero-width space


# ---------------------------------------------------------------------------
# Low-level docx helpers
# ---------------------------------------------------------------------------

def _sub(parent, tag, **attrs):
    el = OxmlElement(tag)
    for k, v in attrs.items():
        el.set(qn(k), v)
    parent.append(el)
    return el


def set_cell_bg(cell, hexcolor):
    tcPr = cell._tc.get_or_add_tcPr()
    shd = OxmlElement("w:shd")
    shd.set(qn("w:val"), "clear")
    shd.set(qn("w:color"), "auto")
    shd.set(qn("w:fill"), hexcolor)
    tcPr.append(shd)


def set_cell_margins(cell, top=100, start=140, bottom=100, end=140):
    tcPr = cell._tc.get_or_add_tcPr()
    mar = OxmlElement("w:tcMar")
    for name, val in (("top", top), ("start", start), ("bottom", bottom), ("end", end)):
        e = OxmlElement("w:" + name)
        e.set(qn("w:w"), str(val))
        e.set(qn("w:type"), "dxa")
        mar.append(e)
    tcPr.append(mar)


def set_cell_borders(cell, **sides):
    """sides: left/right/top/bottom -> (sz_eighths, color) ; None means nil."""
    tcPr = cell._tc.get_or_add_tcPr()
    borders = OxmlElement("w:tcBorders")
    for side in ("top", "left", "bottom", "right"):
        e = OxmlElement("w:" + side)
        if side in sides and sides[side] is not None:
            sz, color = sides[side]
            e.set(qn("w:val"), "single")
            e.set(qn("w:sz"), str(sz))
            e.set(qn("w:space"), "0")
            e.set(qn("w:color"), color)
        else:
            e.set(qn("w:val"), "nil")
        borders.append(e)
    tcPr.append(borders)


def cell_valign(cell, val="center"):
    tcPr = cell._tc.get_or_add_tcPr()
    e = OxmlElement("w:vAlign")
    e.set(qn("w:val"), val)
    tcPr.append(e)


def no_table_borders(table):
    tblPr = table._tbl.tblPr
    borders = OxmlElement("w:tblBorders")
    for side in ("top", "left", "bottom", "right", "insideH", "insideV"):
        e = OxmlElement("w:" + side)
        e.set(qn("w:val"), "nil")
        borders.append(e)
    tblPr.append(borders)


def set_table_layout_fixed(table, total_w):
    tblPr = table._tbl.tblPr
    layout = OxmlElement("w:tblLayout")
    layout.set(qn("w:type"), "fixed")
    tblPr.append(layout)
    tw = OxmlElement("w:tblW")
    tw.set(qn("w:w"), str(total_w))
    tw.set(qn("w:type"), "dxa")
    tblPr.append(tw)


def set_col_widths(table, widths):
    # set grid + each cell width
    for row in table.rows:
        for idx, cell in enumerate(row.cells):
            tcPr = cell._tc.get_or_add_tcPr()
            tcW = tcPr.find(qn("w:tcW"))
            if tcW is None:
                tcW = OxmlElement("w:tcW")
                tcPr.append(tcW)
            tcW.set(qn("w:w"), str(widths[idx]))
            tcW.set(qn("w:type"), "dxa")


def p_spacing(paragraph, before=0, after=80, line=None):
    pPr = paragraph._p.get_or_add_pPr()
    sp = pPr.find(qn("w:spacing"))
    if sp is None:
        sp = OxmlElement("w:spacing")
        pPr.append(sp)
    sp.set(qn("w:before"), str(before))
    sp.set(qn("w:after"), str(after))
    if line is not None:
        sp.set(qn("w:line"), str(line))
        sp.set(qn("w:lineRule"), "auto")


def p_keep_next(paragraph):
    pPr = paragraph._p.get_or_add_pPr()
    _sub(pPr, "w:keepNext")


def add_run(paragraph, text, bold=False, italic=False, color=None, size=None,
            font=None, caps=False):
    r = paragraph.add_run(text)
    r.bold = bold
    r.italic = italic
    rpr = r._r.get_or_add_rPr()
    if color:
        c = OxmlElement("w:color"); c.set(qn("w:val"), color); rpr.append(c)
    if size:
        s = OxmlElement("w:sz"); s.set(qn("w:val"), str(size)); rpr.append(s)
    if font:
        rf = OxmlElement("w:rFonts")
        rf.set(qn("w:ascii"), font); rf.set(qn("w:hAnsi"), font)
        rpr.append(rf)
    if caps:
        _sub(rpr, "w:caps")
    return r


def add_inline_math(paragraph, latex):
    paragraph._p.append(omath(latex, display=False))


def add_display_math(paragraph, latex, align_left=False):
    paragraph._p.append(omath(latex, display=True, align_left=align_left))
