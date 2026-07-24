#!/usr/bin/env python3
"""
Lecture 2: Research Ethics — Word script + activity answer key.

Generates a .docx containing, for every slide:
  - On-slide content (the exact student-facing text)
  - Speaker notes (the teaching script)
  - An Answer Key for the activity ("Apply it") slides.
"""
from docx import Document
from docx.shared import Pt, RGBColor, Inches
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.oxml.ns import qn
from docx.oxml import OxmlElement

TEAL = RGBColor(0x0F, 0x4C, 0x5C)
AQUA = RGBColor(0x2A, 0x9D, 0x8F)
CORAL = RGBColor(0xC0, 0x53, 0x38)
GREEN = RGBColor(0x1E, 0x7A, 0x33)
INK = RGBColor(0x21, 0x2A, 0x33)
MUTED = RGBColor(0x5B, 0x6B, 0x73)

doc = Document()

# ---- base styles ----
normal = doc.styles["Normal"]
normal.font.name = "Calibri"
normal.font.size = Pt(11)
normal.font.color.rgb = INK

sec = doc.sections[0]
sec.left_margin = Inches(1.0)
sec.right_margin = Inches(1.0)
sec.top_margin = Inches(0.9)
sec.bottom_margin = Inches(0.9)


def shade(paragraph, hex_fill):
    pPr = paragraph._p.get_or_add_pPr()
    sh = OxmlElement("w:shd")
    sh.set(qn("w:val"), "clear")
    sh.set(qn("w:color"), "auto")
    sh.set(qn("w:fill"), hex_fill)
    pPr.append(sh)


def border(paragraph, color="2A9D8F", size="18", left=True):
    pPr = paragraph._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    side = "left" if left else "top"
    b = OxmlElement(f"w:{side}")
    b.set(qn("w:val"), "single")
    b.set(qn("w:sz"), size)
    b.set(qn("w:space"), "8")
    b.set(qn("w:color"), color)
    pbdr.append(b)
    pPr.append(pbdr)


def para(text="", size=11, bold=False, italic=False, color=INK, before=2,
         after=4, align=None, indent=None, font="Calibri"):
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    if indent is not None:
        p.paragraph_format.left_indent = Inches(indent)
    if text:
        r = p.add_run(text)
        r.font.size = Pt(size)
        r.font.bold = bold
        r.font.italic = italic
        r.font.color.rgb = color
        r.font.name = font
    return p


def runs_para(runs, size=11, before=2, after=4, indent=None, align=None):
    """runs: list of (text, dict)."""
    p = doc.add_paragraph()
    if align:
        p.alignment = align
    p.paragraph_format.space_before = Pt(before)
    p.paragraph_format.space_after = Pt(after)
    if indent is not None:
        p.paragraph_format.left_indent = Inches(indent)
    for text, ov in runs:
        r = p.add_run(text)
        r.font.size = Pt(ov.get("size", size))
        r.font.bold = ov.get("bold", False)
        r.font.italic = ov.get("italic", False)
        r.font.color.rgb = ov.get("color", INK)
    return p


def bullet(text, size=11, indent=0.35, bold_lead=None):
    p = doc.add_paragraph(style="List Bullet")
    p.paragraph_format.left_indent = Inches(indent)
    p.paragraph_format.space_after = Pt(3)
    if bold_lead:
        r = p.add_run(bold_lead)
        r.font.bold = True
        r.font.size = Pt(size)
    r = p.add_run(text)
    r.font.size = Pt(size)
    return p


def numbered(text, size=11, indent=0.35):
    p = doc.add_paragraph(style="List Number")
    p.paragraph_format.left_indent = Inches(indent)
    p.paragraph_format.space_after = Pt(3)
    r = p.add_run(text)
    r.font.size = Pt(size)
    return p


def label(text, color=TEAL):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(8)
    p.paragraph_format.space_after = Pt(2)
    r = p.add_run(text.upper())
    r.font.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = color
    r.font.name = "Calibri"
    # letter spacing
    return p


def example_block(text):
    p = doc.add_paragraph()
    p.paragraph_format.left_indent = Inches(0.3)
    p.paragraph_format.space_before = Pt(3)
    p.paragraph_format.space_after = Pt(4)
    shade(p, "FBEEE9")
    border(p, color="C05338")
    r = p.add_run("Example:  ")
    r.font.bold = True
    r.font.size = Pt(10.5)
    r.font.color.rgb = CORAL
    r2 = p.add_run(text)
    r2.font.italic = True
    r2.font.size = Pt(10.5)


def notes_block(text):
    label("Speaker notes", MUTED)
    for chunk in text:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.12)
        p.paragraph_format.space_after = Pt(5)
        border(p, color="B7C4C9")
        r = p.add_run(chunk)
        r.font.size = Pt(10.5)
        r.font.color.rgb = RGBColor(0x33, 0x40, 0x46)


def answer_block(items):
    label("Answer key", GREEN)
    for it in items:
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.12)
        p.paragraph_format.space_after = Pt(4)
        shade(p, "E9F5EC")
        border(p, color="1E7A33")
        if isinstance(it, tuple):
            lead, rest = it
            r = p.add_run(lead)
            r.font.bold = True
            r.font.size = Pt(10.5)
            r.font.color.rgb = GREEN
            r2 = p.add_run(rest)
            r2.font.size = Pt(10.5)
        else:
            r = p.add_run(it)
            r.font.size = Pt(10.5)


def slide_heading(num, title):
    p = doc.add_paragraph()
    p.paragraph_format.space_before = Pt(16)
    p.paragraph_format.space_after = Pt(2)
    pPr = p._p.get_or_add_pPr()
    pbdr = OxmlElement("w:pBdr")
    b = OxmlElement("w:bottom")
    b.set(qn("w:val"), "single"); b.set(qn("w:sz"), "6")
    b.set(qn("w:space"), "3"); b.set(qn("w:color"), "0F4C5C")
    pbdr.append(b); pPr.append(pbdr)
    r = p.add_run(f"Slide {num}")
    r.font.bold = True; r.font.size = Pt(15); r.font.color.rgb = TEAL
    r2 = p.add_run("   " + title)
    r2.font.bold = True; r2.font.size = Pt(15); r2.font.color.rgb = INK


def content_label():
    label("On-slide content", AQUA)



# ============================================================================
# TITLE
# ============================================================================
t = doc.add_paragraph()
t.paragraph_format.space_after = Pt(2)
r = t.add_run("Lecture 2: Research Ethics")
r.font.size = Pt(26); r.font.bold = True; r.font.color.rgb = TEAL
st = doc.add_paragraph()
st.paragraph_format.space_after = Pt(2)
r = st.add_run("Slide-by-Slide Script & Activity Answer Key")
r.font.size = Pt(14); r.font.italic = True; r.font.color.rgb = MUTED
para("Target competencies:  9 — apply ethical standards in all stages of the "
     "research process   |   10 — demonstrate proper citation of sources",
     size=10.5, color=MUTED, before=6, after=1)
para("Audience:  Grade 12 STEM, Senior High School", size=10.5, color=MUTED,
     after=1)
para("Recurring case study:  The Barangay Water Filter Project (instructor-"
     "created). Textbook material is from Creswell & Creswell (2023), Research "
     "Design, Ch. 4. Examples not from the textbook are instructor-created.",
     size=10.5, color=MUTED, after=2)

# How to read
label("How to use this document", TEAL)
para("Each entry below gives the exact on-slide content students see, followed "
     "by the speaker notes (the teaching script). The seven activity slides "
     "(5, 11, 16, 20, 23, 26, 27) also include a green Answer Key.", size=10.5)

SLIDES = []

# ---- Slide 1 ----
SLIDES.append(dict(
    num=1, title="A Filter, A Village, A Dilemma",
    content=[
        ("p", "Grade 12 researchers want to test a homemade water filter in a "
              "rural barangay. Before they collect a single drop of water, they "
              "face questions no data can answer for them:"),
        ("b", "Who gets to decide if the community participates?"),
        ("b", "What happens if the filter doesn't work — do they still report that?"),
        ("b", "What if their filter design looks a lot like someone else's?"),
        ("i", "This is where research ethics begins — before the \u201cresearch\u201d "
              "even starts."),
    ],
    notes=["Open with this scenario cold — don't define anything yet. The goal "
           "is to let students feel the tension in the questions before you hand "
           "them vocabulary. Ask the class: \u201cWhat could go wrong here, even "
           "if the science is done perfectly?\u201d Let a few students answer.",
           "The point you're building toward is that good science and ethical "
           "science are not automatically the same thing — you can run a flawless "
           "experiment and still cause harm, deceive people, or take credit "
           "unfairly. Do not resolve any of the three bullet questions yet; tell "
           "students you'll return to this exact scenario throughout the lesson."],
))

# ---- Slide 2 ----
SLIDES.append(dict(
    num=2, title="Ethics Is Not One Checklist Item",
    content=[
        ("b", "Many students think \u201cethics\u201d is something you check once, "
              "at the start of a study."),
        ("b", "In reality, research ethics applies continuously — at every stage "
              "of the research process."),
        ("p", "Planning  \u2192  Beginning the Study  \u2192  Collecting Data  \u2192  "
              "Analyzing Data  \u2192  Reporting Results"),
        ("i", "Every one of these five stages has its own ethical questions."),
    ],
    notes=["This slide reframes a term students already met briefly in Lecture 1 "
           "(when weighing \u201cethical, social, and environmental factors\u201d "
           "for a proposal). Make clear that ethics isn't a single feasibility "
           "checkbox — it's a standard re-applied at every single stage.",
           "This flowchart previews the structure you'll return to later (Slides "
           "12\u201316), so tell students explicitly: \u201cKeep this five-stage "
           "map in your head — we're going to walk through each one.\u201d This is "
           "a structural anchor, not a topic to dwell on yet."],
))

# ---- Slide 3 ----
SLIDES.append(dict(
    num=3, title="Defining Research Ethics",
    content=[
        ("p", "Research ethics — the standards and principles that guide "
              "responsible and trustworthy conduct throughout a research study."),
        ("p", "Research ethics exists because research almost always involves:"),
        ("b", "Collecting data from or about people"),
        ("b", "Working within real communities and environments"),
        ("b", "Producing findings that others will rely on"),
        ("i", "Where there are people and consequences, there are ethical "
              "responsibilities."),
    ],
    notes=["Give students a clean, quotable definition here — this is the term "
           "they'll be tested on, so it should be crisp and memorable. Emphasize "
           "the why embedded in it: ethics exists specifically because research "
           "affects real people and real outcomes.",
           "Tie it back to Slide 1: the water-filter researchers deal with real "
           "households whose water safety may depend on accurate, honest results. "
           "Note the connection to Lecture 1's \u201cbasic steps in the research "
           "process\u201d — ethics governs how each step is carried out."],
))

# ---- Slide 4 ----
SLIDES.append(dict(
    num=4, title="Why Research Ethics Matters",
    content=[
        ("p", "Research ethics protects three things at once:"),
        ("b", "The Participants — prevents harm, exploitation, and disrespect "
              "toward the people involved in a study."),
        ("b", "The Findings — keeps results honest and trustworthy, not distorted "
              "by bias or dishonesty."),
        ("b", "The Researcher's Credibility — protects the researcher's (and their "
              "institution's) reputation for integrity."),
    ],
    notes=["Walk through each using the water-filter scenario: mislead a "
           "household about how their data will be used and you harm a "
           "participant; report only favorable results and you compromise the "
           "findings; if either comes to light, it damages the researcher's "
           "credibility for future work.",
           "Emphasize that the three protections are interconnected — a violation "
           "in one almost always damages the others. This slide answers "
           "\u201cwhy should I care?\u201d before the specific standards."],
))

# ---- Slide 5 (activity) ----
SLIDES.append(dict(
    num=5, title="Who Could Be Affected?  (Activity)",
    content=[
        ("p", "Apply it: Return to the Barangay Water Filter Project. For each "
              "group below, identify one specific way research ethics protects them:"),
        ("n", "The households whose water is being tested"),
        ("n", "The barangay as a whole community"),
        ("n", "The original designer of the earlier filter"),
        ("n", "Future readers who might rely on this research"),
        ("i", "Discuss in pairs, then share with the class."),
    ],
    notes=["This is the lesson's first \u201capply it\u201d moment — resist giving "
           "answers immediately. Let pairs work all four prompts for 3\u20134 "
           "minutes. Students usually get #1 (participants) and #2 (community) "
           "easily; #3 (crediting the earlier researcher) and #4 (future readers) "
           "are harder this early — that's fine, since citation and honest "
           "reporting haven't been formally introduced.",
           "Use the gap productively: tell students \u201cwe'll come back to #3 "
           "and #4 later in this lesson\u201d to build anticipation."],
    answers=[
        ("1. Households — ", "informed consent and confidentiality: they must know "
         "their water is being tested and agree to it, and their identities must "
         "be protected in any report (avoiding harm / respect)."),
        ("2. The barangay community — ", "avoiding harm: the study must not disrupt "
         "shared water access or raise false hope, and should aim to genuinely "
         "benefit the community."),
        ("3. The original filter designer — ", "honesty & proper credit: their "
         "earlier design must be acknowledged/cited, not passed off as original "
         "(this previews the citation section)."),
        ("4. Future readers — ", "honest, accurate reporting: they rely on truthful, "
         "complete results and verifiable sources to build on this work."),
        "Note: #3 and #4 are meant to be hard here — they set up the plagiarism "
        "and citation section later in the lecture.",
    ],
))

# ---- Slide 6 ----
SLIDES.append(dict(
    num=6, title="Four Core Ethical Standards",
    content=[
        ("b", "Honesty & Integrity — reporting data and findings truthfully, "
              "without fabrication."),
        ("b", "Respect for Participants — informing people they are part of a "
              "study and getting their agreement to participate."),
        ("b", "Confidentiality & Privacy — protecting the identity and personal "
              "information of participants."),
        ("b", "Avoiding Harm — preventing physical, social, or emotional harm to "
              "people, communities, and the environment."),
    ],
    notes=["This is the \u201ctable of contents\u201d slide for the next four "
           "concept slides — introduce all four briefly, then go deeper one at a "
           "time. Students don't need to memorize the exact wording yet.",
           "The four principles map onto what professional research communities "
           "across fields (health, social science, engineering) treat as baseline "
           "standards — you're teaching the shared core, not one field's code."],
))

# ---- Slide 7 ----
SLIDES.append(dict(
    num=7, title="Honesty and Integrity in Reporting",
    content=[
        ("p", "Honesty and integrity mean reporting exactly what the data shows — "
              "never inventing, altering, or selectively hiding results. This "
              "includes:"),
        ("b", "Never falsifying data, findings, or conclusions (Creswell & "
              "Creswell, 2023)."),
        ("b", "Reporting results honestly, even when they're disappointing or "
              "unexpected."),
        ("e", "If the water filter only reduces bacteria by 40% instead of the "
              "hoped-for 90%, the honest researcher reports 40% — not a rounded-up, "
              "more impressive number."),
    ],
    notes=["Honesty is usually the easiest of the four principles to grasp, so "
           "move through the definition quickly and spend more time on the "
           "example. Stress that dishonesty isn't always dramatic fabrication — "
           "it's often subtler: rounding favorably, dropping an inconvenient data "
           "point, overstating certainty.",
           "Ask: \u201cWhy might a researcher feel tempted to round up a "
           "disappointing result?\u201d This surfaces the human pressure (wanting "
           "your project to \u201csucceed\u201d) that makes the standard necessary."],
))

# ---- Slide 8 ----
SLIDES.append(dict(
    num=8, title="Respecting Participants and Consent",
    content=[
        ("p", "Respect for participants means people must:"),
        ("b", "Know they are part of a study (its purpose is disclosed, not hidden)."),
        ("b", "Voluntarily agree to take part — never pressured or misled."),
        ("e", "Before collecting a single water sample, the researchers explain to "
              "each household what the study is for, what will be done with their "
              "water, and confirm the household agrees to participate."),
    ],
    notes=["Keep this deliberately simple and plain-language — students don't need "
           "formal consent forms or IRB procedures at this level; they need the "
           "principle of voluntary, informed participation.",
           "Contrast the example with a violation: quietly testing a household's "
           "water without telling them, or implying participation is mandatory. "
           "Note that \u201crespect\u201d here is really honesty aimed outward at "
           "people rather than at the data."],
))

# ---- Slide 9 ----
SLIDES.append(dict(
    num=9, title="Confidentiality and Privacy",
    content=[
        ("p", "Confidentiality and privacy mean protecting participants' "
              "identities and personal information when reporting results. Common "
              "strategies:"),
        ("b", "Using pseudonyms or aliases instead of real names."),
        ("b", "Separating names from responses when recording data (Creswell & "
              "Creswell, 2023)."),
        ("e", "Instead of writing \u201cHousehold of Mrs. Santos reported the water "
              "tastes better,\u201d the report says \u201cHousehold 3 reported the "
              "water tastes better.\u201d"),
    ],
    notes=["This often gets confused with \u201cavoiding harm\u201d (next slide) — "
           "clarify directly: confidentiality is specifically about identity "
           "protection, while avoiding harm is broader.",
           "Ask: \u201cWhy would a household care if their name appears in a public "
           "report, even if the finding is positive?\u201d This shows privacy "
           "matters regardless of whether the information seems sensitive."],
))

# ---- Slide 10 ----
SLIDES.append(dict(
    num=10, title="Avoiding Harm to People and Place",
    content=[
        ("p", "Avoiding harm means protecting participants, the community, and the "
              "environment from negative effects of the research itself. This "
              "includes:"),
        ("b", "Not deceiving or exploiting participants (Creswell & Creswell, 2023)."),
        ("b", "Minimizing disruption to the research site."),
        ("b", "Considering effects on the surrounding community and environment."),
        ("e", "If the researchers' water sampling disrupts the community's daily "
              "access to the well, or if a \u201cfailed\u201d filter is left "
              "installed and mistakenly trusted by residents, real harm has "
              "occurred — separate from whether the data was reported honestly."),
    ],
    notes=["This is the broadest principle, so anchor it with the example — the "
           "\u201cfailed filter left installed\u201d detail matters because harm "
           "can happen even after data collection ends, purely through the "
           "physical consequences of the research existing in a real place.",
           "Ask students to brainstorm one more way the study could unintentionally "
           "harm the community (e.g., taking residents' time repeatedly, raising "
           "false hope). This is where research most visibly touches the "
           "environment, since the water source is the site of study."],
))

# ---- Slide 11 (activity) ----
SLIDES.append(dict(
    num=11, title="Ethical Standards Decision Tree  (Activity)",
    content=[
        ("p", "Apply it: For each mini-scenario, decide which of the four standards "
              "is most directly at risk — Honesty, Respect, Confidentiality, or "
              "Avoiding Harm."),
        ("n", "A researcher tests water without telling the household."),
        ("n", "A report lists a participant's full name and address."),
        ("n", "A researcher only publishes the filter's best-performing test result."),
        ("n", "Repeated data collection visits leave a household without well "
              "access for hours each time."),
    ],
    notes=["This is the consolidation activity for the four standards — resist "
           "explaining until students attempt all four matches.",
           "Some students may reasonably argue overlaps (e.g., #1 could also touch "
           "avoiding harm). Use that as a teaching moment: violations often "
           "overlap, but naming the primary standard at risk builds precision. "
           "Keep this to about 5 minutes."],
    answers=[
        ("1  \u2192  Respect for Participants  ", "— testing without telling the "
         "household violates informed, voluntary participation."),
        ("2  \u2192  Confidentiality & Privacy  ", "— publishing a name and address "
         "exposes the participant's identity."),
        ("3  \u2192  Honesty & Integrity  ", "— publishing only the best result is "
         "selective, misleading reporting."),
        ("4  \u2192  Avoiding Harm  ", "— repeatedly cutting off well access harms "
         "the household and community."),
    ],
))

# ---- Slide 12 ----
SLIDES.append(dict(
    num=12, title="Ethics During the Planning Stage",
    content=[
        ("p", "(Five-stage flowchart reappears with \u201cPlanning\u201d highlighted.)"),
        ("p", "At the planning stage, ethical research means:"),
        ("b", "Choosing a research problem responsibly — one that could genuinely "
              "benefit participants, not just satisfy curiosity (Creswell & "
              "Creswell, 2023)."),
        ("b", "Considering, before data collection ever begins, who might be "
              "affected and how."),
        ("e", "Choosing to test a low-cost filter because the community lacks "
              "access to safe water is a responsibly chosen problem — testing it "
              "purely because it's a \u201cconvenient\u201d barangay near the "
              "school, with no real community benefit in mind, is not."),
    ],
    notes=["This begins the second major arc — walking through the five-stage "
           "flowchart in detail, one stage per slide. Reintroducing the same "
           "graphic (Planning highlighted) shows students where they are.",
           "The key idea is intentionality: ethical planning isn't passive; it "
           "requires actively asking \u201cwho benefits from this research, and "
           "could this topic cause harm before I've even started?\u201d"],
))

# ---- Slide 13 ----
SLIDES.append(dict(
    num=13, title="Ethics During Data Collection",
    content=[
        ("p", "(Flowchart reappears with \u201cCollecting Data\u201d highlighted.)"),
        ("p", "At the data collection stage, ethical research means:"),
        ("b", "Being honest with participants about what is happening and why."),
        ("b", "Never pressuring or coercing participation (Creswell & Creswell, 2023)."),
        ("b", "Never fabricating data that wasn't actually collected."),
        ("e", "If a household declines to have their well water sampled, the "
              "researchers must respect that decision — inventing a data point for "
              "that household to \u201ccomplete the set\u201d would be a serious "
              "ethical violation."),
    ],
    notes=["This revisits honesty and respect (Slides 7\u20138) applied to the "
           "action of collecting data. The repetition is intentional — the same "
           "standards recur across stages, which is the core idea of the lecture.",
           "Dwell on the fabrication example: ask why a researcher under time "
           "pressure might \u201cfill in\u201d a missing data point, and why that "
           "differs fundamentally from honestly reporting an incomplete dataset."],
))

# ---- Slide 14 ----
SLIDES.append(dict(
    num=14, title="Ethics During Data Analysis",
    content=[
        ("p", "(Flowchart reappears with \u201cAnalyzing Data\u201d highlighted.)"),
        ("p", "At the data analysis stage, ethical research means:"),
        ("b", "Avoiding taking sides — not favoring results that make participants "
              "or the researcher look good (Creswell & Creswell, 2023)."),
        ("b", "Reporting the full range of results, including unexpected or "
              "contrary findings."),
        ("e", "If 7 out of 10 households show improved water quality but 3 show no "
              "change, the researchers must report all 10 results — not just the 7 "
              "that support their hypothesis."),
    ],
    notes=["This is where honesty (Slide 7) becomes most concrete and testable — "
           "students can see selective reporting using real numbers.",
           "Ask: \u201cIf only 3 of 10 households improved, how would you feel "
           "about reporting that?\u201d Surface the emotional pull toward "
           "dishonesty, then state plainly that an honestly reported \u201cmixed\u201d "
           "result is not a failure — it's good research."],
))

# ---- Slide 15 ----
SLIDES.append(dict(
    num=15, title="Ethics During Reporting and Writing",
    content=[
        ("p", "(Flowchart reappears with \u201cReporting\u201d highlighted.)"),
        ("p", "At the reporting stage, ethical research means:"),
        ("b", "Communicating findings honestly and clearly."),
        ("b", "Giving proper credit to the ideas and words of others (Creswell & "
              "Creswell, 2023)."),
        ("i", "That second point — giving credit — is its own major skill. It's "
              "coming up next."),
    ],
    notes=["This is the pivot slide of the whole lecture — deliver it with a clear "
           "tonal shift to signal a new (but connected) topic. Don't elaborate on "
           "\u201cgiving credit\u201d beyond this one line.",
           "The goal is continuity: citation isn't a skill bolted onto ethics — "
           "it's simply what honest reporting requires when your work builds on "
           "someone else's, echoing the earlier filter design from Slide 1."],
))

# ---- Slide 16 (activity) ----
SLIDES.append(dict(
    num=16, title="Trace the Stages  (Activity)",
    content=[
        ("p", "Apply it: Sort each researcher action into the correct stage — "
              "Planning, Collecting, Analyzing, or Reporting."),
        ("n", "Deciding to study the barangay because they genuinely lack safe "
              "water access."),
        ("n", "Recording a water sample result exactly as measured, even though "
              "it's disappointing."),
        ("n", "Including both improved and unchanged households in the final "
              "results."),
        ("n", "Properly acknowledging the earlier filter design that inspired "
              "their own."),
    ],
    notes=["This is the consolidation activity for the whole \u201cstages\u201d "
           "section (Slides 12\u201315). Students place each action on the correct "
           "stage of the flowchart.",
           "Item 4 deliberately foreshadows the citation section without teaching "
           "it yet — if students struggle to explain why it belongs at reporting, "
           "that's expected; confirm it's coming up next."],
    answers=[
        ("1  \u2192  Planning  ", "— choosing the research problem responsibly."),
        ("2  \u2192  Collecting Data  ", "— honestly recording what was measured."),
        ("3  \u2192  Analyzing Data  ", "— reporting the full range of results."),
        ("4  \u2192  Reporting  ", "— giving proper credit / citing the earlier "
         "design (previews the citation half of the lecture)."),
    ],
))

# ---- Slide 17 ----
SLIDES.append(dict(
    num=17, title="What Counts as Plagiarism",
    content=[
        ("p", "Plagiarism — presenting someone else's work, ideas, or words as "
              "your own, without giving them credit (Creswell & Creswell, 2023)."),
        ("p", "Plagiarism is not just a rule — it's an ethics violation. It breaks "
              "the same standard of honesty and integrity from earlier in this "
              "lesson."),
        ("e", "If the researchers build their filter using the earlier student's "
              "design but never mention that design in their report, readers are "
              "misled into thinking the design is original — that's plagiarism."),
    ],
    notes=["The most important move here is framing — students often think of "
           "plagiarism as a school-specific \u201crule\u201d disconnected from real "
           "ethics.",
           "Connect it back to Slide 7's Honesty & Integrity: taking credit for "
           "someone else's work is dishonesty, just aimed at ideas instead of "
           "data. This reframe makes the citation mechanics that follow feel "
           "meaningful rather than arbitrary."],
))

# ---- Slide 18 ----
SLIDES.append(dict(
    num=18, title="Two Forms of Plagiarism",
    content=[
        ("b", "Direct Plagiarism — copying someone else's exact words without "
              "credit. Even one sentence, word-for-word, without credit counts."),
        ("b", "Uncredited Paraphrasing — restating someone else's idea in your own "
              "words, but still without giving credit. Changing the wording "
              "doesn't remove the need to cite the original idea."),
    ],
    notes=["Most students already know copy-paste plagiarism is wrong; the harder "
           "concept — worth more time — is uncredited paraphrasing. Many genuinely "
           "believe rewording removes the need to cite.",
           "Correct this directly: the idea still originated with someone else, so "
           "credit is still owed even if not a single word is copied. This sets up "
           "why citation applies to paraphrased material, not just direct quotes."],
))

# ---- Slide 19 ----
SLIDES.append(dict(
    num=19, title="Why We Cite Sources",
    content=[
        ("p", "Citation exists for three connected reasons:"),
        ("n", "Giving credit — acknowledging whose idea or words you used."),
        ("n", "Enabling verification — letting readers check your sources for "
              "themselves."),
        ("n", "Joining the conversation — showing how your work connects to "
              "existing knowledge."),
        ("i", "Citation isn't a punishment for \u201calmost plagiarizing\u201d — "
              "it's how honest research is supposed to work."),
    ],
    notes=["This answers the question students silently ask: \u201cWhy does this "
           "matter if I'm not trying to steal anything?\u201d Reframe citation as "
           "a positive practice, not a defensive one — it's how all researchers "
           "build on each other's work.",
           "Use the water-filter example once more: citing the earlier student's "
           "design doesn't weaken the new work — it strengthens the researchers' "
           "credibility by showing a legitimate foundation."],
))

# ---- Slide 20 (activity) ----
SLIDES.append(dict(
    num=20, title="Plagiarism or Proper Credit?  (Activity)",
    content=[
        ("p", "Apply it: Which version properly credits the source?"),
        ("p", "Version A:  \u201cCoconut husk charcoal can effectively filter "
              "bacteria from contaminated water.\u201d"),
        ("p", "Version B:  \u201cAccording to Reyes (2022), coconut husk charcoal "
              "can effectively filter bacteria from contaminated water.\u201d"),
        ("i", "Which version avoids plagiarism? What's missing from the other?"),
    ],
    notes=["This should feel almost too simple by now — that's intentional; it "
           "confirms students internalized the core idea before adding citation "
           "mechanics.",
           "Preview: \u201cVersion B shows an in-text citation — next, we'll learn "
           "exactly how to build one properly.\u201d A natural, low-key transition."],
    answers=[
        ("Version B is correct.  ", "It names the source of the idea with an "
         "in-text citation \u2014 (Reyes, 2022)."),
        ("Version A is plagiarism.  ", "It presents the same claim as if it were "
         "the researchers' own original finding; the citation of the source is "
         "missing."),
        "Because Version B paraphrases (no direct quote), author + year is enough "
        "\u2014 no page number is required.",
    ],
))

# ---- Slide 21 ----
SLIDES.append(dict(
    num=21, title="Two Parts of Every Citation",
    content=[
        ("p", "Every complete citation has two connected parts:"),
        ("b", "In-Text Citation — a short note within your writing, pointing to a "
              "source.  Example: (Reyes, 2022)."),
        ("b", "Reference List Entry — a full entry at the end of your paper, "
              "giving complete source details."),
        ("i", "The short note in your text always has a matching full entry at the "
              "end."),
    ],
    notes=["Establish the two-part structure before diving into either part — "
           "they're not two separate skills, but two halves of the same citation.",
           "Analogy: the in-text citation is like a claim ticket, and the reference "
           "list entry is what you get when you redeem it — full details live only "
           "in the reference list, so the in-text note only needs to point there."],
))

# ---- Slide 22 ----
SLIDES.append(dict(
    num=22, title="APA In-Text Citations",
    content=[
        ("p", "This course uses APA (American Psychological Association) style for "
              "all citations."),
        ("p", "APA in-text citation format:  (Author's Last Name, Year)"),
        ("b", "Paraphrased idea:  Coconut husk charcoal has shown filtering "
              "potential in prior designs (Reyes, 2022)."),
        ("b", "Direct quote (add page number):  Reyes (2022) found the design "
              "\u201creduced bacterial presence by over 60%\u201d (p. 14)."),
    ],
    notes=["Keep the focus tightly on the author-date format — introducing other "
           "styles now would only confuse (that comparison is for later "
           "coursework).",
           "Point out the difference: a paraphrase needs only (Author, Year), while "
           "a direct quote also needs a page number because you're pointing to the "
           "source's exact wording. Have students note that Slide 20's Version B "
           "was a paraphrase, so no page number was needed."],
))

# ---- Slide 23 (activity) ----
SLIDES.append(dict(
    num=23, title="Practice In-Text Citations  (Activity)",
    content=[
        ("p", "Apply it: Add a properly formatted APA in-text citation to each "
              "sentence."),
        ("n", "A 2021 study by Dela Cruz found that sand filtration removes 80% of "
              "sediment.  (Paraphrase — write the citation.)"),
        ("n", "Dela Cruz's 2021 report stated the filter \u201csignificantly "
              "improved water clarity within 48 hours.\u201d  (Direct quote, page 9 "
              "— write the citation.)"),
    ],
    notes=["Give students two or three minutes to write both independently before "
           "reviewing as a class.",
           "Common errors to watch for: forgetting the comma between author and "
           "year; forgetting \u201cp.\u201d before the page number; or adding a "
           "page number to the paraphrase (unnecessary — only direct quotes need "
           "one). Correct these live."],
    answers=[
        ("1 (paraphrase):  ", "\u2026 sand filtration removes 80% of sediment "
         "(Dela Cruz, 2021)."),
        ("2 (direct quote):  ", "\u2026 \u201csignificantly improved water clarity "
         "within 48 hours\u201d (Dela Cruz, 2021, p. 9)."),
        "Key point: the paraphrase needs only (Author, Year); the direct quote "
        "also needs the page number.",
    ],
))

# ---- Slide 24 ----
SLIDES.append(dict(
    num=24, title="APA Reference List Basics",
    content=[
        ("p", "Every source type has a specific reference-list format. Three common "
              "types:"),
        ("b", "Book:  Author, A. A. (Year). Title of the work. Publisher."),
        ("b", "Journal Article:  Author, A. A. (Year). Title of the article. "
              "Journal Name, Volume(Issue), page range."),
        ("b", "Website:  Author, A. A. (Year, Month Day). Title of the page. Site "
              "Name. URL"),
    ],
    notes=["Present these as patterns to recognize, not to memorize by rote — "
           "students will look them up when writing. The goal is familiarity with "
           "the structure.",
           "Point out what stays constant: author and year always come first, "
           "matching the in-text citation. Only the middle changes — title "
           "formatting and source-specific details like journal name or URL."],
))

# ---- Slide 25 ----
SLIDES.append(dict(
    num=25, title="Sample APA Reference Entries",
    content=[
        ("b", "Book:  Santos, M. R. (2020). Water and community: Local solutions "
              "to global problems. Manila Press."),
        ("b", "Journal Article:  Reyes, J. P. (2022). Low-cost filtration using "
              "coconut husk charcoal. Philippine Journal of Environmental "
              "Engineering, 15(2), 45\u201358."),
        ("b", "Website:  Department of Science and Technology. (2023, March 4). "
              "Community water testing guidelines. DOST Philippines. "
              "https://www.dost.gov.ph"),
    ],
    notes=["This slide lets students see a complete, realistic reference list — not "
           "just abstract templates. Walk through each entry and have students "
           "point out author, year, title, and publisher/journal/site details.",
           "Good moment to note the italics convention: book and journal titles are "
           "italicized; article and webpage titles are not — a common slip."],
))

# ---- Slide 26 (activity) ----
SLIDES.append(dict(
    num=26, title="Build a Reference List  (Activity)",
    content=[
        ("p", "Apply it: Turn this source information into a properly formatted APA "
              "reference entry."),
        ("b", "Author: Dela Cruz, A."),
        ("b", "Year: 2021"),
        ("b", "Article title: Sand filtration effectiveness in rural water systems"),
        ("b", "Journal: Journal of Applied Environmental Science"),
        ("b", "Volume/Issue: 9(3)"),
        ("b", "Pages: 112\u2013120"),
    ],
    notes=["This is the culminating skills-practice slide for citation mechanics — "
           "students assemble a complete entry from raw, unordered information.",
           "Have a few students share answers, and use discrepancies (missing "
           "italics, wrong punctuation, misplaced year) as quick, low-stakes "
           "corrections."],
    answers=[
        ("Correct entry:  ", "Dela Cruz, A. (2021). Sand filtration effectiveness "
         "in rural water systems. Journal of Applied Environmental Science, 9(3), "
         "112\u2013120."),
        "Formatting reminders: the journal name and volume number are italicized; "
        "the article title is not; author and year come first; end with the page "
        "range.",
    ],
))

# ---- Slide 27 (activity) ----
SLIDES.append(dict(
    num=27, title="Full Ethics and Citation Audit  (Activity)",
    content=[
        ("p", "Apply it — one last time: The Barangay Water Filter researchers are "
              "ready to submit their final report. Audit their draft against "
              "everything covered today:"),
        ("b", "Did they honestly report all results, not just favorable ones?"),
        ("b", "Did participating households know about and agree to the study?"),
        ("b", "Are household identities protected in the report?"),
        ("b", "Was the research conducted without unnecessary harm to people or "
              "place?"),
        ("b", "Is the earlier filter design properly cited — both in-text and in "
              "the reference list?"),
        ("i", "If every box can be checked, the research is both scientifically "
              "sound and ethically sound."),
    ],
    notes=["Close by returning to the exact scenario from Slide 1, now fully "
           "resolved through everything students learned — this bookends the "
           "lesson without new content.",
           "Work through the checklist as a class, calling back to where each item "
           "was covered. End on the throughline: ethical research and well-cited "
           "research aren't two separate obligations — both come from the same "
           "commitment to honesty and respect for others' contributions."],
    answers=[
        ("Honesty of results  ", "\u2014 covered on Slide 7 (Honesty & Integrity) "
         "and Slide 14 (report the full range of results)."),
        ("Knew about & agreed to the study  ", "\u2014 Slide 8 (Respect / informed, "
         "voluntary consent)."),
        ("Identities protected  ", "\u2014 Slide 9 (Confidentiality & Privacy; use "
         "\u201cHousehold 3,\u201d not real names)."),
        ("No unnecessary harm  ", "\u2014 Slide 10 (Avoiding Harm to people, "
         "community, and environment)."),
        ("Earlier design cited  ", "\u2014 Slides 17\u201326 (plagiarism, in-text "
         "citation, and reference-list entry)."),
        "Ideal outcome: all five boxes checked \u2014 the study is then both "
        "scientifically sound and ethically sound.",
    ],
))

# ============================================================================
# RENDER SLIDES
# ============================================================================
kinds = {"p": None, "b": None, "i": None, "n": None, "e": None}
for sl in SLIDES:
    slide_heading(sl["num"], sl["title"])
    content_label()
    for kind, text in sl["content"]:
        if kind == "p":
            para(text, size=11, after=4)
        elif kind == "b":
            bullet(text)
        elif kind == "n":
            numbered(text)
        elif kind == "i":
            para(text, size=11, italic=True, color=TEAL, before=3)
        elif kind == "e":
            example_block(text)
    if sl.get("answers"):
        answer_block(sl["answers"])
    notes_block(sl["notes"])

# ---- Appendix ----
slide_heading("A", "Appendix: Slide-to-Competency Alignment")
content_label()
for rng, focus in [
        ("Slides 1\u20135", "Foundation: what research ethics is and why it matters (Comp. 9)"),
        ("Slides 6\u201311", "The four core ethical standards (Comp. 9)"),
        ("Slides 12\u201316", "Applying ethics across all stages of the research process (Comp. 9)"),
        ("Slides 17\u201320", "Plagiarism as the ethical bridge into citation (Comp. 9 \u2192 10)"),
        ("Slides 21\u201326", "APA citation mechanics — in-text and reference list (Comp. 10)"),
        ("Slide 27", "Integrated ethics + citation application (Comp. 9 & 10)")]:
    bullet(focus, bold_lead=rng + " — ")

out = "/projects/sandbox/physics/Lecture2-Research-Ethics-Script.docx"
doc.save(out)
print("Saved", out)
