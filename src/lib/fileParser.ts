/**
 * Server-side text extraction from uploaded files.
 *
 * Supports PDF, DOCX, and plain text (.txt/.md). Runs on the server only
 * (these libraries are not browser-safe).
 */

const MAX_CHARS_PER_FILE = 60_000; // keep prompts within a sane size

export interface ParsedFile {
  fileName: string;
  text: string;
  charCount: number;
  truncated: boolean;
  error?: string;
}

/** Extract text from a single uploaded File (Web API File object). */
export async function extractTextFromFile(file: File): Promise<ParsedFile> {
  const fileName = file.name || "uploaded-file";
  const lower = fileName.toLowerCase();

  try {
    const arrayBuffer = await file.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);

    let text = "";

    if (lower.endsWith(".pdf") || file.type === "application/pdf") {
      text = await extractPdf(buffer);
    } else if (
      lower.endsWith(".docx") ||
      file.type ===
        "application/vnd.openxmlformats-officedocument.wordprocessingml.document"
    ) {
      text = await extractDocx(buffer);
    } else if (
      lower.endsWith(".txt") ||
      lower.endsWith(".md") ||
      lower.endsWith(".markdown") ||
      file.type.startsWith("text/")
    ) {
      text = buffer.toString("utf-8");
    } else {
      // Best-effort fallback: try to read as text.
      text = buffer.toString("utf-8");
    }

    text = normalize(text);
    const truncated = text.length > MAX_CHARS_PER_FILE;
    if (truncated) text = text.slice(0, MAX_CHARS_PER_FILE);

    return { fileName, text, charCount: text.length, truncated };
  } catch (err) {
    return {
      fileName,
      text: "",
      charCount: 0,
      truncated: false,
      error: err instanceof Error ? err.message : "Failed to read file.",
    };
  }
}

/** Extract text from many files and combine into one labeled block. */
export async function extractTextFromFiles(files: File[]): Promise<{
  combinedText: string;
  files: ParsedFile[];
}> {
  const parsed = await Promise.all(files.map(extractTextFromFile));
  const combinedText = parsed
    .filter((p) => p.text)
    .map((p) => `===== FILE: ${p.fileName} =====\n${p.text}`)
    .join("\n\n");
  return { combinedText, files: parsed };
}

async function extractPdf(buffer: Buffer): Promise<string> {
  // Import the library's internal module directly to avoid pdf-parse's
  // "debug mode" auto-reading a bundled test PDF when required at top level.
  const pdfParse = (await import("pdf-parse/lib/pdf-parse.js")).default as (
    b: Buffer
  ) => Promise<{ text: string }>;
  const result = await pdfParse(buffer);
  return result.text || "";
}

async function extractDocx(buffer: Buffer): Promise<string> {
  const mammoth = await import("mammoth");
  const result = await mammoth.extractRawText({ buffer });
  return result.value || "";
}

function normalize(text: string): string {
  return text
    .replace(/\r\n/g, "\n")
    .replace(/\u0000/g, "")
    .replace(/[ \t]+\n/g, "\n")
    .replace(/\n{3,}/g, "\n\n")
    .trim();
}
