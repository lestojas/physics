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
# SLIDE 23 - The Four Components of a Problem Statement
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "The Four Components of a Problem Statement", 23, title_size=27)
_, tf = textbox(s, 0.85, y - 0.05, SW - 1.7, 0.32)
p = para(tf, first=True, space_after=0)
_run(p, "A strong statement needs at least one full sentence per component.", 14, MUTED, italic=True)
data = [
    ["Component", "Purpose", "Key Question It Answers"],
    ["Background context", "Establishes the broader setting in which the problem exists",
     "What does the reader need to know to understand why this matters?"],
    ["Specific problem or gap", "Names the precise issue, contradiction, or knowledge gap the study addresses",
     "What exactly is wrong, missing, or unresolved?"],
    ["Implications", "Explains the consequences of leaving the problem unresolved",
     "Who is affected, and what are the costs of inaction?"],
    ["Objectives or aims", "States what the study will do in response to the gap",
     "What will this research investigate or accomplish?"],
]
cc = {(1, 0): PRIMARY_LT, (2, 0): ACCENT_LT, (3, 0): AMBER_LT, (4, 0): SUCCESS_LT}
styled_table(s, 0.85, y + 0.38, SW - 1.7, data, col_widths=[1.0, 1.5, 1.55],
             size=15, header_size=16, row_h=0.9, header_h=0.55, cell_colors=cc)
notes(s, "Present this as the universal four-part anatomy of a problem statement \u2014 every effective "
      "research problem statement contains these four components in some form, regardless of field or "
      "format. Tell students a strong problem statement needs at least one full sentence per component "
      "\u2014 skipping any one of the four leaves the reader with an unanswered question: why does this "
      "setting matter (context)? what exactly is missing (gap)? who is affected if nothing changes "
      "(implications)? and what will this study actually do (objectives)? Note that these four components "
      "do the same job as a general \"why this study matters\" explanation, just broken into finer, "
      "checkable parts.\n\nVisual: a four-row reference table matching this exact structure, formatted so "
      "students can reuse it directly as a drafting template when writing their own problem statement.")

# =========================================================================
# SLIDE 24 - Example: One Sentence per Component
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "Example \u2014 One Sentence per Component", 24, title_size=27)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Example A topic")
x0 = 0.85
cw = (SW - 1.7 - 0.5) / 2
top = y + 0.5
bottom = 6.72
h = bottom - top
comp_colors = [PRIMARY, ACCENT, "C0870A", SUCCESS]
labels = ["Background context:", "Specific problem or gap:", "Implications:", "Objectives or aims:"]
sentences = [
    "Many coastal barangays in the Philippines depend on shallow wells and rainwater catchments that are vulnerable to microbial contamination, and low-cost solar water distillers have been promoted as an accessible treatment option.",
    "However, existing studies evaluate either the distiller's efficiency or general water safety standards separately, with very few directly measuring the distiller's actual effect on microbial contamination in a real barangay setting.",
    "Without this evidence, communities and local health workers risk relying on a technology whose real protective effect on drinking water safety remains unverified, which could expose residents to preventable waterborne illness.",
    "This study, therefore, aims to determine the effect of a low-cost solar water distiller on the microbial safety of drinking water in a coastal barangay in Zambales.",
]
# LEFT card - the scaffold, one sentence per component
card(s, x0, top, cw, h)
card_header(s, x0, top, cw, "BUILD: ONE SENTENCE PER COMPONENT", INK, size=14.5)
_, tf = textbox(s, x0 + 0.28, top + 0.72, cw - 0.56, h - 0.85)
first = True
for lab, sent, col in zip(labels, sentences, comp_colors):
    p = para(tf, first=first, space_after=5, line_spacing=1.03)
    first = False
    _run(p, lab + " ", 13, col, bold=True, font=F_HEAD)
    _run(p, sent, 13, INK)
# RIGHT card - the finished, submission-ready paragraph
card(s, x0 + cw + 0.5, top, cw, h, fill="FBFDFE", line=SUCCESS)
card_header(s, x0 + cw + 0.5, top, cw, "FINISHED PROBLEM STATEMENT", SUCCESS, size=14.5)
_, tf = textbox(s, x0 + cw + 0.78, top + 0.72, cw - 0.56, h - 0.85)
p = para(tf, first=True, space_after=6, line_spacing=1.16)
_run(p, "\u201c" + " ".join(sentences) + "\u201d", 13, INK, italic=True)
p = para(tf, space_after=0, line_spacing=1.0)
_run(p, "The four components read as one natural paragraph \u2014 a drafting scaffold, not labeled boxes.",
     11.5, MUTED, italic=True)
notes(s, "Build this slide sentence by sentence, revealing one component at a time, so students see the "
      "paragraph accumulate piece by piece rather than appearing all at once as a finished product. Point "
      "out that the finished paragraph reads as one natural piece of academic writing \u2014 the four "
      "components are a drafting scaffold, not four visibly separate boxes that must remain labeled in the "
      "final write-up. Note how directly the Specific Problem/Gap sentence traces back to the Topic "
      "3/Summary gap identified back in Slide 18, and how the Objectives sentence will resurface almost "
      "unchanged as the general research question in the next section.\n\nVisual: reveal the four labeled "
      "sentences in sequence (build animation), then highlight the final combined paragraph in a bordered "
      "box to show the finished, submission-ready product.")

# =========================================================================
# SLIDE 25 - Common Pitfalls in Problem Statements
# =========================================================================
s = new_slide()
y = header(s, "Section 5 \u00b7 Formulating the Problem Statement (Competency 13)",
           "Common Pitfalls in Problem Statements", 25, title_size=28)
data = [
    ["Pitfall", "Missing Component", "Fix"],
    ["Too broad: \u201cWater pollution is a big problem.\u201d", "Specific problem or gap",
     "Narrow to a specific variable, population, or setting"],
    ["Too vague: \u201cSomething should be done about dengue.\u201d", "Objectives or aims",
     "State exactly what the study will investigate or accomplish"],
    ["Merely descriptive: \u201cMany barangays use rainwater.\u201d", "Implications",
     "Add why this is an unresolved issue worth studying"],
    ["Unanswerable: \u201cIs clean water important?\u201d", "Specific problem or gap",
     "Rephrase around something investigable with data"],
]
cc = {(1, 1): DANGER_LT, (2, 1): DANGER_LT, (3, 1): DANGER_LT, (4, 1): DANGER_LT}
styled_table(s, 0.85, y + 0.25, SW - 1.7, data, col_widths=[1.35, 0.95, 1.35],
             size=15.5, header_size=17, row_h=0.9, header_h=0.58,
             header_fill=DANGER, cell_colors=cc)
notes(s, "Go through each pitfall using a \"spot what's wrong\" approach before revealing the fix \u2014 this "
      "keeps students actively diagnosing rather than passively reading. Reframe each pitfall as a missing "
      "component from Slide 23's four-part structure \u2014 editing becomes a checklist task (\"which of the "
      "four parts is absent?\") instead of a vague stylistic judgment.\n\nVisual: none additional; the "
      "table's three-column structure is sufficient.")

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
                "In pairs: name the missing component, then rewrite with one sentence per component (Slide 24).")
notes(s, "Have students work in pairs to name which of the four components (Background Context, Specific "
      "Problem/Gap, Implications, Objectives/Aims) is missing from each statement, then rewrite it by "
      "adding at least one sentence for every component, following the model on Slide 24. Circulate and "
      "watch for a common second-round mistake: students patch one missing component but leave another "
      "one still absent.\n\nVisual: none required; this is a peer-editing activity.")

# =========================================================================
# SECTION 6 (Part III) - RESEARCH QUESTIONS AND HYPOTHESES (Competency 14)
# =========================================================================
EB6 = "Section 6 \u00b7 Research Questions & Hypotheses (Competency 14)"
EB7 = "Section 7 \u00b7 Justifying the Problem with CER (Competency 15)"
EB8 = "Section 8 \u00b7 Assumptions & Limitations (Competency 16)"


def roadmap(slide, y, active=-1, done=None):
    done = done or set()
    stages = ["Research Problem", "Research Questions & Hypotheses",
              "Justifying the Problem (CER)", "Assumptions & Limitations"]
    x = 0.85
    bw = 2.5
    gap = 0.55
    h = 0.95
    for i, st in enumerate(stages):
        if i in done:
            col = SUCCESS
        elif i == active:
            col = ACCENT
        else:
            col = PRIMARY
        b = rrect(slide, x, y, bw, h, fill=col, radius=0.16, shadow=True)
        tf = b.text_frame
        tf.word_wrap = True
        tf.vertical_anchor = MID
        tf.margin_left = Pt(7)
        tf.margin_right = Pt(7)
        p = tf.paragraphs[0]
        p.alignment = CENTER
        p.line_spacing = 1.0
        _run(p, ("\u2713 " if i in done else "") + st, 13, WHITE, bold=True, font=F_HEAD)
        if i < 3:
            right_arrow(slide, x + bw + 0.04, y + h / 2, color=INK, w=0.46, h=0.3)
        x += bw + gap


def scenario_card(slide, x, y, w, h, text, size=18, fill=INK, tcolor=WHITE, label=None):
    c = rrect(slide, x, y, w, h, fill=fill, radius=0.08, shadow=True)
    rrect(slide, x + 0.0, y, 0.13, h, fill=ACCENT, radius=0.0)
    _, tf = textbox(slide, x + 0.42, y + 0.18, w - 0.7, h - 0.36, anchor=MID)
    first = True
    if label:
        p = para(tf, first=True, space_after=6)
        _run(p, label, 13, AMBER, bold=True, font=F_HEAD)
        first = False
    p = para(tf, first=first, space_after=0, line_spacing=1.16)
    _run(p, text, size, tcolor, italic=True)
    return c


# ---- Slide 27 (Part III / 1) Today's Journey ---------------------------
s = new_slide()
y = header(s, EB6, "Today's Journey \u2014 Problem to Proof", 27, title_size=30)
roadmap(s, y + 0.12, active=1)
bullets(s, 0.9, y + 1.45, SW - 1.9, [
    [("Today we complete the ", False), ("backbone of Chapter 1", True, False, PRIMARY),
     (" of your research paper.", False)],
    [("You already have a research ", False), ("problem", True, False, ACCENT),
     (". Today you learn to (1) turn it into answerable questions, (2) defend why it matters, "
      "and (3) be honest about what your study can and cannot claim.", False)],
], size=24, gap=14)
notes(s, "Open by reminding students that a research problem alone is not researchable \u2014 it is too "
      "broad to investigate directly. Emphasize that everything covered today builds directly toward the "
      "manuscript sections they will eventually defend orally, so today's skills are rehearsal for their "
      "research defense, not just requirements to fulfill. Preview that by the end of the lecture, they "
      "will have drafted their own research questions, a CER-based justification paragraph, and a first "
      "attempt at their study's assumptions and limitations.\n\nVisual: a three-node flowchart spanning "
      "the top of the slide, used as a recurring \"you are here\" tracker on later section-divider slides.")

# ---- Slide 28 (Part III / 2) A Reef in Trouble ------------------------
s = new_slide()
y = header(s, EB6, "A Reef in Trouble \u2014 Setting the Scene", 28, title_size=30)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Davao Gulf coral reef")
scenario_card(s, 0.85, y + 0.45, SW - 1.7, 2.35,
              "A marine biology student in Davao City notices that coral cover near the Pujada Bay area "
              "of the Davao Gulf has visibly declined over the past decade. Fisherfolk report smaller "
              "catches. News articles mention \u201ccoral bleaching\u201d and \u201csedimentation from coastal "
              "development.\u201d She wants to study this \u2014 but where does she even start asking questions?",
              size=18, label="THE SCENARIO")
bullets(s, 0.9, y + 3.05, SW - 1.9, [
    [("This is a ", False), ("research problem", True, False, ACCENT),
     (": real, broad, and not yet answerable through investigation.", False)],
    [("Instructor-Created Example", True, False, PRIMARY),
     (" (grounded in publicly documented Davao Gulf coral reef conditions).", False)],
], size=21, gap=8)
# two anchor chips
for i, (lab, col) in enumerate([("Coral reef \u2014 nursery habitat", PRIMARY),
                                ("Fisherfolk \u2014 livelihood at stake", SUCCESS)]):
    cx = 0.9 + i * 6.0
    chip = rrect(s, cx, y + 4.35, 5.6, 0.55, fill=col, radius=0.2)
    fill_frame(chip, [(lab, 15, WHITE, True)], align=CENTER)
notes(s, "Use this scenario as the anchor for the entire Research Questions section. Ask students: \"If "
      "she wrote her whole thesis around 'coral reefs are declining,' could she ever finish?\" Guide them "
      "to see that a problem this size cannot be investigated as-is \u2014 it must be broken into smaller, "
      "focused, answerable pieces. This felt difficulty is exactly why research questions exist.\n\n"
      "Visual: a stylized map of Davao Gulf with a marker on the coastal study site, paired with two "
      "small icons \u2014 a coral reef and a fishing boat \u2014 to visually anchor the scenario.")

# ---- Slide 29 (Part III / 3) Why a Problem Alone Is Not Enough --------
s = new_slide()
y = header(s, EB6, "Why a Problem Alone Is Not Enough", 29, title_size=30)
data = [
    ["Research Problem (broad)", "Research Question (focused)"],
    ["\u201cCoral reefs in Davao Gulf are declining.\u201d",
     "\u201cWhat is the percentage of live coral cover at three reef sites in Davao Gulf?\u201d"],
    ["\u201cFarmers are struggling with pests.\u201d",
     "\u201cWhat is the level of pesticide resistance among fall armyworm populations in a selected "
     "corn-growing municipality?\u201d"],
]
cc = {(1, 0): AMBER_LT, (2, 0): AMBER_LT, (1, 1): SUCCESS_LT, (2, 1): SUCCESS_LT}
styled_table(s, 0.85, y + 0.2, SW - 1.7, data, col_widths=[1, 1.15],
             size=17, header_size=18, row_h=1.15, header_h=0.6, header_fill=INK, cell_colors=cc)
bullets(s, 0.9, y + 3.35, SW - 1.9, [
    [("A ", False), ("research question ", True, False, PRIMARY), ("narrows", False, True),
     (" the problem into something specific, focused, and answerable through data collection.", False)],
    [("This is the first job of Competency 14: narrowing a problem statement into one or more research "
      "questions.", False)],
], size=20, gap=7)
notes(s, "This slide operationalizes Creswell's core idea that research questions and hypotheses are the "
      "next signposts after the purpose statement \u2014 they translate the study's broad intent into "
      "precise, investigable questions. Point out that both example problems above were the size of a "
      "whole news headline, while both example questions could realistically be answered using a specific "
      "data-collection method (water quality testing, insect sampling) within a school year.")

# ---- Slide 30 (Part III / 4) Application: Narrow Your Own Problem -----
s = new_slide()
y = header(s, EB6, "Application \u2014 Narrow Your Own Problem", 30, title_size=30)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity \u00b7 Think\u2013Pair\u2013Share")
scenario_card(s, 0.85, y + 0.5, SW - 1.7, 1.15,
              "Post-harvest losses among small rice farmers in Mindanao are high.",
              size=22, fill=INK, label="GIVEN BROAD PROBLEM")
bullets(s, 0.9, y + 1.95, SW - 1.9, [
    [("In pairs, narrow this into ", False), ("one specific, focused research question", True, False, PRIMARY),
     (".", False)],
    [("Test it against this checklist: Is it ", False), ("clear", False, True),
     ("? Is it ", False), ("specific", False, True),
     ("? Can it be ", False), ("answered through investigation", False, True), (" (not opinion)?", False)],
], size=23, gap=12)
instruction_bar(s, 0.85, y + 3.95, SW - 1.7,
                "3\u20134 minutes, then two or three pairs share out.", color=AMBER)
notes(s, "Give students 3\u20134 minutes, then cold-call two or three pairs. A strong answer might resemble: "
      "\"What is the percentage of post-harvest rice loss attributable to inadequate drying facilities in "
      "[municipality]?\" A weak answer to watch for: \"Why do farmers lose their harvest?\" \u2014 flag this "
      "now as an example of a question that is too broad and too causal-sounding, and tell students you "
      "will return to why \"why\" questions behave differently in Part IV.")

# ---- Slide 31 (Part III / 5) Three Qualities of a Good RQ -------------
s = new_slide()
y = header(s, EB6, "Three Qualities of a Good Research Question", 31, title_size=29)
triad = [
    ("C", "Clear", "anyone reading it understands exactly what is being asked, without further explanation", PRIMARY),
    ("F", "Focused", "narrow enough to be thoroughly answered within your study's timeframe and resources", ACCENT),
    ("A", "Answerable", "resolved through data (measurement, observation, interview), not through opinion or debate", SUCCESS),
]
cw = (SW - 1.7 - 2 * 0.45) / 3
for i, (icon, t, d, col) in enumerate(triad):
    px = 0.85 + i * (cw + 0.45)
    card(s, px, y + 0.3, cw, 3.15)
    circ = rect(s, px + cw / 2 - 0.55, y + 0.65, 1.1, 1.1, fill=col, kind=MSO_SHAPE.OVAL, shadow=True)
    fill_frame(circ, [(icon, 34, WHITE, True)], align=CENTER)
    _, tf = textbox(s, px + 0.2, y + 1.9, cw - 0.4, 0.45)
    p = para(tf, first=True, align=CENTER, space_after=4)
    _run(p, t, 23, INK, bold=True, font=F_HEAD)
    _, tf = textbox(s, px + 0.3, y + 2.4, cw - 0.6, 1.0, anchor=MSO_ANCHOR.TOP)
    p = para(tf, first=True, align=CENTER, space_after=0, line_spacing=1.08)
    _run(p, d, 16, MUTED)
notes(s, "These three qualities exist because a research question performs a very specific job: it must "
      "guide what data you will collect. If a question fails any one of the three tests, a student will "
      "not know what to measure, survey, or observe. Model quickly rejecting a question like \"Is climate "
      "change bad for coral reefs?\" \u2014 it fails \"answerable through investigation\" because \"bad\" is a "
      "value judgment, not a measurable variable.\n\nVisual: a checklist icon set (checkmark/clock/"
      "magnifying-glass) matched to each quality, reusable later as a rubric graphic.")

# ---- Slide 32 (Part III / 6) Application: Diagnose the RQ ------------
s = new_slide()
y = header(s, EB6, "Application \u2014 Diagnose the Research Question", 32, title_size=29)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity")
data = [
    ["Question", "Verdict"],
    ["\u201cWhat is the coral bleaching severity index of three reef sites in Davao Gulf during the dry season?\u201d", "discuss"],
    ["\u201cAre corals important?\u201d", "discuss"],
    ["\u201cWhat is the relationship between soil nitrogen levels and corn yield in a selected Davao del Norte farm?\u201d", "discuss"],
]
cc = {(1, 1): AMBER_LT, (2, 1): AMBER_LT, (3, 1): AMBER_LT}
styled_table(s, 0.85, y + 0.5, SW - 1.7, data, col_widths=[2.6, 0.7],
             size=17, header_size=17, row_h=0.9, header_h=0.55, cell_colors=cc)
instruction_bar(s, 0.85, y + 3.85, SW - 1.7,
                "Sort each as \u2713 Strong or \u2717 Needs Revision \u2014 and say why.")
notes(s, "Walk through each row as a class. The first and third are strong \u2014 specific, measurable, and "
      "clearly scoped to a site/timeframe. The second fails on all three qualities: it is vague, "
      "unbounded, and answerable by simple opinion. Use this to reinforce the diagnostic habit before "
      "moving into hypotheses.")

# ---- Slide 33 (Part III / 7) When Does a Study Need a Hypothesis? ----
s = new_slide()
y = header(s, EB6, "When Does a Study Need a Hypothesis?", 33, title_size=30)
top = rrect(s, SW / 2 - 3.6, y + 0.1, 7.2, 0.95, fill=INK, radius=0.1, shadow=True)
_, tf = textbox(s, SW / 2 - 3.4, y + 0.1, 6.8, 0.95, anchor=MID)
p = para(tf, first=True, space_after=0, align=CENTER, line_spacing=1.05)
_run(p, "Does your study test a ", 16, WHITE)
_run(p, "predicted relationship or difference", 16, AMBER, bold=True)
_run(p, " between variables using statistics?", 16, WHITE)
# branches
by = y + 1.7
lx, rx = 2.1, 8.0
bw = 3.2
connector(s, SW / 2 - 1.5, y + 1.05, lx + bw / 2, by, color=PRIMARY, w=2.5)
connector(s, SW / 2 + 1.5, y + 1.05, rx + bw / 2, by, color=ACCENT, w=2.5)
lbl = rect(s, SW / 2 - 2.7, y + 1.18, 0.7, 0.42, fill=PRIMARY, kind=MSO_SHAPE.OVAL)
fill_frame(lbl, [("YES", 12, WHITE, True)], align=CENTER)
lbl = rect(s, SW / 2 + 2.0, y + 1.18, 0.7, 0.42, fill=ACCENT, kind=MSO_SHAPE.OVAL)
fill_frame(lbl, [("NO", 12, WHITE, True)], align=CENTER)
for lab, sub, col, bx in [("Quantitative study", "Write a HYPOTHESIS", PRIMARY, lx),
                          ("Qualitative study", "Use RESEARCH QUESTIONS only (no hypothesis)", ACCENT, rx)]:
    c1 = rrect(s, bx, by, bw, 0.62, fill=col, radius=0.14, shadow=True)
    fill_frame(c1, [(lab, 16, WHITE, True)], align=CENTER)
    down_arrow(s, bx + bw / 2, by + 0.68, color=INK, h=0.24)
    c2 = rrect(s, bx, by + 0.98, bw, 0.8, fill=CARD, line=col, radius=0.12, shadow=True)
    fill_frame(c2, [(sub, 15.5, INK, True)], align=CENTER)
bullets(s, 0.9, y + 3.75, SW - 1.9, [
    [("A ", False), ("hypothesis", True, True, PRIMARY),
     (" is a researcher's predicted answer to a research question, later tested with statistics.", False)],
    [("Qualitative", True, True, ACCENT),
     (" research uses questions only \u2014 the researcher deliberately avoids predicting a direction, "
      "since the goal is to explore meaning, not test a prediction.", False)],
], size=18, gap=6)
notes(s, "This is the conceptual heart of today's first major idea. Many students think \"hypothesis\" is "
      "a mandatory part of every research paper \u2014 correct this directly. If a student's coral reef study "
      "is quantitative (\"What is the relationship between sedimentation levels and live coral cover "
      "percentage?\"), it needs a hypothesis. If a classmate is doing a qualitative study (\"What are the "
      "lived experiences of small-scale fisherfolk adapting to declining coral reef health in Davao "
      "Gulf?\"), no hypothesis is needed or appropriate \u2014 only a central question and sub-questions.\n\n"
      "Visual: the decision-tree flowchart, colored to separate the quantitative and qualitative "
      "branches \u2014 reusable as a quick-reference poster.")

# ---- Slide 34 (Part III / 8) Application: Hypothesis or Not? ---------
s = new_slide()
y = header(s, EB6, "Application \u2014 Hypothesis or Not?", 34, title_size=30)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity")
data = [
    ["Study Description", "Needs a Hypothesis?"],
    ["Comparing average water turbidity between two reef sites using measured data", "\u2713  /  \u2717"],
    ["Exploring how fisherfolk describe changes in their livelihood over 10 years through interviews", "\u2713  /  \u2717"],
    ["Testing whether a new organic fertilizer increases mung bean yield compared to a control group", "\u2713  /  \u2717"],
]
cc = {(1, 1): PRIMARY_LT, (2, 1): PRIMARY_LT, (3, 1): PRIMARY_LT}
styled_table(s, 0.85, y + 0.5, SW - 1.7, data, col_widths=[2.4, 0.9],
             size=17, header_size=17, row_h=0.85, header_h=0.55, cell_colors=cc)
instruction_bar(s, 0.85, y + 3.75, SW - 1.7,
                "Scan for comparison / relationship words (\u201ccompare, relationship, effect, increase\u201d).")
notes(s, "Row 1 and Row 3 are quantitative comparisons \u2014 both need hypotheses. Row 2 is qualitative and "
      "exploratory \u2014 no hypothesis, only a central question and sub-questions. Use this to cement the "
      "pattern-recognition skill: students should learn to scan a study description for "
      "comparison/relationship language (\"compare,\" \"relationship,\" \"effect,\" \"increase\") as the "
      "signal that a hypothesis is expected.")

# ---- Slide 35 (Part III / 9) How Many Questions Should You Have? -----
s = new_slide()
y = header(s, EB6, "How Many Questions Should You Have?", 35, title_size=30)
data = [
    ["Research Type", "Structure", "Typical Count"],
    ["Quantitative (SOP format)", "1 general objective + several specific sub-questions",
     "At least 3 specific sub-questions, each tied to a measurable variable"],
    ["Qualitative", "1\u20132 central questions + narrower sub-questions",
     "5\u20137 sub-questions per central question (Creswell; capped near a dozen total per Miles & Huberman)"],
    ["Mixed Methods", "Separate quantitative + qualitative questions, plus one question about integrating both datasets",
     "1 quantitative set + 1 qualitative set + 1 mixed methods question"],
]
cc = {(1, 0): PRIMARY_LT, (2, 0): ACCENT_LT, (3, 0): SUCCESS_LT}
styled_table(s, 0.85, y + 0.2, SW - 1.7, data, col_widths=[0.9, 1.6, 1.5],
             size=15.5, header_size=16, row_h=1.15, header_h=0.55, cell_colors=cc)
notes(s, "This slide directly answers a question students almost always ask: \"How many research "
      "questions do I need?\" For quantitative SHS papers, the Philippine convention (seen in Practical "
      "Research 2) is a Statement of the Problem (SOP): one general objective, followed by at least three "
      "specific objectives, each pointing to a variable the study will measure. For qualitative work, "
      "Creswell recommends one or two broad central questions broken into five to seven sub-questions \u2014 "
      "enough to guide an interview without overwhelming the participant or the researcher. Stress that "
      "these are conventions, not rigid laws, but departing from them without reason will raise questions "
      "during a defense panel.")

# ---- Slide 36 (Part III / 10) Worked Example SOP (Coral Reef) --------
s = new_slide()
y = header(s, EB6, "Worked Example \u2014 A Full SOP (Coral Reef)", 36, title_size=29)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example \u00b7 Philippine SHS SOP format")
go = rrect(s, 0.85, y + 0.5, SW - 1.7, 1.15, fill=INK, radius=0.08, shadow=True)
_, tf = textbox(s, 1.2, y + 0.5, SW - 2.4, 1.15, anchor=MID)
p = para(tf, first=True, space_after=4, line_spacing=1.02)
_run(p, "GENERAL OBJECTIVE", 13, AMBER, bold=True, font=F_HEAD)
p = para(tf, space_after=0, line_spacing=1.08)
_run(p, "This study aims to assess the ", 17, WHITE)
_run(p, "coral reef health", 17, "9FE3D6", bold=True)
_run(p, " and its relationship to ", 17, WHITE)
_run(p, "coastal sedimentation levels", 17, "9FE3D6", bold=True)
_run(p, " in a selected barangay along Davao Gulf.", 17, WHITE)
_, tf = textbox(s, 0.9, y + 1.85, SW - 1.9, 0.35)
p = para(tf, first=True, space_after=0)
_run(p, "Specifically, it seeks to answer:", 16, MUTED, bold=True, italic=True)
qs = [
    "What is the percent live coral cover of the selected reef site?",
    "What is the turbidity level (a measure of sedimentation) of the surrounding water?",
    "Is there a significant relationship between turbidity level and percent live coral cover?",
]
cy = y + 2.35
for i, q in enumerate(qs):
    col = SUCCESS if i == 2 else PRIMARY
    badge = rect(s, 1.0, cy, 0.46, 0.46, fill=col, kind=MSO_SHAPE.OVAL)
    fill_frame(badge, [(str(i + 1), 17, WHITE, True)], align=CENTER)
    _, tf = textbox(s, 1.65, cy - 0.05, SW - 2.6, 0.6, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.02)
    _run(p, q, 19, INK)
    cy += 0.68
notes(s, "Walk through why this example works: the general objective states the overall intent in one "
      "sentence; each specific question isolates a single measurable variable or relationship; and the "
      "final question is explicitly relational, signaling that this study will need a hypothesis and an "
      "inferential statistical test. Note for students that specific objective #3, phrased as a "
      "relationship, is the one that will pair with a directional hypothesis in the next slide.")

# ---- Slide 37 (Part III / 11) Worked Example SOP (Agriculture) -------
s = new_slide()
y = header(s, EB6, "Worked Example \u2014 A Full SOP (Agriculture)", 37, title_size=29)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example")
go = rrect(s, 0.85, y + 0.5, SW - 1.7, 1.15, fill=INK, radius=0.08, shadow=True)
_, tf = textbox(s, 1.2, y + 0.5, SW - 2.4, 1.15, anchor=MID)
p = para(tf, first=True, space_after=4, line_spacing=1.02)
_run(p, "GENERAL OBJECTIVE", 13, AMBER, bold=True, font=F_HEAD)
p = para(tf, space_after=0, line_spacing=1.08)
_run(p, "This study aims to determine the ", 17, WHITE)
_run(p, "effect of organic foliar fertilizer application", 17, "9FE3D6", bold=True)
_run(p, " on the ", 17, WHITE)
_run(p, "yield of eggplant (Solanum melongena)", 17, "9FE3D6", bold=True)
_run(p, " in a selected farm in Davao del Sur.", 17, WHITE)
_, tf = textbox(s, 0.9, y + 1.85, SW - 1.9, 0.35)
p = para(tf, first=True, space_after=0)
_run(p, "Specifically, it seeks to answer:", 16, MUTED, bold=True, italic=True)
qs = [
    "What is the average yield (kg per plot) of eggplant grown with organic foliar fertilizer?",
    "What is the average yield of eggplant grown without organic foliar fertilizer (control)?",
    "Is there a significant difference in yield between the two groups?",
]
cy = y + 2.35
for i, q in enumerate(qs):
    col = SUCCESS if i == 2 else PRIMARY
    badge = rect(s, 1.0, cy, 0.46, 0.46, fill=col, kind=MSO_SHAPE.OVAL)
    fill_frame(badge, [(str(i + 1), 17, WHITE, True)], align=CENTER)
    _, tf = textbox(s, 1.65, cy - 0.05, SW - 2.6, 0.6, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.02)
    _run(p, q, 19, INK)
    cy += 0.68
notes(s, "Contrast this with the coral reef example: this SOP is built around a group comparison "
      "(treatment vs. control) rather than a relationship between two continuous variables. Point out that "
      "specific objective #3 signals a comparison-type hypothesis (testing a difference between groups), "
      "while the coral reef example's #3 signals a relationship-type hypothesis (testing an association "
      "between two variables). Both are equally valid \u2014 the phrasing simply depends on the design.")

# ---- Slide 38 (Part III / 12) A Light Touch on Variables -------------
s = new_slide()
y = header(s, EB6, "A Light Touch on Variables", 38, title_size=30)
by = y + 0.4
iv = rrect(s, 1.5, by, 4.3, 1.3, fill=PRIMARY, radius=0.1, shadow=True)
fill_frame(iv, [("INDEPENDENT VARIABLE\n", 16, WHITE, True), ("predictor / cause", 14, "EAF6F8")], align=CENTER)
a = rect(s, 6.0, by + 0.4, 1.3, 0.5, fill=INK, kind=MSO_SHAPE.RIGHT_ARROW)
dv = rrect(s, 7.5, by, 4.3, 1.3, fill=SUCCESS, radius=0.1, shadow=True)
fill_frame(dv, [("DEPENDENT VARIABLE\n", 16, WHITE, True), ("outcome / effect", 14, "E6F5F2")], align=CENTER)
bullets(s, 0.9, y + 2.05, SW - 1.9, [
    [("Coral reef: ", True, False, PRIMARY), ("sedimentation / turbidity level", False, True),
     (" (independent) \u2192 ", False), ("live coral cover", False, True), (" (dependent)", False)],
    [("Agriculture: ", True, False, PRIMARY), ("fertilizer application", False, True),
     (" (independent) \u2192 ", False), ("eggplant yield", False, True), (" (dependent)", False)],
    [("We name variables here ", False), ("only so you can phrase a hypothesis correctly", True),
     (" \u2014 not to master variable measurement, which belongs to your methodology lecture.", False)],
], size=20, gap=9)
notes(s, "Keep this brief and functional, exactly as intended \u2014 this is a preferred, not highly "
      "required, sub-topic, and the goal is only enough vocabulary to write a well-formed hypothesis. Do "
      "not go into operationalization, levels of measurement, or scales; explicitly tell students that is "
      "coming in the methodology lecture. This scoping statement protects today's lecture from sprawling "
      "into statistics.")

# ---- Slide 39 (Part III / 13) Application: Label the Variables -------
s = new_slide()
y = header(s, EB6, "Application \u2014 Label the Variables", 39, title_size=30)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity")
data = [
    ["Study", "Independent Variable", "Dependent Variable"],
    ["\u201cEffect of shade netting on seedling survival rate\u201d", "", ""],
    ["\u201cRelationship between water temperature and coral bleaching extent\u201d", "", ""],
]
cc = {(1, 1): AMBER_LT, (1, 2): AMBER_LT, (2, 1): AMBER_LT, (2, 2): AMBER_LT}
styled_table(s, 0.85, y + 0.5, SW - 1.7, data, col_widths=[1.8, 1.1, 1.1],
             size=17, header_size=16, row_h=1.0, header_h=0.6, cell_colors=cc)
instruction_bar(s, 0.85, y + 3.35, SW - 1.7,
                "Quick 2-minute oral drill \u2014 which variable is the presumed cause, which the effect?")
notes(s, "Quick, low-stakes drill \u2014 2 minutes, whole-class oral answers. The purpose is purely to build "
      "fluency identifying which variable is the presumed cause (independent) and which is the presumed "
      "effect (dependent), since this fluency is what makes writing a clear, directional hypothesis "
      "possible in the next slides.")

# ---- Slide 40 (Part III / 14) Null vs Alternative Hypothesis ---------
s = new_slide()
y = header(s, EB6, "Null vs. Alternative Hypothesis", 40, title_size=30)
two_column(s, y + 0.05,
    left={"title": "NULL HYPOTHESIS  (H\u2080)", "band": MUTED, "head_size": 18,
          "items": [
              "States there is no significant relationship or difference.",
              [("Example: ", True, False, MUTED),
               ("\u201cThere is no significant relationship between turbidity and live coral cover.\u201d", False, True)],
          ], "size": 19, "gap": 10},
    right={"title": "ALTERNATIVE HYPOTHESIS  (H\u2081)", "band": PRIMARY, "head_size": 18,
           "items": [
               "States there is a significant relationship or difference \u2014 often stated directionally.",
               [("Example: ", True, False, PRIMARY),
                ("\u201cThere is a significant negative relationship between turbidity and live coral cover \u2014 "
                 "the higher the turbidity, the lower the coral cover.\u201d", False, True)],
           ], "size": 19, "gap": 10},
    bottom=y + 3.15)
b = rrect(s, 0.85, y + 3.4, SW - 1.7, 0.7, fill=AMBER_LT, radius=0.1)
_, tf = textbox(s, 1.2, y + 3.4, SW - 2.4, 0.7, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.0)
_run(p, "We define these terms today. ", 17, INK, bold=True)
_run(p, "Testing them with p-values and significance levels is deferred to your statistics lecture.", 17, INK_SOFT)
notes(s, "Emphasize this is a definition-only stop, consistent with the boundary set in the outline \u2014 do "
      "not let the discussion drift into explaining p-values or test selection, since that content is "
      "explicitly deferred. Highlight Creswell's point that most researchers ultimately report an "
      "alternative, and preferably directional, hypothesis, because a directional hypothesis communicates "
      "the researcher's specific prediction rather than merely asserting that \"some difference\" exists.")

# ---- Slide 41 (Part III / 15) Application: Write H0 and Ha -----------
s = new_slide()
y = header(s, EB6, "Application \u2014 Write H\u2080 and H\u2081 (Agriculture)", 41, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity")
scenario_card(s, 0.85, y + 0.5, SW - 1.7, 1.0,
              "Given specific objective #3 from the Agriculture SOP (Slide 37): \u201cIs there a significant "
              "difference in yield between the two groups?\u201d",
              size=17, fill=INK, tcolor=WHITE, label=None)
template_card(s, 0.85, y + 1.75, SW - 1.7, 2.4, [
    "H\u2080  (null):",
    "H\u2081  (alternative \u2014 make it directional: which group yields more, and why?):",
], size=21)
notes(s, "Give students two minutes to draft both hypotheses individually, then have three volunteers "
      "share their H\u2081 aloud. A strong directional answer: \"Eggplant plots treated with organic foliar "
      "fertilizer will have significantly higher yield than untreated plots.\" Praise directional language "
      "(higher, lower, greater, more) over vague language (\"will be different\").")

# ---- Slide 42 (Part III / 16) Scripts for Quantitative Questions -----
s = new_slide()
y = header(s, EB6, "Scripts for Writing Quantitative Questions", 42, title_size=28)
card(s, 0.85, y + 0.25, SW - 1.7, 1.15, fill="FBFDFE", line=PRIMARY)
card_header(s, 0.85, y + 0.25, SW - 1.7, "DESCRIPTIVE SCRIPT", PRIMARY, size=15, h=0.5)
_, tf = textbox(s, 1.2, y + 0.82, SW - 2.4, 0.55, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.05)
_run(p, "\u201cWhat is the [level / frequency / percentage] of ______ (variable) among ______ "
        "(participants / site)?\u201d", 18, INK, italic=True)
card(s, 0.85, y + 1.55, SW - 1.7, 1.3, fill="FBFDFE", line=ACCENT)
card_header(s, 0.85, y + 1.55, SW - 1.7, "RELATIONSHIP / DIRECTIONAL SCRIPT", ACCENT, size=15, h=0.5)
_, tf = textbox(s, 1.2, y + 2.12, SW - 2.4, 0.7, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.05)
_run(p, "\u201cIt is predicted that there will be a relationship between ______ (predictor) and ______ "
        "(outcome), such that ______ (direction of the effect).\u201d", 18, INK, italic=True)
b = rrect(s, 0.85, y + 3.05, SW - 1.7, 1.05, fill=INK, radius=0.08, shadow=True)
_, tf = textbox(s, 1.2, y + 3.05, SW - 2.4, 1.05, anchor=MID)
p = para(tf, first=True, space_after=3, line_spacing=1.0)
_run(p, "APPLIED \u2014 CORAL REEF", 12.5, AMBER, bold=True, font=F_HEAD)
p = para(tf, space_after=0, line_spacing=1.05)
_run(p, "\u201cIt is predicted that there will be a relationship between turbidity level and live coral "
        "cover, such that higher turbidity is associated with lower coral cover.\u201d", 16.5, WHITE, italic=True)
notes(s, "These are direct adaptations of Creswell's scripting technique for descriptive and "
      "relationship-oriented quantitative questions. Scripts function like sentence frames in language "
      "learning \u2014 they reduce the cognitive load of \"what do I even write\" so students can focus on "
      "getting their variables and direction correct. Encourage students to keep these two scripts in "
      "their notes as their go-to templates for the rest of the course.")

# ---- Slide 43 (Part III / 17) Scripts for Qualitative Questions ------
s = new_slide()
y = header(s, EB6, "Scripts for Writing Qualitative Questions", 43, title_size=28)
card(s, 0.85, y + 0.3, SW - 1.7, 1.2, fill="FBFDFE", line=ACCENT)
card_header(s, 0.85, y + 0.3, SW - 1.7, "CENTRAL QUESTION SCRIPT", ACCENT, size=15, h=0.5)
_, tf = textbox(s, 1.2, y + 0.88, SW - 2.4, 0.6, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.05)
_run(p, "\u201c______ (How or What) is the ______ (central phenomenon) for ______ (participants) at ______ "
        "(research site)?\u201d", 18, INK, italic=True)
b = rrect(s, 0.85, y + 1.65, SW - 1.7, 1.1, fill=INK, radius=0.08, shadow=True)
_, tf = textbox(s, 1.2, y + 1.65, SW - 2.4, 1.1, anchor=MID)
p = para(tf, first=True, space_after=3, line_spacing=1.0)
_run(p, "APPLIED \u2014 INSTRUCTOR-CREATED EXAMPLE", 12.5, AMBER, bold=True, font=F_HEAD)
p = para(tf, space_after=0, line_spacing=1.06)
_run(p, "\u201cHow do small-scale fisherfolk in a selected Davao Gulf coastal barangay describe changes in "
        "their livelihood amid declining coral reef health?\u201d", 16.5, WHITE, italic=True)
bullets(s, 0.9, y + 2.95, SW - 1.9, [
    [("Two habits to flag: qualitative questions open with ", False), ("how", True, True, ACCENT),
     (" or ", False), ("what", True, True, ACCENT),
     (" (not ", False), ("why", True, True, DANGER),
     (", which implies cause-and-effect), and they focus on a ", False),
     ("single central phenomenon", True), (".", False)],
], size=18, gap=6)
notes(s, "Explicitly connect this back to Slide 30, where a \"why\" question was flagged as a caution. "
      "Explain that why tends to smuggle in causal, quantitative thinking, which conflicts with "
      "qualitative research's exploratory purpose. Model quickly revising \"Why do fisherfolk struggle "
      "economically?\" into \"How do fisherfolk describe their economic struggles?\" so students see the "
      "transformation in real time.")

# ---- Slide 44 (Part III / 18) Workshop: Draft Your Own SOP -----------
s = new_slide()
y = header(s, EB6, "Workshop \u2014 Draft Your Own SOP", 44, title_size=30)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity \u00b7 10\u201315 minutes")
steps = [
    [("Write your ", False), ("general objective", True, False, PRIMARY), (" (1 sentence).", False)],
    [("Write ", False), ("at least 3 specific research questions", True, False, PRIMARY),
     (" (quantitative) or 1 central question + 5\u20137 sub-questions (qualitative).", False)],
    [("If quantitative and relational/comparative, draft your ", False),
     ("H\u2080 and directional H\u2081", True, False, ACCENT), (".", False)],
    [("Trade papers and check each question against the ", False),
     ("Clear\u2013Focused\u2013Answerable", True, False, SUCCESS), (" checklist (Slide 31).", False)],
]
cy = y + 0.55
for i, st in enumerate(steps):
    b = rrect(s, 0.85, cy, SW - 1.7, 0.82, fill=CARD, line=LINE, radius=0.1, shadow=True)
    badge = rect(s, 1.1, cy + 0.19, 0.44, 0.44, fill=PRIMARY, kind=MSO_SHAPE.OVAL)
    fill_frame(badge, [(str(i + 1), 17, WHITE, True)], align=CENTER)
    _, tf = textbox(s, 1.72, cy, SW - 1.7 - 1.15, 0.82, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.02)
    for seg in st:
        t = seg[0]
        bold = seg[1] if len(seg) > 1 else False
        ital = seg[2] if len(seg) > 2 else False
        col = seg[3] if len(seg) > 3 else INK
        _run(p, t, 18, col, bold, ital)
    cy += 0.94
notes(s, "This is the pivot point of the lecture: from modeling to production. Circulate actively during "
      "this workshop \u2014 the most common errors to watch for are (1) specific questions that don't map to "
      "a measurable variable, (2) qualitative questions that sneak in \"why,\" and (3) hypotheses stated "
      "non-directionally (\"there is a difference\" instead of specifying which group is higher). Reserve "
      "the last two minutes for two or three students to read their general objective and first specific "
      "question aloud for whole-class feedback \u2014 this doubles as informal rehearsal for oral defense, "
      "which Part IV will build on directly.")

# =========================================================================
# SECTION 7 (Part IV) - JUSTIFYING THE PROBLEM WITH CER (Competency 15)
# =========================================================================

# ---- Slide 45 (Part IV / 19) From "What" to "So What" ----------------
s = new_slide()
y = header(s, EB7, "From \u201cWhat\u201d to \u201cSo What\u201d", 45, title_size=30)
roadmap(s, y + 0.12, active=2, done={0, 1})
bullets(s, 0.9, y + 1.45, SW - 1.9, [
    [("You now know ", False), ("what", True, True, PRIMARY),
     (" you will investigate. A research panel's very next question will be: ", False),
     ("\u201cSo what? Why does this matter?\u201d", True, False, ACCENT)],
    [("Today you learn a reusable structure for answering that question with ", False),
     ("evidence", True, False, SUCCESS), (", not just enthusiasm.", False)],
], size=24, gap=14)
notes(s, "Frame this transition explicitly as the moment students move from designing a study to "
      "defending it. Tell students that \"why does this matter\" is one of the first questions asked in "
      "almost every research defense, and that today's framework is the tool they will use to answer it "
      "\u2014 both in writing (Chapter 1) and out loud (their defense).")

# ---- Slide 46 (Part IV / 20) Introducing CER -------------------------
s = new_slide()
y = header(s, EB7, "Introducing Claim \u2013 Evidence \u2013 Reasoning", 46, title_size=28)
cer = [
    ("CLAIM", "the problem is worth studying", PRIMARY),
    ("EVIDENCE", "literature findings / gaps you found", ACCENT),
    ("REASONING", "explicit logic linking evidence to the claim", SUCCESS),
]
cw = (SW - 1.7 - 2 * 0.55) / 3
for i, (t, d, col) in enumerate(cer):
    px = 0.85 + i * (cw + 0.55)
    b = rrect(s, px, y + 0.15, cw, 1.35, fill=col, radius=0.12, shadow=True)
    tf = b.text_frame; tf.word_wrap = True; tf.vertical_anchor = MID
    p = tf.paragraphs[0]; p.alignment = CENTER; p.line_spacing = 1.02
    _run(p, t + "\n", 19, WHITE, bold=True, font=F_HEAD)
    _run(p, d, 14, "F2F7F9")
    if i < 2:
        a = rect(s, px + cw + 0.06, y + 0.6, 0.42, 0.45, fill=INK, kind=MSO_SHAPE.RIGHT_ARROW)
bullets(s, 0.9, y + 1.75, SW - 1.9, [
    [("CER", True, False, INK),
     (" builds a convincing, evidence-based argument for why your research problem matters.", False)],
    [("Claim", True, False, PRIMARY), (" = your assertion that the problem is significant and worth studying.", False)],
    [("Evidence", True, False, ACCENT), (" = literature findings, statistics, or documented gaps that support the claim.", False)],
    [("Reasoning", True, False, SUCCESS),
     (" = the explicit logical bridge connecting evidence back to the claim \u2014 the step students most often skip.", False)],
], size=17, gap=6)
notes(s, "CER is a familiar structure from science class (used for evidence-based argumentation in lab "
      "reports), and this slide's job is to show students it transfers directly to justifying a research "
      "problem. Stress that Reasoning is not a summary of the evidence \u2014 it is the sentence that "
      "explicitly explains why the evidence proves the claim. Most weak \"Background of the Study\" "
      "sections in student papers have Claim and Evidence but skip Reasoning entirely, leaving the "
      "connection for the reader to guess.")

# ---- Slide 47 (Part IV / 21) Worked CER Paragraph (Coral Reef) -------
s = new_slide()
y = header(s, EB7, "Worked Example \u2014 CER Paragraph (Coral Reef)", 47, title_size=27)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example")
lx = 0.85
for t, col in [("Claim", PRIMARY), ("Evidence", ACCENT), ("Reasoning", SUCCESS)]:
    dot = rect(s, lx, y + 0.5, 0.26, 0.26, fill=col, kind=MSO_SHAPE.OVAL)
    _, tf = textbox(s, lx + 0.34, y + 0.44, 1.9, 0.35, anchor=MID)
    p = para(tf, first=True, space_after=0)
    _run(p, t, 15, INK, bold=True, font=F_HEAD)
    lx += 2.05
card(s, 0.85, y + 0.95, SW - 1.7, 3.7, fill="FBFDFE", line=LINE)
_, tf = textbox(s, 1.3, y + 1.15, SW - 2.6, 3.3, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.24)
_run(p, "[CLAIM] ", 19, PRIMARY, bold=True)
_run(p, "Investigating coral reef degradation in Davao Gulf is an urgent research priority. ", 19, INK)
_run(p, "[EVIDENCE] ", 19, ACCENT, bold=True)
_run(p, "Regional marine surveys have documented declining live coral cover linked to coastal "
        "sedimentation and rising sea surface temperatures, while local fisherfolk report shrinking "
        "catches over the past decade. ", 19, INK)
_run(p, "[REASONING] ", 19, SUCCESS, bold=True)
_run(p, "Because coral reefs serve as the primary nursery habitat for many commercially important fish "
        "species, continued degradation directly threatens both marine biodiversity and the food security "
        "of coastal communities \u2014 meaning the problem is not just ecological, but also has direct human "
        "consequences that justify immediate study.", 19, INK)
notes(s, "Read this paragraph aloud slowly, pointing to each bracketed label as you go. Emphasize that "
      "the Reasoning sentence is doing real argumentative work \u2014 it is not restating the evidence, it is "
      "explaining the mechanism (reef as nursery habitat) that connects declining coral cover to a "
      "consequence the reader will find compelling (food security). This is the sentence structure "
      "students should aim to replicate.")

# ---- Slide 48 (Part IV / 22) Spot the Missing Reasoning --------------
s = new_slide()
y = header(s, EB7, "Application \u2014 Spot the Missing Reasoning", 48, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity")
card(s, 0.85, y + 0.5, SW - 1.7, 1.8, fill=CARD, line=PRIMARY)
_, tf = textbox(s, 1.3, y + 0.7, SW - 2.6, 1.4, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.2)
_run(p, "\u201cPest resistance among corn farmers is a growing concern. Studies show that fall armyworm "
        "populations in several Mindanao provinces have developed resistance to common pesticides, and "
        "farmer surveys report declining yields.\u201d", 20, INK)
bullets(s, 0.9, y + 2.55, SW - 1.9, [
    [("This paragraph has a ", False), ("Claim", True, False, PRIMARY), (" and ", False),
     ("Evidence", True, False, ACCENT), (" \u2014 but is missing ", False),
     ("Reasoning", True, False, SUCCESS),
     (". In pairs, write one sentence that connects the evidence to why this problem deserves study.", False)],
], size=19, gap=6)
instruction_bar(s, 0.85, y + 3.75, SW - 1.7, "3\u20134 minutes, then two pairs share their Reasoning sentence.")
notes(s, "Give students 3\u20134 minutes, then have two pairs share their Reasoning sentence. A strong answer "
      "links the evidence to a broader consequence: \"Because pesticide resistance forces farmers into "
      "costlier and more frequent chemical applications, unresolved resistance threatens both farm "
      "profitability and long-term soil and environmental health.\" Use weaker answers (ones that simply "
      "restate the evidence) as a teaching moment \u2014 ask the class, \"Does this sentence explain why, or "
      "does it just repeat what?\"")

# ---- Slide 49 (Part IV / 23) Label a Full Paragraph ------------------
s = new_slide()
y = header(s, EB7, "Guided Practice \u2014 Label a Full Paragraph", 49, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity")
card(s, 0.85, y + 0.5, SW - 1.7, 2.75, fill=CARD, line=PRIMARY)
_, tf = textbox(s, 1.3, y + 0.72, SW - 2.6, 2.3, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.28)
_run(p, "\u201cImproving post-harvest handling of rice is a pressing issue for small farmers. National "
        "agriculture data show that up to 16% of harvested rice is lost before it reaches market due to "
        "poor drying and storage facilities. Since post-harvest losses directly reduce farmer income "
        "without any corresponding increase in production cost, addressing this gap offers one of the "
        "most cost-effective ways to improve farmer livelihoods without expanding farmland.\u201d", 19, INK)
instruction_bar(s, 0.85, y + 3.5, SW - 1.7,
                "Label each sentence:  C (Claim)  \u00b7  E (Evidence)  \u00b7  R (Reasoning).")
notes(s, "Reveal the answer after students attempt it individually: sentence 1 = Claim, sentence 2 = "
      "Evidence, sentence 3 = Reasoning. This example is slightly more advanced than Slide 47 because the "
      "Reasoning sentence uses comparative logic (\"without any corresponding increase in production "
      "cost\") \u2014 point this out as a more sophisticated way to argue significance: showing the problem is "
      "solvable efficiently, not just that it is big.")

# ---- Slide 50 (Part IV / 24) Writing Workshop: CER Justification -----
s = new_slide()
y = header(s, EB7, "Writing Workshop \u2014 Draft Your CER Justification", 50, title_size=26)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity \u00b7 15 minutes, individual")
steps = [
    [("Write your ", False), ("Claim", True, False, PRIMARY), (" sentence (the problem is worth studying).", False)],
    [("Write 1\u20132 ", False), ("Evidence", True, False, ACCENT),
     (" sentences (literature findings or documented gaps \u2014 real or plausible placeholders to verify later).", False)],
    [("Write your ", False), ("Reasoning", True, False, SUCCESS),
     (" sentence \u2014 explicitly explain why the evidence proves the claim.", False)],
    [("Underline your Reasoning: does it explain a ", False), ("mechanism or consequence", True),
     (", or just restate the evidence?", False)],
]
cy = y + 0.55
for i, st in enumerate(steps):
    b = rrect(s, 0.85, cy, SW - 1.7, 0.82, fill=CARD, line=LINE, radius=0.1, shadow=True)
    badge = rect(s, 1.1, cy + 0.19, 0.44, 0.44, fill=SUCCESS, kind=MSO_SHAPE.OVAL)
    fill_frame(badge, [(str(i + 1), 17, WHITE, True)], align=CENTER)
    _, tf = textbox(s, 1.72, cy, SW - 1.7 - 1.15, 0.82, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.02)
    for seg in st:
        t = seg[0]
        bold = seg[1] if len(seg) > 1 else False
        ital = seg[2] if len(seg) > 2 else False
        col = seg[3] if len(seg) > 3 else INK
        _run(p, t, 17.5, col, bold, ital)
    cy += 0.94
notes(s, "This paragraph is essentially the seed of their eventual \"Background of the Study\" section. "
      "Circulate and specifically probe any student whose Reasoning sentence simply repeats their "
      "Evidence \u2014 ask them directly, \"Why does that fact matter?\" and have them speak the answer before "
      "writing it down; this oral-to-written technique often produces a much stronger Reasoning sentence "
      "than writing alone.")

# ---- Slide 51 (Part IV / 25) Speaking Workshop: Defend Aloud ---------
s = new_slide()
y = header(s, EB7, "Speaking Workshop \u2014 Defend Your Claim Aloud", 51, title_size=26)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity \u00b7 Defense simulation, 10 min")
steps = [
    [("Partner A reads their ", False), ("Claim sentence only", True, False, PRIMARY),
     (" \u2014 no evidence, no reasoning yet.", False)],
    [("Partner B asks: ", False), ("\u201cSo what? Why should anyone study that?\u201d", True, False, ACCENT)],
    [("Partner A answers ", False), ("out loud, from memory", True, False, SUCCESS),
     (", using their Evidence and Reasoning \u2014 no reading from paper.", False)],
    [("Switch roles.", False)],
]
cy = y + 0.55
for i, st in enumerate(steps):
    b = rrect(s, 0.85, cy, SW - 1.7, 0.72, fill=CARD, line=LINE, radius=0.1, shadow=True)
    badge = rect(s, 1.1, cy + 0.14, 0.44, 0.44, fill=INK, kind=MSO_SHAPE.OVAL)
    fill_frame(badge, [(str(i + 1), 16, WHITE, True)], align=CENTER)
    _, tf = textbox(s, 1.72, cy, SW - 1.7 - 1.15, 0.72, anchor=MID)
    p = para(tf, first=True, space_after=0, line_spacing=1.0)
    for seg in st:
        t = seg[0]
        bold = seg[1] if len(seg) > 1 else False
        ital = seg[2] if len(seg) > 2 else False
        col = seg[3] if len(seg) > 3 else INK
        _run(p, t, 17.5, col, bold, ital)
    cy += 0.82
b = rrect(s, 0.85, cy + 0.02, SW - 1.7, 0.62, fill=AMBER_LT, radius=0.1)
_, tf = textbox(s, 1.2, cy + 0.02, SW - 2.4, 0.62, anchor=MID)
p = para(tf, first=True, space_after=0)
_run(p, "This is exactly the kind of question a research panel will ask during your defense.", 16.5, INK, bold=True)
notes(s, "This activity deliberately mimics the pressure of an oral defense: being asked \"so what?\" cold, "
      "without the safety of reading a script. Tell students that panelists rarely accept \"because it's "
      "an important issue\" as an answer \u2014 they want the specific mechanism or consequence, which is "
      "exactly what the Reasoning step trains them to articulate. After the paired rounds, ask for one or "
      "two volunteers to answer \"so what?\" in front of the whole class, and give the class 30 seconds to "
      "identify whether the answer contained a genuine Reasoning step or only repeated Evidence.\n\n"
      "Visual: none required \u2014 a simple on-screen timer is sufficient support.")

# ---- Slide 52 (Part IV / 26) Common CER Pitfalls in a Defense --------
s = new_slide()
y = header(s, EB7, "Common CER Pitfalls in a Defense", 52, title_size=29)
data = [
    ["Pitfall", "Fix"],
    ["Evidence with no source or citation (\u201cstudies show...\u201d)",
     "Name the actual source, or say \u201cbased on my preliminary reading of...\u201d"],
    ["Reasoning that just restates Evidence in different words",
     "Ask: what happens next if this problem is ignored? State that consequence."],
    ["Claim stated as pure opinion (\u201cthis is a very important topic\u201d)",
     "Ground the claim in a measurable stake \u2014 lives affected, income lost, species threatened"],
]
styled_table(s, 0.85, y + 0.3, SW - 1.7, data, col_widths=[1.05, 1.15],
             size=17.5, header_size=18, row_h=1.0, header_h=0.58, header_fill=DANGER)
notes(s, "These three pitfalls are the most common reasons a panel pushes back during the justification "
      "portion of a defense. Walking through them explicitly gives students a self-editing checklist they "
      "can apply to their own Chapter 1 draft before submission, not just today's practice paragraph.")

# =========================================================================
# SECTION 8 (Part V) - ASSUMPTIONS AND LIMITATIONS (Competency 16)
# =========================================================================

# ---- Slide 53 (Part V / 27) Even the Best Study Has Boundaries -------
s = new_slide()
y = header(s, EB8, "Even the Best Study Has Boundaries", 53, title_size=30)
roadmap(s, y + 0.12, active=3, done={0, 1, 2})
bullets(s, 0.9, y + 1.45, SW - 1.9, [
    [("No study \u2014 not even a professionally funded one \u2014 can measure everything, control everything, "
      "or prove itself beyond all doubt.", False)],
    [("Today's skill is not weakness \u2014 it is ", False), ("precision", True, False, ACCENT),
     (": telling your reader exactly what your study takes for granted, and exactly where its findings "
      "stop applying.", False)],
], size=23, gap=14)
notes(s, "Set the emotional tone here deliberately \u2014 many students believe naming limitations makes "
      "their study look weak, and this slide exists to preempt that misconception before the formal "
      "definitions arrive. Tell them a panel is far more suspicious of a paper that claims no limitations "
      "than one that names them clearly.")

# ---- Slide 54 (Part V / 28) Assumptions vs Limitations Defined -------
s = new_slide()
y = header(s, EB8, "Assumptions vs. Limitations \u2014 Defined", 54, title_size=29)
two_column(s, y + 0.1,
    left={"title": "ASSUMPTIONS", "band": PRIMARY, "head_size": 19, "icon": "\u2713",
          "items": [
              "What you take as true or given, without directly testing it, in order for your study to proceed.",
              [("Example: ", True, False, PRIMARY),
               ("\u201cIt is assumed that survey respondents answered honestly.\u201d", False, True)],
          ], "size": 20, "gap": 12},
    right={"title": "LIMITATIONS", "band": ACCENT, "head_size": 19, "icon": "!",
           "items": [
               "The constraints or weaknesses of your study \u2014 factors beyond your control that may affect your findings.",
               [("Example: ", True, False, ACCENT),
                ("\u201cThis study is limited by a small sample size of 30 farmers, which may not represent the "
                 "entire municipality.\u201d", False, True)],
           ], "size": 20, "gap": 12},
    bottom=y + 3.85)
notes(s, "The clearest way to distinguish these for students: an assumption is a condition you believe is "
      "true but cannot fully verify, while a limitation is a constraint you already know exists. "
      "Assumptions are about trust in your data-gathering process; limitations are about the boundaries of "
      "what your method can achieve.")

# ---- Slide 55 (Part V / 29) Application: Sort Assumption or Limitation
s = new_slide()
y = header(s, EB8, "Application \u2014 Sort Assumption or Limitation", 55, title_size=28)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity")
data = [
    ["Statement", "Assumption or Limitation?"],
    ["\u201cIt is assumed that the water quality test kits used provide accurate turbidity readings.\u201d", ""],
    ["\u201cThe study only measured coral cover during the dry season and may not reflect wet-season conditions.\u201d", ""],
    ["\u201cIt is assumed that farmer-respondents accurately recalled their harvest yields from memory.\u201d", ""],
    ["\u201cOnly one farm cooperative in Davao del Sur was included due to time and travel constraints.\u201d", ""],
]
cc = {(1, 1): AMBER_LT, (2, 1): AMBER_LT, (3, 1): AMBER_LT, (4, 1): AMBER_LT}
styled_table(s, 0.85, y + 0.5, SW - 1.7, data, col_widths=[2.3, 1.0],
             size=16, header_size=16, row_h=0.72, header_h=0.55, cell_colors=cc)
notes(s, "Rows 1 and 3 are assumptions (trust placed in an instrument or a respondent's honesty/memory); "
      "rows 2 and 4 are limitations (known constraints on scope or timing). After students sort these, "
      "ask: \"Could row 1 become a limitation if you had reason to doubt the test kits?\" \u2014 this shows "
      "students the categories depend on the researcher's actual confidence level, not a fixed rule.")

# ---- Slide 56 (Part V / 30) Why Naming Limitations Builds Credibility
s = new_slide()
y = header(s, EB8, "Why Naming Limitations Builds Credibility", 56, title_size=28)
# path 1 (negative)
r1 = rrect(s, 0.85, y + 0.5, 5.0, 1.6, fill=DANGER_LT, line=DANGER, radius=0.1)
_, tf = textbox(s, 1.15, y + 0.5, 4.5, 1.6, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.1)
_run(p, "Study claims \u201cno limitations\u201d", 18, DANGER, bold=True)
a = rect(s, 6.0, y + 1.05, 0.9, 0.5, fill=DANGER, kind=MSO_SHAPE.RIGHT_ARROW)
r1b = rrect(s, 7.05, y + 0.5, 5.4, 1.6, fill=CARD, line=DANGER, radius=0.1)
_, tf = textbox(s, 7.35, y + 0.5, 4.8, 1.6, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.12)
_run(p, "Panel doubts the researcher's self-awareness and rigor", 18, INK)
# path 2 (positive)
r2 = rrect(s, 0.85, y + 2.35, 5.0, 1.7, fill=SUCCESS_LT, line=SUCCESS, radius=0.1)
_, tf = textbox(s, 1.15, y + 2.35, 4.5, 1.7, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.1)
_run(p, "Study names limitations clearly", 18, SUCCESS, bold=True)
a = rect(s, 6.0, y + 3.0, 0.9, 0.5, fill=SUCCESS, kind=MSO_SHAPE.RIGHT_ARROW)
r2b = rrect(s, 7.05, y + 2.35, 5.4, 1.7, fill=CARD, line=SUCCESS, radius=0.1)
_, tf = textbox(s, 7.35, y + 2.35, 4.8, 1.7, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.12)
_run(p, "Panel sees the researcher understands their method's boundaries \u2192 trusts the findings that remain", 18, INK)
notes(s, "This is the conceptual core of the section. Every professional, peer-reviewed study names its "
      "limitations \u2014 it is not an admission of failure but a sign of methodological maturity. Make the "
      "analogy explicit: a doctor who tells you the exact margin of error on a diagnostic test is more "
      "trustworthy than one who claims 100% certainty. Naming limitations is how a researcher shows "
      "control over their own claims.")

# ---- Slide 57 (Part V / 31) Worked Example A&L (Coral Reef) ----------
s = new_slide()
y = header(s, EB8, "Worked Example \u2014 Assumptions & Limitations (Coral Reef)", 57, title_size=24)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example")
two_column(s, y + 0.5,
    left={"title": "ASSUMPTIONS", "band": PRIMARY, "head_size": 18,
          "items": [
              "The water quality testing equipment produces accurate and consistent readings across all sampling sites.",
              "The selected reef sites are representative of general reef conditions within the barangay's coastal zone.",
          ], "size": 18, "gap": 10},
    right={"title": "LIMITATIONS", "band": ACCENT, "head_size": 18,
           "items": [
               "Data collection was limited to a single dry-season sampling period and does not capture seasonal variation.",
               "Only three reef sites in one barangay were covered; results cannot be generalized to the entire Davao Gulf coastline.",
           ], "size": 18, "gap": 10},
    bottom=y + 4.0)
notes(s, "Notice both assumptions are about trusting the instrument and the sample's representativeness, "
      "while both limitations are about scope \u2014 timing and geographic coverage. This paired structure (2 "
      "assumptions, 2 limitations) is a reasonable minimum for an SHS-level paper; more may be added as "
      "the actual methodology develops.")

# ---- Slide 58 (Part V / 32) Worked Example A&L (Agriculture) ---------
s = new_slide()
y = header(s, EB8, "Worked Example \u2014 Assumptions & Limitations (Agriculture)", 58, title_size=24)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Example")
two_column(s, y + 0.5,
    left={"title": "ASSUMPTIONS", "band": PRIMARY, "head_size": 18,
          "items": [
              "All experimental and control plots received equal sunlight and watering except for the fertilizer treatment being tested.",
              "Respondent-farmers reported their historical yield data accurately.",
          ], "size": 18, "gap": 10},
    right={"title": "LIMITATIONS", "band": ACCENT, "head_size": 18,
           "items": [
               "The study was conducted on a single farm, so results may not apply to farms with different soil or climate.",
               "The experiment ran for only one growing cycle, and results may vary across seasons or years.",
           ], "size": 18, "gap": 10},
    bottom=y + 4.0)
notes(s, "Point out the parallel structure with the coral reef example \u2014 this consistency is intentional "
      "and something students should imitate: assumptions cluster around trust in controlled conditions or "
      "respondent honesty, while limitations cluster around generalizability and time constraints. Ask "
      "students to predict: \"What limitation would appear if this experiment had also been affected by an "
      "unexpected typhoon?\" \u2014 guide them toward recognizing environmental/external disruptions as a "
      "third common category of limitation.")

# ---- Slide 59 (Part V / 33) Application: Draft Your Own --------------
s = new_slide()
y = header(s, EB8, "Application \u2014 Draft Your Own", 59, title_size=30)
eg_tag(s, 0.85, y - 0.02, "Instructor-Created Practice Activity \u00b7 10 minutes")
bw = (SW - 1.7 - 0.5) / 2
for title, col, bx in [("Write 2 ASSUMPTIONS", PRIMARY, 0.85),
                       ("Write 2 LIMITATIONS", ACCENT, 0.85 + bw + 0.5)]:
    card(s, bx, y + 0.5, bw, 2.4)
    card_header(s, bx, y + 0.5, bw, title, col, size=17)
    sub = ("what are you trusting to be true without testing it?" if col == PRIMARY
           else "what constraints (time, sample, scope, instruments, events) affect the study?")
    _, tf = textbox(s, bx + 0.3, y + 1.15, bw - 0.6, 0.5)
    p = para(tf, first=True, space_after=0, line_spacing=1.0)
    _run(p, sub, 14, MUTED, italic=True)
    for k in range(2):
        rrect(s, bx + 0.35, y + 1.75 + k * 0.5, bw - 0.7, 0.045, fill=LINE, radius=0.5)
instruction_bar(s, 0.85, y + 3.15, SW - 1.7,
                "Trade with a partner: can they tell your assumptions from your limitations without help?")
notes(s, "The final check in step 3 is the real test of mastery \u2014 if a partner cannot distinguish an "
      "assumption from a limitation without explanation, the statement is probably miscategorized or "
      "poorly worded. Circulate and watch for the most common student error: listing a limitation (\"small "
      "sample size\") disguised as an assumption (\"it is assumed the small sample is enough\").")

# ---- Slide 60 (Part V / 34) Looking Ahead ----------------------------
s = new_slide()
y = header(s, EB8, "Looking Ahead \u2014 Limitations Shape Your Method", 60, title_size=27)
bullets(s, 0.9, y + 0.55, SW - 1.9, [
    [("Some limitations you just wrote \u2014 sample size, timing, instrument choice \u2014 are ", False),
     ("not fixed", True, False, ACCENT),
     (". They will directly shape the ", False), ("methodology decisions", True, False, PRIMARY),
     (" you make next: how you sample, what instruments you choose, and how you schedule data collection.", False)],
    [("Naming a limitation today is often the first step toward ", False),
     ("designing around it", True, False, SUCCESS), (" tomorrow.", False)],
], size=24, gap=16)
b = rrect(s, 0.85, y + 3.1, SW - 1.7, 1.0, fill=INK, radius=0.1, shadow=True)
_, tf = textbox(s, 1.2, y + 3.1, SW - 2.4, 1.0, anchor=MID)
p = para(tf, first=True, space_after=0, line_spacing=1.05)
_run(p, "Research Questions & Hypotheses  +  CER Justification  +  Assumptions & Limitations  ", 16, WHITE, bold=True)
_run(p, "=  the complete Chapter 1.", 16, AMBER, bold=True)
notes(s, "Keep this brief, exactly as scoped \u2014 its purpose is only to motivate students toward the "
      "upcoming methodology content, not to teach any methodology itself. Close by reminding students that "
      "today's three skills \u2014 writing research questions and hypotheses, justifying the problem through "
      "CER, and naming assumptions and limitations \u2014 together complete Chapter 1 of their manuscript, "
      "and that all three are exactly what a defense panel will ask them to explain and defend out loud.")

# ---- Slide 61 (Part V / 35) Recap: Today's Three Competencies --------
s = new_slide()
y = header(s, EB8, "Recap \u2014 Today's Three Competencies", 61, title_size=29)
comp = [
    ("Competency 14", "Research Questions & Hypotheses",
     "Narrow the problem into clear, focused, answerable questions; write directional hypotheses when quantitative", PRIMARY),
    ("Competency 15", "CER Justification",
     "Build a Claim\u2013Evidence\u2013Reasoning argument for why the problem matters", ACCENT),
    ("Competency 16", "Assumptions & Limitations",
     "Name what you take as true (assumptions) and what constrains your study (limitations)", SUCCESS),
]
cw = (SW - 1.7 - 2 * 0.4) / 3
for i, (comp_no, title, desc, col) in enumerate(comp):
    px = 0.85 + i * (cw + 0.4)
    card(s, px, y + 0.25, cw, 3.15)
    card_header(s, px, y + 0.25, cw, comp_no, col, size=17, h=0.6)
    _, tf = textbox(s, px + 0.28, y + 1.0, cw - 0.56, 0.7)
    p = para(tf, first=True, space_after=0, line_spacing=1.0)
    _run(p, title, 18, INK, bold=True, font=F_HEAD)
    _, tf = textbox(s, px + 0.28, y + 1.75, cw - 0.56, 1.6, anchor=MSO_ANCHOR.TOP)
    p = para(tf, first=True, space_after=0, line_spacing=1.12)
    _run(p, desc, 15.5, MUTED)
b = rrect(s, 0.85, y + 3.6, SW - 1.7, 0.62, fill=INK, radius=0.1)
_, tf = textbox(s, 1.2, y + 3.6, SW - 2.4, 0.62, anchor=MID)
p = para(tf, first=True, space_after=0)
_run(p, "Together, these three skills complete the ", 16, WHITE)
_run(p, "argumentative backbone of Chapter 1", 16, AMBER, bold=True)
_run(p, " \u2014 and the core of what you will defend.", 16, WHITE)
notes(s, "Use this closing slide as a rapid-fire oral review \u2014 call on students to define each competency "
      "in one sentence, in their own words, without looking at their notes. This final retrieval practice "
      "reinforces retention and gives one last low-stakes rehearsal of explaining these concepts aloud, "
      "mirroring the defense-style speaking they will need later.")

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
footer(s, 62)
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
