import { GoogleGenAI } from "@google/genai";

/**
 * A single, shared Google Gemini client.
 *
 * The API key is read from the GEMINI_API_KEY environment variable and lives
 * ONLY on the server. It is never sent to the browser. Every call to the AI in
 * this app goes through the /api routes, which run on the server, so the key
 * stays private.
 *
 * Gemini has a genuinely free tier — get a key (no credit card) at
 * https://aistudio.google.com/apikey
 */

const apiKey = process.env.GEMINI_API_KEY;

/**
 * The model to use. Configurable via the GEMINI_MODEL env var so you can swap
 * models without touching code. Falls back to a current free-tier default.
 */
export const GEMINI_MODEL = process.env.GEMINI_MODEL || "gemini-2.5-flash";

/**
 * Returns a ready-to-use Gemini client, or throws a friendly error if the key
 * is missing. We throw here (not at import time) so the app can still start and
 * show a helpful message rather than crashing on boot.
 */
export function getAI(): GoogleGenAI {
  if (!apiKey || apiKey.trim() === "" || apiKey.includes("your-key-goes-here")) {
    throw new Error(
      "Gemini API key is not set. Create a file named .env.local in the project " +
        "root and add: GEMINI_API_KEY=... (get a FREE key at " +
        "https://aistudio.google.com/apikey). Then restart the app."
    );
  }
  return new GoogleGenAI({ apiKey });
}

/**
 * Sends a system instruction + user prompt to Gemini and returns the reply text.
 * Keeps the API routes short and readable.
 */
export async function askAI(options: {
  system: string;
  user: string;
  maxTokens?: number;
}): Promise<string> {
  const ai = getAI();

  const response = await ai.models.generateContent({
    model: GEMINI_MODEL,
    contents: options.user,
    config: {
      systemInstruction: options.system,
      maxOutputTokens: options.maxTokens ?? 12000,
    },
  });

  const text = response.text ?? "";
  if (!text.trim()) {
    throw new Error(
      "The AI returned an empty response. This can happen if the request hit a " +
        "rate limit or a safety filter. Please try again in a moment."
    );
  }
  return text.trim();
}
