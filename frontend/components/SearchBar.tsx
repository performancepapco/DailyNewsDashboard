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
        <Search size={13} className="absolute left-3 top-1/2 -translate-y-1/2 text-[#4a6080]" />
        <input
          type="text"
          value={query}
          onChange={(e) => setQuery(e.target.value)}
          placeholder="Search headlines, sources…"
          className="w-full pl-8 pr-8 py-2 rounded-lg text-xs
                     bg-[#111827] border border-[#1f2d45] text-[#e2eaf8]
                     placeholder:text-[#374559] focus:outline-none
                     focus:border-blue-500/50 focus:ring-1 focus:ring-blue-500/20
                     transition-all duration-200"
        />
        {query && (
          <button
            onClick={() => setQuery("")}
            className="absolute right-2.5 top-1/2 -translate-y-1/2 text-[#4a6080] hover:text-[#8899b4]"
          >
            <X size={12} />
          </button>
        )}
      </div>

      {/* Category filter */}
      <div className="flex items-center gap-1.5 flex-wrap">
        <Filter size={11} className="text-[#4a6080]" />
        <button
          onClick={() => setCategory(ALL)}
          className={`text-[10px] px-2 py-1 rounded-md font-medium transition-colors ${
            category === ALL
              ? "bg-blue-600/30 text-blue-300 border border-blue-500/30"
              : "bg-white/5 text-[#4a6080] border border-white/10 hover:bg-white/10"
          }`}
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
                : "bg-white/5 text-[#4a6080] border border-white/10 hover:bg-white/10"
            }`}
          >
            {meta.label}
          </button>
        ))}
      </div>
    </div>
  );
}
