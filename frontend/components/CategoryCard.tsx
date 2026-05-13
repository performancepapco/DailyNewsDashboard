"use client";

import { useState } from "react";
import { ChevronDown, ChevronUp } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import * as Icons from "lucide-react";
import type { CategoryData } from "@/lib/api";
import { CATEGORY_META } from "@/lib/utils";
import NewsItem from "./NewsItem";

interface Props {
  category: string;
  data: CategoryData;
}

export default function CategoryCard({ category, data }: Props) {
  const [expanded, setExpanded] = useState(true);
  const meta = CATEGORY_META[category] ?? {
    label: category,
    color: "text-blue-400",
    borderColor: "border-blue-500",
    bgColor: "bg-blue-500/10",
    icon: "Newspaper",
  };

  // eslint-disable-next-line @typescript-eslint/no-explicit-any
  const IconComp = (Icons as any)[meta.icon] as React.FC<{ size?: number; className?: string }>;

  const hasItems = data.articles.length > 0;

  return (
    <div
      className={`glass-card border-l-2 ${meta.borderColor} flex flex-col overflow-hidden
                  transition-shadow duration-300 hover:shadow-lg`}
    >
      {/* Header */}
      <button
        onClick={() => setExpanded((p) => !p)}
        className="flex items-center justify-between px-4 py-3.5 w-full text-left
                   hover:bg-[var(--c-ov-xs)] transition-colors"
      >
        <div className="flex items-center gap-2.5">
          <span className={`p-1.5 rounded-md ${meta.bgColor}`}>
            {IconComp && <IconComp size={14} className={meta.color} />}
          </span>
          <span className={`text-sm font-semibold font-display ${meta.color}`}>
            {meta.label}
          </span>
          <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-[var(--c-ov-lg)] text-[var(--c-text-sec)] font-medium">
            {data.articles.length}
          </span>
        </div>
        <span style={{ color: "var(--c-text-muted)" }}>
          {expanded ? <ChevronUp size={14} /> : <ChevronDown size={14} />}
        </span>
      </button>

      {/* Content */}
      <AnimatePresence initial={false}>
        {expanded && (
          <motion.div
            key="content"
            initial={{ height: 0, opacity: 0 }}
            animate={{ height: "auto", opacity: 1 }}
            exit={{ height: 0, opacity: 0 }}
            transition={{ duration: 0.25, ease: "easeInOut" }}
            className="overflow-hidden"
          >
            <div className="flex flex-col gap-1.5 px-2 pb-3">
              {hasItems ? (
                data.articles.map((article, i) => (
                  <NewsItem key={article.id} article={article} index={i} />
                ))
              ) : (
                <p className="text-xs px-2 py-4 text-center italic" style={{ color: "var(--c-text-muted)" }}>
                  No data yet — trigger a refresh to load this category.
                </p>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
