"use client";

import { useMemo, useState } from "react";
import type { GraphLink, GraphNode } from "@/lib/types";
import { getNodeDisplayLabel } from "@/lib/graphLabels";

const TYPE_ORDER = ["Condition", "Symptom", "Biomarker", "RiskFactor", "ClinicalEvidence"] as const;

const COLORS: Record<string, string> = {
  Biomarker: "#7c9eb2",
  Symptom: "#d4956a",
  Condition: "#c46b6b",
  ClinicalEvidence: "#8aad7e",
  RiskFactor: "#c4a94d"
};

const RADII: Record<string, number> = {
  Condition: 12,
  Biomarker: 9,
  Symptom: 8,
  RiskFactor: 7,
  ClinicalEvidence: 5
};

type Positioned = GraphNode & { cx: number; cy: number };

function typeRingIndex(group: string): number {
  const i = (TYPE_ORDER as readonly string[]).indexOf(group);
  return i >= 0 ? i : TYPE_ORDER.length;
}

function nodeRadius(group: string, compact: boolean): number {
  const base = RADII[group] ?? 7;
  return compact ? Math.max(4, base * 0.72) : base;
}

export function ExploreStaticGraph({
  nodes,
  links,
  onNodeClick,
  compact = false,
  emptyHint
}: {
  nodes: GraphNode[];
  links: GraphLink[];
  onNodeClick?: (node: GraphNode) => void;
  /** Tighter rings and type for sidebar / chat mini-graph. */
  compact?: boolean;
  emptyHint?: string;
}) {
  const [hoveredId, setHoveredId] = useState<string | null>(null);

  const { positioned, viewBox, bg, idToPos } = useMemo(() => {
    const empty = {
      positioned: [] as Positioned[],
      viewBox: "0 0 800 600",
      bg: { x: 0, y: 0, w: 800, h: 600 },
      idToPos: new Map<string, Positioned>()
    };
    if (!nodes.length) return empty;

    const ring0 = compact ? 36 : 130;
    const ringStep = compact ? 34 : 88;

    const positioned: Positioned[] = nodes.map((node) => {
      const ti = typeRingIndex(node.group);
      const nodesOfType = nodes.filter((n) => n.group === node.group);
      const indexInType = nodesOfType.indexOf(node);
      const nType = Math.max(nodesOfType.length, 1);
      const angleStep = (2 * Math.PI) / nType;
      const radius = ring0 + ti * ringStep;
      const angle = angleStep * indexInType - Math.PI / 2;
      return {
        ...node,
        cx: radius * Math.cos(angle),
        cy: radius * Math.sin(angle)
      };
    });

    const idToPos = new Map(positioned.map((n) => [n.id, n]));

    let minX = Infinity;
    let minY = Infinity;
    let maxX = -Infinity;
    let maxY = -Infinity;
    const labelPad = compact ? 40 : 56;
    for (const n of positioned) {
      const r = nodeRadius(n.group, compact);
      minX = Math.min(minX, n.cx - r - labelPad);
      maxX = Math.max(maxX, n.cx + r + labelPad);
      minY = Math.min(minY, n.cy - r - (compact ? 8 : 12));
      maxY = Math.max(maxY, n.cy + r + labelPad);
    }
    const pad = compact ? 48 : 72;
    const bw = maxX - minX + pad * 2;
    const bh = maxY - minY + pad * 2;
    const bx = minX - pad;
    const by = minY - pad;
    const vb = `${bx.toFixed(1)} ${by.toFixed(1)} ${bw.toFixed(1)} ${bh.toFixed(1)}`;

    return { positioned, viewBox: vb, bg: { x: bx, y: by, w: bw, h: bh }, idToPos };
  }, [nodes, compact]);

  const linkTouchesHover = (sourceId: string, targetId: string) =>
    hoveredId && (sourceId === hoveredId || targetId === hoveredId);

  if (!positioned.length) {
    return (
      <div
        className={`flex h-full w-full items-center justify-center text-text-muted ${
          compact ? "min-h-[140px] px-3 text-center text-xs" : "min-h-[320px] text-sm"
        }`}
      >
        {emptyHint ?? "No nodes to display."}
      </div>
    );
  }

  return (
    <svg
      role="img"
      aria-label="Knowledge graph"
      viewBox={viewBox}
      className="h-full w-full select-none"
      preserveAspectRatio="xMidYMid meet"
    >
      <rect x={bg.x} y={bg.y} width={bg.w} height={bg.h} fill="#fbfefb" />

      {links.map((link, i) => {
        const s = idToPos.get(String(link.source));
        const t = idToPos.get(String(link.target));
        if (!s || !t) return null;
        const active = linkTouchesHover(String(link.source), String(link.target));
        return (
          <line
            key={`${link.source}-${link.target}-${i}`}
            x1={s.cx}
            y1={s.cy}
            x2={t.cx}
            y2={t.cy}
            stroke="#d0b8ac"
            strokeOpacity={active ? 0.55 : 0.28}
            strokeWidth={active ? 1.5 : 1}
          />
        );
      })}

      {positioned.map((node) => {
        const r = nodeRadius(node.group, compact);
        const fill = COLORS[node.group] ?? "#9a8b80";
        const label = getNodeDisplayLabel(node);
        const maxLen = compact ? 20 : 28;
        const short =
          label.length > maxLen ? `${label.slice(0, compact ? 18 : 26)}…` : label;
        const isHover = hoveredId === node.id;

        return (
          <g
            key={node.id}
            role="button"
            className="cursor-pointer outline-none focus:ring-2 focus:ring-almond-silk/40"
            onMouseEnter={() => setHoveredId(node.id)}
            onMouseLeave={() => setHoveredId(null)}
            onClick={() => onNodeClick?.(node)}
            onKeyDown={(e) => {
              if (e.key === "Enter" || e.key === " ") {
                e.preventDefault();
                onNodeClick?.(node);
              }
            }}
            tabIndex={0}
          >
            <circle
              cx={node.cx}
              cy={node.cy}
              r={isHover ? r * 1.12 : r}
              fill={fill}
              stroke="white"
              strokeWidth={1.5}
              style={{ transition: "r 0.15s ease-out" }}
            />
            <text
              x={node.cx}
              y={node.cy + r + (compact ? 11 : 14)}
              textAnchor="middle"
              fontSize={compact ? 8 : 10}
              fill="#2d2420"
              fontFamily="Inter, system-ui, sans-serif"
              fontWeight={500}
              className="pointer-events-none"
            >
              {short}
            </text>
          </g>
        );
      })}
    </svg>
  );
}
