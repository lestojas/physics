import Anthropic from "@anthropic-ai/sdk";

/**
 * A single, shared Claude client.
 *
 * The API key is read from the ANTHROPIC_API_KEY environment variable and lives
 * ONLY on the server. It is never sent to the browser. Every call to Claude in
 * this app goes through the /api routes, which run on the server, so the key
 * stays private.
 */

const apiKey = process.env.ANTHROPIC_API_KEY;

/**
 * The model to use. Configurable via the CLAUDE_MODEL env var so you can swap
 * models without touching code. Falls back to a sensible, current default.
 */
export const CLAUDE_MODEL = process.env.CLAUDE_MODEL || "claude-sonnet-4-6";

/**
 * Returns a ready-to-use Anthropic client, or throws a friendly error if the
 * key is missing. We throw here (instead of at import time) so the app can
 * still start and show a helpful message rather than crashing on boot.
 */
export function getClaude(): Anthropic {
  if (!apiKey || apiKey.trim() === "" || apiKey.includes("your-key-goes-here")) {
    throw new Error(
      "Claude API key is not set. Create a file named .env.local in the project " +
        "root and add: ANTHROPIC_API_KEY=sk-ant-... (get a key at https://console.anthropic.com/). " +
        "Then restart the app."
    );
  }
  return new Anthropic({ apiKey });
}

/**
 * Small helper that sends a system + user prompt to Claude and returns the
 * plain text of the reply. Keeps the API routes short and readable.
 *
 * Note: we intentionally do NOT set `temperature` so this works across all
 * current Claude models (some newer models reject non-default sampling params).
 */
export async function askClaude(options: {
  system: string;
  user: string;
  maxTokens?: number;
}): Promise<string> {
  const client = getClaude();

  const response = await client.messages.create({
    model: CLAUDE_MODEL,
    max_tokens: options.maxTokens ?? 8000,
    system: options.system,
    messages: [{ role: "user", content: options.user }],
  });

  // Concatenate all text blocks from the response.
  return response.content
    .filter((block): block is Anthropic.TextBlock => block.type === "text")
    .map((block) => block.text)
    .join("\n")
    .trim();
}
