# ILAW Lesson Plan Generator

A DepEd-aligned web app that helps teachers build **ILAW (7Es) lesson plans**. The
actual lesson content is written by **Claude AI** (Anthropic) through a guided,
**4-phase, human-in-the-loop** workflow — you stay in control, Claude does the drafting.

> **AI use, declared.** Every generated plan includes a *Declaration of AI Use*
> citing DepEd Order (DO) No. 3, s. 2026, Annex A, and is self-audited against 9
> quality criteria before it is shown to you.

---

## What it does (the 4 phases)

1. **Curriculum & Competency Tracking** — Upload a MELC / Curriculum Guide / Syllabus
   (PDF, DOCX, TXT, MD) and pick a target competency. Claude maps
   **Prerequisite → Target → Future** competencies.
2. **Context & Reference Ingestion** — Enter learning area, grade, section, sessions,
   standards, and your **learner context**. Optionally upload reference materials.
3. **Interactive Activity Pitch** — Claude proposes **3 distinct options** each for
   *Engage*, *Explore*, and *Elaborate*. You choose, combine, or request tweaks.
4. **Full ILAW Lesson Plan** — Claude writes the complete plan (7Es, SMART objectives,
   10-point reflection checklist) as clean Markdown you can copy or download.

---

## ⭐ How the app connects to Claude (read this first)

You asked how to connect this to Claude so that *Claude* writes the lesson content.
Here is the simple version.

### The idea in one picture

```
Your browser  →  This app's server (keeps your secret key)  →  Claude (Anthropic)
   (the UI)          /api/... routes call Anthropic              writes the content
```

Your **secret API key** never touches the browser. It lives only on the server side of
this app, inside a file called `.env.local`. That is the safe, standard way to do it.

### Step-by-step setup (about 5 minutes)

**1. Get a Claude API key**
   - Go to **https://console.anthropic.com/** and sign in (create an account if needed).
   - Add a small amount of billing credit (the API is pay-as-you-go, separate from a
     Claude.ai chat subscription).
   - Open **API Keys → Create Key**, then copy the key. It looks like `sk-ant-...`.
     Treat it like a password — anyone with it can spend your credit.

**2. Install the tools to run the app**
   - Install **Node.js** (version 18 or newer) from https://nodejs.org/.

**3. Add your key to the app**
   - In the project folder, make a copy of `.env.example` and name the copy
     **`.env.local`**.
   - Open `.env.local` and paste your key:
     ```
     ANTHROPIC_API_KEY=sk-ant-your-real-key-here
     ```
   - Save the file. (`.env.local` is git-ignored, so it will never be uploaded.)

**4. Install and run**
   ```bash
   npm install
   npm run dev
   ```
   Then open **http://localhost:3000** in your browser.

That's it. When you click through the phases, the app sends your inputs to Claude
**from the server**, gets the lesson content back, and shows it to you.

### "I want to put this online so my co-teachers can use it"

Deploy it to **Vercel** (free tier works for light use):
1. Push this project to a GitHub repo.
2. Go to https://vercel.com/, import the repo.
3. In the Vercel project **Settings → Environment Variables**, add
   `ANTHROPIC_API_KEY` with your key (and optionally `CLAUDE_MODEL`).
4. Deploy. Vercel gives you a public link.

Because the key is stored as a server environment variable, it stays private even
though the site is public.

---

## Choosing a model (optional)

Set `CLAUDE_MODEL` in `.env.local`. Sensible options (mid-2026):

| Model | Best for | Relative cost |
|-------|----------|---------------|
| `claude-sonnet-4-6` *(default)* | Balanced quality + speed | $$ |
| `claude-opus-4-8` | Highest-quality writing | $$$ |
| `claude-haiku-4-5` | Fast, cheap drafts | $ |

Model names change over time — check the Anthropic docs if one is rejected.

---

## Project structure

```
src/
├── app/
│   ├── layout.tsx          # Page shell + header
│   ├── page.tsx            # The 4-phase workflow (client UI)
│   ├── globals.css         # Styling (DepEd navy/gold theme)
│   └── api/
│       ├── parse/route.ts      # Extract text from uploaded files
│       ├── map/route.ts        # Phase 1: competency mapping
│       ├── activities/route.ts # Phase 3: pitch 3 activity options
│       └── generate/route.ts   # Phase 4: full ILAW plan
├── lib/
│   ├── anthropic.ts        # Claude client (server-side key handling)
│   ├── prompts.ts          # ALL the AI instructions (persona, ILAW, 9-criteria)
│   ├── fileParser.ts       # PDF / DOCX / TXT / MD text extraction
│   ├── json.ts             # Robust JSON parsing of model replies
│   └── types.ts            # Shared TypeScript types
└── components/             # UploadZone, PhaseStepper, ActivityPitch, PlanOutput
docs/
└── FEATURE_SPEC.md         # Full feature specification
```

**Want to change how Claude behaves?** Edit `src/lib/prompts.ts`. That single file
holds the instructional-designer persona, the ILAW template, and the 9-criteria audit.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Claude API key is not set" | Create `.env.local` with `ANTHROPIC_API_KEY=...`, then restart `npm run dev`. |
| 401 / authentication error | The key is wrong or has no billing credit. Re-copy it from the console. |
| PDF upload returns little text | Scanned PDFs (images) have no selectable text. Paste the text or use a DOCX/TXT. |
| A model name is rejected | Update `CLAUDE_MODEL` to a current model from the Anthropic docs. |

---

## Important notes

- **Human-in-the-loop by design.** Claude drafts; the teacher reviews, edits, and owns
  the final plan. Always verify accuracy and appropriateness for your learners.
- **Privacy.** Uploaded files are parsed in memory to build the prompt and are not
  stored by this app. Avoid uploading sensitive personal data about learners.
