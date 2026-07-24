"use client";

const STEPS = [
  { label: "Curriculum & Competency", sub: "Phase 1" },
  { label: "Context & References", sub: "Phase 2" },
  { label: "Activity Pitch", sub: "Phase 3" },
  { label: "ILAW Lesson Plan", sub: "Phase 4" },
];

export default function PhaseStepper({ current }: { current: number }) {
  return (
    <div className="stepper">
      {STEPS.map((s, i) => {
        const state = i < current ? "done" : i === current ? "active" : "";
        return (
          <div key={i} className={`step ${state}`}>
            <div className="num">{i < current ? "\u2713" : i + 1}</div>
            <div>
              <div className="label">{s.label}</div>
              <div className="sub">{s.sub}</div>
            </div>
          </div>
        );
      })}
    </div>
  );
}
