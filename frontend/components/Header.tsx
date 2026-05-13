"use client";

import { useEffect, useState } from "react";
import { RefreshCw, Cloud, Newspaper, FileText, Bot, TrendingUp, Sun, Moon } from "lucide-react";
import { triggerRefresh } from "@/lib/api";
import { formatIST } from "@/lib/utils";
import { useTheme } from "./ThemeProvider";

interface Props {
  date: string;
  totalItems: number;
  gazetteCount: number;
  aiCount: number;
  alertCount: number;
  lastRefreshed: string | null;
}

export default function Header({
  date,
  totalItems,
  gazetteCount,
  aiCount,
  alertCount,
  lastRefreshed,
}: Props) {
  const [clock, setClock] = useState("");
  const [refreshing, setRefreshing] = useState(false);
  const [refreshMsg, setRefreshMsg] = useState("");
  const { theme, toggle } = useTheme();

  useEffect(() => {
    const tick = () => {
      const now = new Date();
      setClock(
        now.toLocaleTimeString("en-IN", {
          timeZone: "Asia/Kolkata",
          hour: "2-digit",
          minute: "2-digit",
          second: "2-digit",
          hour12: true,
        })
      );
    };
    tick();
    const id = setInterval(tick, 1000);
    return () => clearInterval(id);
  }, []);

  const handleRefresh = async () => {
    setRefreshing(true);
    setRefreshMsg("");
    const ok = await triggerRefresh();
    setRefreshing(false);
    setRefreshMsg(ok ? "Refresh started — data updates in ~1 min" : "Refresh failed — backend may be offline");
    setTimeout(() => setRefreshMsg(""), 6000);
  };

  const formattedDate = date
    ? new Date(date).toLocaleDateString("en-IN", {
        timeZone: "Asia/Kolkata",
        weekday: "long",
        day: "numeric",
        month: "long",
        year: "numeric",
      })
    : "";

  return (
    <header className="sticky top-0 z-30 backdrop-blur-xl border-b"
      style={{ backgroundColor: "var(--c-header-bg)", borderColor: "var(--c-border)" }}>
      <div className="max-w-[1600px] mx-auto px-4 py-3 flex flex-wrap items-center justify-between gap-3">

        {/* Brand + Date */}
        <div className="flex flex-col">
          <h1 className="text-base font-display font-bold text-gradient tracking-tight leading-none">
            Executive Intelligence
          </h1>
          <p className="text-[11px] mt-0.5 font-medium" style={{ color: "var(--c-text-muted)" }}>
            {formattedDate}
          </p>
        </div>

        {/* Live clock */}
        <div className="hidden sm:flex flex-col items-center">
          <span className="text-xl font-mono font-bold tabular-nums tracking-widest"
            style={{ color: "var(--c-text-med)" }}>
            {clock}
          </span>
          <span className="text-[10px] tracking-widest" style={{ color: "var(--c-text-faint)" }}>IST</span>
        </div>

        {/* Metrics chips */}
        <div className="flex flex-wrap items-center gap-2">
          <div className="metric-chip">
            <Newspaper size={11} className="text-blue-400" />
            <span style={{ color: "var(--c-text-sec)" }}>{totalItems} stories</span>
          </div>
          <div className="metric-chip">
            <FileText size={11} className="text-red-400" />
            <span style={{ color: "var(--c-text-sec)" }}>{gazetteCount} gazettes</span>
          </div>
          <div className="metric-chip">
            <Bot size={11} className="text-purple-400" />
            <span style={{ color: "var(--c-text-sec)" }}>{aiCount} AI</span>
          </div>
          {alertCount > 0 && (
            <div className="metric-chip border-red-500/30 animate-pulse-slow">
              <TrendingUp size={11} className="text-red-400" />
              <span className="text-red-400 font-semibold">{alertCount} alerts</span>
            </div>
          )}
        </div>

        {/* Actions */}
        <div className="flex items-center gap-2">
          {/* Theme toggle */}
          <button
            onClick={toggle}
            title={theme === "dark" ? "Switch to light mode" : "Switch to dark mode"}
            className="flex items-center justify-center w-8 h-8 rounded-lg transition-all duration-200
                       border hover:scale-105 active:scale-95"
            style={{
              background: theme === "dark" ? "rgba(251,191,36,0.10)" : "rgba(99,102,241,0.10)",
              borderColor: theme === "dark" ? "rgba(251,191,36,0.25)" : "rgba(99,102,241,0.25)",
              color: theme === "dark" ? "#fbbf24" : "#818cf8",
            }}
          >
            {theme === "dark" ? <Sun size={14} /> : <Moon size={14} />}
          </button>

          {/* Refresh */}
          <div className="flex flex-col items-end gap-0.5">
            <button
              onClick={handleRefresh}
              disabled={refreshing}
              className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium
                         bg-blue-600/20 hover:bg-blue-600/35 text-blue-300
                         border border-blue-500/30 transition-all duration-200 disabled:opacity-50"
            >
              <RefreshCw size={12} className={refreshing ? "animate-spin" : ""} />
              {refreshing ? "Refreshing…" : "Refresh Now"}
            </button>
            {refreshMsg && (
              <span className="text-[10px] max-w-[180px] text-right" style={{ color: "var(--c-text-muted)" }}>
                {refreshMsg}
              </span>
            )}
            {lastRefreshed && !refreshMsg && (
              <span className="text-[10px]" style={{ color: "var(--c-text-faint)" }}>
                Last: {new Date(lastRefreshed).toLocaleTimeString("en-IN", { timeZone: "Asia/Kolkata", hour: "2-digit", minute: "2-digit", hour12: true })} IST
              </span>
            )}
          </div>
        </div>
      </div>
    </header>
  );
}
