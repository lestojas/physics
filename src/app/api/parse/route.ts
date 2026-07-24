import { NextRequest, NextResponse } from "next/server";
import { extractTextFromFiles } from "@/lib/fileParser";

// pdf-parse / mammoth need the full Node.js runtime (not the Edge runtime).
export const runtime = "nodejs";
export const dynamic = "force-dynamic";
export const maxDuration = 60;

/**
 * POST /api/parse
 * Accepts a multipart/form-data body with one or more files under the "files"
 * field. Extracts plain text from each (PDF / DOCX / TXT / MD) and returns the
 * combined text. Used for both syllabus uploads (Phase 1) and reference
 * materials (Phase 2).
 */
export async function POST(req: NextRequest) {
  try {
    const formData = await req.formData();
    const entries = formData.getAll("files");
    const files = entries.filter((e): e is File => e instanceof File);

    if (files.length === 0) {
      return NextResponse.json(
        { error: "No files were uploaded." },
        { status: 400 }
      );
    }

    const { combinedText, files: parsed } = await extractTextFromFiles(files);

    return NextResponse.json({ combinedText, files: parsed });
  } catch (err) {
    return NextResponse.json(
      { error: err instanceof Error ? err.message : "Failed to parse files." },
      { status: 500 }
    );
  }
}
