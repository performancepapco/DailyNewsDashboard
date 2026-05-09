"use client";

import { ExternalLink } from "lucide-react";
import { motion } from "framer-motion";
import type { Article } from "@/lib/api";
import { formatRelativeTime, ALERT_META } from "@/lib/utils";

interface Props {
  article: Article;
  index: number;
}

export default function NewsItem({ article, index }: Props) {
  const alert = ALERT_META[article.alert_level] ?? ALERT_META.none;

  return (
    <motion.div
      initial={{ opacity: 0, y: 8 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.05, duration: 0.3 }}
      className="group relative flex flex-col gap-1 px-4 py-3 rounded-lg
                 bg-white/[0.03] hover:bg-white/[0.06]
                 border border-white/[0.05] hover:border-white/[0.10]
                 transition-all duration-200 cursor-pointer"
    >
      {/* Alert dot */}
      {alert.dot && (
        <span className={`absolute top-3.5 left-1.5 w-1.5 h-1.5 rounded-full ${alert.dot}`} />
      )}

      {/* Headline */}
      <a
        href={article.url}
        target="_blank"
        rel="noopener noreferrer"
        className="text-sm font-medium text-[#e2eaf8] leading-snug
                   group-hover:text-white transition-colors pr-5"
      >
        {article.title}
        <ExternalLink
          className="inline-block ml-1.5 mb-0.5 opacity-0 group-hover:opacity-60 transition-opacity"
          size={11}
        />
      </a>

      {/* Summary */}
      {article.summary && (
        <p className="text-xs text-[#8899b4] leading-relaxed line-clamp-2">
          {article.summary}
        </p>
      )}

      {/* Meta row */}
      <div className="flex items-center gap-3 mt-0.5">
        <span className="text-[10px] font-medium text-[#4a6080] uppercase tracking-wide">
          {article.source}
        </span>
        <span className="text-[10px] text-[#374559]">·</span>
        <span className="text-[10px] text-[#4a6080]">
          {formatRelativeTime(article.published_at)}
        </span>
        {alert.label && (
          <>
            <span className="text-[10px] text-[#374559]">·</span>
            <span className={`text-[10px] font-semibold uppercase tracking-wide ${alert.color}`}>
              {alert.label}
            </span>
          </>
        )}
      </div>
    </motion.div>
  );
}
