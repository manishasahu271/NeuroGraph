import type { Config } from "tailwindcss";

const config: Config = {
  content: ["./src/**/*.{ts,tsx}"],
  theme: {
    extend: {
      colors: {
        almond: { silk: "var(--almond-silk)" },
        powder: { petal: "var(--powder-petal)" },
        linen: "var(--linen)",
        porcelain: "var(--porcelain)",
        "text-primary": "var(--text-primary)",
        "text-secondary": "var(--text-secondary)",
        "text-muted": "var(--text-muted)",
        border: "var(--border)",
        "page-bg": "var(--page-bg)",
        "card-bg": "var(--card-bg)",
        "input-bg": "var(--input-bg)",
        hover: "var(--hover)",
        active: "var(--active)",
        node: {
          biomarker: "var(--node-biomarker)",
          symptom: "var(--node-symptom)",
          condition: "var(--node-condition)",
          evidence: "var(--node-evidence)",
          risk: "var(--node-risk)"
        }
      },
      fontFamily: {
        sans: ["Inter", "-apple-system", "BlinkMacSystemFont", "sans-serif"]
      },
      fontSize: {
        h1: ["32px", { lineHeight: "1.2", fontWeight: "600" }],
        h2: ["24px", { lineHeight: "1.3", fontWeight: "600" }],
        h3: ["18px", { lineHeight: "1.4", fontWeight: "600" }],
        body: ["15px", { lineHeight: "1.6", fontWeight: "400" }]
      },
      boxShadow: {
        soft: "0 1px 3px rgba(45, 36, 32, 0.06)",
        card: "0 4px 20px rgba(45, 36, 32, 0.06)"
      }
    }
  },
  plugins: []
};

export default config;
