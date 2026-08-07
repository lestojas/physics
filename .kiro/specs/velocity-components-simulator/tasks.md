# Implementation Plan: Velocity Components Simulator

## Overview

This plan converts the design into incremental, test-driven coding steps for a
zero-build, self-contained static web app (uniform circular motion). All simulator
assets live under `sims/velocity-components/` and are loaded via classic
`<script>` tags (NOT ES modules) so the app runs from `file://` with no server,
bundler, or external/CDN dependency. Code is namespaced under a single global
`VCS` object (`VCS.physics`, `VCS.render`, `VCS.ui`).

The build order is: scaffolding → pure physics model (with property tests) →
canvas rendering + animation (with property tests) → UI controls/readouts →
`main.js` wiring + equations + landing-page error handling → example / smoke /
integration tests. Each step builds on the previous and ends by wiring things
together, so no orphaned code remains.

Property-based tests use a small **vendored, zero-dependency** test helper so the
shipped simulator stays dependency-free; each property test runs a **minimum of
100 iterations** and is tagged
`Feature: velocity-components-simulator, Property {n}: {property_text}`.

## Tasks

- [ ] 1. Set up repository structure and self-contained scaffolding
  - [ ] 1.1 Create the simulator page shell and stylesheet
    - Create `sims/velocity-components/index.html` with the `<canvas>` Animation_View, and empty containers for the Control_Panel, Readout_Panel, Equation_Panel, and a hidden asset-error banner.
    - Include `physics.js`, `render.js`, `ui.js`, `main.js` at the bottom in dependency order via relative `src` classic `<script>` tags (NOT `type="module"`); link `sim.css` via relative `href`.
    - Create `sims/velocity-components/sim.css` with the panel/layout skeleton and CSS variables for the velocity vs. force colors.
    - Use only relative paths; issue no network/CDN request.
    - _Requirements: 2.1, 2.2, 2.4, 2.5, 2.6_

  - [ ] 1.2 Create the root landing page
    - Create `index.html` at the repository root as an extensible card list, with one visible, labeled control within the initial viewport that launches the Simulator via the relative path `sims/velocity-components/index.html`.
    - Add a hidden inline message element for launch-failure feedback (wired in task 7.3).
    - _Requirements: 1.1, 1.3, 1.5_

  - [ ] 1.3 Add the vendored zero-dependency property-test helper
    - Create a test-only helper (e.g., `sims/velocity-components/tests/lib/pbt.js`) providing value generators (bounded floats, driver picks, angle picks, invalid/edge strings, small-magnitude reals, frame-delta schedules), a `forAll(gen, predicate, {iterations>=100})` runner, and basic shrinking.
    - Keep this helper outside the simulator's loaded assets so it is never referenced by the shipped `index.html` (preserves Req 2.2).
    - _Requirements: 2.2_

- [ ] 2. Implement the pure physics model (`physics.js`)
  - [ ] 2.1 Implement coupled and derived computation
    - In `physics.js`, attach to `VCS.physics`: `RANGES` (r, m, T, v, omega with min/max/unit), `TAU`, `computeTriple(r, driver, driverValue)` (driver value kept exact; two non-driver quantities from `v=2πr/T`, `ω=2π/T`, `v=rω`, `T=2πr/v`, `ω=v/r`, `T=2π/ω`), `computeDerived(r, m, triple)` (`a_c=v²/r`, cross-check `rω²`, `F_net=m·a_c`, non-negative), and `computeMotion(state)`.
    - _Requirements: 4.1, 4.2, 4.3, 4.4, 4.5, 5.1, 5.2, 5.3, 5.4, 5.5, 5.6_

  - [ ]* 2.2 Write property test for temporal coupling consistency
    - **Property 1: Temporal coupling consistency** — `v=2πr/T`, `ω=2π/T`, `v=rω` each hold within 0.1% for all valid states.
    - **Validates: Requirements 4.1, 4.2, 4.3, 4.4**

  - [ ]* 2.3 Write property test for exact driver retention
    - **Property 2: Driver value retained exactly** — the driven quantity in the triple equals the entered value with no drift.
    - **Validates: Requirements 4.5**

  - [ ]* 2.4 Write property test for acceleration consistency
    - **Property 4: Centripetal acceleration consistency** — `a_c=v²/r` and `a_c=rω²` agree within 0.1%.
    - **Validates: Requirements 5.1, 5.2, 5.5**

  - [ ]* 2.5 Write property test for force consistency
    - **Property 5: Centripetal force consistency** — `F_net=m·a_c` and `F_net=m·v²/r` agree within 0.1%.
    - **Validates: Requirements 5.3, 5.4**

  - [ ]* 2.6 Write property test for non-negative magnitudes
    - **Property 6: Non-negative acceleration and force** — `a_c >= 0` and `F_net >= 0` for all valid states.
    - **Validates: Requirements 5.6**

  - [ ] 2.7 Implement input classification, driver switching, and formatting
    - In `physics.js`, add `classifyInput(field, raw)` returning status `accepted | clamped | rejected | ignored` (non-numeric/empty → ignored; `<=0` → rejected; `>0` out-of-range → clamped to nearest bound; in-range → accepted), `switchDriver(state, newDriver)` (preserve `{T,v,ω}`, set `driverValue` to the current value of the new driver), and `formatValue(x)` (≤3 decimals; for `0<|x|<0.001` preserve ≥1 significant figure instead of `0.000`).
    - _Requirements: 3.5, 3.6, 3.7, 3.9, 3.10, 4.6, 4.7, 6.3, 6.4, 11.1, 11.2, 11.3, 11.4, 11.5, 11.6_

  - [ ]* 2.8 Write property test for range clamping
    - **Property 7: Range clamping of numeric inputs** — any strictly-positive value is accepted within range or mapped to the nearest bound.
    - **Validates: Requirements 3.5, 3.6, 3.7, 3.9, 3.10, 11.5**

  - [ ]* 2.9 Write property test for driver-switch preservation and echo
    - **Property 3: Driver-switch preservation and echo** — switching drivers without new input preserves `T`, `v`, `ω` within 0.1% and echoes the preserved value into the new driver input.
    - **Validates: Requirements 4.6, 4.7**

  - [ ]* 2.10 Write property test for numeric formatting rules
    - **Property 10: Numeric formatting rules** — `formatValue` output has ≤3 decimals and preserves ≥1 significant figure for tiny nonzero magnitudes.
    - **Validates: Requirements 6.3, 6.4**

- [ ] 3. Checkpoint - physics model
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 4. Implement canvas rendering and animation (`render.js`)
  - [ ] 4.1 Implement coordinate mapping, canvas init, and object placement
    - In `render.js`, attach to `VCS.render`: `init(canvas, getState, getViewOptions)`; compute `center`, the monotonic `mapRadius(r)` (linear `r∈[0.1,10]` → `[R_min_px, R_max_px]` with margin reserved for vectors/labels so the whole path fits), and the object position `center + R_px·(cosθ, sinθ)`; draw the circular path and the object.
    - _Requirements: 7.1, 7.2_

  - [ ]* 4.2 Write property test for path radius scaling and containment
    - **Property 11: Path radius monotonic scaling and containment** — `r1<r2 ⇒ R_px(r1)<R_px(r2)`, and the path plus margin always fits the Animation_View bounds.
    - **Validates: Requirements 7.1**

  - [ ] 4.3 Implement velocity and force vector geometry and drawing
    - Compute radial unit `u_c=(center-obj)/|center-obj|` and tangent unit `u_v=direction·(-sinθ, cosθ)`; draw the Velocity_Vector (tail=obj, dir=`u_v`, `L_v=k_v·v`, optional readability clamp) and the Force_Vector (tail=obj, dir=`u_c`, `L_f=clamp(k_f·F_net, 0.05·R_px, 1.00·R_px)`) with arrowheads, distinct colors, and text labels; skip the Force_Vector when force display is disabled.
    - _Requirements: 8.1, 8.2, 8.3, 8.5, 8.6, 9.1, 9.2, 9.4, 9.5, 9.6, 9.7_

  - [ ]* 4.4 Write property test for object and vector anchoring
    - **Property 12: Object and vectors anchored on the path** — object distance from center equals `R_px` within epsilon and both vector tails coincide with the object position for all θ.
    - **Validates: Requirements 7.2, 8.1, 9.1**

  - [ ]* 4.5 Write property test for velocity vector orientation
    - **Property 15: Velocity vector orientation** — perpendicular to the radius (90°±1°) and along direction of travel (0°±1°) for all θ.
    - **Validates: Requirements 8.2, 8.3, 8.4**

  - [ ]* 4.6 Write property test for velocity vector length scaling
    - **Property 16: Velocity vector length monotonic in speed** — `v1<v2 ⇒ L_v(v1)<L_v(v2)`.
    - **Validates: Requirements 8.6**

  - [ ]* 4.7 Write property test for force vector orientation
    - **Property 17: Force vector orientation toward center** — points object→center (0°±1°) for all θ.
    - **Validates: Requirements 9.2, 9.3**

  - [ ]* 4.8 Write property test for force vector length linearity
    - **Property 18: Force vector length linearity (pre-clamp)** — unclamped `L_f/F_net = k_f` within 1% across valid states.
    - **Validates: Requirements 9.5**

  - [ ]* 4.9 Write property test for force vector clamping bounds
    - **Property 19: Force vector length clamping bounds and idempotence** — displayed length ∈ `[0.05·R_px, 1.00·R_px]` and clamping is idempotent.
    - **Validates: Requirements 9.6**

  - [ ] 4.10 Implement the rAF render loop and play/pause/reset state machine
    - Add the `requestAnimationFrame` loop with wall-clock `dt` integration `θ += direction·(2π/T)·dt` (one revolution per real `T`); expose `play()`, `pause()`, `reset()` (to `initialTheta`, paused), `isPlaying()`, `currentAngle()`; redraw path, object, and both vectors each frame.
    - _Requirements: 7.3, 7.4, 7.5, 7.6, 7.7, 8.4, 9.3_

  - [ ]* 4.11 Write property test for revolution timing
    - **Property 13: Revolution timing matches real period** — for any frame-delta schedule summing to `T`, integration advances exactly `2π` within 5%.
    - **Validates: Requirements 7.3**

  - [ ]* 4.12 Write property test for reset invariance
    - **Property 14: Reset invariance** — reset from any θ, playing or paused, returns to `initialTheta` and enters the paused state.
    - **Validates: Requirements 7.7**

- [ ] 5. Checkpoint - rendering and animation
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 6. Implement UI controls and readouts (`ui.js`)
  - [ ] 6.1 Build the Control_Panel widgets and animation controls
    - In `ui.js`, attach to `VCS.ui`: `buildControls(root, handlers)` creating inputs for r (m) and m (kg), the active-driver input (s / m·s⁻¹ / rad·s⁻¹), a driver `<select>` (T/v/ω, default T), a force-display toggle, and play/pause/reset buttons; wire change/click handlers to callbacks.
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.11, 7.4, 9.7_

  - [ ] 6.2 Implement readouts, driver echo, validation messages, and asset banner
    - Add `updateReadouts(values)` (r, m, T, v, ω, a_c, F_net with units, via `formatValue`), `echoDriverInput(driver, value)`, per-field `showMessage`/`clearMessage`, and `showAssetError(text)` banner control.
    - _Requirements: 6.1, 6.2, 6.3, 6.4, 4.7, 11.2, 11.3, 11.4, 11.6, 11.7, 1.6, 2.7_

- [ ] 7. Integration and wiring
  - [ ] 7.1 Implement the application bootstrap and orchestration (`main.js`)
    - In `main.js`, hold the authoritative MotionState (defaults r=2, m=1, driver="T", T=4), run the asset self-check (verify `VCS.physics`/`VCS.render`/`VCS.ui` exist and `canvas.getContext("2d")` is available, else show the banner), and orchestrate the flow: input change → `classifyInput` → on accepted/clamped `computeMotion` → `updateReadouts` + echo + push MotionState to `render` (all ≤100 ms); on rejected/ignored keep last valid state and show the message; wire play/pause/reset and the force toggle; populate readouts from defaults before any interaction.
    - _Requirements: 3.8, 4.1, 5.7, 6.5, 6.6, 6.7, 9.7, 11.1, 11.3, 11.4, 11.5, 11.6, 11.7, 2.7_

  - [ ] 7.2 Build the Equation_Panel content and legend
    - In `sims/velocity-components/index.html` (+ `sim.css` styling), render `v=2πr/T`, `ω=2π/T`, `v=rω`, `a_c=v²/r`, `a_c=rω²`, `F_net=m·a_c`, `F_net=m·v²/r` with legible Unicode/CSS notation (π, ω, ², subscripts, ·) and a legend defining all seven symbols with names and units.
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5, 10.6_

  - [ ] 7.3 Wire the landing-page launch and failure fallback
    - In the root `index.html`, activate the launch control to navigate to the Simulator (Animation_View visible) and, on a guarded navigation/open failure, show the inline message and remain on the Landing_Page — with no network call.
    - _Requirements: 1.4, 1.6_

- [ ] 8. Checkpoint - full app wired
  - Ensure all tests pass, ask the user if questions arise.

- [ ] 9. Example, smoke, and integration tests
  - [ ]* 9.1 Write example-based unit tests
    - Default load state equals `computeMotion(defaults)` with driver T; Control_Panel/Readout_Panel presence, labels, and units; pause holds position and play resumes; velocity/force colors differ and each has its label; disabling force hides the Force_Vector; Equation_Panel equations and legend present with legible symbols.
    - _Requirements: 3.1, 3.2, 3.3, 3.4, 3.11, 6.1, 6.2, 6.5, 7.5, 7.6, 8.5, 9.4, 9.7, 10.1, 10.2, 10.3, 10.4, 10.5, 10.6, 11.2, 11.3, 11.4, 11.6_

  - [ ]* 9.2 Write smoke/structure tests
    - Root `index.html` exists; `sims/` exists; every simulator asset resides under `sims/velocity-components/`; all `src`/`href` references are relative.
    - _Requirements: 1.1, 2.1, 2.2, 2.6_

  - [ ]* 9.3 Write `file://` integration and performance tests
    - Landing_Page and Simulator render and animate from disk with zero external network requests and no build/server; launch reaches the visible Animation_View within 2 s; render loop sustains ≥30 FPS over 1 s intervals; readouts update within 100 ms of input changes; simulated asset-load and simulator-open failures show their messages.
    - _Requirements: 1.2, 1.4, 2.3, 2.4, 2.5, 7.8, 3.8, 5.7, 6.6, 2.7, 1.6_

- [ ] 10. Final checkpoint - Ensure all tests pass
  - Ensure all tests pass, ask the user if questions arise.

## Notes

- Tasks marked with `*` are optional test sub-tasks and can be skipped for a faster MVP; core implementation sub-tasks are never optional.
- Each task references specific requirements (and, for property tests, a design property) for traceability.
- Property tests (Properties 1–19) each use the vendored zero-dependency helper, run ≥100 iterations, and are tagged `Feature: velocity-components-simulator, Property {n}: ...`. Tolerances: 0.1% for coupling/derived (P1–P5), 1° for vector angles (P15, P17), 1% for force linearity (P18), 5% for revolution timing (P13).
- The shipped simulator uses classic `<script>` tags under a single `VCS` namespace and relative paths only; the test helper and test files are never referenced by the shipped `index.html`, preserving the self-contained, dependency-free deliverable.
- Checkpoints ensure incremental validation between the physics, rendering, wiring, and final phases.

## Task Dependency Graph

```json
{
  "waves": [
    { "id": 0, "tasks": ["1.1", "1.2", "1.3", "2.1", "4.1", "6.1"] },
    { "id": 1, "tasks": ["2.7", "2.2", "2.3", "2.4", "2.5", "2.6", "4.3", "4.2", "6.2"] },
    { "id": 2, "tasks": ["2.8", "2.9", "2.10", "4.10", "4.4", "4.5", "4.6", "4.7", "4.8", "4.9"] },
    { "id": 3, "tasks": ["7.1", "4.11", "4.12", "7.2", "7.3"] },
    { "id": 4, "tasks": ["9.1", "9.2", "9.3"] }
  ]
}
```
