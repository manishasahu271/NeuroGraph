"use client";

import { Info, X } from "lucide-react";
import { useEffect, useState } from "react";

const STORAGE_KEY = "neurograph-health-banner-dismissed";

export function HealthBanner() {
  const [dismissed, setDismissed] = useState(false);

  useEffect(() => {
    try {
      if (localStorage.getItem(STORAGE_KEY) === "1") setDismissed(true);
    } catch {
      /* ignore */
    }
  }, []);

  if (dismissed) return null;

  return (
    <div className="sticky top-16 z-20 border-b border-border bg-powder-petal/80 backdrop-blur-sm">
      <div className="mx-auto flex w-full max-w-7xl items-start gap-3 px-4 py-3 sm:px-6 lg:px-8">
        <Info className="mt-0.5 h-4 w-4 shrink-0 text-text-muted" aria-hidden />
        <p className="flex-1 text-[12px] font-medium leading-relaxed text-text-secondary sm:text-[13px]">
          NeuroGraph is a research demonstration tool. It is not a medical device. Always consult a healthcare
          professional.
        </p>
        <button
          type="button"
          onClick={() => {
            try {
              localStorage.setItem(STORAGE_KEY, "1");
            } catch {
              /* ignore */
            }
            setDismissed(true);
          }}
          className="ng-btn-scale rounded-lg p-1 text-text-muted transition-colors hover:bg-white/60 hover:text-text-secondary"
          aria-label="Dismiss notice"
        >
          <X className="h-4 w-4" />
        </button>
      </div>
    </div>
  );
}
