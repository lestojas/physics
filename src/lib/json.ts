/**
 * Robustly parse JSON that may arrive from an LLM wrapped in ```json fences
 * or with minor surrounding prose. Throws if no valid JSON object can be found.
 */
export function parseJsonLoose<T = unknown>(raw: string): T {
  const trimmed = raw.trim();

  // 1) Try direct parse.
  try {
    return JSON.parse(trimmed) as T;
  } catch {
    /* fall through */
  }

  // 2) Strip Markdown code fences if present.
  const fenceMatch = trimmed.match(/```(?:json)?\s*([\s\S]*?)```/i);
  if (fenceMatch) {
    try {
      return JSON.parse(fenceMatch[1].trim()) as T;
    } catch {
      /* fall through */
    }
  }

  // 3) Grab the first {...} or [...] block.
  const objMatch = trimmed.match(/[{[][\s\S]*[}\]]/);
  if (objMatch) {
    return JSON.parse(objMatch[0]) as T;
  }

  throw new Error("Could not parse JSON from the model response.");
}
