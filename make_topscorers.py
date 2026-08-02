#!/usr/bin/env python3
"""Render a modern-minimalist 'Top Scorers' leaderboard poster.
Palette restricted to: white, gray, black, yellow, orange.
"""
from PIL import Image, ImageDraw, ImageFont

# ---------------------------------------------------------------- palette
WHITE      = (255, 255, 255)
INK        = (23, 23, 23)      # near-black
GRAY       = (138, 138, 138)   # secondary text
GRAY_SOFT  = (176, 176, 176)
LINE       = (232, 232, 232)   # hairlines
TRACK      = (240, 240, 240)   # bar track
PANEL      = (247, 247, 247)   # faint panel
YELLOW     = (255, 196, 0)
ORANGE     = (255, 106, 0)
AMBER      = (255, 150, 0)     # orange->yellow blend (still within family)

FONT_DIR = "/usr/share/fonts/google-noto/"
def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

SS = 2  # supersampling
def s(v): return int(round(v * SS))

# ---------------------------------------------------------------- data
# (rank, [ (name, section, score) ... ])
GROUPS = [
    (1, [("Ruth Althea T. Cullamat", "Tesla",   27)]),
    (2, [("Roan Krezil L. Castillo", "Edison",  26),
         ("Kylie D. Sabino",         "Maxwell", 26),
         ("Athena B. Tambalila",     "Maxwell", 26)]),
    (3, [("Kristia Ann O. Eviota",   "Maxwell", 25),
         ("Kobe Bryele S. Gabonada", "Edison",  25),
         ("Edvincent B. Mi\u00f1oza","Maxwell", 25)]),
    (4, [("Cyril Joel Amir C. Olivares","Maxwell",24),
         ("Jessielou Sarias",        "Edison",  24),
         ("Andy Jr. M. Tabunan",     "Edison",  24)]),
    (5, [("Linz Jerry L. Abela",     "Edison",  23),
         ("Paulo Miguel M. Flores",  "Edison",  23),
         ("Sean Dykimbe C. Gauzon",  "Maxwell", 23)]),
]
MAX_SCORE = 30

def tier(rank):
    return {1: ORANGE, 2: AMBER, 3: YELLOW, 4: GRAY_SOFT, 5: GRAY_SOFT}[rank]
def tier_text(rank):
    return WHITE if rank in (1, 2) else INK

# ---------------------------------------------------------------- fonts
f_kicker  = F("NotoSans-ExtraBold.ttf", s(19))
f_addr    = F("NotoSans-Regular.ttf",   s(20))
f_strand  = F("NotoSans-Italic.ttf",    s(20))
f_title   = F("NotoSans-Black.ttf",     s(78))
f_sub_b   = F("NotoSans-ExtraBold.ttf", s(26))
f_sub     = F("NotoSans-Medium.ttf",    s(26))
f_colhdr  = F("NotoSans-ExtraBold.ttf", s(15))
f_name    = F("NotoSans-Bold.ttf",      s(28))
f_meta    = F("NotoSans-Medium.ttf",    s(20))
f_badge   = F("NotoSans-Black.ttf",     s(30))
f_badge_s = F("NotoSans-ExtraBold.ttf", s(13))
f_score   = F("NotoSans-Black.ttf",     s(34))
f_scoremx = F("NotoSans-Bold.ttf",      s(19))
f_foot    = F("NotoSans-Medium.ttf",    s(18))

# ---------------------------------------------------------------- geometry
W   = 1300
LM  = 96          # left margin
RM  = 96
CW  = W - LM - RM

# vertical rhythm (compact)
row_h      = 74
grp_gap    = 10
head_h     = 396
foot_h     = 34

n_rows = sum(len(g[1]) for g in GROUPS)
list_h = n_rows * row_h + (len(GROUPS) - 1) * grp_gap
H = head_h + 60 + list_h + foot_h

img  = Image.new("RGB", (s(W), s(H)), WHITE)
d    = ImageDraw.Draw(img)

def text_tracked(draw, xy, txt, font, fill, tracking=0):
    x, y = xy
    for ch in txt:
        draw.text((x, y), ch, font=font, fill=fill)
        w = draw.textlength(ch, font=font)
        x += w + tracking
    return x

def rrect(draw, box, r, fill=None, outline=None, width=1):
    draw.rounded_rectangle(box, radius=r, fill=fill, outline=outline, width=width)

# ---------------------------------------------------------------- header
x = s(LM)

# thin top accent tab (orange) — asymmetric, editorial
d.rectangle([s(LM), s(44), s(LM) + s(56), s(44) + s(7)], fill=ORANGE)

text_tracked(d, (x, s(70)), "NIEVES VILLARICA NATIONAL HIGH SCHOOL",
             f_kicker, INK, tracking=s(1.5))
d.text((x, s(102)), "Brgy. Villarica, Babak District  \u2022  Island Garden City of Samal",
       font=f_addr, fill=GRAY)
d.text((x, s(132)), "Science, Technology, Engineering and Mathematics (STEM)",
       font=f_strand, fill=GRAY)

# big title
ty = s(182)
d.text((x, ty), "TOP", font=f_title, fill=INK)
top_w = d.textlength("TOP", font=f_title)
d.text((x + top_w + s(20), ty), "SCORERS", font=f_title, fill=INK)
# underline accent under whole title
tl_bottom = ty + s(78) + s(14)
d.rectangle([x, tl_bottom, x + s(140), tl_bottom + s(9)], fill=ORANGE)
d.rectangle([x + s(148), tl_bottom, x + s(178), tl_bottom + s(9)], fill=YELLOW)

# subtitle
sy = tl_bottom + s(26)
sx = d.text((x, sy), "PHYSICS 1", font=f_sub_b, fill=INK)
p1w = d.textlength("PHYSICS 1", font=f_sub_b)
d.text((x + p1w + s(14), sy), "\u2014", font=f_sub, fill=GRAY_SOFT)
dash_w = d.textlength("\u2014", font=f_sub)
d.text((x + p1w + s(14) + dash_w + s(14), sy), "Summative Test 1", font=f_sub, fill=GRAY)

# ---------------------------------------------------------------- column headers
# column x anchors
rank_cx   = LM + 44          # center of rank badge
name_x    = LM + 118         # start of name
score_rx  = W - RM           # right edge for score
bar_right = W - RM
bar_left  = W - RM - 210

chy = head_h - 30
d.text((s(LM), s(chy)), "RANK", font=f_colhdr, fill=GRAY_SOFT)
d.text((s(name_x), s(chy)), "STUDENT", font=f_colhdr, fill=GRAY_SOFT)
sc_hdr = "SCORE"
w_sc = d.textlength(sc_hdr, font=f_colhdr)
d.text((s(score_rx) - w_sc, s(chy)), sc_hdr, font=f_colhdr, fill=GRAY_SOFT)
# header rule
d.rectangle([s(LM), s(head_h), s(W - RM), s(head_h) + max(1, SS)], fill=INK)

# ---------------------------------------------------------------- rows
y = head_h + 26
BADGE = 54

for gi, (rank, students) in enumerate(GROUPS):
    grp_top = y
    grp_h = len(students) * row_h
    col = tier(rank)

    # rank badge, vertically centered in group
    bx0 = LM + 44 - BADGE // 2
    by0 = grp_top + (grp_h - BADGE) // 2
    rrect(d, [s(bx0), s(by0), s(bx0 + BADGE), s(by0 + BADGE)], r=s(18), fill=col)
    # rank number centered
    num = str(rank)
    nb = d.textbbox((0, 0), num, font=f_badge)
    nw, nh = nb[2] - nb[0], nb[3] - nb[1]
    d.text((s(bx0 + BADGE // 2) - nw / 2 - nb[0],
            s(by0 + BADGE // 2) - nh / 2 - nb[1]),
           num, font=f_badge, fill=tier_text(rank))

    for si, (name, section, score) in enumerate(students):
        ry = y + si * row_h
        cy = ry + row_h // 2

        # subtle row separator within group (not before first)
        if si > 0:
            d.rectangle([s(name_x), s(ry), s(W - RM), s(ry) + max(1, SS - 1)], fill=LINE)

        # name
        d.text((s(name_x), s(cy - 26)), name, font=f_name, fill=INK)
        # meta: grade + section, section emphasized
        gtxt = "Grade 12"
        d.text((s(name_x), s(cy + 6)), gtxt, font=f_meta, fill=GRAY)
        gw = d.textlength(gtxt, font=f_meta)
        d.text((s(name_x) + gw + s(8), s(cy + 6)), "\u00b7", font=f_meta, fill=GRAY_SOFT)
        dw = d.textlength("\u00b7", font=f_meta)
        d.text((s(name_x) + gw + s(8) + dw + s(8), s(cy + 6)),
               section, font=f_meta, fill=INK)

        # score number (right aligned), with /30 in gray
        big = str(score)
        mx  = "/%d" % MAX_SCORE
        w_mx = d.textlength(mx, font=f_scoremx)
        w_big = d.textlength(big, font=f_score)
        # baseline align: place big then mx
        total_w = w_big + s(3) + w_mx
        start_x = s(score_rx) - total_w
        d.text((start_x, s(cy - 30)), big, font=f_score, fill=INK)
        d.text((start_x + w_big + s(3), s(cy - 10)), mx, font=f_scoremx, fill=GRAY_SOFT)

        # score bar under the score, right aligned
        frac = score / MAX_SCORE
        by = cy + 16
        bx1 = score_rx
        bx0b = score_rx - 190
        rrect(d, [s(bx0b), s(by), s(bx1), s(by + 8)], r=s(4), fill=TRACK)
        fillw = int((bx1 - bx0b) * frac)
        rrect(d, [s(bx0b), s(by), s(bx0b + fillw), s(by + 8)], r=s(4), fill=col)

    y += grp_h + grp_gap

# ---------------------------------------------------------------- output
out = img.resize((W, H), Image.LANCZOS)
out.save("/projects/sandbox/physics/top_scorers.png")
print("saved", out.size)
