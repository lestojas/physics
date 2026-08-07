# Physics Simulations

A collection of interactive, **zero-setup** physics simulations that run directly
in the browser. There is no build step, no server, and no external/network
dependencies - just open `index.html` in any modern browser and pick a simulation.

## Quick start

1. Clone or download this repository.
2. Open `index.html` (at the repository root) in a web browser - a double-click
   works, since everything runs over `file://`.
3. Click **Launch simulator** on any card.

## Simulations

| Simulation | Topic | Folder |
| --- | --- | --- |
| Velocity Components Simulator | Uniform circular motion - period, tangential/angular speed, centripetal acceleration & force | `sims/velocity-components/` |

## Repository layout

```
.
|-- index.html                     # Landing page linking to every simulation
|-- README.md                      # This file
`-- sims/                          # One self-contained folder per simulation
    `-- velocity-components/
        |-- index.html             # The simulation page
        |-- css/                   # Stylesheets
        |   `-- sim.css
        |-- js/                    # Simulation scripts (loaded as classic scripts)
        |   |-- physics.js         # Pure computation model
        |   |-- render.js          # Canvas rendering + animation loop
        |   |-- ui.js              # Controls & readouts
        |   `-- main.js            # Bootstrap / wiring
        |-- tests/                 # Test-only assets (not shipped with the page)
        |   `-- lib/pbt.js         # Vendored zero-dependency property-test helper
        `-- README.md              # Simulation-specific documentation
```

## Adding a new simulation

The layout is intentionally extensible:

1. Create a new folder under `sims/<your-sim-name>/` following the same
   `index.html` + `css/` + `js/` structure.
2. Add a new `<li class="sim-card">` card to the landing page (`index.html`) that
   links to `sims/<your-sim-name>/index.html`.

## Design conventions

- **No build tooling.** Plain HTML, CSS, and JavaScript only.
- **Classic `<script>` tags**, not ES modules, so pages load correctly from
  `file://` (ES-module imports are blocked by browser CORS rules on `file://`).
- **Relative paths only** and **no CDN/network requests**, so a simulation can be
  copied, zipped, or hosted anywhere and still work offline.
- Each simulation namespaces its JavaScript under a single global object to avoid
  collisions.

## Specifications

Design and requirements documents live under `.kiro/specs/`, organized by feature.
