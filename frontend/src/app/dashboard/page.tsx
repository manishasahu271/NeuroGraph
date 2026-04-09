"use client";

import { useEffect, useMemo, useState } from "react";
import { Activity, BookOpen, GitBranch, Share2 } from "lucide-react";
import { GraphStats } from "@/components/GraphStats";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { getGraphStats, getHealth, triggerIngest } from "@/lib/api";

const LABEL_COLORS: Record<string, string> = {
  Biomarker: "var(--node-biomarker)",
  Symptom: "var(--node-symptom)",
  Condition: "var(--node-condition)",
  ClinicalEvidence: "var(--node-evidence)",
  RiskFactor: "var(--node-risk)"
};

export default function DashboardPage() {
  const [health, setHealth] = useState<string>("unknown");
  const [stats, setStats] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [seeding, setSeeding] = useState(false);
  const [error, setError] = useState<string | null>(null);

  async function refresh() {
    setLoading(true);
    setError(null);
    try {
      const h = await getHealth();
      setHealth(h.status);
      const s = await getGraphStats();
      setStats(s);
    } catch (e: any) {
      setError(e?.message || "Failed to load");
    } finally {
      setLoading(false);
    }
  }

  useEffect(() => {
    refresh();
  }, []);

  const cards = useMemo(() => {
    const totals = stats?.totals || {};
    const nodeLabels = stats?.nodes_by_label || [];
    const studies = nodeLabels.find((x: any) => x.label === "ClinicalEvidence")?.count || 0;
    const biomarkers = nodeLabels.find((x: any) => x.label === "Biomarker")?.count || 0;
    return [
      { label: "Total Nodes", value: totals.nodes ?? 0, icon: Share2 },
      { label: "Relationships", value: totals.relationships ?? 0, icon: GitBranch },
      { label: "Clinical Studies", value: studies, icon: BookOpen },
      { label: "Biomarkers Tracked", value: biomarkers, icon: Activity }
    ];
  }, [stats]);

  const composition = useMemo(() => {
    const rows = stats?.nodes_by_label || [];
    const total = rows.reduce((acc: number, r: any) => acc + (r.count || 0), 0) || 1;
    return rows.map((r: any) => ({
      label: r.label,
      count: r.count,
      pct: Math.round(((r.count || 0) / total) * 100)
    }));
  }, [stats]);

  const connected = health === "ok";

  return (
    <div className="space-y-10 pb-12">
      <div className="flex flex-col gap-4 sm:flex-row sm:items-end sm:justify-between">
        <div>
          <h1 className="text-[32px] font-semibold tracking-[-0.02em] text-text-primary">Dashboard</h1>
          <p className="mt-2 max-w-xl text-[15px] text-text-secondary">
            Live metrics for the NeuroGraph knowledge graph and ingestion pipeline.
          </p>
        </div>
        <div className="flex items-center gap-3">
          <span
            className="inline-flex items-center gap-2 rounded-full border border-border bg-white px-3 py-1.5 text-[12px] font-medium text-text-secondary shadow-soft"
            title="API health"
          >
            <span className={`h-2 w-2 rounded-full ${connected ? "bg-node-evidence" : "bg-node-condition"}`} />
            {connected ? "Connected" : "Disconnected"}
          </span>
          <button
            type="button"
            onClick={() => refresh()}
            className="rounded-lg border border-border bg-white px-4 py-2 text-[14px] font-medium text-text-secondary transition hover:bg-linen"
          >
            Refresh
          </button>
          <button
            type="button"
            disabled={seeding}
            onClick={async () => {
              setSeeding(true);
              setError(null);
              try {
                await triggerIngest();
                await refresh();
              } catch (e: any) {
                setError(e?.message || "Seed failed");
              } finally {
                setSeeding(false);
              }
            }}
            className="ng-btn-scale rounded-lg bg-almond-silk px-4 py-2 text-[14px] font-medium text-white shadow-soft hover:brightness-95 disabled:opacity-50"
          >
            {seeding ? "Seeding…" : "Seed Database"}
          </button>
        </div>
      </div>

      {error ? (
        <div className="rounded-xl border border-node-condition/30 bg-node-condition/5 px-4 py-3 text-[14px] text-node-condition">
          {error}
        </div>
      ) : null}

      {loading ? <LoadingSpinner label="Loading metrics…" /> : null}
      <GraphStats items={cards} />

      <section className="rounded-2xl border border-border bg-card-bg p-6 shadow-soft sm:p-8">
        <h2 className="text-2xl font-semibold tracking-[-0.02em] text-text-primary">Graph composition</h2>
        <p className="mt-1 text-[14px] text-text-secondary">Node counts by type in the connected Neo4j database.</p>
        <div className="mt-8 space-y-4">
          {composition.length ? (
            composition.map((row: { label: string; count: number; pct: number }) => (
              <div key={row.label}>
                <div className="mb-1.5 flex items-center justify-between text-[12px]">
                  <span className="font-medium uppercase tracking-[0.05em] text-text-muted">{row.label}</span>
                  <span className="text-text-secondary">
                    {row.count} <span className="text-text-muted">({row.pct}%)</span>
                  </span>
                </div>
                <div className="h-3 w-full overflow-hidden rounded-full bg-linen">
                  <div
                    className="h-full rounded-full transition-all duration-500"
                    style={{
                      width: `${row.pct}%`,
                      backgroundColor: LABEL_COLORS[row.label] || "var(--almond-silk)"
                    }}
                  />
                </div>
              </div>
            ))
          ) : (
            <p className="text-[14px] text-text-muted">Run seed to populate metrics.</p>
          )}
        </div>
      </section>

      <div className="grid gap-6 md:grid-cols-2">
        <div className="rounded-2xl border border-border bg-card-bg p-6 shadow-soft">
          <h3 className="text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted">Nodes by label</h3>
          <pre className="mt-3 max-h-72 overflow-auto rounded-lg border border-border bg-porcelain p-3 text-[11px] leading-relaxed text-text-secondary">
            {JSON.stringify(stats?.nodes_by_label || [], null, 2)}
          </pre>
        </div>
        <div className="rounded-2xl border border-border bg-card-bg p-6 shadow-soft">
          <h3 className="text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted">Relationships by type</h3>
          <pre className="mt-3 max-h-72 overflow-auto rounded-lg border border-border bg-porcelain p-3 text-[11px] leading-relaxed text-text-secondary">
            {JSON.stringify(stats?.relationships_by_type || [], null, 2)}
          </pre>
        </div>
      </div>
    </div>
  );
}
