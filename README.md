# Regulatory Intelligence Dashboard

A live, AI-powered regulatory intelligence tool monitoring 8 global health authorities — automatically fetching, filtering, and summarizing the latest updates every day.

## 🔗 Live demo
👉 [sahils0305.github.io/EMA-FDA---Regulatory-Bulletin](https://sahils0305.github.io/EMA-FDA---Regulatory-Bulletin/)

## Agencies & bodies monitored
- 🇪🇺 EMA — News & Press Releases
- 🇪🇺 EMA — Regulatory & Procedural Guidelines
- 🇺🇸 FDA — Press Releases
- 🇬🇧 MHRA — Inspectorate Updates
- 🇦🇺 TGA — Therapeutic Goods Administration
- 🇨🇦 Health Canada — Drug Products
- 🌍 IMDRF — International Medical Device Regulators Forum (global harmonization body)
- 🌍 WHO — World Health Organization

## What it does
- Pulls live updates from 8 official regulatory RSS feeds daily
- Filters to the most recent 30 days
- Uses Groq AI (Llama 3.1) to generate plain-language summaries of each update
- Displays everything as a searchable, filterable live bulletin with per-agency filtering
- Features the latest update prominently with full-width display
- Auto-updates every morning at 7am UTC via GitHub Actions — zero manual input

## Why I built this
Regulatory Affairs professionals spend significant time manually monitoring agency websites for updates across multiple markets. During my internship at Dabur International Ltd. in Dubai, one of my tasks was visiting health authority websites across multiple markets to track herbal and health product regulation updates — one country at a time, entirely manually. This tool automates exactly that, and adds AI-generated context so the update is immediately actionable.

## How to run it locally
1. Clone the repo
2. Add your Groq API key to a `.env` file as `GROQ_API_KEY`
3. Run `pip install feedparser groq`
4. Run `python generate_bulletin.py`

## Tech stack
Python · feedparser · Groq API (Llama 3.1) · GitHub Actions · GitHub Pages

## Background
Built as a portfolio project ahead of an MSc in Process Validation and Regulatory Affairs at The Technological University of The Shannon, Moylish Campus, Limerick, Ireland. Prior experience includes regulatory lifecycle management across GCC, CIS, and observational exposure to EU/US markets at Dabur International Ltd. and Vieco Pharmaceuticals, Dubai.
