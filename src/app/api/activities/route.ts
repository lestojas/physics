import { NextRequest, NextResponse } from "next/server";
import { askAI } from "@/lib/ai";
import {
  ACTIVITY_PITCH_PROMPT,
  buildActivityUserMessage,
  type LessonContext,
} from "@/lib/prompts";
import { parseJsonLoose } from "@/lib/json";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 120;

/**
 * POST /api/activities  (Phase 3 — Interactive Activity Pitch)
 * Body: { context: LessonContext }
 * Returns 3 distinct options each for ENGAGE / EXPLORE / ELABORATE.
 */
export async function POST(req: NextRequest) {
  try {
    const { context } = (await req.json()) as { context: LessonContext };

    if (!context || !context.targetCompetency) {
      return NextResponse.json(
        { error: "Missing lesson context or target competency." },
        { status: 400 }
      );
    }

    const reply = await askAI({
      system: ACTIVITY_PITCH_PROMPT,
      user: buildActivityUserMessage(context),
      maxTokens: 4000,
    });

    const activities = parseJsonLoose(reply);
    return NextResponse.json({ activities });
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Unexpected error." },
      { status: 500 }
    );
  }
}
