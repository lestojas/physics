# Velocity Components Simulator

An interactive simulation of **uniform circular motion**. Adjust the radius, mass,
and one motion driver, then watch how the coupled quantities and the velocity /
centripetal-force vectors respond in real time.

## Running it

Open `index.html` in a browser, or launch it from the project landing page
(`../../index.html`). No server or build step is required.

## What you can explore

- **Inputs:** radius `r`, mass `m`, and a selectable **motion driver** — period
  `T`, tangential speed `v`, or angular speed `omega`.
- **Coupled quantities** stay mathematically consistent:
  - `v = 2*pi*r / T`
  - `omega = 2*pi / T`
  - `v = r*omega`
- **Derived quantities** shown live with units:
  - Centripetal acceleration: `a_c = v^2 / r = r*omega^2`
  - Net centripetal force: `F_net = m * a_c`
- **Visualization:** an animated object timed to the real period, with a
  **tangential velocity vector** (always perpendicular to the radius) and a
  toggleable **centripetal force vector** (always pointing toward the center).
- **Controls:** play, pause, reset, and a force-vector toggle.
- **Validation:** out-of-range values are clamped, non-positive/non-numeric
  entries are rejected or ignored, each with an inline message.

## File structure

```
velocity-components/
|-- index.html          # Page markup: canvas, panels, equation list + legend
|-- css/
|   `-- sim.css         # Layout and vector-color styling
|-- js/
|   |-- physics.js      # VCS.physics - pure model (coupling, derived values, validation)
|   |-- render.js       # VCS.render - canvas drawing, vectors, animation loop
|   |-- ui.js           # VCS.ui - control widgets and readouts
|   `-- main.js         # VCS.main - state, wiring, asset self-check
`-- tests/
    `-- lib/pbt.js      # Vendored property-based-testing helper (test-only)
```

## Architecture notes

- All modules attach to a single global namespace, `VCS`, and are loaded in
  dependency order (`physics` -> `render` -> `ui` -> `main`) via classic
  `<script>` tags.
- `physics.js` is DOM-free and side-effect-free, making it straightforward to
  unit- and property-test in isolation.
- Assets in `tests/` are **not** referenced by `index.html`, so the shipped page
  stays dependency-free.

## Default state

`r = 2 m`, `m = 1 kg`, driver = `T`, `T = 4 s` - which yields
`v ~= 3.142 m/s`, `omega ~= 1.571 rad/s`, and `a_c = F_net ~= 4.935`.
