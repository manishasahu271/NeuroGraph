"use client";

import { getNodeDisplayLabel } from "@/lib/graphLabels";
import type { GraphLink, GraphNode } from "@/lib/types";

const TYPE_STYLES: Record<string, string> = {
  Biomarker: "bg-node-biomarker/15 text-[#4f6b7a] ring-1 ring-node-biomarker/25",
  Symptom: "bg-node-symptom/15 text-[#a15f3a] ring-1 ring-node-symptom/25",
  Condition: "bg-node-condition/15 text-[#a34d4d] ring-1 ring-node-condition/25",
  ClinicalEvidence: "bg-node-evidence/15 text-[#5a7a52] ring-1 ring-node-evidence/25",
  RiskFactor: "bg-node-risk/15 text-[#8a7535] ring-1 ring-node-risk/25"
};

export function NodeDetail({
  node,
  links,
  allNodes,
  onSelectNeighbor
}: {
  node: GraphNode | null;
  links: GraphLink[];
  /** When provided, connection rows use readable labels (e.g. journal+year for evidence). */
  allNodes?: GraphNode[];
  onSelectNeighbor?: (id: string) => void;
}) {
  if (!node) {
    return (
      <div className="rounded-2xl border border-border bg-card-bg p-6 shadow-soft">
        <p className="text-[14px] text-text-secondary">Click a node in the graph to view details and connections.</p>
      </div>
    );
  }

  const neighbors = links
    .filter((l) => l.source === node.id || l.target === node.id)
    .map((l) => ({
      id: l.source === node.id ? l.target : l.source,
      type: l.type
    }));

  const badge = TYPE_STYLES[node.group] || "bg-linen text-text-secondary ring-1 ring-border";

  function connectionLabel(id: string): string {
    const found = allNodes?.find((x) => x.id === id);
    if (found) return getNodeDisplayLabel(found);
    return id.replaceAll("_", " ");
  }

  return (
    <div className="rounded-2xl border border-border bg-card-bg p-6 shadow-card">
      <div className="mb-3">
        <span className={`inline-flex rounded-full px-2.5 py-0.5 text-[11px] font-medium uppercase tracking-[0.05em] ${badge}`}>
          {node.group}
        </span>
      </div>
      <h2 className="text-xl font-semibold tracking-[-0.02em] text-text-primary">{node.label}</h2>
      {node.description ? <p className="mt-2 text-[14px] leading-relaxed text-text-secondary">{node.description}</p> : null}

      <div className="mt-5">
        <h3 className="text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted">Details</h3>
        <pre className="mt-2 max-h-48 overflow-auto rounded-lg border border-border bg-porcelain p-3 text-[11px] leading-relaxed text-text-secondary">
          {JSON.stringify(node.properties, null, 2)}
        </pre>
      </div>

      <div className="mt-6">
        <h3 className="text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted">Connections</h3>
        <ul className="mt-3 space-y-2">
          {neighbors.length ? (
            neighbors.slice(0, 40).map((n) => (
              <li key={`${n.type}-${n.id}`}>
                <button
                  type="button"
                  onClick={() => onSelectNeighbor?.(n.id)}
                  className="flex w-full items-center gap-3 rounded-xl border border-border bg-linen/50 px-3 py-2.5 text-left transition hover:bg-powder-petal"
                >
                  <span className="h-2 w-2 shrink-0 rounded-full bg-almond-silk" />
                  <span className="flex-1 truncate text-[14px] font-medium text-text-primary">
                    {connectionLabel(n.id)}
                  </span>
                  <span className="shrink-0 rounded-full bg-white px-2 py-0.5 text-[10px] font-medium uppercase tracking-wide text-text-muted ring-1 ring-border">
                    {n.type}
                  </span>
                </button>
              </li>
            ))
          ) : (
            <li className="text-[14px] text-text-muted">No connections in the current view.</li>
          )}
        </ul>
      </div>
    </div>
  );
}
