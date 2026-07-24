import { NextRequest, NextResponse } from "next/server";
import { askClaude } from "@/lib/anthropic";
import {
  FULL_PLAN_PROMPT,
  buildPlanUserMessage,
  type LessonContext,
} from "@/lib/prompts";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 300;

/**
 * POST /api/generate  (Phase 4 — Full ILAW Lesson Plan)
 * Body: {
 *   context: LessonContext,
 *   selectedActivities: { engage?, explore?, elaborate? },
 *   tweaks?: string
 * }
 * Returns the complete ILAW lesson plan as Markdown.
 */
export async function POST(req: NextRequest) {
  try {
    const { context, selectedActivities = {}, tweaks = "" } =
      (await req.json()) as {
        context: LessonContext;
        selectedActivities?: {
          engage?: string;
          explore?: string;
          elaborate?: string;
        };
        tweaks?: string;
      };

    if (!context || !context.targetCompetency) {
      return NextResponse.json(
        { error: "Missing lesson context or target competency." },
        { status: 400 }
      );
    }

    const markdown = await askClaude({
      system: FULL_PLAN_PROMPT,
      user: buildPlanUserMessage({ context, selectedActivities, tweaks }),
      maxTokens: 8000,
    });

    return NextResponse.json({ markdown });
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Unexpected error." },
      { status: 500 }
    );
  }
}
