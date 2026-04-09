import type { GraphResponse, QueryResponse } from "@/lib/types";

const API = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

async function check(res: Response) {
  if (!res.ok) {
    const txt = await res.text().catch(() => "");
    throw new Error(`API ${res.status}: ${txt || res.statusText}`);
  }
  return res;
}

export async function queryGraph(question: string): Promise<QueryResponse> {
  const res = await fetch(`${API}/api/query`, {
    method: "POST",
    headers: { "Content-Type": "application/json" },
    body: JSON.stringify({ question })
  });
  await check(res);
  return (await res.json()) as QueryResponse;
}

export async function getGraphData(node?: string): Promise<GraphResponse> {
  const url = node ? `${API}/api/graph?node=${encodeURIComponent(node)}` : `${API}/api/graph`;
  const res = await fetch(url, { cache: "no-store" });
  await check(res);
  return (await res.json()) as GraphResponse;
}

export async function getHealth(): Promise<{ status: string }> {
  const res = await fetch(`${API}/api/health`, { cache: "no-store" });
  await check(res);
  return (await res.json()) as { status: string };
}

export async function triggerIngest(): Promise<any> {
  const res = await fetch(`${API}/api/ingest`, { method: "POST" });
  await check(res);
  return await res.json();
}

export async function getGraphStats(): Promise<any> {
  const res = await fetch(`${API}/api/stats`, { cache: "no-store" });
  await check(res);
  return await res.json();
}

