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
     "label": "EMA News", "color": "#60A5FA", "glow": "rgba(96,165,250,0.18)", "bg": "rgba(96,165,250,0.1)"},
    {"url": "https://www.ema.europa.eu/en/regulatory-and-procedural-guideline.xml",
     "label": "EMA Guidelines", "color": "#FBBF24", "glow": "rgba(251,191,36,0.18)", "bg": "rgba(251,191,36,0.1)"},
    {"url": "https://www.fda.gov/about-fda/contact-fda/stay-informed/rss-feeds/press-releases/rss.xml",
     "label": "FDA", "color": "#F87171", "glow": "rgba(248,113,113,0.18)", "bg": "rgba(248,113,113,0.1)"},
    {"url": "https://mhrainspectorate.blog.gov.uk/feed/",
     "label": "MHRA", "color": "#34D399", "glow": "rgba(52,211,153,0.18)", "bg": "rgba(52,211,153,0.1)"},
    {"url": "https://www.tga.gov.au/feeds/article.xml",
     "label": "TGA", "color": "#C084FC", "glow": "rgba(192,132,252,0.18)", "bg": "rgba(192,132,252,0.1)"},
    {"url": "https://www.canada.ca/en/health-canada/services/drugs-health-products/drug-products/feed.html",
     "label": "Health Canada", "color": "#FB923C", "glow": "rgba(251,146,60,0.18)", "bg": "rgba(251,146,60,0.1)"},
    {"url": "https://www.imdrf.org/news-events/news.xml",
     "label": "IMDRF", "color": "#22D3EE", "glow": "rgba(34,211,238,0.18)", "bg": "rgba(34,211,238,0.1)"},
    {"url": "https://www.who.int/rss-feeds/news-english.xml",
     "label": "WHO", "color": "#38BDF8", "glow": "rgba(56,189,248,0.18)", "bg": "rgba(56,189,248,0.1)"},
]
 
cutoff = datetime.now(timezone.utc) - timedelta(days=30)
all_entries = []
 
for feed_info in FEEDS:
    try:
        feed = feedparser.parse(feed_info["url"])
        count = 0
        for entry in feed.entries:
            try:
                published_dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
                if published_dt >= cutoff:
                    all_entries.append({
                        "label": feed_info["label"],
                        "color": feed_info["color"],
                        "glow": feed_info["glow"],
                        "bg": feed_info["bg"],
                        "title": entry.title,
                        "link": entry.link,
                        "date": datetime(*entry.published_parsed[:6]).strftime("%d %b %Y"),
                        "date_sort": datetime(*entry.published_parsed[:6]).strftime("%Y-%m-%d"),
                        "summary": ""
                    })
                    count += 1
            except Exception:
                pass
        print(f"✓ {feed_info['label']}: {count} items")
    except Exception as e:
        print(f"✗ {feed_info['label']} failed: {e}")
 
all_entries.sort(key=lambda e: e["date_sort"], reverse=True)
print(f"\n✓ {len(all_entries)} total items — summarizing...")
 
for entry in all_entries:
    try:
        entry["summary"] = summarize_entry(entry["title"])
        time.sleep(2)
    except Exception as e:
        entry["summary"] = "Summary unavailable."
        print(f"Skipped: {e}")
 
print("✓ Building premium website...")
 
generated = datetime.now().strftime("%d %b %Y, %H:%M UTC")
entries_json = json.dumps(all_entries)
source_counts = {}
for e in all_entries:
    source_counts[e["label"]] = source_counts.get(e["label"], 0) + 1
 
featured = all_entries[0] if all_entries else None
 
# ── CSS ─────────────────────────────────────────────────────────────────
CSS = """
*{box-sizing:border-box;margin:0;padding:0}
html{scroll-behavior:smooth}
body{font-family:-apple-system,BlinkMacSystemFont,'Segoe UI',sans-serif;background:#080D1A;color:#EEF2FF;overflow-x:hidden}
 
/* NAV */
nav{position:fixed;top:0;left:0;right:0;z-index:300;height:58px;display:flex;align-items:center;background:rgba(8,13,26,0.85);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.06)}
.nav-i{max-width:1140px;width:100%;margin:0 auto;padding:0 32px;display:flex;align-items:center;justify-content:space-between}
.nav-logo{font-size:15px;font-weight:700;color:#EEF2FF;letter-spacing:-0.3px}
.nav-logo em{color:#C9A050;font-style:normal}
.nav-links{display:flex;gap:28px}
.nav-links a{color:#8A9BB5;font-size:13px;text-decoration:none;transition:color .2s}
.nav-links a:hover{color:#EEF2FF}
.nav-pill{background:rgba(201,160,80,0.12);border:1px solid rgba(201,160,80,0.25);color:#C9A050;font-size:11px;padding:5px 12px;border-radius:20px;display:flex;align-items:center;gap:6px;font-weight:600;letter-spacing:.5px}
.nav-dot{width:6px;height:6px;background:#C9A050;border-radius:50%;animation:blink 2s infinite}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.25}}
 
/* HERO */
.hero{min-height:100vh;display:flex;align-items:center;padding:100px 32px 80px;position:relative;overflow:hidden;background:#080D1A;background-image:radial-gradient(rgba(255,255,255,0.055) 1px,transparent 0);background-size:28px 28px}
.hero-orb-1{position:absolute;width:700px;height:700px;border-radius:50%;background:radial-gradient(circle,rgba(201,160,80,0.1) 0%,transparent 65%);top:-200px;right:-150px;animation:orb1 12s ease-in-out infinite;pointer-events:none}
.hero-orb-2{position:absolute;width:500px;height:500px;border-radius:50%;background:radial-gradient(circle,rgba(96,165,250,0.07) 0%,transparent 65%);bottom:-150px;left:-100px;animation:orb2 15s ease-in-out infinite;pointer-events:none}
.hero-orb-3{position:absolute;width:300px;height:300px;border-radius:50%;background:radial-gradient(circle,rgba(52,211,153,0.05) 0%,transparent 65%);top:40%;left:50%;animation:orb3 18s ease-in-out infinite;pointer-events:none}
@keyframes orb1{0%,100%{transform:translate(0,0)}50%{transform:translate(-50px,60px)}}
@keyframes orb2{0%,100%{transform:translate(0,0)}50%{transform:translate(60px,-40px)}}
@keyframes orb3{0%,100%{transform:translate(-50%,-50%)}50%{transform:translate(calc(-50% + 40px),calc(-50% + 30px))}}
.hero-i{max-width:1140px;width:100%;margin:0 auto;position:relative;z-index:1}
.hero-eye{display:inline-flex;align-items:center;gap:8px;background:rgba(201,160,80,0.1);border:1px solid rgba(201,160,80,0.22);color:#C9A050;font-size:11px;letter-spacing:2px;text-transform:uppercase;padding:7px 16px;border-radius:24px;margin-bottom:32px;font-weight:600}
.hero h1{font-size:clamp(40px,5.5vw,72px);font-weight:800;line-height:1.05;letter-spacing:-2.5px;margin-bottom:28px;max-width:820px;color:#EEF2FF}
.hero h1 .gold{background:linear-gradient(120deg,#C9A050 0%,#F0D47A 50%,#C9A050 100%);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text}
.hero-sub{font-size:18px;color:#8A9BB5;line-height:1.75;max-width:560px;margin-bottom:44px;font-weight:400}
.hero-ctas{display:flex;gap:14px;flex-wrap:wrap;margin-bottom:56px}
.btn-gold{background:linear-gradient(135deg,#C9A050,#D4AE60);color:#080D1A;padding:14px 30px;border-radius:10px;font-size:14px;font-weight:700;text-decoration:none;letter-spacing:.2px;transition:all .2s;box-shadow:0 4px 20px rgba(201,160,80,0.3)}
.btn-gold:hover{transform:translateY(-2px);box-shadow:0 8px 28px rgba(201,160,80,0.4)}
.btn-ghost{border:1px solid rgba(255,255,255,0.18);color:#EEF2FF;padding:14px 30px;border-radius:10px;font-size:14px;font-weight:500;text-decoration:none;transition:all .2s;backdrop-filter:blur(8px)}
.btn-ghost:hover{border-color:rgba(255,255,255,0.4);background:rgba(255,255,255,0.06)}
.agency-row{display:flex;flex-wrap:wrap;gap:10px;padding-top:40px;border-top:1px solid rgba(255,255,255,0.07)}
.agency-chip{display:flex;align-items:center;gap:7px;background:rgba(255,255,255,0.04);border:1px solid rgba(255,255,255,0.08);padding:7px 13px;border-radius:24px;font-size:12px;color:#8A9BB5;transition:all .2s}
.agency-chip:hover{border-color:rgba(255,255,255,0.18);color:#EEF2FF}
.agency-glow{width:8px;height:8px;border-radius:50%;flex-shrink:0}
 
/* SECTION BASE */
.sec{padding:88px 32px}
.sec-i{max-width:1140px;margin:0 auto}
.sec-eye{font-size:11px;letter-spacing:2px;text-transform:uppercase;color:#C9A050;font-weight:700;margin-bottom:14px}
.sec-h{font-size:clamp(28px,3vw,42px);font-weight:800;letter-spacing:-1px;line-height:1.15;margin-bottom:18px;color:#EEF2FF}
.sec-sub{font-size:16px;color:#8A9BB5;line-height:1.8;max-width:580px}
 
/* WHY */
.why{background:#0A101F}
.why-grid{display:grid;grid-template-columns:1fr 1fr;gap:72px;margin-top:56px;align-items:start}
.why-text{font-size:15px;color:#8A9BB5;line-height:1.9}
.why-text p+p{margin-top:18px}
.why-text strong{color:#EEF2FF;font-weight:600}
.why-right{display:flex;flex-direction:column;gap:14px}
.why-pull{background:rgba(201,160,80,0.06);border-left:3px solid #C9A050;padding:24px 28px;border-radius:0 12px 12px 0;margin-bottom:4px}
.why-pull p{font-size:16px;color:#EEF2FF;line-height:1.7;font-style:italic;font-weight:400}
.why-pull cite{display:block;margin-top:10px;font-size:12px;color:#4B5E7A;font-style:normal;letter-spacing:.5px}
.cred{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:12px;padding:18px 22px}
.cred-l{font-size:10px;text-transform:uppercase;letter-spacing:1.5px;color:#4B5E7A;margin-bottom:6px;font-weight:600}
.cred-v{font-size:14px;color:#EEF2FF;line-height:1.55;font-weight:500}
 
/* HOW */
.how{background:#060C18}
.steps{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:56px;position:relative}
.steps::before{content:'';position:absolute;top:32px;left:calc(16.66% + 20px);right:calc(16.66% + 20px);height:1px;background:repeating-linear-gradient(90deg,#C9A050 0,#C9A050 5px,transparent 5px,transparent 12px)}
.step{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.07);border-radius:16px;padding:30px 26px;transition:border-color .3s}
.step:hover{border-color:rgba(201,160,80,0.3)}
.step-n{width:48px;height:48px;background:linear-gradient(135deg,#C9A050,#D4AE60);border-radius:50%;display:flex;align-items:center;justify-content:center;font-size:18px;font-weight:800;color:#080D1A;margin-bottom:18px;position:relative;z-index:1;box-shadow:0 4px 16px rgba(201,160,80,0.35)}
.step h3{font-size:16px;font-weight:700;margin-bottom:10px;color:#EEF2FF}
.step p{font-size:13px;color:#8A9BB5;line-height:1.65}
.step-tags{display:flex;flex-wrap:wrap;gap:6px;margin-top:16px}
.step-tag{background:rgba(255,255,255,0.06);color:#8A9BB5;font-size:11px;padding:4px 9px;border-radius:5px}
 
/* BULLETIN */
.bul-hdr{background:linear-gradient(180deg,#0D1425 0%,#080D1A 100%);padding:36px 32px;border-bottom:1px solid rgba(255,255,255,0.06)}
.bul-hdr-i{max-width:1140px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:16px}
.bul-title{font-size:22px;font-weight:700;color:#EEF2FF;letter-spacing:-.5px}
.live{display:inline-flex;align-items:center;gap:6px;background:rgba(52,211,153,0.1);border:1px solid rgba(52,211,153,0.25);color:#34D399;font-size:10px;font-weight:700;letter-spacing:2px;padding:5px 12px;border-radius:20px;text-transform:uppercase}
.live-d{width:6px;height:6px;background:#34D399;border-radius:50%;animation:blink 1.5s infinite;box-shadow:0 0 6px #34D399}
.bul-ts{color:#4B5E7A;font-size:12px;font-family:monospace}
 
/* STATS */
.stats{background:#0A101F;border-bottom:1px solid rgba(255,255,255,0.06);padding:24px 32px}
.stats-i{max-width:1140px;margin:0 auto;display:flex;gap:0;flex-wrap:wrap}
.stat{padding:4px 32px;border-right:1px solid rgba(255,255,255,0.07);display:flex;flex-direction:column;gap:4px}
.stat:first-child{padding-left:0}
.stat:last-child{border-right:none}
.stat-n{font-size:28px;font-weight:800;line-height:1;letter-spacing:-1px;color:#EEF2FF}
.stat-l{font-size:11px;color:#4B5E7A;text-transform:uppercase;letter-spacing:.8px}
 
/* LEGEND */
.legend{background:#080D1A;border-bottom:1px solid rgba(255,255,255,0.06);padding:14px 32px}
.legend-i{max-width:1140px;margin:0 auto;display:flex;gap:16px;flex-wrap:wrap;align-items:center}
.leg-item{display:flex;align-items:center;gap:7px;font-size:12px;color:#6B7A99}
.leg-dot{width:8px;height:8px;border-radius:50%;flex-shrink:0}
.leg-ct{background:rgba(255,255,255,0.06);padding:1px 7px;border-radius:10px;font-size:10px;color:#4B5E7A}
 
/* CONTROLS */
.ctrl-wrap{position:sticky;top:58px;z-index:200;background:rgba(8,13,26,0.95);backdrop-filter:blur(20px);-webkit-backdrop-filter:blur(20px);border-bottom:1px solid rgba(255,255,255,0.07);padding:14px 32px}
.ctrl{max-width:1140px;margin:0 auto;display:flex;gap:10px;flex-wrap:wrap;align-items:center}
.srch-w{position:relative;flex:1;min-width:180px;max-width:300px}
.srch-ic{position:absolute;left:12px;top:50%;transform:translateY(-50%);color:#4B5E7A;pointer-events:none}
.srch{width:100%;padding:9px 12px 9px 36px;background:rgba(255,255,255,0.05);border:1px solid rgba(255,255,255,0.1);border-radius:8px;font-size:13px;color:#EEF2FF;outline:none;transition:all .2s}
.srch::placeholder{color:#4B5E7A}
.srch:focus{border-color:rgba(201,160,80,0.5);background:rgba(255,255,255,0.07);box-shadow:0 0 0 3px rgba(201,160,80,0.1)}
.filters{display:flex;gap:6px;flex-wrap:wrap}
.f-btn{padding:7px 13px;border-radius:7px;border:1px solid rgba(255,255,255,0.1);background:rgba(255,255,255,0.04);font-size:12px;cursor:pointer;color:#8A9BB5;font-weight:500;transition:all .2s;white-space:nowrap}
.f-btn:hover{border-color:rgba(255,255,255,0.2);color:#EEF2FF;background:rgba(255,255,255,0.07)}
.f-btn.active{background:var(--c,#C9A050);color:#080D1A;border-color:var(--c,#C9A050);box-shadow:0 0 16px var(--g,rgba(201,160,80,0.3));font-weight:700}
.f-ct{font-size:10px;opacity:.7;margin-left:2px}
 
/* RESULTS */
.res-info{max-width:1140px;margin:20px auto 0;padding:0 32px;font-size:13px;color:#4B5E7A}
 
/* FEATURED CARD */
.feat-wrap{max-width:1140px;margin:20px auto 0;padding:0 32px}
.feat{border-radius:18px;border:1px solid rgba(255,255,255,0.1);overflow:hidden;position:relative;transition:all .3s;cursor:default}
.feat:hover{border-color:rgba(255,255,255,0.18);transform:translateY(-2px)}
.feat-inner{padding:36px 40px;position:relative;z-index:1}
.feat-meta{display:flex;align-items:center;gap:12px;margin-bottom:18px;flex-wrap:wrap}
.feat-new{background:linear-gradient(135deg,#C9A050,#D4AE60);color:#080D1A;font-size:10px;font-weight:800;letter-spacing:2px;text-transform:uppercase;padding:5px 12px;border-radius:20px}
.c-badge{font-size:10px;font-weight:700;text-transform:uppercase;letter-spacing:.8px;padding:4px 10px;border-radius:6px}
.feat-date{font-size:12px;color:#4B5E7A;font-family:monospace}
.feat-title{font-size:clamp(20px,2.5vw,28px);font-weight:800;line-height:1.25;letter-spacing:-.5px;color:#EEF2FF;margin-bottom:16px;max-width:820px}
.feat-sum{font-size:15px;color:#8A9BB5;line-height:1.75;max-width:720px;margin-bottom:22px}
.feat-link{font-size:13px;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:6px;padding:10px 20px;border-radius:8px;border:1px solid;transition:all .2s}
.feat-link:hover{opacity:.85;transform:translateX(2px)}
 
/* GRID */
.grid{max-width:1140px;margin:16px auto 0;padding:0 32px 72px;display:grid;grid-template-columns:repeat(auto-fill,minmax(330px,1fr));gap:16px}
.card{background:rgba(255,255,255,0.03);border:1px solid rgba(255,255,255,0.08);border-radius:14px;overflow:hidden;display:flex;flex-direction:column;transition:all .25s;cursor:default}
.card:hover{border-color:var(--c,rgba(255,255,255,0.2));box-shadow:0 0 0 1px var(--c,transparent),0 16px 40px rgba(0,0,0,0.5),0 0 40px var(--g,transparent);transform:translateY(-3px)}
.card-stripe{height:3px}
.card-body{padding:20px;display:flex;flex-direction:column;gap:10px;flex:1}
.card-meta{display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:6px}
.card-date{font-size:11px;color:#4B5E7A;font-family:monospace}
.card-title{font-size:14px;font-weight:700;line-height:1.45;color:#EEF2FF}
.card-sum{font-size:13px;color:#8A9BB5;line-height:1.65;flex:1}
.card-lnk{font-size:12px;font-weight:600;text-decoration:none;display:inline-flex;align-items:center;gap:4px;margin-top:4px;opacity:.85;transition:opacity .2s}
.card-lnk:hover{opacity:1}
 
/* EMPTY */
.empty{grid-column:1/-1;text-align:center;padding:72px 32px;color:#4B5E7A}
.empty p{font-size:16px;margin-bottom:8px;color:#8A9BB5}
 
/* FOOTER */
footer{background:#050A15;border-top:1px solid rgba(255,255,255,0.05);padding:56px 32px 40px}
.ft-i{max-width:1140px;margin:0 auto;display:flex;justify-content:space-between;align-items:flex-start;flex-wrap:wrap;gap:32px}
.ft-name{font-size:16px;font-weight:700;color:#EEF2FF;margin-bottom:8px}
.ft-desc{font-size:13px;color:#4B5E7A;line-height:1.6;max-width:340px}
.ft-links{display:flex;gap:10px;flex-wrap:wrap}
.ft-lnk{display:flex;align-items:center;gap:7px;color:#8A9BB5;font-size:13px;text-decoration:none;padding:9px 16px;border:1px solid rgba(255,255,255,0.1);border-radius:9px;transition:all .2s;font-weight:500}
.ft-lnk:hover{color:#EEF2FF;border-color:rgba(255,255,255,0.25);background:rgba(255,255,255,0.04)}
.ft-bot{max-width:1140px;margin:32px auto 0;padding-top:24px;border-top:1px solid rgba(255,255,255,0.05);display:flex;justify-content:space-between;flex-wrap:wrap;gap:8px;color:#2E3D52;font-size:12px}
 
/* RESPONSIVE */
@media(max-width:900px){
  .why-grid,.steps{grid-template-columns:1fr}
  .steps::before{display:none}
  .hero h1{letter-spacing:-1.5px}
}
@media(max-width:600px){
  .nav-links,.nav-pill{display:none}
  .hero,.sec,.stats,.legend,.bul-hdr,.ctrl-wrap{padding-left:16px;padding-right:16px}
  .feat-wrap,.grid,.res-info{padding-left:16px;padding-right:16px}
  .feat-inner{padding:24px 22px}
  .grid{grid-template-columns:1fr}
  .stat{padding:4px 20px}
  .ft-i{flex-direction:column}
}
 
/* FADE IN */
@keyframes fadeUp{from{opacity:0;transform:translateY(16px)}to{opacity:1;transform:none}}
.card,.feat{animation:fadeUp .4s ease both}
"""
 
# ── JS ──────────────────────────────────────────────────────────────────
JS_DATA = f"const entries={entries_json};"
JS_LOGIC = r"""
let currentFilter='all';
const featWrap=document.getElementById('featWrap');
 
function renderGrid(data){
  const g=document.getElementById('grid');
  if(!data.length){g.innerHTML='<div class="empty"><p>No updates found</p><span>Try a different filter or search term.</span></div>';return;}
  g.innerHTML=data.map((e,i)=>`
    <div class="card" style="--c:${e.color};--g:${e.glow};animation-delay:${Math.min(i*0.05,0.4)}s">
      <div class="card-stripe" style="background:${e.color}"></div>
      <div class="card-body">
        <div class="card-meta">
          <span class="c-badge" style="background:${e.bg};color:${e.color}">${e.label}</span>
          <span class="card-date">${e.date}</span>
        </div>
        <div class="card-title">${e.title}</div>
        <div class="card-sum">${e.summary}</div>
        <a class="card-lnk" href="${e.link}" target="_blank" style="color:${e.color}">View source →</a>
      </div>
    </div>
  `).join('');
}
 
function filterCards(){
  const q=document.getElementById('srch').value.toLowerCase().trim();
  const isDefault=currentFilter==='all'&&!q;
  const info=document.getElementById('resInfo');
  if(isDefault){
    featWrap.style.display='block';
    renderGrid(entries.slice(1));
    info.textContent=entries.length+' updates across 8 agencies in the last 30 days';
  } else {
    featWrap.style.display='none';
    const f=entries.filter(e=>{
      const mf=currentFilter==='all'||e.label===currentFilter;
      const ms=!q||e.title.toLowerCase().includes(q)||e.summary.toLowerCase().includes(q)||e.label.toLowerCase().includes(q);
      return mf&&ms;
    });
    renderGrid(f);
    info.textContent=f.length+' update'+(f.length!==1?'s':'')+' shown';
  }
}
 
function setFilter(f,btn){
  currentFilter=f;
  document.querySelectorAll('.f-btn').forEach(b=>b.classList.remove('active'));
  btn.classList.add('active');
  filterCards();
}
 
filterCards();
"""
JS = JS_DATA + "\n" + JS_LOGIC
 
# ── LEGEND ──────────────────────────────────────────────────────────────
legend_parts = []
for fi in FEEDS:
    ct = source_counts.get(fi["label"], 0)
    if ct > 0:
        legend_parts.append(
            f'<span class="leg-item">'
            f'<span class="leg-dot" style="background:{fi["color"]};box-shadow:0 0 6px {fi["glow"]}"></span>'
            f'{fi["label"]}'
            f'<span class="leg-ct">{ct}</span>'
            f'</span>'
        )
LEGEND_HTML = "\n".join(legend_parts)
 
# ── FILTERS ─────────────────────────────────────────────────────────────
filter_parts = [
    f'<button class="f-btn active" style="--c:#C9A050;--g:rgba(201,160,80,0.2)" onclick="setFilter(\'all\',this)">All <span class="f-ct">{len(all_entries)}</span></button>'
]
for fi in FEEDS:
    ct = source_counts.get(fi["label"], 0)
    if ct > 0:
        label_js = fi["label"].replace("'", "\\'")
        filter_parts.append(
            f'<button class="f-btn" style="--c:{fi["color"]};--g:{fi["glow"]}" onclick="setFilter(\'{label_js}\',this)">'
            f'{fi["label"]} <span class="f-ct">{ct}</span></button>'
        )
FILTER_HTML = "\n".join(filter_parts)
 
# ── STATS ────────────────────────────────────────────────────────────────
STATS_HTML = f"""
<div class="stat"><div class="stat-n">{len(all_entries)}</div><div class="stat-l">Updates</div></div>
<div class="stat"><div class="stat-n">8</div><div class="stat-l">Agencies</div></div>
<div class="stat"><div class="stat-n">30</div><div class="stat-l">Day window</div></div>
<div class="stat"><div class="stat-n" style="color:#34D399">Daily</div><div class="stat-l">Auto-refresh</div></div>
"""
 
# ── FEATURED CARD ────────────────────────────────────────────────────────
if featured:
    feat_bg = f"linear-gradient(120deg, {featured['glow']} 0%, rgba(255,255,255,0.02) 55%)"
    feat_border_l = featured['color']
    FEAT_HTML = f"""
<div class="feat-wrap" id="featWrap">
  <div class="feat" style="background:{feat_bg};border-left:4px solid {feat_border_l}">
    <div class="feat-inner">
      <div class="feat-meta">
        <span class="feat-new">Latest Update</span>
        <span class="c-badge" style="background:{featured['bg']};color:{featured['color']}">{featured['label']}</span>
        <span class="feat-date">{featured['date']}</span>
      </div>
      <div class="feat-title">{featured['title']}</div>
      <div class="feat-sum">{featured['summary']}</div>
      <a href="{featured['link']}" target="_blank" class="feat-link" style="color:{featured['color']};border-color:{featured['color']};background:{featured['bg']}">Read full update →</a>
    </div>
  </div>
</div>
"""
else:
    FEAT_HTML = '<div id="featWrap" style="display:none"></div>'
 
# ── AGENCY CHIPS ─────────────────────────────────────────────────────────
chips = []
for fi in FEEDS:
    chips.append(
        f'<span class="agency-chip">'
        f'<span class="agency-glow" style="background:{fi["color"]};box-shadow:0 0 8px {fi["color"]}"></span>'
        f'{fi["label"]}'
        f'</span>'
    )
CHIPS_HTML = "\n".join(chips)
 
# ── FULL HTML ────────────────────────────────────────────────────────────
html = f"""<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>Sahil Subramaniam — Regulatory Intelligence</title>
<style>{CSS}</style>
</head>
<body>
 
<nav>
  <div class="nav-i">
    <div class="nav-logo">Sahil <em>Subramaniam</em></div>
    <div class="nav-links">
      <a href="#why">About</a>
      <a href="#how">How it works</a>
      <a href="#bulletin">Bulletin</a>
      <a href="https://www.linkedin.com/in/sahil-subramaniam-1007272b3" target="_blank">LinkedIn</a>
    </div>
    <div class="nav-pill"><div class="nav-dot"></div> Live · 8 Agencies</div>
  </div>
</nav>
 
<section class="hero" id="home">
  <div class="hero-orb-1"></div>
  <div class="hero-orb-2"></div>
  <div class="hero-orb-3"></div>
  <div class="hero-i">
    <div class="hero-eye"><div class="nav-dot"></div> Global Regulatory Intelligence</div>
    <h1>RA professionals deserve<br><span class="gold">better tools.</span></h1>
    <p class="hero-sub">AI is reshaping every industry. Regulatory Affairs should be no different. This tool monitors 8 global agencies daily — so you can focus on the work that actually matters.</p>
    <div class="hero-ctas">
      <a href="#bulletin" class="btn-gold">View Live Bulletin</a>
      <a href="#why" class="btn-ghost">Why I built this</a>
    </div>
    <div class="agency-row">
      {CHIPS_HTML}
    </div>
  </div>
</section>
 
<section class="sec why" id="why">
  <div class="sec-i">
    <div class="sec-eye">The Problem + The Person</div>
    <div class="sec-h">Where this came from</div>
    <div class="why-grid">
      <div class="why-text">
        <p>During my time as a Regulatory Affairs intern at <strong>Dabur International Ltd.</strong> in Dubai, one of my tasks was to manually visit health authority websites across multiple markets — checking for updates to herbal and health product regulations, one country at a time.</p>
        <p>It was tedious, time-consuming, and entirely manual. Every update had to be found, read, interpreted, and logged by hand. For a function as critical as regulatory affairs, it felt like an unnecessary drain on time that could be spent on actual strategy.</p>
        <p>That experience planted the seed. <strong>AI is ubiquitous now</strong> — it's reshaping finance, medicine, law. Regulatory Affairs, with its volume of documentation, multi-market complexity, and constant change, is exactly where it can make a real difference. Not to replace RA professionals, but to handle the tedious so they can focus on the holistic.</p>
        <p>This tool is a small proof of that idea — built as I prepare to begin my <strong>MSc in Process Validation and Regulatory Affairs</strong> at The Technological University of The Shannon, Moylish Campus, Limerick, Ireland.</p>
      </div>
      <div class="why-right">
        <div class="why-pull">
          <p>"RA professionals shouldn't be spending their day manually refreshing health authority websites. That's exactly the kind of task AI should be handling."</p>
          <cite>— The thinking behind this project</cite>
        </div>
        <div class="cred">
          <div class="cred-l">Background</div>
          <div class="cred-v">RA Intern — Dabur International Ltd., Dubai<br>QC Intern — Vieco Pharmaceuticals, Dubai</div>
        </div>
        <div class="cred">
          <div class="cred-l">Currently</div>
          <div class="cred-v">Prospective MSc student — Process Validation &amp; Regulatory Affairs<br>The Technological University of The Shannon, Moylish Campus, Limerick, Ireland</div>
        </div>
      </div>
    </div>
  </div>
</section>
 
<section class="sec how" id="how">
  <div class="sec-i">
    <div class="sec-eye">Under the Hood</div>
    <div class="sec-h">How it works</div>
    <p class="sec-sub">Three steps, fully automated, running every morning without any manual input.</p>
    <div class="steps">
      <div class="step">
        <div class="step-n">1</div>
        <h3>Fetch</h3>
        <p>Every day at 7am UTC, the tool pulls live updates directly from 8 official regulatory RSS feeds — no scraping, no third parties, no manual work.</p>
        <div class="step-tags">
          <span class="step-tag">EMA</span><span class="step-tag">FDA</span><span class="step-tag">MHRA</span><span class="step-tag">TGA</span><span class="step-tag">Health Canada</span><span class="step-tag">IMDRF</span><span class="step-tag">WHO</span>
        </div>
      </div>
      <div class="step">
        <div class="step-n">2</div>
        <h3>Summarize</h3>
        <p>Each update is passed through an AI model that generates a plain-language one-sentence summary — what changed and why it matters for RA teams.</p>
        <div class="step-tags">
          <span class="step-tag">Groq API</span><span class="step-tag">Llama 3.1</span><span class="step-tag">30-day filter</span>
        </div>
      </div>
      <div class="step">
        <div class="step-n">3</div>
        <h3>Publish</h3>
        <p>The bulletin is automatically rebuilt and deployed as a live searchable webpage — always current, always free, zero manual steps.</p>
        <div class="step-tags">
          <span class="step-tag">GitHub Actions</span><span class="step-tag">GitHub Pages</span><span class="step-tag">Zero cost</span>
        </div>
      </div>
    </div>
  </div>
</section>
 
<div id="bulletin">
 
  <div class="bul-hdr">
    <div class="bul-hdr-i">
      <div style="display:flex;align-items:center;gap:14px">
        <div class="bul-title">Global Regulatory Bulletin</div>
        <div class="live"><div class="live-d"></div> Live</div>
      </div>
      <div class="bul-ts">Updated: {generated}</div>
    </div>
  </div>
 
  <div class="stats">
    <div class="stats-i">{STATS_HTML}</div>
  </div>
 
  <div class="legend">
    <div class="legend-i">{LEGEND_HTML}</div>
  </div>
 
  <div class="ctrl-wrap">
    <div class="ctrl">
      <div class="srch-w">
        <svg class="srch-ic" width="14" height="14" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24"><circle cx="11" cy="11" r="8"/><path d="m21 21-4.35-4.35"/></svg>
        <input class="srch" id="srch" type="text" placeholder="Search across all agencies..." oninput="filterCards()">
      </div>
      <div class="filters">{FILTER_HTML}</div>
    </div>
  </div>
 
  <div class="res-info" id="resInfo">{len(all_entries)} updates across 8 agencies in the last 30 days</div>
 
  {FEAT_HTML}
 
  <div class="grid" id="grid"></div>
 
</div>
 
<footer>
  <div class="ft-i">
    <div>
      <div class="ft-name">Sahil Subramaniam</div>
      <div class="ft-desc">Regulatory Affairs professional-in-training. Building AI tools to make RA smarter, faster, and less tedious — one feed at a time.</div>
    </div>
    <div class="ft-links">
      <a href="https://www.linkedin.com/in/sahil-subramaniam-1007272b3" target="_blank" class="ft-lnk">
        <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M20.447 20.452h-3.554v-5.569c0-1.328-.027-3.037-1.852-3.037-1.853 0-2.136 1.445-2.136 2.939v5.667H9.351V9h3.414v1.561h.046c.477-.9 1.637-1.85 3.37-1.85 3.601 0 4.267 2.37 4.267 5.455v6.286zM5.337 7.433a2.062 2.062 0 01-2.063-2.065 2.064 2.064 0 112.063 2.065zm1.782 13.019H3.555V9h3.564v11.452zM22.225 0H1.771C.792 0 0 .774 0 1.729v20.542C0 23.227.792 24 1.771 24h20.451C23.2 24 24 23.227 24 22.271V1.729C24 .774 23.2 0 22.222 0h.003z"/></svg>
        LinkedIn
      </a>
      <a href="https://github.com/sahils0305/EMA-FDA---Regulatory-Bulletin" target="_blank" class="ft-lnk">
        <svg width="14" height="14" fill="currentColor" viewBox="0 0 24 24"><path d="M12 0C5.374 0 0 5.373 0 12c0 5.302 3.438 9.8 8.207 11.387.599.111.793-.261.793-.577v-2.234c-3.338.726-4.033-1.416-4.033-1.416-.546-1.387-1.333-1.756-1.333-1.756-1.089-.745.083-.729.083-.729 1.205.084 1.839 1.237 1.839 1.237 1.07 1.834 2.807 1.304 3.492.997.107-.775.418-1.305.762-1.604-2.665-.305-5.467-1.334-5.467-5.931 0-1.311.469-2.381 1.236-3.221-.124-.303-.535-1.524.117-3.176 0 0 1.008-.322 3.301 1.23A11.509 11.509 0 0112 5.803c1.02.005 2.047.138 3.006.404 2.291-1.552 3.297-1.23 3.297-1.23.653 1.653.242 2.874.118 3.176.77.84 1.235 1.911 1.235 3.221 0 4.609-2.807 5.624-5.479 5.921.43.372.823 1.102.823 2.222v3.293c0 .319.192.694.801.576C20.566 21.797 24 17.3 24 12c0-6.627-5.373-12-12-12z"/></svg>
        GitHub
      </a>
    </div>
  </div>
  <div class="ft-bot">
    <span>Always verify against official sources before regulatory use.</span>
    <span>Auto-updates daily via GitHub Actions · Built with Groq AI + Python</span>
  </div>
</footer>
 
<script>{JS}</script>
</body>
</html>"""
 
with open("index.html", "w", encoding="utf-8") as f:
    f.write(html)
 
print(f"\n✓ Premium website saved — {len(all_entries)} entries across {len(FEEDS)} agencies")
 
