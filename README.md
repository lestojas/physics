# Physics League — Kinematics Championship (Game-Show Screenshow)

A **completely standalone**, zero-setup web app that serves as the **main screen
show** for the gamified *Physics League: Kinematics Championship*. It runs the
entire game from a single page — open `index.html` in a browser. No build step,
no external/network dependencies, works fully offline.

> This is its own separate web, independent of any other project. Everything the
> show needs lives in `index.html`.

Developed by Philip Jayson Lestojas.

## Quick start

- Double-click `index.html` (or serve the folder) and run the show from the
  browser. Click **⛶ Fullscreen** for presentation mode.

## Features

- **Built-in per-question timer** — Round 1: 20 s, Round 2: 5 min, Round 3: 50 s —
  with start / pause / reset and a countdown warning + beep in the final seconds.
- **Manual answer reveal** — the answer stays hidden until you click *Reveal Answer*.
- **One-click scoring for 6 groups** — after the reveal, click every group that
  answered correctly. Round 2 uses **Full (+30) / Partial (+15)** buttons plus the
  **Flip-First** star.
- **Live per-problem points (Round 2)** — each group's row shows the points it
  earned on the current problem, updating instantly as you set Full / Partial /
  Flip-First and toggle the Mystery Multiplier.
- **No always-on scoreboard** — running totals are intentionally hidden so the
  standings never spoil the excitement. Open the sortable **🏆 Leaderboard**
  overlay only when you want to reveal them (great for the finale). It's a
  **table with a per-round score breakdown** (R1 / R2 / R3 / Total).
- **Browse Questions** — the **☰ Questions** menu lists every slide (with which
  ones are revealed / scored) so you can jump straight to a previous question and
  edit its score; totals recalculate instantly.
- **Thrilling, phase-based audio** — distinct, driving game-show beds for the
  **question** (beat-the-clock groove), the **answer reveal** (triumphant
  fanfare), and **scoring** (high-energy tally groove), plus sound effects:
  rising final-3-seconds countdown ticks, a dramatic time's-up buzzer, a reveal
  flourish, and a reward chime when a group is awarded points. All synthesized
  live with the Web Audio API — no audio files, fully offline. Toggle with
  **♪ Music** and set the volume.
- **Editable team names** and **persistent scores** — everything is saved in the
  browser (localStorage) and **survives a page refresh**; it only clears when you
  press *Reset scores*.

## Twists (all built in)

| Round | Twist | Behavior |
| --- | --- | --- |
| 1 | **Double Trouble** | Two questions are secretly worth **+20**; the value is revealed only *after* boards are up. |
| 2 | **Flip First** | The first team to finish correctly gets a **+5** bonus (star button). |
| 2 | **Mystery Multiplier** | A toggle that makes one problem worth **double points**. |
| 3 | **Wildcard** | One question is worth **3× points (+45)**, revealed only after boards are up. |

## Rounds

- **Round 1 — Rapid Recall** (10 conceptual questions, 20 s each, +10 each).
- **Round 2 — Problem Showdown** (3 numerical problems, ~5 min each, +30 full / +15 partial).
- **Round 3 — Lightning Final** (5 mixed questions, ~50 s each, +15 each).

Max points with no twists triggered: **R1 = 120, R2 = 90, R3 = 105 → 315 total.**

> **Round 1 order (per host request):** the original Q1 is shown as **Q8**, the
> original Q8 as **Q9**, and the original Q9 as **Q1**. All other Round 1
> questions keep their number. Double Trouble sits on displayed positions 4 and 8.

## Keyboard shortcuts

| Key | Action |
| --- | --- |
| <kbd>Space</kbd> | Start / pause the timer |
| <kbd>&larr;</kbd> / <kbd>&rarr;</kbd> | Previous / next question |
| <kbd>R</kbd> | Reveal the answer |
| <kbd>Esc</kbd> | Close an open overlay |

## Conventions

- **No build tooling** — plain HTML, CSS, and JavaScript in one self-contained file.
- **Classic `<script>` block**, not an ES module, so it loads from `file://`.
- **No CDN / network requests** — works fully offline.
