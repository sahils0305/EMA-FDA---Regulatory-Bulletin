# Regulatory Intelligence Bulletin

An automated regulatory monitoring tool. Every day it pulls updates from health-authority feeds, uses AI to draft a summary and classification for each one, tracks open consultations, and publishes a searchable public bulletin. It runs with no manual input.

## 🔗 Live Demo
👉 [Regulatory Intelligence Bulletin](https://sahils0305.github.io/EMA-FDA---Regulatory-Bulletin/)

> **Status: working prototype.** The AI analysis has not yet been independently validated (see [Validation](#validation-in-progress)). It is a screening aid, not a compliance tool.

---

## The Problem
Regulatory Affairs teams spend significant time checking health-authority websites across markets. During my internship at Dabur International Ltd. in Dubai, part of my work was visiting these sites one country at a time to track regulatory updates for herbal and health products. This project automates the monitoring and adds an AI layer to help prioritise what to read first.

---

## Sources Monitored
| Source | Region | Feed |
|--------|--------|------|
| EMA – News | EU | RSS |
| EMA – Regulatory & Procedural Guidelines | EU | RSS |
| FDA – Press Releases | US | RSS |
| MHRA (MedRegs blog) | UK | RSS |
| Health Canada | Canada | RSS |
| TGA | Australia | RSS |
| WHO | Global | RSS |

TGA and WHO restrict automated access and can be unreliable. The live **Source Health** panel on the site shows each source as *Operational*, *No new updates* or *Failed*, so gaps are visible rather than hidden.

Not included: IMDRF (its feed has been inactive since 2021) and ICH (no official RSS feed).

---

## Features
- **Daily automated monitoring** of regulator feeds (30-day window)
- **Deduplication** — merges the same story reported by several sources
- **Official source vs AI separation** — each card shows official information (title, date, link) apart from the AI-assisted analysis
- **AI-assisted analysis** — summary, "why it matters", update type, therapeutic area, action level (Action Required / Monitor / Awareness)
- **Traceability** — every AI output is stamped with model, prompt version and retrieval time
- **Open Consultation Tracker** — consultations shown separately; past deadlines are hidden
- **Source Health panel** — status, item count and latest item date per source
- **AI failure tripwire** — if more than 25% of AI calls fail, the run stops and the last good page stays online instead of publishing empty analyses
- **Daily JSON snapshots** (`data/`) kept for future trend analysis
- Search, per-source filtering, one-click "Copy Weekly Brief", mobile-responsive design

---

## Architecture
```
Regulator RSS feeds
        ↓
Feed parsing (Python / feedparser) + source health check
        ↓
Deduplication (title similarity)
        ↓
AI analysis (Groq API, GPT-OSS 20B, prompt v2)
  → summary, why it matters, update type,
    action level, therapeutic area, consultation deadline
        ↓
Failure tripwire (stop if >25% of AI calls fail)
        ↓
Daily snapshot saved to data/  +  static HTML page generated
        ↓
GitHub Actions (daily, 07:00 UTC)  →  GitHub Pages
```

## Tech Stack
- **Python**, **feedparser** — ingestion, deduplication, page generation
- **Groq API (openai/gpt-oss-20b)** — AI analysis
- **GitHub Actions** — daily schedule
- **GitHub Pages** — hosting
- **Vanilla HTML/CSS/JS** — frontend, no frameworks

---

## Validation (in progress)
AI output can be wrong, so I am testing it. I am hand-labelling 100+ real updates (update type, action level, therapeutic area) from my own reading of the source, then comparing against the AI's labels to measure accuracy and review the errors. Results will be published here once complete. No accuracy figures are claimed until then.

---

## Limitations
- AI summaries and classifications can be wrong or incomplete; always check the linked official source.
- Coverage depends on what each regulator publishes as a feed. It is not a complete record of regulatory change.
- It does not assess compliance or replace professional regulatory judgement.

---

## How to Run Locally
1. Clone the repo
2. `pip install feedparser groq python-dateutil`
3. Set your key: `export GROQ_API_KEY=your_key_here`
4. `python generate_bulletin.py`
5. Open `index.html`

---

## Roadmap
- [x] Source health monitoring and AI failure tripwire
- [x] Daily snapshots for trend analysis
- [ ] Validation study and published accuracy results
- [ ] Trend detection — update frequency per source over time
- [ ] Regulatory calendar — consultation closing dates and implementation deadlines
- [ ] Divergence flagging — where FDA and EMA guidance on the same topic differs
- [ ] Structured impact notes per update

---

## About
Built by Sahil Subramaniam, MSc Process Validation & Regulatory Affairs (Pharmaceuticals) student at TUS Moylish Campus, Limerick. Previously Regulatory Affairs Intern at Dabur International Ltd. and Quality Control Intern at Vieco Pharmaceuticals, Dubai. Built with AI-assisted development tools; I designed, tested and maintain the system.

[LinkedIn](https://www.linkedin.com/in/sahil-subramaniam-1007272b3)

*Always verify against official agency sources before using for regulatory decision-making.*
