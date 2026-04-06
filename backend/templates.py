# templates.py — UI components, CSS, and HTML helpers
# Each function returns a self-contained HTML string.
# main.py imports these and assembles the final page.

CSS = '''
:root{
  --ink:#0d0d0d;--ink2:#1a1a1a;
  --paper:#f5f0e8;--paper2:#ede8de;--paper3:#e4ddd0;
  --rule:rgba(13,13,13,.12);--rule2:rgba(13,13,13,.05);
  --accent:#c8372d;--accent2:#1d4ed8;--accent3:#047857;--accent4:#7c3aed;--accent5:#b45309;
  --mono:"IBM Plex Mono",monospace;
  --serif:"DM Serif Display",serif;
  --sans:"DM Sans",sans-serif;
  --syne:"Syne",sans-serif;
}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{
  background:var(--paper);color:var(--ink);
  font-family:var(--sans);font-size:15px;line-height:1.6;
  min-height:100vh;
  background-image:url("data:image/svg+xml,%3Csvg xmlns='http://www.w3.org/2000/svg' width='300' height='300'%3E%3Cfilter id='n'%3E%3CfeTurbulence type='fractalNoise' baseFrequency='0.9' numOctaves='4' stitchTiles='stitch'/%3E%3C/filter%3E%3Crect width='300' height='300' filter='url(%23n)' opacity='0.03'/%3E%3C/svg%3E");
}
.ticker-strip{background:var(--ink);color:var(--paper);display:flex;align-items:center;height:32px;overflow:hidden;position:sticky;top:0;z-index:1000;}
.ticker-kicker{flex-shrink:0;font-family:var(--mono);font-size:9px;font-weight:600;letter-spacing:3px;padding:0 16px;border-right:1px solid rgba(255,255,255,.1);height:100%;display:flex;align-items:center;background:var(--accent);color:#fff;white-space:nowrap;}
.ticker-scroll{flex:1;overflow:hidden;position:relative;}
.ticker-scroll::before,.ticker-scroll::after{content:"";position:absolute;top:0;bottom:0;width:48px;z-index:2;pointer-events:none;}
.ticker-scroll::before{left:0;background:linear-gradient(90deg,var(--ink),transparent);}
.ticker-scroll::after{right:0;background:linear-gradient(270deg,var(--ink),transparent);}
.ticker-track{display:inline-flex;white-space:nowrap;font-family:var(--mono);font-size:10px;letter-spacing:.5px;color:rgba(245,240,232,.55);animation:scroll-ticker 65s linear infinite;padding-left:48px;gap:0;}
@keyframes scroll-ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
.masthead{background:var(--paper);border-bottom:3px solid var(--ink);}
.masthead-inner{max-width:1320px;margin:0 auto;padding:24px 40px 18px;display:grid;grid-template-columns:1fr auto 1fr;align-items:end;gap:20px;}
.masthead-left,.masthead-right{font-family:var(--mono);font-size:10px;letter-spacing:2px;color:rgba(13,13,13,.38);}
.masthead-right{text-align:right;display:flex;flex-direction:column;align-items:flex-end;gap:6px;}
.pub-name{font-family:var(--serif);font-size:clamp(38px,5.5vw,70px);line-height:1;letter-spacing:-2px;text-align:center;color:var(--ink);}
.pub-sub{font-family:var(--mono);font-size:9px;letter-spacing:5px;text-align:center;color:rgba(13,13,13,.38);margin-top:8px;}
.live-indicator{display:flex;align-items:center;gap:7px;font-family:var(--mono);font-size:9px;letter-spacing:3px;color:var(--accent);font-weight:600;}
.live-pulse{width:7px;height:7px;border-radius:50%;background:var(--accent);animation:pulse-live 1.4s ease-in-out infinite;box-shadow:0 0 8px var(--accent);}
@keyframes pulse-live{0%,100%{opacity:1;transform:scale(1)}50%{opacity:.3;transform:scale(.75)}}
.live-time{font-family:var(--mono);font-size:12px;color:var(--ink);font-weight:500;letter-spacing:1px;}
.stats-rail{background:var(--ink);overflow-x:auto;scrollbar-width:none;border-bottom:1px solid rgba(255,255,255,.04);}
.stats-rail::-webkit-scrollbar{display:none}
.stats-inner{max-width:1320px;margin:0 auto;display:flex;padding:0 40px;}
.stat-brick{flex:1;min-width:150px;padding:14px 20px;border-right:1px solid rgba(255,255,255,.05);transition:background .2s;cursor:default;}
.stat-brick:last-child{border-right:none}.stat-brick:hover{background:rgba(255,255,255,.04)}
.stat-num{font-family:var(--syne);font-size:24px;font-weight:800;line-height:1;color:#fff;letter-spacing:-1px;}
.stat-lbl{font-size:9px;color:rgba(245,240,232,.38);margin-top:4px;letter-spacing:.3px;font-family:var(--mono);line-height:1.3;}
.stat-delta{font-size:9px;font-family:var(--mono);margin-top:5px;letter-spacing:.5px;}
.trend-up{color:#34d399}.trend-neutral{color:rgba(245,240,232,.28)}
.section-nav{position:sticky;top:32px;z-index:900;background:var(--paper2);border-bottom:2px solid var(--ink);}
.nav-inner{max-width:1320px;margin:0 auto;padding:0 40px;display:flex;overflow-x:auto;scrollbar-width:none;}
.nav-inner::-webkit-scrollbar{display:none}
.nav-tab{flex-shrink:0;background:none;border:none;font-family:var(--syne);font-size:10px;font-weight:800;letter-spacing:2.5px;text-transform:uppercase;color:rgba(13,13,13,.38);padding:13px 22px;cursor:pointer;transition:all .2s;border-bottom:3px solid transparent;margin-bottom:-2px;}
.nav-tab:hover{color:var(--ink);background:rgba(13,13,13,.03)}
.nav-tab.active{color:var(--ink);border-bottom-color:var(--accent);background:var(--paper);}
.main-wrap{max-width:1320px;margin:0 auto;padding:0 40px 80px;}
.tab-section{display:none}.tab-section.active{display:block}
.section-heading{padding:32px 0 0;border-bottom:2px solid var(--ink);margin-bottom:0;display:flex;align-items:baseline;justify-content:space-between;}
.sec-title{font-family:var(--syne);font-size:10px;font-weight:800;letter-spacing:4px;text-transform:uppercase;padding-bottom:10px;}
.sec-count{font-family:var(--mono);font-size:10px;color:rgba(13,13,13,.35);padding-bottom:10px;}
.editorial-grid{display:grid;grid-template-columns:1fr 340px;gap:0;border-bottom:1px solid var(--rule);}
.editorial-main{padding:28px 28px 28px 0;border-right:1px solid var(--rule);}
.editorial-sidebar{padding:28px 0 28px 28px;}
.card-lead{cursor:pointer;transition:all .25s;padding:20px;border:1px solid transparent;position:relative;opacity:0;transform:translateY(14px);}
.card-lead.visible{opacity:1;transform:none;transition:opacity .5s ease,transform .5s ease;}
.card-lead::before{content:"";position:absolute;left:0;top:0;bottom:0;width:3px;background:transparent;transition:background .2s;border-radius:0;}
.card-lead:hover::before{background:var(--accent)}
.card-lead:hover{background:rgba(13,13,13,.018)}
.card-lead:hover .card-lead-title{color:var(--accent)}
.card-lead-kicker{display:flex;align-items:center;gap:10px;margin-bottom:14px;}
.card-lead-title{font-family:var(--serif);font-size:26px;line-height:1.22;margin-bottom:12px;transition:color .2s;letter-spacing:-.3px;}
.card-lead-deck{font-size:14px;color:rgba(13,13,13,.58);line-height:1.7;margin-bottom:16px;font-style:italic;}
.card-meta{display:flex;gap:12px;font-family:var(--mono);font-size:10px;color:rgba(13,13,13,.4);letter-spacing:.3px;margin-bottom:12px;}
.byline{color:var(--ink);font-weight:600;}
.card-tags{display:flex;flex-wrap:wrap;gap:6px;}
.card-compact{cursor:pointer;display:flex;gap:14px;align-items:flex-start;padding:18px 0;border-bottom:1px solid var(--rule);transition:all .2s;opacity:0;transform:translateX(8px);}
.card-compact.visible{opacity:1;transform:none;transition:opacity .48s ease,transform .48s ease;}
.card-compact:last-child{border-bottom:none}
.card-compact:hover .card-compact-title{color:var(--accent)}
.card-num{font-family:var(--syne);font-size:28px;font-weight:800;line-height:1;color:rgba(13,13,13,.08);flex-shrink:0;width:36px;text-align:right;padding-top:4px;}
.card-compact-body{flex:1}
.card-compact-title{font-family:var(--serif);font-size:15px;line-height:1.4;margin:5px 0 7px;transition:color .2s;}
.card-compact-meta{font-family:var(--mono);font-size:9px;color:rgba(13,13,13,.32);letter-spacing:.3px;}
.tab-badge{font-family:var(--mono);font-size:8px;font-weight:600;letter-spacing:1.5px;padding:3px 7px;border-radius:1px;text-transform:uppercase;display:inline-block;}
.tab-openai{background:rgba(16,163,127,.1);color:#0a7a60;border:1px solid rgba(16,163,127,.18)}
.tab-claude{background:rgba(200,55,45,.09);color:#b03028;border:1px solid rgba(200,55,45,.18)}
.tab-gemini{background:rgba(29,78,216,.09);color:#1d4ed8;border:1px solid rgba(29,78,216,.18)}
.tab-china{background:rgba(220,38,38,.09);color:#dc2626;border:1px solid rgba(220,38,38,.18)}
.tab-progress{background:rgba(4,120,87,.09);color:#047857;border:1px solid rgba(4,120,87,.18)}
.tab-agi{background:rgba(124,58,237,.1);color:#6d28d9;border:1px solid rgba(124,58,237,.18)}
.tab-all{background:rgba(13,13,13,.05);color:var(--ink);border:1px solid var(--rule)}
.read-time{font-family:var(--mono);font-size:9px;letter-spacing:.8px;color:rgba(13,13,13,.32)}
.atag{font-family:var(--mono);font-size:9px;letter-spacing:.8px;padding:2px 7px;border:1px solid var(--rule);color:rgba(13,13,13,.35);}
.stats-row{display:grid;grid-template-columns:repeat(3,1fr);border-top:1px solid var(--rule);}
.stat-brick-light{padding:18px 22px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);}
.stat-brick-light:last-child{border-right:none}
.stat-brick-light .sbl-num{font-family:var(--syne);font-size:26px;font-weight:800;color:var(--ink);letter-spacing:-1px;line-height:1;}
.stat-brick-light .sbl-lbl{font-size:10px;color:rgba(13,13,13,.38);font-family:var(--mono);letter-spacing:.3px;margin-top:4px;}
.stat-brick-light .sbl-delta{font-size:9px;font-family:var(--mono);margin-top:5px;}
.stat-brick-light .trend-up{color:var(--accent3)}.stat-brick-light .trend-neutral{color:rgba(13,13,13,.28)}
.preds-grid{display:grid;grid-template-columns:repeat(3,1fr);border:1px solid var(--rule);margin-top:0;}
.pred-card{padding:26px;border-right:1px solid var(--rule);border-bottom:1px solid var(--rule);position:relative;transition:background .2s;opacity:0;transform:translateY(10px);overflow:hidden;}
.pred-card.visible{opacity:1;transform:none;transition:opacity .5s ease,transform .5s ease;}
.pred-card:nth-child(3n){border-right:none}
.pred-card:nth-last-child(-n+3){border-bottom:none}
.pred-card:hover{background:rgba(13,13,13,.015)}
.pred-card::after{content:"";position:absolute;top:0;left:0;right:0;height:3px;opacity:0;transition:opacity .25s;}
.pred-card:hover::after{opacity:1}
.stance-bull::after{background:var(--accent3)}.stance-caut::after{background:var(--accent5)}.stance-alarm::after{background:var(--accent)}.stance-prag::after{background:var(--accent2)}
.pred-header{display:flex;align-items:flex-start;gap:12px;margin-bottom:14px;}
.pred-emo{font-size:26px;line-height:1;flex-shrink:0;}
.pred-name{font-family:var(--syne);font-size:13px;font-weight:800;}
.pred-role{font-family:var(--mono);font-size:9px;color:rgba(13,13,13,.38);letter-spacing:.3px;margin-top:2px;}
.pred-year-tag{margin-left:auto;font-family:var(--mono);font-size:9px;color:var(--accent);background:rgba(200,55,45,.07);padding:3px 7px;border:1px solid rgba(200,55,45,.18);flex-shrink:0;white-space:nowrap;}
.pred-quote{font-family:var(--serif);font-size:13px;line-height:1.7;color:rgba(13,13,13,.7);font-style:italic;margin-bottom:18px;}
.pred-conf-row{display:flex;align-items:center;gap:10px;}
.pred-conf-lbl{font-family:var(--mono);font-size:8px;letter-spacing:1px;color:rgba(13,13,13,.28);flex-shrink:0;}
.pred-conf-bar{flex:1;height:2px;background:rgba(13,13,13,.08);overflow:hidden;}
.pred-conf-fill{height:100%;background:var(--ink);transition:width 1s ease;}
.pred-conf-pct{font-family:var(--mono);font-size:9px;color:rgba(13,13,13,.38);flex-shrink:0;}
.tl-wrap{padding:28px 0 28px 28px;border-top:1px solid var(--rule);position:relative;}
.tl-wrap::before{content:"";position:absolute;left:14px;top:36px;bottom:36px;width:1px;background:var(--rule);}
.tl-item{display:flex;gap:24px;margin-bottom:24px;align-items:flex-start;opacity:0;transform:translateX(-8px);}
.tl-item.visible{opacity:1;transform:none;transition:opacity .5s ease,transform .5s ease;}
.tl-dot{width:11px;height:11px;border-radius:50%;flex-shrink:0;margin-top:5px;border:2px solid var(--paper);box-shadow:0 0 0 1px rgba(13,13,13,.2);}
.tl-body{flex:1}
.tl-year{font-family:var(--mono);font-size:9px;letter-spacing:2px;color:rgba(13,13,13,.38);margin-bottom:3px;text-transform:uppercase;}
.tl-event{font-family:var(--syne);font-size:14px;font-weight:700;margin-bottom:5px;}
.tl-desc{font-size:13px;color:rgba(13,13,13,.55);line-height:1.6;}
.agi-consensus{border:2px solid var(--ink);margin:28px 0;display:grid;grid-template-columns:1fr 1fr 1fr;background:var(--ink);color:var(--paper);}
.agi-stat{padding:28px 32px;border-right:1px solid rgba(255,255,255,.07);text-align:center;}
.agi-stat:last-child{border-right:none}
.agi-big{font-family:var(--syne);font-size:52px;font-weight:800;line-height:1;letter-spacing:-3px;}
.agi-label{font-family:var(--mono);font-size:9px;letter-spacing:1px;color:rgba(245,240,232,.38);margin-top:10px;line-height:1.5;}
.modal-bg{position:fixed;inset:0;background:rgba(13,13,13,.82);z-index:2000;display:none;align-items:flex-start;justify-content:center;padding:48px 20px 80px;overflow-y:auto;backdrop-filter:blur(3px);}
.modal-bg.open{display:flex;animation:fadeM .2s ease;}
@keyframes fadeM{from{opacity:0}to{opacity:1}}
.modal-sheet{background:var(--paper);width:100%;max-width:720px;padding:52px;position:relative;border-left:4px solid var(--accent);box-shadow:16px 16px 0 rgba(13,13,13,.18),0 0 0 1px rgba(13,13,13,.06);animation:slideM .28s cubic-bezier(.4,0,.2,1);flex-shrink:0;}
@keyframes slideM{from{transform:translateY(18px)}to{transform:translateY(0)}}
.modal-x{position:absolute;top:18px;right:18px;background:none;border:1px solid var(--rule);width:30px;height:30px;cursor:pointer;font-size:13px;display:flex;align-items:center;justify-content:center;transition:all .2s;font-family:var(--mono);color:rgba(13,13,13,.5);}
.modal-x:hover{background:var(--ink);color:var(--paper);border-color:var(--ink);}
.modal-kicker{display:flex;gap:10px;align-items:center;margin-bottom:18px;flex-wrap:wrap;}
.modal-readtime,.modal-views{font-family:var(--mono);font-size:9px;letter-spacing:1px;color:rgba(13,13,13,.38);}
.modal-title{font-family:var(--serif);font-size:30px;line-height:1.2;margin-bottom:12px;letter-spacing:-.3px;}
.modal-deck{font-size:14px;font-style:italic;color:rgba(13,13,13,.55);line-height:1.65;margin-bottom:14px;}
.modal-byline{font-family:var(--mono);font-size:10px;letter-spacing:.5px;color:rgba(13,13,13,.45);margin-bottom:18px;}
.modal-divider{height:2px;background:var(--ink);margin-bottom:22px;}
.modal-body p{font-size:15px;line-height:1.9;margin-bottom:18px;color:rgba(13,13,13,.78);}
.modal-chips{display:flex;flex-wrap:wrap;gap:7px;margin-top:22px;padding-top:22px;border-top:1px solid var(--rule);}
.chip{font-family:var(--mono);font-size:9px;letter-spacing:1px;padding:3px 9px;border:1px solid var(--rule);color:rgba(13,13,13,.4);}
.site-footer{background:var(--ink);color:rgba(245,240,232,.35);padding:28px 40px;display:flex;justify-content:space-between;align-items:center;font-family:var(--mono);font-size:9px;letter-spacing:1px;gap:20px;}
.footer-brand{color:var(--paper);font-family:var(--serif);font-size:22px;letter-spacing:-.5px;flex-shrink:0;}
::-webkit-scrollbar{width:5px;height:5px}::-webkit-scrollbar-track{background:var(--paper2)}::-webkit-scrollbar-thumb{background:rgba(13,13,13,.18)}
@media(max-width:1100px){
  .editorial-grid{grid-template-columns:1fr}
  .editorial-main{border-right:none;padding-right:0;border-bottom:1px solid var(--rule)}
  .editorial-sidebar{padding-left:0;padding-top:0}
  .preds-grid{grid-template-columns:1fr 1fr}
  .pred-card:nth-child(3n){border-right:inherit}
  .pred-card:nth-child(2n){border-right:none}
  .stats-row{grid-template-columns:1fr 1fr}
  .agi-consensus{grid-template-columns:1fr}
  .agi-stat{border-right:none;border-bottom:1px solid rgba(255,255,255,.07)}
  .agi-stat:last-child{border-bottom:none}
}
@media(max-width:680px){
  .masthead-inner{grid-template-columns:1fr;text-align:center;gap:6px}
  .masthead-left{display:none}
  .masthead-right{align-items:center}
  .main-wrap,.stats-inner,.site-footer,.masthead-inner,.nav-inner{padding-left:16px;padding-right:16px}
  .modal-sheet{padding:28px 18px}
  .preds-grid{grid-template-columns:1fr}
  .pred-card:nth-child(n){border-right:none}
  .stats-row{grid-template-columns:1fr}
  .site-footer{flex-direction:column;text-align:center;gap:10px}
}
'''

def head() -> str:
    return f'<!DOCTYPE html>\n<html lang="en">\n<head>\n<meta charset="UTF-8"><meta name="viewport" content="width=device-width,initial-scale=1.0">\n<title>THE BRIEF &#8212; AI Intelligence, Unfiltered</title>\n<link rel="preconnect" href="https://fonts.googleapis.com">\n<link href="https://fonts.googleapis.com/css2?family=DM+Serif+Display:ital@0;1&family=Syne:wght@400;500;600;700;800&family=IBM+Plex+Mono:wght@400;500;600&family=DM+Sans:ital,wght@0,300;0,400;0,500;1,400&display=swap" rel="stylesheet">\n<style>{CSS}</style>\n</head>'

def ticker_bar() -> str:
    news = [
        "OpenAI weekly users cross 300M",
        "DeepSeek R2 trained for ~$2M &#8212; Nvidia falls 17%",
        "Claude 3.7 Sonnet leads on 7 of 10 key benchmarks",
        "Gemma 3 hits 40M downloads in 30 days",
        "Gemini 2.0 Ultra ships 1M token context window",
        "Bengio revises AGI estimate to 5&#8209;10 years",
        "Anthropic valued at $40B post Series E",
        "MCP protocol adopted across 50,000+ integrations",
    ]
    inner = "".join(f'<span>&#x25CF;&nbsp;&thinsp;{n}&emsp;</span>' for n in news * 2)
    return f'<div class="ticker-strip"><span class="ticker-kicker">LIVE&nbsp;FEED</span><div class="ticker-scroll"><div class="ticker-track">{inner}</div></div></div>'

def masthead() -> str:
    return '''<header class="masthead">
  <div class="masthead-inner">
    <div class="masthead-left">VOL.&thinsp;1 &nbsp;/&nbsp; ISSUE&thinsp;04 &nbsp;/&nbsp; APRIL 2026</div>
    <div style="text-align:center">
      <div class="pub-name">THE BRIEF</div>
      <div class="pub-sub">ARTIFICIAL INTELLIGENCE &nbsp;&middot;&nbsp; UNFILTERED</div>
    </div>
    <div class="masthead-right">
      <div class="live-indicator"><span class="live-pulse"></span>LIVE</div>
      <div class="live-time" id="ltime">--:--:--</div>
    </div>
  </div>
</header>'''

def nav_tabs() -> str:
    tabs = [("all","All"),("openai","OpenAI"),("claude","Claude"),("gemini","Gemini"),("china","China"),("progress","Progress"),("agi","AGI")]
    btns = "".join(f'<button class="nav-tab{" active" if t=="all" else ""}" data-tab="{t}" onclick="switchTab(\'{t}\')">{lbl}</button>' for t,lbl in tabs)
    return f'<nav class="section-nav"><div class="nav-inner">{btns}</div></nav>'

def stats_rail(stats: list) -> str:
    items = "".join(f'''<div class="stat-brick">
    <div class="stat-num">{s["value"]}</div>
    <div class="stat-lbl">{s["label"]}</div>
    <div class="stat-delta {"trend-up" if s.get("trend")=="up" else "trend-neutral"}">{s.get("delta","")}</div>
  </div>''' for s in stats[:6])
    return f'<div class="stats-rail"><div class="stats-inner">{items}</div></div>'

def article_card_lead(a: dict) -> str:
    tags_html = "".join(f'<span class="atag">{t}</span>' for t in (a.get("tags") or [])[:3])
    return f'''<article class="card-lead" onclick="openArticle({a["id"]})">
  <div class="card-lead-kicker">
    <span class="tab-badge tab-{a["tab"]}">{a["tab"].upper()}</span>
    <span class="read-time">{a.get("read_time",5)}&thinsp;min read</span>
  </div>
  <h2 class="card-lead-title">{a["title"]}</h2>
  <p class="card-lead-deck">{a.get("subtitle") or ""}</p>
  <div class="card-meta">
    <span class="byline">{a.get("author","Staff")}</span>
    <span>{a.get("source","")}</span>
  </div>
  <div class="card-tags">{tags_html}</div>
</article>'''

def article_card_compact(a: dict, idx: int = 0) -> str:
    return f'''<article class="card-compact" onclick="openArticle({a["id"]})">
  <div class="card-num">{str(idx+1).zfill(2)}</div>
  <div class="card-compact-body">
    <span class="tab-badge tab-{a["tab"]}">{a["tab"].upper()}</span>
    <h3 class="card-compact-title">{a["title"]}</h3>
    <div class="card-compact-meta">{a.get("author","Staff")} &middot; {a.get("read_time",5)}&thinsp;min</div>
  </div>
</article>'''

def prediction_card(p: dict) -> str:
    stance_cls = {"bullish":"stance-bull","cautious":"stance-caut","alarmed":"stance-alarm","pragmatic":"stance-prag"}.get(p.get("stance",""),"")
    conf = p.get("confidence",50)
    return f'''<div class="pred-card {stance_cls}">
  <div class="pred-header">
    <span class="pred-emo">{p.get("avatar","")}</span>
    <div><div class="pred-name">{p["scientist"]}</div><div class="pred-role">{p["role"]}, {p["org"]}</div></div>
    <div class="pred-year-tag">{p["year_prediction"]}</div>
  </div>
  <blockquote class="pred-quote">&ldquo;{p["quote"]}&rdquo;</blockquote>
  <div class="pred-conf-row">
    <span class="pred-conf-lbl">CONFIDENCE</span>
    <div class="pred-conf-bar"><div class="pred-conf-fill" style="width:{conf}%"></div></div>
    <span class="pred-conf-pct">{conf}%</span>
  </div>
</div>'''

def timeline_item(year: str, event: str, desc: str, color: str = "var(--ink)") -> str:
    return f'''<div class="tl-item">
  <div class="tl-dot" style="background:{color}"></div>
  <div class="tl-body">
    <div class="tl-year">{year}</div>
    <div class="tl-event">{event}</div>
    <div class="tl-desc">{desc}</div>
  </div>
</div>'''

def modal_shell() -> str:
    return '''<div class="modal-bg" id="modal-bg" onclick="closeModal(event)">
  <div class="modal-sheet">
    <button class="modal-x" onclick="closeModalDirect()">&#x2715;</button>
    <div class="modal-kicker" id="mk"></div>
    <h1 class="modal-title" id="mt"></h1>
    <p class="modal-deck" id="md"></p>
    <div class="modal-byline" id="mb"></div>
    <div class="modal-divider"></div>
    <div class="modal-body" id="mbody"></div>
    <div class="modal-chips" id="mchips"></div>
  </div>
</div>'''

def scripts() -> str:
    return '''<script>
(function tick(){
  var el=document.getElementById("ltime");
  if(el)el.textContent=new Date().toLocaleTimeString("en-US",{hour:"2-digit",minute:"2-digit",second:"2-digit"});
  setTimeout(tick,1000);
})();

function switchTab(tab){
  document.querySelectorAll(".nav-tab").forEach(function(b){b.classList.toggle("active",b.dataset.tab===tab);});
  document.querySelectorAll(".tab-section").forEach(function(s){s.classList.toggle("active",s.dataset.tab===tab);});
  var nav=document.querySelector(".section-nav");
  if(nav)window.scrollTo({top:nav.offsetTop-4,behavior:"smooth"});
}

async function openArticle(id){
  try{
    var r=await fetch("/api/articles/"+id);
    var a=await r.json();
    document.getElementById("mk").innerHTML=\'<span class="tab-badge tab-\'+a.tab+\'">\'+a.tab.toUpperCase()+\'</span><span class="modal-readtime">\'+( a.read_time||5)+\' min read</span><span class="modal-views">\'+a.views+\' views</span>\';
    document.getElementById("mt").textContent=a.title;
    document.getElementById("md").textContent=a.subtitle||"";
    document.getElementById("mb").innerHTML="<strong>"+(a.author||"Staff")+"</strong> &nbsp;/&nbsp; "+(a.source||"The Brief");
    document.getElementById("mbody").innerHTML=(a.content||"").split("\\n\\n").map(function(p){return"<p>"+p.trim()+"</p>";}).join("");
    document.getElementById("mchips").innerHTML=(a.tags||[]).map(function(t){return\'<span class="chip">#\'+t+\'</span>\';}).join("");
    document.getElementById("modal-bg").classList.add("open");
    document.body.style.overflow="hidden";
  }catch(e){console.error("openArticle error:",e);}
}
function closeModal(e){if(e.target.id==="modal-bg")closeModalDirect();}
function closeModalDirect(){document.getElementById("modal-bg").classList.remove("open");document.body.style.overflow="";}
document.addEventListener("keydown",function(e){if(e.key==="Escape")closeModalDirect();});

var io=new IntersectionObserver(function(entries){
  entries.forEach(function(e){if(e.isIntersecting){e.target.classList.add("visible");io.unobserve(e.target);}});
},{threshold:0.06});
function observe(){
  document.querySelectorAll(".card-lead,.card-compact,.pred-card,.tl-item").forEach(function(el){io.observe(el);});
}
observe();
document.querySelectorAll(".nav-tab").forEach(function(btn){
  btn.addEventListener("click",function(){setTimeout(observe,50);});
});
</script>'''
