import Link from "next/link";
import { BookOpen, MessageCircle, Network } from "lucide-react";

const FEATURES = [
  {
    title: "Ask Questions",
    description:
      "Query the knowledge graph in natural language and get explainable answers backed by clinical research.",
    icon: MessageCircle
  },
  {
    title: "Explore Connections",
    description:
      "Visualize how digital biomarkers connect to symptoms and conditions through an interactive graph.",
    icon: Network
  },
  {
    title: "Research-Backed",
    description: "Every connection is supported by published peer-reviewed clinical studies.",
    icon: BookOpen
  }
];

export default function HomePage() {
  return (
    <div className="space-y-16 pb-16">
      <section className="relative overflow-hidden rounded-3xl border border-border bg-porcelain shadow-card">
        <div className="hero-graph-bg absolute inset-0 opacity-70" aria-hidden />
        <div className="relative px-6 py-16 text-center sm:px-12 sm:py-20">
          <p className="mb-4 text-[11px] font-medium uppercase tracking-[0.05em] text-text-muted">
            AI · Knowledge graph · Explainable clinical context
          </p>
          <h1 className="mx-auto max-w-[700px] text-balance text-[32px] font-semibold leading-tight tracking-[-0.02em] text-text-primary sm:text-[40px]">
            What if your phone could tell you your brain was struggling before you even noticed?
          </h1>
          <p className="mx-auto mt-6 max-w-2xl text-[15px] leading-relaxed text-text-secondary sm:text-[18px]">
            NeuroGraph maps digital biomarkers to cognitive health using AI-powered knowledge graphs.
          </p>
          <div className="mt-10 flex flex-wrap items-center justify-center gap-4">
            <Link
              href="/chat"
              className="ng-btn-scale inline-flex items-center justify-center rounded-full bg-almond-silk px-8 py-[14px] text-[15px] font-medium text-white shadow-soft transition hover:brightness-95"
            >
              Try it now
            </Link>
            <Link
              href="/explore"
              className="ng-btn-scale inline-flex items-center justify-center rounded-full border border-border bg-white px-8 py-[14px] text-[15px] font-medium text-text-secondary transition hover:bg-linen"
            >
              Explore the graph
            </Link>
          </div>
        </div>
      </section>

      <section className="grid gap-6 md:grid-cols-3">
        {FEATURES.map((f) => {
          const Icon = f.icon;
          return (
            <div
              key={f.title}
              className="ng-card-lift rounded-2xl border border-border bg-card-bg p-8 shadow-soft"
            >
              <div className="mb-5 flex h-11 w-11 items-center justify-center rounded-xl bg-linen text-text-muted">
                <Icon className="h-5 w-5" strokeWidth={1.75} />
              </div>
              <h3 className="text-[18px] font-semibold text-text-primary">{f.title}</h3>
              <p className="mt-2 text-[15px] leading-relaxed text-text-secondary">{f.description}</p>
            </div>
          );
        })}
      </section>

      <section className="rounded-2xl border border-border bg-white p-8 shadow-soft sm:p-10">
        <h2 className="text-2xl font-semibold tracking-[-0.02em] text-text-primary">Start with example questions</h2>
        <p className="mt-2 max-w-xl text-[15px] leading-relaxed text-text-secondary">
          Open Chat to see Biomarker → Symptom → Condition paths and citations from the literature.
        </p>
        <div className="mt-6">
          <Link
            href="/chat"
            className="ng-btn-scale inline-flex rounded-full bg-almond-silk px-6 py-3 text-sm font-medium text-white hover:brightness-95"
          >
            Go to Chat
          </Link>
        </div>
      </section>
    </div>
  );
}
