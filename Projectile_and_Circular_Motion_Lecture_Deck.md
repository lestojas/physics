# Lecture Deck: Projectile & Circular Motion Investigation

*Pacing note: this deck runs long by design (31 slides) since the prior structural outline already stripped out lower-priority tiers. If the July 28 (3:00–4:00 PM) block runs short, Slides 23 and 29 are the safest trims — they're conceptual bridges, not core competency material.*

---

## Slide 1: Motion in Two Dimensions — Today's Target

**Content:**
- Today's competency, stated plainly: *carry out first-hand investigations involving 2-dimensional projectile and circular motion to investigate factors such as speed, radius, and centripetal force.*
- Two big ideas for the day, side by side:

| Projectile Motion | Circular Motion |
|---|---|
| A curved path caused by *gravity alone* | A curved path caused by a *center-seeking pull* |
| Speed and direction *both* change | Speed stays constant, but *direction* constantly changes |

**Speaker Notes:** Frame the whole session as answering one question twice: "why does this path curve, and what controls how much it curves?" We'll answer it first for things that fly through the air, then for things that spin. By the end of the hour, students should be ready to physically test the second answer with their own hands.

---

## Slide 2: The Shape Hiding in Plain Sight

**Content:**
- A diver leaving a cliff. Sparks flying off a welder's torch. Water arcing out of a park fountain.
- All three trace the *exact same curve* — even though nobody planned it that way.
- That curve has a name: the ***parabola***, and it shows up *any time* something launches into the air and gravity is the only thing acting on it afterward.

**Speaker Notes:** Open with the vivid images rather than the definition. Ask students what a diver's fall, welding sparks, and a fountain jet could possibly have in common — let them sit with that for a second before revealing it's the same geometric shape. This is the "aha" that should anchor the whole first half of the lesson: gravity writes the same signature every time.

**[Visual Suggestion:** A three-panel image strip — cliff diver mid-fall, welding sparks, and a fountain arc — with a single dashed parabolic curve overlaid on all three to visually prove they match.]

---

## Slide 3: Locating a Particle in Two Dimensions

**Content:**
- In *one* dimension, a single number tells you where something is.
- In *two* dimensions, you need **two numbers at once** — an *x*-position and a *y*-position — tracked *simultaneously*, not one after the other.
- This pair is bundled into a single arrow called the **position vector**, pointing from the origin to wherever the object currently is.

**Speaker Notes:** Keep this brief and conversational — students already have vector intuition from the prior unit. The key upgrade here is *simultaneity*: x and y aren't happening in sequence, they're happening together, at the same instant, for the same object.

---

## Slide 4: Breaking Velocity Into Two Directions

**Content:**
- Any launch velocity can be split into two perpendicular ingredients:

$$v_x = v_i\cos\theta_i \qquad v_y = v_i\sin\theta_i$$

- Think of a cannon fired at an angle: part of its "push" sends the ball *forward*, part of it sends the ball *upward* — and *trigonometry* tells you exactly how much of each.
- This is the *only* piece of vector-splitting needed for today — no adding multiple vectors together yet (that's Aug 4's job).

**Speaker Notes:** This is a *minimal* decomposition — one vector, split into two pieces. Be explicit that this is *not* the full vector-addition unit students will get in a week; it's just enough trigonometry to separate one launch velocity into its horizontal and vertical "ingredients."

---

## Slide 5: The Independence Principle

**Content:**
- Picture a hockey puck gliding in a straight line across a frictionless table.
- Someone gives it a *single sideways puff of air*. The puck now drifts diagonally — but its *original* forward speed never changed one bit.
- The generalization: ***motion in two dimensions can be modeled as two independent motions in each of the two perpendicular directions*** — a nudge in *y* never touches what's happening in *x*, and vice versa.
- This is *the* single most important idea in projectile motion. Everything else today builds on it.

**Speaker Notes:** This is the air-hockey-puck thought experiment straight from the reference text. Walk through it slowly: the puck moves at constant velocity in x; a puff of air in y adds a y-velocity but the x-velocity is completely unaffected. That independence is what lets us solve horizontal and vertical motion as two *separate*, simpler problems instead of one tangled one.

**[Visual Suggestion:** Two-row motion diagram — top row shows a puck moving at constant spacing horizontally; bottom row shows the same puck after a sideways puff, now drifting diagonally, with horizontal vector arrows of *identical length* in both rows to visually prove the x-component never changed.]

---

## Slide 6: Problem Solving #1 — Example 4.1 (Motion in a Plane)

**Content:**
- **Scenario:** a particle starts at the origin with a given horizontal and vertical initial velocity. It accelerates *only* in the horizontal direction — the vertical direction has zero acceleration.
- **Why this problem, right now:** it's the cleanest possible numerical proof of the independence principle — one direction changes, the other doesn't, and the math shows it explicitly.
- **Strategic framework:**
  1. Identify which direction has acceleration and which doesn't.
  2. Write the velocity-vs-time expression for *each* direction separately (constant acceleration model in x, constant velocity model in y).
  3. Combine both components into a single velocity vector at the requested time.
  4. Use the Pythagorean theorem and arctangent to convert that vector into a *speed* and a *direction angle*.

**Speaker Notes:** Let students predict the outcome before you solve it: "if only x has acceleration, what happens to the y-velocity over time?" They should say "nothing changes" — then the math confirms it. This cements Slide 5's principle with real numbers.

---

## Slide 7: The Governing Equations of Projectile Motion

**Content:**
- Two separate "mini-problems" running on the same clock, *t*:

| Horizontal (x) | Vertical (y) |
|---|---|
| *constant velocity* | *constant acceleration, a = –g* |
| $x_f = x_i + v_{xi}t$ | $y_f = y_i + v_{yi}t - \tfrac{1}{2}gt^2$ |
| — | $v_{yf} = v_{yi} - gt$ |

- *g* is the only acceleration in the whole system, and it only ever touches the *y*-equations.

**Speaker Notes:** This slide is the payoff of Slide 5 — students now see the independence principle turned into an actual toolkit. Emphasize the problem-solving habit: horizontal motion is *always* the "easy" constant-velocity equation; vertical motion is *always* the familiar free-fall equation from the previous unit, just relabeled with y instead of x.

---

## Slide 8: Problem Solving #2 — Problem 6 (Mug Slides Off the Counter)

**Content:**
- **Scenario:** an object slides horizontally off a raised surface (a bar counter) and falls a known horizontal distance before landing.
- **Why this problem, right now:** it's a *purely horizontal launch* — the simplest possible case, with $v_{yi} = 0$, making it the perfect first test of the governing equations above.
- **Strategic framework:**
  1. Set the point of departure as the origin; identify known and unknown quantities symbolically (height, horizontal distance).
  2. Use the vertical equation to solve for *time of fall* — this step never touches the horizontal motion.
  3. Plug that time into the horizontal equation to solve for *launch speed*.
  4. Use the time-of-fall to find the vertical velocity component at landing, then combine with the horizontal component to get impact speed and angle.

**Speaker Notes:** Highlight that step 2 doesn't require knowing the horizontal speed at all — that's the independence principle in action again. This is also a great moment to point out that "how fast something falls" is entirely separate from "how far it travels," a distinction that trips students up constantly.

---

## Slide 9: Special-Case Shortcuts — Range and Max Height

**Content:**
- When a projectile launches and lands at the *same height*, two shortcut formulas save time:

$$h = \frac{v_i^2\sin^2\theta_i}{2g} \qquad R = \frac{v_i^2\sin 2\theta_i}{g}$$

- ***Important boundary:*** these only work for a *symmetric* trip — same launch and landing level. If a ball is thrown off a cliff or lands on a slope, these formulas *don't apply* — go back to the full equations from Slide 7 instead.

**Speaker Notes:** Present these as convenience tools, not new physics — they're just Slide 7's equations pre-solved for one common situation. Stress the boundary condition hard; it's the single most common source of error when students first meet these formulas, since they're tempted to use them everywhere.

---

## Slide 10: Problem Solving #3 — Example 4.2 (The Long Jump)

**Content:**
- **Scenario:** an athlete leaves the ground at a known angle and speed, and lands back at the *same level* he took off from.
- **Why this problem, right now:** textbook-perfect fit for the Slide 9 shortcuts — same-level launch and landing, known angle and speed.
- **Strategic framework:**
  1. Confirm the same-level condition is met — this licenses using the shortcut formulas.
  2. Plug the given speed and angle directly into the range formula to find horizontal distance.
  3. Plug the same values into the max-height formula to find peak height.
  4. Sanity-check both results against realistic human-scale numbers.

**Speaker Notes:** This is deliberately the *first* time students get to skip the multi-step process from Slide 8 — a nice payoff moment. Ask them to notice how much faster this solve went once the shortcut conditions were satisfied.

---

## Slide 11: How Launch Angle Changes the Flight

**Content:**
- Same *speed*, different *angle* → dramatically different paths.
- A shallow angle sends an object *far but low*; a steep angle sends it *high but not far*.
- Somewhere between those extremes is a launch angle that maximizes horizontal distance for a given speed — the range formula from Slide 9 reveals *which* angle that is, without needing to test every possibility by hand.

**Speaker Notes:** Keep this qualitative and visual — the goal is intuition, not derivation. A useful classroom demo: ask students to picture throwing a ball almost flat versus almost straight up, and predict which travels farther. Most will correctly sense that *neither extreme* wins.

**[Visual Suggestion:** A fan of 3–4 trajectory arcs launched from the same point at the same speed but different angles, layered on one set of axes, so students can visually compare how range and height trade off against each other.]

---

## Slide 12: Problem Solving #4 — Problem 9 (Speed at Half Max Height)

**Content:**
- **Scenario:** a projectile's speed at its *maximum height* is described as exactly half its speed at the point where it's reached *half* of that maximum height. The launch angle is unknown.
- **Why this problem, right now:** it forces students to reason about *how* the two velocity components behave at different points of the trajectory — a direct test of angle intuition.
- **Strategic framework:**
  1. Recall that at maximum height, the *vertical* velocity component is exactly zero — so speed at the peak is *purely horizontal*.
  2. Express the speed at the halfway point using both velocity components (horizontal stays constant; vertical is found from the height-velocity relationship).
  3. Set up the ratio described in the problem as an algebraic equation.
  4. Solve for the launch angle.

**Speaker Notes:** This is more algebra-heavy than the previous problems — that's intentional, since it's a "required but sits right at the edge" style problem. Walk through the logic of step 1 carefully; students often forget that horizontal speed at the peak equals the *initial* horizontal speed, since horizontal velocity never changes throughout the flight.

---

## Slide 13: How Launch Speed Changes the Flight

**Content:**
- Same *angle*, different *speed* → same *shape*, different *scale*.
- Doubling the launch speed doesn't just double the range — because speed appears *squared* in both the range and max-height formulas, the effect compounds fast.
- This matters anywhere launch speed is the variable an athlete, engineer, or animal can actually control — angle is often fixed by circumstance, but speed rarely is.

**Speaker Notes:** Tie this directly back to the puma example coming up next — animals and athletes usually can't easily change their launch angle mid-jump, but they absolutely can generate more speed through stronger muscles or a longer running start. That's the real-world lever most commonly pulled.

---

## Slide 14: Problem Solving #5 — Problem 7 (The Puma's Leap)

**Content:**
- **Scenario:** a puma — described as among the best jumpers of any animal — clears a known maximum height while leaving the ground at a 45° angle.
- **Why this problem, right now:** direct, real-world application of how launch *speed* determines *height*, using the maximum-height shortcut from Slide 9.
- **Strategic framework:**
  1. Convert the given height into SI units (metric) before doing anything else.
  2. Recognize the angle (45°) and height are both known — the max-height formula has only one unknown left: launch speed.
  3. Rearrange the max-height formula to isolate speed.
  4. Solve numerically and sanity-check against realistic animal-locomotion speeds.

**Speaker Notes:** This is a good moment to highlight unit conversion as its own small skill — the original height is given in feet, and skipping the conversion is the single most common way students get this one wrong. Once solved, compare the puma's required speed to a human sprinting speed for a fun scale check.

---

## Slide 15: From Straight Lines to Circles — A New Kind of Motion

**Content:**
- Everything so far involved a *changing* speed and a *changing* direction, both driven by gravity.
- Now: a Ferris wheel car, a satellite in orbit, a car rounding a curve — all moving at *roughly constant speed*, yet still very clearly *not* moving in a straight line.
- That's ***circular motion*** — a different curved path, driven by a completely different cause.

**Speaker Notes:** This is a short signpost slide, not a deep dive — just enough to reset student expectations before the vocabulary shift. Ask: "if speed isn't changing, is this thing accelerating at all?" Don't answer yet — that tension carries directly into Slide 17.

---

## Slide 16: Uniform Circular Motion Defined

**Content:**
- When an object travels a circular path at a *constant speed*, physicists call it ***uniform circular motion*** — common enough to earn its own name and its own toolkit of equations.
- A spinning record, a carousel horse, a satellite in a circular orbit — all textbook examples of the same underlying motion.
- The one thing that's *always* true: the velocity vector is *tangent* to the circle at every instant, and *perpendicular* to the radius.

**Speaker Notes:** Draw the "always tangent" idea out physically — imagine releasing a ball mid-spin on a string; it flies off in a straight line tangent to the circle at the release point, not toward the center and not along the circle. That tangent direction *is* the velocity direction at that instant.

---

## Slide 17: Why Constant Speed Still Means Accelerating

**Content:**
- Common misconception: "constant speed" means "no acceleration." **False.**
- ***Acceleration is a change in velocity — and velocity is a vector, made of both speed and direction.***
- In circular motion, the *speed* never changes, but the *direction* is changing at every single instant — and that alone is enough to count as acceleration.

**Speaker Notes:** This deserves real airtime — it's one of the most persistent misconceptions in the whole unit. Use a whirling ball on a string: ask "is its speed changing?" (no) "is its direction changing?" (constantly) "so is it accelerating?" (yes). Make students say the answer out loud before moving on.

**[Visual Suggestion:** A circle with velocity vectors of *identical length* drawn tangent at four different points around the circle, visually emphasizing that the arrow length (speed) never changes while its direction rotates continuously.]

---

## Slide 18: Centripetal Acceleration — Always Toward the Center

**Content:**
$$a_c = \frac{v^2}{r}$$

- Called ***centripetal*** acceleration — literally "center-seeking."
- It *always* points from the object straight toward the center of the circle, never along the path itself.
- Bigger speed *or* smaller radius → bigger acceleration. That relationship is the entire foundation of today's upcoming investigation.

**Speaker Notes:** Don't derive this from scratch — that similar-triangles proof belongs in a more advanced course. What matters here is the *shape* of the relationship: acceleration grows with the *square* of speed, and grows as radius shrinks. Have students predict, before revealing the formula, whether doubling the speed should double or quadruple the acceleration — most will guess wrong, which makes the reveal land harder.

---

## Slide 19: Measuring the Motion — Period and Speed

**Content:**
$$T = \frac{2\pi r}{v}$$

- The ***period*** *T* is simply the time for *one full lap* around the circle.
- Useful because *T* is often the number you actually *know* in real life — a satellite's orbital period, a wheel's rotations per minute, a Ferris wheel's ride time — while *v* is usually the harder number to measure directly.
- This equation is really just "distance = speed × time," rearranged, applied to the circle's circumference.

**Speaker Notes:** Frame this as a *practical translation tool* rather than new physics — it converts between "how fast" and "how long per lap," two ways of describing the exact same motion. This sets up both upcoming worked examples, which each hand students a period-like quantity instead of a speed.

---

## Slide 20: Problem Solving #6 — Example 4.6 (Centripetal Acceleration of the Earth)

**Content:**
- **Scenario:** find the Earth's centripetal acceleration as it orbits the Sun, using the orbital period (one year) and the known orbital radius — *not* a directly given speed.
- **Why this problem, right now:** it's the natural combination of Slides 18 and 19 — students don't have *v* directly, so they must build it from *T* first.
- **Strategic framework:**
  1. Recognize that *v* is unknown but *T* and *r* are both given.
  2. Substitute the period-speed relationship into the centripetal acceleration formula to eliminate *v* entirely, producing a version of the formula written in terms of *T* and *r* only.
  3. Convert the period into seconds to match SI units for radius.
  4. Substitute numbers and solve.

**Speaker Notes:** This is a great "aha" moment for combining two formulas rather than treating them as isolated tools. Point out afterward how tiny the resulting acceleration is compared to everyday centripetal accelerations — a nice scale contrast for the very next problem.

---

## Slide 21: Problem Solving #7 — Problem 19 (Astronaut Docking With a Satellite)

**Content:**
- **Scenario:** an astronaut is preparing to dock with a satellite in a known circular orbit above Earth, where the local free-fall (centripetal) acceleration is already given.
- **Why this problem, right now:** runs the *same* two formulas from Slide 20, but in the opposite direction — acceleration is known, speed and period are the unknowns.
- **Strategic framework:**
  1. Start from the centripetal acceleration formula, this time solving *for* speed rather than plugging speed in.
  2. Use the given radius (Earth's radius plus orbital altitude) to complete that calculation.
  3. Take the resulting speed and plug it into the period-speed formula to find the orbital period.
  4. Double-check that both answers are physically sensible for a satellite altitude of a few hundred kilometers.

**Speaker Notes:** Have students notice this is essentially Slide 20 in reverse — same two formulas, different known and unknown. That flexibility (solving the same relationship for different variables depending on what's given) is exactly the skill this pair of problems is meant to build.

---

## Slide 22: Centripetal Force — The Push Toward the Center

**Content:**
$$F_c = \frac{mv^2}{r}$$

- Acceleration doesn't happen on its own — something has to *cause* it. For circular motion, that cause is the ***centripetal force***, always aimed toward the center, same direction as the acceleration it produces.
- In real life, that force wears many disguises: *tension* in a swung string, *friction* between tires and road on a curve, *gravity* pulling a satellite inward.
- This formula is really just Newton's second law ($F = ma$), applied to the acceleration formula from Slide 18 — a preview of the dynamics work coming on August 4th.

**Speaker Notes:** Keep this conceptual and forward-looking rather than diving into free-body diagrams — that formal force analysis is intentionally saved for the Newton's Laws lesson. The goal today is just for students to recognize that "acceleration toward the center" implies "some force pushing toward the center," and to start noticing that force in everyday situations (a car turning, a swung object, an orbiting satellite).

---

## Slide 23: Heads-Up: A Gap in This Chapter's Problems

**Content:**
- This textbook chapter covers circular motion purely as ***kinematics*** — acceleration, period, and speed — because *force* isn't formally introduced until the *next* chapter (Newton's Laws).
- Result: none of this chapter's practice problems ask students to solve for centripetal *force* numerically.
- **Workaround:** since $F_c = mv^2/r = m \cdot a_c$, force and acceleration scale *identically* for a fixed mass — every acceleration problem coming up doubles as a force problem in disguise, once mass is added.

**Speaker Notes:** Be upfront about this with students rather than papering over it — it's a good moment to model how real curricula sometimes split a single topic across two chapters, and how a careful student can still connect the dots. This also reinforces the pacing boundary from the syllabus: full force-based problem-solving (with free-body diagrams) is intentionally deferred to August 4th.

---

## Slide 24: Problem Solving #8 — Problem 21 (Discus Throw)

**Content:**
- **Scenario:** an athlete swings a discus of known mass along a circular path of known radius, reaching a known maximum speed.
- **Why this problem, right now:** clean, direct application of the centripetal acceleration formula in an athletic, relatable context — and since mass is given, it's the closest thing this chapter offers to a force calculation (see Slide 23).
- **Strategic framework:**
  1. Identify the radius and maximum speed directly from the scenario.
  2. Substitute both into the centripetal acceleration formula.
  3. Solve for the maximum radial acceleration.
  4. *(Bonus reasoning, not required by the original problem):* since mass is also given, discuss — without formally solving — how that same number could scale directly into a force value once Newton's second law is formally covered.

**Speaker Notes:** Use the bonus reasoning step as a bridge-building moment rather than an actual additional calculation — the goal is conceptual continuity into the force unit, not extra unassigned work.

---

## Slide 25: The Investigation Question — What Affects Centripetal Force?

**Content:**
- Today's guiding question, the one students will physically test: ***how do speed and radius affect the centripetal force needed to keep an object moving in a circle?***
- Before any data collection, the variables need to be sorted:

| Variable Type | What It Is |
|---|---|
| Independent | speed, radius |
| Dependent | centripetal force |
| Controlled | mass of the spinning object |

**Speaker Notes:** This slide *is* the formal launch of the "carry out first-hand investigations" half of the competency. Spend real time here making sure students can articulate, in their own words, which variables they're changing on purpose versus which one they're just watching change as a result.

---

## Slide 26: Apparatus and Setup for the Investigation

**Content:**
- Classic classroom setup: a small stopper (or rubber tube) tied to one end of a string, threaded through a hollow tube, with a set of washers hung from the other end to provide a known, adjustable pulling force.
- The stopper is whirled overhead in a horizontal circle; the string length between hand and stopper sets the *radius*, and the speed of the whirl is adjusted so the hanging washers stay steady.
- If a physical apparatus isn't available, a simulation of the same setup works identically for testing the same variables.

**Speaker Notes:** Walk through the physical logic of *why* this setup works: the hanging washers provide a known, measurable force pulling the stopper inward — that known force stands in for centripetal force, letting students work backward to test the v²/r relationship even without directly measuring force in the string itself. Emphasize basic safety: clear space, secure grip, safety glasses if available.

**[Visual Suggestion:** A labeled diagram of the stopper-tube-washer apparatus — string through a hollow tube, stopper whirling in a horizontal circle above the tube, washers hanging below providing tension — with the radius and swing direction clearly marked.]

---

## Slide 27: Predicting the Relationships Before Testing

**Content:**
- Before collecting a single data point, use the formula itself to make a prediction:

$$F_c = \frac{mv^2}{r}$$

- Holding radius and mass fixed, doubling speed should *quadruple* the force needed (speed is squared).
- Holding speed and mass fixed, doubling the radius should *halve* the force needed (radius is in the denominator).
- Writing these predictions down *before* testing turns the lab from "collect random numbers" into "test a specific claim."

**Speaker Notes:** This is standard scientific-method practice, and it's worth naming explicitly: a prediction made *before* data collection is a *hypothesis*; the same claim made *after* seeing the data isn't testing anything. Have students commit their predictions to paper before touching any apparatus.

---

## Slide 28: Problem Solving #9 — Problem 20 (Athlete Swinging a Ball on a Chain)

**Content:**
- **Scenario:** an athlete swings a ball on a chain at two different chain lengths and two different rotation rates — a shorter chain spun faster, and a longer chain spun slower.
- **Why this problem, right now:** it's essentially *this lesson's investigation, done on paper first* — comparing how radius and rotation rate together shape speed and acceleration.
- **Strategic framework:**
  1. Convert each rotation rate into a usable speed, using the period-speed relationship from Slide 19 (rotations per second connect to period, and period connects to speed via circumference).
  2. Compare the two resulting speeds directly to answer which setup produces the greater speed.
  3. Apply the centripetal acceleration formula to each of the two setups separately.
  4. Compare both accelerations and connect the result back to the predictions made in Slide 27.

**Speaker Notes:** Treat this as a rehearsal — solving it carefully here is what will let students correctly interpret their own physical data in a few minutes. Point out that this problem varies *both* radius and rotation rate at once, which is exactly the kind of multi-variable comparison their own investigation will need to handle.

---

## Slide 29: From Data to Conclusion — Linking Results to the Formula

**Content:**
- Collected numbers alone aren't a conclusion — a conclusion *explains* what the numbers mean.
- A strong conclusion does three things: states what was changed, states what happened to the force as a result, and explicitly connects that pattern back to $F_c = mv^2/r$.
- Example structure (not a required script): *"As the radius increased while speed was held constant, the measured force decreased — consistent with the inverse relationship predicted by the formula."*

**Speaker Notes:** This is where the lab work gets tied back to the theory taught earlier in the period. Push students to use the word "consistent with" (or "inconsistent with," if their data doesn't match) rather than just describing what happened — that's the difference between reporting and *interpreting* data.

---

## Slide 30: Projectile vs. Circular Motion — Two Types, One Framework

**Content:**

| | Projectile Motion | Circular Motion |
|---|---|---|
| Cause of curving | gravity (constant, downward) | centripetal force (toward center) |
| Speed | changes throughout flight | stays constant |
| Direction | changes | changes |
| Acceleration direction | always straight down | always toward the center |
| Everyday example | a thrown ball | a car rounding a curve |

- Both are genuinely *two-dimensional* motions — but the *reason* each one curves is completely different, and that difference is the entire story of today's lesson.

**Speaker Notes:** Use this table as the closing synthesis — students should be able to fill in every cell from memory by now. This is also a natural moment to acknowledge, briefly, that both types of motion assumed a *stationary observer* watching from the ground — a detail that becomes important very soon.

---

## Slide 31: Exit Ticket

**Content:**
- **Problem 1 (Projectile Motion):** Chapter 4, Problem 8 — a projectile's horizontal range is described as exactly three times its maximum height; find the launch angle. *(Mirrors Problem Solving #4.)*
- **Problem 2 (Circular Motion):** Chapter 4, Problem 22 — a tire of known radius rotates at a constant rate in revolutions per minute; find the speed and acceleration of a point on its outer edge. *(Mirrors Problem Solving #6.)*

**Speaker Notes:** Both problems intentionally echo the structure of problems already solved together in class — the goal is to check whether students can reproduce the *strategy*, not whether they can memorize a brand-new scenario. Circulate while they work rather than solving either one aloud.
