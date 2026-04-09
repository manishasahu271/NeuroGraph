"use client";

import { useCallback, useEffect, useMemo, useState } from "react";
import { Search, X } from "lucide-react";
import { GraphViewer } from "@/components/GraphViewer";
import { NodeDetail } from "@/components/NodeDetail";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { getGraphData } from "@/lib/api";
import { getNodeDisplayLabel } from "@/lib/graphLabels";
import type { GraphLink, GraphNode } from "@/lib/types";

const GROUPS = ["Biomarker", "Symptom", "Condition", "ClinicalEvidence", "RiskFactor"] as const;

const PILL_ACTIVE: Record<string, string> = {
  Biomarker: "bg-node-biomarker/90 text-white border-transparent shadow-sm",
  Symptom: "bg-node-symptom/90 text-white border-transparent shadow-sm",
  Condition: "bg-node-condition/90 text-white border-transparent shadow-sm",
  ClinicalEvidence: "bg-node-evidence/90 text-white border-transparent shadow-sm",
  RiskFactor: "bg-node-risk/90 text-white border-transparent shadow-sm"
};

const PILL_DOT: Record<string, string> = {
  Biomarker: "bg-node-biomarker",
  Symptom: "bg-node-symptom",
  Condition: "bg-node-condition",
  ClinicalEvidence: "bg-node-evidence",
  RiskFactor: "bg-node-risk"
};

export default function ExplorePage() {
  const [nodes, setNodes] = useState<GraphNode[]>([]);
  const [links, setLinks] = useState<GraphLink[]>([]);
  const [loading, setLoading] = useState(true);
  const [selected, setSelected] = useState<GraphNode | null>(null);
  const [search, setSearch] = useState("");
  const [focusLabel, setFocusLabel] = useState<string | null>(null);
  const [filters, setFilters] = useState<Record<string, boolean>>({
    Biomarker: true,
    Symptom: true,
    Condition: true,
    ClinicalEvidence: true,
    RiskFactor: true
  });

  const loadFull = useCallback(async () => {
    setLoading(true);
    try {
      const data = await getGraphData();
      setNodes(data.nodes);
      setLinks(data.links);
      setSelected(null);
      setFocusLabel(null);
    } finally {
      setLoading(false);
    }
  }, []);

  useEffect(() => {
    loadFull();
  }, [loadFull]);

  const filtered = useMemo(() => {
    const s = search.trim().toLowerCase();
    const ns = nodes.filter((n) => {
      if (filters[n.group] === false) return false;
      if (!s) return true;
      const hay = `${n.id} ${n.label} ${getNodeDisplayLabel(n)}`.toLowerCase();
      return hay.includes(s);
    });
    const allowed = new Set(ns.map((n) => n.id));
    const ls = links.filter((l) => allowed.has(String(l.source)) && allowed.has(String(l.target)));
    return { nodes: ns, links: ls };
  }, [nodes, links, search, filters]);

  async function loadSubgraph(id: string, fallback?: GraphNode) {
    setLoading(true);
    try {
      const data = await getGraphData(id);
      setNodes(data.nodes);
      setLinks(data.links);
      const found = data.nodes.find((n) => n.id === id) ?? null;
      setSelected(found ?? fallback ?? null);
      setFocusLabel(id);
    } catch (e) {
      console.error(e);
      setFocusLabel(null);
      setSelected(fallback ?? null);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8 pb-12">
      <div>
        <h1 className="text-[32px] font-semibold tracking-[-0.02em] text-text-primary">Explore the Knowledge Graph</h1>
        <p className="mt-2 max-w-3xl text-[15px] leading-relaxed text-text-secondary">
          Pan, zoom, and filter an interactive view of biomarkers, symptoms, conditions, evidence, and risk factors.
        </p>
      </div>

      <div className="rounded-2xl border border-border bg-card-bg p-5 shadow-soft sm:p-6">
        <div className="flex flex-col gap-4 lg:flex-row lg:items-center">
          <div className="relative flex-1">
            <Search className="pointer-events-none absolute left-4 top-1/2 h-4 w-4 -translate-y-1/2 text-text-muted" />
            <input
              className="w-full rounded-full border border-border bg-linen py-3 pl-11 pr-4 text-[15px] text-text-primary placeholder:text-text-muted focus:border-almond-silk focus:outline-none focus:ring-2 focus:ring-almond-silk/20"
              value={search}
              onChange={(e) => setSearch(e.target.value)}
              placeholder="Search nodes…"
              aria-label="Search graph nodes"
            />
          </div>
          <div className="flex flex-wrap items-center gap-2 lg:justify-end">
            {focusLabel ? (
              <button
                type="button"
                onClick={() => loadFull()}
                className="inline-flex items-center gap-1.5 rounded-full border border-border bg-powder-petal px-3 py-1.5 text-[12px] font-medium text-text-secondary transition hover:bg-linen"
              >
                Focus: {focusLabel}
                <X className="h-3.5 w-3.5" />
              </button>
            ) : null}
            {GROUPS.map((g) => {
              const on = filters[g];
              return (
                <button
                  key={g}
                  type="button"
                  onClick={() => setFilters((f) => ({ ...f, [g]: !f[g] }))}
                  className={`inline-flex items-center gap-2 rounded-full border px-3 py-1.5 text-[12px] font-medium transition ${
                    on
                      ? `${PILL_ACTIVE[g]}`
                      : "border-border bg-white text-text-secondary hover:bg-linen"
                  }`}
                >
                  <span className={`h-2 w-2 rounded-full ${PILL_DOT[g]}`} />
                  {g}
                </button>
              );
            })}
          </div>
        </div>
        <div className="mt-3 flex flex-wrap gap-2">
          <button
            type="button"
            onClick={() => loadSubgraph("typing_speed_decline")}
            className="text-[12px] font-medium text-almond-silk underline-offset-4 hover:underline"
          >
            Quick focus: typing_speed_decline
          </button>
        </div>
      </div>

      {loading ? <LoadingSpinner label="Loading graph…" /> : null}

      <div
        className={`grid min-h-0 gap-6 lg:gap-8 ${
          selected ? "lg:grid-cols-[minmax(0,1fr)_min(360px,38vw)]" : "lg:grid-cols-1"
        }`}
      >
        <div
          className="relative min-h-[480px] min-w-0 w-full lg:min-h-0"
          style={{ height: "calc(100vh - 220px)" }}
        >
          <GraphViewer
            variant="explore"
            nodes={filtered.nodes}
            links={filtered.links}
            height={640}
            onNodeClick={(n) => {
              setSelected(n);
              void loadSubgraph(n.id, n);
            }}
          />
          {!selected ? (
            <p className="pointer-events-none absolute bottom-20 left-1/2 z-[5] max-w-sm -translate-x-1/2 text-center text-[13px] text-text-muted">
              Click a node to view details and connections.
            </p>
          ) : null}
        </div>
        {selected ? (
          <div className="min-w-0 lg:max-w-none">
            <NodeDetail
              node={selected}
              links={links}
              allNodes={nodes}
              onSelectNeighbor={(id) => {
                const neighbor = nodes.find((x) => x.id === id);
                void loadSubgraph(id, neighbor);
              }}
            />
          </div>
        ) : (
          <div className="rounded-2xl border border-border bg-card-bg p-5 shadow-soft lg:hidden">
            <p className="text-[14px] text-text-secondary">
              Click a node in the graph to view details and connections.
            </p>
          </div>
        )}
      </div>
    </div>
  );
}
