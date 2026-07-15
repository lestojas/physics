# -*- coding: utf-8 -*-
"""All authored content for the solution key. build(g) receives builder helpers."""


def build(g):
    banner            = g["banner"]
    strategy_note     = g["strategy_note"]
    reference_table   = g["reference_table"]
    section_header    = g["section_header"]
    problem           = g["problem"]
    given_required    = g["given_required"]
    solution_header   = g["solution_header"]
    step              = g["step"]
    derive            = g["derive"]
    answer_box        = g["answer_box"]
    conclusion_box    = g["conclusion_box"]
    insight           = g["insight"]

    banner()
    strategy_note()
    reference_table()

    # =====================================================================
    section_header(1, "Motion of an Air Parcel in a Tube")
    problem("A parcel of air moving in a straight tube with a constant acceleration of "
            "24.00 m/s\u00b2 has a velocity of 13.0 m/s at 10:05:00 a.m. "
            "(a) What is its velocity at 10:05:01 a.m.? (b) At 10:05:04 a.m.? (c) At 10:04:59 a.m.?")
    given_required(
        [
            [("t", "Acceleration  "), ("m", r"a = +24.00\ \text{m/s}^{2}"), ("t", "  (constant)")],
            [("t", "Reference time  "), ("m", r"t = 0"), ("t", " : 10:05:00 a.m.")],
            [("t", "Initial velocity  "), ("m", r"v_0 = 13.0\ \text{m/s}")],
        ],
        [
            [("m", r"v"), ("t", "  at  "), ("m", r"t = +1.00\ \text{s}"), ("t", "  (10:05:01 a.m.)")],
            [("m", r"v"), ("t", "  at  "), ("m", r"t = +4.00\ \text{s}"), ("t", "  (10:05:04 a.m.)")],
            [("m", r"v"), ("t", "  at  "), ("m", r"t = -1.00\ \text{s}"), ("t", "  (10:04:59 a.m.)")],
        ])
    solution_header()
    step("Step 1.", [("t", "We know "), ("m", r"v_0"), ("t", ", "), ("m", r"a"), ("t", ", and "),
                     ("m", r"t"), ("t", ", and we want "), ("m", r"v"), ("t", " while position "),
                     ("m", r"x"), ("t", " is missing. Choose "), ("b", "Equation 1"), ("t", ".")])
    derive(r"v &= v_0 + at")
    step("Part (a).", [("t", "At "), ("m", r"t = +1.00\ \text{s}"), ("t", ":")])
    derive(r"v &= 13.0 + (24.00)(1.00) \\ &= 13.0 + 24.0 \\ &= 37.0\ \text{m/s}")
    answer_box("Part (a)", r"v = 37.0\ \text{m/s}")
    step("Part (b).", [("t", "At "), ("m", r"t = +4.00\ \text{s}"), ("t", ":")])
    derive(r"v &= 13.0 + (24.00)(4.00) \\ &= 13.0 + 96.0 \\ &= 109.0\ \text{m/s}")
    answer_box("Part (b)", r"v = 109.0\ \text{m/s}")
    step("Part (c).", [("t", "At "), ("m", r"t = -1.00\ \text{s}"),
                       ("t", " (one second before the reference time):")])
    derive(r"v &= 13.0 + (24.00)(-1.00) \\ &= 13.0 - 24.0 \\ &= -11.0\ \text{m/s}")
    answer_box("Part (c)", r"v = -11.0\ \text{m/s}")
    insight([("t", "The choice of the initial instant "), ("m", r"t = 0"),
             ("t", " is arbitrary; a negative time simply denotes a state before that chosen "
                   "reference. The negative result "), ("m", r"v = -11.0\ \text{m/s}"),
             ("t", " is physically meaningful: at that earlier moment the parcel was moving in the "
                   "opposite (negative) direction before slowing, reversing, and moving in the "
                   "positive direction.")])

    # =====================================================================
    section_header(2, "Landing Jet on an Aircraft Carrier")
    problem("A jet lands on an aircraft carrier at a speed of 140 mi/h (\u2248 63 m/s). "
            "(A) What is its acceleration (assumed constant) if it stops in 2.0 s due to an "
            "arresting cable? (B) If the jet touches down at position x\u1d62 = 0, what is its "
            "final position?")
    given_required(
        [
            [("t", "Initial position  "), ("m", r"x_0 = 0\ \text{m}")],
            [("t", "Initial velocity  "), ("m", r"v_0 = 63\ \text{m/s}")],
            [("t", "Final velocity  "), ("m", r"v = 0\ \text{m/s}"), ("t", "  (fully stopped)")],
            [("t", "Time interval  "), ("m", r"t = 2.0\ \text{s}")],
        ],
        [
            [("t", "Acceleration  "), ("m", r"a"), ("t", "  in  "), ("m", r"\text{m/s}^{2}")],
            [("t", "Final position  "), ("m", r"x_f"), ("t", "  in metres")],
        ])
    solution_header()
    step("Part (A).", [("t", "We have "), ("m", r"v_0"), ("t", ", "), ("m", r"v"), ("t", ", and "),
                       ("m", r"t"), ("t", "; position is missing, so use "), ("b", "Equation 1"),
                       ("t", " and solve for "), ("m", r"a"), ("t", ":")])
    derive(r"a &= \frac{v - v_0}{t} \\ &= \frac{0 - 63}{2.0} \\ &= -31.5\ \text{m/s}^{2}")
    answer_box("Part (A)", r"a = -31.5\ \text{m/s}^{2}")
    step("Part (B).", [("t", "To avoid propagating any rounding in "), ("m", r"a"),
                       ("t", ", omit acceleration and use "), ("b", "Equation 4"), ("t", ":")])
    derive(r"x &= x_0 + \tfrac{1}{2}(v_0 + v)\,t \\ &= 0 + \tfrac{1}{2}(63 + 0)(2.0) \\ "
           r"&= \tfrac{1}{2}(63)(2.0) \\ &= 63\ \text{m}")
    answer_box("Part (B)", r"x_f = 63\ \text{m}")
    insight([("t", "Stress the meaning of the negative sign in "), ("m", r"a = -31.5\ \text{m/s}^{2}"),
             ("t", ". Ask: does negative acceleration always mean slowing down? Because the initial "
                   "velocity is positive and the acceleration is negative, the two vectors point in "
                   "opposite directions, so here the jet does decelerate.")])

    # =====================================================================
    section_header(3, "Uniformly Accelerating Object")
    problem("An object moving with uniform acceleration has a velocity of 12.0 cm/s in the positive "
            "x direction when its x coordinate is 3.00 cm. If its x coordinate 2.00 s later is "
            "25.00 cm, what is its acceleration?")
    given_required(
        [
            [("t", "Initial position  "), ("m", r"x_0 = 3.00\ \text{cm}")],
            [("t", "Initial velocity  "), ("m", r"v_0 = +12.0\ \text{cm/s}")],
            [("t", "Final position  "), ("m", r"x = 25.00\ \text{cm}")],
            [("t", "Time interval  "), ("m", r"t = 2.00\ \text{s}")],
        ],
        [
            [("t", "Acceleration  "), ("m", r"a"), ("t", "  in  "), ("m", r"\text{cm/s}^{2}")],
        ])
    solution_header()
    step("Step 1.", [("t", "Final velocity "), ("m", r"v"),
                     ("t", " is neither given nor required \u2014 it is the missing variable \u2014 "
                           "so use "), ("b", "Equation 2"), ("t", ".")])
    derive(r"x &= x_0 + v_0 t + \tfrac{1}{2}a t^{2}")
    step("Step 2.", [("t", "Rearrange to isolate "), ("m", r"a"), ("t", ":")])
    derive(r"x - x_0 - v_0 t &= \tfrac{1}{2}a t^{2} \\ a &= \frac{2\,(x - x_0 - v_0 t)}{t^{2}}")
    step("Step 3.", [("t", "Substitute the known values:")])
    derive(r"a &= \frac{2\,[\,25.00 - 3.00 - (12.0)(2.00)\,]}{(2.00)^{2}} \\ "
           r"&= \frac{2\,[\,25.00 - 3.00 - 24.00\,]}{4.00} \\ "
           r"&= \frac{2(-2.00)}{4.00} = \frac{-4.00}{4.00} \\ &= -1.00\ \text{cm/s}^{2}")
    answer_box("", r"a = -1.00\ \text{cm/s}^{2}")
    insight([("t", "Reinforce coordinate-system discipline. Writing every algebraic step and every "
                   "unit exposes why the numerator becomes a negative change "),
             ("m", r"(-2.00\ \text{cm})"),
             ("t", ", which in turn gives a negative acceleration. Skipping steps is where sign "
                   "errors creep in.")])

    # =====================================================================
    section_header(4, "Electron in a Cathode-Ray Tube")
    problem("An electron in a cathode-ray tube accelerates uniformly from 2.00 \u00d7 10\u2074 m/s to "
            "6.00 \u00d7 10\u2076 m/s over 1.50 cm. (a) In what time interval does the electron travel "
            "this 1.50 cm? (b) What is its acceleration?")
    given_required(
        [
            [("t", "Initial velocity  "), ("m", r"v_0 = 2.00\times10^{4}\ \text{m/s}")],
            [("t", "Final velocity  "), ("m", r"v = 6.00\times10^{6}\ \text{m/s}")],
            [("t", "Displacement  "), ("m", r"x - x_0 = 1.50\ \text{cm} = 0.0150\ \text{m}")],
        ],
        [
            [("t", "Time interval  "), ("m", r"t"), ("t", "  in seconds")],
            [("t", "Acceleration  "), ("m", r"a"), ("t", "  in  "), ("m", r"\text{m/s}^{2}")],
        ])
    solution_header()
    step("Part (a).", [("t", "Acceleration is the missing variable, so use "), ("b", "Equation 4"),
                       ("t", " and solve for "), ("m", r"t"), ("t", ":")])
    derive(r"t &= \frac{2\,(x - x_0)}{v_0 + v} \\ "
           r"&= \frac{2\,(0.0150)}{2.00\times10^{4} + 6.00\times10^{6}} \\ "
           r"&= \frac{0.0300}{6.02\times10^{6}} \\ &\approx 4.98\times10^{-9}\ \text{s}")
    answer_box("Part (a)", r"t \approx 4.98\times10^{-9}\ \text{s} = 4.98\ \text{ns}")
    step("Part (b).", [("t", "Use "), ("b", "Equation 3"),
                       ("t", ", which avoids the time we just computed:")])
    derive(r"a &= \frac{v^{2} - v_0^{\,2}}{2\,(x - x_0)} \\ "
           r"&= \frac{(6.00\times10^{6})^{2} - (2.00\times10^{4})^{2}}{2\,(0.0150)} \\ "
           r"&= \frac{3.60\times10^{13} - 4.00\times10^{8}}{0.0300} \\ "
           r"&\approx 1.20\times10^{15}\ \text{m/s}^{2}")
    answer_box("Part (b)", r"a \approx 1.20\times10^{15}\ \text{m/s}^{2}")
    insight([("t", "A good place to practise scientific notation and significant figures. Note that "),
             ("m", r"v_0^{\,2} = 4.00\times10^{8}"),
             ("t", " is five orders of magnitude smaller than "), ("m", r"v^{2} = 3.60\times10^{13}"),
             ("t", ", so it barely affects the result \u2014 yet keeping it models honest bookkeeping.")])

    # =====================================================================
    section_header(5, "The Case of the Impossible Rhinoceros")
    problem("Why is the following situation impossible? Starting from rest, a charging rhinoceros "
            "moves 50.0 m in a straight line in 10.0 s. Her acceleration is constant during the "
            "entire motion, and her final speed is 8.00 m/s.")
    given_required(
        [
            [("t", "Initial velocity  "), ("m", r"v_0 = 0\ \text{m/s}"), ("t", "  (from rest)")],
            [("t", "Displacement  "), ("m", r"\Delta x = 50.0\ \text{m}")],
            [("t", "Time interval  "), ("m", r"t = 10.0\ \text{s}")],
            [("t", "Reported final speed  "), ("m", r"v = 8.00\ \text{m/s}")],
            [("t", "Assumption: acceleration "), ("m", r"a"), ("t", " is constant")],
        ],
        [
            [("t", "Show the scenario is internally contradictory")],
        ])
    solution_header()
    step("Method A.", [("t", "Compute the displacement implied by the start/end speeds using "),
                       ("b", "Equation 4"), ("t", ":")])
    derive(r"\Delta x &= \tfrac{1}{2}(v_0 + v)\,t \\ &= \tfrac{1}{2}(0 + 8.00)(10.0) \\ &= 40.0\ \text{m}")
    step("", [("t", "But the problem claims 50.0 m \u2014 a direct contradiction.")])
    step("Method B.", [("t", "Compute the final speed required to cover 50.0 m in 10.0 s from rest:")])
    derive(r"v &= \frac{2\,\Delta x}{t} - v_0 \\ &= \frac{2\,(50.0)}{10.0} - 0 \\ &= 10.0\ \text{m/s}")
    step("", [("t", "This requires 10.0 m/s, not the stated 8.00 m/s.")])
    step("Method C.", [("t", "Compare the acceleration implied by two different equations:")])
    derive(r"\text{Eq. 2:}\quad 50.0 &= \tfrac{1}{2}a(10.0)^{2} \;\Rightarrow\; a = 1.00\ \text{m/s}^{2} \\ "
           r"\text{Eq. 1:}\quad 8.00 &= 0 + a(10.0) \;\Rightarrow\; a = 0.800\ \text{m/s}^{2}")
    conclusion_box("Why it is impossible",
                   "A single constant acceleration cannot be both 1.00 m/s\u00b2 and 0.800 m/s\u00b2. "
                   "The displacement, final speed, and constant-acceleration conditions over-constrain "
                   "the motion and contradict one another, so the situation cannot occur.")
    insight([("t", "This is a diagnostic problem: each method attacks the same contradiction from a "
                   "different variable (displacement, final speed, acceleration). Showing all three "
                   "teaches students that a well-posed kinematics problem must be self-consistent.")])

    # =====================================================================
    section_header(6, "Two Competing Toy Cars")
    problem("At t = 0, one toy car rolls on a straight track with initial position 15.0 cm, initial "
            "velocity 23.50 cm/s, and constant acceleration 2.40 cm/s\u00b2. At the same moment, a "
            "second car rolls on an adjacent track with initial position 10.0 cm, initial velocity "
            "15.50 cm/s, and zero acceleration. (a) When, if ever, do the cars have equal speeds? "
            "(b) What are those speeds? (c) When, if ever, do they pass each other? (d) Where? "
            "(e) Explain the difference between (a) and (c).")
    given_required(
        [
            [("b", "Car 1 (accelerating)")],
            [("m", r"x_{1,0} = 15.0\ \text{cm},\ \ v_{1,0} = 23.50\ \text{cm/s}")],
            [("m", r"a_{1} = 2.40\ \text{cm/s}^{2}")],
            [("b", "Car 2 (constant speed)")],
            [("m", r"x_{2,0} = 10.0\ \text{cm},\ \ v_{2,0} = 15.50\ \text{cm/s}")],
            [("m", r"a_{2} = 0")],
        ],
        [
            [("t", "(a) time of equal speeds  "), ("m", r"v_1 = v_2")],
            [("t", "(b) that common speed")],
            [("t", "(c) time(s) they pass  "), ("m", r"x_1 = x_2")],
            [("t", "(d) positions where they pass")],
            [("t", "(e) compare (a) and (c) conceptually")],
        ])
    solution_header()
    step("Part (a).", [("t", "Write each velocity function and set them equal:")])
    derive(r"v_1(t) &= 23.50 + 2.40\,t \\ v_2(t) &= 15.50")
    derive(r"23.50 + 2.40\,t &= 15.50 \\ 2.40\,t &= -8.00 \\ t &= -3.33\ \text{s}")
    conclusion_box("Part (a)",
                   "Since motion is considered only for t \u2265 0, there is no future instant at which "
                   "the two cars share the same speed.")
    step("Part (b).", [("t", "Mathematically, at "), ("m", r"t = -3.33\ \text{s}"),
                       ("t", " both speeds equal "), ("m", r"15.50\ \text{cm/s}"),
                       ("t", ". Physically, for "), ("m", r"t \ge 0"),
                       ("t", ", Car 1 is always faster and still accelerating, so their speeds never "
                             "match after release.")])
    step("Part (c).", [("t", "Write each position function and set them equal:")])
    derive(r"x_1(t) &= 15.0 + 23.50\,t + 1.20\,t^{2} \\ x_2(t) &= 10.0 + 15.50\,t")
    derive(r"15.0 + 23.50\,t + 1.20\,t^{2} &= 10.0 + 15.50\,t \\ 1.20\,t^{2} + 8.00\,t + 5.00 &= 0")
    step("", [("t", "Apply the quadratic formula:")])
    derive(r"t &= \frac{-8.00 \pm \sqrt{(8.00)^{2} - 4(1.20)(5.00)}}{2(1.20)} \\ "
           r"&= \frac{-8.00 \pm \sqrt{40.0}}{2.40} \\ "
           r"t_1 &\approx -0.698\ \text{s}, \quad t_2 \approx -5.97\ \text{s}")
    conclusion_box("Part (c)",
                   "Both roots are negative, so there is no physical time (t \u2265 0) at which the cars "
                   "pass each other.")
    step("Part (d).", [("t", "The (past) mathematical intersection points lie on Car 2's line:")])
    derive(r"x(t_1) &= 10.0 + 15.50(-0.698) \approx -0.82\ \text{cm} \\ "
           r"x(t_2) &= 10.0 + 15.50(-5.97) \approx -82.5\ \text{cm}")
    step("Part (e).", [("t", "Equal "), ("b", "speeds"),
                       ("t", " means the two position-time graphs have the same slope (same rate of "
                             "motion), regardless of location. "), ("b", "Passing"),
                       ("t", " means the graphs intersect \u2014 the cars occupy the same point in "
                             "space \u2014 regardless of their rates. They are different questions "
                             "about different features of the graphs.")])
    insight([("t", "A superb conceptual question. Car 1 starts ahead "),
             ("m", r"(15.0 > 10.0)"), ("t", " and faster "), ("m", r"(23.50 > 15.50)"),
             ("t", ", while also accelerating, so the slower constant-speed Car 2 can never catch it "
                   "for "), ("m", r"t \ge 0"),
             ("t", ". The negative solutions describe where the paths would have crossed in the past "
                   "had the same equations held before release.")])

    # =====================================================================
    section_header(7, "The Speeding Car and the Motorcycle Trooper")
    problem("You are driving at a constant speed of 45.0 m/s when you pass a trooper on a motorcycle "
            "hidden behind a billboard. One second after your car passes the billboard, the trooper "
            "sets out from the billboard to catch you, accelerating at a constant 3.00 m/s\u00b2. "
            "How long does it take the trooper to overtake your car?")
    given_required(
        [
            [("t", "Car speed  "), ("m", r"v_{\text{car}} = 45.0\ \text{m/s}"), ("t", "  (constant)")],
            [("t", "Trooper acceleration  "), ("m", r"a = 3.00\ \text{m/s}^{2}"), ("t", "  (from rest)")],
            [("t", "Trooper starts 1.00 s after the car passes the billboard")],
        ],
        [
            [("t", "Time  "), ("m", r"t"), ("t", "  for the trooper to overtake the car")],
        ])
    solution_header()
    step("Method 1.", [("t", "Let "), ("m", r"t = 0"),
                       ("t", " be the moment the trooper starts. The car already had a 1.00 s head "
                             "start of "), ("m", r"45.0\ \text{m/s} \times 1.00\ \text{s} = 45.0\ \text{m}"),
                       ("t", ":")])
    derive(r"x_{\text{troop}}(t) &= \tfrac{1}{2}(3.00)\,t^{2} = 1.50\,t^{2} \\ "
           r"x_{\text{car}}(t) &= 45.0 + 45.0\,t")
    step("", [("t", "Set the positions equal and simplify:")])
    derive(r"1.50\,t^{2} &= 45.0 + 45.0\,t \\ 1.50\,t^{2} - 45.0\,t - 45.0 &= 0 \\ "
           r"t^{2} - 30.0\,t - 30.0 &= 0")
    derive(r"t &= \frac{30.0 \pm \sqrt{(30.0)^{2} + 120}}{2} = \frac{30.0 \pm \sqrt{1020}}{2} \\ "
           r"&\approx \frac{30.0 + 31.937}{2} \approx 31.0\ \text{s}")
    answer_box("Method 1", r"t \approx 31.0\ \text{s}", note="(measured from when the trooper starts)")
    step("Method 2.", [("t", "Let "), ("m", r"T = 0"),
                       ("t", " be the moment the car passes the billboard; the trooper's elapsed time "
                             "is "), ("m", r"(T - 1.00)"), ("t", ":")])
    derive(r"x_{\text{car}}(T) &= 45.0\,T \\ x_{\text{troop}}(T) &= \tfrac{1}{2}(3.00)(T - 1.00)^{2}")
    derive(r"1.50\,T^{2} - 3.00\,T + 1.50 &= 45.0\,T \\ 1.50\,T^{2} - 48.0\,T + 1.50 &= 0 \\ "
           r"T^{2} - 32.0\,T + 1.00 &= 0")
    derive(r"T &= \frac{32.0 \pm \sqrt{(32.0)^{2} - 4}}{2} = \frac{32.0 \pm \sqrt{1020}}{2} \\ "
           r"&\approx 32.0\ \text{s}")
    answer_box("Method 2", r"T \approx 32.0\ \text{s}", note="(measured from when the car passes the billboard)")
    insight([("t", "Present both methods side by side. Method 1 measures 31.0 s from the trooper's "
                   "start; Method 2 measures 32.0 s from the billboard \u2014 exactly 1.00 s more, "
                   "the head-start delay. Both place the overtaking at the same point "),
             ("m", r"(x \approx 1439\ \text{m})"),
             ("t", ", showing the physical event is independent of the chosen time origin.")])
