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
LINE       = (234, 234, 234)   # hairlines (within a tied group)
GRP_LINE   = (213, 213, 213)   # divider between rank groups
TRACK      = (240, 240, 240)   # bar track
PANEL      = (247, 247, 247)   # faint panel
YELLOW     = (255, 196, 0)
ORANGE     = (255, 106, 0)
AMBER      = (255, 150, 0)

# medal metals (ranks 1-3)
GOLD       = (214, 168, 54)
SILVER     = (168, 172, 178)
BRONZE     = (178, 118, 66)

FONT_DIR = "/usr/share/fonts/google-noto/"
def F(name, size):
    return ImageFont.truetype(FONT_DIR + name, size)

SS = 2  # supersampling
def s(v): return int(round(v * SS))

def lerp(c1, c2, t):
    return tuple(int(round(c1[i] + (c2[i] - c1[i]) * t)) for i in range(3))
def lighten(c, t): return lerp(c, (255, 255, 255), t)
def darken(c, t):  return lerp(c, (0, 0, 0), t)

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

MEDAL = {1: GOLD, 2: SILVER, 3: BRONZE}
def tier(rank):
    # color used for the score accent bar
    return {1: GOLD, 2: SILVER, 3: BRONZE, 4: GRAY_SOFT, 5: GRAY_SOFT}[rank]
def medal_text(rank):
    return WHITE if rank == 3 else INK   # bronze needs light text; gold/silver dark

# ---------------------------------------------------------------- fonts
f_kicker  = F("NotoSans-ExtraBold.ttf", s(19))
f_addr    = F("NotoSans-Regular.ttf",   s(20))
f_strand  = F("NotoSans-Italic.ttf",    s(20))
f_title   = F("NotoSans-Black.ttf",     s(78))
f_sub_b   = F("NotoSans-ExtraBold.ttf", s(23))
f_sub     = F("NotoSans-Medium.ttf",    s(23))
f_test    = F("NotoSans-ExtraBold.ttf", s(27))
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
row_h      = 66
grp_gap    = 10
head_h     = 396
foot_h     = 36

n_rows = sum(len(g[1]) for g in GROUPS)
list_h = n_rows * row_h           # uniform row height, no per-group gaps
H = head_h + 26 + list_h + foot_h

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

def text_vc(draw, x, cy, txt, font, fill):
    """Draw text left-anchored at x, vertically centered on cy (device px)."""
    b = draw.textbbox((0, 0), txt, font=font)
    draw.text((x, cy - (b[1] + b[3]) / 2), txt, font=font, fill=fill)
    return draw.textlength(txt, font=font)

def medal_badge(bx0, by0, size, base):
    """Paste a metallic gradient rounded-square badge (base px coords)."""
    ds = s(size)
    col = Image.new("RGB", (1, ds))
    top, mid, bot = lighten(base, 0.42), base, darken(base, 0.24)
    for yy in range(ds):
        t = yy / (ds - 1)
        col.putpixel((0, yy), lerp(top, mid, t * 2) if t < 0.5
                     else lerp(mid, bot, (t - 0.5) * 2))
    grad = col.resize((ds, ds))
    mask = Image.new("L", (ds, ds), 0)
    ImageDraw.Draw(mask).rounded_rectangle([0, 0, ds - 1, ds - 1], radius=s(16), fill=255)
    img.paste(grad, (s(bx0), s(by0)), mask)
    rrect(d, [s(bx0), s(by0), s(bx0 + size) - 1, s(by0 + size) - 1],
          r=s(16), outline=darken(base, 0.32), width=max(1, SS))

def outline_badge(bx0, by0, size):
    rrect(d, [s(bx0), s(by0), s(bx0 + size), s(by0 + size)],
          r=s(16), fill=WHITE, outline=GRAY_SOFT, width=max(2, SS))

# ---------------------------------------------------------------- header
x = s(LM)

# thin top accent tab (orange) — asymmetric, editorial
d.rectangle([s(LM), s(44), s(LM) + s(56), s(44) + s(7)], fill=ORANGE)

text_tracked(d, (x, s(70)), "NIEVES VILLARICA NATIONAL HIGH SCHOOL",
             f_kicker, INK, tracking=s(1.5))
d.text((x, s(102)), "Brgy. Villarica, Babak District, Island Garden City of Samal",
       font=f_addr, fill=GRAY)
d.text((x, s(132)), "Science, Technology, Engineering, and Mathematics (STEM)",
       font=f_strand, fill=GRAY)

# big title
ty = s(182)
d.text((x, ty), "TOP", font=f_title, fill=INK)
top_w = d.textlength("TOP", font=f_title)
d.text((x + top_w + s(20), ty), "SCORERS", font=f_title, fill=INK)
tl_bottom = ty + s(78)

# subtitle: PHYSICS 1  ·  [ Summative Test 1 ]  (test emphasized w/ highlight)
sy = tl_bottom + s(22)
d.text((x, sy), "PHYSICS 1", font=f_sub_b, fill=GRAY)
pb = d.textbbox((0, 0), "PHYSICS 1", font=f_sub_b)
line_mid = sy + (pb[1] + pb[3]) / 2.0            # vertical center of subtitle line
cur = x + (pb[2] - pb[0]) + s(18)
# separator dot, centered on the line
dot = "\u2022"
db = d.textbbox((0, 0), dot, font=f_sub_b)
d.text((cur, line_mid - (db[1] + db[3]) / 2.0), dot, font=f_sub_b, fill=GRAY_SOFT)
cur += (db[2] - db[0]) + s(18)
# highlighted "Summative Test 1" — box symmetric around the glyph box
tb = d.textbbox((0, 0), "Summative Test 1", font=f_test)
tw, th = tb[2] - tb[0], tb[3] - tb[1]
pad_x, pad_y = s(16), s(11)
box_l = cur
box_t = line_mid - th / 2.0 - pad_y
box_r = cur + tw + 2 * pad_x
box_b = line_mid + th / 2.0 + pad_y
rrect(d, [box_l, box_t, box_r, box_b], r=s(9), fill=YELLOW)
d.text((box_l + pad_x - tb[0], line_mid - (tb[1] + tb[3]) / 2.0),
       "Summative Test 1", font=f_test, fill=INK)

# ---------------------------------------------------------------- column anchors (dynamic)
def wbase(txt, font):
    return d.textlength(txt, font=font) / SS

rank_cx   = LM + 44                      # center of rank badge
name_x    = LM + 112                     # start of student name column
score_rx  = W - RM                       # right edge for score
bar_w     = 150                          # score accent bar width

# widest content per column (base px)
all_students = [st for _, sts in GROUPS for st in sts]
max_name = max(wbase(n, f_name) for n, _, _ in all_students)
max_sect = max(wbase("Grade 12 - " + sec, f_meta) for _, sec, _ in all_students)

# left edge of the score block (bar defines it)
score_block_left = score_rx - bar_w
# center the grade&section column in the space between name-end and score-block
name_end = name_x + max_name
free = score_block_left - name_end - max_sect
gap  = max(int(free / 2), 72)            # equal, comfortable gaps (>=72)
sect_x = int(name_end + gap)

# column headers
chy = head_h - 28
d.text((s(LM), s(chy)), "RANK", font=f_colhdr, fill=GRAY_SOFT)
d.text((s(name_x), s(chy)), "NAME OF STUDENT", font=f_colhdr, fill=GRAY_SOFT)
d.text((s(sect_x), s(chy)), "GRADE & SECTION", font=f_colhdr, fill=GRAY_SOFT)
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

    # rank badge, aligned to the FIRST student's row of this rank
    first_cy = grp_top + row_h / 2.0
    bx0 = LM + 44 - BADGE / 2.0
    by0 = first_cy - BADGE / 2.0
    if rank in MEDAL:
        medal_badge(int(round(bx0)), int(round(by0)), BADGE, MEDAL[rank])
        num_fill = medal_text(rank)
    else:
        outline_badge(int(round(bx0)), int(round(by0)), BADGE)
        num_fill = INK
    # rank number centered on the first student's row
    num = str(rank)
    nb = d.textbbox((0, 0), num, font=f_badge)
    d.text((s(LM + 44) - (nb[0] + nb[2]) / 2.0,
            s(first_cy) - (nb[1] + nb[3]) / 2.0),
           num, font=f_badge, fill=num_fill)

    for si, (name, section, score) in enumerate(students):
        ry = y + si * row_h
        cy = ry + row_h / 2.0
        dcy = s(cy)

        # row separators: full-width divider at each new group (merged rank cell),
        # thin partial line (from name column) between students tied at one rank
        if si == 0:
            if gi > 0:
                d.rectangle([s(LM), s(ry), s(W - RM), s(ry) + max(1, SS)], fill=GRP_LINE)
        else:
            d.rectangle([s(name_x), s(ry), s(W - RM), s(ry) + max(1, SS - 1)], fill=LINE)

        # col 2: name of student (centered on cy)
        text_vc(d, s(name_x), dcy, name, f_name, INK)

        # col 3: grade & section -> "Grade 12 - <section>" (hyphen)
        gx = text_vc(d, s(sect_x), dcy, "Grade 12 - ", f_meta, GRAY)
        text_vc(d, s(sect_x) + gx, dcy, section, f_meta, INK)

        # col 4: score "27 / 30" right aligned, number centered on cy
        big = str(score)
        mx  = " / %d" % MAX_SCORE
        w_big = d.textlength(big, font=f_score)
        w_mx  = d.textlength(mx, font=f_scoremx)
        start_x = s(score_rx) - (w_big + w_mx)
        bb = d.textbbox((0, 0), big, font=f_score)
        d.text((start_x, dcy - (bb[1] + bb[3]) / 2.0), big, font=f_score, fill=INK)
        mb = d.textbbox((0, 0), mx, font=f_scoremx)
        d.text((start_x + w_big, dcy - (mb[1] + mb[3]) / 2.0), mx,
               font=f_scoremx, fill=GRAY_SOFT)

        # thin score accent bar under the number (identical offset every row)
        frac = score / MAX_SCORE
        by = cy + 20
        bx0b, bx1b = s(score_rx - bar_w), s(score_rx)
        rrect(d, [bx0b, s(by), bx1b, s(by) + s(6)], r=s(3), fill=TRACK)
        fillw = int(round((bx1b - bx0b) * frac))
        rrect(d, [bx0b, s(by), bx0b + fillw, s(by) + s(6)], r=s(3), fill=col)

    y += grp_h

# ---------------------------------------------------------------- output
out = img.resize((W, H), Image.LANCZOS)
out.save("/projects/sandbox/physics/top_scorers.png")
print("saved", out.size)
