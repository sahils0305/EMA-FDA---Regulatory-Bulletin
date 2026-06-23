# EMA + FDA Regulatory Intelligence Bulletin

A live regulatory intelligence tool that automatically fetches, filters, and AI-summarizes the latest updates from the European Medicines Agency (EMA) and the US Food and Drug Administration (FDA).

## What it does
- Pulls live updates from 3 official regulatory RSS feeds (EMA News, EMA Guidelines, FDA Press Releases)
- Filters to the most recent 30 days only
- Uses Groq AI (Llama 3.1) to generate a plain-language one-sentence summary of each update
- Displays everything as a clean, styled bulletin with source links

## Why I built this
Regulatory Affairs professionals spend significant time manually monitoring agency websites for updates across multiple markets. This tool automates that monitoring and surfaces what matters, with AI-generated context — reducing the time from "something changed" to "I understand what changed and why it matters."

## How to run it
1. Open `bulletin.ipynb` in Google Colab
2. Add your Groq API key to Colab Secrets as `GROQ_API_KEY` (free at console.groq.com)
3. Run the notebook — a fresh bulletin generates in about 1 minute

## Tech stack
- Python
- feedparser (RSS ingestion)
- Groq API / Llama 3.1 (AI summarization)
- Google Colab (execution environment)

## Data sources
- [EMA News and Press Releases](https://www.ema.europa.eu/en/news-events/news)
- [EMA Regulatory and Procedural Guidelines](https://www.ema.europa.eu/en/human-regulatory-overview/research-development/scientific-guidelines)
- [FDA Press Releases](https://www.fda.gov/news-events/fda-newsroom/press-announcements)

## Background
Built as part of a regulatory affairs portfolio ahead of an MSc in Process Validation and Regulatory Affairs (Technological University of the Shannon, 2026). Prior experience as Regulatory Affairs intern in Dabur International Ltd. and Quality Control intern in Vieco Pharmaceuticals
