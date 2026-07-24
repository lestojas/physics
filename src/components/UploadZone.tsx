"use client";

import { useRef, useState } from "react";

interface Props {
  label: string;
  onExtracted: (text: string, fileNames: string[]) => void;
}

/**
 * A reusable file picker that uploads to /api/parse and returns the extracted
 * plain text to the parent. Handles PDF / DOCX / TXT / MD.
 */
export default function UploadZone({ label, onExtracted }: Props) {
  const inputRef = useRef<HTMLInputElement>(null);
  const [files, setFiles] = useState<string[]>([]);
  const [busy, setBusy] = useState(false);
  const [error, setError] = useState("");

  async function handleFiles(fileList: FileList | null) {
    if (!fileList || fileList.length === 0) return;
    setBusy(true);
    setError("");

    try {
      const form = new FormData();
      Array.from(fileList).forEach((f) => form.append("files", f));

      const res = await fetch("/api/parse", { method: "POST", body: form });
      const data = await res.json();
      if (!res.ok) throw new Error(data.error || "Upload failed.");

      const names = Array.from(fileList).map((f) => f.name);
      setFiles((prev) => [...prev, ...names]);
      onExtracted(data.combinedText || "", names);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Upload failed.");
    } finally {
      setBusy(false);
      if (inputRef.current) inputRef.current.value = "";
    }
  }

  return (
    <div>
      <div
        className="dropzone"
        onClick={() => inputRef.current?.click()}
        onDragOver={(e) => e.preventDefault()}
        onDrop={(e) => {
          e.preventDefault();
          handleFiles(e.dataTransfer.files);
        }}
      >
        {busy ? (
          <span>
            <span className="spinner" style={{ borderTopColor: "#0b3d91" }} />{" "}
            Reading files…
          </span>
        ) : (
          <>
            <div style={{ fontWeight: 600 }}>{label}</div>
            <div style={{ fontSize: 12, marginTop: 4 }}>
              Click to browse or drag &amp; drop — PDF, DOCX, TXT, or MD
            </div>
          </>
        )}
      </div>

      <input
        ref={inputRef}
        type="file"
        multiple
        accept=".pdf,.docx,.txt,.md,.markdown"
        style={{ display: "none" }}
        onChange={(e) => handleFiles(e.target.files)}
      />

      {files.length > 0 && (
        <div style={{ marginTop: 6 }}>
          {files.map((name, i) => (
            <span key={i} className="file-pill">
              &#128196; {name}
            </span>
          ))}
        </div>
      )}

      {error && (
        <div className="alert alert-error" style={{ marginTop: 10 }}>
          {error}
        </div>
      )}
    </div>
  );
}
