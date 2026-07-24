/** Shared types used by both the UI and the API layer. */

export interface CompetencyMapping {
  targetCompetency: string;
  prerequisiteCompetencies: string[];
  futureCompetencies: string[];
  suggestedStandards: {
    contentStandard: string;
    performanceStandard: string;
  };
  notes: string;
}

export interface ActivityOption {
  title: string;
  description: string;
  materials: string[];
  rationale: string;
  inclusivityNote: string;
}

export interface ActivitiesResponse {
  engage: ActivityOption[];
  explore: ActivityOption[];
  elaborate: ActivityOption[];
}

export type ActivityStage = "engage" | "explore" | "elaborate";

export interface LessonContextForm {
  teacherName: string;
  learningArea: string;
  gradeLevel: string;
  section: string;
  numberOfSessions: string;
  targetCompetency: string;
  contentStandard: string;
  performanceStandard: string;
  learnerContext: string;
}
