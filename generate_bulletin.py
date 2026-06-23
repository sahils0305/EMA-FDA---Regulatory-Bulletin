import feedparser
import time
from datetime import datetime, timedelta, timezone
from groq import Groq
import os

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
     "label": "EMA — News & Press", "color": "#44608A"},
    {"url": "https://www.ema.europa.eu/en/regulatory-and-procedural-guideline.xml",
     "label": "EMA — Guidelines", "color": "#B08D3F"},
    {"url": "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
     "label": "FDA — Press Releases", "color": "#9B2C2C"},
]

cutoff = datetime.now(timezone.utc) - timedelta(days=30)
all_entries = []

for feed_info in FEEDS:
    feed = feedparser.parse(feed_info["url"])
    for entry in feed.entries:
        try:
            published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
            if published_dt >= cutoff:
                entry["source_label"] = feed_info["label"]
                entry["source_color"] = feed_info["color"]
                all_entries.append(entry)
        except Exception:
            pass

all_entries.sort(key=lambda e: e.published_parsed, reverse=True)
print(f"✓ {len(all_entries)} items found — summarizing...")

for entry in all_entries:
    try:
        entry["ai_summary"] = summarize_entry(entry.title, entry.get("summary", ""))
        time.sleep(2)
    except Exception as e:
        entry["ai_summary"] = "Summary unavailable."
        print(f"Skipped: {e}")

print("✓ Summaries done — building HTML...")

generated = datetime.now().strftime("%d %b %Y, %H:%M UTC")

html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>EMA + FDA Regulatory Intelligence Bulletin</title>
</head>
<body style="margin:0;padding:20px;background:#ECEEF1;">
<div style="font-family:Georgia,serif;background:#F5F6F8;color:#1C1F26;max-width:720px;margin:0 auto;border:1px solid #e0e0e0;border-radius:4px;overflow:hidden;">
  <div style="background:#14213D;padding:28px 36px;">
    <p style="color:#B08D3F;font-family:monospace;font-size:11px;letter-spacing:2px;text-transform:uppercase;margin:0 0 6px 0;">Regulatory Intelligence Dashboard</p>
    <h1 style="color:#F5F6F8;margin:0;font-size:26px;">EMA + FDA Bulletin</h1>
    <p style="color:#F5F6F899;font-family:monospace;font-size:11px;margin:8px 0 0 0;">Generated: {generated} | {len(all_entries)} updates in last 30 days</p>
  </div>
  <div style="height:3px;background:#B08D3F;"></div>
  <div style="padding:16px 36px;display:flex;gap:16px;flex-wrap:wrap;border-bottom:1px solid #1C1F261A;">
    <span style="font-family:monospace;font-size:11px;color:#44608A;">● EMA News & Press</span>
    <span style="font-family:monospace;font-size:11px;color:#B08D3F;">● EMA Guidelines</span>
    <span style="font-family:monospace;font-size:11px;color:#9B2C2C;">● FDA Press Releases</span>
  </div>
  <div style="padding:0 36px;">
"""

for i, entry in enumerate(all_entries):
    color = entry["source_color"]
    label = entry["source_label"]
    date_str = datetime(*entry.published_parsed[:6]).strftime("%d %b %Y")
    border = "1px solid #1C1F261A" if i < len(all_entries)-1 else "none"
    html += f"""
    <div style="padding:20px 0;border-bottom:{border};">
      <div style="margin-bottom:6px;">
        <span style="background:{color}18;color:{color};font-family:monospace;font-size:10px;text-transform:uppercase;padding:3px 8px;border-radius:3px;letter-spacing:1px;">{label}</span>
        <span style="color:#1C1F2666;font-family:monospace;font-size:11px;margin-left:10px;">{date_str}</span>
      </div>
      <h2 style="font-size:17px;margin:4px 0 6px 0;line-height:1.4;">{entry['title']}</h2>
      <p style="font-size:14px;margin:0 0 8px 0;color:#1C1F26CC;line-height:1.6;">{entry['ai_summary']}</p>
      <a href="{entry['link']}" target="_blank" style="color:#14213D;font-family:monospace;font-size:11px;text-decoration:none;border-bottom:1px solid #14213D99;">View source →</a>
    </div>
    """

html += """
  </div>
  <div style="background:#14213D;color:#F5F6F899;text-align:center;padding:14px;font-family:monospace;font-size:11px;">
    Built with live EMA + FDA RSS feeds + Groq AI — verify against official sources before regulatory use.
  </div>
</div>
</body>
</html>"""

with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)

print("✓ index.html saved successfully!")
