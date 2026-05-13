"use client";

import { useCallback, useEffect, useState } from "react";
import { fetchDashboard, type DashboardData, type Article } from "@/lib/api";
import { CATEGORY_META } from "@/lib/utils";
import Header from "@/components/Header";
import CategoryCard from "@/components/CategoryCard";
import TrendCard from "@/components/TrendCard";
import AlertBanner from "@/components/AlertBanner";
import SearchBar from "@/components/SearchBar";
import StrategicSignals from "@/components/StrategicSignals";
import ExportMenu from "@/components/ExportMenu";

const TREND_CATEGORIES = ["google_trends", "twitter_trends"] as const;
const NEWS_CATEGORIES = [
  "international", "national", "andhra",
  "logistics", "gconnect", "indiapost", "gazette", "ai",
  "viral_news", "health_wealth_ai",
] as const;

export default function DashboardPage() {
  const [data, setData] = useState<DashboardData | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [searchQuery, setSearchQuery] = useState("");
  const [searchCategory, setSearchCategory] = useState("all");

  const load = useCallback(async () => {
    setLoading(true);
    setError(false);
    const result = await fetchDashboard();
    if (result) setData(result);
    else setError(true);
    setLoading(false);
  }, []);

  // Initial load + auto-refresh every 5 minutes
  useEffect(() => {
    load();
    const id = setInterval(load, 5 * 60 * 1000);
    return () => clearInterval(id);
  }, [load]);

  // Filter articles by search query + category
  const filteredData = useCallback((): DashboardData | null => {
    if (!data) return null;
    if (!searchQuery && searchCategory === "all") return data;

    const filterArticles = (articles: Article[]): Article[] =>
      articles.filter((a) => {
        const matchesCat = searchCategory === "all" || a.category === searchCategory;
        const matchesQ =
          !searchQuery ||
          a.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
          a.summary.toLowerCase().includes(searchQuery.toLowerCase());
        return matchesCat && matchesQ;
      });

    const newCats = Object.fromEntries(
      Object.entries(data.categories).map(([key, cat]) => [
        key,
        { ...cat, articles: filterArticles(cat.articles) },
      ])
    );

    return {
      ...data,
      categories: newCats,
      total_items: Object.values(newCats).reduce((s, c) => s + c.articles.length, 0),
      alerts: filterArticles(data.alerts),
    };
  }, [data, searchQuery, searchCategory]);

  const visible = filteredData();

  if (loading && !data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4">
        <div className="w-8 h-8 rounded-full border-2 border-blue-500 border-t-transparent animate-spin" />
        <p className="text-sm text-[#4a6080]">Loading intelligence dashboard…</p>
        <p className="text-xs text-[#374559] max-w-sm text-center">
          Connecting to the data backend. This may take a moment on first load.
        </p>
      </div>
    );
  }

  if (error && !data) {
    return (
      <div className="flex flex-col items-center justify-center min-h-screen gap-4 px-4">
        <div className="text-4xl">⚠️</div>
        <h2 className="text-lg font-semibold text-red-400">Backend Unavailable</h2>
        <p className="text-sm text-[#4a6080] max-w-sm text-center">
          Cannot reach the data backend. The service may be starting up — please wait
          30 seconds and retry. If the problem persists, check the backend deployment.
        </p>
        <button
          onClick={load}
          className="px-4 py-2 rounded-lg text-sm font-medium bg-blue-600/20 text-blue-300 border border-blue-500/30 hover:bg-blue-600/35 transition-colors"
        >
          Retry
        </button>
      </div>
    );
  }

  const d = visible ?? data!;

  return (
    <div className="min-h-screen bg-[var(--c-bg)]">
      <Header
        date={d.date}
        totalItems={d.total_items}
        gazetteCount={d.gazette_count}
        aiCount={d.ai_count}
        alertCount={d.alerts.length}
        lastRefreshed={d.last_refreshed}
      />

      <main className="max-w-[1600px] mx-auto px-3 sm:px-5 py-5 flex flex-col gap-5">

        {/* Alert banner */}
        {d.alerts.length > 0 && <AlertBanner alerts={d.alerts} />}

        {/* Search + filter */}
        <SearchBar
          onSearch={(q, cat) => {
            setSearchQuery(q);
            setSearchCategory(cat);
          }}
        />

        {/* Trend cards — horizontal pair */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-3 items-start">
          {TREND_CATEGORIES.map((cat) => (
            <TrendCard
              key={cat}
              category={cat}
              articles={d.categories[cat]?.articles ?? []}
            />
          ))}
        </div>

        {/* Main news — masonry columns, cards flow top-to-bottom and fill gaps */}
        <div className="columns-1 md:columns-2 xl:columns-3 gap-3">
          {NEWS_CATEGORIES.map((cat) => {
            const catData = d.categories[cat];
            if (!catData || catData.articles.length === 0) return null;
            return (
              <div key={cat} className="break-inside-avoid mb-3">
                <CategoryCard category={cat} data={catData} />
              </div>
            );
          })}
        </div>

        {/* Strategic signals footer */}
        {data && <StrategicSignals data={data} />}

        {/* Footer */}
        <footer className="flex items-center justify-between py-4 border-t border-[var(--c-border)] no-print">
          <p className="text-[10px] text-[var(--c-text-faint)]">
            Executive Intelligence Dashboard · Fully local · Auto-refreshes daily at 09:00 AM IST
          </p>
          <ExportMenu />
        </footer>
      </main>
    </div>
  );
}
