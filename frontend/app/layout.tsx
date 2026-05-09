import type { Metadata } from "next";
import "./globals.css";

export const metadata: Metadata = {
  title: "Executive Intelligence Dashboard",
  description: "Daily aggregated briefing — 10 strategic categories, ranked and summarised",
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className="dark">
      <body className="bg-[#0B1220] text-[#f0f4ff] min-h-screen font-sans antialiased">
        {children}
      </body>
    </html>
  );
}
