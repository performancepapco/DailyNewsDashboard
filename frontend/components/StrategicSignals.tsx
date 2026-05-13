"use client";

import { Zap, ShieldAlert, Bot, Building2, type LucideIcon } from "lucide-react";
import type { Article, DashboardData } from "@/lib/api";

interface Props {
  data: DashboardData;
}

function SignalSection({
  icon: Icon,
  label,
  color,
  items,
}: {
  icon: LucideIcon;
  label: string;
  color: string;
  items: Article[];
}) {
  return (
    <div className="glass-card flex flex-col gap-2 p-4">
      <div className="flex items-center gap-2 mb-1">
        <Icon size={13} className={color} />
        <span className={`text-xs font-bold uppercase tracking-widest ${color}`}>{label}</span>
      </div>
      {items.length === 0 ? (
        <p className="text-xs italic" style={{ color: "var(--c-text-faint)" }}>Nothing flagged today.</p>
      ) : (
        <ul className="flex flex-col gap-1.5">
          {items.slice(0, 4).map((a) => (
            <li key={a.id}>
              <a
                href={a.url}
                target="_blank"
                rel="noopener noreferrer"
                className={`text-xs leading-relaxed flex items-start gap-1.5 transition-colors hover:text-[var(--c-text-med)]`}
                style={{ color: "var(--c-text-sec)" }}
              >
                <span className={`${color} mt-0.5 shrink-0`}>›</span>
                <span>{a.title}</span>
              </a>
            </li>
          ))}
        </ul>
      )}
    </div>
  );
}

export default function StrategicSignals({ data }: Props) {
  const allArticles = Object.values(data.categories).flatMap((c) => c.articles);

  const signals = allArticles.filter((a) => a.score >= 0.8).slice(0, 4);
  const risks = allArticles.filter((a) => a.alert_level === "critical").slice(0, 4);
  const aiItems = (data.categories["ai"]?.articles ?? []).slice(0, 4);
  const govItems = [
    ...(data.categories["gazette"]?.articles ?? []),
    ...(data.categories["indiapost"]?.articles ?? []),
    ...(data.categories["gconnect"]?.articles ?? []),
  ].slice(0, 4);

  return (
    <section className="mt-8 mb-6">
      <h2 className="text-xs font-semibold uppercase tracking-widest mb-3 px-1" style={{ color: "var(--c-text-muted)" }}>
        Today's Strategic Summary
      </h2>
      <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-3">
        <SignalSection icon={Zap}        label="Strategic Signals" color="text-blue-400"    items={signals} />
        <SignalSection icon={ShieldAlert} label="Emerging Risks"    color="text-red-400"     items={risks} />
        <SignalSection icon={Bot}        label="AI Watch"          color="text-purple-400"  items={aiItems} />
        <SignalSection icon={Building2}  label="Government Watch"  color="text-emerald-400" items={govItems} />
      </div>
    </section>
  );
}
