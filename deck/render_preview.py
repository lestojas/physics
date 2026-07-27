"""
Approximate visual renderer for layout QA.

Reads the generated pptx and draws every shape (fill, outline, text) to a PNG
using matplotlib. Not pixel-perfect (text wrapping is estimated) but reliably
surfaces overlaps, out-of-bounds shapes, and gross text overflow.

Also prints a text report of shapes that fall outside the 13.333 x 7.5 canvas
and text boxes whose estimated wrapped height exceeds their frame.
"""
import sys
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle, Ellipse, Polygon
import textwrap
from pptx import Presentation
from pptx.util import Emu
from pptx.enum.shapes import MSO_SHAPE_TYPE

EMU_IN = 914400.0
W, H = 13.333, 7.5

prs = Presentation("Lecture3.pptx")


def emu_in(v):
    return (v or 0) / EMU_IN


def rgb_of(shape):
    try:
        if shape.fill.type is not None and shape.fill.type == 1:  # solid
            c = shape.fill.fore_color.rgb
            return "#%02x%02x%02x" % (c[0], c[1], c[2])
    except Exception:
        pass
    return None


def line_of(shape):
    try:
        if shape.line.color and shape.line.color.type is not None:
            c = shape.line.color.rgb
            return "#%02x%02x%02x" % (c[0], c[1], c[2])
    except Exception:
        pass
    return None


def text_of(shape):
    if not shape.has_text_frame:
        return None, 12, None
    runs = []
    size = 12
    color = None
    for p in shape.text_frame.paragraphs:
        for r in p.runs:
            runs.append(r.text)
            if r.font.size:
                size = r.font.size.pt
            try:
                if r.font.color and r.font.color.type is not None:
                    cc = r.font.color.rgb
                    color = "#%02x%02x%02x" % (cc[0], cc[1], cc[2])
            except Exception:
                pass
    return "".join(runs), size, color


report = []

for idx, slide in enumerate(prs.slides, start=1):
    fig, ax = plt.subplots(figsize=(W, H), dpi=80)
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.invert_yaxis()
    ax.axis("off")
    fig.subplots_adjust(left=0, right=1, top=1, bottom=0)

    def walk(shapes):
        for sh in shapes:
            try:
                x, y = emu_in(sh.left), emu_in(sh.top)
                w, h = emu_in(sh.width), emu_in(sh.height)
            except Exception:
                continue
            # bounds check
            if x < -0.05 or y < -0.05 or x + w > W + 0.05 or y + h > H + 0.05:
                # allow decorative ovals slightly off-canvas only if clearly decorative (large)
                if not (w > 2.5 and h > 2.5):
                    report.append(f"S{idx}: shape out of bounds x={x:.2f} y={y:.2f} w={w:.2f} h={h:.2f} type={sh.shape_type}")
            fill = rgb_of(sh)
            line = line_of(sh)
            is_oval = False
            try:
                is_oval = "OVAL" in str(sh.adjustments) or (sh.shape_type == MSO_SHAPE_TYPE.AUTO_SHAPE and getattr(sh, 'auto_shape_type', None) is not None and 'OVAL' in str(sh.auto_shape_type))
            except Exception:
                pass
            if fill or line:
                if is_oval:
                    ax.add_patch(Ellipse((x + w/2, y + h/2), w, h,
                                 facecolor=fill or "none",
                                 edgecolor=line or "none", linewidth=1))
                else:
                    ax.add_patch(FancyBboxPatch((x, y), w, h,
                                 boxstyle="round,pad=0,rounding_size=0.04",
                                 facecolor=fill or "none",
                                 edgecolor=line or "none", linewidth=0.8))
            txt, size, color = text_of(sh)
            if txt:
                # estimate wrap width (chars) from box width & font size
                char_w = size * 0.0072  # inches per char approx
                maxchars = max(4, int(w / char_w)) if char_w > 0 else 40
                wrapped = []
                for line_txt in txt.split("\n"):
                    wrapped.extend(textwrap.wrap(line_txt, maxchars) or [""])
                line_h = size * 1.25 / 72.0
                est_h = len(wrapped) * line_h
                if est_h > h + 0.12:
                    report.append(f"S{idx}: TEXT OVERFLOW est_h={est_h:.2f} box_h={h:.2f} :: '{txt[:45]}'")
                ax.text(x + 0.05, y + h/2, "\n".join(wrapped),
                        fontsize=size * 0.82, color=color or "#142530",
                        va="center", ha="left", wrap=True)
            if sh.shape_type == MSO_SHAPE_TYPE.GROUP:
                walk(sh.shapes)

    # tables
    for sh in slide.shapes:
        if sh.has_table:
            x, y = emu_in(sh.left), emu_in(sh.top)
            tbl = sh.table
            rows = len(tbl.rows); cols = len(tbl.columns)
            cxs = [emu_in(c.width) for c in tbl.columns]
            rhs = [emu_in(r.height) for r in tbl.rows]
            cy = y
            for r in range(rows):
                cx = x
                for cc in range(cols):
                    cell = tbl.cell(r, cc)
                    f = rgb_of(cell) if False else None
                    try:
                        cf = cell.fill.fore_color.rgb
                        f = "#%02x%02x%02x" % (cf[0], cf[1], cf[2])
                    except Exception:
                        f = "#ffffff"
                    ax.add_patch(Rectangle((cx, cy), cxs[cc], rhs[r],
                                 facecolor=f, edgecolor="#dde7e9", linewidth=0.5))
                    ct = cell.text
                    if ct:
                        char_w = 12 * 0.0072
                        maxchars = max(4, int(cxs[cc] / char_w))
                        wrapped = textwrap.wrap(ct, maxchars) or [""]
                        est_h = len(wrapped) * (12 * 1.25 / 72.0)
                        if est_h > rhs[r] + 0.1:
                            report.append(f"S{idx}: TABLE CELL overflow r{r}c{cc} est={est_h:.2f} h={rhs[r]:.2f} :: '{ct[:40]}'")
                        ax.text(cx + 0.06, cy + rhs[r]/2, "\n".join(wrapped),
                                fontsize=9.5, va="center", ha="left")
                    cx += cxs[cc]
                cy += rhs[r]

    walk(slide.shapes)
    fig.savefig(f"preview_{idx:02d}.png", dpi=80)
    plt.close(fig)

print("Rendered", len(prs.slides._sldIdLst), "slides")
print("=== LAYOUT REPORT ===")
if not report:
    print("No out-of-bounds or overflow issues detected.")
for r in report:
    print(r)
