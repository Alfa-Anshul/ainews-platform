from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3, json

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

DB_PATH = "/tmp/ainews.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db(); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT, tab TEXT, title TEXT, subtitle TEXT,
        content TEXT, author TEXT, source TEXT, tags TEXT, views INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT, label TEXT, value TEXT, category TEXT, icon TEXT, trend TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT, scientist TEXT, role TEXT, quote TEXT,
        year_prediction TEXT, confidence INTEGER, avatar TEXT)''')
    if c.execute('SELECT COUNT(*) FROM articles').fetchone()[0] == 0:
        seed_data(c)
    conn.commit(); conn.close()

def seed_data(c):
    arts = [
        ("openai","OpenAI Reaches 300 Million Weekly Active Users","ChatGPT dominates the consumer AI market with unprecedented growth","""OpenAI has shattered every metric in 2025-2026, crossing 300 million weekly active users across all its products. ChatGPT alone accounts for over 180 million daily conversations, while the API powers thousands of enterprise integrations globally. The company's revenue crossed $5 billion ARR in Q1 2026, driven largely by ChatGPT Plus subscriptions and Azure OpenAI API usage through Microsoft's cloud.

The GPT-4o and o3 model families continue to anchor OpenAI's commercial success. However, analysts note a growing concern: user retention is being challenged by Anthropic's Claude 3.7 Sonnet, which scores higher on coding benchmarks and long-context reasoning. OpenAI's response has been aggressive — slashing API prices by 40% and releasing Sora 2 for video generation to create a moat through multi-modal capabilities.

Despite the competition, OpenAI's developer ecosystem remains its strongest asset. With over 2 million developers building on its APIs and enterprise deals with Apple, Microsoft, and Salesforce, OpenAI still holds the largest installed base of any AI platform. The question is no longer dominance but sustainability — can they maintain this lead as Claude, Gemini, and open-source models close the gap?""","Aniket Shah","TechCrunch",'["OpenAI","ChatGPT","AGI"]'),
        ("openai","The Cracks in OpenAI's Moat: Developer Exodus Begins","Enterprise teams quietly migrate to Claude and open-source alternatives","""A quiet but significant shift is underway in the enterprise AI landscape. Multiple Fortune 500 companies — including three major banks and two healthcare giants — have begun migrating production workloads from OpenAI's API to Anthropic's Claude 3.7 Sonnet and the open-source Llama 3.3 family. The primary drivers: reliability, cost predictability, and compliance with data privacy regulations.

OpenAI's API outages in late 2025 spooked enterprise buyers. Three significant incidents caused downstream failures in customer-facing applications. Anthropic, meanwhile, has had 99.97% uptime over the same period. For enterprise CIOs, that delta is career-defining.

Cost is another driver. Anthropic's Claude Haiku 3.5 processes 200,000 tokens per dollar at output speed, making it significantly more economical for bulk summarization and classification tasks.""","Priya Mehta","The Information",'["OpenAI","Enterprise","Migration"]'),
        ("claude","Why Claude is Outperforming GPT-4o on Every Benchmark That Matters","Constitutional AI, 200K context, and safety-first training give Anthropic an edge","""Claude 3.7 Sonnet has emerged as the model of choice for professional developers and enterprise teams. Its performance on the MMLU Pro, HumanEval+, and GPQA benchmarks now exceeds GPT-4o on 7 out of 10 tested domains.

The real differentiator is Claude's Constitutional AI training methodology. By training the model to reason about its own outputs against a set of principles, Anthropic has produced a model with notably lower hallucination rates on factual tasks. Internal studies show Claude hallucinating on medical literature queries at approximately 2.3% vs GPT-4o's 4.1%.

Claude's 200,000 token context window is also a practical game-changer. Enterprise use cases — auditing legal contracts, analyzing clinical trial PDFs, reviewing codebases — require feeding massive documents into a single context. Claude handles this with minimal degradation in output quality.""","Aniket Shah","AI Trends Weekly",'["Claude","Anthropic","Benchmarks"]'),
        ("claude","Anthropic's $40B Valuation: The Safety-First Bet Is Paying Off","From safety-focused startup to enterprise AI powerhouse in 3 years","""When Dario Amodei and Daniela Amodei left OpenAI in 2021, many in Silicon Valley questioned the commercial viability of a safety-first AI lab. Three years later, Anthropic is valued at $40 billion, has $4.5 billion in committed revenue, and has signed deals with AWS, Google Cloud, and Salesforce.

The Constitutional AI framework has proven to be not just ethically superior but commercially compelling. Regulated industries require explainability and auditability. Claude's chain-of-thought reasoning, combined with Anthropic's commitment to model cards and safety research, has made it the default choice for compliance-conscious buyers.

Anthropic's model release cadence has also accelerated. Claude 3.7 Sonnet shipped in February 2026, with Claude 4 Opus expected in Q3 2026.""","Rohan Verma","Bloomberg Technology",'["Anthropic","Claude","Valuation"]'),
        ("gemini","Google Gemma 3: Open Source Is Eating the AI World","Google's open-weights strategy reshapes the competitive landscape","""Google's Gemma 3 release in early 2026 was a watershed moment for open-source AI. The 27B parameter model — freely available for commercial use — matched GPT-4o Mini on most standard benchmarks while running comfortably on a single H100 GPU.

The release reflects Google's strategic pivot: rather than competing solely on proprietary API revenue, DeepMind and Google Research are betting that seeding the ecosystem with capable open-weight models will drive adoption of Google Cloud infrastructure, TPU rentals, and Vertex AI managed deployments.

Hugging Face reports Gemma 3 has been downloaded over 40 million times since launch — more than any previous open model release. The Gemma ecosystem has catalyzed medical, legal, and code-specialized fine-tuned variants.""","Siddharth Rao","Wired",'["Google","Gemma","OpenSource"]'),
        ("gemini","Gemini 2.0 Ultra: Google's Counterattack at the Frontier","Deep Research, real-time grounding, and 1M context put Gemini back in contention","""After a rocky 2024 debut, Gemini 2.0 Ultra represents Google's most credible challenge yet to OpenAI and Anthropic at the frontier. The model ships with native tool use, a 1 million token context window, real-time web grounding, and Deep Research mode.

In head-to-head evaluations on long-context retrieval tasks, Gemini 2.0 Ultra outperforms both Claude 3.7 Sonnet and GPT-4o. For enterprise use cases involving large document corpora — law firms, research institutions, financial analysts — this is a decisive advantage.

Google's distribution is also unmatched. With Gemini embedded in Google Workspace, Search, and Android, no other AI company has comparable first-party surface area. Daily Gemini interactions in Google products exceed 1 billion.""","Ananya Krishnan","The Verge",'["Google","Gemini","LLM"]'),
        ("china","China's AGI Race: DeepSeek, Kimi, and the National AI Imperative","Beijing mobilizes $50B in state funding as Chinese labs close the capability gap","""China's AI industry has undergone a dramatic transformation. DeepSeek-V3 and DeepSeek-R1 shocked the global AI community in late 2025 by achieving GPT-4o-level performance at a fraction of the training cost — an estimated $6 million vs OpenAI's hundreds of millions.

Kimi (by Moonshot AI) has emerged as China's Claude equivalent — a 128K context model with exceptional long-document comprehension. ByteDance's Doubao and Alibaba's Qwen 2.5 family have pushed to frontier capability levels.

Beijing's national AI strategy — backed by $50 billion in state investment — is accelerating capability development at a pace that makes Western observers deeply uncomfortable. Chinese labs have responded to chip embargoes with algorithmic efficiency rather than raw compute.""","Li Wei","MIT Technology Review",'["China","DeepSeek","AGI"]'),
        ("china","DeepSeek R2: The $2M Model That Humbled Silicon Valley","Chinese startup's efficiency breakthrough rewrites the economics of frontier AI","""DeepSeek's R2 model, released in March 2026, has become the most discussed AI development since ChatGPT's launch. Trained for approximately $2 million using sparse mixture-of-experts, multi-head latent attention, and aggressive inference-time compute — R2 achieves scores on mathematical reasoning and coding that exceed GPT-4o.

The implications are profound. Silicon Valley's thesis — that frontier AI requires massive compute budgets accessible only to trillion-dollar companies — appears to be wrong. DeepSeek has demonstrated that algorithmic innovation can substitute for raw compute.

Nvidia's stock dropped 17% the day DeepSeek R2 was publicly benchmarked. For the US-China AI competition, R2 is a Sputnik-moment equivalent.""","Aniket Shah","Financial Times",'["DeepSeek","China","Efficiency"]'),
        ("progress","AI in 2026: From Language Models to Autonomous Agents","The shift from text generation to goal-directed action is the defining trend of 2026","""The AI narrative in 2026 is no longer about which model writes better poetry. It's about which systems can take actions in the world — browsing the web, writing and executing code, sending emails, managing files, and completing multi-step workflows without human intervention.

OpenAI's Operator, Anthropic's Computer Use API, and Google's Project Mariner have all shipped production-grade agentic capabilities. The Model Context Protocol (MCP) — developed by Anthropic and now adopted by OpenAI and Google — provides a standardized way for AI models to interface with external tools, databases, and services.

Enterprise adoption of AI agents is accelerating fastest in software engineering (GitHub Copilot Workspace, Cursor), customer service (Salesforce Agentforce), and financial analysis.""","Aniket Shah","AI Trends Weekly",'["Agents","AGI","Progress"]'),
        ("agi","AGI by 2027? The Scientists Who Say Yes","A growing faction of researchers believes general intelligence is closer than consensus admits","""The question of when — not whether — artificial general intelligence arrives has shifted from philosophy seminar to mainstream technical debate. Sam Altman has publicly stated his belief that AGI will be built within OpenAI's current research agenda. Demis Hassabis told the Financial Times in January 2026 that DeepMind is 'likely within years, not decades' of systems that match human performance across cognitive domains.

The technical case for accelerating timelines rests on three observations: scaling laws have not plateaued as many predicted; inference-time compute provides a second scaling dimension beyond training compute; and the capability jump from GPT-3 to GPT-4 to o3 has been dramatically faster than most researchers forecasted.

The counterarguments are real — current models still lack genuine causal reasoning and embodied understanding. But the optimists point out that these limitations were cited about every previous generation of models.""","Prof. James Wu","Nature AI",'["AGI","Predictions","Future"]')
    ]
    for a in arts:
        c.execute('INSERT INTO articles (tab,title,subtitle,content,author,source,tags) VALUES (?,?,?,?,?,?,?)', a)

    stats = [
        ("OpenAI Weekly Users","300M+","openai","\U0001f465","+15% QoQ"),
        ("ChatGPT Daily Chats","180M","openai","\U0001f4ac","+22% YoY"),
        ("OpenAI ARR","$5B+","openai","\U0001f4b0","+180% YoY"),
        ("Claude Enterprise Customers","10,000+","claude","\U0001f3e2","+300% YoY"),
        ("Anthropic Valuation","$40B","claude","\U0001f4c8","Series E"),
        ("Claude Uptime","99.97%","claude","\u2705","vs 99.1% GPT-4o"),
        ("Gemma 3 Downloads","40M+","gemini","\u2b07\ufe0f","30 days"),
        ("Gemini Daily Interactions","1B+","gemini","\u2728","Google Workspace"),
        ("Gemini Context Window","1M tokens","gemini","\U0001f4dc","Industry leading"),
        ("DeepSeek R2 Cost","~$2M","china","\U0001f525","vs $100M+ GPT-4"),
        ("China AI Investment","$50B","china","\U0001f1e8\U0001f1f3","State 2026"),
        ("Qwen 2.5-72B Score","Top 5","china","\U0001f916","MMLU Pro"),
        ("AI Agents in Production","2M+","progress","\U0001f916","Enterprise"),
        ("MCP Integrations","50,000+","progress","\U0001f50c","Ecosystem"),
        ("AGI Timeline Consensus","5-10 yrs","agi","\U0001f9e0","Leading Researchers"),
        ("Researchers Expect AGI < 2035","73%","agi","\U0001f52e","Survey 2026")
    ]
    for s in stats:
        c.execute('INSERT INTO stats (label,value,category,icon,trend) VALUES (?,?,?,?,?)', s)

    preds = [
        ("Sam Altman","CEO, OpenAI","AGI is not a distant theoretical concept. We expect to build it within this decade, possibly within years. The scaling laws have not broken down — if anything, inference-time compute has opened a second frontier we are only beginning to explore.","2027-2028",85,"\U0001f3af"),
        ("Demis Hassabis","CEO, Google DeepMind","We are likely years, not decades, away from systems that match or exceed human performance across most cognitive domains. The combination of foundation models, world models, and RL is converging faster than anyone predicted.","2028-2030",78,"\U0001f9ec"),
        ("Yoshua Bengio","Turing Award Laureate","I've revised my timeline. The progress in reasoning, planning, and code generation over the last two years has been remarkable. My current estimate is 5-10 years to systems that most researchers would call AGI.","2030-2035",65,"\U0001f393"),
        ("Dario Amodei","CEO, Anthropic","AGI — or what I call 'powerful AI' — could arrive as early as 2026-2027. This is both exciting and deeply concerning. The safety work we need to do to make this go well is not keeping pace with capability development.","2026-2027",80,"\U0001f6e1\ufe0f"),
        ("Geoffrey Hinton","AI Pioneer, Turing Laureate","I left Google because I became genuinely alarmed about the pace of progress. These systems are approaching capabilities that we do not understand and cannot fully control. The timeline question is less important than the alignment question.","2025-2030",72,"\u26a0\ufe0f"),
        ("Fei-Fei Li","Stanford HAI","AGI as typically defined is a moving goalpost. But systems that can genuinely assist humans across open-ended real-world tasks? Those are arriving now. The question is how we govern and distribute them equitably.","2025-2028",70,"\U0001f30d")
    ]
    for p in preds:
        c.execute('INSERT INTO predictions (scientist,role,quote,year_prediction,confidence,avatar) VALUES (?,?,?,?,?,?)', p)

init_db()

@app.get("/api/articles")
def get_articles(tab: str = None):
    conn = get_db()
    rows = conn.execute('SELECT * FROM articles WHERE tab=? ORDER BY created_at DESC',(tab,)).fetchall() if tab else conn.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    return [{**dict(r), 'tags': json.loads(r['tags']) if r['tags'] else []} for r in rows]

@app.get("/api/articles/{article_id}")
def get_article(article_id: int):
    conn = get_db()
    conn.execute('UPDATE articles SET views=views+1 WHERE id=?',(article_id,)); conn.commit()
    r = conn.execute('SELECT * FROM articles WHERE id=?',(article_id,)).fetchone()
    conn.close()
    if not r: raise HTTPException(404)
    return {**dict(r), 'tags': json.loads(r['tags']) if r['tags'] else []}

@app.get("/api/stats")
def get_stats(category: str = None):
    conn = get_db()
    rows = conn.execute('SELECT * FROM stats WHERE category=?',(category,)).fetchall() if category else conn.execute('SELECT * FROM stats').fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/predictions")
def get_predictions():
    conn = get_db()
    rows = conn.execute('SELECT * FROM predictions').fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/", response_class=HTMLResponse)
def index(): return HTMLResponse(HTML)

HTML = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>AI Pulse — Live Intelligence Feed 2026</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bebas+Neue&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root{--bg:#030712;--bg2:#0a0f1e;--bg3:#0d1529;--surface:rgba(255,255,255,.04);--surface2:rgba(255,255,255,.08);--border:rgba(255,255,255,.08);--text:#f0f4ff;--muted:#6b7280;--accent:#38bdf8;--accent2:#818cf8;--accent3:#34d399;--accent4:#f472b6;--accent5:#fb923c;--gold:#fbbf24;--red:#f87171}
*{margin:0;padding:0;box-sizing:border-box}html{scroll-behavior:smooth}
body{background:var(--bg);color:var(--text);font-family:'Space Grotesk',sans-serif;min-height:100vh;overflow-x:hidden}
body::before{content:'';position:fixed;inset:0;background:radial-gradient(ellipse 80% 50% at 20% -10%,rgba(56,189,248,.12),transparent 60%),radial-gradient(ellipse 60% 40% at 80% 110%,rgba(129,140,248,.10),transparent 60%);pointer-events:none;z-index:0}
body::after{content:'';position:fixed;inset:0;background-image:linear-gradient(rgba(255,255,255,.015) 1px,transparent 1px),linear-gradient(90deg,rgba(255,255,255,.015) 1px,transparent 1px);background-size:60px 60px;pointer-events:none;z-index:0}
.ticker-wrap{position:fixed;top:0;width:100%;background:linear-gradient(90deg,#0c1a2e,#0a1628,#0c1a2e);border-bottom:1px solid rgba(56,189,248,.3);z-index:1000;overflow:hidden;height:32px;display:flex;align-items:center}
.ticker-wrap::before,.ticker-wrap::after{content:'';position:absolute;top:0;bottom:0;width:80px;z-index:2}
.ticker-wrap::before{left:0;background:linear-gradient(90deg,#0c1a2e,transparent)}
.ticker-wrap::after{right:0;background:linear-gradient(270deg,#0c1a2e,transparent)}
.ticker-label{flex-shrink:0;background:var(--accent);color:#000;font-size:10px;font-weight:700;letter-spacing:2px;padding:0 12px;height:100%;display:flex;align-items:center;z-index:3}
.ticker-inner{display:flex;animation:ticker 50s linear infinite;white-space:nowrap}
.ticker-item{font-size:11px;color:var(--muted);padding:0 40px;font-family:'JetBrains Mono',monospace}
.ticker-item span{color:var(--accent)}
@keyframes ticker{0%{transform:translateX(0)}100%{transform:translateX(-50%)}}
header{position:relative;z-index:100;padding:60px 0 0}
.header-inner{max-width:1400px;margin:0 auto;padding:32px 40px 0;display:flex;align-items:center;justify-content:space-between}
.logo{display:flex;align-items:center;gap:16px}
.logo-icon{width:44px;height:44px;background:linear-gradient(135deg,var(--accent),var(--accent2));border-radius:12px;display:flex;align-items:center;justify-content:center;font-size:20px;box-shadow:0 0 30px rgba(56,189,248,.4);animation:pulse-logo 3s ease-in-out infinite}
@keyframes pulse-logo{0%,100%{box-shadow:0 0 20px rgba(56,189,248,.3)}50%{box-shadow:0 0 50px rgba(56,189,248,.7)}}
.logo-title{font-family:'Bebas Neue',sans-serif;font-size:32px;letter-spacing:3px;background:linear-gradient(135deg,var(--accent),var(--accent2));-webkit-background-clip:text;-webkit-text-fill-color:transparent}
.logo-subtitle{font-size:10px;color:var(--muted);letter-spacing:3px;text-transform:uppercase;margin-top:2px}
.header-meta{display:flex;align-items:center;gap:16px;font-size:12px;color:var(--muted)}
.live-dot{width:8px;height:8px;background:var(--accent3);border-radius:50%;animation:blink 1.5s ease-in-out infinite;box-shadow:0 0 8px var(--accent3)}
@keyframes blink{0%,100%{opacity:1}50%{opacity:.3}}
.hero{position:relative;z-index:10;max-width:1400px;margin:0 auto;padding:60px 40px 40px}
.hero-eyebrow{font-size:11px;letter-spacing:4px;color:var(--accent);text-transform:uppercase;font-family:'JetBrains Mono',monospace;margin-bottom:16px;opacity:0;animation:fadeUp .8s .2s forwards}
.hero-title{font-family:'Bebas Neue',sans-serif;font-size:clamp(52px,8vw,96px);line-height:.92;letter-spacing:2px;margin-bottom:20px;opacity:0;animation:fadeUp .8s .4s forwards}
.hero-title .l1{color:var(--text);display:block}
.hero-title .l2{background:linear-gradient(135deg,var(--accent),var(--accent2),var(--accent3));-webkit-background-clip:text;-webkit-text-fill-color:transparent;display:block}
.hero-sub{font-size:16px;color:var(--muted);max-width:600px;line-height:1.6;opacity:0;animation:fadeUp .8s .6s forwards}
@keyframes fadeUp{from{opacity:0;transform:translateY(30px)}to{opacity:1;transform:translateY(0)}}
.stats-bar{position:relative;z-index:10;max-width:1400px;margin:0 auto;padding:0 40px}
.stats-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px}
.stat-card{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:20px 24px;position:relative;overflow:hidden;transition:all .3s;opacity:0;animation:fadeUp .6s forwards}
.stat-card:hover{background:var(--surface2);border-color:rgba(56,189,248,.3);transform:translateY(-4px)}
.stat-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,var(--accent),var(--accent2));opacity:0;transition:opacity .3s}
.stat-card:hover::before{opacity:1}
.stat-icon{font-size:22px;margin-bottom:8px}
.stat-value{font-family:'Bebas Neue',sans-serif;font-size:32px;letter-spacing:1px;color:var(--accent);line-height:1}
.stat-label{font-size:12px;color:var(--muted);margin-top:4px}
.stat-trend{font-size:11px;color:var(--accent3);font-family:'JetBrains Mono',monospace;margin-top:8px}
.tabs-section{position:relative;z-index:10;max-width:1400px;margin:0 auto;padding:40px 40px 0}
.tabs-nav{display:flex;gap:4px;background:rgba(255,255,255,.03);border:1px solid var(--border);border-radius:20px;padding:6px;margin-bottom:40px;overflow-x:auto;scrollbar-width:none}
.tabs-nav::-webkit-scrollbar{display:none}
.tab-btn{flex-shrink:0;background:none;border:none;color:var(--muted);font-family:'Space Grotesk',sans-serif;font-size:13px;font-weight:500;padding:10px 22px;border-radius:14px;cursor:pointer;transition:all .3s;display:flex;align-items:center;gap:8px;white-space:nowrap}
.tab-btn:hover{color:var(--text);background:var(--surface)}
.tab-btn.active{background:linear-gradient(135deg,rgba(56,189,248,.2),rgba(129,140,248,.2));color:var(--text);border:1px solid rgba(56,189,248,.3)}
.tab-dot{width:6px;height:6px;border-radius:50%;background:var(--muted);transition:all .3s}
.tab-btn.active .tab-dot{background:var(--accent);box-shadow:0 0 8px var(--accent)}
.content-area{position:relative;z-index:10;max-width:1400px;margin:0 auto;padding:0 40px 80px}
.tab-content{display:none}
.tab-content.active{display:block;animation:fadeIn .5s ease}
@keyframes fadeIn{from{opacity:0;transform:translateY(12px)}to{opacity:1;transform:translateY(0)}}
.articles-grid{display:grid;grid-template-columns:2fr 1fr;gap:24px;margin-bottom:40px}
.article-card-featured{background:var(--surface);border:1px solid var(--border);border-radius:24px;overflow:hidden;cursor:pointer;transition:all .4s cubic-bezier(.4,0,.2,1)}
.article-card-featured:hover{border-color:rgba(56,189,248,.4);transform:translateY(-6px);box-shadow:0 24px 60px rgba(0,0,0,.5)}
.article-featured-header{padding:32px 32px 0}
.article-featured-visual{height:200px;margin:24px 32px;border-radius:16px;background:linear-gradient(135deg,var(--bg3),var(--bg2));border:1px solid var(--border);display:flex;align-items:center;justify-content:center;position:relative;overflow:hidden}
.article-featured-visual::before{content:'';position:absolute;inset:0;background:linear-gradient(135deg,rgba(56,189,248,.1),rgba(129,140,248,.1))}
.vis-icon{position:relative;z-index:1;font-size:72px;animation:float 3s ease-in-out infinite}
@keyframes float{0%,100%{transform:translateY(0)}50%{transform:translateY(-10px)}}
.article-featured-body{padding:0 32px 32px}
.article-tag{display:inline-flex;align-items:center;gap:6px;font-size:10px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--accent);background:rgba(56,189,248,.1);border:1px solid rgba(56,189,248,.2);padding:4px 10px;border-radius:6px;margin-bottom:12px}
.article-title{font-size:22px;font-weight:700;line-height:1.3;margin-bottom:10px}
.article-subtitle{font-size:14px;color:var(--muted);line-height:1.5;margin-bottom:16px}
.article-meta{display:flex;align-items:center;gap:16px;font-size:12px;color:var(--muted)}
.article-author{color:var(--accent2);font-weight:500}
.articles-sidebar{display:flex;flex-direction:column;gap:16px}
.article-card-small{background:var(--surface);border:1px solid var(--border);border-radius:16px;padding:20px;cursor:pointer;transition:all .3s;flex:1}
.article-card-small:hover{border-color:rgba(56,189,248,.3);transform:translateX(6px);background:var(--surface2)}
.small-title{font-size:15px;font-weight:600;line-height:1.4;margin-bottom:8px}
.small-meta{font-size:11px;color:var(--muted)}
.modal-overlay{position:fixed;inset:0;background:rgba(0,0,0,.85);z-index:2000;display:none;align-items:center;justify-content:center;padding:40px;backdrop-filter:blur(8px)}
.modal-overlay.open{display:flex;animation:fadeIn .3s}
.modal{background:var(--bg2);border:1px solid rgba(56,189,248,.2);border-radius:28px;max-width:760px;width:100%;max-height:80vh;overflow-y:auto;padding:48px;position:relative;box-shadow:0 40px 100px rgba(0,0,0,.8)}
.modal::-webkit-scrollbar{width:4px}
.modal::-webkit-scrollbar-thumb{background:var(--border);border-radius:2px}
.modal-close{position:absolute;top:20px;right:20px;background:var(--surface);border:1px solid var(--border);color:var(--muted);width:36px;height:36px;border-radius:10px;cursor:pointer;font-size:18px;display:flex;align-items:center;justify-content:center;transition:all .2s}
.modal-close:hover{color:var(--text);background:var(--surface2)}
.modal-tag{font-size:10px;font-weight:600;letter-spacing:2px;text-transform:uppercase;color:var(--accent);margin-bottom:16px;display:block}
.modal-title{font-size:28px;font-weight:700;line-height:1.25;margin-bottom:12px}
.modal-subtitle{font-size:16px;color:var(--muted);margin-bottom:20px;line-height:1.5}
.modal-meta{display:flex;gap:20px;font-size:12px;color:var(--muted);margin-bottom:32px;padding-bottom:32px;border-bottom:1px solid var(--border)}
.modal-content{font-size:15px;line-height:1.8;color:rgba(240,244,255,.85);white-space:pre-line}
.modal-tags{display:flex;flex-wrap:wrap;gap:8px;margin-top:28px}
.modal-tag-chip{font-size:11px;color:var(--accent2);background:rgba(129,140,248,.1);border:1px solid rgba(129,140,248,.2);padding:4px 12px;border-radius:20px}
.predictions-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-bottom:40px}
.prediction-card{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:28px;position:relative;transition:all .3s;overflow:hidden}
.prediction-card::before{content:'"';position:absolute;top:10px;left:20px;font-size:80px;font-family:Georgia,serif;color:rgba(56,189,248,.08);line-height:1;pointer-events:none}
.prediction-card:hover{border-color:rgba(56,189,248,.3);transform:translateY(-4px);box-shadow:0 20px 50px rgba(0,0,0,.4)}
.pred-avatar{font-size:36px;margin-bottom:12px}
.pred-name{font-size:17px;font-weight:700;margin-bottom:2px}
.pred-role{font-size:11px;color:var(--muted);margin-bottom:16px}
.pred-quote{font-size:13px;color:rgba(240,244,255,.75);line-height:1.7;margin-bottom:16px}
.pred-footer{display:flex;justify-content:space-between;align-items:center}
.pred-year{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--accent);background:rgba(56,189,248,.1);padding:4px 10px;border-radius:6px}
.pred-conf{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--muted)}
.conf-bar{width:60px;height:4px;background:var(--border);border-radius:2px;overflow:hidden}
.conf-fill{height:100%;background:linear-gradient(90deg,var(--accent),var(--accent2));border-radius:2px}
.section-header{display:flex;align-items:flex-end;justify-content:space-between;margin-bottom:28px}
.section-title{font-family:'Bebas Neue',sans-serif;font-size:36px;letter-spacing:2px}
.section-count{font-size:12px;color:var(--muted);font-family:'JetBrains Mono',monospace}
.all-articles-grid{display:grid;grid-template-columns:repeat(3,1fr);gap:20px}
.article-card-medium{background:var(--surface);border:1px solid var(--border);border-radius:20px;padding:24px;cursor:pointer;transition:all .3s cubic-bezier(.4,0,.2,1);display:flex;flex-direction:column;gap:12px}
.article-card-medium:hover{border-color:rgba(56,189,248,.3);transform:translateY(-6px);box-shadow:0 20px 50px rgba(0,0,0,.4)}
.card-emoji{font-size:36px;display:block}
.card-medium-title{font-size:16px;font-weight:600;line-height:1.4}
.card-medium-sub{font-size:13px;color:var(--muted);line-height:1.5}
.card-medium-footer{display:flex;justify-content:space-between;padding-top:12px;border-top:1px solid var(--border);font-size:11px;color:var(--muted)}
.stats-detail-grid{display:grid;grid-template-columns:repeat(4,1fr);gap:16px;margin-top:20px}
.timeline{position:relative;margin:40px 0;padding-left:32px}
.timeline::before{content:'';position:absolute;left:0;top:0;bottom:0;width:2px;background:linear-gradient(180deg,var(--accent),var(--accent2),var(--accent3));border-radius:1px}
.timeline-item{position:relative;padding-bottom:32px}
.timeline-dot{position:absolute;left:-37px;top:4px;width:12px;height:12px;border-radius:50%;background:var(--accent);border:2px solid var(--bg);box-shadow:0 0 12px var(--accent)}
.timeline-year{font-family:'JetBrains Mono',monospace;font-size:13px;color:var(--accent);margin-bottom:6px}
.timeline-event{font-size:16px;font-weight:600;margin-bottom:4px}
.timeline-desc{font-size:13px;color:var(--muted);line-height:1.6}
footer{position:relative;z-index:10;border-top:1px solid var(--border);padding:32px 40px;max-width:1400px;margin:0 auto;display:flex;align-items:center;justify-content:space-between;font-size:12px;color:var(--muted)}
::-webkit-scrollbar{width:6px;height:6px}
::-webkit-scrollbar-track{background:var(--bg)}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px}
@media(max-width:1024px){.articles-grid,.all-articles-grid{grid-template-columns:1fr}.predictions-grid,.stats-detail-grid{grid-template-columns:repeat(2,1fr)}.stats-grid{grid-template-columns:repeat(2,1fr)}}
@media(max-width:640px){.header-inner,.hero,.tabs-section,.content-area{padding-left:20px;padding-right:20px}.hero-title{font-size:48px}.predictions-grid,.all-articles-grid,.stats-detail-grid{grid-template-columns:1fr}.modal{padding:28px 20px}}
.tag-china{color:var(--red)!important;background:rgba(248,113,113,.1)!important;border-color:rgba(248,113,113,.2)!important}
.tag-agi{color:var(--gold)!important;background:rgba(251,191,36,.1)!important;border-color:rgba(251,191,36,.2)!important}
.tag-gemini{color:var(--accent3)!important;background:rgba(52,211,153,.1)!important;border-color:rgba(52,211,153,.2)!important}
.tag-claude{color:var(--accent4)!important;background:rgba(244,114,182,.1)!important;border-color:rgba(244,114,182,.2)!important}
.tag-progress{color:var(--accent5)!important;background:rgba(251,146,60,.1)!important;border-color:rgba(251,146,60,.2)!important}
.tag-openai{color:var(--accent)!important;background:rgba(56,189,248,.1)!important;border-color:rgba(56,189,248,.2)!important}
</style></head>
<body>
<div class="ticker-wrap">
  <div class="ticker-label">LIVE</div>
  <div class="ticker-inner">
    <span class="ticker-item">🤖 <span>OpenAI</span> reaches 300M weekly active users — Q1 2026</span>
    <span class="ticker-item">🧠 <span>Claude 3.7 Sonnet</span> outperforms GPT-4o on 7/10 benchmarks</span>
    <span class="ticker-item">🇨🇳 <span>DeepSeek R2</span> trained for ~$2M — Nvidia drops 17%</span>
    <span class="ticker-item">🌟 <span>Gemma 3</span> hits 40M downloads in 30 days</span>
    <span class="ticker-item">⚡ <span>Gemini 2.0 Ultra</span> ships 1M token context window</span>
    <span class="ticker-item">🔮 <span>Dario Amodei</span> predicts AGI as early as 2026-2027</span>
    <span class="ticker-item">📈 <span>Anthropic</span> valued at $40B after Series E</span>
    <span class="ticker-item">🚀 <span>MCP protocol</span> adopted by OpenAI, Google — 50,000+ integrations</span>
    <span class="ticker-item">🤖 <span>OpenAI</span> reaches 300M weekly active users — Q1 2026</span>
    <span class="ticker-item">🧠 <span>Claude 3.7 Sonnet</span> outperforms GPT-4o on 7/10 benchmarks</span>
    <span class="ticker-item">🇨🇳 <span>DeepSeek R2</span> trained for ~$2M — Nvidia drops 17%</span>
    <span class="ticker-item">🌟 <span>Gemma 3</span> hits 40M downloads in 30 days</span>
    <span class="ticker-item">⚡ <span>Gemini 2.0 Ultra</span> ships 1M token context window</span>
    <span class="ticker-item">🔮 <span>Dario Amodei</span> predicts AGI as early as 2026-2027</span>
    <span class="ticker-item">📈 <span>Anthropic</span> valued at $40B after Series E</span>
    <span class="ticker-item">🚀 <span>MCP protocol</span> adopted by OpenAI, Google — 50,000+ integrations</span>
  </div>
</div>

<header>
  <div class="header-inner">
    <div class="logo">
      <div class="logo-icon">⚡</div>
      <div>
        <div class="logo-title">AI PULSE</div>
        <div class="logo-subtitle">Intelligence Feed · 2026</div>
      </div>
    </div>
    <div class="header-meta">
      <div class="live-dot"></div>
      <span>LIVE</span>
      <span style="color:var(--border)">|</span>
      <span id="ct"></span>
      <span style="color:var(--border)">|</span>
      <span style="color:var(--accent)">ainews.anervea.ai</span>
    </div>
  </div>
</header>

<div class="hero">
  <div class="hero-eyebrow">// The Intelligence Report — April 2026</div>
  <h1 class="hero-title"><span class="l1">THE AI ARMS RACE</span><span class="l2">IS ACCELERATING</span></h1>
  <p class="hero-sub">From DeepSeek's $2M shock to Claude outperforming GPT-4o, Gemini's 1M context window, and China's AGI sprint — the most consequential technology race in human history, in real time.</p>
</div>

<div class="stats-bar"><div class="stats-grid" id="top-stats"></div></div>

<div class="tabs-section">
  <div class="tabs-nav">
    <button class="tab-btn active" onclick="switchTab('all')"><div class="tab-dot"></div> All Stories</button>
    <button class="tab-btn" onclick="switchTab('openai')"><div class="tab-dot"></div> 🤖 OpenAI</button>
    <button class="tab-btn" onclick="switchTab('claude')"><div class="tab-dot"></div> 🛡️ Claude</button>
    <button class="tab-btn" onclick="switchTab('gemini')"><div class="tab-dot"></div> ✨ Gemini</button>
    <button class="tab-btn" onclick="switchTab('china')"><div class="tab-dot"></div> 🇨🇳 China</button>
    <button class="tab-btn" onclick="switchTab('progress')"><div class="tab-dot"></div> 🚀 AI Progress</button>
    <button class="tab-btn" onclick="switchTab('agi')"><div class="tab-dot"></div> 🧠 AGI Future</button>
  </div>
</div>

<div class="content-area">
  <div class="tab-content active" id="tab-all">
    <div class="section-header"><div class="section-title">ALL STORIES</div><div class="section-count" id="all-count"></div></div>
    <div class="all-articles-grid" id="all-articles"></div>
  </div>
  <div class="tab-content" id="tab-openai">
    <div class="section-header"><div class="section-title">OPENAI INTELLIGENCE</div><div class="section-count">300M+ Weekly Users · $5B ARR</div></div>
    <div class="articles-grid" id="openai-featured"></div>
    <div class="stats-detail-grid" id="openai-stats"></div>
  </div>
  <div class="tab-content" id="tab-claude">
    <div class="section-header"><div class="section-title">CLAUDE & ANTHROPIC</div><div class="section-count">$40B Valuation · Safety-First AI</div></div>
    <div class="articles-grid" id="claude-featured"></div>
    <div class="stats-detail-grid" id="claude-stats"></div>
  </div>
  <div class="tab-content" id="tab-gemini">
    <div class="section-header"><div class="section-title">GEMINI & GEMMA</div><div class="section-count">1B Daily Interactions · 40M Downloads</div></div>
    <div class="articles-grid" id="gemini-featured"></div>
    <div class="stats-detail-grid" id="gemini-stats"></div>
  </div>
  <div class="tab-content" id="tab-china">
    <div class="section-header"><div class="section-title">CHINA'S AGI SPRINT</div><div class="section-count">$50B State Funding · DeepSeek Shock</div></div>
    <div class="articles-grid" id="china-featured"></div>
    <div class="stats-detail-grid" id="china-stats"></div>
  </div>
  <div class="tab-content" id="tab-progress">
    <div class="section-header"><div class="section-title">AI PROGRESS REPORT</div><div class="section-count">Agents · MCP · Infrastructure</div></div>
    <div class="articles-grid" id="progress-featured"></div>
    <div class="section-header" style="margin-top:48px"><div class="section-title">CAPABILITY TIMELINE</div></div>
    <div class="timeline">
      <div class="timeline-item"><div class="timeline-dot"></div><div class="timeline-year">2022</div><div class="timeline-event">ChatGPT Launch — Consumer AI Goes Mainstream</div><div class="timeline-desc">100M users in 60 days. The era of language model products begins.</div></div>
      <div class="timeline-item"><div class="timeline-dot" style="background:var(--accent2);box-shadow:0 0 12px var(--accent2)"></div><div class="timeline-year">2023</div><div class="timeline-event">GPT-4, Claude 2, Gemini — The Capability Explosion</div><div class="timeline-desc">Multimodal AI, 100K context, code generation surpasses humans on competitive programming.</div></div>
      <div class="timeline-item"><div class="timeline-dot" style="background:var(--accent3);box-shadow:0 0 12px var(--accent3)"></div><div class="timeline-year">2024</div><div class="timeline-event">Agents, Reasoning Models, Open Source Explosion</div><div class="timeline-desc">o1 and Claude 3.5 introduce inference-time reasoning. LLaMA 3 democratizes frontier AI.</div></div>
      <div class="timeline-item"><div class="timeline-dot" style="background:var(--gold);box-shadow:0 0 12px var(--gold)"></div><div class="timeline-year">2025</div><div class="timeline-event">DeepSeek Shock, Claude 3.7, Gemini 2.0</div><div class="timeline-desc">DeepSeek R1 redefines training economics. 1M context windows arrive. AI enters every enterprise workflow.</div></div>
      <div class="timeline-item"><div class="timeline-dot" style="background:var(--red);box-shadow:0 0 12px var(--red)"></div><div class="timeline-year">2026 →</div><div class="timeline-event">AGI Threshold? The Convergence Point</div><div class="timeline-desc">Leading researchers update timelines. Autonomous agents handle entire workflows. The capability gap narrows.</div></div>
    </div>
  </div>
  <div class="tab-content" id="tab-agi">
    <div class="section-header"><div class="section-title">AGI: IS IT THE FUTURE?</div><div class="section-count">Predictions from Top Scientists</div></div>
    <div class="articles-grid" id="agi-featured"></div>
    <div class="section-header" style="margin-top:48px"><div class="section-title">WHAT THE EXPERTS SAY</div><div class="section-count">6 Leading Voices</div></div>
    <div class="predictions-grid" id="preds"></div>
    <div style="background:var(--surface);border:1px solid rgba(251,191,36,.2);border-radius:24px;padding:40px;margin-top:20px">
      <div style="font-family:'Bebas Neue',sans-serif;font-size:28px;letter-spacing:2px;color:var(--gold);margin-bottom:20px">THE CONSENSUS VIEW</div>
      <p style="font-size:15px;line-height:1.8;color:rgba(240,244,255,.8);max-width:800px">The AI research community has reached an unusual moment of convergence: even skeptics are revising their timelines upward. The combination of scaling laws that haven't plateaued, inference-time compute as a second scaling dimension, and efficiency breakthroughs like DeepSeek's mixture-of-experts architecture suggests that AGI may arrive before most policymakers and institutions have prepared for it.</p>
      <div style="display:grid;grid-template-columns:repeat(3,1fr);gap:20px;margin-top:28px">
        <div style="text-align:center;padding:20px;background:rgba(255,255,255,.03);border-radius:12px;border:1px solid var(--border)"><div style="font-family:'Bebas Neue',sans-serif;font-size:40px;color:var(--accent)">73%</div><div style="font-size:12px;color:var(--muted);margin-top:4px">of surveyed AI researchers believe AGI arrives before 2035</div></div>
        <div style="text-align:center;padding:20px;background:rgba(255,255,255,.03);border-radius:12px;border:1px solid var(--border)"><div style="font-family:'Bebas Neue',sans-serif;font-size:40px;color:var(--accent2)">5-10</div><div style="font-size:12px;color:var(--muted);margin-top:4px">years: Yoshua Bengio's revised timeline estimate (2026)</div></div>
        <div style="text-align:center;padding:20px;background:rgba(255,255,255,.03);border-radius:12px;border:1px solid var(--border)"><div style="font-family:'Bebas Neue',sans-serif;font-size:40px;color:var(--accent3)">$1T+</div><div style="font-size:12px;color:var(--muted);margin-top:4px">projected global AI investment by 2027</div></div>
      </div>
    </div>
  </div>
</div>

<footer><div>⚡ <strong>AI Pulse</strong> — ainews.anervea.ai · Powered by Anervea</div><div>Data from public research &amp; benchmarks · Updated continuously</div></footer>

<div class="modal-overlay" id="moverlay" onclick="closeMO(event)">
  <div class="modal" id="modal">
    <button class="modal-close" onclick="closeM()">✕</button>
    <span class="modal-tag" id="mtag"></span>
    <div class="modal-title" id="mtitle"></div>
    <div class="modal-subtitle" id="msub"></div>
    <div class="modal-meta" id="mmeta"></div>
    <div class="modal-content" id="mcontent"></div>
    <div class="modal-tags" id="mtags"></div>
  </div>
</div>

<script>
const EMO={openai:'🤖',claude:'🛡️',gemini:'✨',china:'🇨🇳',progress:'🚀',agi:'🧠'};
const CLR={openai:'var(--accent)',claude:'var(--accent4)',gemini:'var(--accent3)',china:'var(--red)',progress:'var(--accent5)',agi:'var(--gold)'};
const CLS={openai:'tag-openai',claude:'tag-claude',gemini:'tag-gemini',china:'tag-china',progress:'tag-progress',agi:'tag-agi'};

setInterval(()=>{ document.getElementById('ct').textContent=new Date().toLocaleTimeString('en-US',{hour:'2-digit',minute:'2-digit',second:'2-digit'}); },1000);

async function init(){
  const [arts,stats,preds]=await Promise.all([
    fetch('/api/articles').then(r=>r.json()),
    fetch('/api/stats').then(r=>r.json()),
    fetch('/api/predictions').then(r=>r.json())
  ]);
  renderTopStats();
  renderAll(arts);
  ['openai','claude','gemini','china','progress','agi'].forEach(t=>{
    renderFeatured(t, arts.filter(a=>a.tab===t));
    renderTabStats(t, stats);
  });
  renderPreds(preds);
}

function renderTopStats(){
  const d=[{i:'👥',v:'300M+',l:'OpenAI Weekly Users',t:'+15% QoQ'},{i:'📈',v:'$40B',l:'Anthropic Valuation',t:'Series E'},{i:'🔥',v:'~$2M',l:'DeepSeek R2 Cost',t:'vs $100M GPT-4'},{i:'⬇️',v:'40M+',l:'Gemma 3 Downloads',t:'30-day record'}];
  document.getElementById('top-stats').innerHTML=d.map((s,i)=>`<div class="stat-card" style="animation-delay:${.7+i*.1}s"><div class="stat-icon">${s.i}</div><div class="stat-value">${s.v}</div><div class="stat-label">${s.l}</div><div class="stat-trend">↑ ${s.t}</div></div>`).join('');
}

function renderAll(arts){
  document.getElementById('all-count').textContent=`${arts.length} articles`;
  document.getElementById('all-articles').innerHTML=arts.map(a=>`
    <div class="article-card-medium" onclick="openA(${a.id})">
      <span class="card-emoji">${EMO[a.tab]||'📰'}</span>
      <div class="article-tag ${CLS[a.tab]||''}">${a.tab.toUpperCase()}</div>
      <div class="card-medium-title">${a.title}</div>
      <div class="card-medium-sub">${a.subtitle||''}</div>
      <div class="card-medium-footer"><span>${a.author||'Staff'}</span><span>${a.source||''}</span></div>
    </div>`).join('');
}

function renderFeatured(tab,arts){
  const el=document.getElementById(`${tab}-featured`);
  if(!el||!arts.length)return;
  const [f,...rest]=arts;
  el.innerHTML=`
    <div class="article-card-featured" onclick="openA(${f.id})">
      <div class="article-featured-header"><div class="article-tag ${CLS[tab]||''}">${EMO[tab]} ${tab.toUpperCase()}</div></div>
      <div class="article-featured-visual"><span class="vis-icon">${EMO[tab]||'📰'}</span></div>
      <div class="article-featured-body">
        <div class="article-title">${f.title}</div>
        <div class="article-subtitle">${f.subtitle||''}</div>
        <div class="article-meta"><span class="article-author">${f.author||'Staff'}</span><span>·</span><span>${f.source||''}</span></div>
      </div>
    </div>
    <div class="articles-sidebar">
      ${rest.map(a=>`<div class="article-card-small" onclick="openA(${a.id})"><div class="article-tag ${CLS[tab]||''}" style="font-size:9px;padding:3px 8px;margin-bottom:8px">${tab.toUpperCase()}</div><div class="small-title">${a.title}</div><div class="small-meta">${a.author||'Staff'} · ${a.source||''}</div></div>`).join('')}
    </div>`;
}

function renderTabStats(tab,all){
  const el=document.getElementById(`${tab}-stats`);
  if(!el)return;
  const s=all.filter(x=>x.category===tab);
  el.innerHTML=s.map(x=>`<div class="stat-card"><div class="stat-icon">${x.icon||'📊'}</div><div class="stat-value" style="color:${CLR[tab]||'var(--accent)'}">${x.value}</div><div class="stat-label">${x.label}</div><div class="stat-trend">${x.trend||''}</div></div>`).join('');
}

function renderPreds(preds){
  document.getElementById('preds').innerHTML=preds.map(p=>`
    <div class="prediction-card">
      <div class="pred-avatar">${p.avatar||'🧠'}</div>
      <div class="pred-name">${p.scientist}</div>
      <div class="pred-role">${p.role}</div>
      <div class="pred-quote">${p.quote}</div>
      <div class="pred-footer">
        <div class="pred-year">${p.year_prediction}</div>
        <div class="pred-conf"><div class="conf-bar"><div class="conf-fill" style="width:${p.confidence}%"></div></div><span>${p.confidence}%</span></div>
      </div>
    </div>`).join('');
}

async function openA(id){
  const a=await fetch(`/api/articles/${id}`).then(r=>r.json());
  document.getElementById('mtag').textContent=`${EMO[a.tab]||''} ${a.tab.toUpperCase()}`;
  document.getElementById('mtitle').textContent=a.title;
  document.getElementById('msub').textContent=a.subtitle||'';
  document.getElementById('mmeta').innerHTML=`<span>✍️ ${a.author||'Staff'}</span><span>📰 ${a.source||'AI Pulse'}</span><span>👁️ ${a.views} views</span>`;
  document.getElementById('mcontent').textContent=a.content;
  document.getElementById('mtags').innerHTML=(a.tags||[]).map(t=>`<span class="modal-tag-chip">#${t}</span>`).join('');
  document.getElementById('moverlay').classList.add('open');
  document.body.style.overflow='hidden';
}
function closeMO(e){if(e.target===document.getElementById('moverlay'))closeM();}
function closeM(){document.getElementById('moverlay').classList.remove('open');document.body.style.overflow='';}
document.addEventListener('keydown',e=>{if(e.key==='Escape')closeM();});

const TABS=['all','openai','claude','gemini','china','progress','agi'];
function switchTab(tab){
  document.querySelectorAll('.tab-content').forEach(e=>e.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(e=>e.classList.remove('active'));
  document.getElementById(`tab-${tab}`).classList.add('active');
  document.querySelectorAll('.tab-btn')[TABS.indexOf(tab)].classList.add('active');
  window.scrollTo({top:380,behavior:'smooth'});
}

init();
</script>
</body></html>
"""
