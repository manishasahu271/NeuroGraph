export interface GraphNode {
  id: string;
  label: string;
  group: "Biomarker" | "Symptom" | "Condition" | "ClinicalEvidence" | "RiskFactor" | string;
  description: string;
  properties: Record<string, unknown>;
}

export interface GraphLink {
  source: string;
  target: string;
  type: string;
  properties: Record<string, unknown>;
}

export interface QueryResponse {
  answer: string;
  paths: GraphPath[];
  evidence: Evidence[];
}

export interface GraphPath {
  biomarker: string;
  symptom: string;
  condition: string;
  confidence: number;
  strength?: number;
  correlation?: number;
}

export interface Evidence {
  title: string;
  doi: string;
  journal: string;
  year: number;
  summary: string;
}

export interface GraphResponse {
  nodes: GraphNode[];
  links: GraphLink[];
}

