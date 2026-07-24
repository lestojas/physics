import { NextRequest, NextResponse } from "next/server";
import { askAI } from "@/lib/ai";
import {
  FULL_PLAN_PROMPT,
  buildPlanUserMessage,
  type LessonContext,
} from "@/lib/prompts";
import { DEFAULT_ILAW_TEMPLATE } from "@/lib/defaultTemplate";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 300;

/**
 * POST /api/generate  (Phase 4 — Full ILAW Lesson Plan)
 * Body: {
 *   context: LessonContext,
 *   selectedActivities: { engage?, explore?, elaborate? },
 *   tweaks?: string,
 *   templateText?: string   // if empty/omitted, the built-in default is used
 * }
 * Returns the complete ILAW lesson plan as Markdown.
 */
export async function POST(req: NextRequest) {
  try {
    const {
      context,
      selectedActivities = {},
      tweaks = "",
      templateText = "",
    } = (await req.json()) as {
      context: LessonContext;
      selectedActivities?: {
        engage?: string;
        explore?: string;
        elaborate?: string;
      };
      tweaks?: string;
      templateText?: string;
    };

    if (!context || !context.targetCompetency) {
      return NextResponse.json(
        { error: "Missing lesson context or target competency." },
        { status: 400 }
      );
    }

    // Use the teacher's uploaded template if present; otherwise the default.
    const hasCustom = templateText.trim().length > 0;
    const template = hasCustom ? templateText : DEFAULT_ILAW_TEMPLATE;

    const markdown = await askAI({
      system: FULL_PLAN_PROMPT,
      user: buildPlanUserMessage({
        context,
        selectedActivities,
        tweaks,
        templateText: template,
        templateSource: hasCustom ? "uploaded" : "default",
      }),
      maxTokens: 12000,
    });

    return NextResponse.json({ markdown });
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Unexpected error." },
      { status: 500 }
    );
  }
}
