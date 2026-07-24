import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "ILAW Lesson Plan Generator",
  description:
    "DepEd-aligned, Claude-powered ILAW (7Es) lesson plan generator with a 4-phase, human-in-the-loop workflow.",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en">
      <body>
        <header className="app-header">
          <div className="container">
            <h1>
              <span className="lamp">&#128161;</span> ILAW Lesson Plan Generator
            </h1>
            <p>
              DepEd-aligned 7Es lesson plans, drafted with Claude AI under your
              professional review.
            </p>
          </div>
        </header>
        <main>
          <div className="container">{children}</div>
        </main>
      </body>
    </html>
  );
}
