"use client";

import type { GraphLink, GraphNode } from "@/lib/types";
import { ExploreStaticGraph } from "@/components/ExploreStaticGraph";

export type GraphViewerVariant = "default" | "explore";

export function GraphViewer({
  nodes,
  links,
  height = 520,
  onNodeClick,
  variant = "default"
}: {
  nodes: GraphNode[];
  links: GraphLink[];
  height?: number;
  onNodeClick?: (node: GraphNode) => void;
  variant?: GraphViewerVariant;
}) {
  if (variant === "explore") {
    return (
      <div className="relative h-full min-h-[400px] w-full overflow-hidden rounded-2xl border border-border bg-porcelain shadow-card">
        <div className="absolute inset-0 min-h-0">
          <ExploreStaticGraph nodes={nodes} links={links} onNodeClick={onNodeClick} />
        </div>
        <div className="pointer-events-none absolute bottom-4 left-4 z-10 rounded-xl border border-border bg-white/90 p-3 text-xs shadow-soft backdrop-blur-sm">
          <div className="mb-2 font-medium text-text-primary">Legend</div>
          <ul className="space-y-1.5 text-text-secondary">
            <li className="flex items-center gap-2">
              <span className="h-3 w-3 shrink-0 rounded-full bg-[#7c9eb2]" />
              Behavioral pattern
            </li>
            <li className="flex items-center gap-2">
              <span className="h-3 w-3 shrink-0 rounded-full bg-[#d4956a]" />
              Symptom
            </li>
            <li className="flex items-center gap-2">
              <span className="h-3 w-3 shrink-0 rounded-full bg-[#c46b6b]" />
              Condition
            </li>
            <li className="flex items-center gap-2">
              <span className="h-3 w-3 shrink-0 rounded-full bg-[#8aad7e]" />
              Clinical evidence
            </li>
            <li className="flex items-center gap-2">
              <span className="h-3 w-3 shrink-0 rounded-full bg-[#c4a94d]" />
              Risk factor
            </li>
          </ul>
        </div>
      </div>
    );
  }

  return (
    <div
      className="overflow-hidden rounded-2xl border border-border bg-porcelain shadow-card"
      style={{ height }}
    >
      <ExploreStaticGraph
        compact
        nodes={nodes}
        links={links}
        onNodeClick={onNodeClick}
        emptyHint="No paths yet — ask a question that returns graph reasoning."
      />
    </div>
  );
}
