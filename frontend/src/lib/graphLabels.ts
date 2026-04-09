import type { GraphNode } from "./types";

/** Short label for graph canvas (esp. ClinicalEvidence: journal + year, not raw DOI). */
export function getNodeDisplayLabel(node: Pick<GraphNode, "id" | "label" | "group" | "properties">): string {
  if (node.group === "ClinicalEvidence") {
    const p = node.properties || {};
    const journal = String(p.journal ?? "").trim();
    const year = p.year;
    if (journal && year != null && String(year).length) {
      return `${journal} ${year}`;
    }
    const title = String(p.title ?? "").trim();
    if (title) {
      const parts = title.split(/\s+/);
      const words = parts.slice(0, 5).join(" ");
      return parts.length > 5 ? `${words}…` : words;
    }
    const id = String(node.id);
    const tail = id.split("/").pop() || id;
    return `Study ${tail}`;
  }
  const raw = (node.label || node.id).trim();
  if (raw.includes("_")) {
    return raw
      .split("_")
      .map((w) => (w ? w.charAt(0).toUpperCase() + w.slice(1).toLowerCase() : w))
      .join(" ");
  }
  return raw;
}

export function getGraphNodeSize(group: string): number {
  switch (group) {
    case "Condition":
      return 10;
    case "Biomarker":
      return 8;
    case "Symptom":
      return 7;
    case "RiskFactor":
      return 6;
    case "ClinicalEvidence":
      return 4;
    default:
      return 6;
  }
}

export function getGraphNodeColor(group: string): string {
  switch (group) {
    case "Biomarker":
      return "#7c9eb2";
    case "Symptom":
      return "#d4956a";
    case "Condition":
      return "#c46b6b";
    case "ClinicalEvidence":
      return "#8aad7e";
    case "RiskFactor":
      return "#c4a94d";
    default:
      return "#9a8b80";
  }
}
