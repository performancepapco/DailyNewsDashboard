import { clsx, type ClassValue } from "clsx";
import { twMerge } from "tailwind-merge";

export function cn(...inputs: ClassValue[]) {
  return twMerge(clsx(inputs));
}

export const CATEGORY_META: Record<
  string,
  { label: string; color: string; borderColor: string; bgColor: string; icon: string }
> = {
  international:  { label: "International News",     color: "text-blue-400",   borderColor: "border-blue-500",   bgColor: "bg-blue-500/10",   icon: "Globe" },
  national:       { label: "National News · India",  color: "text-indigo-400", borderColor: "border-indigo-500", bgColor: "bg-indigo-500/10", icon: "Flag" },
  andhra:         { label: "Andhra Pradesh",          color: "text-violet-400", borderColor: "border-violet-500", bgColor: "bg-violet-500/10", icon: "MapPin" },
  logistics:      { label: "Logistics & Markets",    color: "text-amber-400",  borderColor: "border-amber-500",  bgColor: "bg-amber-500/10",  icon: "Truck" },
  gconnect:       { label: "GConnect Updates",       color: "text-emerald-400",borderColor: "border-emerald-500",bgColor: "bg-emerald-500/10",icon: "Building2" },
  indiapost:      { label: "India Post",             color: "text-orange-400", borderColor: "border-orange-500", bgColor: "bg-orange-500/10", icon: "Mail" },
  gazette:        { label: "Gazette Notifications",  color: "text-red-400",    borderColor: "border-red-500",    bgColor: "bg-red-500/10",    icon: "FileText" },
  google_trends:  { label: "Google Trends",          color: "text-cyan-400",   borderColor: "border-cyan-500",   bgColor: "bg-cyan-500/10",   icon: "TrendingUp" },
  twitter_trends: { label: "X / Twitter Trends",    color: "text-sky-400",    borderColor: "border-sky-500",    bgColor: "bg-sky-500/10",    icon: "MessageSquare" },
  ai:             { label: "AI Updates",             color: "text-purple-400", borderColor: "border-purple-500", bgColor: "bg-purple-500/10", icon: "Bot" },
};

export const ALERT_META: Record<string, { label: string; color: string; dot: string }> = {
  critical:    { label: "Critical",     color: "text-red-400",    dot: "bg-red-500" },
  important:   { label: "Important",   color: "text-amber-400",  dot: "bg-amber-500" },
  positive:    { label: "Positive",    color: "text-emerald-400",dot: "bg-emerald-500" },
  none:        { label: "",            color: "",                 dot: "" },
};

export function formatRelativeTime(dateStr: string | null | undefined): string {
  if (!dateStr) return "";
  const diff = Date.now() - new Date(dateStr).getTime();
  const mins = Math.floor(diff / 60000);
  if (mins < 1) return "just now";
  if (mins < 60) return `${mins}m ago`;
  const hrs = Math.floor(mins / 60);
  if (hrs < 24) return `${hrs}h ago`;
  return `${Math.floor(hrs / 24)}d ago`;
}

export function formatIST(date: Date): string {
  return date.toLocaleString("en-IN", {
    timeZone: "Asia/Kolkata",
    weekday: "long",
    day: "numeric",
    month: "long",
    year: "numeric",
  });
}
