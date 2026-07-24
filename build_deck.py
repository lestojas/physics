# -*- coding: utf-8 -*-
import re
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
import deck_engine as E

TEMPLATE = "1 Physics 1_Physical Quantities & SI Units.pptx"
OUT = "Projectile and Circular Motion.pptx"
A = "assets"

# segment shortcuts
t  = lambda s: ("t", s)
b  = lambda s: ("b", s)
it = lambda s: ("i", s)
var = lambda s: ("var", s)
sub = lambda s: ("sub", s)
sup = lambda s: ("sup", s)

# ---- equations ----
EQ_S4 = [[var('v'), sub('x'), t('  =  '), var('v'), sub('i'), t(' cos '), var('θ'), sub('i'),
          t('          '),
          var('v'), sub('y'), t('  =  '), var('v'), sub('i'), t(' sin '), var('θ'), sub('i')]]
EQ_S9 = [[var('h'), t('  =  '), var('v'), sub('i'), sup('2'), t(' sin'), sup('2'), var('θ'), sub('i'),
          t('  /  2'), var('g'),
          t('           '),
          var('R'), t('  =  '), var('v'), sub('i'), sup('2'), t(' sin 2'), var('θ'), sub('i'),
          t('  /  '), var('g')]]
EQ_S18 = [[var('a'), sub('c'), t('  =  '), var('v'), sup('2'), t('  /  '), var('r')]]
EQ_S19 = [[var('T'), t('  =  2π'), var('r'), t('  /  '), var('v')]]
EQ_FC = [[var('F'), sub('c'), t('  =  '), var('m'), var('v'), sup('2'), t('  /  '), var('r')]]

# slide-7 equation cells
C_X = [var('x'), sub('f'), t(' = '), var('x'), sub('i'), t(' + '), var('v'), sub('xi'), var('t')]
C_Y = [var('y'), sub('f'), t(' = '), var('y'), sub('i'), t(' + '), var('v'), sub('yi'), var('t'),
       t(' \u2013 \u00bd'), var('g'), var('t'), sup('2')]
C_VYF = [var('v'), sub('yf'), t(' = '), var('v'), sub('yi'), t(' \u2013 '), var('g'), var('t')]
C_ACC = [t('constant acceleration,  '), var('a'), t(' = \u2013'), var('g')]


def strip_md(s):
    s = s.replace("***", "").replace("**", "").replace("*", "")
    return s


# =====================================================================
prs = Presentation(TEMPLATE)
base = prs.slides[3]                 # content template slide
orig_ids = list(prs.slides._sldIdLst)   # 10 originals (0..9)

# ---------------------------------------------------------------- cover
cover = prs.slides[0]
tb2 = E.find_shape(cover, "TextBox 2")   # 'Physics 1'
tb13 = E.find_shape(cover, "TextBox 13")  # 'Prepared by ...'
# reposition course tag top-left
tb2.left = Inches(0.7); tb2.top = Inches(0.45)
tb2.width = Inches(6.0); tb2.height = Inches(0.5)
# big lecture title in lower white band
title = cover.shapes.add_textbox(Inches(0.7), Inches(5.55), Inches(11.9), Inches(0.9))
tf = title.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; E.no_bullet(p)
r = p.add_run(); r.text = "Projectile & Circular Motion"
r.font.name = E.FONT_BOLD; r.font.size = Pt(38); r.font.bold = True
r.font.color.rgb = E.TITLE_CLR
sub_tb = cover.shapes.add_textbox(Inches(0.7), Inches(6.33), Inches(11.9), Inches(0.5))
tf = sub_tb.text_frame; tf.word_wrap = True
p = tf.paragraphs[0]; p.alignment = PP_ALIGN.CENTER; E.no_bullet(p)
r = p.add_run(); r.text = "Motion in Two Dimensions  \u2014  A First-Hand Investigation"
r.font.name = E.FONT; r.font.size = Pt(18); r.font.italic = True
r.font.color.rgb = E.GREY
# move author line to bottom center
tb13.left = Inches(0.7); tb13.top = Inches(6.78)
tb13.width = Inches(11.9); tb13.height = Inches(0.4)
for para in tb13.text_frame.paragraphs:
    para.alignment = PP_ALIGN.CENTER


# ---------------------------------------------------------------- helper
def new_slide(title_text, notes):
    s = E.duplicate_slide(prs, base)
    E.set_title(s, title_text)
    E.remove_body(s)
    E.set_notes(s, strip_md(notes))
    return s


# ================================================================== S1
s = new_slide("Motion in Two Dimensions \u2014 Today's Target",
    "Frame the whole session as answering one question twice: \"why does this path curve, and what controls how much it curves?\" We'll answer it first for things that fly through the air, then for things that spin. By the end of the hour, students should be ready to physically test the second answer with their own hands.")
E.add_bullets(s, [
    "Today's competency, stated plainly: *carry out first-hand investigations involving 2-dimensional projectile and circular motion to investigate factors such as speed, radius, and centripetal force.*",
    "Two big ideas for the day, side by side:",
], E.CL, E.CT, E.CW, 1.4, size=18)
E.add_table(s, ["Projectile Motion", "Circular Motion"],
    [["A curved path caused by *gravity alone*", "A curved path caused by a *center-seeking pull*"],
     ["Speed and direction *both* change", "Speed stays constant, but *direction* constantly changes"]],
    E.CL, 3.35, E.CW, [5.9, 5.9], size=17, header_size=18, row_height=0.85,
    first_col_bold=False)

# ================================================================== S2
s = new_slide("The Shape Hiding in Plain Sight",
    "Open with the vivid images rather than the definition. Ask students what a diver's fall, welding sparks, and a fountain jet could possibly have in common - let them sit with that for a second before revealing it's the same geometric shape. This is the \"aha\" that should anchor the whole first half of the lesson: gravity writes the same signature every time.")
E.add_bullets(s, [
    "A diver leaving a cliff. Sparks flying off a welder's torch. Water arcing out of a park fountain.",
    "All three trace the *exact same curve* \u2014 even though nobody planned it that way.",
    "That curve has a name: the ***parabola***, and it shows up *any time* something launches into the air and gravity is the only thing acting on it afterward.",
], E.CL, E.CT, E.CW, 1.9, size=18)
E.add_image_fit(s, f"{A}/parabola_scenes.png", E.CL, 3.95, E.CW, 2.55, valign="top")

# ================================================================== S3
s = new_slide("Locating a Particle in Two Dimensions",
    "Keep this brief and conversational - students already have vector intuition from the prior unit. The key upgrade here is simultaneity: x and y aren't happening in sequence, they're happening together, at the same instant, for the same object.")
E.add_bullets(s, [
    "In *one* dimension, a single number tells you where something is.",
    "In *two* dimensions, you need **two numbers at once** \u2014 an *x*-position and a *y*-position \u2014 tracked *simultaneously*, not one after the other.",
    "This pair is bundled into a single arrow called the **position vector**, pointing from the origin to wherever the object currently is.",
], E.CL, E.CT + 0.5, E.CW, 3.6, size=22, gap=14)

# ================================================================== S4
s = new_slide("Breaking Velocity Into Two Directions",
    "This is a minimal decomposition - one vector, split into two pieces. Be explicit that this is not the full vector-addition unit students will get in a week; it's just enough trigonometry to separate one launch velocity into its horizontal and vertical \"ingredients.\"")
E.add_bullets(s, ["Any launch velocity can be split into two perpendicular ingredients:"],
              E.CL, E.CT, E.CW, 0.7, size=19)
E.add_equation(s, EQ_S4, 2.6, size=24, width=9.4)
E.add_bullets(s, [
    "Think of a cannon fired at an angle: part of its \"push\" sends the ball *forward*, part of it sends the ball *upward* \u2014 and *trigonometry* tells you exactly how much of each.",
    "This is the *only* piece of vector-splitting needed for today \u2014 no adding multiple vectors together yet (that's Aug 4's job).",
], E.CL, 4.15, E.CW, 2.3, size=18)

# ================================================================== S5
s = new_slide("The Independence Principle",
    "This is the air-hockey-puck thought experiment straight from the reference text. Walk through it slowly: the puck moves at constant velocity in x; a puff of air in y adds a y-velocity but the x-velocity is completely unaffected. That independence is what lets us solve horizontal and vertical motion as two separate, simpler problems instead of one tangled one.")
E.add_bullets(s, [
    "Picture a hockey puck gliding in a straight line across a frictionless table.",
    "Someone gives it a *single sideways puff of air*. The puck now drifts diagonally \u2014 but its *original* forward speed never changed one bit.",
    "The generalization: ***motion in two dimensions can be modeled as two independent motions in each of the two perpendicular directions*** \u2014 a nudge in *y* never touches what's happening in *x*, and vice versa.",
    "This is *the* single most important idea in projectile motion. Everything else today builds on it.",
], E.CL, E.CT, E.CW, 2.2, size=16, gap=5)
E.add_image_fit(s, f"{A}/independence.png", E.CL, 4.2, E.CW, 2.35, valign="top")

# ================================================================== S7
s = new_slide("The Governing Equations of Projectile Motion",
    "This slide is the payoff of Slide 5 - students now see the independence principle turned into an actual toolkit. Emphasize the problem-solving habit: horizontal motion is always the \"easy\" constant-velocity equation; vertical motion is always the familiar free-fall equation from the previous unit, just relabeled with y instead of x.")
E.add_bullets(s, ["Two separate \"mini-problems\" running on the same clock, *t* :"],
              E.CL, E.CT, E.CW, 0.6, size=19)
E.add_table(s, ["Horizontal  (x)", "Vertical  (y)"],
    [["constant velocity", C_ACC],
     [C_X, C_Y],
     ["\u2014", C_VYF]],
    E.CL, 2.6, E.CW, [5.9, 5.9], size=17, header_size=18, row_height=0.62,
    first_col_bold=False)
E.add_bullets(s, [
    "*g* is the only acceleration in the whole system, and it only ever touches the *y*-equations.",
], E.CL, 5.3, E.CW, 1.0, size=18)

# ================================================================== S9
s = new_slide("Special-Case Shortcuts \u2014 Range and Max Height",
    "Present these as convenience tools, not new physics - they're just Slide 7's equations pre-solved for one common situation. Stress the boundary condition hard; it's the single most common source of error when students first meet these formulas, since they're tempted to use them everywhere.")
E.add_bullets(s, ["When a projectile launches and lands at the *same height*, two shortcut formulas save time:"],
              E.CL, E.CT, E.CW, 0.7, size=19)
E.add_equation(s, EQ_S9, 2.6, size=23, width=10.0)
E.add_callout(s, [
    "***Important boundary:*** these only work for a *symmetric* trip \u2014 same launch and landing level. If a ball is thrown off a cliff or lands on a slope, these formulas *don't apply* \u2014 go back to the full equations from Slide 7 instead.",
], 4.35, size=18, height=1.6)

# ================================================================== S11
s = new_slide("How Launch Angle Changes the Flight",
    "Keep this qualitative and visual - the goal is intuition, not derivation. A useful classroom demo: ask students to picture throwing a ball almost flat versus almost straight up, and predict which travels farther. Most will correctly sense that neither extreme wins.")
E.add_bullets(s, [
    "Same *speed*, different *angle* \u2192 dramatically different paths.",
    "A shallow angle sends an object *far but low*; a steep angle sends it *high but not far*.",
    "Somewhere between those extremes is a launch angle that maximizes horizontal distance for a given speed \u2014 the range formula from Slide 9 reveals *which* angle that is, without needing to test every possibility by hand.",
], E.CL, E.CT, 6.1, 4.6, size=18)
E.add_image_fit(s, f"{A}/trajectory_fan.png", 7.1, E.CT, 5.4, 4.7, valign="middle")

# ================================================================== S13
s = new_slide("How Launch Speed Changes the Flight",
    "Tie this directly back to the puma example coming up next - animals and athletes usually can't easily change their launch angle mid-jump, but they absolutely can generate more speed through stronger muscles or a longer running start. That's the real-world lever most commonly pulled.")
E.add_bullets(s, [
    "Same *angle*, different *speed* \u2192 same *shape*, different *scale*.",
    "Doubling the launch speed doesn't just double the range \u2014 because speed appears *squared* in both the range and max-height formulas, the effect compounds fast.",
    "This matters anywhere launch speed is the variable an athlete, engineer, or animal can actually control \u2014 angle is often fixed by circumstance, but speed rarely is.",
], E.CL, E.CT + 0.4, E.CW, 3.8, size=22, gap=14)

# ================================================================== S15
s = new_slide("From Straight Lines to Circles \u2014 A New Kind of Motion",
    "This is a short signpost slide, not a deep dive - just enough to reset student expectations before the vocabulary shift. Ask: \"if speed isn't changing, is this thing accelerating at all?\" Don't answer yet - that tension carries directly into Slide 17.")
E.add_bullets(s, [
    "Everything so far involved a *changing* speed and a *changing* direction, both driven by gravity.",
    "Now: a Ferris wheel car, a satellite in orbit, a car rounding a curve \u2014 all moving at *roughly constant speed*, yet still very clearly *not* moving in a straight line.",
    "That's ***circular motion*** \u2014 a different curved path, driven by a completely different cause.",
], E.CL, E.CT + 0.4, E.CW, 3.8, size=22, gap=14)

# ================================================================== S16
s = new_slide("Uniform Circular Motion Defined",
    "Draw the \"always tangent\" idea out physically - imagine releasing a ball mid-spin on a string; it flies off in a straight line tangent to the circle at the release point, not toward the center and not along the circle. That tangent direction is the velocity direction at that instant.")
E.add_bullets(s, [
    "When an object travels a circular path at a *constant speed*, physicists call it ***uniform circular motion*** \u2014 common enough to earn its own name and its own toolkit of equations.",
    "A spinning record, a carousel horse, a satellite in a circular orbit \u2014 all textbook examples of the same underlying motion.",
    "The one thing that's *always* true: the velocity vector is *tangent* to the circle at every instant, and *perpendicular* to the radius.",
], E.CL, E.CT + 0.4, E.CW, 3.8, size=22, gap=14)

# ================================================================== S17
s = new_slide("Why Constant Speed Still Means Accelerating",
    "This deserves real airtime - it's one of the most persistent misconceptions in the whole unit. Use a whirling ball on a string: ask \"is its speed changing?\" (no) \"is its direction changing?\" (constantly) \"so is it accelerating?\" (yes). Make students say the answer out loud before moving on.")
E.add_bullets(s, [
    "Common misconception: \"constant speed\" means \"no acceleration.\" **False.**",
    "***Acceleration is a change in velocity \u2014 and velocity is a vector, made of both speed and direction.***",
    "In circular motion, the *speed* never changes, but the *direction* is changing at every single instant \u2014 and that alone is enough to count as acceleration.",
], E.CL, E.CT, 6.5, 4.6, size=19)
E.add_image_fit(s, f"{A}/circle_vectors.png", 7.5, E.CT, 5.05, 4.7, valign="middle")

# ================================================================== S18
s = new_slide("Centripetal Acceleration \u2014 Always Toward the Center",
    "Don't derive this from scratch - that similar-triangles proof belongs in a more advanced course. What matters here is the shape of the relationship: acceleration grows with the square of speed, and grows as radius shrinks. Have students predict, before revealing the formula, whether doubling the speed should double or quadruple the acceleration - most will guess wrong, which makes the reveal land harder.")
E.add_equation(s, EQ_S18, 2.0, size=27, width=5.6)
E.add_bullets(s, [
    "Called ***centripetal*** acceleration \u2014 literally \"center-seeking.\"",
    "It *always* points from the object straight toward the center of the circle, never along the path itself.",
    "Bigger speed *or* smaller radius \u2192 bigger acceleration. That relationship is the entire foundation of today's upcoming investigation.",
], E.CL, 3.35, E.CW, 3.2, size=20, gap=12)

# ================================================================== S19
s = new_slide("Measuring the Motion \u2014 Period and Speed",
    "Frame this as a practical translation tool rather than new physics - it converts between \"how fast\" and \"how long per lap,\" two ways of describing the exact same motion. This sets up both upcoming worked examples, which each hand students a period-like quantity instead of a speed.")
E.add_equation(s, EQ_S19, 2.0, size=27, width=5.6)
E.add_bullets(s, [
    "The ***period*** *T* is simply the time for *one full lap* around the circle.",
    "Useful because *T* is often the number you actually *know* in real life \u2014 a satellite's orbital period, a wheel's rotations per minute, a Ferris wheel's ride time \u2014 while *v* is usually the harder number to measure directly.",
    "This equation is really just \"distance = speed \u00d7 time,\" rearranged, applied to the circle's circumference.",
], E.CL, 3.35, E.CW, 3.2, size=20, gap=12)

# ================================================================== S22
s = new_slide("Centripetal Force \u2014 The Push Toward the Center",
    "Keep this conceptual and forward-looking rather than diving into free-body diagrams - that formal force analysis is intentionally saved for the Newton's Laws lesson. The goal today is just for students to recognize that \"acceleration toward the center\" implies \"some force pushing toward the center,\" and to start noticing that force in everyday situations (a car turning, a swung object, an orbiting satellite).")
E.add_equation(s, EQ_FC, 2.0, size=27, width=6.0)
E.add_bullets(s, [
    "Acceleration doesn't happen on its own \u2014 something has to *cause* it. For circular motion, that cause is the ***centripetal force***, always aimed toward the center, same direction as the acceleration it produces.",
    "In real life, that force wears many disguises: *tension* in a swung string, *friction* between tires and road on a curve, *gravity* pulling a satellite inward.",
    "This formula is really just Newton's second law (F = ma), applied to the acceleration formula from Slide 18 \u2014 a preview of the dynamics work coming on August 4th.",
], E.CL, 3.35, E.CW, 3.2, size=18, gap=8)

# ================================================================== S23
s = new_slide("Heads-Up: A Gap in This Chapter's Problems",
    "Be upfront about this with students rather than papering over it - it's a good moment to model how real curricula sometimes split a single topic across two chapters, and how a careful student can still connect the dots. This also reinforces the pacing boundary from the syllabus: full force-based problem-solving (with free-body diagrams) is intentionally deferred to August 4th.")
E.add_bullets(s, [
    "This textbook chapter covers circular motion purely as ***kinematics*** \u2014 acceleration, period, and speed \u2014 because *force* isn't formally introduced until the *next* chapter (Newton's Laws).",
    "Result: none of this chapter's practice problems ask students to solve for centripetal *force* numerically.",
], E.CL, E.CT, E.CW, 2.0, size=19)
E.add_callout(s, [
    "**Workaround:** since F\u1d04 = mv\u00b2/r = m \u00b7 a\u1d04 , force and acceleration scale *identically* for a fixed mass \u2014 every acceleration problem coming up doubles as a force problem in disguise, once mass is added.",
], 4.35, size=18, height=1.5)

# ================================================================== S25
s = new_slide("The Investigation Question \u2014 What Affects Centripetal Force?",
    "This slide is the formal launch of the \"carry out first-hand investigations\" half of the competency. Spend real time here making sure students can articulate, in their own words, which variables they're changing on purpose versus which one they're just watching change as a result.")
E.add_bullets(s, [
    "Today's guiding question, the one students will physically test: ***how do speed and radius affect the centripetal force needed to keep an object moving in a circle?***",
    "Before any data collection, the variables need to be sorted:",
], E.CL, E.CT, E.CW, 1.5, size=18)
E.add_table(s, ["Variable Type", "What It Is"],
    [["Independent", "speed, radius"],
     ["Dependent", "centripetal force"],
     ["Controlled", "mass of the spinning object"]],
    E.CL, 3.55, E.CW, [3.6, 8.2], size=18, header_size=18, row_height=0.62,
    first_col_bold=True)

# ================================================================== S26
s = new_slide("Apparatus and Setup for the Investigation",
    "Walk through the physical logic of why this setup works: the hanging washers provide a known, measurable force pulling the stopper inward - that known force stands in for centripetal force, letting students work backward to test the v-squared/r relationship even without directly measuring force in the string itself. Emphasize basic safety: clear space, secure grip, safety glasses if available.")
E.add_bullets(s, [
    "Classic classroom setup: a small stopper (or rubber tube) tied to one end of a string, threaded through a hollow tube, with a set of washers hung from the other end to provide a known, adjustable pulling force.",
    "The stopper is whirled overhead in a horizontal circle; the string length between hand and stopper sets the *radius*, and the speed of the whirl is adjusted so the hanging washers stay steady.",
    "If a physical apparatus isn't available, a simulation of the same setup works identically for testing the same variables.",
], E.CL, E.CT, 7.0, 4.6, size=18)
E.add_image_fit(s, f"{A}/apparatus.png", 8.0, E.CT, 4.55, 4.7, valign="middle")

# ================================================================== S27
s = new_slide("Predicting the Relationships Before Testing",
    "This is standard scientific-method practice, and it's worth naming explicitly: a prediction made before data collection is a hypothesis; the same claim made after seeing the data isn't testing anything. Have students commit their predictions to paper before touching any apparatus.")
E.add_bullets(s, ["Before collecting a single data point, use the formula itself to make a prediction:"],
              E.CL, E.CT, E.CW, 0.7, size=18)
E.add_equation(s, EQ_FC, 2.55, size=24, width=6.0)
E.add_bullets(s, [
    "Holding radius and mass fixed, doubling speed should *quadruple* the force needed (speed is squared).",
    "Holding speed and mass fixed, doubling the radius should *halve* the force needed (radius is in the denominator).",
    "Writing these predictions down *before* testing turns the lab from \"collect random numbers\" into \"test a specific claim.\"",
], E.CL, 4.0, E.CW, 2.6, size=18)

# ================================================================== S29
s = new_slide("From Data to Conclusion \u2014 Linking Results to the Formula",
    "This is where the lab work gets tied back to the theory taught earlier in the period. Push students to use the word \"consistent with\" (or \"inconsistent with,\" if their data doesn't match) rather than just describing what happened - that's the difference between reporting and interpreting data.")
E.add_bullets(s, [
    "Collected numbers alone aren't a conclusion \u2014 a conclusion *explains* what the numbers mean.",
    "A strong conclusion does three things: states what was changed, states what happened to the force as a result, and explicitly connects that pattern back to F\u1d04 = mv\u00b2/r.",
], E.CL, E.CT, E.CW, 1.9, size=19)
E.add_callout(s, [
    "Example structure (not a required script):",
    "*\"As the radius increased while speed was held constant, the measured force decreased \u2014 consistent with the inverse relationship predicted by the formula.\"*",
], 4.15, size=18, height=1.7)

# ================================================================== S30
s = new_slide("Projectile vs. Circular Motion \u2014 Two Types, One Framework",
    "Use this table as the closing synthesis - students should be able to fill in every cell from memory by now. This is also a natural moment to acknowledge, briefly, that both types of motion assumed a stationary observer watching from the ground - a detail that becomes important very soon.")
E.add_table(s, ["", "Projectile Motion", "Circular Motion"],
    [["Cause of curving", "gravity (constant, downward)", "centripetal force (toward center)"],
     ["Speed", "changes throughout flight", "stays constant"],
     ["Direction", "changes", "changes"],
     ["Acceleration direction", "always straight down", "always toward the center"],
     ["Everyday example", "a thrown ball", "a car rounding a curve"]],
    E.CL, 1.95, E.CW, [3.0, 4.4, 4.4], size=15, header_size=16, row_height=0.55,
    first_col_bold=True)
E.add_bullets(s, [
    "Both are genuinely *two-dimensional* motions \u2014 but the *reason* each one curves is completely different, and that difference is the entire story of today's lesson.",
], E.CL, 5.15, E.CW, 1.3, size=17)

# ---------------------------------------------------------------- cleanup
E.delete_sldIds(prs, orig_ids[1:10])   # remove old content slides, keep cover

prs.save(OUT)
print("Saved", OUT, "with", len(prs.slides.__iter__.__self__._sldIdLst), "slides")
print("slide count:", len(prs.slides._sldIdLst))
