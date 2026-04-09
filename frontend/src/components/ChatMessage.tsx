import type { Evidence, GraphPath } from "@/lib/types";
import { ExternalLink } from "lucide-react";

function doiUrl(doi: string) {
  return `https://doi.org/${encodeURIComponent(doi)}`;
}

function formatConfidencePct(c: number | undefined): string {
  if (c == null || Number.isNaN(c)) return "—";
  const n = c <= 1 ? c * 100 : c;
  return `${Math.round(n)}%`;
}

function confidenceBadgeClass(conf: number | undefined): string {
  if (conf == null || Number.isNaN(conf)) return "bg-linen text-text-muted";
  const x = conf <= 1 ? conf : conf / 100;
  if (x >= 0.8) return "bg-node-evidence/25 text-[#5a7a52] ring-1 ring-node-evidence/30";
  if (x >= 0.65) return "bg-almond-silk/20 text-text-primary ring-1 ring-almond-silk/25";
  return "bg-powder-petal text-text-secondary ring-1 ring-border";
}

export function ChatMessage({
  role,
  content,
  paths,
  evidence
}: {
  role: "user" | "assistant";
  content: string;
  paths?: GraphPath[];
  evidence?: Evidence[];
}) {
  const isUser = role === "user";
  return (
    <div className={`ng-msg-in flex ${isUser ? "justify-end" : "justify-start"}`}>
      <div
        className={`max-w-[min(100%,820px)] rounded-2xl px-5 py-4 ${
          isUser
            ? "bg-almond-silk text-white shadow-soft"
            : "border border-border bg-card-bg text-text-primary shadow-soft"
        }`}
      >
        <div className={`text-[15px] leading-relaxed ${isUser ? "text-white" : "text-text-primary"}`}>{content}</div>

        {!isUser && paths && paths.length > 0 ? (
          <details className="mt-4 group/paths border-t border-border pt-4">
            <summary className="cursor-pointer text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted transition group-open/paths:text-text-secondary">
              Graph paths
            </summary>
            <div className="mt-3 space-y-3">
              {paths.map((p, idx) => (
                <div
                  key={`${p.biomarker}-${p.symptom}-${p.condition}-${idx}`}
                  className="rounded-lg bg-linen p-4 ring-1 ring-border/60"
                >
                  <div className="mb-2 flex flex-wrap items-center gap-2">
                    <span
                      className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-semibold ${confidenceBadgeClass(p.confidence)}`}
                    >
                      {formatConfidencePct(p.confidence)}
                    </span>
                    {p.strength != null && p.correlation != null ? (
                      <span className="text-[11px] text-text-muted">
                        INDICATES {formatConfidencePct(p.strength)} · ASSOCIATED{" "}
                        {formatConfidencePct(p.correlation)}
                      </span>
                    ) : null}
                  </div>
                  <div className="text-[14px] font-medium leading-relaxed text-text-primary">
                    <span className="text-node-biomarker">{p.biomarker.replaceAll("_", " ")}</span>
                    <span className="mx-1.5 text-text-muted">→</span>
                    <span className="text-node-symptom">{p.symptom.replaceAll("_", " ")}</span>
                    <span className="mx-1.5 text-text-muted">→</span>
                    <span className="text-node-condition">{p.condition.replaceAll("_", " ")}</span>
                  </div>
                </div>
              ))}
            </div>
          </details>
        ) : null}

        {!isUser && evidence && evidence.length > 0 ? (
          <details className="mt-4 group/ev border-t border-border pt-4">
            <summary className="cursor-pointer text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted transition group-open/ev:text-text-secondary">
              Clinical evidence
            </summary>
            <div className="mt-3 space-y-3">
              {evidence.map((e) => (
                <a
                  key={e.doi}
                  href={doiUrl(e.doi)}
                  target="_blank"
                  rel="noreferrer"
                  className="ng-card-lift block rounded-lg border border-l-[3px] border-border border-l-node-evidence bg-white px-4 py-3 shadow-soft transition hover:ring-1 hover:ring-border"
                >
                  <div className="flex items-start justify-between gap-2">
                    <div className="text-[15px] font-semibold text-text-primary">{e.title}</div>
                    <ExternalLink className="mt-0.5 h-4 w-4 shrink-0 text-text-muted" />
                  </div>
                  <div className="mt-1 text-[12px] text-text-muted">
                    {e.journal} · {e.year} · DOI {e.doi}
                  </div>
                  {e.summary ? <div className="mt-2 text-[13px] leading-relaxed text-text-secondary">{e.summary}</div> : null}
                </a>
              ))}
            </div>
          </details>
        ) : null}
      </div>
    </div>
  );
}
