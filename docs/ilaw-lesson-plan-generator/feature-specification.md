# ILAW Lesson Plan Generator — Feature Specification

**Version:** 1.0
**Status:** Draft for review
**Audience:** Product, Engineering, Instructional Design
**Compliance anchor:** DepEd DO 3 s. 2026 (Annex A — Declaration of AI Use)

---

## 1. Purpose & Vision

The **ILAW Lesson Plan Generator** is a web application that helps Philippine public
and private school teachers produce standards-aligned, inclusive, and pedagogically
sound lesson plans using the DepEd **ILAW** framework (a 7-E learning experience model:
Elicit, Engage, Explore, Explain, Elaborate, Evaluate, Extend).

The system pairs an **Instructional Design engine** (curriculum alignment + rubric
compliance) with an **AI generation engine** (activity ideation + full plan authoring),
keeping the teacher in control through a human-in-the-loop approval step.

### Design principles
- **Teacher-in-command:** AI proposes, the teacher decides. No plan is finalized without approval.
- **Standards-first:** Every plan is traceable to a competency (prerequisite → target → next).
- **Inclusive by default:** Accommodations and differentiation are required fields, not afterthoughts.
- **Auditable & compliant:** Every plan passes a 9-criterion rubric audit and carries a Declaration of AI Use.

---

## 2. System Architecture Overview

```
┌──────────────────────────────────────────────────────────────────────┐
│                            Web Client (SPA)                            │
│   Wizard UI · Uploads · Activity Pitch Review · Plan Viewer/Editor     │
└───────────────┬───────────────────────────────────┬───────────────────┘
                │ REST/JSON + SSE (streaming)         │
┌───────────────▼───────────────┐   ┌────────────────▼──────────────────┐
│        Application API         │   │        AI Orchestration            │
│  Auth · Projects · Documents   │   │  Prompt assembly · LLM calls       │
│  Competency graph · Audit svc  │   │  Activity pitch · Plan generation  │
└───────┬───────────────┬────────┘   └───────────┬────────────────────────┘
        │               │                         │
┌───────▼──────┐ ┌──────▼───────┐  ┌──────────────▼───────────┐
│  Relational  │ │ Object store │  │  Document parsing +       │
│  DB (meta,   │ │ (uploads,    │  │  vector index (RAG over   │
│  plans,graph)│ │  exports)    │  │  syllabi & references)    │
└──────────────┘ └──────────────┘  └───────────────────────────┘
```

### Suggested technology stack
| Layer | Recommendation | Notes |
|---|---|---|
| Frontend | React + TypeScript, Tailwind | Wizard/stepper UX, Markdown table rendering |
| Backend API | Node.js (NestJS) or Python (FastAPI) | Whichever the team prefers; FastAPI pairs well with parsing/ML libs |
| Database | PostgreSQL | Relational data + `pgvector` for embeddings |
| Object storage | S3-compatible | Uploaded references + exported plans |
| Document parsing | PDF/DOCX/TXT extractors + OCR fallback | e.g., `pdfplumber`, `python-docx`, Tesseract |
| AI layer | LLM via provider API | System prompt in companion doc; streaming responses |
| Export | Markdown → DOCX/PDF | Preserve DepEd table structure |

---

## 3. Functional Requirements by Phase

### Phase 1 — Competency & Curriculum Tracking

**3.1 Syllabus parsing**
- Accept uploads: **PDF, DOCX, TXT** (curriculum guides, MELCs, subject syllabi).
- Extract text, normalize into a structured competency list (code, description, domain, quarter).
- OCR fallback for scanned/image PDFs; flag low-confidence extractions for teacher review.

**3.2 Prerequisite & vertical alignment mapping**
For a teacher-selected **Target Competency**, the system surfaces:
1. **Prerequisite / Previous Competency** — prior knowledge learners should already hold.
2. **Target Competency** — the focus of the current lesson.
3. **Future / Next Competency** — where the lesson leads in the progression.

- Mapping is inferred from the parsed syllabus ordering + semantic similarity, then presented
  as an editable suggestion (teacher can override any of the three).

**Acceptance criteria**
- Uploading a valid MELC document produces a browsable, searchable competency list.
- Selecting any target competency renders a prerequisite/target/next triad that the teacher can edit.

---

### Phase 2 — Context & Reference Ingestion

**Structured inputs**
- Learning Area, Grade Level, Section, Number of Sessions.
- Target Learning Competency & Curriculum Standards (linked from Phase 1).
- **Learner Context:** teacher observations — strengths, interests, barriers, readiness levels, language needs.

**Reference materials**
- Upload/attach: books, toolkits, PDFs, Markdown; add URLs.
- References are parsed and indexed for retrieval-augmented generation (RAG).

**Pedagogical freedom**
- The generator respects uploaded references **and** may introduce creative, evidence-based
  activities from external pedagogical sources. Any externally-sourced technique is labeled as such.

**Acceptance criteria**
- All required metadata fields validated before advancing.
- At least the Learner Context free-text is captured (required, cannot be empty).
- Uploaded references are retrievable and cited when used in generation.

---

### Phase 3 — Interactive Activity Pitch (Human-in-the-Loop)

- Before authoring the full plan, the system presents **3 distinct activity options** for the
  key stages: **Engage, Explore, Elaborate** (extensible to other E-stages).
- Each option includes: title, short rationale, materials, time estimate, differentiation note,
  and which rubric criteria it strengthens.
- Teacher actions per stage: **Select · Combine · Request tweak · Regenerate.**
- No full plan is generated until the teacher confirms selections.

**Acceptance criteria**
- Exactly 3 options are offered per key stage.
- Teacher choices (including combinations and tweak requests) are persisted and feed the final generation.
- A clear "Approve & Generate Plan" gate exists.

---

### Phase 4 — Full ILAW Lesson Plan Generation

Output strictly follows the DepEd **ILAW template**:

1. **Header & Metadata** — Lesson Title, Learning Area, Teacher Name, Grade/Section, Sessions,
   References, and **Declaration of AI Use** citing compliance with **DO 3 s. 2026 (Annex A)**.
2. **Intentions** — mastery goals aligned to learner context.
3. **Learning Competency & Curriculum Standards** — explicit statements of what learners learn/know.
4. **Learning Objectives** — SMART (Specific, Measurable, Achievable, Relevant, Time-bound).
5. **Learner Context** — strengths, interests, barriers, readiness levels.
6. **Learning Experience (7Es / ILAW):** Elicit · Engage · Explore · Explain · Elaborate · Evaluate · Extend.
7. **Reflections & Self-Assessment Checklist** — standard 10-point reflection table (Yes/No/Notes).

**Rendering & editing**
- Rendered as clean **Markdown tables**; fully editable in-app.
- Export to DOCX/PDF preserving table structure.

**Acceptance criteria**
- All 7 template sections present and populated.
- Metadata includes a valid, non-empty Declaration of AI Use referencing DO 3 s. 2026 Annex A.
- The plan is only rendered after passing the Quality Audit (Section 4).

---

## 4. Quality & Rubric Compliance Audit

Every generated plan is auto-evaluated against **9 criteria** before rendering. Each criterion
receives a status (**Pass / Needs Work**), evidence pointer (section reference), and, if failing,
an actionable fix. The plan renders only after all criteria pass or the teacher explicitly overrides.

| # | Criterion | What it checks |
|---|---|---|
| 1 | **Alignment** | Intentions aligned to competencies, objectives, and expected outcomes |
| 2 | **Coherence** | Intentions consistently evident across objectives, activities, assessment, closure |
| 3 | **Teachability** | Another teacher can implement with minimal extra explanation |
| 4 | **Pedagogical Design** | Sound engagement, sequencing, scaffolding, active participation, meaningful processing |
| 5 | **Contextualization** | Integration, localization, contextualization, real-life connections |
| 6 | **Inclusivity** | Support for disabilities, barriers, language needs, varied readiness, unique contexts |
| 7 | **Embedded Assessment** | Assessment embedded throughout to monitor progress and identify support needs |
| 8 | **Validity** | Assessments align with intentions and yield valid evidence of learning |
| 9 | **Actionable Interventions** | "Ways Forward" interventions actionable for remediation/enrichment/adjustment |

**Audit UX**
- Displayed as a compliance panel next to the plan (per-criterion badges + expandable evidence).
- Failing criteria offer a one-click "Ask AI to fix this" action that regenerates only the affected section.

---

## 5. Data Model (core entities)

| Entity | Key fields |
|---|---|
| `User` | id, name, role (teacher/admin), school, division |
| `Project` (lesson plan workspace) | id, owner, learning_area, grade_level, section, sessions |
| `Document` | id, project_id, type (syllabus/reference), source (upload/url), parse_status |
| `Competency` | id, code, description, domain, quarter, order_index, document_id |
| `CompetencyLink` | target_id, prerequisite_id, next_id (editable triad) |
| `LearnerContext` | project_id, strengths, interests, barriers, readiness, language_needs |
| `ActivityPitch` | stage (engage/explore/elaborate), options[3], selection, tweak_notes |
| `LessonPlan` | project_id, sections (JSON per ILAW template), markdown, version |
| `AuditResult` | plan_id, criterion, status, evidence_ref, fix_suggestion |
| `AIDeclaration` | plan_id, model, prompt_summary, human_edits, do3_2026_ack |

---

## 6. Non-Functional Requirements

- **Privacy:** Learner context may include sensitive observations. Store minimally; no learner PII
  beyond what the teacher enters. Support deletion/export of a project's data.
- **Localization:** UI and generated content support English and Filipino; allow mother-tongue
  terms in early grades. Generated plans can localize examples to the school's community.
- **Accessibility:** WCAG 2.1 AA for the app UI.
- **Reliability:** Autosave drafts at each phase; resume incomplete projects.
- **Auditability:** Persist AI model, prompt summary, and human edits for each plan (feeds the Declaration of AI Use).
- **Performance:** Streamed generation (SSE) so teachers see progress; parsing of a typical MELC PDF under ~30s.

---

## 7. End-to-End User Flow

1. Teacher creates a project → uploads syllabus/MELC (**Phase 1**).
2. Selects target competency → confirms prerequisite/target/next triad.
3. Enters metadata, learner context, and references (**Phase 2**).
4. Reviews 3 activity options per key stage; selects/combines/tweaks (**Phase 3**).
5. Approves → AI generates the full ILAW plan (**Phase 4**).
6. System runs the 9-criterion audit; teacher resolves any "Needs Work" items.
7. Teacher edits, then exports (DOCX/PDF) with the Declaration of AI Use attached.

---

## 8. Out of Scope (v1)

- Learning Management System (LMS) grade syncing.
- Multi-teacher real-time co-editing.
- Automated grading of student submissions.

---

## 9. Companion Artifact

The AI behavior that powers Phases 3–4 and the rubric audit is defined in
[`system-prompt.md`](./system-prompt.md).
