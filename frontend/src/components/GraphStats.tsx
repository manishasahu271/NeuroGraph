import type { LucideIcon } from "lucide-react";

export function GraphStats({
  items
}: {
  items: Array<{ label: string; value: string | number; hint?: string; icon?: LucideIcon }>;
}) {
  return (
    <div className="grid gap-4 sm:grid-cols-2 xl:grid-cols-4">
      {items.map((it) => {
        const Icon = it.icon;
        return (
          <div
            key={it.label}
            className="ng-card-lift relative overflow-hidden rounded-2xl border border-border bg-card-bg p-6 shadow-soft"
          >
            {Icon ? (
              <Icon className="absolute right-4 top-4 h-5 w-5 text-text-muted opacity-80" strokeWidth={1.5} />
            ) : null}
            <div className="text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted">{it.label}</div>
            <div className="mt-2 text-[36px] font-semibold leading-none tracking-[-0.02em] text-text-primary">
              {it.value}
            </div>
            {it.hint ? <div className="mt-2 text-[12px] text-text-muted">{it.hint}</div> : null}
          </div>
        );
      })}
    </div>
  );
}
