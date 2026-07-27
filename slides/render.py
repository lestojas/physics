"""
Lightweight PPTX -> PNG renderer for LAYOUT VERIFICATION.
Not pixel-perfect: approximates shapes/fills/text using Lato metrics so we can
eyeball layout and detect text overflow before finalizing.
"""
import sys, os
from PIL import Image, ImageDraw, ImageFont
from pptx import Presentation
from pptx.util import Emu, Pt
from pptx.oxml.ns import qn
from pptx.enum.shapes import MSO_SHAPE_TYPE
try:
    from pptx.enum.shapes import MSO_SHAPE
except Exception:
    MSO_SHAPE = None

FDIR = "/opt/toolchains/.local/share/mise/installs/ruby/3.4.4/lib/ruby/3.4.0/rdoc/generator/template/darkfish/fonts"
REG = os.path.join(FDIR, "Lato-Regular.ttf")
ITAL = os.path.join(FDIR, "Lato-RegularItalic.ttf")

DPI = 120.0
PXI = DPI  # px per inch
EMU_PER_IN = 914400.0

_font_cache = {}


def font(size_pt, bold=False, italic=False):
    key = (round(size_pt, 1), italic)
    if key not in _font_cache:
        path = ITAL if italic else REG
        px = max(6, int(size_pt * PXI / 72.0))
        _font_cache[key] = ImageFont.truetype(path, px)
    return _font_cache[key]


def emu_px(v):
    return (v / EMU_PER_IN) * PXI if v is not None else 0


def col_of(rgb, default="2B2B2B"):
    try:
        return "#" + str(rgb)
    except Exception:
        return "#" + default


def safe_fill(shape):
    try:
        if shape.fill.type == 1:  # solid
            return "#" + str(shape.fill.fore_color.rgb)
    except Exception:
        pass
    return None


def safe_line(shape):
    try:
        if shape.line.fill.type == 1:
            return "#" + str(shape.line.color.rgb), max(1, int(emu_px(shape.line.width) if shape.line.width else 1))
    except Exception:
        pass
    return None, 0


def tokens_of_paragraph(p):
    """Return (tokens, is_bullet). tokens: list of dicts, or 'NL' marker."""
    pPr = p._p.find(qn('a:pPr'))
    is_bullet = False
    indent_px = 0
    if pPr is not None and pPr.find(qn('a:buChar')) is not None:
        is_bullet = True
        marL = pPr.get('marL')
        indent_px = emu_px(int(marL)) if marL else 34
    toks = []
    for r in p.runs:
        sz = r.font.size.pt if r.font.size else 18
        bold = bool(r.font.bold)
        ital = bool(r.font.italic)
        color = col_of(r.font.color.rgb) if _has_color(r) else "#2B2B2B"
        text = r.text
        parts = text.split("\n")
        for i, part in enumerate(parts):
            if i > 0:
                toks.append("NL")
            for w in part.split(" "):
                toks.append({"w": w, "sz": sz, "b": bold, "i": ital, "c": color})
                toks.append({"w": " ", "sz": sz, "b": bold, "i": ital, "c": color, "space": True})
    return toks, is_bullet, indent_px


def _has_color(r):
    try:
        _ = r.font.color.rgb
        return r.font.color.type is not None
    except Exception:
        return False


def tok_w(t):
    f = font(t["sz"], t["b"], t["i"])
    w = f.getlength(t["w"])
    if t["b"]:
        w *= 1.06
    return w


def layout_lines(toks, max_w):
    lines = []
    cur = []
    cur_w = 0
    for t in toks:
        if t == "NL":
            lines.append(cur); cur = []; cur_w = 0
            continue
        w = tok_w(t)
        if t.get("space"):
            if cur:
                cur.append(t); cur_w += w
            continue
        if cur_w + w > max_w and cur:
            # trim trailing space
            while cur and cur[-1].get("space"):
                cur.pop()
            lines.append(cur); cur = [t]; cur_w = w
        else:
            cur.append(t); cur_w += w
    if cur:
        while cur and cur[-1].get("space"):
            cur.pop()
        lines.append(cur)
    return lines


def line_w(line):
    return sum(tok_w(t) for t in line)


def line_h(line):
    return max([t["sz"] for t in line], default=14) * PXI / 72.0


def draw_text_frame(draw, tf, x, y, w, h, warn, sid, name):
    ml = emu_px(tf.margin_left) if tf.margin_left is not None else emu_px(91440)
    mr = emu_px(tf.margin_right) if tf.margin_right is not None else emu_px(91440)
    mt = emu_px(tf.margin_top) if tf.margin_top is not None else emu_px(45720)
    mb = emu_px(tf.margin_bottom) if tf.margin_bottom is not None else emu_px(45720)
    va = tf.vertical_anchor  # None top, MIDDLE=3, BOTTOM=4
    cx = x + ml
    cw = w - ml - mr
    # build all lines with metadata
    blocks = []
    total_h = 0
    for p in tf.paragraphs:
        toks, is_bullet, indent = tokens_of_paragraph(p)
        if not any(isinstance(t, dict) for t in toks):
            # empty paragraph -> small gap
            sz = 14
            blocks.append({"lines": [], "indent": 0, "bullet": False, "sa": 0, "ls": 1.0, "align": p.alignment, "empty_h": sz * PXI / 72.0})
            total_h += sz * PXI / 72.0
            continue
        text_w = cw - indent
        lines = layout_lines(toks, text_w)
        ls = p.line_spacing if p.line_spacing else 1.0
        if not isinstance(ls, float) and not isinstance(ls, int):
            ls = 1.0
        sa = p.space_after.pt if p.space_after else 0
        sb = p.space_before.pt if p.space_before else 0
        bh = 0
        for ln in lines:
            bh += line_h(ln) * ls
        bh += (sa + sb) * PXI / 72.0
        blocks.append({"lines": lines, "indent": indent, "bullet": is_bullet,
                       "sa": sa, "sb": sb, "ls": ls, "align": p.alignment,
                       "bullet_color": _bullet_color(p)})
        total_h += bh
    # vertical anchor
    if va == 3:  # middle
        ty = y + mt + max(0, (h - mt - mb - total_h) / 2)
    elif va == 4:  # bottom
        ty = y + h - mb - total_h
    else:
        ty = y + mt
    # overflow check
    if ty + total_h > y + h + 3:
        warn.append(f"  [OVERFLOW-V] slide {sid} '{name}': text height {total_h:.0f}px > box {h-mt-mb:.0f}px")
    # draw
    yy = ty
    for blk in blocks:
        if not blk["lines"]:
            yy += blk.get("empty_h", 8)
            continue
        yy += blk["sb"] * PXI / 72.0 if blk.get("sb") else 0
        for li, ln in enumerate(blk["lines"]):
            lw = line_w(ln)
            lh = line_h(ln)
            align = blk["align"]
            base_x = cx + blk["indent"]
            avail = cw - blk["indent"]
            if align == 2:  # center
                sx = base_x + max(0, (avail - lw) / 2)
            elif align == 3:  # right
                sx = base_x + max(0, avail - lw)
            else:
                sx = base_x
            if lw > avail + 4:
                warn.append(f"  [OVERFLOW-H] slide {sid} '{name}': line width {lw:.0f} > {avail:.0f}")
            if blk["bullet"] and li == 0:
                draw.rectangle([cx, yy + lh*0.32, cx + lh*0.28, yy + lh*0.6], fill=blk["bullet_color"] or "#1D7A8C")
            xx = sx
            for t in ln:
                f = font(t["sz"], t["b"], t["i"])
                draw.text((xx, yy), t["w"], font=f, fill=t["c"])
                xx += tok_w(t)
            yy += lh * blk["ls"]
        yy += blk["sa"] * PXI / 72.0


def _bullet_color(p):
    pPr = p._p.find(qn('a:pPr'))
    if pPr is not None:
        buClr = pPr.find(qn('a:buClr'))
        if buClr is not None:
            srgb = buClr.find(qn('a:srgbClr'))
            if srgb is not None:
                return "#" + srgb.get('val')
    return None


def draw_shape(draw, shape, warn, sid):
    x = emu_px(shape.left); y = emu_px(shape.top)
    w = emu_px(shape.width); h = emu_px(shape.height)
    # bounds check
    if x < -4 or y < -4 or x + w > 1600 + 4 or y + h > 900 + 4:
        warn.append(f"  [OUT-OF-BOUNDS] slide {sid}: shape at ({x:.0f},{y:.0f}) size ({w:.0f}x{h:.0f})")
    fill = safe_fill(shape)
    lc, lw = safe_line(shape)
    ast = None
    try:
        if shape.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE:
            ast = shape.auto_shape_type
    except Exception:
        ast = None
    name = str(ast)
    if ast is not None and "OVAL" in str(ast):
        draw.ellipse([x, y, x + w, y + h], fill=fill, outline=lc, width=lw or 1)
    elif ast is not None and "RIGHT_ARROW" in str(ast):
        midy = y + h / 2
        bx = x + w * 0.55
        draw.polygon([(x, y + h*0.28), (bx, y + h*0.28), (bx, y),
                      (x + w, midy), (bx, y + h), (bx, y + h*0.72), (x, y + h*0.72)],
                     fill=fill or "#1D7A8C")
    elif ast is not None and "DOWN_ARROW" in str(ast):
        midx = x + w / 2
        by = y + h * 0.5
        draw.polygon([(x + w*0.28, y), (x + w*0.72, y), (x + w*0.72, by),
                      (x + w, by), (midx, y + h), (x, by), (x + w*0.28, by)],
                     fill=fill or "#1D7A8C")
    elif ast is not None and ("CHEVRON" in str(ast) or "PENTAGON" in str(ast)):
        pt = w * 0.16
        draw.polygon([(x, y), (x + w - pt, y), (x + w, y + h/2),
                      (x + w - pt, y + h), (x, y + h), (x + pt, y + h/2)],
                     fill=fill or "#1D7A8C")
    elif ast is not None and "ROUNDED_RECTANGLE" in str(ast):
        rad = min(w, h) * 0.14
        try:
            draw.rounded_rectangle([x, y, x + w, y + h], radius=rad, fill=fill, outline=lc, width=lw or 1)
        except Exception:
            draw.rectangle([x, y, x + w, y + h], fill=fill, outline=lc, width=lw or 1)
    else:
        if fill or lc:
            draw.rectangle([x, y, x + w, y + h], fill=fill, outline=lc, width=lw or 1)
    # text
    if shape.has_text_frame and shape.text_frame.text.strip():
        draw_text_frame(draw, shape.text_frame, x, y, w, h, warn, sid, name)


def draw_table(draw, gshape, warn, sid):
    tbl = gshape.table
    x0 = emu_px(gshape.left); y0 = emu_px(gshape.top)
    col_w = [emu_px(c.width) for c in tbl.columns]
    row_h = [emu_px(r.height) for r in tbl.rows]
    yy = y0
    for ri, r in enumerate(tbl.rows):
        xx = x0
        for ci in range(len(col_w)):
            cell = tbl.cell(ri, ci)
            cw = col_w[ci]; ch = row_h[ri]
            fill = None
            try:
                if cell.fill.type == 1:
                    fill = "#" + str(cell.fill.fore_color.rgb)
            except Exception:
                pass
            draw.rectangle([xx, yy, xx + cw, yy + ch], fill=fill, outline="#C9D5DD", width=1)
            if cell.text_frame.text.strip():
                draw_text_frame(draw, cell.text_frame, xx, yy, cw, ch, warn, sid, f"cell{ri},{ci}")
            xx += cw
        yy += row_h[ri]


def render(path, outdir):
    prs = Presentation(path)
    W = int(emu_px(prs.slide_width)); H = int(emu_px(prs.slide_height))
    os.makedirs(outdir, exist_ok=True)
    warn = []
    imgs = []
    for i, slide in enumerate(prs.slides, 1):
        img = Image.new("RGB", (W, H), "#FFFFFF")
        draw = ImageDraw.Draw(img)
        for shape in slide.shapes:
            try:
                if shape.has_table:
                    draw_table(draw, shape, warn, i)
                    continue
            except Exception:
                pass
            try:
                draw_shape(draw, shape, warn, i)
            except Exception as e:
                warn.append(f"  [render-err] slide {i}: {e}")
        p = os.path.join(outdir, f"slide_{i:02d}.png")
        img.save(p)
        imgs.append(img)
    # contact sheets: 2 cols x 3 rows
    thumb_w, thumb_h = 760, 428
    per = 6
    sheet_idx = 1
    for start in range(0, len(imgs), per):
        chunk = imgs[start:start + per]
        cols, rows = 2, 3
        sheet = Image.new("RGB", (cols * thumb_w + 30, rows * thumb_h + 40), "#DDE3E8")
        for j, im in enumerate(chunk):
            t = im.resize((thumb_w, thumb_h))
            r, c = divmod(j, cols)
            sheet.paste(t, (10 + c * (thumb_w + 10), 10 + r * (thumb_h + 10)))
        sp = os.path.join(outdir, f"sheet_{sheet_idx}.png")
        sheet.save(sp)
        sheet_idx += 1
    print(f"Rendered {len(imgs)} slides -> {outdir}")
    if warn:
        print(f"\n{len(warn)} layout warning(s):")
        for wln in warn:
            print(wln)
    else:
        print("No overflow / out-of-bounds warnings.")


if __name__ == "__main__":
    render(sys.argv[1], sys.argv[2])
