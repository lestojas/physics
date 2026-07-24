# ILAW Lesson Plan Generator

A DepEd-aligned web app that helps teachers build **ILAW (7Es) lesson plans**. The
actual lesson content is written by **Google Gemini AI** through a guided,
**4-phase, human-in-the-loop** workflow — you stay in control, Gemini does the drafting.

> **100% free to run.** Gemini has a real free tier (no credit card), and you can host
> the website for free on Vercel. See the deploy guide below to get your own live link.

> **AI use, declared.** Every generated plan includes a *Declaration of AI Use* citing
> DepEd Order (DO) No. 3, s. 2026, Annex A, and is self-audited against 9 quality
> criteria before it is shown to you.

---

## What it does (the 4 phases)

1. **Curriculum & Competency Tracking** — Upload a MELC / Curriculum Guide / Syllabus
   (PDF, DOCX, TXT, MD) and pick a target competency. Gemini maps
   **Prerequisite → Target → Future** competencies.
2. **Context & Reference Ingestion** — Enter learning area, grade, section, sessions,
   standards, and your **learner context**. Optionally upload reference materials **and
   your own lesson-plan template**.
3. **Interactive Activity Pitch** — Gemini proposes **3 distinct options** each for
   *Engage*, *Explore*, and *Elaborate*. You choose, combine, or request tweaks.
4. **Full ILAW Lesson Plan** — Gemini writes the complete plan (7Es, SMART objectives,
   10-point reflection checklist) as clean Markdown you can copy or download.

### Templates: your own, or the built-in default
In Phase 2 you can **upload your own ILAW template** (`.docx`, `.pdf`, `.txt`, `.md`).
If you don't upload one, the app uses a **built-in default DepEd ILAW template**
automatically. Either way, the generated plan follows that structure.

---

## Part A — Get a FREE Gemini API key (about 2 minutes)

The app needs a key so it can ask Gemini to write the content. It's free.

1. Go to **https://aistudio.google.com/apikey**
2. Sign in with any Google account.
3. Click **Create API key** (choose "Create in new project" if asked).
4. Copy the key. Keep it private — treat it like a password.

That's the only credential you need. **No credit card, no billing setup.**

---

## Part B — Get a live website link (deploy on Vercel, free)

This is the easiest way to get a working link you can open on any device and share
with co-teachers. You do **not** need to install anything on your computer.

1. **Put the code on GitHub** — it already is, in this repository. If this is still on a
   branch (a pull request), open the PR on GitHub and click **Merge** so the code is on
   the `main` branch. (Ask if you're unsure — I can do this for you.)
2. Go to **https://vercel.com/** and click **Sign Up**, then **Continue with GitHub**
   (free "Hobby" plan is fine).
3. Click **Add New… → Project**, find this repository (`physics`), and click **Import**.
4. Before deploying, open **Environment Variables** and add one:
   - **Name:** `GEMINI_API_KEY`
   - **Value:** *(paste the key from Part A)*
5. Click **Deploy** and wait about a minute.
6. Vercel gives you a public link like `https://your-project.vercel.app` — **that's your
   live website.** Open it and start generating plans.

Because the key is stored as a server-side Environment Variable in Vercel, it stays
private even though the website is public.

> **One-click option:** you can also click this button (it pre-fills the setup and asks
> for your `GEMINI_API_KEY`):
>
> [![Deploy with Vercel](https://vercel.com/button)](https://vercel.com/new/clone?repository-url=https://github.com/lestojas/physics&env=GEMINI_API_KEY&envDescription=Free%20Gemini%20API%20key&envLink=https://aistudio.google.com/apikey&project-name=ilaw-lesson-plan-generator)

**Updating the live site later:** any change merged into `main` on GitHub auto-deploys
to your Vercel link. Nothing else to do.

---

## Part C — (Optional) Run it on your own computer

Only needed if you want to develop/test locally instead of using the live link.

1. Install **Node.js** (version 18 or newer) from https://nodejs.org/.
2. Download this project (GitHub → **Code → Download ZIP**, then unzip) or `git clone` it.
3. In the project folder, copy `.env.example` to a new file named **`.env.local`** and add
   your key:
   ```
   GEMINI_API_KEY=your-real-key-here
   ```
4. In a terminal, run:
   ```bash
   npm install
   npm run dev
   ```
5. Open **http://localhost:3000**.

---

## Choosing a model (optional)

Set `GEMINI_MODEL` in your environment (in `.env.local` locally, or in Vercel's env vars):

| Model | Best for | Free tier |
|-------|----------|-----------|
| `gemini-2.5-flash` *(default)* | Balanced quality + speed | ✅ Yes |
| `gemini-2.5-flash-lite` | Fastest / lightest | ✅ Yes |

"Flash" models are the free-tier workhorses. Model names change over time — check the
Gemini docs if one is rejected.

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
│   ├── ai.ts               # Gemini client (server-side key handling)
│   ├── prompts.ts          # ALL the AI instructions (persona, ILAW, 9-criteria)
│   ├── defaultTemplate.ts  # Built-in default ILAW template
│   ├── fileParser.ts       # PDF / DOCX / TXT / MD text extraction
│   ├── json.ts             # Robust JSON parsing of model replies
│   └── types.ts            # Shared TypeScript types
└── components/             # UploadZone, PhaseStepper, ActivityPitch, PlanOutput
docs/
└── FEATURE_SPEC.md         # Full feature specification
```

**Want to change how the AI behaves?** Edit `src/lib/prompts.ts`. To change the default
plan layout, edit `src/lib/defaultTemplate.ts`.

---

## Troubleshooting

| Problem | Fix |
|---------|-----|
| "Gemini API key is not set" | Add `GEMINI_API_KEY` in Vercel env vars (or `.env.local` locally) and redeploy/restart. |
| 400 / invalid API key | Re-copy the key from https://aistudio.google.com/apikey. |
| "empty response" / rate limit | Free tier has per-minute limits; wait a few seconds and try again. |
| PDF upload returns little text | Scanned PDFs (images) have no selectable text. Use a DOCX/TXT or paste the text. |
| A model name is rejected | Set `GEMINI_MODEL` to a current model from the Gemini docs. |

---

## Important notes

- **Human-in-the-loop by design.** Gemini drafts; the teacher reviews, edits, and owns
  the final plan. Always verify accuracy and appropriateness for your learners.
- **Privacy.** Uploaded files are parsed in memory to build the prompt and are not
  stored by this app. Avoid uploading sensitive personal data about learners.
