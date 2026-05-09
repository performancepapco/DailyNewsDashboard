export interface Article {
  id: number;
  date_key: string;
  category: string;
  title: string;
  summary: string;
  source: string;
  url: string;
  published_at: string | null;
  score: number;
  alert_level: string;
}

export interface CategoryData {
  name: string;
  articles: Article[];
}

export interface DashboardData {
  date: string;
  categories: Record<string, CategoryData>;
  total_items: number;
  alerts: Article[];
  gazette_count: number;
  ai_count: number;
  last_refreshed: string | null;
}

export async function fetchDashboard(): Promise<DashboardData | null> {
  try {
    const res = await fetch("/api/dashboard", { next: { revalidate: 300 } });
    if (!res.ok) return null;
    return res.json();
  } catch {
    return null;
  }
}

export async function fetchWeather(
  apiKey: string,
  city = "Vijayawada",
  country = "IN"
): Promise<{ temp: number; description: string; icon: string } | null> {
  try {
    const res = await fetch(
      `https://api.openweathermap.org/data/2.5/weather?q=${city},${country}&appid=${apiKey}&units=metric`
    );
    if (!res.ok) return null;
    const data = await res.json();
    return {
      temp: Math.round(data.main.temp),
      description: data.weather[0].description,
      icon: data.weather[0].icon,
    };
  } catch {
    return null;
  }
}

export async function triggerRefresh(): Promise<boolean> {
  try {
    const res = await fetch("/api/refresh", { method: "POST" });
    return res.ok;
  } catch {
    return false;
  }
}
