# Feature Specification — ILAW Lesson Plan Generator

**Version:** 1.0
**Owner:** Instructional Design + Full-Stack Engineering
**Status:** Implemented (MVP)

---

## 1. Purpose

Provide DepEd Philippines teachers a guided web tool that uses Claude AI to draft
**ILAW (7Es) lesson plans** that are curriculum-aligned, inclusive, and
classroom-ready, while keeping the teacher firmly in control (human-in-the-loop).

## 2. Goals & Non-Goals

**Goals**
- Generate complete ILAW lesson plans that pass a built-in 9-criteria quality audit.
- Track vertical competency alignment (prerequisite → target → future).
- Let teachers approve/tweak activity ideas before the full plan is written.
- Keep the Anthropic API key private (server-side only).
- Declare AI use per DO 3, s. 2026, Annex A in every output.

**Non-Goals (MVP)**
- User accounts, authentication, and multi-user persistence.
- A database or long-term storage of plans (output is copy/download only).
- Editing the rendered plan inline (teacher edits after copy/download).
- OCR of scanned image-only PDFs.

## 3. Users

- **Primary:** Public/private school teachers preparing lesson plans.
- **Secondary:** Master teachers / instructional coaches reviewing plans.

## 4. System Architecture

```
Browser (Next.js client)
   │  fetch()
   ▼
Next.js API routes (server, Node.js runtime)   ← ANTHROPIC_API_KEY lives here only
   │  @anthropic-ai/sdk
   ▼
Anthropic Claude Messages API
```

- **Framework:** Next.js 14 (App Router), React 18, TypeScript.
- **AI:** Anthropic Claude via `@anthropic-ai/sdk`; model configurable via `CLAUDE_MODEL`.
- **File parsing (server):** `pdf-parse` (PDF), `mammoth` (DOCX), native UTF-8 (TXT/MD).
- **Rendering:** `react-markdown` + `remark-gfm` for GFM tables.

### 4.1 API Endpoints

| Route | Phase | Input | Output |
|-------|-------|-------|--------|
| `POST /api/parse` | 1 & 2 | multipart files | `{ combinedText, files[] }` |
| `POST /api/map` | 1 | `{ syllabusText, targetCompetency }` | `{ mapping }` (JSON) |
| `POST /api/activities` | 3 | `{ context }` | `{ activities }` (JSON) |
| `POST /api/generate` | 4 | `{ context, selectedActivities, tweaks }` | `{ markdown }` |

All AI routes run on the Node.js runtime and never expose the API key to the client.

## 5. Functional Requirements — the 4 Phases

### Phase 1 — Competency & Curriculum Tracking
- Accept uploads of curriculum guides / MELCs / syllabi (PDF, DOCX, TXT, MD).
- From the uploaded text + a user-chosen target competency, produce:
  - **Prerequisite** competency(ies)
  - **Target** competency (cleaned)
  - **Future/Next** competency(ies)
  - Suggested Content & Performance Standards
- If the source lacks explicit progression, infer from standard K-12 progression and flag it.

### Phase 2 — Context & Reference Ingestion
- Capture: Teacher Name, Learning Area*, Grade Level*, Section, No. of Sessions,
  Target Competency*, Content/Performance Standards, Learner Context.
- Optionally ingest reference materials (books, toolkits, PDFs, notes).
- Pedagogical freedom: allow evidence-based external strategies beyond the references.

### Phase 3 — Interactive Activity Pitch (Human-in-the-Loop)
- Present **exactly 3 distinct options** for **Engage, Explore, Elaborate**.
- Each option: title, description, materials, pedagogical rationale, inclusivity note.
- Teacher selects one per stage (optional), adds free-text tweaks, or re-pitches.

### Phase 4 — Full ILAW Lesson Plan Generation
Output sections (clean Markdown, tables where structured):
1. Header & Metadata + **Declaration of AI Use** (DO 3 s. 2026 Annex A)
2. Intentions
3. Learning Competency & Curriculum Standards
4. Learning Objectives (SMART)
5. Learner Context
6. Learning Experience (**7Es**: ELICIT, ENGAGE, EXPLORE, EXPLAIN, ELABORATE, EVALUATE, EXTEND)
7. Reflections & Self-Assessment (10-row Yes/No/Notes table)
8. Quality Assurance table confirming the 9-criteria audit

## 6. Quality & Rubric Compliance Audit

Every plan is self-audited by the model against these 9 criteria before rendering, with
a confirmation table appended:

1. Alignment 2. Coherence 3. Teachability 4. Pedagogical Design 5. Contextualization
6. Inclusivity 7. Embedded Assessment 8. Validity 9. Actionable Interventions ("Ways Forward")

## 7. Non-Functional Requirements

- **Security:** API key server-side only; `.env.local` git-ignored; no key in client bundle.
- **Privacy:** Files parsed in memory; not persisted by the app.
- **Resilience:** Robust JSON parsing of model replies (tolerates code fences/prose).
- **Limits:** Per-file text capped (~60k chars) to control prompt size/cost.
- **Configurability:** All AI behavior centralized in `src/lib/prompts.ts`.

## 8. Future Enhancements

- DOCX/PDF export of the finished plan (not just Markdown).
- Saved plans + teacher accounts.
- Streaming responses for faster perceived generation.
- OCR for scanned PDFs.
- Alignment to a specific uploaded DepEd ILAW template file (byte-for-byte fidelity).
- Batch generation across multiple competencies / a full unit.
