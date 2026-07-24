"use client";

import { useState } from "react";
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";

export default function PlanOutput({ markdown }: { markdown: string }) {
  const [copied, setCopied] = useState(false);

  function download() {
    const blob = new Blob([markdown], { type: "text/markdown;charset=utf-8" });
    const url = URL.createObjectURL(blob);
    const a = document.createElement("a");
    a.href = url;
    a.download = "ILAW-Lesson-Plan.md";
    a.click();
    URL.revokeObjectURL(url);
  }

  async function copy() {
    await navigator.clipboard.writeText(markdown);
    setCopied(true);
    setTimeout(() => setCopied(false), 1800);
  }

  return (
    <div>
      <div className="btn-row" style={{ justifyContent: "flex-end", marginTop: 0 }}>
        <button className="btn btn-secondary" onClick={copy}>
          {copied ? "\u2713 Copied" : "Copy Markdown"}
        </button>
        <button className="btn btn-primary" onClick={download}>
          &#11015; Download .md
        </button>
      </div>
      <div className="plan">
        <ReactMarkdown remarkPlugins={[remarkGfm]}>{markdown}</ReactMarkdown>
      </div>
    </div>
  );
}
