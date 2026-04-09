"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";

const LINKS = [
  { href: "/", label: "Home" },
  { href: "/chat", label: "Chat" },
  { href: "/explore", label: "Explore" },
  { href: "/dashboard", label: "Dashboard" }
];

export function Navbar() {
  const pathname = usePathname();

  return (
    <header className="sticky top-0 z-30 h-16 border-b border-border bg-white shadow-soft">
      <div className="mx-auto flex h-full w-full max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link
          href="/"
          className="flex items-center gap-2 text-text-primary transition-opacity hover:opacity-80"
        >
          <span className="text-xl leading-none" aria-hidden>
            🧠
          </span>
          <span className="text-base font-semibold tracking-[-0.02em] text-text-primary">NeuroGraph</span>
        </Link>
        <nav className="flex items-center gap-1 sm:gap-2">
          {LINKS.map((l) => {
            const active = pathname === l.href || (l.href !== "/" && pathname.startsWith(l.href));
            return (
              <Link
                key={l.href}
                href={l.href}
                className={`relative px-3 py-2 text-sm font-medium text-text-secondary transition-colors hover:text-text-primary ${
                  active ? "text-text-primary" : ""
                }`}
              >
                {l.label}
                {active ? (
                  <span
                    className="absolute bottom-0 left-2 right-2 h-0.5 rounded-full bg-almond-silk"
                    aria-hidden
                  />
                ) : null}
              </Link>
            );
          })}
        </nav>
      </div>
    </header>
  );
}
