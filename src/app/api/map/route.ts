import { NextRequest, NextResponse } from "next/server";
import { askClaude } from "@/lib/anthropic";
import { COMPETENCY_MAPPING_PROMPT, buildCompetencyUserMessage } from "@/lib/prompts";
import { parseJsonLoose } from "@/lib/json";

export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

/**
 * POST /api/map  (Phase 1 — Competency & Vertical Alignment Mapping)
 * Body: { syllabusText: string, targetCompetency: string }
 * Returns the prerequisite / target / future competency mapping as JSON.
 */
export async function POST(req: NextRequest) {
  try {
    const { syllabusText = "", targetCompetency = "" } = await req.json();

    if (!targetCompetency.trim()) {
      return NextResponse.json(
        { error: "Please provide a target competency." },
        { status: 400 }
      );
    }

    const reply = await askClaude({
      system: COMPETENCY_MAPPING_PROMPT,
      user: buildCompetencyUserMessage({ syllabusText, targetCompetency }),
      maxTokens: 2000,
    });

    const mapping = parseJsonLoose(reply);
    return NextResponse.json({ mapping });
  } catch (err) {
    return NextResponse.json(
      { error: friendlyError(err) },
      { status: 500 }
    );
  }
}

function friendlyError(err: unknown): string {
  const msg = err instanceof Error ? err.message : "Unexpected error.";
  return msg;
}
