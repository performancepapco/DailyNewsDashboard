"use client";

import { AlertTriangle, AlertCircle, Info, CheckCircle } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import type { Article } from "@/lib/api";

interface Props {
  alerts: Article[];
}

const LEVEL_CONFIG = {
  critical: {
    bg: "bg-red-500/10 border-red-500/30",
    text: "text-red-300",
    icon: AlertTriangle,
    label: "CRITICAL",
  },
  important: {
    bg: "bg-amber-500/10 border-amber-500/30",
    text: "text-amber-300",
    icon: AlertCircle,
    label: "IMPORTANT",
  },
  positive: {
    bg: "bg-emerald-500/10 border-emerald-500/30",
    text: "text-emerald-300",
    icon: CheckCircle,
    label: "POSITIVE",
  },
  informational: {
    bg: "bg-blue-500/10 border-blue-500/30",
    text: "text-blue-300",
    icon: Info,
    label: "INFO",
  },
};

export default function AlertBanner({ alerts }: Props) {
  if (!alerts || alerts.length === 0) return null;

  return (
    <div className="flex flex-col gap-2">
      <h2 className="text-xs font-semibold text-[#4a6080] uppercase tracking-widest px-1">
        Active Alerts
      </h2>
      <AnimatePresence>
        {alerts.slice(0, 5).map((alert, i) => {
          const cfg =
            LEVEL_CONFIG[alert.alert_level as keyof typeof LEVEL_CONFIG] ??
            LEVEL_CONFIG.informational;
          const Icon = cfg.icon;

          return (
            <motion.a
              key={alert.id}
              href={alert.url}
              target="_blank"
              rel="noopener noreferrer"
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: i * 0.06 }}
              className={`flex items-start gap-3 px-4 py-2.5 rounded-lg border
                          ${cfg.bg} hover:brightness-110 transition-all duration-200`}
            >
              <Icon size={13} className={`${cfg.text} mt-0.5 shrink-0`} />
              <div className="min-w-0">
                <span className={`text-[10px] font-bold uppercase tracking-widest ${cfg.text} mr-2`}>
                  {cfg.label}
                </span>
                <span className="text-xs text-[#c8d8f0] leading-snug">{alert.title}</span>
                <span className="block text-[10px] text-[#4a6080] mt-0.5">{alert.source}</span>
              </div>
            </motion.a>
          );
        })}
      </AnimatePresence>
    </div>
  );
}
