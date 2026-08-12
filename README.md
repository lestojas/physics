# PHYlip Simulators

A collection of interactive, **zero-setup** physics simulators that run directly
in the browser. Open `index.html` and pick a simulator - no build step and no
external/network dependencies.

Developed by Philip Jayson Lestojas.

## Quick start

1. Open `index.html` (repository root) in a browser and click a simulator card.
2. Every simulator also works on its own - open any file in `sims/` directly.

> Tip: the collapsible sidebar auto-discovers simulators when the folder is
> served by a local web server. When opened via `file://` (double-click), it
> falls back to a built-in list (see `sidebar.js`), which already includes all
> current simulators.

## Simulators

All simulators live in the `sims/` folder, one `.html` file each:

| Simulator | Topic | File |
| --- | --- | --- |
| Uniform Circular Motion | 4-in-1: tangential speed, period & frequency, centripetal acceleration, centripetal force | `sims/uniform-circular-motion.html` |
| Projectile Motion | The common cases of projectile motion | `sims/projectile-motion.html` |
| Falling Target | Why an aimed projectile always hits a target dropped at launch | `sims/falling-target.html` |

## Repository layout

```
.
|-- index.html                       # Landing page (cards for every simulator)
|-- styles.css                       # Shared site styles
|-- sidebar.js                       # Shared, auto-discovering collapsible sidebar
|-- README.md
`-- sims/                            # All simulators, one .html file each
    |-- velocity-components.html
    |-- projectile-motion.html
    |-- falling-target.html
    `-- _template.html               # Starter template (files starting with "_" are ignored)
```

## Adding a new simulator

1. Copy `sims/_template.html` to `sims/<your-sim-name>.html` (lowercase, hyphens).
2. Change the `<title>` and heading, and build the simulator inside
   `<main class="content">`. Keep the two lines that load `../styles.css` and
   `../sidebar.js`.
3. Add a matching card to `index.html`. For reliable `file://` navigation, also
   add the filename to the `FALLBACK` list in `sidebar.js`.

## Conventions

- **No build tooling** - plain HTML, CSS, and JavaScript.
- **Classic `<script>` blocks**, not ES modules, so pages load from `file://`.
- **Relative paths only**, **no CDN/network requests** - works fully offline.
- Simulators with heavier logic namespace their JavaScript (e.g. Velocity
  Components uses a single global `VCS` object) and prefix any sim-specific CSS
  classes that would otherwise collide with `styles.css`.

## Specifications

Design and requirements documents live under `.kiro/specs/`, organized by feature.
