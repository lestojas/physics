# ILAW Lesson Plan Generator

A web application that helps DepEd Philippines teachers generate standards-aligned,
inclusive, and pedagogically sound lesson plans using the **ILAW 7-E framework**
(Elicit · Engage · Explore · Explain · Elaborate · Evaluate · Extend), with a
human-in-the-loop activity approval step and an automatic 9-criterion quality audit.

## What's here

| Document | Purpose |
|---|---|
| [`feature-specification.md`](./feature-specification.md) | Full product/engineering spec: architecture, Phases 1–4, data model, quality audit engine, non-functional requirements, and user flow. |
| [`system-prompt.md`](./system-prompt.md) | Production-ready AI system prompt that powers activity ideation, full plan generation, and the rubric self-audit. |

## The workflow at a glance

1. **Phase 1 — Competency & Curriculum Tracking:** Upload syllabus/MELCs; map prerequisite → target → next competency.
2. **Phase 2 — Context & Reference Ingestion:** Capture learning area, grade/section, sessions, learner context, and references.
3. **Phase 3 — Interactive Activity Pitch:** Review 3 options each for Engage/Explore/Elaborate; select, combine, or tweak.
4. **Phase 4 — Full ILAW Plan Generation:** Produce the complete DepEd ILAW plan (7 sections) as clean Markdown tables.

Every generated plan is auto-audited against 9 quality criteria (Alignment, Coherence,
Teachability, Pedagogical Design, Contextualization, Inclusivity, Embedded Assessment,
Validity, Actionable Interventions) and carries a **Declaration of AI Use** compliant with
**DepEd DO 3 s. 2026 (Annex A)**.

## Status

Draft design deliverables (v1). No application code yet — these documents define the
feature and the AI behavior to be implemented.
