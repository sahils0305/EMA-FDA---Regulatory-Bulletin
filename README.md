# Regulatory Intelligence Platform

An AI-powered regulatory intelligence tool that automatically monitors global health authorities, agencies, feeds, classifies updates, flags required actions, tracks open consultations, and publishes a live searchable bulletin — updated daily with zero manual input.

## 🔗 Live Demo
👉 [Regulatory Intelligence Tool](https://sahils0305.github.io/EMA-FDA---Regulatory-Bulletin/)

---

## The Problem
Regulatory Affairs professionals spend significant time manually monitoring health authority websites across multiple markets. During my internship at Dabur International Ltd. in Dubai, one of my tasks was visiting health authority websites across multiple markets to track herbal and health product regulation updates — one country at a time, entirely manually. This tool attempts to automate the monitoring and adds an AI-powered intelligence layer so updates are immediately actionable.

---

## Agencies Monitored
| Agency | Region | Feed Type |
|--------|--------|-----------|
| EMA — News & Press | EU | RSS |
| EMA — Regulatory Guidelines | EU | RSS |
| FDA | US | RSS |
| MHRA (MedRegs) | UK | RSS |
| TGA | Australia | RSS |
| Health Canada | Canada | RSS |
| IMDRF | Global | RSS |
| WHO | Global | RSS |

---

## Features
- **Live monitoring** of 8 global regulatory RSS feeds, agencies and authorities
- **Deduplication engine** — merges entries appearing across multiple agencies
- **AI classification** — each update is analyzed for action type, therapeutic area, and action required level
- **Action Required flagging** — Red (Action Required) / Amber (Monitor) / Green (Awareness) per update
- **Open Consultation Tracker** — surfaces consultation-type updates separately with deadline extraction
- **AI summaries** — plain-language one-sentence summary per update
- **Search and multi-agency filtering**
- **Featured latest update** — most recent item displayed prominently
- **Copy Weekly Brief** — one-click export of the full bulletin as formatted plain text
- **Auto-updates daily** at 7am UTC via GitHub Actions
- **Mobile responsive** dark premium design

---

## Architecture
RSS Feeds (8 sources)

↓

Feed Parser (Python / feedparser)

↓

Deduplication Engine (title similarity matching)

↓

AI Analysis Layer (Groq API / Llama 3.1)

→ Summary

→ Action Type (Guideline / Safety Alert / Approval / Consultation / etc.)

→ Action Required (Action Required / Monitor / Awareness)

→ Therapeutic Area (Small Molecule / Biologic / Medical Device / etc.)

→ Consultation Deadline (if applicable)

↓

HTML Generation (Python)

→ Open Consultation Tracker

→ Featured Latest Update

→ Searchable Card Grid

→ Copy Weekly Brief

↓

GitHub Actions (daily cron at 7am UTC)

↓

GitHub Pages (live public URL)

---

## Tech Stack
- **Python** — feed ingestion, deduplication, HTML generation
- **feedparser** — RSS parsing
- **Groq API (Llama 3.1)** — AI analysis and summarization
- **GitHub Actions** — daily automation (cron schedule)
- **GitHub Pages** — free static hosting
- **Vanilla HTML/CSS/JS** — frontend (no frameworks, no dependencies)

---

## How to Run Locally
1. Clone the repo
2. Install dependencies: `pip install feedparser groq`
3. Set your Groq API key as an environment variable: `export GROQ_API_KEY=your_key_here`
4. Run: `python generate_bulletin.py`
5. Open `index.html` in your browser

---

## Future Roadmap
- [ ] Trend Detection — track update frequency per agency over time
- [ ] Regulatory Divergence Flagging — detect when FDA and EMA issue conflicting guidance on the same topic
- [ ] Horizon Scanning — surface upcoming Committee meeting agendas and expected guidance
- [ ] Regulatory Calendar View — timeline of implementation deadlines and consultation closing dates
- [ ] "What This Means" Impact Layer — structured impact assessment per update (affected functions, regulatory risk, recommended actions)

---

## Background
Built as a portfolio project ahead of an MSc in Process Validation and Regulatory Affairs at The Technological University of The Shannon, Moylish Campus, Limerick, Ireland. Prior experience includes tenure as regulatory affairs intern at Dabur International Ltd. and a quality control intern at Vieco Pharmaceuticals, Dubai.

---

*Always verify against official agency sources before using for regulatory decision-making.*
