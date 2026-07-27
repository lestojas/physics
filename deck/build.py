"""
Build the full Lecture 3 PowerPoint deck (51 slides, 16:9).

Slide content is copied verbatim from the lecture script; each slide's Visual
Suggestion is realised as a diagram/graphic, and the Speaker Notes are placed
in the notes pane.
"""
import theme as T
from theme import (Deck, base, header, footer, bullets, numbered, table, card,
                   rect, textbox, callout, funnel, chevron_flow, step_cards,
                   chain_vertical, quad_grid, icon_checklist, cer_boxes,
                   big_paragraph, set_notes, arrow_between,
                   INK, INK_SOFT, WHITE, PAPER, PAPER_2, CLOUD, DEEP, TEAL,
                   AQUA, SKY, SAND, CORAL, PLUM, LEAF, RED, _mix)
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE

d = Deck()


def title_band(slide, section, title, subtitle=None, source=None, number=None):
    c = base(slide, section)
    header(slide, section, title, subtitle=subtitle, source=source, number=number)
    return c


# ===========================================================================
# SLIDE 1 - The Research Problem Journey (SECTION OPENER)
# ===========================================================================
s = d.new()
c = base(s, "OPENER", decor_waves=False)
# full-bleed hero band
rect(s, 0, 0, 13.333, 7.5, DEEP)
# layered wave shapes bottom
w1 = rect(s, -1, 5.7, 16, 3, _mix(DEEP, WHITE, 0.08), shape=MSO_SHAPE.OVAL)
w2 = rect(s, -2, 6.2, 18, 3, _mix(DEEP, TEAL, 0.5), shape=MSO_SHAPE.OVAL)
w3 = rect(s, -1, 6.7, 17, 3, TEAL, shape=MSO_SHAPE.OVAL)
textbox(s, 0.9, 0.75, 11.5, 0.4,
        [{"text": "LECTURE 3  -  STEM SENIOR HIGH SCHOOL RESEARCH", "size": 13,
          "color": SAND, "bold": True}])
textbox(s, 0.9, 1.15, 11.6, 1.7,
        [{"text": "The Research Problem Journey", "size": 46, "color": WHITE,
          "bold": True, "line_spacing": 0.98}])
textbox(s, 0.9, 2.55, 11.4, 0.55,
        [{"text": "Review of Literature for Identifying Research Problems  |  Competencies 11-16",
          "size": 16, "color": _mix(WHITE, TEAL, 0.25), "italic": True}])
# six-node chevron flow
chevron_flow(s, 0.9, 3.35, 11.55, 0.95, [
    (1, "Evaluate sources"),
    (2, "Synthesize literature"),
    (3, "Formulate the problem"),
    (4, "Develop questions / hypotheses"),
    (5, "Justify (CER)"),
    (6, "Define assumptions & limitations"),
], AQUA)
# subtitles for stops (parenthetical qualifiers)
quals = ["", "(and write it up)", "(in depth)", "(quantitative focus)",
         "", "(quantitative focus)"]
cw = (11.55 - 0.12 * 5) / 6
for i, q in enumerate(quals):
    if q:
        cx = 0.9 + i * (cw + 0.12)
        textbox(s, cx + 0.5, 4.34, cw, 0.35,
                [{"text": q, "size": 9.5, "color": _mix(WHITE, TEAL, 0.35),
                  "italic": True, "align": PP_ALIGN.CENTER}])
callout_txt = ("Each stop builds on the one before it - you cannot skip a step "
               "and still end up with a defensible research problem.")
cc = rect(s, 0.9, 4.95, 11.55, 0.62, _mix(DEEP, WHITE, 0.12),
          shape=MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s, 0.9, 4.95, 0.09, 0.62, SAND, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 1.15, 4.95, 11.1, 0.62,
        [{"text": callout_txt, "size": 14, "color": WHITE, "italic": True}],
        anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 0.9, 7.05, 11.5, 0.35,
        [{"text": "Running case study: one coastal-barangay plastic-waste story carried through every stage.",
          "size": 10.5, "color": WHITE, "italic": True}])
set_notes(s, "Open by naming the destination before the details: by the end of this lecture, every group will walk away with a complete, defensible research problem package - not just a topic. Frame the six stops as a single pipeline, not six unrelated skills. Tell them we will use one running example (coastal plastic waste) so they can watch the same piece of research evolve through every stage, and a second example (dengue) that they will build up themselves, piece by piece, across several practice slides.")

# ===========================================================================
# SLIDE 2 - Too Many Sources, Too Little Time
# ===========================================================================
s = d.new()
c = title_band(s, "P1", "Too Many Sources, Too Little Time",
               subtitle="Scenario framing", number=2)
bullets(s, 0.62, 2.35, 7.2, 4, [
    {"text": "A STEM research group wants to study plastic waste in a coastal barangay.", "gap": 14},
    {"text": "A search turns up: **3 government reports, 4 peer-reviewed journal articles, 12 news articles, 20+ blog posts and social media threads.**", "gap": 14},
    {"text": "The real question isn't *\u201CHow much can I find?\u201D* - it's *\u201CWhich of these can I actually trust and use?\u201D*", "gap": 14},
], c, size=17)
# visual: mixed pile of source icons in a "search results" panel
card(s, 8.2, 2.35, 4.5, 4.3, WHITE, CLOUD)
rect(s, 8.2, 2.35, 4.5, 0.55, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 8.45, 2.35, 4.0, 0.55, [{"text": "\U0001F50D   Search results (unsorted)",
        "size": 13, "color": WHITE, "bold": True}], anchor=MSO_ANCHOR.MIDDLE)
pile = [("Gov't reports", "3", SKY), ("Journal articles", "4", AQUA),
        ("News articles", "12", SAND), ("Blogs / social", "20+", CORAL)]
yy = 3.1
for name, n, col in pile:
    card(s, 8.45, yy, 4.0, 0.62, PAPER_2, CLOUD, shadow=False)
    bd = rect(s, 8.6, yy + 0.11, 0.72, 0.4, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, 8.6, yy + 0.11, 0.72, 0.4, [{"text": n, "size": 14, "color": WHITE,
            "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 9.5, yy, 2.8, 0.62, [{"text": name, "size": 13, "color": INK,
            "bold": True}], anchor=MSO_ANCHOR.MIDDLE)
    yy += 0.78
set_notes(s, "Anchor the whole section in a problem students will genuinely face the moment they start their own capstone research: information overload. Emphasize that having more sources is not the same as having better sources, and that a paper built on weak sources collapses no matter how well it's written afterward. This sets up the need for a deliberate, criteria-based way of judging sources rather than just grabbing whatever appears first in a search engine.")

# ===========================================================================
# SLIDE 3 - Types and Quality of Sources
# ===========================================================================
s = d.new()
c = title_band(s, "P1", "Types and Quality of Sources",
               subtitle="Comparison table", number=3)
table(s, 0.62, 2.15, 12.1,
      ["Category", "Definition", "Typical Example"],
      [
        ["***Primary source***", "Original data or firsthand account produced by the researcher(s) who conducted the study", "A journal article reporting a barangay's original waste-audit data"],
        ["***Secondary source***", "A work that describes, summarizes, or comments on someone else's original research", "A news article reporting on that same waste-audit study"],
        ["***Scholarly / peer-reviewed source***", "Reviewed by an editorial board of experts before publication", "An article in a refereed academic journal"],
        ["***Popular / non-scholarly source***", "Written for a general audience, no formal expert review", "A blog post, opinion piece, or social media post"],
      ], c, col_widths=[3.1, 5.0, 4.0], header_size=14, body_size=12.5,
      row_h=1.02, header_h=0.5)
set_notes(s, "Make the distinction practical, not just definitional: primary vs. secondary is about how close the source is to the original data, while scholarly vs. popular is about whether the source went through expert vetting before publication. These are two separate sliders, not one - a news article can be secondary and still reasonably reliable, while a blog post can be primary (a firsthand account) but still not scholarly. Students often collapse these into one 'good vs. bad' category; keeping the two dimensions separate produces sharper source judgments later.")

# ===========================================================================
# SLIDE 4 - Rating Real Sources on Plastic Waste
# ===========================================================================
s = d.new()
c = title_band(s, "P1", "Rating Real Sources on Plastic Waste",
               subtitle="Annotated examples", source="instructor", number=4)
cards4 = [
    ("A", "A journal article in an environmental science journal reporting original beach-litter survey data", "primary, scholarly", AQUA, "MOST CREDIBLE"),
    ("B", "A national government agency's technical report on coastal solid-waste management", "primary, non-scholarly but authoritative", SKY, "HIGHLY AUTHORITATIVE"),
    ("C", "A news outlet's article summarizing Source A's findings for the public", "secondary, non-scholarly", SAND, "USE WITH CARE"),
    ("D", "A social media post claiming \u201Cplastic pollution is exaggerated\u201D with no citations", "neither primary nor scholarly - low credibility", CORAL, "EXCLUDE"),
]
x = 0.62
cw = (12.1 - 0.3 * 3) / 4
for i, (letter, desc, verdict, col, rank) in enumerate(cards4):
    cx = x + i * (cw + 0.3)
    card(s, cx, 2.25, cw, 4.35, WHITE, CLOUD)
    rect(s, cx, 2.25, cw, 0.72, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    bd = rect(s, cx + 0.18, 2.36, 0.5, 0.5, WHITE, shape=MSO_SHAPE.OVAL)
    textbox(s, cx + 0.18, 2.36, 0.5, 0.5, [{"text": letter, "size": 18,
            "color": col, "bold": True, "align": PP_ALIGN.CENTER}],
            anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, cx + 0.8, 2.25, cw - 0.9, 0.72, [{"text": "Source " + letter,
            "size": 14, "color": WHITE, "bold": True}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, cx + 0.2, 3.1, cw - 0.4, 2.1, [{"text": desc, "size": 12,
            "color": INK, "line_spacing": 1.03}])
    rule = rect(s, cx + 0.2, 5.35, cw - 0.4, 0.02, CLOUD)
    textbox(s, cx + 0.2, 5.45, cw - 0.4, 0.75, [{"text": verdict, "size": 12.5,
            "color": col, "bold": True, "italic": True, "line_spacing": 0.97}])
    pill = rect(s, cx + 0.2, 6.25, cw - 0.4, 0.3, _mix(col, WHITE, 0.8),
                shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, cx + 0.2, 6.24, cw - 0.4, 0.3, [{"text": rank, "size": 10,
            "color": _mix(col, INK, 0.3), "bold": True, "align": PP_ALIGN.CENTER}],
            anchor=MSO_ANCHOR.MIDDLE)
set_notes(s, "Walk through these four side-by-side so students see that credibility is not binary - Source B is not 'scholarly' in the peer-review sense, but it's still highly authoritative because it comes from the mandated data-collecting agency itself. This nuance matters: SHS students often assume 'not a journal article' automatically means 'not usable,' when in fact government and institutional reports are frequently the backbone of applied research. Source D is the clear example of a source to exclude entirely - no author accountability, no evidence, no traceable data.")

# ===========================================================================
# SLIDE 5 - Five Criteria for Judging Sources
# ===========================================================================
s = d.new()
c = title_band(s, "P1", "Five Criteria for Judging Sources",
               subtitle="Matrix / checklist", source="textbook", number=5)
icon_checklist(s, 0.62, 2.15, 12.1, [
    ("\u2605", "Authority", "Is the author or institution qualified / recognized in the field?"),
    ("\u2713", "Accuracy", "Is the information supported by evidence and free of clear errors?"),
    ("\u21BB", "Currency", "Was it published recently enough to still be relevant (the textbook recommends favoring literature from roughly the last 10 years)?"),
    ("\u25CE", "Relevance", "Does it actually connect to the topic being studied?"),
    ("\u2696", "Purpose / Bias", "Was it written to inform, or to persuade / sell?"),
], c, item_h=0.84, gap=0.12)
set_notes(s, "These five criteria come directly from how the textbook describes evaluating literature quality - looking at whether a journal has a refereed editorial board, whether a publisher is well-established, and whether the work is recent. Frame currency carefully: older sources aren't automatically disqualified, especially if they're foundational or still widely cited, but a 10-year-old statistic on plastic waste volumes is far less reliable than one from the past two or three years given how fast environmental data changes. Have students notice that no single criterion is sufficient on its own.")

# ===========================================================================
# SLIDE 6 - Practice: Rate These Three Sources
# ===========================================================================
s = d.new()
c = title_band(s, "P1", "Practice: Rate These Three Sources",
               subtitle="Activity", source="instructor", number=6)
# activity banner
act = rect(s, 0.62, 2.1, 12.1, 0.6, _mix(c, WHITE, 0.82),
           shape=MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s, 0.62, 2.1, 0.09, 0.6, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.9, 2.1, 11.6, 0.6, [{"text": "\u270E  IN PAIRS  -  apply the five criteria (Slide 5) to a new topic: urban flooding in Metro Manila.",
        "size": 14, "color": INK, "bold": True}], anchor=MSO_ANCHOR.MIDDLE)
numbered(s, 0.9, 3.0, 7.0, 2.2, [
    {"text": "A 2024 peer-reviewed hydrology journal article"},
    {"text": "A 2015 blog post on flood-prevention tips"},
    {"text": "A government flood-risk map with technical documentation"},
], c, size=16, gap=14)
# decision worksheet table
table(s, 8.15, 3.0, 4.55, ["Source", "Criterion cited", "Decision"],
      [["1", "", ""], ["2", "", ""], ["3", "", ""]], c,
      col_widths=[0.9, 2.05, 1.6], row_h=0.62, header_size=12, body_size=12)
callout(s, 0.62, 5.75, 12.1, 0.72,
        "For each: Keep, Use with caution, or Reject? Justify with at least one criterion.",
        c, italic=False, size=15)
set_notes(s, "Deliberately switch the topic away from plastic waste here so students practice transferring the skill rather than just recalling the coastal-waste examples from the previous slides. Circulate while pairs work and listen for whether they're citing a specific criterion rather than a vague gut feeling. This is the checkpoint that confirms competency 11 has actually landed before moving into synthesis.")

# ===========================================================================
# SLIDE 7 - A Pile of Credible Sources
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "A Pile of Credible Sources",
               subtitle="Scenario framing", number=7)
bullets(s, 0.62, 2.4, 6.7, 4, [
    {"text": "The group has now filtered their list down to **8 credible, relevant sources** on coastal plastic waste.", "gap": 16},
    {"text": "Reading each one in isolation still leaves them with 8 separate summaries - *not a research direction.*", "gap": 16},
    {"text": "The next skill: *reading across* sources instead of *reading through* them one at a time.", "gap": 16},
], c, size=17)
# visual: 8 scattered docs -> organized table
for i, (dx, dy) in enumerate([(7.7,2.4),(8.5,2.55),(9.4,2.35),(10.2,2.6),
                               (7.9,3.3),(8.8,3.15),(9.7,3.35),(10.5,3.2)]):
    dcard = rect(s, dx, dy, 0.62, 0.8, WHITE, shape=MSO_SHAPE.ROUNDED_RECTANGLE,
                 line_color=CLOUD, shadow=True)
    rect(s, dx + 0.1, dy + 0.15, 0.42, 0.06, _mix(c, WHITE, 0.4))
    rect(s, dx + 0.1, dy + 0.3, 0.42, 0.06, CLOUD)
    rect(s, dx + 0.1, dy + 0.45, 0.3, 0.06, CLOUD)
arrow_between(s, 8.9, 4.35, 2.1, 0.5, c, "down")
org = card(s, 7.7, 5.05, 3.9, 1.5, WHITE, CLOUD)
rect(s, 7.7, 5.05, 3.9, 0.4, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 7.7, 5.05, 3.9, 0.4, [{"text": "One organized synthesis table",
        "size": 13, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}],
        anchor=MSO_ANCHOR.MIDDLE)
for r in range(3):
    rect(s, 7.9, 5.6 + r*0.28, 3.5, 0.05, CLOUD)
set_notes(s, "This is the pivot point of the whole lecture. Having good sources (Part 1) is necessary but not sufficient - the real intellectual work of a literature review happens when a student stops describing individual studies and starts comparing them against each other. Preview that this comparison is exactly what will reveal the 'gap' they need for their own study - and, later in this section, the skeleton of how to actually write that comparison up.")

# ===========================================================================
# SLIDE 8 - Summarizing vs. Synthesizing Literature
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "Summarizing vs. Synthesizing Literature",
               subtitle="Comparison table", source="textbook", number=8)
table(s, 0.62, 2.2, 12.1,
      ["", "***Summarizing***", "***Synthesizing***"],
      [
        ["**Focus**", "One source at a time", "Multiple sources compared together"],
        ["**Output**", "\u201CStudy A found X. Study B found Y.\u201D", "\u201CSeveral studies found X, but none examined Y in this context.\u201D"],
        ["**Purpose**", "Shows you understood each study", "Shows how the studies relate - where they agree, disagree, or leave something unexamined"],
      ], c, col_widths=[1.9, 4.6, 5.6], row_h=1.15, header_size=14,
      body_size=13, first_col_bold=True)
set_notes(s, "The textbook frames a literature review's purpose as connecting a study to the larger, ongoing dialogue in the field - not simply reporting what each source said. Make explicit that summarizing is a necessary first step, but a review that stops at summarizing every source back-to-back reads like a list, not an argument. The synthesis skill is specifically about drawing connections across the row, not down each column.")

# ===========================================================================
# SLIDE 9 - Tools for Synthesizing Literature
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "Tools for Synthesizing Literature",
               subtitle="Concept map / matrix", source="tb_inst", number=9)
# left card: synthesis matrix (instructor)
card(s, 0.62, 2.3, 5.55, 3.5, WHITE, CLOUD)
rect(s, 0.62, 2.3, 5.55, 0.62, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.85, 2.3, 5.1, 0.62, [{"text": "Starting tool - Synthesis matrix",
        "size": 15, "color": WHITE, "bold": True}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 0.85, 3.05, 5.1, 1.0, [{"text": "A simple table with one row per source and columns for *Key Finding*, *Method*, and *Theme / Gap Noted*.",
        "size": 12.5, "color": INK, "line_spacing": 1.05}])
# mini matrix mock
mm_y = 4.15
rect(s, 0.85, mm_y, 5.1, 0.32, _mix(AQUA, WHITE, 0.3))
for r in range(3):
    rect(s, 0.85, mm_y + 0.32 + r*0.32, 5.1, 0.3, WHITE if r%2 else PAPER_2,
         line_color=CLOUD, line_w=0.5)
for cx in [2.2, 3.55, 4.9]:
    rect(s, cx, mm_y, 0.02, 1.28, CLOUD)
# right card: literature map (textbook)
card(s, 7.18, 2.3, 5.55, 3.5, WHITE, CLOUD)
rect(s, 7.18, 2.3, 5.55, 0.62, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 7.41, 2.3, 5.1, 0.62, [{"text": "Next-level tool - Literature map",
        "size": 15, "color": WHITE, "bold": True}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 7.41, 3.05, 5.1, 1.0, [{"text": "A visual diagram that groups sources into broad categories and shows where the *proposed study* fits relative to existing research.",
        "size": 12.5, "color": INK, "line_spacing": 1.05}])
# mini tree map
rect(s, 9.5, 4.1, 0.9, 0.34, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
for i, bx in enumerate([7.7, 8.9, 10.1, 11.3]):
    rect(s, bx, 4.75, 0.85, 0.32, _mix(SKY, WHITE, 0.35),
         shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    arrow_between(s, bx + 0.42 - 0.02 + (9.95 - bx)*0, 4.46, 0.02, 0.28, SKY, "down") if False else None
star = rect(s, 8.9, 5.25, 0.85, 0.34, CORAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 8.9, 5.24, 0.85, 0.34, [{"text": "your study", "size": 8.5,
        "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}],
        anchor=MSO_ANCHOR.MIDDLE)
# connecting arrow label
arrow_between(s, 6.25, 3.85, 0.85, 0.4, c)
textbox(s, 5.9, 4.3, 1.55, 0.6, [{"text": "same purpose, two formats",
        "size": 9, "color": INK_SOFT, "italic": True, "align": PP_ALIGN.CENTER,
        "line_spacing": 0.9}])
callout(s, 0.62, 6.05, 12.1, 0.72,
        "Both tools do the same job: turn a stack of readings into a picture of what's already known and what isn't yet.",
        c, size=14)
set_notes(s, "Introduce the synthesis matrix first because it's the more approachable entry point for SHS-level work. Then connect it to the textbook's literature map concept, which arranges literature into broad topic categories with the proposed study placed at the point where it extends existing work. Frame the two as complementary: the matrix is what you build while reading; the map is often what you can build after, once the categories become clear.")

# ===========================================================================
# SLIDE 10 - A Synthesis Matrix in Action
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "A Synthesis Matrix in Action",
               subtitle="Sample data table", source="instructor", number=10)
table(s, 0.62, 2.2, 12.1,
      ["Source", "Key Finding", "Method", "Theme / Gap Noted"],
      [
        ["Journal Article A", "Coastal households under-segregate plastic waste", "Survey", "Focuses on urban, not coastal, communities"],
        ["Journal Article B", "Peer influence affects waste-sorting behavior in schools", "Interviews", "Studies youth, not adult household behavior"],
        ["Government Report C", "Coastal barangays report high volumes of uncollected plastic", "Waste audit data", "Reports volume, not *why* segregation fails"],
        ["Journal Article D", "Community education programs increase recycling participation", "Quasi-experiment", "Tested in urban, not coastal, settings"],
      ], c, col_widths=[2.2, 4.0, 2.0, 3.9], row_h=0.92, header_size=13,
      body_size=12, first_col_bold=True)
# highlight the gap column
rect(s, 0.62 + 2.2 + 4.0 + 2.0, 2.2, 3.9, 0.5 + 0.92*4, None,
     shape=MSO_SHAPE.RECTANGLE, line_color=CORAL, line_w=2.25)
textbox(s, 8.8, 6.55, 3.9, 0.4, [{"text": "\u2191 The gap lives in this column",
        "size": 12, "color": CORAL, "bold": True, "italic": True,
        "align": PP_ALIGN.CENTER}])
set_notes(s, "Walk the class down each row first, then across - that shift from vertical to horizontal reading is the entire synthesis skill in miniature. Point out that no single source in this table answers the question 'why do plastic-segregation behaviors fail specifically in coastal barangay households,' even though every source touches a piece of it. That absence - visible only once the sources sit side by side - is what a gap looks like in practice.")

# ===========================================================================
# SLIDE 11 - Finding Gaps Across Studies
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "Finding Gaps Across Studies",
               subtitle="What a gap can look like", source="textbook", number=11)
bullets(s, 0.62, 2.25, 6.6, 4.2, [
    {"text": "A **gap** can mean:", "gap": 8, "bold": True},
    {"text": "An unstudied population, site, or context", "level": 1, "gap": 6},
    {"text": "Contradictory findings across studies", "level": 1, "gap": 6},
    {"text": "A topic mentioned but not directly investigated", "level": 1, "gap": 14},
    {"text": "Researchers often signal a gap with phrases like *\u201Cwhat remains to be explored\u201D* or *\u201Clittle empirical research\u201D* on a topic.", "gap": 14},
    {"text": "Naming the gap precisely is what turns a stack of readings into a direction for new research.", "gap": 8},
], c, size=15.5)
# Venn diagram (3 circles) on right
cx0, cy0 = 9.9, 4.15
r_ = 1.15
circ_defs = [(cx0 - 0.7, cy0 - 0.55, SKY, "Studies on\nsegregation", 8.0, 3.2),
             (cx0 + 0.7, cy0 - 0.55, AQUA, "Studies on coastal\ncommunities", 10.9, 3.2),
             (cx0, cy0 + 0.75, SAND, "Studies on adult\nhousehold behavior", 9.4, 6.15)]
for vx, vy, col, lbl, lx, ly in circ_defs:
    o = rect(s, vx - r_, vy - r_, r_*2, r_*2, col, shape=MSO_SHAPE.OVAL)
    T._set_transparency(o, 55)
    o.line.color.rgb = col
    o.line.width = Pt(1.25)
# circle labels
textbox(s, 7.25, 2.35, 1.75, 0.6, [{"text": "Studies on\nsegregation", "size": 10.5,
        "color": SKY, "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}],
        anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 11.35, 2.35, 1.9, 0.6, [{"text": "Studies on coastal\ncommunities", "size": 10.5,
        "color": AQUA, "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}],
        anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 8.5, 6.0, 2.8, 0.5, [{"text": "Studies on adult household behavior", "size": 10.5,
        "color": _mix(SAND, INK, 0.45), "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}],
        anchor=MSO_ANCHOR.MIDDLE)
# gap label center
textbox(s, cx0 - 0.55, cy0 - 0.15, 1.1, 0.5, [{"text": "the gap", "size": 11,
        "color": INK, "bold": True, "align": PP_ALIGN.CENTER}],
        anchor=MSO_ANCHOR.MIDDLE)
set_notes(s, "These gap-signaling phrases are drawn directly from how published researchers write about deficiencies in prior literature - students will start noticing this exact language once they read real journal introductions. Reinforce that a gap is not 'nobody has ever studied plastic waste' (far too broad to be true) - it's a specific, narrow absence, like the coastal-household angle in Slide 10's matrix.")

# ===========================================================================
# SLIDE 12 - Practice: Write Your Gap Statement
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "Practice: Write Your Gap Statement",
               subtitle="Activity", source="instructor", number=12)
callout(s, 0.62, 2.35, 12.1, 0.72,
        "Using the matrix from Slide 10, complete this sentence starter:",
        c, italic=False, size=15)
# big sentence frame card
card(s, 1.4, 3.4, 10.5, 2.0, WHITE, CLOUD)
rect(s, 1.4, 3.4, 0.11, 2.0, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 1.8, 3.4, 9.9, 2.0, [
    {"text": "\u201CWhile much research has examined _______________ ,",
     "size": 19, "color": INK, "italic": True, "space_after": 8, "line_spacing": 1.1},
    {"text": "few studies have looked at _______________",
     "size": 19, "color": INK, "italic": True, "space_after": 8, "line_spacing": 1.1},
    {"text": "in the context of _______________ .\u201D",
     "size": 19, "color": INK, "italic": True, "line_spacing": 1.1},
], anchor=MSO_ANCHOR.MIDDLE)
callout(s, 0.62, 5.7, 12.1, 0.7,
        "Example scaffold only - write your OWN completed version before checking with a partner.",
        CORAL, size=14)
set_notes(s, "This sentence frame is deliberately modeled on the real 'what remains to be explored' language researchers use. Watch for students who fill in something too broad - push them to make the third blank as specific as the matrix allows, since that specificity is exactly what will make the literature review (next) and the eventual problem statement researchable rather than vague.")

# ===========================================================================
# SLIDE 13 - Structuring a Quantitative Literature Review
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "Structuring a Quantitative Literature Review",
               source="textbook", number=13)
textbox(s, 0.62, 1.95, 12.0, 0.55, [{"text": "A synthesis matrix organizes your notes. A literature review organizes your writing. The textbook recommends five parts:",
        "size": 14, "color": INK_SOFT, "italic": True, "line_spacing": 1.0}])
funnel(s, 3.7, 2.6, 6.0, 3.4, 4.05, [
    ("1  Introduction", "tells the reader what sections follow"),
    ("2  Topic 1", "literature on the independent / predictor variable(s)"),
    ("3  Topic 2", "literature on the dependent / outcome variable(s)"),
    ("4  Topic 3", "studies relating both variables (closest studies to yours)"),
    ("5  Summary", "key themes, why more research is needed, how your study fills the need"),
], c)
set_notes(s, "Make the shift explicit: everything up to this slide has been about finding the gap; this slide is about writing it up in the format expected of a quantitative study. Emphasize why Topic 3 is deliberately kept short - the textbook notes this section should be relatively brief, containing only studies closest to the proposed topic, because that is often exactly where the gap lives. If a topic is so new that Topic 3 has almost nothing in it, that scarcity itself is evidence of the gap.")

# ===========================================================================
# SLIDE 14 - The Five-Part Structure Applied
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "The Five-Part Structure Applied",
               subtitle="Annotated example", source="instructor", number=14)
callout(s, 0.62, 2.05, 12.1, 0.62,
        "Variables: predictor = peer-led education program exposure;  outcome = plastic-segregation compliance",
        c, italic=False, size=13.5)
step_cards(s, 0.62, 2.85, 12.1, 3.75, [
    (1, "Introduction", "Previews that the review covers education interventions, segregation behavior, and studies linking the two"),
    (2, "Topic 1 (predictor)", "Summarizes studies on community / peer education program effectiveness in general"),
    (3, "Topic 2 (outcome)", "Summarizes studies on household waste-segregation behavior and its typical determinants"),
    (4, "Topic 3 (both together)", "Notes that almost no studies connect education exposure to segregation compliance in coastal households - the gap"),
    (5, "Summary", "States the theme, names the gap, and previews how this study will address it"),
], c, cols=3, gap=0.22, title_size=13, body_size=11)
set_notes(s, "Point out that Topic 3 in this example is thin almost on purpose - that thinness IS the finding. This is the moment where the synthesis matrix (Slide 10) and the gap statement (Slide 12) stop being separate exercises and become raw material that slots directly into a formal review section.")

# ===========================================================================
# SLIDE 15 - Practice: Sketch Your Review Structure
# ===========================================================================
s = d.new()
c = title_band(s, "P2", "Practice: Sketch Your Review Structure",
               subtitle="Activity", source="instructor", number=15)
card(s, 0.62, 2.15, 12.1, 1.35, _mix(c, WHITE, 0.85), _mix(c, WHITE, 0.5))
rect(s, 0.62, 2.15, 0.11, 1.35, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.95, 2.28, 11.5, 1.1, [
    {"text": "Scenario", "size": 13, "color": c, "bold": True, "space_after": 3},
    {"text": "A group studies whether *exposure to vector-control education campaigns* (predictor) affects *household mosquito-breeding-site elimination behavior* (outcome) in an urban barangay.",
     "size": 14.5, "color": INK, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
# blank five-box template
labels = ["Introduction", "Topic 1", "Topic 2", "Topic 3", "Summary"]
bw = (12.1 - 0.25*4)/5
for i, lb in enumerate(labels):
    bx = 0.62 + i*(bw + 0.25)
    card(s, bx, 3.9, bw, 2.2, WHITE, CLOUD)
    rect(s, bx, 3.9, bw, 0.5, c if i != 3 else CORAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, bx, 3.9, bw, 0.5, [{"text": lb, "size": 12.5, "color": WHITE,
            "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    for r in range(3):
        rect(s, bx + 0.15, 4.7 + r*0.42, bw - 0.3, 0.02, CLOUD)
callout(s, 0.62, 6.35, 12.1, 0.62,
        "In pairs, write ONE sentence per part - just the skeleton, not the full review.",
        CORAL, size=14)
set_notes(s, "Keep this activity light - one sentence per part, five sentences total - since the goal is recognizing the shape of a quantitative review, not drafting a full one in class. Circulate and check specifically that their 'Topic 3' sentence names a genuine, narrow intersection rather than repeating Topic 1 or Topic 2 in different words.")

# ===========================================================================
# SLIDE 16 - From Research Gap to Problem
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "From Research Gap to Problem",
               subtitle="Transition", number=16)
card(s, 0.62, 2.35, 12.1, 1.15, _mix(SKY, WHITE, 0.85), _mix(SKY, WHITE, 0.5))
rect(s, 0.62, 2.35, 0.11, 1.15, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.95, 2.35, 11.5, 1.15, [
    {"text": "The group's gap statement", "size": 12.5, "color": SKY, "bold": True, "space_after": 3},
    {"text": "\u201CFew studies examine why coastal barangay households under-segregate plastic waste despite high reported volumes.\u201D",
     "size": 15.5, "color": INK, "italic": True, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
# two contrasting cards
card(s, 0.62, 3.85, 5.95, 2.6, WHITE, CLOUD)
rect(s, 0.62, 3.85, 5.95, 0.55, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 3.85, 5.95, 0.55, [{"text": "Gap statement", "size": 15,
        "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 0.9, 4.6, 5.4, 1.7, [{"text": "Describes what's *missing in the literature.*  It is diagnostic - about the literature.",
        "size": 15, "color": INK, "line_spacing": 1.1}], anchor=MSO_ANCHOR.MIDDLE)
card(s, 6.77, 3.85, 5.95, 2.6, WHITE, CLOUD)
rect(s, 6.77, 3.85, 5.95, 0.55, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 6.77, 3.85, 5.95, 0.55, [{"text": "Problem statement", "size": 15,
        "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 7.05, 4.6, 5.4, 1.7, [{"text": "Goes one step further - it *commits to studying that gap directly,* and defends why it deserves attention.",
        "size": 15, "color": INK, "line_spacing": 1.1}], anchor=MSO_ANCHOR.MIDDLE)
arrow_between(s, 6.4, 4.85, 0.5, 0.55, c)
set_notes(s, "Keep this transition brief but explicit, since students often treat the gap statement and the problem statement as the same thing. The gap statement is diagnostic - it's about the literature. The problem statement is directive - it's about this study. The next several slides go into real depth on how to build one properly, since a rushed problem statement is the single most common weak point in student research proposals.")

# ===========================================================================
# SLIDE 17 - Topic, Problem, and Question
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Topic, Problem, and Question",
               subtitle="A narrowing funnel", number=17)
funnel(s, 2.7, 2.35, 8.0, 3.4, 3.9, [
    ("TOPIC", "\u201CPlastic waste in coastal communities\u201D - the general subject area"),
    ("PROBLEM", "\u201CCoastal barangay households under-segregate plastic waste despite high volumes\u201D"),
    ("QUESTION", "\u201CWhat factors influence plastic-segregation behavior among coastal barangay households?\u201D"),
], c)
callout(s, 0.62, 6.5, 12.1, 0.62,
        "Each level is narrower than the one before it.", c, size=15)
set_notes(s, "This funnel diagnoses a very common student error: presenting a topic when a problem or a question is required. Have students test any given sentence by asking, 'Could someone write an entire book just on this?' - if yes, it's still a topic, not a problem. Everything in this section builds toward filling that middle box properly.")

# ===========================================================================
# SLIDE 18 - The Four Elements of a Problem Statement
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "The Four Elements of a Problem Statement",
               subtitle="Checklist / matrix", source="guide", number=18)
quad_grid(s, 0.62, 2.15, 12.1, 4.05, [
    {"title": "Gap  -  \u201CWhat's going wrong?\u201D", "body": "The core issue itself: what's not working, or what's missing between what's happening and what should be happening."},
    {"title": "Orientation  -  \u201CWhen, where, how?\u201D", "body": "The when, where, and how: places the problem in its broader context."},
    {"title": "Impact  -  \u201CWho's affected, how much?\u201D", "body": "The measurable effects or consequences: who or what is harmed, and how much."},
    {"title": "Significance  -  \u201CWhy does it matter now?\u201D", "body": "Why solving it matters to the people or institutions involved, and why it deserves attention now."},
], [RED, SKY, CORAL, LEAF])
callout(s, 0.62, 6.35, 12.1, 0.62,
        "A strong problem statement usually touches all four - not necessarily in this order, and not always in four separate sentences.",
        c, size=13)
set_notes(s, "Frame this as a more detailed lens on the same 'problem' box from the Slide 17 funnel - it doesn't replace the funnel, it zooms into what belongs inside it. Note that Gap here means the same thing as the literature gap from Part 2, just restated as the problem itself rather than a missing piece of research. Orientation and Impact are the two elements students skip most often - they'll state the problem and jump straight to why it matters, without ever grounding the reader in when, where, and how severely it's happening.")

# ===========================================================================
# SLIDE 19 - GOIS Applied to Plastic Waste
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "GOIS Applied to Plastic Waste",
               subtitle="Annotated example", source="instructor", number=19)
gois = [
    ("Gap", "Coastal barangay households continue to under-segregate plastic waste despite general awareness of the problem.", RED),
    ("Orientation", "This pattern has grown alongside rising population and consumption in the barangay, with recent waste audits showing increasing volumes even after a past one-time awareness campaign.", SKY),
    ("Impact", "Unsorted plastic contributes to clogged waterways, coastal pollution, and rising costs for local waste management.", CORAL),
    ("Significance", "Understanding the household-level reasons behind this gap matters to barangay officials designing future waste-education programs, and to the coastal ecosystem the community depends on.", LEAF),
]
yy = 2.2
for label, body, col in gois:
    card(s, 0.62, yy, 12.1, 1.02, WHITE, CLOUD)
    tag = rect(s, 0.62, yy, 2.35, 1.02, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, 0.62, yy, 2.35, 1.02, [{"text": label, "size": 16, "color": WHITE,
            "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 3.15, yy, 9.35, 1.02, [{"text": body, "size": 13.5, "color": INK,
            "line_spacing": 1.03}], anchor=MSO_ANCHOR.MIDDLE)
    yy += 1.12
set_notes(s, "Read this as four connected sentences before pointing out the labels - the goal is for students to hear it as one coherent paragraph, not four disconnected fill-in-the-blanks. Note that Gap here is nearly identical to the gap statement built back in Part 2 (Slide 12) - this is deliberate, showing students that the literature-synthesis work they already did isn't separate from problem-statement writing, it IS half the raw material for it.")

# ===========================================================================
# SLIDE 20 - Practice: Spot the Four Elements
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Practice: Spot the Four Elements",
               subtitle="Activity", source="instructor", number=20)
big_paragraph(s, 0.62, 2.2, 12.1, 2.95,
    "E-waste from discarded electronics has risen sharply in Philippine cities over the past five years as device turnover has accelerated. Improperly discarded devices leak heavy metals into soil and water, posing health risks to nearby residents and waste workers. Few local ordinances currently regulate household e-waste disposal, leaving local governments without clear tools to address a growing public health concern.",
    c, size=15)
callout(s, 0.62, 5.4, 12.1, 1.1,
        "In pairs, label which sentence(s) reflect Gap, Orientation, Impact, and Significance.",
        c, italic=False, size=15)
# element chips
chips = [("Gap", RED), ("Orientation", SKY), ("Impact", CORAL), ("Significance", LEAF)]
cxx = 3.0
for lbl, col in chips:
    ch = rect(s, cxx, 5.95, 1.75, 0.42, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, cxx, 5.94, 1.75, 0.42, [{"text": lbl, "size": 12, "color": WHITE,
            "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    cxx += 1.9
set_notes(s, "Using a fresh topic (e-waste) instead of the running plastic-waste example forces students to recognize the four elements rather than simply recall the labels from the previous slide. Note that this paragraph deliberately doesn't label its own parts - that mirrors real published writing, where the four elements are woven together rather than announced.")

# ===========================================================================
# SLIDE 21 - Providing Context Without Overload
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Providing Context Without Overload",
               subtitle="Orientation - two failure modes", source="guide", number=21)
# two failure-mode cards
card(s, 0.62, 2.15, 5.95, 1.5, _mix(CORAL, WHITE, 0.85), _mix(CORAL, WHITE, 0.5))
textbox(s, 0.9, 2.28, 5.4, 1.25, [
    {"text": "Too little context", "size": 14.5, "color": CORAL, "bold": True, "space_after": 3},
    {"text": "Reader doesn't understand why the problem matters.", "size": 13, "color": INK, "line_spacing": 1.02}],
    anchor=MSO_ANCHOR.MIDDLE)
card(s, 6.77, 2.15, 5.95, 1.5, _mix(CORAL, WHITE, 0.85), _mix(CORAL, WHITE, 0.5))
textbox(s, 7.05, 2.28, 5.4, 1.25, [
    {"text": "Too much context", "size": 14.5, "color": CORAL, "bold": True, "space_after": 3},
    {"text": "Reader loses the actual problem in unrelated background.", "size": 13, "color": INK, "line_spacing": 1.02}],
    anchor=MSO_ANCHOR.MIDDLE)
callout(s, 0.62, 3.85, 12.1, 0.62,
        "Ask: Does this detail help explain why the problem exists - or is it just extra information?",
        c, size=13.5)
# before / after
card(s, 0.62, 4.65, 5.95, 1.75, WHITE, CLOUD)
rect(s, 0.62, 4.65, 5.95, 0.45, RED, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 4.65, 5.95, 0.45, [{"text": "Too broad", "size": 13, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 0.9, 5.2, 5.4, 1.1, [{"text": "\u201CLow engagement is caused by technology access, family support, and curriculum design.\u201D",
        "size": 13, "color": INK, "italic": True, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
card(s, 6.77, 4.65, 5.95, 1.75, WHITE, CLOUD)
rect(s, 6.77, 4.65, 5.95, 0.45, LEAF, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 6.77, 4.65, 5.95, 0.45, [{"text": "Narrowed", "size": 13, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 7.05, 5.2, 5.4, 1.1, [{"text": "Focus on just one contributing factor - e.g., how a lack of interactive activities in the curriculum affects student engagement in a specific grade level and subject.",
        "size": 12.5, "color": INK, "italic": True, "line_spacing": 1.02}], anchor=MSO_ANCHOR.MIDDLE)
arrow_between(s, 6.4, 5.25, 0.5, 0.55, c)
set_notes(s, "This is the single most common way student problem statements fail - not from having the wrong elements, but from trying to explain everything at once and ending up unfocused. Emphasize the guiding test: every piece of context earns its place only if it helps explain why the problem exists; everything else, no matter how interesting, is noise that should be cut. Narrowing to one contributing factor doesn't make the problem less important - it makes it actually researchable.")

# ===========================================================================
# SLIDE 22 - Practice: Narrow an Overly Broad Scope
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Practice: Narrow an Overly Broad Scope",
               subtitle="Activity  -  dengue thread begins", source="instructor", number=22)
card(s, 1.5, 2.4, 10.3, 1.3, WHITE, CLOUD)
rect(s, 1.5, 2.4, 0.11, 1.3, RED, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 1.85, 2.4, 9.7, 1.3, [
    {"text": "Broad starting point", "size": 12.5, "color": RED, "bold": True, "space_after": 4},
    {"text": "\u201CDengue cases keep increasing in our city, and something needs to be done.\u201D",
     "size": 17, "color": INK, "italic": True, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
# three narrowing chips
targets = [("one contributing factor", CORAL), ("one population", SKY), ("one setting", AQUA)]
cxx = 1.85
for lbl, col in targets:
    arrow_between(s, cxx - 0.35, 4.15, 0.3, 0.42, c) if cxx > 2 else None
    ch = rect(s, cxx, 4.1, 3.0, 0.55, _mix(col, WHITE, 0.15), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, cxx, 4.09, 3.0, 0.55, [{"text": lbl, "size": 13.5, "color": WHITE,
            "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    cxx += 3.4
callout(s, 0.62, 5.0, 12.1, 0.72,
        "In pairs, narrow this to ONE specific contributing factor, population, and setting - following the model from Slide 21.",
        c, italic=False, size=14)
callout(s, 0.62, 5.95, 12.1, 0.7,
        "Keep your narrowed version - you'll build on it for the next several slides.",
        CORAL, size=14)
set_notes(s, "Tell students explicitly that this isn't a one-off exercise - whatever they narrow this dengue scenario down to will carry forward through root-cause analysis (coming up next) all the way to a full problem statement later in this section. A reasonable narrowed target to nudge stuck groups toward: household-level compliance with mosquito-breeding-site elimination in a specific urban barangay.")

# ===========================================================================
# SLIDE 23 - Symptoms vs. Root Cause
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Symptoms vs. Root Cause",
               subtitle="Concept map", source="guide", number=23)
# iceberg diagram on right
ice_x = 9.6
# waterline
rect(s, 7.85, 4.0, 5.0, 0.05, SKY)
tip = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(ice_x-1.5), Inches(2.4), Inches(3.0), Inches(1.55))
tip.rotation = 180
T._set_fill(tip, _mix(SKY, WHITE, 0.2)); T._no_line(tip); tip.shadow.inherit = False
base_ice = s.shapes.add_shape(MSO_SHAPE.ISOSCELES_TRIANGLE, Inches(ice_x-2.3), Inches(4.05), Inches(4.6), Inches(2.4))
base_ice.rotation = 180
T._set_fill(base_ice, DEEP); T._no_line(base_ice); base_ice.shadow.inherit = False
textbox(s, ice_x-1.5, 2.75, 3.0, 0.9, [{"text": "Symptoms", "size": 14, "color": DEEP, "bold": True, "align": PP_ALIGN.CENTER, "space_after": 2},{"text": "visible above", "size": 10, "color": INK_SOFT, "align": PP_ALIGN.CENTER}])
textbox(s, ice_x-2.3, 4.55, 4.6, 1.4, [{"text": "Root cause", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "space_after": 2},{"text": "hidden beneath", "size": 10, "color": _mix(WHITE, SKY, 0.3), "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
bullets(s, 0.62, 2.2, 7.0, 4.3, [
    {"text": "**Symptoms** - the observable, surface-level effects; visible, but don't explain *why* it's happening.", "gap": 12},
    {"text": "**Root cause** - the underlying reason that gives rise to the symptoms; addressing it produces a lasting solution.", "gap": 12},
    {"text": "A single symptom rarely points to one clear cause - like a headache that could point to dozens of conditions. It's usually a *pattern* of symptoms, examined together, that narrows down the real explanation.", "gap": 12},
    {"text": "Mistaking a symptom for the root cause leads to solutions that only provide temporary relief.", "gap": 8},
], c, size=14)
set_notes(s, "The medical-diagnosis comparison is worth dwelling on: doctors don't diagnose from one symptom in isolation, they look at a cluster of symptoms occurring together. The same logic applies to research problems - low attendance alone doesn't tell you why students are disengaged, but low attendance combined with high missing-work rates combined with low participation starts to sketch a real pattern. This reframes 'digging deeper' as a structured, evidence-based process, not just guessing.")

# ===========================================================================
# SLIDE 24 - The 5 Whys Method
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "The 5 Whys Method", source="guide", number=24)
textbox(s, 0.62, 1.95, 12.0, 0.5, [{"text": "Chain diagram - low engagement in online learning:  ask *\u201Cwhy?\u201D* repeatedly, usually about five times, until you reach a real underlying cause, not another symptom.",
        "size": 13, "color": INK_SOFT, "italic": True, "line_spacing": 1.0}])
chain_vertical(s, 1.9, 2.55, 9.5, [
    ("Why is there high missing work?", "Students aren't participating in discussions."),
    ("Why aren't they participating?", "They don't feel comfortable speaking up online."),
    ("Why not?", "They're unsure of the material and feel disconnected from the instructor."),
    ("Why?", "Lessons are lecture-heavy with little room for feedback."),
    ("Why?", "Course design emphasizes content delivery over interaction; instructors may lack training in online engagement."),
], c, step_h=0.62, gap=0.12, q_w=2.7, body_size=12)
set_notes(s, "Point out how far this chain traveled - from 'missing work' (a symptom nobody would dispute) to 'instructor training and course design' (a root cause almost nobody would have guessed from the first symptom alone). That distance is the entire point of the method: the obvious first-guess explanation is very rarely the real one. Also flag that five is a guideline, not a rule - sometimes the real cause appears after three whys, sometimes it takes seven; stop when the answer to 'why' starts repeating itself or stops producing new information.")

# ===========================================================================
# SLIDE 25 - Root-Cause Digging for Plastic Waste
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Root-Cause Digging for Plastic Waste",
               source="instructor", number=25)
card(s, 0.62, 1.95, 12.1, 0.62, _mix(c, WHITE, 0.85), _mix(c, WHITE, 0.5))
textbox(s, 0.9, 1.95, 11.6, 0.62, [{"text": "Symptom:  High volumes of uncollected, improperly segregated plastic waste despite past awareness campaigns.",
        "size": 13, "color": INK, "bold": True}], anchor=MSO_ANCHOR.MIDDLE)
chain_vertical(s, 2.2, 2.75, 8.9, [
    ("Why?", "Households aren't consistently sorting plastic waste at the source."),
    ("Why?", "Many find sorting inconvenient or are unclear on which bin or schedule to use."),
    ("Why?", "Collection schedules and bin systems are inconsistently applied at the household level."),
    ("Why?", "There's been little ongoing, community-level reinforcement beyond a single initial campaign."),
], c, root_label="Plausible root cause: absence of sustained, peer-reinforced education and a convenient household sorting system - NOT simply \u201Clow awareness.\u201D",
   step_h=0.6, gap=0.13, q_w=1.4, body_size=12.5)
set_notes(s, "Highlight explicitly that 'people don't know plastic is bad for the environment' is almost never the real root cause once you dig - awareness campaigns are common, but sustained, convenient, reinforced systems are rare. This distinction between the obvious first-guess symptom (low awareness) and the less obvious systemic root cause (lack of reinforcement/convenience) is exactly the kind of insight that makes a research problem worth studying rather than obvious.")

# ===========================================================================
# SLIDE 26 - Practice: Run Your Own 5 Whys
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Practice: Run Your Own 5 Whys",
               subtitle="Activity  -  dengue thread continues", source="instructor", number=26)
bullets(s, 0.62, 2.3, 7.1, 4, [
    {"text": "Return to your narrowed dengue scenario from Slide 22.", "gap": 12},
    {"text": "**Starting symptom:** low household compliance with mosquito-breeding-site elimination.", "gap": 12},
    {"text": "In pairs, run your own \u201Cwhy\u201D chain - **at least three levels deep** - to propose a plausible root cause.", "gap": 12},
], c, size=15)
card(s, 0.62, 5.35, 12.1, 1.15, _mix(CORAL, WHITE, 0.85), _mix(CORAL, WHITE, 0.5))
rect(s, 0.62, 5.35, 0.11, 1.15, CORAL, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.95, 5.35, 11.5, 1.15, [
    {"text": "If stuck, consider:", "size": 12.5, "color": CORAL, "bold": True, "space_after": 3},
    {"text": "awareness of specific breeding sites  -  convenience of disposal / container-cleaning routines  -  trust in local health campaigns.",
     "size": 13.5, "color": INK, "line_spacing": 1.03}], anchor=MSO_ANCHOR.MIDDLE)
# blank chain template on right
for i in range(3):
    yy = 2.35 + i*0.9
    card(s, 8.0, yy, 4.7, 0.72, WHITE, CLOUD)
    q = rect(s, 8.0, yy, 1.2, 0.72, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, 8.0, yy, 1.2, 0.72, [{"text": "Why?", "size": 12, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    rect(s, 9.45, yy + 0.35, 3.0, 0.02, CLOUD)
    if i < 2:
        arrow_between(s, 10.1, yy + 0.72, 0.2, 0.18, c, "down")
set_notes(s, "Give groups a firm few minutes and then have two or three pairs share their chains aloud - root-cause chains often diverge in interesting, defensible ways even from the same starting symptom, and that's a feature, not a problem, worth naming explicitly. Keep pushing any group that stops at 'people don't know about dengue prevention' to ask at least one more 'why.'")

# ===========================================================================
# SLIDE 27 - Bringing the Criteria Together
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Bringing the Criteria Together",
               subtitle="Textbook- and guide-based, reconciled", source="tb_guide", number=27)
table(s, 0.62, 2.35, 12.1,
      ["Lecture 1 Checklist", "Problem Statement Element (Slide 18)"],
      [
        ["***Clear*** - plain, specific language", "Supports precise *Gap* and *Orientation*"],
        ["***Specific*** - names population, context, issue", "Supports *Orientation*"],
        ["***Researchable*** - can realistically be studied", "Supports a well-scoped *Gap*"],
        ["***Significant*** - matters to a real audience", "Supports *Impact* and *Significance*"],
      ], c, col_widths=[6.0, 6.1], row_h=0.92, header_size=14, body_size=13.5,
      first_col_bold=False)
set_notes(s, "Reassure students these aren't two competing frameworks to memorize separately - the four-point checklist from Lecture 1 is really asking the same questions as the four elements in a different order. Use this slide as the final quality check before writing: run a draft through both columns, and if it satisfies the left side, it will almost always satisfy the right side too.")

# ===========================================================================
# SLIDE 28 - The Full Problem Statement, Written Out
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "The Full Problem Statement, Written Out",
               subtitle="Annotated example", source="instructor", number=28)
big_paragraph(s, 0.62, 2.15, 12.1, 3.75,
    "In a coastal barangay in the Philippines, despite general community awareness of plastic pollution, households continue to under-segregate plastic waste, resulting in high volumes of uncollected and improperly sorted plastic entering local waterways. This pattern has intensified as the barangay's population and consumption have grown, with waste audits showing rising volumes even after a past one-time awareness campaign. Left unaddressed, continued improper segregation contributes to clogged waterways, coastal pollution, and rising costs for local waste management. Understanding the household-level, systemic reasons behind this gap - beyond simple awareness - is significant for barangay officials designing sustainable, peer-reinforced waste-education programs rather than one-time campaigns.",
    c, size=13.5)
callout(s, 0.62, 6.1, 12.1, 0.72,
        "Built from: the gap (Part 2), the root-cause insight (Slide 25), and all four elements (Slide 18).",
        c, size=14)
set_notes(s, "Walk through this paragraph and show, sentence by sentence, exactly which earlier slide each piece came from - the gap statement from Part 2, the root-cause insight from Slide 25, and the four-element structure from Slide 18. The point of this slide is to make visible that a strong problem statement isn't written in one sitting from a blank page; it's assembled from work the researcher has already done.")

# ===========================================================================
# SLIDE 29 - Practice: Write the Full Statement
# ===========================================================================
s = d.new()
c = title_band(s, "P3", "Practice: Write the Full Statement",
               subtitle="Activity  -  dengue thread payoff", source="instructor", number=29)
# assembly visual
pieces = [("Slide 22", "narrowed scope", CORAL), ("Slide 26", "root cause", SKY)]
cxx = 1.6
for sl, lbl, col in pieces:
    card(s, cxx, 2.5, 3.7, 1.2, WHITE, CLOUD)
    rect(s, cxx, 2.5, 3.7, 0.42, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, cxx, 2.5, 3.7, 0.42, [{"text": sl, "size": 12.5, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, cxx, 2.95, 3.7, 0.7, [{"text": lbl, "size": 14, "color": INK, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    cxx += 4.5
textbox(s, 5.3, 2.85, 0.9, 0.5, [{"text": "+", "size": 30, "color": c, "bold": True, "align": PP_ALIGN.CENTER}])
arrow_between(s, 6.55, 4.0, 0.5, 0.5, c, "down") if False else None
result = card(s, 1.6, 4.15, 10.1, 1.05, _mix(c, WHITE, 0.85), _mix(c, WHITE, 0.5))
textbox(s, 1.9, 4.15, 9.5, 1.05, [{"text": "One full problem-statement paragraph for the dengue scenario",
        "size": 16, "color": INK, "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 1.0}], anchor=MSO_ANCHOR.MIDDLE)
arrow_between(s, 6.4, 3.75, 0.5, 0.35, c, "down")
callout(s, 0.62, 5.55, 12.1, 0.9,
        "Combine your work from Slide 22 + Slide 26. Check it against BOTH columns from Slide 27 before sharing with another pair.",
        CORAL, size=14.5)
set_notes(s, "This is the payoff slide for the entire dengue thread running through this section - students are not starting from scratch, they're assembling pieces they already built themselves, which is exactly the iterative process real researchers go through (research informs the writing, writing reveals what still needs more research, and so on). Let a few pairs read their paragraphs aloud and have the class check them against the Slide 27 table together.")

# ===========================================================================
# SLIDE 30 - From Problem to Guiding Questions
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "From Problem to Guiding Questions",
               subtitle="Transition", number=30)
steps30 = [
    ("Problem statement", "tells the reader WHAT is wrong or unknown.", PLUM),
    ("...but not yet actionable", "It doesn't tell the researcher WHAT to actually go out and ask or measure.", _mix(PLUM, INK_SOFT, 0.3)),
    ("Quantitative move", "turn the problem into a precise question - or a testable prediction - about specific variables.", c),
]
yy = 2.7
for title, body, col in steps30:
    card(s, 1.6, yy, 10.1, 1.05, WHITE, CLOUD)
    rect(s, 1.6, yy, 3.4, 1.05, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, 1.75, yy, 3.1, 1.05, [{"text": title, "size": 15, "color": WHITE, "bold": True, "line_spacing": 0.95}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 5.2, yy, 6.3, 1.05, [{"text": body, "size": 14, "color": INK, "line_spacing": 1.03}], anchor=MSO_ANCHOR.MIDDLE)
    yy += 1.15
    if yy < 5.2:
        arrow_between(s, 6.4, yy - 0.13, 0.4, 0.15, c, "down")
set_notes(s, "Keep this brief - its only job is to signal that the problem statement, while necessary, is still not 'actionable' on its own. Preview that this section goes deep specifically into the quantitative side of this step, since that's where most STEM capstone studies in this course will ultimately land.")

# ===========================================================================
# SLIDE 31 - Two Types of Quantitative Questions
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "Two Types of Quantitative Questions",
               subtitle="Fill-in-the-blank templates", source="textbook", number=31)
card(s, 0.62, 2.15, 12.1, 1.35, WHITE, CLOUD)
rect(s, 0.62, 2.15, 3.3, 1.35, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 2.15, 3.3, 1.35, [{"text": "Descriptive question", "size": 15, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "space_after": 3},{"text": "describes a single variable", "size": 11.5, "color": WHITE, "italic": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 4.1, 2.3, 8.4, 1.05, [{"text": "\u201CWhat is the frequency and variation of scores on ____ (variable) for ____ (participants)?\u201D",
        "size": 14.5, "color": INK, "italic": True, "line_spacing": 1.08}], anchor=MSO_ANCHOR.MIDDLE)
card(s, 0.62, 3.7, 12.1, 1.7, WHITE, CLOUD)
rect(s, 0.62, 3.7, 3.3, 1.7, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 3.7, 3.3, 1.7, [{"text": "Relationship / inferential question", "size": 15, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "space_after": 3},{"text": "how two or more variables relate, often grounded in a theory", "size": 11, "color": WHITE, "italic": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 4.1, 3.82, 8.4, 1.5, [{"text": "\u201C____ (theory) suggests ____ (relationship). It is predicted that there will be a relationship between ____ (predictor) and ____ (outcome), such that ____ (direction of effect).\u201D",
        "size": 13.5, "color": INK, "italic": True, "line_spacing": 1.1}], anchor=MSO_ANCHOR.MIDDLE)
callout(s, 0.62, 5.6, 12.1, 0.85,
        "Descriptive questions come first in most quantitative studies - you need to know what your data even looks like before you can test relationships within it.",
        c, size=14)
set_notes(s, "These fill-in-the-blank scripts come directly from how the textbook teaches question-writing, simplified here for first-time use. Emphasize the sequencing point at the bottom - students often want to jump straight to a relationship question, but a good quantitative study usually reports basic descriptive findings (means, frequencies, ranges) before testing whether variables relate to each other.")

# ===========================================================================
# SLIDE 32 - Naming Your Variables
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "Naming Your Variables",
               subtitle="The building blocks of a quantitative study", source="textbook", number=32)
bullets(s, 0.62, 2.25, 6.7, 3.4, [
    {"text": "**Independent / predictor variable** - the variable thought to influence or predict an outcome.", "gap": 12},
    {"text": "**Dependent / outcome variable** - the variable being affected or predicted.", "gap": 12},
    {"text": "**Mediating variable** - a variable that might explain *how* or *why* the predictor affects the outcome, even if it isn't the main focus.", "gap": 12},
], c, size=14.5)
# variable diagram on right
pv = rect(s, 8.0, 2.5, 2.0, 0.85, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
textbox(s, 8.0, 2.5, 2.0, 0.85, [{"text": "Predictor\nvariable", "size": 12.5, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}], anchor=MSO_ANCHOR.MIDDLE)
ov = rect(s, 10.65, 2.5, 2.0, 0.85, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
textbox(s, 10.65, 2.5, 2.0, 0.85, [{"text": "Outcome\nvariable", "size": 12.5, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}], anchor=MSO_ANCHOR.MIDDLE)
arrow_between(s, 10.05, 2.78, 0.55, 0.3, c)
mv = rect(s, 9.3, 3.85, 2.05, 0.8, PLUM, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
textbox(s, 9.3, 3.85, 2.05, 0.8, [{"text": "Mediating\nvariable", "size": 12, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}], anchor=MSO_ANCHOR.MIDDLE)
arrow_between(s, 10.25, 3.4, 0.18, 0.5, PLUM, "down")
callout(s, 0.62, 5.85, 12.1, 0.85,
        "The strongest quantitative studies ground their variable relationships in an existing theory - a theory gives you a reason to predict the relationship, not just a hunch.",
        c, size=14)
set_notes(s, "This vocabulary matters because it's exactly what students will need for every remaining step in this section - writing questions, writing hypotheses, and even naming limitations later (Part 6 will return to 'mediating variable' directly). The point about theory is worth slowing down on: a hypothesis grounded in a named theory reads as far more rigorous than one that just states a guess, because it shows the researcher understands why the variables might be connected, not just that they might be.")

# ===========================================================================
# SLIDE 33 - Descriptive vs. Relationship Questions Applied
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "Descriptive vs. Relationship Questions Applied",
               subtitle="Annotated example", source="instructor", number=33)
card(s, 0.62, 2.15, 12.1, 1.15, WHITE, CLOUD)
rect(s, 0.62, 2.15, 2.6, 1.15, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 2.15, 2.6, 1.15, [{"text": "Descriptive RQ", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 3.4, 2.15, 9.1, 1.15, [{"text": "\u201CWhat is the frequency and variation of plastic-segregation compliance scores among households in the coastal barangay?\u201D",
        "size": 14, "color": INK, "italic": True, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
card(s, 0.62, 3.45, 12.1, 2.0, WHITE, CLOUD)
rect(s, 0.62, 3.45, 2.6, 2.0, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 3.45, 2.6, 2.0, [{"text": "Relationship RQ", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "space_after": 2},{"text": "theory-grounded", "size": 11, "color": WHITE, "italic": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 3.4, 3.55, 9.1, 1.8, [{"text": "\u201CSocial Learning Theory suggests that behavior is shaped through observing and interacting with role models and community norms. It is predicted that there will be a relationship between household exposure to peer-led education programs (predictor) and plastic-segregation compliance (outcome), such that greater exposure is associated with higher compliance.\u201D",
        "size": 12.5, "color": INK, "italic": True, "line_spacing": 1.08}], anchor=MSO_ANCHOR.MIDDLE)
callout(s, 0.62, 5.65, 12.1, 0.72,
        "Variables named:  predictor = peer-education program exposure;  outcome = segregation compliance.",
        c, italic=False, size=14)
set_notes(s, "Show how the descriptive question would typically come first in the actual study - the group would need to know the general spread of compliance scores before it makes sense to test whether program exposure relates to them. Note that Social Learning Theory is used here as a genuine, real theoretical grounding, not an invented one - this is what 'grounding in a theory' looks like in practice, connecting a recognized behavioral framework to the specific variables at hand.")

# ===========================================================================
# SLIDE 34 - Qualities of a Good Question
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "Qualities of a Good Question",
               subtitle="Checklist", source="textbook", number=34)
icon_checklist(s, 0.62, 2.25, 7.1, [
    ("\u25CE", "Specific", "Names the variable(s) or phenomenon clearly."),
    ("\u2713", "Researchable", "Can be answered using data the group can realistically collect."),
    ("\u2194", "Aligned", "Connects directly back to the problem statement, not a tangent."),
], c, item_h=1.05, gap=0.18)
# alignment chain on right
chain_lbls = [("Problem\nStatement", c), ("Research\nQuestion", AQUA), ("Data\nCollection", SKY)]
yy = 2.45
for lbl, col in chain_lbls:
    rect(s, 8.6, yy, 3.4, 0.85, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
    textbox(s, 8.6, yy, 3.4, 0.85, [{"text": lbl, "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}], anchor=MSO_ANCHOR.MIDDLE)
    yy += 1.2
    if yy < 5.2:
        arrow_between(s, 10.15, yy - 0.35, 0.3, 0.35, PLUM, "down")
textbox(s, 8.6, 5.5, 3.4, 0.4, [{"text": "alignment = link strength", "size": 11, "color": PLUM, "bold": True, "italic": True, "align": PP_ALIGN.CENTER}])
callout(s, 0.62, 6.35, 12.1, 0.7,
        "A question can be well-written and still fail this checklist if it doesn't actually answer the problem the group identified.",
        c, size=13.5)
set_notes(s, "The aligned criterion is the one students skip most often - they write a technically clear, researchable question that has quietly drifted away from the problem statement they spent the last section building. Make this explicit: alignment isn't optional polish, it's the entire point of writing the question in the first place.")

# ===========================================================================
# SLIDE 35 - Questions vs. Hypotheses
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "Questions vs. Hypotheses",
               subtitle="Comparison table", source="textbook", number=35)
table(s, 0.62, 2.15, 12.1,
      ["", "***Qualitative***", "***Quantitative***"],
      [
        ["**Uses**", "Research questions (central question + sub-questions)", "Research questions **or** hypotheses"],
        ["**Wording**", "Begins with *what* or *how*; open-ended", "States a predicted relationship between variables"],
        ["**Intent**", "Explore and understand a phenomenon in depth", "Test or predict a relationship"],
        ["**Example**", "\u201CHow do coastal barangay residents describe their household waste-sorting habits?\u201D", "\u201CIt is predicted that households with active community education programs will show higher plastic-segregation compliance.\u201D"],
      ], c, col_widths=[1.6, 5.25, 5.25], row_h=0.95, header_size=14,
      body_size=12.5, first_col_bold=True)
set_notes(s, "Ground this in the textbook's own reasoning: qualitative researchers deliberately avoid hypotheses because they don't want to predict a direction before hearing from participants. Quantitative researchers do the opposite: they state a predicted relationship up front because their whole design is built around testing it. Neither approach is 'better' - the choice depends entirely on what the problem statement calls for.")

# ===========================================================================
# SLIDE 36 - Writing a Directional Hypothesis
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "Writing a Directional Hypothesis",
               source="textbook", number=36)
textbox(s, 0.62, 1.95, 12.0, 0.9, [{"text": "A hypothesis is a *prediction*, in plain language, about the relationship between variables - using directional words like",
        "size": 13.5, "color": INK, "line_spacing": 1.03}])
# directional word chips
words = ["affects", "influences", "predicts", "impacts", "determines", "causes", "is related to"]
cxx, cyy = 0.62, 2.55
for w in words:
    ww = 0.13*len(w) + 0.4
    if cxx + ww > 12.7:
        cxx = 0.62; cyy += 0.5
    chip = rect(s, cxx, cyy, ww, 0.4, _mix(c, WHITE, 0.15), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, cxx, cyy, ww, 0.4, [{"text": w, "size": 12.5, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    cxx += ww + 0.18
textbox(s, 0.62, 3.15, 12.0, 0.4, [{"text": "Studies commonly state more than one hypothesis, labeled H1, H2, and so on:",
        "size": 13.5, "color": INK_SOFT, "italic": True}])
card(s, 0.62, 3.65, 12.1, 1.05, WHITE, CLOUD)
rect(s, 0.62, 3.65, 1.1, 1.05, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 3.65, 1.1, 1.05, [{"text": "H1", "size": 20, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 1.95, 3.65, 10.5, 1.05, [{"text": "Households with access to peer-led education programs will show higher plastic-segregation compliance than households without access.",
        "size": 13.5, "color": INK, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
card(s, 0.62, 4.85, 12.1, 1.25, WHITE, CLOUD)
rect(s, 0.62, 4.85, 1.1, 1.25, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 4.85, 1.1, 1.25, [{"text": "H2", "size": 20, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 1.95, 4.85, 10.5, 1.25, [{"text": "The positive relationship between education-program exposure and segregation compliance will be stronger in households with school-aged children than in those without.",
        "size": 13.5, "color": INK, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
set_notes(s, "Keep this at the plain-language, directional-prediction level - formal null/alternative notation and statistical significance testing belong to a later statistics-focused lesson, not here. The H1/H2 labeling convention is worth introducing now, though, since students will see it constantly once they start reading real quantitative studies, and it's simply a way of organizing multiple predictions within one study, not a statistical procedure in itself.")

# ===========================================================================
# SLIDE 37 - One Problem, Two Approaches
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "One Problem, Two Approaches",
               subtitle="Coastal Plastic Waste Study", source="instructor", number=37)
# problem box at top branching
pb = card(s, 4.0, 2.1, 5.3, 0.75, _mix(c, WHITE, 0.15), None)
textbox(s, 4.0, 2.1, 5.3, 0.75, [{"text": "Coastal plastic waste problem statement", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
arrow_between(s, 3.0, 3.0, 0.4, 0.45, AQUA, "down")
arrow_between(s, 9.9, 3.0, 0.4, 0.45, SKY, "down")
# qualitative side
card(s, 0.62, 3.6, 5.95, 2.95, WHITE, CLOUD)
rect(s, 0.62, 3.6, 5.95, 0.5, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 3.6, 5.95, 0.5, [{"text": "Qualitative path", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 0.85, 4.2, 5.5, 2.25, [
    {"text": "Central question", "size": 11.5, "color": AQUA, "bold": True, "space_after": 2},
    {"text": "\u201CHow do residents of a coastal barangay describe their household plastic-waste-sorting habits?\u201D", "size": 12, "color": INK, "italic": True, "space_after": 7, "line_spacing": 1.02},
    {"text": "Sub-questions", "size": 11.5, "color": AQUA, "bold": True, "space_after": 2},
    {"text": "1. What barriers do residents describe to consistent sorting?", "size": 11.5, "color": INK, "space_after": 2, "line_spacing": 1.0},
    {"text": "2. How do residents describe community attitudes toward waste segregation?", "size": 11.5, "color": INK, "line_spacing": 1.0},
])
# quantitative side
card(s, 6.77, 3.6, 5.95, 2.95, WHITE, CLOUD)
rect(s, 6.77, 3.6, 5.95, 0.5, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 6.77, 3.6, 5.95, 0.5, [{"text": "Quantitative path", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 7.0, 4.2, 5.5, 2.25, [
    {"text": "Hypothesis (H1)", "size": 11.5, "color": SKY, "bold": True, "space_after": 3},
    {"text": "\u201CHouseholds with access to peer-led education programs will show higher plastic-segregation compliance than households without access.\u201D", "size": 12.5, "color": INK, "italic": True, "line_spacing": 1.08}],
    anchor=MSO_ANCHOR.TOP)
set_notes(s, "This is the payoff slide for Part 4 - showing the same problem statement branching into two legitimate but different research paths makes the qualitative/quantitative distinction concrete rather than abstract. Ask students which approach they'd choose if their group only had time for interviews with 10 households versus a survey of 200 households - the practical constraint, not just the 'feel' of the topic, often decides the approach.")

# ===========================================================================
# SLIDE 38 - Practice: Draft Your Own Question
# ===========================================================================
s = d.new()
c = title_band(s, "P4", "Practice: Draft Your Own Question",
               subtitle="Activity  -  dengue thread continues", source="instructor", number=38)
textbox(s, 0.62, 2.2, 12.0, 0.5, [{"text": "Use the full dengue problem statement your pair wrote in Slide 29. In pairs, draft either:",
        "size": 15, "color": INK, "bold": True, "line_spacing": 1.0}])
card(s, 0.62, 2.85, 5.95, 2.35, WHITE, CLOUD)
rect(s, 0.62, 2.85, 5.95, 0.5, SKY, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 2.85, 5.95, 0.5, [{"text": "(a)  Descriptive question", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 0.9, 3.5, 5.4, 1.6, [{"text": "A descriptive quantitative question AND name its variable.",
        "size": 14.5, "color": INK, "line_spacing": 1.08}], anchor=MSO_ANCHOR.MIDDLE)
card(s, 6.77, 2.85, 5.95, 2.35, WHITE, CLOUD)
rect(s, 6.77, 2.85, 5.95, 0.5, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 6.77, 2.85, 5.95, 0.5, [{"text": "(b)  Directional hypothesis", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 7.05, 3.5, 5.4, 1.6, [{"text": "A directional hypothesis (H1) AND name both the predictor and outcome variables.",
        "size": 14.5, "color": INK, "line_spacing": 1.08}], anchor=MSO_ANCHOR.MIDDLE)
callout(s, 0.62, 5.5, 12.1, 0.75,
        "Check your draft against the aligned criterion (Slide 34) before sharing.",
        CORAL, size=14.5)
set_notes(s, "Reusing their own dengue problem statement from Slide 29 - rather than a fresh scenario - keeps the iterative thread going and shows students this is one continuous piece of work, not six disconnected worksheets. Collect a few examples on the board, specifically flagging any question or hypothesis that drifted from their own problem statement.")

# ===========================================================================
# SLIDE 39 - Why Should Anyone Care?
# ===========================================================================
s = d.new()
c = title_band(s, "P5", "Why Should Anyone Care?",
               subtitle="Scenario framing", number=39)
bullets(s, 0.62, 2.5, 7.0, 3.5, [
    {"text": "The group has a strong problem statement and an aligned research question.", "gap": 16},
    {"text": "A reader - a teacher, a panel, a barangay official - will still ask: *\u201CSo what? Why does this matter enough to study?\u201D*", "gap": 16},
    {"text": "A problem statement alone doesn't answer that. It needs to be **argued for**, not just announced.", "gap": 16},
], c, size=17)
# big "So what?" graphic
sw = rect(s, 8.2, 2.7, 4.4, 3.0, _mix(c, WHITE, 0.12), shape=MSO_SHAPE.ROUNDED_RECTANGLE, shadow=True)
textbox(s, 8.2, 2.9, 4.4, 1.5, [{"text": "\u201CSo what?\u201D", "size": 34, "color": c, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 8.5, 4.4, 3.8, 1.1, [{"text": "The question every reader silently asks of your research problem.",
        "size": 13.5, "color": INK, "italic": True, "align": PP_ALIGN.CENTER, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
set_notes(s, "This is the moment to reframe research writing as persuasive, not just descriptive. Preview that the next several slides introduce a simple three-part structure for building exactly that case.")

# ===========================================================================
# SLIDE 40 - Introducing the CER Framework
# ===========================================================================
s = d.new()
c = title_band(s, "P5", "Introducing the CER Framework",
               subtitle="Concept map", source="instructor", number=40)
cer_boxes(s, 0.62, 2.5, 12.1, [
    ("Claim", "the statement you're arguing for (your research problem matters)"),
    ("Evidence", "the data or literature findings that support the claim"),
    ("Reasoning", "the explanation connecting the evidence to the claim"),
], [LEAF, SKY, CORAL], box_h=1.75, gap=0.55)
callout(s, 0.62, 4.75, 12.1, 1.5,
        "CER is a widely used argumentation framework from science education, applied here to research writing. It is not a term used in the assigned research-methods textbook itself, but it gives us a simple structure for the same task the textbook describes.",
        c, size=14)
set_notes(s, "Be transparent with students about where this framework comes from - it isn't in the Creswell textbook by name, but it maps closely onto how the textbook actually describes a strong introduction. Presenting CER as a translation of that same logic into a format students may already recognize from science class builds confidence rather than introducing something entirely foreign.")

# ===========================================================================
# SLIDE 41 - Building Your CER Argument
# ===========================================================================
s = d.new()
c = title_band(s, "P5", "Building Your CER Argument",
               subtitle="Mapping table", source="textbook", number=41)
maps = [
    ("Claim", "your problem statement is significant and worth studying", LEAF),
    ("Evidence", "findings from your literature synthesis and review (Part 2)  +  relevant data or statistics", SKY),
    ("Reasoning", "why that evidence, taken together, shows this specific gap matters", CORAL),
]
yy = 2.2
for label, body, col in maps:
    card(s, 0.62, yy, 12.1, 0.95, WHITE, CLOUD)
    rect(s, 0.62, yy, 2.3, 0.95, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, 0.62, yy, 2.3, 0.95, [{"text": label, "size": 16, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 3.1, yy, 9.4, 0.95, [{"text": body, "size": 14, "color": INK, "line_spacing": 1.02}], anchor=MSO_ANCHOR.MIDDLE)
    yy += 1.05
callout(s, 0.62, 5.6, 12.1, 0.85,
        "This mirrors how published research introductions work: state the problem, review supporting evidence, then explain its importance to a specific audience.",
        c, size=14)
set_notes(s, "Connect this explicitly back to Part 2 - the synthesis matrix, literature review structure, and gap statement students already built are not separate assignments, they are literally the 'Evidence' component of this argument.")

# ===========================================================================
# SLIDE 42 - A Full CER Paragraph
# ===========================================================================
s = d.new()
c = title_band(s, "P5", "A Full CER Paragraph",
               subtitle="Annotated example (illustrative figures, not verified statistics)", source="instructor", number=42)
cer42 = [
    ("Claim", "\u201CUnderstanding why coastal barangay households under-segregate plastic waste is an urgent research problem.\u201D", LEAF),
    ("Evidence", "\u201CGovernment waste audits report high volumes of uncollected plastic in coastal areas, and while several studies examine urban segregation behavior and youth attitudes toward recycling, none directly examine household-level behavior in coastal barangay contexts.\u201D", SKY),
    ("Reasoning", "\u201CBecause coastal communities face unique waste-management challenges - such as tidal debris and limited collection infrastructure - findings from urban studies may not apply, making this a distinct and understudied problem worth investigating directly.\u201D", CORAL),
]
yy = 2.35
for label, body, col in cer42:
    h = 1.15 if label != "Evidence" else 1.35
    card(s, 0.62, yy, 12.1, h, WHITE, CLOUD)
    rect(s, 0.62, yy, 2.1, h, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, 0.62, yy, 2.1, h, [{"text": label, "size": 15, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 2.9, yy, 9.6, h, [{"text": body, "size": 13, "color": INK, "italic": True, "line_spacing": 1.05}], anchor=MSO_ANCHOR.MIDDLE)
    yy += h + 0.13
set_notes(s, "Read this paragraph aloud as one continuous piece before breaking it back into its three labeled parts. Note explicitly that the specific figures referenced here are illustrative for teaching purposes; when students write their own, they must cite their actual sources and real data.")

# ===========================================================================
# SLIDE 43 - Practice: Build Your Own CER
# ===========================================================================
s = d.new()
c = title_band(s, "P5", "Practice: Build Your Own CER",
               subtitle="Activity  -  dengue thread continues", source="instructor", number=43)
textbox(s, 0.62, 2.2, 12.0, 0.5, [{"text": "Use your dengue problem statement (Slide 29) and these evidence bullets:",
        "size": 15, "color": INK, "bold": True}])
bullets(s, 0.9, 2.75, 11.5, 1.3, [
    {"text": "Local health data show recurring dengue clusters in mosquito-breeding hotspots.", "gap": 6},
    {"text": "Existing studies examine larvicide use and fogging, but few examine household-level elimination behavior.", "gap": 6},
], c, size=14)
# blank CER template
cer_boxes(s, 0.62, 4.1, 12.1, [
    ("Claim", "one sentence"),
    ("Evidence", "one sentence"),
    ("Reasoning", "one sentence"),
], [LEAF, SKY, CORAL], box_h=1.5, gap=0.55)
callout(s, 0.62, 5.95, 12.1, 0.62,
        "In pairs, write one Claim sentence, one Evidence sentence, and one Reasoning sentence.",
        CORAL, size=14.5)
set_notes(s, "By this point, students have carried the dengue scenario through narrowing (Slide 22), root-cause analysis (Slide 26), a full problem statement (Slide 29), and a research question or hypothesis (Slide 38) - this CER paragraph is the final piece, arguing for the very problem they've now built from the ground up. Listen for pairs whose 'Reasoning' sentence simply restates the 'Evidence' sentence; push them toward explaining why the evidence supports the claim.")

# ===========================================================================
# SLIDE 44 - No Study Is Perfect
# ===========================================================================
s = d.new()
c = title_band(s, "P6", "No Study Is Perfect",
               subtitle="Scenario framing", number=44)
bullets(s, 0.62, 2.5, 7.0, 3.5, [
    {"text": "The group now has a problem, a question, and a justified argument for why it matters.", "gap": 16},
    {"text": "One task remains: being honest about what the study *takes for granted* and what it *cannot fully cover.*", "gap": 16},
    {"text": "Every real study - published or student-led - has **both.**", "gap": 16},
], c, size=17)
# two-column reassurance graphic
card(s, 8.2, 2.6, 4.4, 1.55, WHITE, CLOUD)
rect(s, 8.2, 2.6, 4.4, 0.48, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 8.2, 2.6, 4.4, 0.48, [{"text": "\u2713  Takes for granted", "size": 13, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 8.45, 3.2, 3.9, 0.85, [{"text": "Assumptions", "size": 15, "color": INK, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
card(s, 8.2, 4.35, 4.4, 1.55, WHITE, CLOUD)
rect(s, 8.2, 4.35, 4.4, 0.48, SAND, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 8.2, 4.35, 4.4, 0.48, [{"text": "!  Cannot fully cover", "size": 13, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 8.45, 4.95, 3.9, 0.85, [{"text": "Limitations", "size": 15, "color": INK, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
set_notes(s, "Frame this not as a weakness to hide but as a standard, expected part of any honest research proposal. This framing matters because SHS students sometimes worry that naming a limitation will make their proposal look weak, when in fact its absence is what actually signals inexperience to a reader.")

# ===========================================================================
# SLIDE 45 - Assumptions vs. Limitations
# ===========================================================================
s = d.new()
c = title_band(s, "P6", "Assumptions vs. Limitations",
               subtitle="Comparison table", source="instructor", number=45)
table(s, 0.62, 2.2, 12.1,
      ["", "***Assumption***", "***Limitation***"],
      [
        ["**Definition**", "Something the researcher takes as true, but does not test", "A constraint or weakness that affects the study, often outside the researcher's control"],
        ["**Example**", "\u201CSurvey respondents will answer honestly about their waste habits.\u201D", "\u201CThe study covers only one barangay within one semester.\u201D"],
        ["**Function**", "Lets the study proceed without re-proving every basic condition", "Sets honest boundaries around how far the findings can be applied"],
      ], c, col_widths=[1.9, 5.1, 5.1], row_h=1.15, header_size=14,
      body_size=12.5, first_col_bold=True)
callout(s, 0.62, 6.45, 12.1, 0.55,
        "An assumption is something you choose to believe without checking; a limitation is something you can't change even if you wanted to.",
        c, size=12.5)
set_notes(s, "The clearest way to help students tell these apart: an assumption is something you're choosing to believe without checking; a limitation is something you can't change even if you wanted to.")

# ===========================================================================
# SLIDE 46 - Common Limitation Categories in Quantitative Research
# ===========================================================================
s = d.new()
c = title_band(s, "P6", "Common Limitation Categories",
               subtitle="Adapted from the deficiencies framework in Part 2", source="textbook", number=46)
icon_checklist(s, 0.62, 2.1, 12.1, [
    ("\u25C9", "Sample / Population", "Is the sample small, narrow, or drawn from just one context, limiting how far results generalize?"),
    ("\u25AC", "Measurement", "Are the instruments or scales used to measure your variables valid and reliable?"),
    ("\u25C8", "Theoretical Framework", "Does the study rely on a single theory that may not capture the full picture?"),
    ("\u2194", "Uncontrolled / Mediating Variables", "Are there variables that could influence the outcome but weren't measured or controlled for?"),
    ("\u25CE", "Generalizability / Scope", "How far, realistically, can the findings be applied beyond the specific group and setting studied?"),
], c, item_h=0.84, gap=0.11, glyph_size=15)
set_notes(s, "These categories are a direct adaptation of the same 'deficiencies' categories the textbook used earlier to describe gaps in other people's research - sample/population, measurement validity, theory development, and mediating variables. The insight here is that the exact same lens researchers use to critique prior literature is the lens they should turn on their own study once it's designed. This is genuinely useful, quantitative-specific vocabulary - far more precise than a vague 'this study has limitations' statement.")

# ===========================================================================
# SLIDE 47 - Naming Your Study's Assumptions
# ===========================================================================
s = d.new()
c = title_band(s, "P6", "Naming Your Study's Assumptions",
               subtitle="Coastal plastic waste study", source="instructor", number=47)
textbox(s, 0.62, 2.35, 12.0, 0.4, [{"text": "Reasonable assumptions include:", "size": 15, "color": INK, "bold": True}])
for i, txt in enumerate([
    "Survey respondents will report their waste habits honestly.",
    "Barangay waste-audit records reflect actual collected volumes accurately.",
]):
    yy = 2.95 + i*1.0
    card(s, 0.62, yy, 12.1, 0.85, WHITE, CLOUD)
    bd = rect(s, 0.85, yy + 0.2, 0.45, 0.45, AQUA, shape=MSO_SHAPE.OVAL)
    textbox(s, 0.85, yy + 0.19, 0.45, 0.45, [{"text": "\u2713", "size": 16, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 1.5, yy, 10.9, 0.85, [{"text": txt, "size": 15, "color": INK, "line_spacing": 1.02}], anchor=MSO_ANCHOR.MIDDLE)
card(s, 0.62, 5.3, 12.1, 1.0, _mix(c, WHITE, 0.82), _mix(c, WHITE, 0.5))
rect(s, 0.62, 5.3, 0.11, 1.0, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.95, 5.3, 11.5, 1.0, [{"text": "Ask:  \u201CWhat am I treating as true without actually testing it?\u201D",
        "size": 16, "color": INK, "bold": True, "italic": True}], anchor=MSO_ANCHOR.MIDDLE)
set_notes(s, "The guiding question here is the practical tool students should walk away with. Emphasize that assumptions aren't flaws to fix; they're conditions the researcher is knowingly relying on, and naming them shows methodological self-awareness.")

# ===========================================================================
# SLIDE 48 - Naming Your Study's Limitations
# ===========================================================================
s = d.new()
c = title_band(s, "P6", "Naming Your Study's Limitations",
               subtitle="Mapped to Slide 46's categories", source="instructor", number=48)
lims = [
    ("Sample / Population", "The study covers only one coastal barangay, so findings may not generalize to other coastal areas.", SKY),
    ("Measurement", "Self-reported segregation compliance may not perfectly reflect actual household behavior.", AQUA),
    ("Generalizability / Scope", "Data collection within a single school semester limits observation of seasonal waste patterns.", SAND),
]
yy = 2.35
for label, body, col in lims:
    card(s, 0.62, yy, 12.1, 0.95, WHITE, CLOUD)
    rect(s, 0.62, yy, 3.1, 0.95, col, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
    textbox(s, 0.72, yy, 2.9, 0.95, [{"text": label, "size": 13.5, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER, "line_spacing": 0.95}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, 3.9, yy, 8.6, 0.95, [{"text": body, "size": 14, "color": INK, "line_spacing": 1.03}], anchor=MSO_ANCHOR.MIDDLE)
    yy += 1.05
card(s, 0.62, 5.65, 12.1, 0.95, _mix(c, WHITE, 0.82), _mix(c, WHITE, 0.5))
rect(s, 0.62, 5.65, 0.11, 0.95, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.95, 5.65, 11.5, 0.95, [{"text": "Ask:  \u201CWhich category does this constraint fall under - and is it truly outside my control?\u201D",
        "size": 15, "color": INK, "bold": True, "italic": True}], anchor=MSO_ANCHOR.MIDDLE)
set_notes(s, "Point out that explicitly naming which category each limitation falls under (rather than just listing constraints) is what separates a rigorous quantitative limitations section from a vague, generic one. This is also a useful sanity check: if a 'limitation' doesn't fit any category from Slide 46, it may actually be an assumption in disguise.")

# ===========================================================================
# SLIDE 49 - The Full Assumptions & Limitations Write-Up
# ===========================================================================
s = d.new()
c = title_band(s, "P6", "The Full Assumptions & Limitations Write-Up",
               subtitle="Annotated example", source="instructor", number=49)
big_paragraph(s, 0.62, 2.25, 12.1, 3.9,
    "This study assumes that household respondents will report their plastic-segregation habits honestly, and that barangay waste-audit records accurately reflect actual collected volumes. The study is limited by its focus on a single coastal barangay (sample / population), which may restrict how broadly the findings apply to other coastal communities; by its reliance on self-reported compliance data, which may not fully capture actual behavior (measurement); and by its single-semester timeframe, which limits observation of seasonal variation in waste patterns (generalizability / scope).",
    c, size=15)
callout(s, 0.62, 6.35, 12.1, 0.62,
        "Brief, specific, and explicitly categorized - naming the category in parentheses makes the writing more precise without making it longer.",
        c, size=13)
set_notes(s, "This closing paragraph shows students what a complete, quantitative-focused assumptions-and-limitations section actually looks like in finished form - brief, specific, and explicitly categorized rather than a vague closing disclaimer. Note how naming the category in parentheses after each limitation (as modeled here) makes the writing more precise without making it longer.")

# ===========================================================================
# SLIDE 50 - Practice: Assumptions and Limitations
# ===========================================================================
s = d.new()
c = title_band(s, "P6", "Practice: Assumptions and Limitations",
               subtitle="Activity  -  school recycling scenario", source="instructor", number=50)
card(s, 0.62, 2.3, 12.1, 1.0, _mix(c, WHITE, 0.85), _mix(c, WHITE, 0.5))
rect(s, 0.62, 2.3, 0.11, 1.0, c, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.95, 2.3, 11.5, 1.0, [
    {"text": "Scenario", "size": 12.5, "color": c, "bold": True, "space_after": 3},
    {"text": "A group is evaluating whether a school's recycling program has increased student recycling behavior.", "size": 15, "color": INK, "line_spacing": 1.03}], anchor=MSO_ANCHOR.MIDDLE)
# two target boxes
card(s, 0.62, 3.55, 5.95, 1.9, WHITE, CLOUD)
rect(s, 0.62, 3.55, 5.95, 0.5, AQUA, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.62, 3.55, 5.95, 0.5, [{"text": "Write TWO assumptions", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
for r in range(2):
    rect(s, 0.9, 4.35 + r*0.5, 5.4, 0.02, CLOUD)
    textbox(s, 0.9, 4.15 + r*0.5, 0.4, 0.35, [{"text": f"{r+1}.", "size": 13, "color": AQUA, "bold": True}])
card(s, 6.77, 3.55, 5.95, 1.9, WHITE, CLOUD)
rect(s, 6.77, 3.55, 5.95, 0.5, SAND, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 6.77, 3.55, 5.95, 0.5, [{"text": "Write TWO limitations (+ category)", "size": 14, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
for r in range(2):
    rect(s, 7.05, 4.35 + r*0.5, 5.4, 0.02, CLOUD)
    textbox(s, 7.05, 4.15 + r*0.5, 0.4, 0.35, [{"text": f"{r+1}.", "size": 13, "color": _mix(SAND, INK, 0.3), "bold": True}])
callout(s, 0.62, 5.75, 12.1, 0.7,
        "For each limitation, name which category from Slide 46 it falls under. Use the guiding questions from Slides 47-48 to check your answers.",
        CORAL, size=13.5)
set_notes(s, "The recycling-program scenario is intentionally close to students' own school life. A common confusion to watch for: students sometimes list a limitation as an assumption (e.g., 'the program was implemented correctly' is closer to an assumption, not a limitation) - use any such mix-up as a live teaching moment against the Slide 45 table.")

# ===========================================================================
# SLIDE 51 - The Full Journey, One Page
# ===========================================================================
s = d.new()
c = base(s, "CLOSE", decor_waves=False)
rect(s, 0, 0, 13.333, 7.5, DEEP)
w2 = rect(s, -2, 6.4, 18, 3, _mix(DEEP, TEAL, 0.5), shape=MSO_SHAPE.OVAL)
w3 = rect(s, -1, 6.9, 17, 3, TEAL, shape=MSO_SHAPE.OVAL)
textbox(s, 0.62, 0.5, 11.5, 0.4, [{"text": "THE FULL JOURNEY  -  ONE PAGE", "size": 13, "color": SAND, "bold": True}])
textbox(s, 0.62, 0.85, 11.5, 0.7, [{"text": "One coastal barangay. One research problem, fully built.", "size": 26, "color": WHITE, "bold": True}])
rect(s, 0.63, 1.6, 1.7, 0.055, SAND)
journey = [
    (1, "Evaluated sources", "on coastal plastic waste using the five credibility criteria", TEAL),
    (2, "Synthesized them", "into a matrix and structured a quantitative literature review", SKY),
    (3, "Formulated a problem", "using Gap-Orientation-Impact-Significance and root-cause analysis", CORAL),
    (4, "Developed a question & hypothesis", "theory-grounded, naming predictor and outcome variables", PLUM),
    (5, "Justified the problem", "using a Claim-Evidence-Reasoning argument", LEAF),
    (6, "Named assumptions", "and categorized the study's limitations", SAND),
]
bw = (12.1 - 0.25*2) / 3
for i, (n, title, body, col) in enumerate(journey):
    r = i // 3
    cc = i % 3
    bx = 0.62 + cc*(bw + 0.25)
    by = 1.9 + r*1.35
    card(s, bx, by, bw, 1.2, _mix(DEEP, WHITE, 0.1), None)
    bd = rect(s, bx + 0.2, by + 0.2, 0.5, 0.5, col, shape=MSO_SHAPE.OVAL)
    textbox(s, bx + 0.2, by + 0.19, 0.5, 0.5, [{"text": str(n), "size": 17, "color": WHITE, "bold": True, "align": PP_ALIGN.CENTER}], anchor=MSO_ANCHOR.MIDDLE)
    textbox(s, bx + 0.85, by + 0.14, bw - 1.0, 1.0, [
        {"text": title, "size": 13.5, "color": WHITE, "bold": True, "space_after": 2, "line_spacing": 0.95},
        {"text": body, "size": 10.5, "color": _mix(WHITE, TEAL, 0.3), "line_spacing": 0.98}],
        anchor=MSO_ANCHOR.MIDDLE)
cc = rect(s, 0.62, 4.7, 12.1, 0.95, _mix(DEEP, WHITE, 0.14), shape=MSO_SHAPE.ROUNDED_RECTANGLE)
rect(s, 0.62, 4.7, 0.11, 0.95, SAND, shape=MSO_SHAPE.ROUNDED_RECTANGLE)
textbox(s, 0.95, 4.7, 11.5, 0.95, [{"text": "...and one dengue scenario your own pair carried through narrowing, root-cause digging, a full problem statement, a hypothesis, and a CER argument - start to finish.",
        "size": 13.5, "color": WHITE, "italic": True, "line_spacing": 1.03}], anchor=MSO_ANCHOR.MIDDLE)
textbox(s, 0.62, 6.75, 11.5, 0.4, [{"text": "Lecture 3  -  Review of Literature for Identifying Research Problems  |  Competencies 11-16", "size": 11, "color": WHITE, "italic": True}])
set_notes(s, "Close by walking the class back through the entire vertical spine of the lecture using the running coastal plastic-waste case study as the thread. Emphasize that these six competencies are not separate skills to be checked off individually - they are one continuous, iterative process that produces a single defensible research problem. Remind students that their own dengue work across the practice slides mirrors exactly what researchers do: each stage informs and refines the ones around it. Send them off with the reassurance that they now have a repeatable process they can apply to any capstone topic they choose.")

d.save("Lecture3.pptx")
print("Built through slide", len(d.prs.slides._sldIdLst))
