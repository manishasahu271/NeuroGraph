import { ArrowRight } from "lucide-react";

const EXAMPLES = [
  "What does declining typing speed indicate?",
  "My sleep is fragmented and I'm more forgetful — what could this mean?",
  "What biomarkers are linked to early Alzheimer's?",
  "Show me the connection between social isolation and depression"
];

export function ExampleQueries({ onPick }: { onPick: (q: string) => void }) {
  return (
    <div className="mb-4 grid gap-3 sm:grid-cols-2">
      {EXAMPLES.map((q) => (
        <button
          key={q}
          type="button"
          onClick={() => onPick(q)}
          className="group ng-card-lift flex items-center justify-between gap-3 rounded-xl border border-border bg-linen p-4 text-left transition-colors hover:border-almond-silk/30 hover:bg-powder-petal"
        >
          <span className="text-[14px] leading-snug text-text-secondary">{q}</span>
          <ArrowRight
            className="h-4 w-4 shrink-0 text-text-muted transition-transform group-hover:translate-x-0.5 group-hover:text-almond-silk"
            strokeWidth={2}
          />
        </button>
      ))}
    </div>
  );
}
