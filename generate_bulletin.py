import feedparser
import time
import json
import os
from datetime import datetime, timedelta, timezone
from groq import Groq

client = Groq(api_key=os.environ.get('GROQ_API_KEY'))

def summarize_entry(title, description=""):
    prompt = f"""You are a regulatory affairs professional. In one clear sentence, explain what changed and why it matters for RA teams.

Title: {title}
Description: {description}

One sentence summary:"""
    response = client.chat.completions.create(
        model="llama-3.1-8b-instant",
        messages=[{"role": "user", "content": prompt}],
        max_tokens=100
    )
    return response.choices[0].message.content.strip()

FEEDS = [
    {"url": "https://www.ema.europa.eu/en/news.xml",
     "label": "EMA News & Press", "color": "#2E5EA8", "bg": "#EBF0FA"},
    {"url": "https://www.ema.europa.eu/en/regulatory-and-procedural-guideline.xml",
     "label": "EMA Guidelines", "color": "#8B6914", "bg": "#FBF5E6"},
    {"url": "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
     "label": "FDA Press Releases", "color": "#8B1A1A", "bg": "#FAEBEB"},
]

cutoff = datetime.now(timezone.utc) - timedelta(days=30)
all_entries = []

for feed_info in FEEDS:
    feed = feedparser.parse(feed_info["url"])
    for entry in feed.entries:
        try:
            published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            if published_dt >= cutoff:
                all_entries.append({
                    "label": feed_info["label"],
                    "color": feed_info["color"],
                    "bg": feed_info["bg"],
                    "title": entry.title,
                    "link": entry.link,
                    "date": datetime(*entry.published_parsed[:6]).strftime("%d %b %Y"),
                    "summary": ""
                })
        except Exception:
            pass

all_entries.sort(key=lambda e: e["date"], reverse=True)
print(f"✓ {len(all_entries)} items found — summarizing...")

for entry in all_entries:
    try:
        entry["summary"] = summarize_entry(entry["title"])
        time.sleep(2)
    except Exception as e:
        entry["summary"] = "Summary unavailable."
        print(f"Skipped: {e}")

print("✓ Building dashboard...")

generated = datetime.now().strftime("%d %b %Y, %H:%M UTC")
entries_json = json.dumps(all_entries)

ema_news_count = sum(1 for e in all_entries if e["label"] == "EMA News & Press")
ema_guide_count = sum(1 for e in all_entries if e["label"] == "EMA Guidelines")
fda_count = sum(1 for e in all_entries if e["label"] == "FDA Press Releases")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EMA + FDA Regulatory Intelligence Dashboard</title>
<style>
  * {{ box-sizing: border-box; margin: 0; padding: 0; }}
  body {{ font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif; background: #F0F2F5; color: #1A1D27; }}

  /* HEADER */
  .header {{ background: #0B1929; padding: 0 32px; position: sticky; top: 0; z-index: 100; box-shadow: 0 2px 12px rgba(0,0,0,0.3); }}
  .header-inner {{ max-width: 1100px; margin: 0 auto; display: flex; align-items: center; justify-content: space-between; height: 64px; }}
  .header-left {{ display: flex; align-items: center; gap: 12px; }}
  .live-badge {{ background: #16A34A; color: white; font-size: 10px; font-weight: 700; letter-spacing: 1.5px; padding: 3px 8px; border-radius: 20px; text-transform: uppercase; display: flex; align-items: center; gap: 5px; }}
  .live-dot {{ width: 6px; height: 6px; background: white; border-radius: 50%; animation: pulse 1.5s infinite; }}
  @keyframes pulse {{ 0%, 100% {{ opacity: 1; }} 50% {{ opacity: 0.3; }} }}
  .header-title {{ color: white; font-size: 17px; font-weight: 600; letter-spacing: -0.3px; }}
  .header-sub {{ color: #C9A050; font-size: 11px; letter-spacing: 1px; text-transform: uppercase; margin-top: 1px; }}
  .header-right {{ color: #6B7A99; font-size: 12px; }}

  /* STATS BAR */
  .stats-bar {{ background: white; border-bottom: 1px solid #E5E7EB; }}
  .stats-inner {{ max-width: 1100px; margin: 0 auto; padding: 16px 32px; display: flex; gap: 32px; align-items: center; flex-wrap: wrap; }}
  .stat {{ display: flex; flex-direction: column; gap: 2px; }}
  .stat-num {{ font-size: 24px; font-weight: 700; line-height: 1; }}
  .stat-label {{ font-size: 11px; color: #6B7280; text-transform: uppercase; letter-spacing: 0.5px; }}
  .stat-divider {{ width: 1px; height: 36px; background: #E5E7EB; }}

  /* CONTROLS */
  .controls {{ max-width: 1100px; margin: 24px auto 0; padding: 0 32px; display: flex; gap: 12px; flex-wrap: wrap; align-items: center; }}
  .search-wrap {{ position: relative; flex: 1; min-width: 200px; }}
  .search-icon {{ position: absolute; left: 12px; top: 50%; transform: translateY(-50%); color: #9CA3AF; }}
  .search-input {{ width: 100%; padding: 10px 12px 10px 36px; border: 1px solid #E5E7EB; border-radius: 8px; font-size: 14px; background: white; outline: none; transition: border-color 0.2s; }}
  .search-input:focus {{ border-color: #2E5EA8; box-shadow: 0 0 0 3px rgba(46,94,168,0.1); }}
  .filter-btn {{ padding: 9px 16px; border-radius: 8px; border: 1px solid #E5E7EB; background: white; font-size: 13px; cursor: pointer; transition: all 0.15s; color: #374151; font-weight: 500; }}
  .filter-btn:hover {{ border-color: #9CA3AF; }}
  .filter-btn.active {{ background: #0B1929; color: white; border-color: #0B1929; }}

  /* RESULTS COUNT */
  .results-info {{ max-width: 1100px; margin: 16px auto 0; padding: 0 32px; font-size: 13px; color: #6B7280; }}

  /* GRID */
  .grid {{ max-width: 1100px; margin: 16px auto 40px; padding: 0 32px; display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 16px; }}

  /* CARD */
  .card {{ background: white; border-radius: 12px; border: 1px solid #E5E7EB; overflow: hidden; transition: box-shadow 0.2s, transform 0.2s; display: flex; flex-direction: column; }}
  .card:hover {{ box-shadow: 0 4px 20px rgba(0,0,0,0.08); transform: translateY(-2px); }}
  .card-top {{ height: 4px; }}
  .card-body {{ padding: 20px; flex: 1; display: flex; flex-direction: column; gap: 10px; }}
  .card-meta {{ display: flex; align-items: center; justify-content: space-between; }}
  .card-badge {{ font-size: 10px; font-weight: 600; text-transform: uppercase; letter-spacing: 0.8px; padding: 3px 8px; border-radius: 4px; }}
  .card-date {{ font-size: 12px; color: #9CA3AF; }}
  .card-title {{ font-size: 15px; font-weight: 600; line-height: 1.4; color: #111827; }}
  .card-summary {{ font-size: 13px; color: #4B5563; line-height: 1.6; flex: 1; }}
  .card-link {{ font-size: 12px; color: #2E5EA8; text-decoration: none; font-weight: 500; display: inline-flex; align-items: center; gap: 4px; margin-top: 4px; }}
  .card-link:hover {{ text-decoration: underline; }}

  /* EMPTY STATE */
  .empty {{ max-width: 1100px; margin: 60px auto; padding: 0 32px; text-align: center; color: #9CA3AF; }}

  /* FOOTER */
  .footer {{ background: #0B1929; color: #4B5E7A; text-align: center; padding: 20px; font-size: 12px; margin-top: auto; }}
  .footer a {{ color: #C9A050; text-decoration: none; }}

  @media (max-width: 600px) {{
    .header-inner, .stats-inner, .controls, .grid, .results-info {{ padding-left: 16px; padding-right: 16px; }}
    .grid {{ grid-template-columns: 1fr; }}
    .stat-divider {{ display: none; }}
  }}
</style>
</head>
<body>

<header class="header">
  <div class="header-inner">
    <div class="header-left">
      <div>
        <div class="header-sub">Regulatory Intelligence</div>
        <div class="header-title">EMA + FDA Bulletin</div>
      </div>
      <div class="live-badge"><div class="live-dot"></div> Live</div>
    </div>
    <div class="header-right">Updated: {generated}</div>
  </div>
</header>

<div class="stats-bar">
  <div class="stats-inner">
    <div class="stat">
      <div class="stat-num" style="color:#1A1D27">{len(all_entries)}</div>
      <div class="stat-label">Total Updates</div>
    </div>
    <div class="stat-divider"></div>
    <div class="stat">
      <div class="stat-num" style="color:#2E5EA8">{ema_news_count}</div>
      <div class="stat-label">EMA News</div>
    </div>
    <div class="stat-divider"></div>
    <div class="stat">
      <div class="stat-num" style="color:#8B6914">{ema_guide_count}</div>
      <div class="stat-label">EMA Guidelines</div>
    </div>
    <div class="stat-divider"></div>
    <div class="stat">
      <div class="stat-num" style="color:#8B1A1A">{fda_count}</div>
      <div class="stat-label">FDA Releases</div>
    </div>
    <div class="stat-divider"></div>
    <div class="stat">
      <div class="stat-num" style="color:#6B7280">30</div>
      <div class="stat-label">Day Window</div>
    </div>
  </div>
</div>

<div class="controls">
  <div class="search-wrap">
    <svg class="search-icon" width="16" height="16" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
    <input class="search-input" type="text" placeholder="Search updates..." id="searchInput" oninput="filterCards()">
  </div>
  <button class="filter-btn active" onclick="setFilter('all', this)">All</button>
  <button class="filter-btn" onclick="setFilter('EMA News & Press', this)" style="border-left: 3px solid #2E5EA8">EMA News</button>
  <button class="filter-btn" onclick="setFilter('EMA Guidelines', this)" style="border-left: 3px solid #8B6914">Guidelines</button>
  <button class="filter-btn" onclick="setFilter('FDA Press Releases', this)" style="border-left: 3px solid #8B1A1A">FDA</button>
</div>

<div class="results-info" id="resultsInfo">{len(all_entries)} updates in the last 30 days</div>

<div class="grid" id="grid"></div>

<footer class="footer">
  Built with live EMA + FDA RSS feeds + Groq AI &nbsp;·&nbsp; Auto-updates daily via GitHub Actions &nbsp;·&nbsp;
  <a href="https://github.com/sahils0305/EMA-FDA---Regulatory-Bulletin" target="_blank">View on GitHub</a>
  &nbsp;·&nbsp; Always verify against official sources before regulatory use.
</footer>

<script>
const entries = {entries_json};
let currentFilter = 'all';

function renderCards(data) {{
  const grid = document.getElementById('grid');
  document.getElementById('resultsInfo').textContent = data.length + ' update' + (data.length !== 1 ? 's' : '') + ' shown';
  if (data.length === 0) {{
    grid.innerHTML = '<div class="empty" style="grid-column:1/-1"><p style="font-size:18px;margin-bottom:8px">No updates found</p><p>Try adjusting your search or filter.</p></div>';
    return;
  }}
  grid.innerHTML = data.map(e => `
    <div class="card" data-label="${{e.label}}">
      <div class="card-top" style="background:${{e.color}}"></div>
      <div class="card-body">
        <div class="card-meta">
          <span class="card-badge" style="background:${{e.bg}};color:${{e.color}}">${{e.label}}</span>
          <span class="card-date">${{e.date}}</span>
        </div>
        <div class="card-title">${{e.title}}</div>
        <div class="card-summary">${{e.summary}}</div>
        <a class="card-link" href="${{e.link}}" target="_blank">View source →</a>
      </div>
    </div>
  `).join('');
}}

function filterCards() {{
  const q = document.getElementById('searchInput').value.toLowerCase();
  const filtered = entries.filter(e => {{
    const matchFilter = currentFilter === 'all' || e.label === currentFilter;
    const matchSearch = !q || e.title.toLowerCase().includes(q) || e.summary.toLowerCase().includes(q);
    return matchFilter && matchSearch;
  }});
  renderCards(filtered);
}}

function setFilter(filter, btn) {{
  currentFilter = filter;
  document.querySelectorAll('.filter-btn').forEach(b => b.classList.remove('active'));
  btn.classList.add('active');
  filterCards();
}}

renderCards(entries);
</script>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✓ Dashboard saved successfully!")
