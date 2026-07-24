"use client";

import { useState } from "react";
import PhaseStepper from "@/components/PhaseStepper";
import UploadZone from "@/components/UploadZone";
import ActivityPitch from "@/components/ActivityPitch";
import PlanOutput from "@/components/PlanOutput";
import type {
  ActivitiesResponse,
  ActivityStage,
  CompetencyMapping,
  LessonContextForm,
} from "@/lib/types";

const EMPTY_FORM: LessonContextForm = {
  teacherName: "",
  learningArea: "",
  gradeLevel: "",
  section: "",
  numberOfSessions: "1",
  targetCompetency: "",
  contentStandard: "",
  performanceStandard: "",
  learnerContext: "",
};

export default function Home() {
  const [phase, setPhase] = useState(0);
  const [error, setError] = useState("");

  // Phase 1
  const [syllabusText, setSyllabusText] = useState("");
  const [mapping, setMapping] = useState<CompetencyMapping | null>(null);
  const [mapping_busy, setMappingBusy] = useState(false);

  // Phase 2
  const [form, setForm] = useState<LessonContextForm>(EMPTY_FORM);
  const [referencesText, setReferencesText] = useState("");
  const [templateText, setTemplateText] = useState("");
  const [templateFileName, setTemplateFileName] = useState("");

  // Phase 3
  const [activities, setActivities] = useState<ActivitiesResponse | null>(null);
  const [selected, setSelected] = useState<Record<ActivityStage, number | null>>({
    engage: null,
    explore: null,
    elaborate: null,
  });
  const [tweaks, setTweaks] = useState("");
  const [activitiesBusy, setActivitiesBusy] = useState(false);

  // Phase 4
  const [markdown, setMarkdown] = useState("");
  const [planBusy, setPlanBusy] = useState(false);

  function update<K extends keyof LessonContextForm>(
    key: K,
    value: LessonContextForm[K]
  ) {
    setForm((f) => ({ ...f, [key]: value }));
  }

  function buildContext() {
    return {
      teacherName: form.teacherName,
      learningArea: form.learningArea,
      gradeLevel: form.gradeLevel,
      section: form.section,
      numberOfSessions: form.numberOfSessions,
      targetCompetency: form.targetCompetency,
      contentStandard: form.contentStandard,
      performanceStandard: form.performanceStandard,
      learnerContext: form.learnerContext,
      referencesText,
      competencyMapping: mapping,
    };
  }

  // ---- Phase 1: map competencies ----
  async function mapCompetencies() {
    if (!form.targetCompetency.trim()) {
      setError("Please enter the target learning competency first.");
      return;
    }
    setError("");
    setMappingBusy(true);
    try {
      const res = await fetch("/api/map", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          syllabusText,
          targetCompetency: form.targetCompetency,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Mapping failed.");
      const m = data.mapping as CompetencyMapping;
      setMapping(m);
      // Pre-fill suggested standards if the teacher hasn't typed any.
      setForm((f) => ({
        ...f,
        contentStandard: f.contentStandard || m.suggestedStandards?.contentStandard || "",
        performanceStandard:
          f.performanceStandard || m.suggestedStandards?.performanceStandard || "",
      }));
    } catch (err) {
      setError(err instanceof Error ? err.message : "Mapping failed.");
    } finally {
      setMappingBusy(false);
    }
  }

  // ---- Phase 3: pitch activities ----
  async function pitchActivities() {
    if (!form.learningArea.trim() || !form.gradeLevel.trim()) {
      setError("Please fill in at least the Learning Area and Grade Level.");
      return;
    }
    setError("");
    setActivitiesBusy(true);
    setPhase(2);
    try {
      const res = await fetch("/api/activities", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ context: buildContext() }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Could not generate activities.");
      setActivities(data.activities as ActivitiesResponse);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not generate activities.");
    } finally {
      setActivitiesBusy(false);
    }
  }

  // ---- Phase 4: generate full plan ----
  async function generatePlan() {
    setError("");
    setPlanBusy(true);
    setPhase(3);
    try {
      const chosen = (stage: ActivityStage) => {
        const idx = selected[stage];
        if (idx == null || !activities) return undefined;
        const opt = activities[stage][idx];
        return `${opt.title} — ${opt.description}`;
      };

      const res = await fetch("/api/generate", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          context: buildContext(),
          selectedActivities: {
            engage: chosen("engage"),
            explore: chosen("explore"),
            elaborate: chosen("elaborate"),
          },
          tweaks,
          templateText,
        }),
      });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Could not generate the plan.");
      setMarkdown(data.markdown as string);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Could not generate the plan.");
    } finally {
      setPlanBusy(false);
    }
  }

  function selectActivity(stage: ActivityStage, index: number) {
    setSelected((s) => ({ ...s, [stage]: index }));
  }

  return (
    <>
      <PhaseStepper current={phase} />

      {error && <div className="alert alert-error">{error}</div>}

      {/* ---------- PHASE 1 ---------- */}
      {phase === 0 && (
        <div className="card">
          <h2>Phase 1 — Curriculum &amp; Competency Tracking</h2>
          <p className="hint">
            Upload your Curriculum Guide / MELC / Syllabus (optional) and enter the
            target competency. Gemini maps what comes before and after it.
          </p>

          <div className="field">
            <UploadZone
              label="Upload Curriculum / MELC / Syllabus"
              onExtracted={(text) => setSyllabusText(text)}
            />
          </div>

          <div className="field">
            <label>
              Target Learning Competency <span className="req">*</span>
            </label>
            <textarea
              placeholder="e.g., Explain how the different structures of the circulatory and respiratory systems work together…"
              value={form.targetCompetency}
              onChange={(e) => update("targetCompetency", e.target.value)}
            />
          </div>

          <button
            className="btn btn-secondary"
            onClick={mapCompetencies}
            disabled={mapping_busy}
          >
            {mapping_busy ? (
              <>
                <span className="spinner" /> Mapping…
              </>
            ) : (
              "Map Prerequisite → Target → Future"
            )}
          </button>

          {mapping && (
            <div style={{ marginTop: 18 }}>
              <div className="map-grid">
                <div className="map-col prev">
                  <h4>Prerequisite</h4>
                  <ul>
                    {mapping.prerequisiteCompetencies?.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                </div>
                <div className="map-col target">
                  <h4>Target</h4>
                  <p style={{ fontSize: 13, margin: 0 }}>{mapping.targetCompetency}</p>
                </div>
                <div className="map-col future">
                  <h4>Future</h4>
                  <ul>
                    {mapping.futureCompetencies?.map((c, i) => (
                      <li key={i}>{c}</li>
                    ))}
                  </ul>
                </div>
              </div>
              {mapping.notes && (
                <p className="hint" style={{ marginTop: 10 }}>
                  <em>{mapping.notes}</em>
                </p>
              )}
            </div>
          )}

          <div className="btn-row">
            <span />
            <button
              className="btn btn-primary"
              onClick={() => {
                if (!form.targetCompetency.trim()) {
                  setError("Please enter the target learning competency.");
                  return;
                }
                setError("");
                setPhase(1);
              }}
            >
              Continue to Context &rarr;
            </button>
          </div>
        </div>
      )}

      {/* ---------- PHASE 2 ---------- */}
      {phase === 1 && (
        <div className="card">
          <h2>Phase 2 — Context &amp; Reference Ingestion</h2>
          <p className="hint">
            Tell Gemini about your class and materials. The more context, the more
            tailored and inclusive the plan.
          </p>

          <div className="grid-2">
            <div className="field">
              <label>Teacher Name</label>
              <input
                type="text"
                value={form.teacherName}
                onChange={(e) => update("teacherName", e.target.value)}
              />
            </div>
            <div className="field">
              <label>
                Learning Area <span className="req">*</span>
              </label>
              <input
                type="text"
                placeholder="e.g., Science"
                value={form.learningArea}
                onChange={(e) => update("learningArea", e.target.value)}
              />
            </div>
            <div className="field">
              <label>
                Grade Level <span className="req">*</span>
              </label>
              <input
                type="text"
                placeholder="e.g., Grade 9"
                value={form.gradeLevel}
                onChange={(e) => update("gradeLevel", e.target.value)}
              />
            </div>
            <div className="field">
              <label>Section</label>
              <input
                type="text"
                value={form.section}
                onChange={(e) => update("section", e.target.value)}
              />
            </div>
            <div className="field">
              <label>Number of Sessions</label>
              <input
                type="text"
                value={form.numberOfSessions}
                onChange={(e) => update("numberOfSessions", e.target.value)}
              />
            </div>
          </div>

          <div className="grid-2">
            <div className="field">
              <label>Content Standard</label>
              <textarea
                value={form.contentStandard}
                onChange={(e) => update("contentStandard", e.target.value)}
              />
            </div>
            <div className="field">
              <label>Performance Standard</label>
              <textarea
                value={form.performanceStandard}
                onChange={(e) => update("performanceStandard", e.target.value)}
              />
            </div>
          </div>

          <div className="field">
            <label>Learner Context</label>
            <textarea
              placeholder="Strengths, interests, barriers, language needs, readiness levels, learners with disabilities, class size…"
              value={form.learnerContext}
              onChange={(e) => update("learnerContext", e.target.value)}
            />
          </div>

          <div className="field">
            <label>Reference Materials (optional)</label>
            <UploadZone
              label="Upload Books / Toolkits / PDFs / Notes"
              onExtracted={(text) =>
                setReferencesText((prev) => (prev ? prev + "\n\n" + text : text))
              }
            />
          </div>

          <div className="field">
            <label>Lesson Plan Template</label>
            {templateText ? (
              <div className="alert alert-info" style={{ marginBottom: 8 }}>
                Using your uploaded template:{" "}
                <strong>{templateFileName || "custom template"}</strong>.{" "}
                <a
                  href="#"
                  onClick={(e) => {
                    e.preventDefault();
                    setTemplateText("");
                    setTemplateFileName("");
                  }}
                >
                  Remove &amp; use the default template
                </a>
              </div>
            ) : (
              <div className="alert alert-info" style={{ marginBottom: 8 }}>
                Using the <strong>built-in default DepEd ILAW template</strong>. To use
                your own format, upload it below (.docx, .pdf, .txt, or .md).
              </div>
            )}
            <UploadZone
              label="Upload your own ILAW template (optional)"
              onExtracted={(text, fileNames) => {
                setTemplateText(text);
                setTemplateFileName(fileNames[0] || "");
              }}
            />
          </div>

          <div className="btn-row">
            <button className="btn btn-secondary" onClick={() => setPhase(0)}>
              &larr; Back
            </button>
            <button
              className="btn btn-primary"
              onClick={pitchActivities}
              disabled={activitiesBusy}
            >
              {activitiesBusy ? (
                <>
                  <span className="spinner" /> Pitching activities…
                </>
              ) : (
                "Pitch Activity Options \u2192"
              )}
            </button>
          </div>
        </div>
      )}

      {/* ---------- PHASE 3 ---------- */}
      {phase === 2 && (
        <div className="card">
          <h2>Phase 3 — Interactive Activity Pitch</h2>
          <p className="hint">
            Pick one option per stage (or leave a stage unpicked to let Gemini
            choose). Add tweak notes below before generating the full plan.
          </p>

          {activitiesBusy && (
            <div className="loading-block">
              <div className="spinner" />
              Gemini is designing 3 distinct options for Engage, Explore, and
              Elaborate…
            </div>
          )}

          {activities && !activitiesBusy && (
            <>
              <ActivityPitch
                activities={activities}
                selected={selected}
                onSelect={selectActivity}
              />

              <div className="field">
                <label>Tweaks / Notes (optional)</label>
                <textarea
                  placeholder="e.g., Combine Explore option 1 with option 3; localize to our barangay's fishing livelihood; keep materials no-cost."
                  value={tweaks}
                  onChange={(e) => setTweaks(e.target.value)}
                />
              </div>

              <div className="btn-row">
                <button className="btn btn-secondary" onClick={() => setPhase(1)}>
                  &larr; Back
                </button>
                <button
                  className="btn btn-secondary"
                  onClick={pitchActivities}
                  disabled={activitiesBusy}
                >
                  &#8635; Re-pitch
                </button>
                <button className="btn btn-primary" onClick={generatePlan}>
                  Generate ILAW Lesson Plan &rarr;
                </button>
              </div>
            </>
          )}
        </div>
      )}

      {/* ---------- PHASE 4 ---------- */}
      {phase === 3 && (
        <div className="card">
          <h2>
            Phase 4 — ILAW Lesson Plan
            <span className="badge">DO 3 s. 2026 compliant</span>
          </h2>
          <p className="hint">
            Auto-audited against all 9 quality criteria before rendering. Review,
            edit, and make it your own.
          </p>

          {planBusy && (
            <div className="loading-block">
              <div className="spinner" />
              Gemini is writing and self-auditing your full ILAW lesson plan…
            </div>
          )}

          {markdown && !planBusy && <PlanOutput markdown={markdown} />}

          {!planBusy && (
            <div className="btn-row">
              <button className="btn btn-secondary" onClick={() => setPhase(2)}>
                &larr; Back to activities
              </button>
              {markdown && (
                <button className="btn btn-primary" onClick={generatePlan}>
                  &#8635; Regenerate
                </button>
              )}
            </div>
          )}
        </div>
      )}
    </>
  );
}
