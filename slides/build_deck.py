"""
Build: Lecture 3 - Review of Literature for Identifying Research Problems
Modern 16:9 PowerPoint deck (44 slides). Content copied from the source script,
visual suggestions realised as diagrams, speaker notes placed in Notes.
"""
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE, MSO_CONNECTOR

import helpers as H
from helpers import (
    C, rect, rrect, textbox, para, _run, fill_frame, header, background,
    bullets, checklist, card, card_header, two_column, styled_table,
    down_arrow, right_arrow, vchain, soft_shadow, footer,
    INK, INK_SOFT, PRIMARY, PRIMARY_DK, PRIMARY_LT, ACCENT, ACCENT_LT,
    AMBER, AMBER_LT, SUCCESS, SUCCESS_LT, DANGER, DANGER_LT, BG, CARD,
    MUTED, LINE, WHITE, F_TITLE, F_HEAD, F_BODY, F_LIGHT, SW, SH,
)

prs = Presentation()
prs.slide_width = Inches(SW)
prs.slide_height = Inches(SH)
BLANK = prs.slide_layouts[6]

CENTER = PP_ALIGN.CENTER
LEFT = PP_ALIGN.LEFT
MID = MSO_ANCHOR.MIDDLE


def new_slide():
    return prs.slides.add_slide(BLANK)


def notes(slide, text):
    slide.notes_slide.notes_text_frame.text = text


# --------------------------------------------------------- shared diagrams
def process_strip(slide, x, y, w, h, stages, size=13):
    n = len(stages)
    overlap = 0.26
    cw = (w + overlap * (n - 1)) / n
    for i, st in enumerate(stages):
        cx = x + i * (cw - overlap)
        col = PRIMARY if i % 2 == 0 else PRIMARY_DK
        shp = rect(slide, cx, y, cw, h, fill=col, kind=MSO_SHAPE.CHEVRON)
        fill_frame(shp, [(st, size, WHITE, True)], align=CENTER)


def funnel(slide, cx, y, items, widths, colors, box_h=0.72, gap=0.16, size=19):
    cy = y
    for i, it in enumerate(items):
        w = widths[i]
        b = rrect(slide, cx - w / 2, cy, w, box_h, fill=colors[i], radius=0.14, shadow=True)
        tf = b.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MID
        p = tf.paragraphs[0]
        p.alignment = CENTER
        p.line_spacing = 1.0
        if isinstance(it, tuple):
            _run(p, it[0] + "  ", size, WHITE, bold=True, font=F_HEAD)
            _run(p, it[1], size - 3, "EAF6F8")
        else:
            _run(p, it, size, WHITE, bold=True, font=F_HEAD)
        cy += box_h + gap
    return cy


def connector(slide, x1, y1, x2, y2, color=PRIMARY, w=2.0):
    ln = slide.shapes.add_connector(MSO_CONNECTOR.STRAIGHT,
                                    Inches(x1), Inches(y1), Inches(x2), Inches(y2))
    ln.line.color.rgb = C(color)
    ln.line.width = Pt(w)
    ln.shadow.inherit = False
    return ln


def template_card(slide, x, y, w, h, rows, size=24, gap=0.2, label_w=None):
    """rows: list of (label, blank?) -> a fill-in line with a rule."""
    card(slide, x, y, w, h)
    inner = x + 0.4
    cy = y + 0.35
    rh = (h - 0.6) / len(rows)
    for label in rows:
        _, tf = textbox(slide, inner, cy, w - 0.8, rh * 0.5)
        p = para(tf, first=True, space_after=0)
        _run(p, label, size, INK, bold=True, font=F_HEAD)
        # blank rule
        rl = rrect(slide, inner, cy + rh * 0.62, w - 0.8, 0.045, fill=LINE, radius=0.5)
        cy += rh
    return cy


def instruction_bar(slide, x, y, w, text, color=AMBER, text_color=INK, icon="\u270E"):
    b = rrect(slide, x, y, w, 0.62, fill=color, radius=0.12)
    ic = rect(slide, x + 0.2, y + 0.11, 0.4, 0.4, fill=WHITE, kind=MSO_SHAPE.OVAL)
    fill_frame(ic, [(icon, 15, color, True)], align=CENTER)
    _, tf = textbox(slide, x + 0.78, y, w - 1.0, 0.62, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.0)
    _run(p, text, 17, text_color, bold=True, font=F_HEAD)


def eg_tag(slide, x, y, text):
    """Small 'Instructor-Created Example' pill."""
    w = 0.14 + 0.088 * len(text)
    b = rrect(slide, x, y, min(w, 5.2), 0.34, fill=PRIMARY_LT, radius=0.5)
    _, tf = textbox(slide, x + 0.18, y, min(w, 5.2) - 0.2, 0.34, anchor=MID)
    p = para(tf, first=True, space_after=0)
    _run(p, text, 11.5, PRIMARY_DK, bold=True, font=F_HEAD)


# =========================================================================
# SLIDE 1 - Title hero
# =========================================================================
s = new_slide()
background(s, INK)
# decorative shapes
rect(s, SW - 3.0, -2.2, 5.2, 5.2, fill=INK_SOFT, kind=MSO_SHAPE.OVAL)
rect(s, SW - 1.7, 0.7, 2.2, 2.2, fill=PRIMARY, kind=MSO_SHAPE.OVAL)
rect(s, SW - 2.35, 3.15, 0.75, 0.75, fill=ACCENT, kind=MSO_SHAPE.OVAL)
rrect(s, 0.9, 1.0, 0.14, 1.1, fill=ACCENT, radius=0.5)
# eyebrow
_, tf = textbox(s, 1.2, 1.02, 8.0, 0.4)
p = para(tf, first=True, space_after=0)
_run(p, "LECTURE 3", 16, PRIMARY_LT, bold=True, font=F_HEAD)
# title
_, tf = textbox(s, 1.15, 1.5, 9.6, 2.4)
p = para(tf, first=True, space_after=2, line_spacing=1.02)
_run(p, "Review of Literature", 46, WHITE, bold=True, font=F_TITLE)
p = para(tf, space_after=0, line_spacing=1.02)
_run(p, "for Identifying Research Problems", 46, WHITE, bold=True, font=F_TITLE)
# subtitle
_, tf = textbox(s, 1.18, 3.75, 9.4, 1.0)
p = para(tf, first=True, space_after=0, line_spacing=1.1)
_run(p, "Turning what others have studied into ", 20, PRIMARY_LT)
_run(p, "your", 20, ACCENT, bold=True, italic=True)
_run(p, " research problem, questions, and justification", 20, PRIMARY_LT)
# competencies pill
b = rrect(s, 1.2, 4.75, 4.6, 0.5, fill=PRIMARY, radius=0.4)
fill_frame(b, [("Competencies 11\u201316  \u00b7  Quantitative & Mixed Methods", 13.5, WHITE, True)], align=CENTER)
# process strip
_, tf = textbox(s, 1.2, 5.55, 8.0, 0.3)
p = para(tf, first=True, space_after=0)
_run(p, "THE RESEARCH WORKFLOW", 11, MUTED, bold=True, font=F_HEAD)
process_strip(s, 1.2, 5.9, 10.9, 0.62,
              ["Sources", "Synthesis", "Problem", "Questions", "Justification"], size=13)
# running examples footnote
_, tf = textbox(s, 1.2, 6.75, 11.0, 0.6)
p = para(tf, first=True, space_after=1, line_spacing=1.05)
_run(p, "Running examples (Philippine STEM):  ", 11.5, ACCENT, bold=True)
_run(p, "A) low-cost solar water distiller in a Zambales coastal barangay   \u00b7   "
        "B) dengue outbreak early-warning model for a Metro Manila city", 11.5, PRIMARY_LT)
notes(s, "Open by telling students this lecture answers a very practical question: \"I have an idea "
      "\u2014 now what?\" Emphasize that today's lesson is the engine room connecting an initial idea to an "
      "actual, defensible research problem. Set expectations: by the end, they will be able to evaluate "
      "sources, synthesize them into a gap, and write a problem statement, research questions/hypotheses, "
      "and a justification for a quantitative or mixed methods study.\n\n"
      "Visual: a clean horizontal research workflow diagram with five labeled stages "
      "(Sources \u2192 Synthesis \u2192 Problem Statement \u2192 Research Questions/Hypotheses \u2192 Justification). "
      "This same diagram reappears (highlighted stage-by-stage) throughout the deck to orient students.")

# =========================================================================
# SLIDE 2 - Why Literature Comes Before Solutions
# =========================================================================
s = new_slide()
y = header(s, "Section 1 \u00b7 Why Literature Review Comes First",
           "Why Literature Comes Before Solutions", 2)
two_column(s, y, 
    left={"title": "WITHOUT reviewing literature", "band": DANGER, "icon": "\u2715",
          "items": ["Risk of repeating a solution that already exists",
                    "Missing a known design flaw",
                    "Misjudging what data is even available"],
          "size": 22},
    right={"title": "WITH reviewing literature", "band": SUCCESS, "icon": "\u2713",
           "items": ["The study builds on, extends, or fills a real gap in existing knowledge"],
           "size": 22},
    bottom=5.75)
# key idea bar
b = rrect(s, 0.85, 6.0, SW - 1.7, 0.78, fill=INK, radius=0.1)
_, tf = textbox(s, 1.2, 6.0, SW - 2.4, 0.78, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.02)
_run(p, "KEY IDEA   ", 15, AMBER, bold=True, font=F_HEAD)
_run(p, "Research must ", 18, WHITE)
_run(p, "contribute", 18, AMBER, bold=True)
_run(p, " something new \u2014 not just restate an interesting topic.", 18, WHITE)
notes(s, "Ground this in Example A: a student wants to build a solar water distiller for a coastal "
      "barangay. If they skip the literature, they might not know that similar low-cost distillers have "
      "already been tested in other Philippine coastal communities \u2014 with results, design flaws, and "
      "lessons already documented. Explain that reviewing literature is not \"extra homework\" \u2014 it is the "
      "mechanism by which a study earns its place as research rather than just a project. Tie this "
      "explicitly to what students learned about ethics and citation in Lecture 2: using others' work "
      "responsibly is what allows this whole process to happen with integrity.\n\n"
      "Visual: a simple cause-and-effect model \u2014 two branching paths from the same starting idea, one "
      "leading to \"duplicated effort / weak contribution,\" the other to \"informed, defensible study.\"")

# =========================================================================
# SLIDE 3 - Today's Learning Roadmap
# =========================================================================
s = new_slide()
y = header(s, "Section 1 \u00b7 Why Literature Review Comes First",
           "Today's Learning Roadmap", 3)
steps = ["Evaluate sources", "Synthesize the literature", "Write the literature review",
         "Formulate the problem statement", "Develop research questions / hypotheses",
         "Justify the problem (CER)", "State assumptions & limitations"]
palette = [PRIMARY, PRIMARY, PRIMARY_DK, ACCENT, ACCENT, SUCCESS, AMBER]
cy = y + 0.05
rh = 0.63
x0 = 2.6
bw = 8.2
for i, st in enumerate(steps):
    badge = rect(s, x0 - 0.02, cy, 0.5, 0.5, fill=palette[i], kind=MSO_SHAPE.OVAL)
    fill_frame(badge, [(str(i + 1), 18, WHITE, True)], align=CENTER)
    bar = rrect(s, x0 + 0.7, cy, bw, 0.5, fill=CARD, line=LINE, radius=0.14, shadow=True)
    _, tf = textbox(s, x0 + 1.0, cy, bw - 0.4, 0.5, anchor=MID)
    p = para(tf, first=True, space_after=0)
    _run(p, st, 20, INK, bold=True, font=F_HEAD)
    if i < len(steps) - 1:
        connector(s, x0 + 0.23, cy + 0.5, x0 + 0.23, cy + rh, color=LINE, w=2.5)
    cy += rh
notes(s, "Walk through the roadmap once, briefly, so students see this is one continuous chain of "
      "reasoning, not seven unrelated topics. Tell them each stage's output becomes the next stage's "
      "input \u2014 sources feed synthesis, synthesis reveals gaps, gaps become problem statements, and so on. "
      "This framing reduces cognitive load because students always know \"where we are\" in the chain.\n\n"
      "Visual: a numbered vertical research process flowchart with arrows connecting each stage \u2014 reused "
      "as a \"you are here\" locator at the start of each new section.")

# =========================================================================
# SLIDE 4 - What Counts as a Source?
# =========================================================================
s = new_slide()
y = header(s, "Section 2 \u00b7 Evaluating Sources (Competency 11)",
           "What Counts as a Source?", 4)
cats = [
    ("JA", PRIMARY, "Journal articles", "Reports of actual studies (a question/hypothesis, data, an answer)"),
    ("BK", ACCENT, "Books", "Research monographs or edited collections"),
    ("GR", SUCCESS, "Government / institutional reports", "e.g., DOST, DENR, DOH, PSA"),
    ("WB", AMBER, "Credible websites", "From recognized organizations, not personal blogs or social media posts"),
]
cw = (SW - 1.7 - 0.5) / 2
ch = 1.95
positions = [(0.85, y + 0.1), (0.85 + cw + 0.5, y + 0.1),
             (0.85, y + 0.1 + ch + 0.35), (0.85 + cw + 0.5, y + 0.1 + ch + 0.35)]
for (mono, col, title, desc), (px, py) in zip(cats, positions):
    card(s, px, py, cw, ch)
    tile = rrect(s, px + 0.32, py + 0.35, 1.15, 1.15, fill=col, radius=0.2, shadow=True)
    fill_frame(tile, [(mono, 30, WHITE, True)], align=CENTER)
    _, tf = textbox(s, px + 1.7, py + 0.35, cw - 2.0, 1.3)
    p = para(tf, first=True, space_after=5, line_spacing=1.0)
    _run(p, title, 21, INK, bold=True, font=F_HEAD)
    p = para(tf, space_after=0, line_spacing=1.05)
    _run(p, desc, 15.5, MUTED)
notes(s, "Keep this concrete \u2014 students need a working mental checklist before they touch real "
      "material. Note that not everything found through a search engine counts as a usable academic "
      "source; the next few slides will teach them how to tell the difference, not just what the "
      "categories are.\n\nVisual: a simple four-box category chart, one icon per source type, as a quick "
      "visual reference students can mentally return to.")

# =========================================================================
# SLIDE 5 - Example: Sorting Real Sources
# =========================================================================
s = new_slide()
y = header(s, "Section 2 \u00b7 Evaluating Sources (Competency 11)",
           "Example \u2014 Sorting Real Sources", 5)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example")
data = [
    ["Item Found", "Source Type"],
    ["DOST-published feasibility study on solar water distillation", "Government / institutional report"],
    ["Peer-reviewed journal article on membrane distillation for rural water treatment", "Journal article"],
    ["A barangay health worker's personal Facebook post about \u201cclean water tips\u201d", "Not an academic source"],
    ["A university thesis available through an online repository", "Academic source (student research)"],
    ["A blog post summarizing \u201c5 easy DIY water filters\u201d", "Not an academic source"],
]
cell_colors = {(3, 1): DANGER_LT, (5, 1): DANGER_LT, (1, 1): SUCCESS_LT, (2, 1): SUCCESS_LT, (4, 1): PRIMARY_LT}
styled_table(s, 0.85, y + 0.45, SW - 1.7, data, col_widths=[1.6, 1.0],
             size=17, header_size=17, row_h=0.72, header_h=0.55, cell_colors=cell_colors)
notes(s, "Have students predict the category before revealing each answer \u2014 this creates a low-stakes "
      "retrieval moment before the harder evaluation skill in the next slide. Point out that a Facebook "
      "post can still contain useful ideas worth investigating further, but it is not itself citable as "
      "scholarly evidence.\n\nVisual: none needed beyond the table \u2014 keep this slide text-light and let "
      "the table do the work.")

# =========================================================================
# SLIDE 6 - The A-R-A Test
# =========================================================================
s = new_slide()
y = header(s, "Section 2 \u00b7 Evaluating Sources (Competency 11)",
           "The A-R-A Test for Sources", 6)
ara = [
    ("A", "Authority", "Who wrote it? What are their credentials or affiliation?", PRIMARY),
    ("R", "Relevance", "Does it actually match your topic, population, or timeframe?", ACCENT),
    ("A", "Accuracy", "Can the claims be checked or confirmed elsewhere?", SUCCESS),
]
cw = (SW - 1.7 - 2 * 0.45) / 3
for i, (letter, title, desc, col) in enumerate(ara):
    px = 0.85 + i * (cw + 0.45)
    card(s, px, y + 0.1, cw, 2.9)
    circ = rect(s, px + cw / 2 - 0.55, y + 0.4, 1.1, 1.1, fill=col, kind=MSO_SHAPE.OVAL, shadow=True)
    fill_frame(circ, [(letter, 40, WHITE, True)], align=CENTER)
    _, tf = textbox(s, px + 0.2, y + 1.65, cw - 0.4, 0.4)
    p = para(tf, first=True, align=CENTER, space_after=4)
    _run(p, title, 22, INK, bold=True, font=F_HEAD)
    _, tf = textbox(s, px + 0.28, y + 2.15, cw - 0.56, 0.9)
    p = para(tf, first=True, align=CENTER, space_after=0, line_spacing=1.05)
    _run(p, desc, 16, MUTED)
b = rrect(s, 0.85, y + 3.25, SW - 1.7, 0.7, fill=INK, radius=0.1)
_, tf = textbox(s, 1.2, y + 3.25, SW - 2.4, 0.7, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.0)
_run(p, "A source should pass ", 18, WHITE)
_run(p, "all three", 18, AMBER, bold=True)
_run(p, " \u2014 not just one \u2014 before it earns a place in your study.", 18, WHITE)
notes(s, "Frame this as a fast, usable filter \u2014 not the full professional information-literacy toolkit "
      "researchers eventually learn in college, just enough rigor to keep students from citing unreliable "
      "material. Emphasize that a source can be well-written and still fail the test (e.g., accurate but "
      "irrelevant, or relevant but from an unverifiable author).\n\nVisual: a decision tree \u2014 \"Does it "
      "have a credible author? \u2192 Does it match your topic? \u2192 Can you verify its claims?\" ending in "
      "\"Usable\" or \"Not usable yet \u2014 dig deeper.\"")

# =========================================================================
# SLIDE 7 - Example: Applying the A-R-A Test
# =========================================================================
s = new_slide()
y = header(s, "Section 2 \u00b7 Evaluating Sources (Competency 11)",
           "Example \u2014 Applying the A-R-A Test", 7)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
data = [
    ["Source", "Authority", "Relevance", "Accuracy", "Verdict"],
    ["DOST-published engineering report on solar distillers", "High (government agency)", "High (same technology)", "Checkable (data included)", "USABLE"],
    ["Personal blog: \u201cHow I Built My Own Water Filter\u201d", "Unclear author", "Partial (different method)", "Cannot verify claims", "NOT USABLE"],
    ["International journal article on solar distillation efficiency", "High (peer-reviewed)", "High", "Checkable", "USABLE"],
]
cell_colors = {(1, 4): SUCCESS_LT, (3, 4): SUCCESS_LT, (2, 4): DANGER_LT}
styled_table(s, 0.85, y + 0.5, SW - 1.7, data, col_widths=[1.9, 1.25, 1.2, 1.3, 1.0],
             size=14.5, header_size=15, row_h=0.92, header_h=0.5, cell_colors=cell_colors)
notes(s, "Walk through the table row by row and ask students to justify each verdict in their own words "
      "before you confirm it. This rehearses the A-R-A test on a topic they will actually use later in the "
      "lesson (Example A), so the skill and the content reinforce each other.\n\nVisual: none additional "
      "\u2014 the comparison table itself is the visual.")

# =========================================================================
# SLIDE 8 - Application: Rate These Sources
# =========================================================================
s = new_slide()
y = header(s, "Section 2 \u00b7 Evaluating Sources (Competency 11)",
           "Application \u2014 Rate These Sources", 8)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example B topic")
data = [
    ["#", "Source", "Your verdict (apply A-R-A)"],
    ["1", "A DOH dengue surveillance report with raw case data", ""],
    ["2", "A viral text message claiming a \u201cmiracle dengue cure\u201d", ""],
    ["3", "A peer-reviewed study on rainfall and dengue incidence in an Asian city", ""],
    ["4", "A five-year-old news article about a local dengue outbreak", ""],
]
cell_colors = {(1, 2): AMBER_LT, (2, 2): AMBER_LT, (3, 2): AMBER_LT, (4, 2): AMBER_LT}
styled_table(s, 0.85, y + 0.5, SW - 1.7, data, col_widths=[0.3, 2.4, 1.5],
             size=17, header_size=16, row_h=0.72, header_h=0.5, cell_colors=cell_colors)
instruction_bar(s, 0.85, y + 3.85, SW - 1.7,
                "In pairs: apply Authority \u2013 Relevance \u2013 Accuracy to each, then share out.")
notes(s, "This is a guided-practice checkpoint \u2014 students apply the A-R-A test independently in pairs, "
      "then share out. Circulate to catch common errors, especially the tendency to treat \"recent\" as "
      "automatically the same as \"accurate,\" or to assume a government report is automatically "
      "unbiased.\n\nVisual: none required; this is a discussion-based worksheet slide.")

# =========================================================================
# SLIDE 9 - Summarizing vs Synthesizing
# =========================================================================
s = new_slide()
y = header(s, "Section 3 \u00b7 Synthesizing the Literature (Competency 12)",
           "Summarizing vs. Synthesizing", 9)
data = [
    ["Summarizing", "Synthesizing"],
    ["Describes one source at a time", "Connects multiple sources by theme"],
    ["\u201cSource A found X. Source B found Y.\u201d", "\u201cSources A and B agree that X, but disagree on Y.\u201d"],
    ["Produces a list", "Produces an argument about the state of knowledge"],
]
styled_table(s, 0.85, y + 0.2, SW - 1.7, data, col_widths=[1, 1],
             size=20, header_size=20, row_h=1.0, header_h=0.62,
             header_fill=MUTED)
# recolor second header to primary via overlay
notes(s, "Name this as the single most common trap for beginning researchers: writing what looks like a "
      "literature review but is actually just a string of one-paragraph book reports. Tell students that a "
      "synthesis should read like a conversation between sources, not a list of separate summaries.\n\n"
      "Visual: a side-by-side visual \u2014 on the left, disconnected boxes (one per source); on the right, "
      "the same boxes connected by lines into a shared theme \u2014 reinforcing \"listing\" versus \"weaving.\"")

# =========================================================================
# SLIDE 10 - Example: Summary vs Synthesis
# =========================================================================
s = new_slide()
y = header(s, "Section 3 \u00b7 Synthesizing the Literature (Competency 12)",
           "Example \u2014 Summary vs. Synthesis Side by Side", 10, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example B \u2014 three dengue-prediction studies")
# summary card
card(s, 0.85, y + 0.5, SW - 1.7, 1.7)
card_header(s, 0.85, y + 0.5, SW - 1.7, "SUMMARY VERSION", MUTED, size=16)
_, tf = textbox(s, 1.2, y + 1.3, SW - 2.4, 0.9, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.1)
_run(p, "\u201cStudy 1 used rainfall data. Study 2 used temperature data. "
        "Study 3 used both rainfall and temperature.\u201d", 22, INK, italic=True)
# synthesis card
card(s, 0.85, y + 2.4, SW - 1.7, 1.85, fill="FBFDFE", line=PRIMARY)
card_header(s, 0.85, y + 2.4, SW - 1.7, "SYNTHESIS VERSION", PRIMARY, size=16)
_, tf = textbox(s, 1.2, y + 3.2, SW - 2.4, 1.0, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.1)
_run(p, "\u201cMost dengue prediction studies rely on rainfall and temperature, but they consistently "
        "leave out ", 22, INK, italic=True)
_run(p, "human mobility patterns", 22, ACCENT, bold=True, italic=True)
_run(p, " \u2014 a factor increasingly seen as relevant in outbreak spread.\u201d", 22, INK, italic=True)
notes(s, "Read both versions aloud and ask students which one would actually help a reader understand "
      "what's missing in the field. Point out that the synthesis version does something the summary "
      "cannot: it sets up a gap, which is exactly what the next few slides will teach them to find on "
      "purpose.\n\nVisual: none needed \u2014 direct text contrast is the point.")

# =========================================================================
# SLIDE 11 - Grouping Sources by Theme
# =========================================================================
s = new_slide()
y = header(s, "Section 3 \u00b7 Synthesizing the Literature (Competency 12)",
           "Grouping Sources by Theme", 11)
steps = [
    [("Step 1  ", True, False, PRIMARY), ("Read across all your gathered sources", False)],
    [("Step 2  ", True, False, PRIMARY), ("Identify shared variables, populations, or ideas", False)],
    [("Step 3  ", True, False, PRIMARY), ("Cluster sources under those shared themes (not by author or date)", False)],
]
bullets(s, 0.9, y + 0.25, 5.6, steps, size=21, gap=18, bullet_color=PRIMARY)
# concept map right side
cxr = 9.35
cy0 = y + 1.55
center = rect(s, cxr - 0.85, cy0 - 0.5, 1.7, 1.0, fill=INK, kind=MSO_SHAPE.ROUNDED_RECTANGLE)
try:
    center.adjustments[0] = 0.2
except Exception:
    pass
fill_frame(center, [("Gathered\nsources", 15, WHITE, True)], align=CENTER)
themes = [("Rainfall-based\nmodels", PRIMARY, cxr - 1.7, cy0 - 2.35),
          ("Temperature-based\nmodels", ACCENT, cxr + 1.05, cy0 - 1.0),
          ("Combined climate\nmodels", SUCCESS, cxr - 1.7, cy0 + 1.35)]
for label, col, bx, by in themes:
    connector(s, cxr, cy0, bx + 0.85, by + 0.42, color=LINE, w=2.0)
for label, col, bx, by in themes:
    bub = rrect(s, bx, by, 1.9, 0.85, fill=col, radius=0.2, shadow=True)
    fill_frame(bub, [(label, 13.5, WHITE, True)], align=CENTER)
notes(s, "Explain that grouping by theme is what makes synthesis possible \u2014 you cannot compare sources "
      "that are scattered randomly. Use Example B again: sources might cluster into \"rainfall-based "
      "models,\" \"temperature-based models,\" and \"combined climate models,\" which immediately makes it "
      "visible where overlaps and gaps sit.\n\nVisual: a concept map with three or four theme bubbles, "
      "each containing two to three small source labels \u2014 modelling the clustering process.")

# =========================================================================
# SLIDE 12 - Spotting Gaps, Issues, and Needs
# =========================================================================
s = new_slide()
y = header(s, "Section 3 \u00b7 Synthesizing the Literature (Competency 12)",
           "Spotting Gaps, Issues, and Needs", 12)
gin = [
    ("Gap", PRIMARY, "Something the literature has not studied yet"),
    ("Issue", ACCENT, "Something the literature disagrees or is inconsistent about"),
    ("Need", SUCCESS, "Something the literature explicitly calls for but has not yet addressed"),
]
cw = (SW - 1.7 - 2 * 0.45) / 3
for i, (title, col, desc) in enumerate(gin):
    px = 0.85 + i * (cw + 0.45)
    card(s, px, y + 0.25, cw, 3.4)
    card_header(s, px, y + 0.25, cw, title.upper(), col, size=20, h=0.7)
    _, tf = textbox(s, px + 0.3, y + 1.2, cw - 0.6, 2.2, anchor=MSO_ANCHOR.TOP)
    p = para(tf, first=True, space_after=0, line_spacing=1.15)
    _run(p, desc, 22, INK)
notes(s, "Stress that not every synthesis reveals a gap \u2014 sometimes it reveals a disagreement (issue) "
      "or an explicit call for more research (need), and all three are valid springboards for a new study. "
      "Beginning researchers often assume they must find a totally unstudied topic; reframe this as "
      "unrealistic and unnecessary \u2014 even a small, well-defined gap is enough.\n\nVisual: three-column "
      "layout with color-coded headers keeping the definitions visually distinct.")

# =========================================================================
# SLIDE 13 - Example: Finding the Real Gap
# =========================================================================
s = new_slide()
y = header(s, "Section 3 \u00b7 Synthesizing the Literature (Competency 12)",
           "Example \u2014 Finding the Real Gap", 13)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example B topic")
bullets(s, 0.9, y + 0.55, SW - 1.9, [
    "Most Philippine dengue early-warning studies use rainfall and temperature data",
    "Few studies incorporate community-level human mobility patterns, even though outbreaks often follow people's movement, not just weather",
], size=23, gap=12, bullet_color=PRIMARY)
# arrow synthesis -> gap
b = rrect(s, 0.85, y + 2.35, SW - 1.7, 1.15, fill=ACCENT_LT, line=ACCENT, radius=0.08)
_, tf = textbox(s, 1.2, y + 2.35, SW - 2.4, 1.15, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.1)
_run(p, "IDENTIFIED GAP   ", 15, ACCENT, bold=True, font=F_HEAD)
_run(p, "The role of ", 23, INK)
_run(p, "human mobility", 23, ACCENT, bold=True)
_run(p, " in dengue prediction models remains underexplored.", 23, INK)
# small flow
mini = ["Synthesis finding", "Identified gap"]
xx = 3.2
for i, m in enumerate(mini):
    bb = rrect(s, xx, y + 3.75, 3.0, 0.55, fill=(PRIMARY if i == 0 else ACCENT), radius=0.2)
    fill_frame(bb, [(m, 15, WHITE, True)], align=CENTER)
    if i == 0:
        right_arrow(s, xx + 3.1, y + 4.02, color=INK, w=0.55)
    xx += 3.65
notes(s, "Walk through how this gap statement emerged directly from the synthesis on Slide 10 \u2014 this is "
      "the payoff moment where students see synthesis is not just an exercise, it produces the seed of a "
      "real problem statement. Ask students to predict what a research problem statement built from this "
      "gap might sound like, previewing Section 5.\n\nVisual: a short cause-and-effect model showing "
      "\"synthesis finding \u2192 identified gap,\" visually linking back to Slide 10.")

# =========================================================================
# SLIDE 14 - The Synthesis Matrix Tool
# =========================================================================
s = new_slide()
y = header(s, "Section 3 \u00b7 Synthesizing the Literature (Competency 12)",
           "The Synthesis Matrix Tool", 14)
bullets(s, 0.9, y + 0.05, SW - 1.9, [
    [("A ", False), ("synthesis matrix", True, False, PRIMARY), (" is a table where each row is a source and each column is a theme", False)],
    "Filling in the cells shows which sources cover which themes \u2014 and which themes are thin or missing",
], size=20, gap=8, bullet_color=PRIMARY)
data = [
    ["Source", "Rainfall factor", "Temperature factor", "Mobility factor"],
    ["Study 1", "\u2713", "", ""],
    ["Study 2", "", "\u2713", ""],
    ["Study 3", "\u2713", "\u2713", ""],
]
cc = {(1, 3): AMBER_LT, (2, 3): AMBER_LT, (3, 3): AMBER_LT}
styled_table(s, 0.85, y + 1.6, SW - 1.7, data, col_widths=[1, 1.2, 1.3, 1.2],
             size=20, header_size=17, row_h=0.62, header_h=0.6, cell_colors=cc)
_, tf = textbox(s, 0.85, y + 4.05, SW - 1.7, 0.4)
p = para(tf, first=True, space_after=0)
_run(p, "The empty ", 15, MUTED)
_run(p, "Mobility factor", 15, AMBER, bold=True)
_run(p, " column is exactly the gap \u2014 the matrix makes gaps visible almost automatically.", 15, MUTED)
notes(s, "Present this as a thinking tool, not a required format \u2014 some students will find it easier to "
      "spot gaps visually in a matrix than by reading notes. Point out the empty \"Mobility factor\" column "
      "is exactly the gap identified on the previous slide \u2014 the matrix makes gaps visible almost "
      "automatically.\n\nVisual: the matrix itself; empty cells are colour-shaded to draw the eye toward "
      "the gap.")

# =========================================================================
# SLIDE 15 - Application: Build a Mini Synthesis Matrix
# =========================================================================
s = new_slide()
y = header(s, "Section 3 \u00b7 Synthesizing the Literature (Competency 12)",
           "Application \u2014 Build a Mini Synthesis Matrix", 15, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
data = [
    ["Source", "Distiller design", "Water safety testing", "Community adoption"],
    ["Source 1: engineering report", "\u2713", "", ""],
    ["Source 2: WHO water safety guideline", "", "\u2713", ""],
    ["Source 3: rural adoption case study", "", "", "\u2713"],
]
styled_table(s, 0.85, y + 0.5, SW - 1.7, data, col_widths=[1.9, 1.2, 1.4, 1.4],
             size=18, header_size=16, row_h=0.7, header_h=0.6)
instruction_bar(s, 0.85, y + 3.55, SW - 1.7,
                "In pairs: which theme has the weakest coverage? Phrase a one-sentence gap statement from it.")
notes(s, "Ask students, in pairs, to identify which theme has the weakest coverage and phrase a "
      "one-sentence gap statement from it. This directly rehearses the skill they will need heavily in "
      "Section 5 (writing a problem statement), so treat this as a checkpoint rather than a throwaway "
      "activity.\n\nVisual: none additional \u2014 the matrix is the activity.")

# =========================================================================
# SLIDE 16 - What a Literature Review Actually Does
# =========================================================================
s = new_slide()
y = header(s, "Section 4 \u00b7 Writing the Literature Review",
           "What a Literature Review Actually Does", 16, title_size=29)
items = [
    "Shares what related studies have already found",
    "Connects your study to the larger, ongoing conversation in the field",
    "Provides a framework for judging the importance of your study",
    "Gives a benchmark for later comparing your own results",
]
cy = y + 0.5
for i, it in enumerate(items):
    b = rrect(s, 1.6, cy, SW - 3.2, 0.82, fill=CARD, line=LINE, radius=0.12, shadow=True)
    badge = rect(s, 1.85, cy + 0.19, 0.44, 0.44, fill=PRIMARY, kind=MSO_SHAPE.OVAL)
    fill_frame(badge, [(str(i + 1), 17, WHITE, True)], align=CENTER)
    _, tf = textbox(s, 2.55, cy, SW - 3.2 - 1.1, 0.82, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.0)
    _run(p, it, 22, INK)
    cy += 1.02
notes(s, "Clarify that everything students have done so far (evaluating sources, synthesizing, finding a "
      "gap) has been preparation \u2014 this slide introduces the actual written product that packages all of "
      "that. In quantitative and mixed methods research specifically, the literature review is written "
      "before data collection and directly sets up the research questions or hypotheses that follow.\n\n"
      "Visual: none required \u2014 keep this a clean transition slide.")

# =========================================================================
# SLIDE 17 - The Quantitative Literature Review Structure
# =========================================================================
s = new_slide()
y = header(s, "Section 4 \u00b7 Writing the Literature Review",
           "The Quantitative Literature Review Structure", 17, title_size=28)
items = [
    ("1  Introduction", "previews the sections to come"),
    ("2  Topic 1", "literature on the independent variable"),
    ("3  Topic 2", "literature on the dependent variable"),
    ("4  Topic 3", "studies that connect both variables together"),
    ("5  Summary", "key themes \u00b7 why more research is needed \u00b7 how the study fills the need"),
]
widths = [9.6, 8.4, 7.2, 6.0, 8.8]
colors = [PRIMARY, PRIMARY, PRIMARY_DK, ACCENT, INK]
funnel(s, SW / 2, y + 0.12, items, widths, colors, box_h=0.78, gap=0.14, size=18)
notes(s, "Explain that this five-part structure is the standard way quantitative studies organize a "
      "written literature review \u2014 it keeps the review tightly focused on the variables the study will "
      "actually investigate, rather than sprawling into loosely related topics. Point out that Topic 3 is "
      "usually the shortest section because directly relevant combined studies are often scarce \u2014 and "
      "that scarcity is often itself part of the gap.\n\nVisual: a funnel-shaped process diagram narrowing "
      "from Topic 1 and Topic 2 (broad, separate) down into Topic 3 (narrow, combined) and finally the "
      "Summary.")

# =========================================================================
# SLIDE 18 - Example: Applying the Five-Part Structure
# =========================================================================
s = new_slide()
y = header(s, "Section 4 \u00b7 Writing the Literature Review",
           "Example \u2014 Applying the Five-Part Structure", 18, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
rows = [
    ("Introduction:", "This review covers solar water distillation design, microbial water safety, and studies linking the two"),
    ("Topic 1 (independent variable):", "literature on solar water distiller designs and efficiency"),
    ("Topic 2 (dependent variable):", "literature on microbial contamination levels and water safety standards"),
    ("Topic 3 (linking studies):", "the few existing studies testing distillation's direct effect on microbial safety"),
    ("Summary:", "most studies test distillation efficiency or water safety separately, rarely together in a Philippine coastal barangay setting"),
]
cy = y + 0.5
for i, (lab, body) in enumerate(rows):
    col = [PRIMARY, PRIMARY, PRIMARY_DK, ACCENT, INK][i]
    tab = rrect(s, 0.85, cy, 0.12, 0.62, fill=col, radius=0.5)
    _, tf = textbox(s, 1.15, cy, SW - 2.1, 0.7, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.02)
    _run(p, lab + "  ", 18.5, col, bold=True, font=F_HEAD)
    _run(p, body, 18.5, INK)
    cy += 0.82
notes(s, "Walk through each part slowly, showing how the outline mirrors the five-part structure exactly. "
      "This is the moment students see that \"the gap\" they found earlier fits naturally into the Summary "
      "section as the closing statement of the literature review.\n\nVisual: none additional \u2014 the "
      "outline itself functions as the visual scaffold.")

# =========================================================================
# SLIDE 19 - Literature Review in a Mixed Methods Study
# =========================================================================
s = new_slide()
y = header(s, "Section 4 \u00b7 Writing the Literature Review",
           "Literature Review in a Mixed Methods Study", 19, title_size=28)
# central node
top = rrect(s, SW / 2 - 2.1, y + 0.15, 4.2, 0.7, fill=INK, radius=0.12, shadow=True)
fill_frame(top, [("Which phase leads the study's design?", 17, WHITE, True)], align=CENTER)
# branches
by = y + 1.85
lx, rx = 2.4, 8.0
bw = 3.0
connector(s, SW / 2, y + 0.85, lx + bw / 2, by, color=PRIMARY, w=2.5)
connector(s, SW / 2, y + 0.85, rx + bw / 2, by, color=ACCENT, w=2.5)
for label, desc, col, bx in [
    ("Quantitative-first", "Include a fuller literature review upfront, similar to the five-part structure", PRIMARY, lx),
    ("Qualitative-first", "Include less literature upfront; more may be added later as findings emerge", ACCENT, rx)]:
    card_header(s, bx, by, bw, label, col, size=17)
    cbody = card(s, bx, by + 0.62, bw, 1.85)
    _, tf = textbox(s, bx + 0.28, by + 0.62, bw - 0.56, 1.85, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.12)
    _run(p, desc, 18, INK)
b = rrect(s, 0.85, y + 4.35, SW - 1.7, 0.62, fill=PRIMARY_LT, radius=0.1)
_, tf = textbox(s, 1.2, y + 4.35, SW - 2.4, 0.62, anchor=MID)
p = para(tf, first=True, space_after=0)
_run(p, "The choice depends on which phase leads the study's design.", 18, INK_SOFT, bold=True)
notes(s, "Keep this brief \u2014 the goal is only to help students recognize that \"how much literature "
      "review, and when\" is a design decision tied to which method leads, not a fixed rule. Since most SHS "
      "capstone-style studies are quantitative or quantitative-led mixed methods, reassure students the "
      "five-part structure from the previous slides will usually apply.\n\nVisual: a short decision tree "
      "with two branches labelled \"Quantitative-first\" and \"Qualitative-first,\" each pointing to a "
      "different literature review depth.")

# =========================================================================
# SLIDE 20 - Application: Outline Your Own Review
# =========================================================================
s = new_slide()
y = header(s, "Section 4 \u00b7 Writing the Literature Review",
           "Application \u2014 Outline Your Own Review", 20, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Activity template")
template_card(s, 0.85, y + 0.5, SW - 1.7, 4.3, [
    "Introduction:", "Topic 1 (independent variable):", "Topic 2 (dependent variable):",
    "Topic 3 (linking studies):", "Summary / gap statement:",
], size=22)
notes(s, "Have students use their own emerging topic (or Example B, dengue prediction, if they don't have "
      "one yet) to fill in this template. This is a natural checkpoint before moving into problem "
      "statement writing, since the Summary line they write here becomes the raw material for the next "
      "section.\n\nVisual: none needed; the template is the activity.")

# =========================================================================
# SLIDE 21 - From Gap to Problem Statement
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "From Gap to Problem Statement", 21)
bw = 5.1
by = y + 0.85
# step 1
card(s, 0.85, by, bw, 2.3)
card_header(s, 0.85, by, bw, "STEP 1 \u00b7 YOU HAVE A GAP", PRIMARY, size=16)
_, tf = textbox(s, 1.15, by + 0.8, bw - 0.6, 1.4, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.12)
_run(p, "\u201cHuman mobility is underused in dengue prediction models.\u201d", 22, INK, italic=True)
# arrow
a = rect(s, 6.15, by + 0.9, 1.0, 0.5, fill=ACCENT, kind=MSO_SHAPE.RIGHT_ARROW)
# step 2
card(s, 7.4, by, bw, 2.3)
card_header(s, 7.4, by, bw, "STEP 2 \u00b7 PROBLEM STATEMENT", ACCENT, size=16)
_, tf = textbox(s, 7.7, by + 0.8, bw - 0.6, 1.4, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.12)
_run(p, "A focused, researchable claim about what is missing and why it matters", 22, INK)
notes(s, "Emphasize that a gap and a problem statement are not the same thing \u2014 a gap describes what's "
      "missing in the literature, while a problem statement describes the specific issue your study will "
      "investigate. This distinction prevents students from simply copying their gap sentence and calling "
      "it a problem statement.\n\nVisual: none additional \u2014 the two-step arrow captures the "
      "transformation clearly enough on its own.")

# =========================================================================
# SLIDE 22 - Characteristics of a Researchable Problem
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "Characteristics of a Researchable Problem", 22, title_size=28)
checklist(s, 1.4, y + 0.35, SW - 2.8, [
    [("Addresses a real ", False), ("knowledge gap", True)],
    [("Is ", False), ("current and relevant", True), (", not outdated", False)],
    [("Is ", False), ("based on facts and evidence", True), (", not assumptions or hypothetical situations", False)],
    [("Is ", False), ("tangible", True), (" \u2014 realistic given the time, budget, and skills available", False)],
    [("Naturally ", False), ("generates further research questions", True)],
], size=23, row_h=0.72, gap=0.18)
notes(s, "Point out that \"tangible\" is often the criterion beginning researchers ignore \u2014 an excellent "
      "problem statement that would require resources or access far beyond a school-based project is not "
      "usable yet, no matter how interesting it is. Encourage students to test any problem statement they "
      "draft against all five criteria, not just one or two.\n\nVisual: a checklist-style graphic (five "
      "checkmarks) that can repeat later as a self-assessment tool.")

# =========================================================================
# SLIDE 23 - Three Building Blocks
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "Three Building Blocks: Context, Relevance, Strategy", 23, title_size=26)
items = [
    ("Context", "the background and current situation surrounding the issue"),
    ("Relevance", "why the issue matters, and who is affected if it stays unresolved"),
    ("Strategy", "the general goal and approach your study will take to address it"),
]
widths = [10.6, 8.6, 6.6]
colors = [PRIMARY, ACCENT, SUCCESS]
funnel(s, SW / 2, y + 0.15, items, widths, colors, box_h=0.85, gap=0.16, size=19)
b = rrect(s, SW / 2 - 4.0, y + 3.25, 8.0, 0.68, fill=INK, radius=0.14, shadow=True)
fill_frame(b, [("\u2193  These three, written in order, build a complete problem statement", 16.5, WHITE, True)], align=CENTER)
notes(s, "Present this as a practical writing formula, not an abstract theory \u2014 students often freeze "
      "when told to \"just write a problem statement,\" so giving them three concrete building blocks to "
      "write in sequence makes the task approachable. Note that this structure works whether the final "
      "study is fully quantitative or a quantitative-led mixed methods design.\n\nVisual: a funnel diagram "
      "narrowing from Context (widest) to Relevance to Strategy (narrowest), ending in a single "
      "problem-statement sentence.")

# =========================================================================
# SLIDE 24 - Example: Writing a Problem Statement Step by Step
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "Example \u2014 Writing a Problem Statement Step by Step", 24, title_size=25)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
rows = [
    ("Context:", "Many coastal barangays rely on unsafe drinking water sources, and low-cost solar distillers have been proposed as a solution", PRIMARY),
    ("Relevance:", "Existing studies test either distiller efficiency or water safety standards, but rarely both together in an actual barangay setting", ACCENT),
    ("Strategy:", "This study will test the distiller's real-world effect on microbial water safety", SUCCESS),
]
cy = y + 0.5
for lab, body, col in rows:
    tab = rrect(s, 0.85, cy, 0.12, 0.68, fill=col, radius=0.5)
    _, tf = textbox(s, 1.15, cy, SW - 2.1, 0.75, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.05)
    _run(p, lab + "  ", 18, col, bold=True, font=F_HEAD)
    _run(p, body, 18, INK)
    cy += 0.78
# final boxed statement
fb = rrect(s, 0.85, cy + 0.05, SW - 1.7, 1.15, fill=INK, radius=0.08, shadow=True)
_, tf = textbox(s, 1.2, cy + 0.05, SW - 2.4, 1.15, anchor=MID)
p = para(tf, first=True, space_after=3, line_spacing=1.05)
_run(p, "FINAL PROBLEM STATEMENT", 13, AMBER, bold=True, font=F_HEAD)
p = para(tf, space_after=0, line_spacing=1.08)
_run(p, "\u201cThis study addresses the limited evidence on whether a low-cost solar water distiller "
        "measurably improves the microbial safety of drinking water in a coastal barangay setting.\u201d",
     17.5, WHITE, italic=True)
notes(s, "Read the final boxed statement aloud and ask students to identify which sentence came from "
      "Context, which from Relevance, and which from Strategy \u2014 this reverse-engineering check reinforces "
      "the formula. Note how directly this statement traces back to the Topic 3/Summary gap identified in "
      "Slide 18.\n\nVisual: none additional beyond the highlighted final-statement box.")

# =========================================================================
# SLIDE 25 - Common Pitfalls in Problem Statements
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "Common Pitfalls in Problem Statements", 25, title_size=28)
data = [
    ["Pitfall", "Fix"],
    ["Too broad: \u201cWater pollution is a big problem.\u201d", "Narrow to a specific variable, population, or setting"],
    ["Too vague: \u201cSomething should be done about dengue.\u201d", "State exactly what is missing or unresolved"],
    ["Merely descriptive: \u201cMany barangays use rainwater.\u201d", "Add why this is an unresolved issue worth studying"],
    ["Unanswerable: \u201cIs clean water important?\u201d", "Rephrase around something investigable with data"],
]
styled_table(s, 0.85, y + 0.25, SW - 1.7, data, col_widths=[1.15, 1.0],
             size=18, header_size=18, row_h=0.86, header_h=0.58,
             header_fill=DANGER)
notes(s, "Go through each pitfall using a \"spot what's wrong\" approach before revealing the fix \u2014 this "
      "keeps students actively diagnosing rather than passively reading. Connect the \"merely descriptive\" "
      "pitfall back to Slide 22's criteria: a true problem statement must show why something is "
      "unresolved, not just describe a situation.\n\nVisual: none additional; the table's two-column "
      "contrast is sufficient.")

# =========================================================================
# SLIDE 26 - Application: Diagnose and Fix
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "Application \u2014 Diagnose and Fix", 26)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example")
statements = [
    "\u201cRenewable energy is important for the Philippines.\u201d",
    "\u201cThis study is about students and their phones.\u201d",
    "\u201cFlooding happens in many cities during the rainy season.\u201d",
]
cy = y + 0.55
for i, st in enumerate(statements):
    b = rrect(s, 0.85, cy, SW - 1.7, 0.95, fill=CARD, line=LINE, radius=0.1, shadow=True)
    badge = rect(s, 1.1, cy + 0.26, 0.44, 0.44, fill=DANGER, kind=MSO_SHAPE.OVAL)
    fill_frame(badge, [(str(i + 1), 17, WHITE, True)], align=CENTER)
    _, tf = textbox(s, 1.75, cy, SW - 1.7 - 1.2, 0.95, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.0)
    _run(p, st, 22, INK, italic=True)
    cy += 1.12
instruction_bar(s, 0.85, cy - 0.02, SW - 1.7,
                "In pairs: name the pitfall, then rewrite using the Context \u2013 Relevance \u2013 Strategy formula.")
notes(s, "Have students work in pairs to name which pitfall each statement falls into, then rewrite it "
      "using the Context\u2013Relevance\u2013Strategy formula from Slide 23. Circulate and prompt students who "
      "write a \"fixed\" version that is still too broad \u2014 a common second-round mistake.\n\nVisual: none "
      "required; this is a peer-editing activity.")

# =========================================================================
# SLIDE 27 - From Problem Statement to Research Questions
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "From Problem Statement to Research Questions", 27, title_size=27)
# left problem node
ph = 1.4
pby = y + 1.1
pnode = rrect(s, 0.9, pby, 3.4, ph, fill=INK, radius=0.1, shadow=True)
fill_frame(pnode, [("Problem Statement\nnames the issue", 17, WHITE, True)], align=CENTER)
rqs = ["Research Question 1", "Research Question 2", "Research Question 3"]
qx = 6.6
qh = 0.72
qy = y + 0.35
for i, q in enumerate(rqs):
    b = rrect(s, qx, qy, 5.4, qh, fill=PRIMARY if i != 2 else PRIMARY_DK, radius=0.15, shadow=True)
    fill_frame(b, [(q, 18, WHITE, True)], align=CENTER)
    connector(s, 4.3, pby + ph / 2, qx, qy + qh / 2, color=ACCENT, w=2.2)
    qy += qh + 0.5
bullets(s, 0.9, y + 3.1, SW - 1.9, [
    "A problem statement names the issue",
    "Research questions break that issue into specific, answerable pieces",
    "One problem statement can lead to one or several research questions",
], size=19, gap=6, bullet_color=PRIMARY, h=1.6)
notes(s, "Use Example A's problem statement from Slide 24 and ask students what specific question it "
      "raises \u2014 guide them toward something like \"Is there a significant difference in microbial "
      "contamination before and after distillation?\" This models the narrowing process concretely before "
      "the formal criteria are introduced.\n\nVisual: a single arrow diagram \u2014 \"Problem Statement\" "
      "branching into two or three \"Research Question\" boxes.")

# =========================================================================
# SLIDE 28 - Qualities of a Good Research Question
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "Qualities of a Good Research Question", 28, title_size=28)
qual = [
    ("Clear", "uses precise, unambiguous language", PRIMARY),
    ("Focused", "addresses one specific issue, not several at once", ACCENT),
    ("Answerable", "can actually be investigated through data collection", SUCCESS),
]
cw = (SW - 1.7 - 2 * 0.5) / 3
for i, (t, d, col) in enumerate(qual):
    px = 0.85 + i * (cw + 0.5)
    card(s, px, y + 0.35, cw, 3.1)
    circ = rect(s, px + cw / 2 - 0.5, y + 0.7, 1.0, 1.0, fill=col, kind=MSO_SHAPE.OVAL, shadow=True)
    fill_frame(circ, [("\u2713", 34, WHITE, True)], align=CENTER)
    _, tf = textbox(s, px + 0.2, y + 1.85, cw - 0.4, 0.45)
    p = para(tf, first=True, align=CENTER, space_after=4)
    _run(p, t, 23, INK, bold=True, font=F_HEAD)
    _, tf = textbox(s, px + 0.3, y + 2.35, cw - 0.6, 1.0, anchor=MSO_ANCHOR.TOP)
    p = para(tf, first=True, align=CENTER, space_after=0, line_spacing=1.08)
    _run(p, d, 17, MUTED)
notes(s, "Point out that \"answerable\" is the criterion students most often miss \u2014 a research question "
      "phrased as an opinion (\"Should schools invest in solar energy?\") cannot be answered with data the "
      "way a phrased comparison or relationship question can.\n\nVisual: none required; keep this a clean "
      "checklist.")

# =========================================================================
# SLIDE 29 - Example: Turning a Problem Into Questions
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "Example \u2014 Turning a Problem Into Questions", 29, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
card(s, 0.85, y + 0.6, SW - 1.7, 1.4)
card_header(s, 0.85, y + 0.6, SW - 1.7, "PROBLEM STATEMENT (from Slide 24)", INK, size=15)
_, tf = textbox(s, 1.2, y + 1.4, SW - 2.4, 0.6, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.05)
_run(p, "Limited evidence on whether the distiller improves microbial water safety.", 20, INK)
down_arrow(s, SW / 2, y + 2.15, color=ACCENT, w=0.55, h=0.4)
card(s, 0.85, y + 2.7, SW - 1.7, 1.5, fill="FBFDFE", line=PRIMARY)
card_header(s, 0.85, y + 2.7, SW - 1.7, "RESEARCH QUESTION", PRIMARY, size=15)
_, tf = textbox(s, 1.2, y + 3.5, SW - 2.4, 0.7, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.08)
_run(p, "\u201cWhat is the difference in microbial contamination levels of drinking water before and after "
        "solar distillation treatment?\u201d", 21, INK, italic=True)
notes(s, "Ask students to check this question against the three qualities from Slide 28 \u2014 is it clear, "
      "focused, and answerable? This rehearses evaluation, not just recall, and prepares them to critique "
      "their own questions later.\n\nVisual: none additional.")

# =========================================================================
# SLIDE 30 - Introducing the Hypothesis
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "Introducing the Hypothesis", 30)
card(s, 0.85, y + 0.5, SW - 1.7, 1.7, fill=PRIMARY_LT, line=PRIMARY)
_, tf = textbox(s, 1.3, y + 0.5, SW - 2.6, 1.7, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.1)
_run(p, "A ", 24, INK)
_run(p, "hypothesis", 24, PRIMARY_DK, bold=True, italic=True)
_run(p, " is a predicted answer to a research question, stated before data is collected.", 24, INK)
b = rrect(s, 0.85, y + 2.6, SW - 1.7, 1.5, fill=CARD, line=LINE, radius=0.1, shadow=True)
_, tf = textbox(s, 1.3, y + 2.6, SW - 2.6, 1.5, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.15)
_run(p, "Quantitative studies typically use ", 22, INK)
_run(p, "hypotheses", 22, ACCENT, bold=True)
_run(p, "; purely exploratory studies may use ", 22, INK)
_run(p, "research questions only", 22, SUCCESS, bold=True)
_run(p, ".", 22, INK)
notes(s, "Keep this brief and definitional \u2014 the point is only to introduce hypotheses as the "
      "quantitative counterpart to research questions, not to reopen the qualitative-vs-quantitative "
      "discussion from Lecture 1 in depth. Reassure students that since this course is building toward "
      "quantitative and mixed methods studies, they will usually be writing both a research question and "
      "its matching hypothesis.\n\nVisual: none required.")

# =========================================================================
# SLIDE 31 - Variables in a Hypothesis
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "Variables in a Hypothesis", 31)
by = y + 0.65
iv = rrect(s, 1.3, by, 4.2, 1.7, fill=PRIMARY, radius=0.1, shadow=True)
tf = iv.text_frame; tf.word_wrap = True; tf.vertical_anchor = MID
p = tf.paragraphs[0]; p.alignment = CENTER; p.line_spacing = 1.05
_run(p, "INDEPENDENT VARIABLE\n", 17, WHITE, bold=True, font=F_HEAD)
_run(p, "the factor being tested or changed\n", 15, "EAF6F8")
_run(p, "(e.g., use of the solar distiller)", 15, AMBER, italic=True)
a = rect(s, 5.75, by + 0.55, 1.6, 0.55, fill=INK, kind=MSO_SHAPE.RIGHT_ARROW)
fill_frame(a, [("affects", 13, WHITE, True)], align=CENTER)
dv = rrect(s, 7.85, by, 4.2, 1.7, fill=SUCCESS, radius=0.1, shadow=True)
tf = dv.text_frame; tf.word_wrap = True; tf.vertical_anchor = MID
p = tf.paragraphs[0]; p.alignment = CENTER; p.line_spacing = 1.05
_run(p, "DEPENDENT VARIABLE\n", 17, WHITE, bold=True, font=F_HEAD)
_run(p, "the outcome being measured\n", 15, "E6F5F2")
_run(p, "(e.g., microbial contamination level)", 15, AMBER, italic=True)
b = rrect(s, 0.85, by + 2.35, SW - 1.7, 0.75, fill=PRIMARY_LT, radius=0.1)
_, tf = textbox(s, 1.2, by + 2.35, SW - 2.4, 0.75, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.0)
_run(p, "A hypothesis predicts how the independent variable affects the dependent variable.", 20, INK_SOFT, bold=True)
notes(s, "Keep this at the level needed only to write a hypothesis \u2014 detailed measurement scales and "
      "operationalization are beyond this lesson. Reconnect to Slide 17's Topic 1/Topic 2 structure: the "
      "independent and dependent variables here are the same two variables the literature review was built "
      "around.\n\nVisual: a variable relationship diagram \u2014 an \"Independent Variable\" box with an arrow "
      "pointing to a \"Dependent Variable\" box.")

# =========================================================================
# SLIDE 32 - Null vs Alternative Hypothesis
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "Null vs. Alternative Hypothesis", 32)
two_column(s, y + 0.05,
    left={"title": "NULL HYPOTHESIS  (H\u2080)", "band": MUTED,
          "items": ["States there is no significant difference or relationship"], "size": 22},
    right={"title": "ALTERNATIVE HYPOTHESIS  (H\u2081)", "band": PRIMARY,
           "items": ["States there is a significant difference or relationship"], "size": 22},
    bottom=y + 1.95)
# Example A box
b = rrect(s, 0.85, y + 2.2, SW - 1.7, 1.75, fill=INK, radius=0.08, shadow=True)
_, tf = textbox(s, 1.25, y + 2.2, SW - 2.5, 1.75, anchor=MID)
p = para(tf, first=True, space_after=6, line_spacing=1.05)
_run(p, "EXAMPLE A", 13, AMBER, bold=True, font=F_HEAD)
p = para(tf, space_after=5, line_spacing=1.05)
_run(p, "H\u2080  ", 20, "9FB8C8", bold=True)
_run(p, "There is no significant difference in contamination levels before and after distillation.", 19, WHITE)
p = para(tf, space_after=0, line_spacing=1.05)
_run(p, "H\u2081  ", 20, AMBER, bold=True)
_run(p, "There is a significant difference.", 19, WHITE)
notes(s, "Define these two terms only \u2014 do not move into how they are statistically tested, since that "
      "belongs to a later methodology lesson. Frame the null and alternative hypothesis as two competing "
      "predictions the eventual data collection will help decide between.\n\nVisual: none additional; the "
      "two-column layout with the paired example is sufficient.")

# =========================================================================
# SLIDE 33 - Writing RQs & Hypotheses for Quantitative/Mixed Studies
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "Writing RQs & Hypotheses for Quantitative / Mixed Studies", 33, title_size=24)
data = [
    ["Question Type", "Sentence Starter", "Best Fit"],
    ["Descriptive", "\u201cWhat is the level / extent of\u2026?\u201d", "Quantitative"],
    ["Comparative", "\u201cIs there a difference between\u2026?\u201d", "Quantitative"],
    ["Relationship", "\u201cIs there a relationship / effect between\u2026?\u201d", "Quantitative"],
    ["Follow-up qualitative", "\u201cHow do participants experience / explain\u2026?\u201d", "Added in mixed methods designs"],
]
cc = {(4, 2): ACCENT_LT}
styled_table(s, 0.85, y + 0.35, SW - 1.7, data, col_widths=[1.0, 1.7, 1.2],
             size=18, header_size=18, row_h=0.76, header_h=0.58, cell_colors=cc)
notes(s, "Explain that in a fully quantitative study, all research questions typically follow the "
      "descriptive, comparative, or relationship formats shown here, each paired with a matching "
      "hypothesis. In a mixed methods study, researchers often keep the quantitative question and "
      "hypothesis as the main driver, then add one qualitative follow-up question to explore why or how "
      "the quantitative result occurred \u2014 this is the practical bridge between the two approaches without "
      "turning today's lesson into a full mixed methods design lecture.\n\nVisual: none additional; the "
      "reference table itself functions as a usable writing tool.")

# =========================================================================
# SLIDE 34 - Example: The Complete Chain
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "Example \u2014 The Complete Chain", 34)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
vchain(s, 2.3, y + 0.55, 8.7, [
    ("Problem Statement:", "limited evidence on whether the distiller improves microbial water safety"),
    ("Research Question:", "Is there a significant difference in microbial contamination before and after distillation?"),
    ("Hypothesis (H\u2081):", "there is a significant difference in contamination levels before and after treatment"),
    ("Mixed methods add-on:", "How do barangay residents perceive the safety of the distilled water?"),
], box_h=0.86, gap=0.26, colors=[INK, PRIMARY, ACCENT, SUCCESS], text_size=16)
notes(s, "Trace the chain top to bottom, showing students that every element they've learned so far "
      "connects \u2014 nothing here was invented from scratch; each line grew directly out of the one above "
      "it. This slide functions as a model answer students can compare their own work against in the "
      "following activity.\n\nVisual: a vertical chain diagram with connecting arrows between each of the "
      "four boxes, visually reinforcing continuity.")

# =========================================================================
# SLIDE 35 - Application: Draft Your Own Chain
# =========================================================================
s = new_slide()
y = header(s, "Section 6 \u00b7 Research Questions and Hypotheses (Competency 14)",
           "Application \u2014 Draft Your Own Chain", 35)
eg_tag(s, 0.85, y - 0.02, "Activity template \u00b7 Example B topic or your own")
template_card(s, 0.85, y + 0.5, SW - 1.7, 4.3, [
    "Problem Statement:", "Research Question:", "Hypothesis (H\u2081):",
    "(Optional mixed methods add-on question):",
], size=23)
notes(s, "Have students complete this individually using either Example B (dengue prediction) or their own "
      "emerging topic, then trade with a partner to check each line against the criteria taught earlier "
      "(researchable problem statement, clear/focused/answerable RQ, testable hypothesis). This is the "
      "lesson's main checkpoint before moving into justification.\n\nVisual: none needed; the template "
      "drives the activity.")

# =========================================================================
# SLIDE 36 - Justifying Why This Problem Matters
# =========================================================================
s = new_slide()
y = header(s, "Section 7 \u00b7 Justifying the Problem with CER (Competency 15)",
           "Justifying Why This Problem Matters", 36, title_size=28)
b1 = rrect(s, 1.4, y + 0.4, SW - 2.8, 0.9, fill=CARD, line=LINE, radius=0.12, shadow=True)
_, tf = textbox(s, 1.75, y + 0.4, SW - 3.4, 0.9, anchor=MID)
p = para(tf, first=True, space_after=0)
_run(p, "A problem statement says ", 22, INK)
_run(p, "what", 22, PRIMARY, bold=True)
_run(p, " you will study", 22, INK)
b2 = rrect(s, 1.4, y + 1.5, SW - 2.8, 0.9, fill=CARD, line=LINE, radius=0.12, shadow=True)
_, tf = textbox(s, 1.75, y + 1.5, SW - 3.4, 0.9, anchor=MID)
p = para(tf, first=True, space_after=0)
_run(p, "A justification explains ", 22, INK)
_run(p, "why it deserves", 22, ACCENT, bold=True)
_run(p, " to be studied", 22, INK)
b3 = rrect(s, 1.4, y + 2.7, SW - 2.8, 1.15, fill=INK, radius=0.1, shadow=True)
_, tf = textbox(s, 1.75, y + 2.7, SW - 3.4, 1.15, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.05)
_run(p, "Tool for building this justification:  the ", 20, WHITE)
_run(p, "Claim \u2013 Evidence \u2013 Reasoning (CER)", 20, AMBER, bold=True)
_run(p, " framework", 20, WHITE)
notes(s, "Frame CER as solving a real writing problem: many students can state a problem but struggle to "
      "argue convincingly for its importance. Preview that CER gives them a repeatable three-part "
      "structure for that argument, built directly from material they already have \u2014 their literature "
      "synthesis.\n\nVisual: none required; a brief framing slide.")

# =========================================================================
# SLIDE 37 - Breaking Down Claim, Evidence, Reasoning
# =========================================================================
s = new_slide()
y = header(s, "Section 7 \u00b7 Justifying the Problem with CER (Competency 15)",
           "Breaking Down Claim, Evidence, Reasoning", 37, title_size=28)
cer = [
    ("Claim", "this problem is worth studying", PRIMARY),
    ("Evidence", "findings and gaps drawn from your literature synthesis", ACCENT),
    ("Reasoning", "the explicit logic connecting the evidence to the claim", SUCCESS),
]
cw = (SW - 1.7 - 2 * 0.4) / 3
for i, (t, d, col) in enumerate(cer):
    px = 0.85 + i * (cw + 0.4)
    card(s, px, y + 0.25, cw, 2.5)
    card_header(s, px, y + 0.25, cw, t.upper(), col, size=19, h=0.65)
    _, tf = textbox(s, px + 0.28, y + 1.05, cw - 0.56, 1.6, anchor=MSO_ANCHOR.TOP)
    p = para(tf, first=True, space_after=0, line_spacing=1.12)
    _run(p, d, 20, INK)
    if i < 2:
        a = rect(s, px + cw - 0.02, y + 1.25, 0.44, 0.4, fill=INK, kind=MSO_SHAPE.RIGHT_ARROW)
b = rrect(s, 0.85, y + 3.05, SW - 1.7, 0.85, fill=PRIMARY_LT, radius=0.1)
_, tf = textbox(s, 1.2, y + 3.05, SW - 2.4, 0.85, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.05)
_run(p, "CER = ", 18, PRIMARY_DK, bold=True)
_run(p, "you assert something, back it with real findings, and explain why those findings support your assertion.", 18, INK_SOFT)
notes(s, "Emphasize that Evidence in a CER paragraph should come straight from the synthesis work done in "
      "Section 3 \u2014 this is not new information, but a repackaging of what students already found. "
      "Reasoning is the part students most often skip; without it, a paragraph is just a claim next to a "
      "citation, with no argument connecting them.\n\nVisual: a three-part concept map with arrows: Claim "
      "\u2192 supported by \u2192 Evidence \u2192 explained by \u2192 Reasoning, looping back to reinforce the Claim.")

# =========================================================================
# SLIDE 38 - Example: A Worked CER Paragraph
# =========================================================================
s = new_slide()
y = header(s, "Section 7 \u00b7 Justifying the Problem with CER (Competency 15)",
           "Example \u2014 A Worked CER Paragraph", 38)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
# legend
lx = 0.85
for t, col in [("Claim", PRIMARY), ("Evidence", ACCENT), ("Reasoning", SUCCESS)]:
    dot = rect(s, lx, y + 0.5, 0.26, 0.26, fill=col, kind=MSO_SHAPE.OVAL)
    _, tf = textbox(s, lx + 0.34, y + 0.44, 1.7, 0.35, anchor=MID)
    p = para(tf, first=True, space_after=0)
    _run(p, t, 15, INK, bold=True, font=F_HEAD)
    lx += 2.0
card(s, 0.85, y + 1.0, SW - 1.7, 3.0, fill="FBFDFE", line=LINE)
_, tf = textbox(s, 1.3, y + 1.25, SW - 2.6, 2.5, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.3)
_run(p, "[Claim] ", 20, PRIMARY, bold=True)
_run(p, "Testing the solar distiller's effect on microbial water safety is a worthwhile research problem. ", 20, INK)
_run(p, "[Evidence] ", 20, ACCENT, bold=True)
_run(p, "Existing studies test distiller efficiency or water safety separately, but rarely evaluate both together in an actual barangay setting. ", 20, INK)
_run(p, "[Reasoning] ", 20, SUCCESS, bold=True)
_run(p, "Because coastal communities are adopting these distillers based on efficiency claims alone, verifying their actual effect on water safety directly addresses a real, practical gap in current knowledge.", 20, INK)
notes(s, "Read the paragraph aloud once as a whole, then a second time pausing to label each bracketed "
      "part. Ask students to notice that this exact paragraph could be dropped directly into the "
      "introduction of a research proposal \u2014 this is a real, usable piece of writing, not just a "
      "classroom exercise.\n\nVisual: colour-code or bracket-label the three sentence parts directly on the "
      "slide so students can visually trace Claim, Evidence, and Reasoning.")

# =========================================================================
# SLIDE 39 - Application: Spot the Claim, Evidence, Reasoning
# =========================================================================
s = new_slide()
y = header(s, "Section 7 \u00b7 Justifying the Problem with CER (Competency 15)",
           "Application \u2014 Spot the Claim, Evidence, Reasoning", 39, title_size=27)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example B topic")
card(s, 0.85, y + 0.55, SW - 1.7, 2.85, fill=CARD, line=PRIMARY)
_, tf = textbox(s, 1.3, y + 0.8, SW - 2.6, 2.35, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.3)
_run(p, "\u201cImproving dengue prediction models is an important research problem. Most existing models rely "
        "only on rainfall and temperature, leaving out human mobility patterns that influence outbreak "
        "spread. Since mobility data is now more accessible through mobile network records, incorporating "
        "it could meaningfully improve prediction accuracy for local health units.\u201d", 20, INK)
instruction_bar(s, 0.85, y + 3.6, SW - 1.7,
                "Individually: label each sentence as Claim, Evidence, or Reasoning \u2014 then compare with a partner.")
notes(s, "Have students individually label each sentence as Claim, Evidence, or Reasoning, then compare "
      "with a partner before a whole-class check. Use any disagreement as a teaching moment \u2014 reasoning "
      "sentences are often the ones students misidentify as evidence, since both sentences discuss the "
      "same topic.\n\nVisual: none additional; students annotate directly on a printed or digital copy of "
      "the paragraph.")

# =========================================================================
# SLIDE 40 - Assumptions vs Limitations
# =========================================================================
s = new_slide()
y = header(s, "Section 8 \u00b7 Assumptions and Limitations (Competency 16)",
           "Assumptions vs. Limitations", 40)
two_column(s, y + 0.1,
    left={"title": "ASSUMPTIONS", "band": PRIMARY, "head_size": 19,
          "items": [
              "Things you take as true / given, without directly testing them",
              [("Example: ", True, False, PRIMARY), ("participants will answer survey questions honestly", False, True)],
          ], "size": 21, "gap": 12},
    right={"title": "LIMITATIONS", "band": ACCENT, "head_size": 19,
           "items": [
               "Constraints or weaknesses in the study's design or scope",
               [("Example: ", True, False, ACCENT), ("the study only covers one barangay, so results may not generalize", False, True)],
           ], "size": 21, "gap": 12},
    bottom=y + 3.7)
notes(s, "Explain the core distinction simply: assumptions are things you trust to be true because "
      "testing them isn't practical, while limitations are things you openly admit might weaken your "
      "conclusions. Both are a normal, expected part of any real study \u2014 including this framing prevents "
      "students from feeling like naming a limitation is confessing to a flawed project.\n\nVisual: none "
      "additional; the two-column table carries the concept clearly.")

# =========================================================================
# SLIDE 41 - Why Naming Limitations Builds Credibility
# =========================================================================
s = new_slide()
y = header(s, "Section 8 \u00b7 Assumptions and Limitations (Competency 16)",
           "Why Naming Limitations Builds Credibility", 41, title_size=28)
# before / after
bw = (SW - 1.7 - 0.5) / 2
card(s, 0.85, y + 0.3, bw, 2.0)
card_header(s, 0.85, y + 0.3, bw, "HIDES ITS LIMITATIONS", DANGER, size=17, icon="\u2715")
_, tf = textbox(s, 1.15, y + 1.1, bw - 0.6, 1.15, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.12)
_run(p, "Looks either naive or dishonest to a careful reader", 21, INK)
card(s, 0.85 + bw + 0.5, y + 0.3, bw, 2.0)
card_header(s, 0.85 + bw + 0.5, y + 0.3, bw, "NAMES ITS LIMITATIONS", SUCCESS, size=17, icon="\u2713")
_, tf = textbox(s, 0.85 + bw + 0.8, y + 1.1, bw - 0.6, 1.15, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.12)
_run(p, "Shows the researcher understands the boundaries of their own claims", 21, INK)
b = rrect(s, 0.85, y + 2.7, SW - 1.7, 1.0, fill=INK, radius=0.1, shadow=True)
_, tf = textbox(s, 1.2, y + 2.7, SW - 2.4, 1.0, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.05)
_run(p, "Limitations do not weaken a study \u2014 ", 22, WHITE, bold=True)
_run(p, "hiding them does.", 22, AMBER, bold=True)
notes(s, "Reinforce this with a quick example: if a study only samples one school but claims its findings "
      "apply to \"all Filipino students,\" a reader will distrust the whole study; naming that limitation "
      "instead protects the researcher's credibility and shows scientific maturity.\n\nVisual: none "
      "required; a short reflective framing slide.")

# =========================================================================
# SLIDE 42 - Example: Assumptions & Limitations for a Real Study
# =========================================================================
s = new_slide()
y = header(s, "Section 8 \u00b7 Assumptions and Limitations (Competency 16)",
           "Example \u2014 Assumptions & Limitations for a Real Study", 42, title_size=26)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
two_column(s, y + 0.5,
    left={"title": "ASSUMPTIONS", "band": PRIMARY, "head_size": 19,
          "items": [
              "the water samples collected are representative of the barangay's typical water source",
              "the testing equipment used gives accurate microbial readings",
          ], "size": 21, "gap": 12},
    right={"title": "LIMITATIONS", "band": ACCENT, "head_size": 19,
           "items": [
               "the study covers only one barangay over a short testing period, so results may not apply to other coastal communities or seasons",
           ], "size": 21, "gap": 12},
    bottom=y + 4.0)
notes(s, "Point out how directly these lines connect to the study's actual design choices \u2014 assumptions "
      "and limitations are not generic disclaimers, they are specific to what this particular study did "
      "and did not do. Ask students what would happen to the assumptions list if the researcher instead "
      "tested the equipment's accuracy directly \u2014 it would move from \"assumption\" to \"verified fact,\" a "
      "subtle but important shift.\n\nVisual: none additional; the two labeled lists are sufficient.")

# =========================================================================
# SLIDE 43 - Application: Identify Assumptions and Limitations
# =========================================================================
s = new_slide()
y = header(s, "Section 8 \u00b7 Assumptions and Limitations (Competency 16)",
           "Application \u2014 Identify Assumptions and Limitations", 43, title_size=26)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example B topic")
b = rrect(s, 0.85, y + 0.55, SW - 1.7, 1.15, fill=INK, radius=0.1, shadow=True)
_, tf = textbox(s, 1.2, y + 0.55, SW - 2.4, 1.15, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.1)
_run(p, "SCENARIO   ", 14, AMBER, bold=True, font=F_HEAD)
_run(p, "A study uses one year of rainfall, temperature, and mobile network mobility data from a "
        "single city to test a new dengue prediction model.", 20, WHITE)
bw = (SW - 1.7 - 0.5) / 2
for title, col, bx in [("List \u2265 2 Assumptions", PRIMARY, 0.85),
                        ("List \u2265 2 Limitations", ACCENT, 0.85 + bw + 0.5)]:
    card(s, bx, y + 1.95, bw, 2.15)
    card_header(s, bx, y + 1.95, bw, title, col, size=17)
    for k in range(2):
        rl = rrect(s, bx + 0.35, y + 2.9 + k * 0.55, bw - 0.7, 0.045, fill=LINE, radius=0.5)
instruction_bar(s, 0.85, y + 4.25, SW - 1.7,
                "In pairs: don't confuse a limitation (only one city) with an assumption (mobility data reflects real movement).")
notes(s, "Circulate as students work in pairs; a common early mistake is confusing a limitation (\"only "
      "one city was studied\") with an assumption (\"mobility data accurately reflects real movement "
      "patterns\") \u2014 use this as a chance to reinforce the distinction from Slide 40 one more time before "
      "wrapping up.\n\nVisual: none required; discussion-based activity.")

# =========================================================================
# SLIDE 44 - The Complete Research Reasoning Chain (recap)
# =========================================================================
s = new_slide()
background(s, INK)
rect(s, -1.5, -1.5, 4.5, 4.5, fill=INK_SOFT, kind=MSO_SHAPE.OVAL)
rrect(s, 0.85, 0.6, 0.14, 0.9, fill=ACCENT, radius=0.5)
_, tf = textbox(s, 1.15, 0.55, 11.0, 0.35)
p = para(tf, first=True, space_after=0)
_run(p, "CLOSING", 13, PRIMARY_LT, bold=True, font=F_HEAD)
_, tf = textbox(s, 1.12, 0.9, 11.4, 0.7)
p = para(tf, first=True, space_after=0)
_run(p, "The Complete Research Reasoning Chain", 30, WHITE, bold=True, font=F_TITLE)
stages = ["Sources", "Synthesis", "Gap", "Literature Review",
          "Problem Statement", "Research Question / Hypothesis",
          "CER Justification", "Assumptions & Limitations"]
cols = [PRIMARY, PRIMARY, PRIMARY_DK, PRIMARY_DK, ACCENT, ACCENT, SUCCESS, AMBER]
# two rows of 4, snake
rowy = [2.15, 4.35]
bw2 = 2.7
gapx = 0.42
startx = 0.85
positions = []
# row 1 left->right
for i in range(4):
    positions.append((startx + i * (bw2 + gapx), rowy[0]))
# row 2 left->right (reading order)
for i in range(4):
    positions.append((startx + i * (bw2 + gapx), rowy[1]))
for i, (st, (px, py)) in enumerate(zip(stages, positions)):
    b = rrect(s, px, py, bw2, 1.25, fill=cols[i], radius=0.12, shadow=True)
    tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = MID
    p = tf.paragraphs[0]; p.alignment = CENTER; p.line_spacing = 1.0
    _run(p, str(i + 1) + "\n", 13, "D9EEF2", bold=True)
    _run(p, st, 15.5, WHITE, bold=True, font=F_HEAD)
    # arrows within row
    if i in (0, 1, 2, 4, 5, 6):
        right_arrow(s, px + bw2 + 0.02, py + 0.62, color=PRIMARY_LT, w=0.38, h=0.34)
# connector from row1 end to row2 start
connector(s, positions[3][0] + bw2 / 2, rowy[0] + 1.25,
          positions[4][0] + bw2 / 2, rowy[1], color=ACCENT, w=2.5)
_, tf = textbox(s, 0.85, 5.95, SW - 1.7, 0.9, anchor=MSO_ANCHOR.TOP)
p = para(tf, first=True, space_after=0, align=CENTER, line_spacing=1.1)
_run(p, "One continuous argument \u2014 every stage feeds directly into the next.", 18, PRIMARY_LT, italic=True)
footer(s, 44)
notes(s, "Close by tracing the full chain from top to bottom once more, reminding students that every "
      "stage they practiced today feeds directly into the next \u2014 this is not a checklist of separate "
      "skills but one continuous argument. Briefly note that the limitations they just identified will "
      "later shape decisions about how they actually collect and analyze data, without going into that "
      "process now.\n\nVisual: the same research process flowchart from Slide 3, now with every stage "
      "fully labeled and briefly annotated \u2014 a single reference image summarising the entire lesson.")

# --------------------------------------------------------------- save
import os
out = os.path.join(os.path.dirname(__file__), "..",
                   "Lecture3-Review-of-Literature.pptx")
out = os.path.abspath(out)
prs.save(out)
print("Saved:", out, "slides:", len(prs.slides._sldIdLst))
