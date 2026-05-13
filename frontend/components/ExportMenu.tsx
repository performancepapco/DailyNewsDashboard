"use client";

import { Download } from "lucide-react";

export default function ExportMenu() {
  const handlePrint = () => window.print();

  return (
    <button
      onClick={handlePrint}
      className="no-print flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium
                 transition-all duration-200 border"
      style={{
        background: "var(--c-ov-sm)",
        color: "var(--c-text-sec)",
        borderColor: "var(--c-ov-bd)",
      }}
      onMouseEnter={(e) => {
        (e.currentTarget as HTMLButtonElement).style.background = "var(--c-ov-md)";
        (e.currentTarget as HTMLButtonElement).style.color = "var(--c-text-med)";
      }}
      onMouseLeave={(e) => {
        (e.currentTarget as HTMLButtonElement).style.background = "var(--c-ov-sm)";
        (e.currentTarget as HTMLButtonElement).style.color = "var(--c-text-sec)";
      }}
      title="Print / Save as PDF"
    >
      <Download size={12} />
      Export PDF
    </button>
  );
}
