from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import db
import templates as T

app = FastAPI(title="The Brief — AI Intelligence")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
db.init_db()


# ── REST API ───────────────────────────────────────────────────────────────

@app.get("/api/articles")
def list_articles(tab: str = None):
    return db.get_articles(tab)

@app.get("/api/articles/{aid}")
def read_article(aid: int):
    a = db.get_article(aid)
    if not a:
        raise HTTPException(status_code=404, detail="Not found")
    return a

@app.get("/api/stats")
def list_stats(category: str = None):
    return db.get_stats(category)

@app.get("/api/predictions")
def list_predictions():
    return db.get_predictions()


# ── PAGE BUILDERS ──────────────────────────────────────────────────────────

def _tab_section(tab_id: str, articles: list, all_stats: list) -> str:
    """Build one <div class=tab-section> for the given tab."""
    is_all   = tab_id == "all"
    active   = " active" if is_all else ""
    count    = f"{len(articles)} article{'s' if len(articles) != 1 else ''}"
    heading  = "ALL DISPATCHES" if is_all else tab_id.upper()

    html  = f'<div class="tab-section{active}" data-tab="{tab_id}">'
    html += f'<div class="section-heading"><span class="sec-title">{heading}</span><span class="sec-count">{count}</span></div>'

    if is_all:
        # Three-column numbered compact grid
        cols = [articles[:3], articles[3:7], articles[7:]]
        html += '<div style="display:grid;grid-template-columns:repeat(3,1fr);gap:0;border-bottom:1px solid var(--rule)">'
        for col in cols:
            html += '<div style="border-right:1px solid var(--rule);">'
            for i, a in enumerate(col):
                html += T.article_card_compact(a, i)
            html += '</div>'
        html += '</div>'
    else:
        # Editorial layout: big lead on left, compact stack on right
        html += '<div class="editorial-grid">'
        html += '<div class="editorial-main">'
        if articles:
            html += T.article_card_lead(articles[0])
        html += '</div><div class="editorial-sidebar">'
        for i, a in enumerate(articles[1:]):
            html += T.article_card_compact(a, i)
        html += '</div></div>'

        # Inline stats row for this topic
        tab_stats = [s for s in all_stats if s["category"] == tab_id][:3]
        if tab_stats:
            html += '<div class="stats-row">'
            for s in tab_stats:
                tc = "trend-up" if s.get("trend") == "up" else "trend-neutral"
                html += (
                    f'<div class="stat-brick-light">'
                    f'<div class="sbl-num">{s["value"]}</div>'
                    f'<div class="sbl-lbl">{s["label"]}</div>'
                    f'<div class="sbl-delta {tc}">{s.get("delta","")}</div>'
                    f'</div>'
                )
            html += '</div>'

    html += '</div>'
    return html


def _agi_section(predictions: list) -> str:
    """Build the AGI tab: prediction cards + consensus box + timeline."""
    pred_html = "".join(T.prediction_card(p) for p in predictions)

    tl_data = [
        ("2022", "ChatGPT launches. Consumer AI goes mainstream.",
         "100M users in 60 days. The public interfaces with frontier AI for the first time.",
         "#0a7a60"),
        ("2023", "GPT-4, Claude 2, Gemini. The capability explosion.",
         "Multimodal AI, 100K context windows, code generation surpasses competitive programming benchmarks.",
         "#1d4ed8"),
        ("2024", "Agents, reasoning models, open-source explosion.",
         "o1 and Claude 3.5 introduce inference-time reasoning. LLaMA 3 democratizes frontier capability.",
         "#7c3aed"),
        ("2025", "DeepSeek shock. Claude 3.7. Gemini 2.0.",
         "DeepSeek redefines training economics. 1M context windows arrive. AI enters every enterprise workflow.",
         "#b45309"),
        ("2026 \u2192", "The convergence point.",
         "Leading researchers revise timelines upward. Autonomous agents handle complete workflows.",
         "#c8372d"),
    ]
    tl_html = "".join(T.timeline_item(yr, ev, desc, col) for yr, ev, desc, col in tl_data)

    return (
        '<div class="tab-section" data-tab="agi">'
        '<div class="section-heading">'
        '<span class="sec-title">AGI: THE QUESTION OF OUR TIME</span>'
        '<span class="sec-count">Predictions from 6 leading researchers</span>'
        '</div>'
        f'<div class="preds-grid">{pred_html}</div>'
        '<div class="agi-consensus">'
        '<div class="agi-stat"><div class="agi-big">73%</div><div class="agi-label">OF SURVEYED AI RESEARCHERS EXPECT AGI BEFORE 2035</div></div>'
        '<div class="agi-stat"><div class="agi-big">5&#8209;10</div><div class="agi-label">YEARS &#8212; YOSHUA BENGIO&#8217;S REVISED ESTIMATE (2026)</div></div>'
        '<div class="agi-stat"><div class="agi-big">$1T+</div><div class="agi-label">PROJECTED GLOBAL AI INVESTMENT BY 2027</div></div>'
        '</div>'
        '<div style="padding:0 0 20px">'
        '<div class="section-heading" style="margin-bottom:0"><span class="sec-title">CAPABILITY TIMELINE</span></div>'
        f'<div class="tl-wrap">{tl_html}</div>'
        '</div>'
        '</div>'
    )


# ── MAIN ROUTE ─────────────────────────────────────────────────────────────

@app.get("/", response_class=HTMLResponse)
def index():
    all_articles  = db.get_articles()
    all_stats     = db.get_stats()
    all_preds     = db.get_predictions()

    page  = T.head()
    page += "<body>"
    page += T.ticker_bar()
    page += T.masthead()
    page += T.stats_rail(all_stats[:6])
    page += T.nav_tabs()
    page += '<div class="main-wrap">'

    # Standard tabs
    for tab in ["all", "openai", "claude", "gemini", "china", "progress"]:
        arts = all_articles if tab == "all" else [a for a in all_articles if a["tab"] == tab]
        page += _tab_section(tab, arts, all_stats)

    # AGI tab has its own special layout
    page += _agi_section(all_preds)

    page += "</div>"  # .main-wrap
    page += T.modal_shell()
    page += '''
<footer class="site-footer">
  <div class="footer-brand">The Brief</div>
  <div>ainews.anervea.live &nbsp;&middot;&nbsp; Anervea Intelligence Platform</div>
  <div>Public research &amp; benchmarks &nbsp;&middot;&nbsp; Continuous updates</div>
</footer>'''
    page += T.scripts()
    page += "</body></html>"
    return HTMLResponse(page)
