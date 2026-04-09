# 🧠 NeuroGraph

**What if your phone could tell you your brain was struggling before you even noticed?**

NeuroGraph is an AI-powered cognitive health knowledge graph that connects digital behavioral patterns from everyday device usage to cognitive symptoms and clinical conditions. It uses RDF knowledge graph modeling, GraphRAG retrieval, and clinical research evidence to provide explainable, traceable health insights.

![NeuroGraph](https://img.shields.io/badge/Neo4j-Knowledge_Graph-blue) ![Python](https://img.shields.io/badge/Python-FastAPI-green) ![Next.js](https://img.shields.io/badge/Next.js-Frontend-black) ![Docker](https://img.shields.io/badge/Docker-Containerized-blue)

## 🏗️ Architecture

```
┌─────────────────────────────┐     ┌──────────────────────────────────┐
│   Vercel (Frontend)         │     │   Railway (Backend + Database)   │
│                             │     │                                  │
│   Next.js 14 App            │────▶│   FastAPI Backend (Python)       │
│   • Chat Interface          │ API │   • GraphRAG Query Engine        │
│   • Graph Explorer          │     │   • ETL Pipeline                 │
│   • Dashboard               │     │   • RDF Export                   │
│                             │     │                                  │
│                             │     │   Neo4j 5 Database               │
│                             │     │   • RDF Knowledge Graph          │
│                             │     │   • 65 nodes, 111 relationships  │
└─────────────────────────────┘     └──────────────────────────────────┘
```

## 🔬 How It Works

1. **ETL Pipeline** ingests clinical research data, extracts entities (behavioral patterns, symptoms, conditions), and loads them as RDF-style triples into Neo4j
2. **Knowledge Graph** models relationships: Behavioral Patterns → Symptoms → Conditions, backed by published clinical studies with DOI links
3. **GraphRAG Engine** converts natural language questions into Cypher queries, traverses the graph, and generates explainable answers with evidence citations
4. **RDF Export** outputs the graph in standard Turtle format for interoperability with other semantic web tools

## 💡 Example Queries

- "I've been typing slower and making more mistakes lately — should I be concerned?"
- "I'm sleeping badly and keep forgetting things — what could be going on?"
- "I can't focus at work, I'm always switching between apps"
- "I've stopped going out and lost interest in things I used to enjoy"

Each response includes:
- Plain English explanation
- Graph reasoning paths (Pattern → Symptom → Condition) with confidence scores
- Clinical studies with DOI links supporting each connection

## 🛠️ Tech Stack

| Layer | Technology |
|-------|-----------|
| Knowledge Graph | Neo4j 5, RDF, SPARQL, Cypher |
| AI/LLM | LangChain, OpenAI GPT-4o-mini, Hugging Face Sentence Transformers |
| Backend | Python, FastAPI, rdflib |
| Frontend | Next.js 14, React 18, Tailwind CSS, react-force-graph-2d |
| ETL | Custom Python pipeline with Airflow orchestration, embedding-based deduplication |
| Infrastructure | Docker, Docker Compose, Vercel (frontend), Railway (backend) |

## 📊 Knowledge Graph Schema

**Node Types:**
- **Behavioral Patterns** (20) — typing speed, sleep patterns, mobility, app usage, social interactions
- **Symptoms** (15) — memory lapses, attention deficit, fatigue, mood changes, etc.
- **Conditions** (10) — MCI, Alzheimer's, depression, anxiety, burnout, ADHD, Parkinson's, etc.
- **Clinical Evidence** (12) — peer-reviewed studies from Nature Medicine, JMIR, npj Dementia, etc.
- **Risk Factors** (8) — age, lifestyle, genetics, social isolation

**Relationships:**
- `INDICATES` — behavioral pattern signals a symptom (with strength score)
- `ASSOCIATED_WITH` — symptom linked to condition (with correlation score)
- `SUPPORTS` — clinical study backs a connection
- `INCREASES_RISK_OF` — risk factor raises condition probability
- `COMORBID_WITH` — conditions that co-occur

## 📚 Research Foundation

Built on published peer-reviewed research:
- [AI and Wearables for Cognitive Impairment Detection](https://doi.org/10.2196/86262) — JMIR, 2026
- [Smartphone Sensing for Cognitive Impairment](https://doi.org/10.48550/arXiv.2509.23158) — arXiv, 2025
- [Smartwatch-Based MCI Detection](https://doi.org/10.1038/s41591-025-03468-w) — Nature Medicine, 2025
- [Voice Analysis for Cognitive Impairment](https://doi.org/10.1038/s44400-025-00040-0) — npj Dementia, 2025

## 🚀 Quick Start

```bash
# Clone
git clone https://github.com/manishasahu271/NeuroGraph.git
cd NeuroGraph

# Configure
cp backend/.env.example backend/.env  # Add your API keys

# Run
docker-compose up

# Visit http://localhost:3000
# Go to Dashboard → Click "Seed Database" to populate the graph
```

## ⚠️ Disclaimer

NeuroGraph is a research demonstration tool. It is not a medical device and should not be used for clinical diagnosis. Always consult a healthcare professional.

## 📄 License

MIT
