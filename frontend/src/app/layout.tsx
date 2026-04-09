import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Navbar } from "@/components/Navbar";
import { HealthBanner } from "@/components/HealthBanner";

const inter = Inter({
  subsets: ["latin"],
  weight: ["300", "400", "500", "600", "700"],
  display: "swap",
  variable: "--font-inter"
});

export const metadata: Metadata = {
  title: "NeuroGraph",
  description: "AI-powered cognitive health knowledge graph"
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" className={inter.variable}>
      <body className={`${inter.className} min-h-screen bg-page-bg text-text-primary antialiased`}>
        <Navbar />
        <HealthBanner />
        <main className="mx-auto min-h-[calc(100vh-8rem)] w-full max-w-7xl px-4 py-10 sm:px-6 lg:px-8">
          <div className="ng-page-enter">{children}</div>
        </main>
      </body>
    </html>
  );
}
