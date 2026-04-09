"use client";

import { useMemo, useState } from "react";
import { ArrowUp } from "lucide-react";
import { ExampleQueries } from "@/components/ExampleQueries";
import { ChatMessage } from "@/components/ChatMessage";
import { GraphViewer } from "@/components/GraphViewer";
import { LoadingSpinner } from "@/components/LoadingSpinner";
import { queryGraph } from "@/lib/api";
import type { GraphLink, GraphNode, QueryResponse } from "@/lib/types";

type Msg = { role: "user" | "assistant"; content: string; data?: QueryResponse };

function pathsToGraph(data?: QueryResponse): { nodes: GraphNode[]; links: GraphLink[] } {
  if (!data?.paths?.length) return { nodes: [], links: [] };
  const nodeMap = new Map<string, GraphNode>();
  const links: GraphLink[] = [];

  for (const p of data.paths) {
    const b = p.biomarker;
    const s = p.symptom;
    const c = p.condition;
    if (b)
      nodeMap.set(b, {
        id: b,
        label: b.replaceAll("_", " ").replace(/\b\w/g, (m) => m.toUpperCase()),
        group: "Biomarker",
        description: "",
        properties: {}
      });
    if (s)
      nodeMap.set(s, {
        id: s,
        label: s.replaceAll("_", " ").replace(/\b\w/g, (m) => m.toUpperCase()),
        group: "Symptom",
        description: "",
        properties: {}
      });
    if (c)
      nodeMap.set(c, {
        id: c,
        label: c.replaceAll("_", " ").replace(/\b\w/g, (m) => m.toUpperCase()),
        group: "Condition",
        description: "",
        properties: {}
      });
    if (b && s) links.push({ source: b, target: s, type: "INDICATES", properties: { confidence: p.confidence } });
    if (s && c) links.push({ source: s, target: c, type: "ASSOCIATED_WITH", properties: { confidence: p.confidence } });
  }
  return { nodes: Array.from(nodeMap.values()), links };
}

export default function ChatPage() {
  const [messages, setMessages] = useState<Msg[]>([
    {
      role: "assistant",
      content:
        "Ask about cognitive health, digital biomarkers, and symptoms. I’ll return reasoning paths and evidence from the knowledge graph. (Without an OpenAI key, NeuroGraph uses a deterministic graph routing mode.)"
    }
  ]);
  const [text, setText] = useState("");
  const [loading, setLoading] = useState(false);
  const lastAssistant = [...messages].reverse().find((m) => m.role === "assistant" && m.data)?.data;
  const miniGraph = useMemo(() => pathsToGraph(lastAssistant), [lastAssistant]);

  async function run(q: string) {
    const question = q.trim();
    if (!question) return;
    setLoading(true);
    setMessages((m) => [...m, { role: "user", content: question }]);
    setText("");
    try {
      const data = await queryGraph(question);
      setMessages((m) => [...m, { role: "assistant", content: data.answer, data }]);
    } catch (e: any) {
      setMessages((m) => [
        ...m,
        {
          role: "assistant",
          content: `Request failed: ${e?.message || "unknown error"}`
        }
      ]);
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="space-y-8">
      <div>
        <h1 className="text-[32px] font-semibold tracking-[-0.02em] text-text-primary">Chat</h1>
        <p className="mt-2 max-w-2xl text-[15px] leading-relaxed text-text-secondary">
          Natural language in — explainable graph paths and study citations out.
        </p>
      </div>

      <div className="grid gap-8 md:grid-cols-[3fr_2fr] lg:grid-cols-[7fr_3fr]">
        <div className="flex min-h-[560px] flex-col rounded-2xl border border-border bg-porcelain shadow-soft">
          <div className="flex flex-1 flex-col gap-4 overflow-hidden p-4 sm:p-6">
            <ExampleQueries onPick={(q) => run(q)} />
            <div className="min-h-0 flex-1 space-y-4 overflow-y-auto pr-1">
              {messages.map((m, idx) => (
                <ChatMessage
                  key={idx}
                  role={m.role}
                  content={m.content}
                  paths={m.data?.paths}
                  evidence={m.data?.evidence}
                />
              ))}
              {loading ? <LoadingSpinner label="Thinking…" /> : null}
            </div>
          </div>

          <form
            className="border-t border-border bg-porcelain/90 p-4 sm:p-5"
            onSubmit={(e) => {
              e.preventDefault();
              run(text);
            }}
          >
            <div className="flex items-center gap-2 rounded-full border border-border bg-input-bg py-1 pl-4 pr-1 shadow-inner">
              <input
                className="min-w-0 flex-1 border-0 bg-transparent py-3 text-[15px] text-text-primary placeholder:text-text-muted focus:outline-none focus:ring-0"
                value={text}
                onChange={(e) => setText(e.target.value)}
                placeholder="Ask about cognitive health biomarkers…"
                aria-label="Your question"
              />
              <button
                type="submit"
                disabled={loading}
                className="ng-btn-scale flex h-11 w-11 shrink-0 items-center justify-center rounded-full bg-almond-silk text-white shadow-soft transition hover:brightness-95 disabled:opacity-50"
                aria-label="Send"
              >
                <ArrowUp className="h-5 w-5" strokeWidth={2.25} />
              </button>
            </div>
          </form>
        </div>

        <aside className="flex flex-col gap-4">
          <div className="rounded-2xl border border-border bg-card-bg p-4 shadow-soft">
            <h2 className="text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted">Reasoning paths</h2>
            <p className="mt-1 text-[13px] leading-relaxed text-text-secondary">
              Live mini-graph from the latest assistant reply: Biomarker → Symptom → Condition.
            </p>
          </div>
          <GraphViewer nodes={miniGraph.nodes} links={miniGraph.links} height={400} />
        </aside>
      </div>

    </div>
  );
}
