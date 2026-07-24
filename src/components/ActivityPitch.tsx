"use client";

import type {
  ActivitiesResponse,
  ActivityOption,
  ActivityStage,
} from "@/lib/types";

interface Props {
  activities: ActivitiesResponse;
  selected: Record<ActivityStage, number | null>;
  onSelect: (stage: ActivityStage, index: number) => void;
}

const STAGES: { key: ActivityStage; label: string }[] = [
  { key: "engage", label: "Engage" },
  { key: "explore", label: "Explore" },
  { key: "elaborate", label: "Elaborate" },
];

export default function ActivityPitch({ activities, selected, onSelect }: Props) {
  return (
    <div>
      {STAGES.map(({ key, label }) => (
        <div className="stage-block" key={key}>
          <div className="stage-title">{label}</div>
          {(activities[key] || []).map((opt, i) => (
            <OptionCard
              key={i}
              opt={opt}
              selected={selected[key] === i}
              onClick={() => onSelect(key, i)}
            />
          ))}
        </div>
      ))}
    </div>
  );
}

function OptionCard({
  opt,
  selected,
  onClick,
}: {
  opt: ActivityOption;
  selected: boolean;
  onClick: () => void;
}) {
  return (
    <div className={`option ${selected ? "selected" : ""}`} onClick={onClick}>
      <div className="opt-head">
        <span className="radio" />
        {opt.title}
      </div>
      <p>{opt.description}</p>
      {opt.materials?.length > 0 && (
        <div className="meta">
          <strong>Materials:</strong>{" "}
          {opt.materials.map((m, i) => (
            <span className="tag" key={i}>
              {m}
            </span>
          ))}
        </div>
      )}
      {opt.rationale && (
        <p className="meta">
          <strong>Why it works:</strong> {opt.rationale}
        </p>
      )}
      {opt.inclusivityNote && (
        <p className="meta">
          <strong>Inclusivity:</strong> {opt.inclusivityNote}
        </p>
      )}
    </div>
  );
}
