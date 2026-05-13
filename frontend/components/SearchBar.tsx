"use client";

import { useState, useEffect } from "react";
import { Search, X, Filter } from "lucide-react";
import { CATEGORY_META } from "@/lib/utils";

interface Props {
  onSearch: (query: string, category: string) => void;
}

const ALL = "all";

export default function SearchBar({ onSearch }: Props) {
  const [query, setQuery] = useState("");
  const [category, setCategory] = useState(ALL);

  useEffect(() => {
    const id = setTimeout(() => onSearch(query, category), 250);
    return () => clearTimeout(id);
  }, [query, category, onSearch]);

  return (
    <div className="flex flex-wrap items-center gap-2 no-print">
      {/* Search input */}
      <div className="relative flex-1 min-w-[200px]">
        <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2" style={{ color: "var(--c-text-muted)" }} />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search headlines, sources…"
          className="w-full pl-8 pr-8 py-2 rounded-lg text-xs
                     focus:outline-none focus:ring-1 focus:ring-blue-500/20
                     transition-all duration-200"
          style={{
            background: "var(--c-bg-panel)",
            border: "1px solid var(--c-border)",
            color: "var(--c-text-med)",
          }}
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 transition-colors"
            style={{ color: "var(--c-text-muted)" }}
          >
            <X size={12} />
          </button>
        )}
      </div>

      {/* Category filter */}
      <div className="flex items-center gap-1.5 flex-wrap">
        <Filter size={11} style={{ color: "var(--c-text-muted)" }} />
        <button
          onClick={() => setCategory(ALL)}
          className={`text-[10px] px-2 py-1 rounded-md font-medium transition-colors ${
            category === ALL
              ? "bg-blue-600/30 text-blue-300 border border-blue-500/30"
              : "border hover:bg-[var(--c-ov-md)]"
          }`}
          style={category !== ALL ? {
            background: "var(--c-ov-sm)",
            color: "var(--c-text-muted)",
            borderColor: "var(--c-ov-bd)",
          } : undefined}
        >
          All
        </button>
        {Object.entries(CATEGORY_META).map(([key, meta]) => (
          <button
            key={key}
            onClick={() => setCategory(category === key ? ALL : key)}
            className={`text-[10px] px-2 py-1 rounded-md font-medium transition-colors ${
              category === key
                ? `${meta.bgColor} ${meta.color} border ${meta.borderColor}/40`
                : "border"
            }`}
            style={category !== key ? {
              background: "var(--c-ov-sm)",
              color: "var(--c-text-muted)",
              borderColor: "var(--c-ov-bd)",
            } : undefined}
          >
            {meta.label}
          </button>
        ))}
      </div>
    </div>
  );
}
