# Physics Simulations

A collection of interactive, **zero-setup** physics simulations that run directly
in the browser. There is no build step, no server, and no external/network
dependencies - just open `index.html` and pick a simulation.

## Quick start

1. Clone or download this repository.
2. Open `index.html` (at the repository root) in a web browser - a double-click
   works, since everything runs over `file://`.
3. Click **Launch simulator** on any card.

## Simulations

Every simulation is a **single self-contained `.html` file** living in the
`sims/` folder (CSS and JavaScript are inlined, so each file works on its own).

| Simulation | Topic | File |
| --- | --- | --- |
| Velocity Components Simulator | Uniform circular motion - period, tangential/angular speed, centripetal acceleration & force | `sims/velocity-components.html` |

## Repository layout

```
.
|-- index.html                       # Landing page linking to every simulation
|-- README.md                        # This file
`-- sims/                            # All simulations, one .html file each
    `-- velocity-components.html     # Uniform circular motion simulator
```

## Adding a new simulation

1. Create a new single self-contained file `sims/<your-sim-name>.html` with its
   CSS and JavaScript inlined (no external assets, relative links only).
2. Add a new `<li class="sim-card">` card to the landing page (`index.html`)
   pointing at `sims/<your-sim-name>.html`.

That's it - the new simulation lives alongside the others in the same folder.

## Design conventions

- **No build tooling.** Plain HTML, CSS, and JavaScript only.
- **Single-file simulations.** Each simulator is one `.html` file with inline
  `<style>` and `<script>` blocks - simple to open, copy, or share.
- **Classic `<script>` blocks**, not ES modules, so pages load correctly from
  `file://` (ES-module imports are blocked by browser CORS rules on `file://`).
- **No CDN/network requests**, so a simulation works fully offline.
- Each simulation namespaces its JavaScript under a single global object to avoid
  collisions.

## Specifications

Design and requirements documents live under `.kiro/specs/`, organized by feature.
