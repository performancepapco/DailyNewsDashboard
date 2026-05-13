"use client";

import { TrendingUp, ExternalLink } from "lucide-react";
import { motion } from "framer-motion";
import type { Article } from "@/lib/api";
import { CATEGORY_META } from "@/lib/utils";

interface Props {
  category: "google_trends" | "twitter_trends";
  articles: Article[];
}

export default function TrendCard({ category, articles }: Props) {
  const meta = CATEGORY_META[category];

  return (
    <div className={`glass-card border-l-2 ${meta.borderColor} flex flex-col overflow-hidden`}>
      <div className="flex items-center gap-2 px-4 py-3 border-b border-[var(--c-ov-bd)]">
        <span className={`p-1.5 rounded-md ${meta.bgColor}`}>
          <TrendingUp size={13} className={meta.color} />
        </span>
        <span className={`text-sm font-semibold font-display ${meta.color}`}>{meta.label}</span>
        <span className="text-[10px] px-1.5 py-0.5 rounded-full bg-[var(--c-ov-lg)] text-[var(--c-text-sec)] font-medium">
          {articles.length}
        </span>
      </div>

      <ol className="flex flex-col px-3 pb-3 pt-2 gap-1">
        {articles.length === 0 && (
          <li className="text-xs py-3 text-center italic" style={{ color: "var(--c-text-muted)" }}>
            No trend data — trigger a refresh.
          </li>
        )}
        {articles.map((a, i) => (
          <motion.li
            key={a.id}
            initial={{ opacity: 0, x: -6 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: i * 0.04 }}
            className="group flex items-start gap-2.5 px-2 py-2 rounded-lg
                       hover:bg-[var(--c-ov-hover)] transition-colors"
          >
            <span className={`text-sm font-bold font-mono ${meta.color} opacity-60 w-5 shrink-0`}>
              {i + 1}
            </span>
            <a
              href={a.url}
              target="_blank"
              rel="noopener noreferrer"
              className="text-xs leading-snug flex items-center gap-1 transition-colors"
              style={{ color: "var(--c-text-med)" }}
            >
              {a.title.replace(/^Trending(?: on X)?:\s*/i, "")}
              <ExternalLink size={10} className="shrink-0 opacity-0 group-hover:opacity-50 transition-opacity" />
            </a>
          </motion.li>
        ))}
      </ol>
    </div>
  );
}
