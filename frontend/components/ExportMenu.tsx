"use client";

import { Download } from "lucide-react";

export default function ExportMenu() {
  const handlePrint = () => window.print();

  return (
    <button
      onClick={handlePrint}
      className="no-print flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium
                 bg-white/5 hover:bg-white/10 text-[#8899b4] hover:text-[#e2eaf8]
                 border border-white/10 transition-all duration-200"
      title="Print / Save as PDF"
    >
      <Download size={12} />
      Export PDF
    </button>
  );
}
