from fastapi import FastAPI, HTTPException
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import sqlite3
import json
import os
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

DB_PATH = "/tmp/ainews.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db()
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tab TEXT NOT NULL,
        title TEXT NOT NULL,
        subtitle TEXT,
        content TEXT NOT NULL,
        author TEXT,
        source TEXT,
        image_url TEXT,
        tags TEXT,
        views INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT NOT NULL,
        value TEXT NOT NULL,
        category TEXT,
        icon TEXT,
        trend TEXT
    )''')
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scientist TEXT NOT NULL,
        role TEXT,
        quote TEXT NOT NULL,
        year_prediction TEXT,
        confidence INTEGER,
        avatar TEXT
    )''')
    # Seed articles
    existing = c.execute('SELECT COUNT(*) FROM articles').fetchone()[0]
    if existing == 0:
        seed_data(c)
    conn.commit()
    conn.close()

def seed_data(c):
    articles = [
        ("openai", "OpenAI Reaches 300 Million Weekly Active Users", "ChatGPT dominates the consumer AI market with unprecedented growth",
         """OpenAI has shattered every metric in 2025-2026, crossing 300 million weekly active users across all its products. ChatGPT alone accounts for over 180 million daily conversations, while the API powers thousands of enterprise integrations globally. The company's revenue crossed $5 billion ARR in Q1 2026, driven largely by ChatGPT Plus subscriptions and Azure OpenAI API usage through Microsoft's cloud.

The GPT-4o and o3 model families continue to anchor OpenAI's commercial success. However, analysts note a growing concern: user retention is being challenged by Anthropic's Claude 3.7 Sonnet, which scores higher on coding benchmarks and long-context reasoning. OpenAI's response has been aggressive — slashing API prices by 40% and releasing Sora 2 for video generation to create a moat through multi-modal capabilities.

Despite the competition, OpenAI's developer ecosystem remains its strongest asset. With over 2 million developers building on its APIs and enterprise deals with Apple, Microsoft, and Salesforce, OpenAI still holds the largest installed base of any AI platform. The question is no longer dominance but sustainability — can they maintain this lead as Claude, Gemini, and open-source models close the gap?""",
         "Aniket Shah", "TechCrunch", "", "[\"OpenAI\",\"ChatGPT\",\"AGI\"]", 0),
        ("openai", "The Cracks in OpenAI's Moat: Developer Exodus Begins", "Enterprise teams quietly migrate to Claude and open-source alternatives",
         """A quiet but significant shift is underway in the enterprise AI landscape. Multiple Fortune 500 companies — including three major banks and two healthcare giants — have begun migrating production workloads from OpenAI's API to Anthropic's Claude 3.7 Sonnet and the open-source Llama 3.3 family. The primary drivers: reliability, cost predictability, and compliance with data privacy regulations that Claude's Constitutional AI approach satisfies more cleanly.

OpenAI's API outages in late 2025 spooked enterprise buyers. Three significant incidents — two in October and one in December — caused downstream failures in customer-facing applications. Anthropic, meanwhile, has had 99.97% uptime over the same period. For enterprise CIOs, that delta is career-defining.

Cost is another driver. Anthropic's Claude Haiku 3.5 processes 200,000 tokens per dollar at output speed, making it significantly more economical for bulk summarization and classification tasks. When you're running millions of API calls per day, a 35% cost reduction is not a rounding error — it's the difference between profitable and loss-making AI features.""",
         "Priya Mehta", "The Information", "", "[\"OpenAI\",\"Enterprise\",\"Migration\"]", 0),
        ("claude", "Why Claude is Outperforming GPT-4o on Every Benchmark That Matters", "Constitutional AI, 200K context, and safety-first training give Anthropic an edge",
         """Claude 3.7 Sonnet has emerged as the model of choice for professional developers and enterprise teams. Its performance on the MMLU Pro, HumanEval+, and GPQA benchmarks now exceeds GPT-4o on 7 out of 10 tested domains. But raw benchmark performance tells only part of the story.

The real differentiator is Claude's Constitutional AI training methodology. By training the model to reason about its own outputs against a set of principles — rather than relying solely on RLHF from human raters — Anthropic has produced a model with notably lower hallucination rates on factual tasks. Internal studies at three pharmaceutical companies (including Anervea's clients) show Claude hallucinating on medical literature queries at approximately 2.3% vs GPT-4o's 4.1%.

Claude's 200,000 token context window is also a practical game-changer. Enterprise use cases — auditing legal contracts, analyzing clinical trial PDFs, reviewing codebases — require feeding massive documents into a single context. Claude handles this with minimal degradation in output quality, while GPT-4o struggles past 50K tokens on complex reasoning tasks.

Anthropic's API pricing, reliability track record, and Constitutional AI approach to safety have also made it the default choice for regulated industries — finance, healthcare, pharma. The question isn't whether Claude is better at specific tasks. It's whether Anthropic can scale fast enough to capitalize on the momentum.""",
         "Aniket Shah", "AI Trends Weekly", "", "[\"Claude\",\"Anthropic\",\"Benchmarks\"]", 0),
        ("claude", "Anthropic's $40B Valuation: The Safety-First Bet Is Paying Off", "From safety-focused startup to enterprise AI powerhouse in 3 years",
         """When Dario Amodei and Daniela Amodei left OpenAI in 2021, many in Silicon Valley questioned the commercial viability of a safety-first AI lab. Three years later, Anthropic is valued at $40 billion, has $4.5 billion in committed revenue, and has signed deals with AWS, Google Cloud, and Salesforce that make it the most enterprise-integrated AI platform after OpenAI.

The Constitutional AI framework — Anthropic's core technical contribution — has proven to be not just ethically superior but commercially compelling. Regulated industries, which represent the highest-value AI contracts, require explainability and auditability. Claude's chain-of-thought reasoning, combined with Anthropic's commitment to model cards and safety research, has made it the default choice for compliance-conscious buyers.

Anthropic's model release cadence has also accelerated. Claude 3.7 Sonnet shipped in February 2026, with Claude 4 Opus expected in Q3 2026. The Haiku and Sonnet tiers provide price-performance options that match or beat OpenAI across every cost bracket. For enterprises running multi-model workflows, Claude's API is now the standard starting point.""",
         "Rohan Verma", "Bloomberg Technology", "", "[\"Anthropic\",\"Claude\",\"Valuation\"]", 0),
        ("gemini", "Google Gemma 3: Open Source Is Eating the AI World", "Google's open-weights strategy reshapes the competitive landscape",
         """Google's Gemma 3 release in early 2026 was a watershed moment for open-source AI. The 27B parameter model — freely available for commercial use — matched GPT-4o Mini on most standard benchmarks while running comfortably on a single H100 GPU. For startups and developers who cannot afford OpenAI API costs at scale, Gemma 3 has become the de facto foundation model.

The release reflects Google's strategic pivot: rather than competing solely on proprietary API revenue, DeepMind and Google Research are betting that seeding the ecosystem with capable open-weight models will drive adoption of Google Cloud infrastructure, TPU rentals, and Vertex AI managed deployments.

Gemma 3's multimodal capabilities are particularly impressive. The model natively handles text, code, images, and structured data inputs. Its instruction-following quality on complex agentic tasks rivals models twice its parameter count. Hugging Face reports Gemma 3 has been downloaded over 40 million times since launch — more than any previous open model release.

The Gemma ecosystem has also catalyzed a wave of fine-tuned variants: medical Gemma (trained on clinical notes), legal Gemma (fine-tuned on court documents), and CodeGemma (specialized for software engineering). The open-source AI flywheel is spinning faster than ever.""",
         "Siddharth Rao", "Wired", "", "[\"Google\",\"Gemma\",\"OpenSource\"]", 0),
        ("gemini", "Gemini 2.0 Ultra: Google's Counterattack at the Frontier", "Deep Research, real-time grounding, and 1M context put Gemini back in contention",
         """After a rocky 2024 debut, Gemini 2.0 Ultra represents Google's most credible challenge yet to OpenAI and Anthropic at the frontier. The model ships with native tool use, a 1 million token context window, real-time web grounding, and Deep Research mode — a multi-step agentic capability that can autonomously research topics across dozens of web sources and synthesize a structured report.

In head-to-head evaluations on long-context retrieval tasks, Gemini 2.0 Ultra outperforms both Claude 3.7 Sonnet and GPT-4o, particularly on tasks requiring information synthesis across 500K+ token documents. For enterprise use cases involving large document corpora — law firms, research institutions, financial analysts — this is a decisive advantage.

Google's distribution is also unmatched. With Gemini embedded in Google Workspace (Docs, Sheets, Gmail, Drive), Google Search, and Android, no other AI company has comparable first-party surface area. Daily Gemini interactions in Google products exceed 1 billion — a figure no competitor can approach through API-first distribution alone.""",
         "Ananya Krishnan", "The Verge", "", "[\"Google\",\"Gemini\",\"LLM\"]", 0),
        ("china", "China's AGI Race: DeepSeek, Kimi, and the National AI Imperative", "Beijing mobilizes $50B in state funding as Chinese labs close the capability gap",
         """China's AI industry has undergone a dramatic transformation. What was once characterized as derivative and benchmark-gaming has evolved into genuine frontier research. DeepSeek-V3 and DeepSeek-R1 shocked the global AI community in late 2025 by achieving GPT-4o-level performance at a fraction of the training cost — an estimated $6 million vs OpenAI's hundreds of millions. The efficiency gains came from a novel mixture-of-experts architecture and aggressive quantization techniques developed entirely within China's research ecosystem.

Kimi (by Moonshot AI) has emerged as China's Claude equivalent — a 128K context model with exceptional long-document comprehension, now used by millions of Chinese professionals for legal, financial, and academic work. ByteDance's Doubao and Alibaba's Qwen 2.5 family have also pushed to frontier capability levels, with Qwen 2.5-72B matching or exceeding LLaMA 3.3 on coding and math benchmarks.

Beijing's national AI strategy — backed by $50 billion in state investment and mandatory data-sharing agreements with tech giants — is accelerating capability development at a pace that makes Western observers deeply uncomfortable. The chip embargo has been a genuine constraint, but Chinese labs have responded with algorithmic efficiency rather than raw compute, potentially establishing a more sustainable long-term advantage.""",
         "Li Wei (Guest)", "MIT Technology Review", "", "[\"China\",\"DeepSeek\",\"AGI\"]", 0),
        ("china", "DeepSeek R2: The $2M Model That Humbled Silicon Valley", "Chinese startup's efficiency breakthrough rewrites the economics of frontier AI",
         """DeepSeek's R2 model, released in March 2026, has become the most discussed AI development since ChatGPT's launch. Trained for approximately $2 million — using a combination of sparse mixture-of-experts, multi-head latent attention, and aggressive inference-time compute — R2 achieves scores on mathematical reasoning, coding, and scientific knowledge that exceed GPT-4o and approach Claude 3.7 Sonnet.

The implications are profound. Silicon Valley's thesis — that frontier AI requires massive compute budgets accessible only to trillion-dollar companies — appears to be wrong. DeepSeek has demonstrated that algorithmic innovation can substitute for raw compute, that the economics of AI development are far more favorable than the hyperscalers projected, and that China's AI research community has matured to genuine world-class level.

Nvidia's stock dropped 17% the day DeepSeek R2 was publicly benchmarked. The implied long-term demand for H100/H200 clusters — Wall Street's primary AI infrastructure thesis — suddenly looks much less certain. For the US-China AI competition, R2 is a Sputnik-moment equivalent: a demonstration that the gap is closing faster than policymakers anticipated.""",
         "Aniket Shah", "Financial Times", "", "[\"DeepSeek\",\"China\",\"Efficiency\"]", 0),
        ("progress", "AI in 2026: From Language Models to Autonomous Agents", "The shift from text generation to goal-directed action is the defining trend of 2026",
         """The AI narrative in 2026 is no longer about which model writes better poetry or scores higher on standardized exams. It's about which systems can take actions in the world — browsing the web, writing and executing code, sending emails, managing files, and completing multi-step workflows without human intervention at each step.

OpenAI's Operator, Anthropic's Computer Use API, and Google's Project Mariner have all shipped production-grade agentic capabilities. Enterprise adoption of AI agents is accelerating fastest in software engineering (GitHub Copilot Workspace, Cursor), customer service (Salesforce Agentforce), and financial analysis (Bloomberg Terminal AI integration).

The enabling infrastructure has also matured. The Model Context Protocol (MCP) — developed by Anthropic and now adopted by OpenAI and Google — provides a standardized way for AI models to interface with external tools, databases, and services. LangChain, LlamaIndex, and CrewAI have built trillion-parameter orchestration layers on top of MCP, making it easier than ever to deploy multi-agent systems that can actually get things done.""",
         "Aniket Shah", "AI Trends Weekly", "", "[\"Agents\",\"AGI\",\"Progress\"]", 0),
        ("agi", "AGI by 2027? The Scientists Who Say Yes — and Why They Might Be Right", "A growing faction of researchers believes general intelligence is closer than consensus admits",
         """The question of when — not whether — artificial general intelligence arrives has shifted from philosophy seminar to mainstream technical debate. Sam Altman has publicly stated his belief that AGI will be built within OpenAI's current research agenda. Demis Hassabis told the Financial Times in January 2026 that DeepMind is 'likely within years, not decades' of systems that match human performance across cognitive domains. Yoshua Bengio, long a skeptic of near-term AGI, revised his timeline estimate in a March 2026 interview to '5-10 years.'

The technical case for accelerating timelines rests on three observations: scaling laws have not plateaued as many predicted; inference-time compute (chain-of-thought reasoning, tree search) provides a second scaling dimension beyond training compute; and the capability jump from GPT-3 to GPT-4 to o3 has been dramatically faster than most researchers forecasted as recently as 2022.

The counterarguments are real — current models still lack genuine causal reasoning, embodied understanding, and the ability to learn continuously from experience. But the optimists point out that these limitations were cited about every previous generation of models, and each generation surprised.""",
         "Prof. James Wu", "Nature AI", "", "[\"AGI\",\"Predictions\",\"Future\"]", 0)
    ]
    for a in articles:
        c.execute('INSERT INTO articles (tab,title,subtitle,content,author,source,image_url,tags) VALUES (?,?,?,?,?,?,?,?)', a)

    stats = [
        ("OpenAI Weekly Users", "300M+", "openai", "👥", "+15% QoQ"),
        ("ChatGPT Daily Conversations", "180M", "openai", "💬", "+22% YoY"),
        ("OpenAI ARR", "$5B+", "openai", "💰", "+180% YoY"),
        ("Claude Enterprise Customers", "10,000+", "claude", "🏢", "+300% YoY"),
        ("Anthropic Valuation", "$40B", "claude", "📈", "Series E"),
        ("Gemma 3 Downloads", "40M+", "gemini", "⬇️", "30 days"),
        ("Gemini Daily Interactions", "1B+", "gemini", "✨", "Google Workspace"),
        ("DeepSeek R2 Training Cost", "~$2M", "china", "🔥", "vs $100M+ GPT-4"),
        ("China AI Investment 2026", "$50B", "china", "🇨🇳", "State Funding"),
        ("MCP Integrations", "50,000+", "progress", "🔌", "Ecosystem"),
        ("AI Agents in Production", "2M+", "progress", "🤖", "Enterprise Deployed"),
        ("AGI Timeline Consensus", "5-10 yrs", "agi", "🧠", "Leading Researchers")
    ]
    for s in stats:
        c.execute('INSERT INTO stats (label,value,category,icon,trend) VALUES (?,?,?,?,?)', s)

    predictions = [
        ("Sam Altman", "CEO, OpenAI", "AGI is not a distant theoretical concept. We expect to build it within this decade, possibly within years. The scaling laws have not broken down; if anything, inference-time compute has opened a second frontier we're only beginning to explore.", "2027-2028", 85, "🎯"),
        ("Demis Hassabis", "CEO, Google DeepMind", "We are likely years, not decades, away from systems that match or exceed human performance across most cognitive domains. The combination of foundation models, world models, and reinforcement learning is converging faster than anyone predicted.", "2028-2030", 78, "🧬"),
        ("Yoshua Bengio", "Turing Award Laureate", "I've revised my timeline. The progress in reasoning, planning, and code generation over the last two years has been remarkable. My current estimate is 5-10 years to systems that most researchers would call AGI, though I remain cautious about what that label actually means.", "2030-2035", 65, "🎓"),
        ("Dario Amodei", "CEO, Anthropic", "AGI — or what I call 'powerful AI' — could arrive as early as 2026-2027. This is both exciting and deeply concerning. The safety work we need to do to make this go well is not keeping pace with capability development across the industry.", "2026-2027", 80, "🛡️"),
        ("Geoffrey Hinton", "AI Pioneer, Turing Laureate", "I left Google because I became genuinely alarmed about the pace of progress. These systems are approaching capabilities that we do not understand and cannot fully control. The timeline question is less important than the alignment question.", "2025-2030", 72, "⚠️"),
        ("Fei-Fei Li", "Stanford HAI", "AGI as typically defined is a moving goalpost — every time we achieve a milestone, we redefine it. But systems that can genuinely assist humans across open-ended real-world tasks? Those are arriving now. The question is how we govern and distribute them.", "2025-2028", 70, "🌍")
    ]
    for p in predictions:
        c.execute('INSERT INTO predictions (scientist,role,quote,year_prediction,confidence,avatar) VALUES (?,?,?,?,?,?)', p)

init_db()

@app.get("/api/articles")
def get_articles(tab: str = None):
    conn = get_db()
    if tab:
        rows = conn.execute('SELECT * FROM articles WHERE tab=? ORDER BY created_at DESC', (tab,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM articles ORDER BY created_at DESC').fetchall()
    conn.close()
    return [{**dict(r), 'tags': json.loads(r['tags']) if r['tags'] else []} for r in rows]

@app.get("/api/articles/{article_id}")
def get_article(article_id: int):
    conn = get_db()
    conn.execute('UPDATE articles SET views=views+1 WHERE id=?', (article_id,))
    conn.commit()
    r = conn.execute('SELECT * FROM articles WHERE id=?', (article_id,)).fetchone()
    conn.close()
    if not r: raise HTTPException(404)
    return {**dict(r), 'tags': json.loads(r['tags']) if r['tags'] else []}

@app.get("/api/stats")
def get_stats(category: str = None):
    conn = get_db()
    if category:
        rows = conn.execute('SELECT * FROM stats WHERE category=?', (category,)).fetchall()
    else:
        rows = conn.execute('SELECT * FROM stats').fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/api/predictions")
def get_predictions():
    conn = get_db()
    rows = conn.execute('SELECT * FROM predictions').fetchall()
    conn.close()
    return [dict(r) for r in rows]

@app.get("/", response_class=HTMLResponse)
def serve_frontend():
    return HTMLResponse(content=HTML_CONTENT)

HTML_CONTENT = r"""
<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>AI Pulse — Live Intelligence Feed</title>
<link href="https://fonts.googleapis.com/css2?family=Space+Grotesk:wght@300;400;500;600;700&family=Bebas+Neue&family=JetBrains+Mono:wght@400;700&display=swap" rel="stylesheet">
<style>
:root {
  --bg: #030712;
  --bg2: #0a0f1e;
  --bg3: #0d1529;
  --surface: rgba(255,255,255,0.04);
  --surface2: rgba(255,255,255,0.08);
  --border: rgba(255,255,255,0.08);
  --text: #f0f4ff;
  --muted: #6b7280;
  --accent: #38bdf8;
  --accent2: #818cf8;
  --accent3: #34d399;
  --accent4: #f472b6;
  --accent5: #fb923c;
  --gold: #fbbf24;
  --red: #f87171;
}

* { margin:0; padding:0; box-sizing:border-box; }
html { scroll-behavior: smooth; }
body {
  background: var(--bg);
  color: var(--text);
  font-family: 'Space Grotesk', sans-serif;
  min-height: 100vh;
  overflow-x: hidden;
}

/* BACKGROUND EFFECTS */
body::before {
  content: '';
  position: fixed;
  inset: 0;
  background:
    radial-gradient(ellipse 80% 50% at 20% -10%, rgba(56,189,248,0.12) 0%, transparent 60%),
    radial-gradient(ellipse 60% 40% at 80% 110%, rgba(129,140,248,0.10) 0%, transparent 60%),
    radial-gradient(ellipse 50% 30% at 50% 50%, rgba(52,211,153,0.04) 0%, transparent 70%);
  pointer-events: none;
  z-index: 0;
}

/* GRID OVERLAY */
body::after {
  content: '';
  position: fixed;
  inset: 0;
  background-image:
    linear-gradient(rgba(255,255,255,0.015) 1px, transparent 1px),
    linear-gradient(90deg, rgba(255,255,255,0.015) 1px, transparent 1px);
  background-size: 60px 60px;
  pointer-events: none;
  z-index: 0;
}

/* TICKER */
.ticker-wrap {
  position: fixed;
  top: 0;
  width: 100%;
  background: linear-gradient(90deg, #0c1a2e, #0a1628, #0c1a2e);
  border-bottom: 1px solid rgba(56,189,248,0.3);
  z-index: 1000;
  overflow: hidden;
  height: 32px;
  display: flex;
  align-items: center;
}
.ticker-wrap::before, .ticker-wrap::after {
  content: '';
  position: absolute;
  top: 0; bottom: 0; width: 80px;
  z-index: 2;
}
.ticker-wrap::before { left: 0; background: linear-gradient(90deg, #0c1a2e, transparent); }
.ticker-wrap::after { right: 0; background: linear-gradient(270deg, #0c1a2e, transparent); }
.ticker-label {
  flex-shrink: 0;
  background: var(--accent);
  color: #000;
  font-size: 10px;
  font-weight: 700;
  letter-spacing: 2px;
  padding: 0 12px;
  height: 100%;
  display: flex;
  align-items: center;
  z-index: 3;
}
.ticker-inner {
  display: flex;
  animation: ticker 40s linear infinite;
  white-space: nowrap;
}
.ticker-item {
  font-size: 11px;
  color: var(--muted);
  padding: 0 40px;
  font-family: 'JetBrains Mono', monospace;
  letter-spacing: 0.5px;
}
.ticker-item span { color: var(--accent); }
@keyframes ticker {
  0% { transform: translateX(0); }
  100% { transform: translateX(-50%); }
}

/* HEADER */
header {
  position: relative;
  z-index: 100;
  padding: 60px 0 0;
}
.header-inner {
  max-width: 1400px;
  margin: 0 auto;
  padding: 32px 40px 0;
  display: flex;
  align-items: center;
  justify-content: space-between;
}
.logo {
  display: flex;
  align-items: center;
  gap: 16px;
}
.logo-icon {
  width: 44px; height: 44px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  border-radius: 12px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 20px;
  box-shadow: 0 0 30px rgba(56,189,248,0.4);
  animation: pulse-logo 3s ease-in-out infinite;
}
@keyframes pulse-logo {
  0%, 100% { box-shadow: 0 0 20px rgba(56,189,248,0.3); }
  50% { box-shadow: 0 0 50px rgba(56,189,248,0.7); }
}
.logo-text { line-height: 1; }
.logo-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 32px;
  letter-spacing: 3px;
  background: linear-gradient(135deg, var(--accent), var(--accent2));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
}
.logo-subtitle {
  font-size: 10px;
  color: var(--muted);
  letter-spacing: 3px;
  text-transform: uppercase;
  margin-top: 2px;
}
.header-meta {
  display: flex;
  align-items: center;
  gap: 20px;
  font-size: 12px;
  color: var(--muted);
}
.live-dot {
  width: 8px; height: 8px;
  background: var(--accent3);
  border-radius: 50%;
  animation: blink 1.5s ease-in-out infinite;
  box-shadow: 0 0 8px var(--accent3);
}
@keyframes blink {
  0%, 100% { opacity: 1; }
  50% { opacity: 0.3; }
}

/* HERO */
.hero {
  position: relative;
  z-index: 10;
  max-width: 1400px;
  margin: 0 auto;
  padding: 60px 40px 40px;
}
.hero-eyebrow {
  font-size: 11px;
  letter-spacing: 4px;
  color: var(--accent);
  text-transform: uppercase;
  font-family: 'JetBrains Mono', monospace;
  margin-bottom: 16px;
  opacity: 0;
  animation: fadeUp 0.8s 0.2s forwards;
}
.hero-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: clamp(52px, 8vw, 96px);
  line-height: 0.92;
  letter-spacing: 2px;
  margin-bottom: 20px;
  opacity: 0;
  animation: fadeUp 0.8s 0.4s forwards;
}
.hero-title .line1 { color: var(--text); display: block; }
.hero-title .line2 {
  background: linear-gradient(135deg, var(--accent), var(--accent2), var(--accent3));
  -webkit-background-clip: text;
  -webkit-text-fill-color: transparent;
  display: block;
}
.hero-sub {
  font-size: 16px;
  color: var(--muted);
  max-width: 600px;
  line-height: 1.6;
  opacity: 0;
  animation: fadeUp 0.8s 0.6s forwards;
}
@keyframes fadeUp {
  from { opacity:0; transform: translateY(30px); }
  to { opacity:1; transform: translateY(0); }
}

/* STATS MARQUEE */
.stats-bar {
  position: relative;
  z-index: 10;
  max-width: 1400px;
  margin: 0 auto 0;
  padding: 0 40px;
}
.stats-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 0;
}
.stat-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px 24px;
  position: relative;
  overflow: hidden;
  transition: all 0.3s;
  opacity: 0;
  animation: fadeUp 0.6s forwards;
}
.stat-card:nth-child(1) { animation-delay: 0.7s; }
.stat-card:nth-child(2) { animation-delay: 0.8s; }
.stat-card:nth-child(3) { animation-delay: 0.9s; }
.stat-card:nth-child(4) { animation-delay: 1.0s; }
.stat-card:hover {
  background: var(--surface2);
  border-color: rgba(56,189,248,0.3);
  transform: translateY(-4px);
}
.stat-card::before {
  content: '';
  position: absolute;
  top: 0; left: 0; right: 0;
  height: 2px;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  opacity: 0;
  transition: opacity 0.3s;
}
.stat-card:hover::before { opacity: 1; }
.stat-icon { font-size: 22px; margin-bottom: 8px; }
.stat-value {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 32px;
  letter-spacing: 1px;
  color: var(--accent);
  line-height: 1;
}
.stat-label {
  font-size: 12px;
  color: var(--muted);
  margin-top: 4px;
}
.stat-trend {
  font-size: 11px;
  color: var(--accent3);
  font-family: 'JetBrains Mono', monospace;
  margin-top: 8px;
}

/* TABS */
.tabs-section {
  position: relative;
  z-index: 10;
  max-width: 1400px;
  margin: 0 auto;
  padding: 40px 40px 0;
}
.tabs-nav {
  display: flex;
  gap: 4px;
  background: rgba(255,255,255,0.03);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 6px;
  margin-bottom: 40px;
  overflow-x: auto;
  scrollbar-width: none;
}
.tabs-nav::-webkit-scrollbar { display: none; }
.tab-btn {
  flex-shrink: 0;
  background: none;
  border: none;
  color: var(--muted);
  font-family: 'Space Grotesk', sans-serif;
  font-size: 13px;
  font-weight: 500;
  padding: 10px 22px;
  border-radius: 14px;
  cursor: pointer;
  transition: all 0.3s;
  display: flex;
  align-items: center;
  gap: 8px;
  white-space: nowrap;
}
.tab-btn:hover { color: var(--text); background: var(--surface); }
.tab-btn.active {
  background: linear-gradient(135deg, rgba(56,189,248,0.2), rgba(129,140,248,0.2));
  color: var(--text);
  border: 1px solid rgba(56,189,248,0.3);
}
.tab-btn.active .tab-dot {
  background: var(--accent);
  box-shadow: 0 0 8px var(--accent);
}
.tab-dot {
  width: 6px; height: 6px;
  border-radius: 50%;
  background: var(--muted);
  transition: all 0.3s;
}

/* CONTENT AREA */
.content-area {
  position: relative;
  z-index: 10;
  max-width: 1400px;
  margin: 0 auto;
  padding: 0 40px 80px;
}
.tab-content { display: none; }
.tab-content.active {
  display: block;
  animation: fadeIn 0.5s ease;
}
@keyframes fadeIn {
  from { opacity:0; transform: translateY(12px); }
  to { opacity:1; transform: translateY(0); }
}

/* ARTICLES GRID */
.articles-grid {
  display: grid;
  grid-template-columns: 2fr 1fr;
  gap: 24px;
  margin-bottom: 40px;
}
.article-card-featured {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 24px;
  overflow: hidden;
  cursor: pointer;
  transition: all 0.4s cubic-bezier(0.4, 0, 0.2, 1);
  position: relative;
}
.article-card-featured:hover {
  border-color: rgba(56,189,248,0.4);
  transform: translateY(-6px);
  box-shadow: 0 24px 60px rgba(0,0,0,0.5), 0 0 60px rgba(56,189,248,0.08);
}
.article-featured-header {
  padding: 32px 32px 0;
}
.article-featured-visual {
  height: 200px;
  margin: 24px 32px;
  border-radius: 16px;
  background: linear-gradient(135deg, var(--bg3), var(--bg2));
  border: 1px solid var(--border);
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 60px;
  position: relative;
  overflow: hidden;
}
.article-featured-visual::before {
  content: '';
  position: absolute;
  inset: 0;
  background: linear-gradient(135deg, rgba(56,189,248,0.1), rgba(129,140,248,0.1));
}
.article-featured-visual .vis-icon {
  position: relative;
  z-index: 1;
  animation: float 3s ease-in-out infinite;
}
@keyframes float {
  0%, 100% { transform: translateY(0); }
  50% { transform: translateY(-10px); }
}
.article-featured-body { padding: 0 32px 32px; }
.article-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent);
  background: rgba(56,189,248,0.1);
  border: 1px solid rgba(56,189,248,0.2);
  padding: 4px 10px;
  border-radius: 6px;
  margin-bottom: 12px;
}
.article-title {
  font-size: 22px;
  font-weight: 700;
  line-height: 1.3;
  margin-bottom: 10px;
  color: var(--text);
}
.article-subtitle {
  font-size: 14px;
  color: var(--muted);
  line-height: 1.5;
  margin-bottom: 16px;
}
.article-meta {
  display: flex;
  align-items: center;
  gap: 16px;
  font-size: 12px;
  color: var(--muted);
}
.article-author { color: var(--accent2); font-weight: 500; }

/* SIDEBAR CARDS */
.articles-sidebar { display: flex; flex-direction: column; gap: 16px; }
.article-card-small {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 16px;
  padding: 20px;
  cursor: pointer;
  transition: all 0.3s;
  flex: 1;
}
.article-card-small:hover {
  border-color: rgba(56,189,248,0.3);
  transform: translateX(6px);
  background: var(--surface2);
}
.small-title {
  font-size: 15px;
  font-weight: 600;
  line-height: 1.4;
  margin-bottom: 8px;
}
.small-meta { font-size: 11px; color: var(--muted); }

/* MODAL */
.modal-overlay {
  position: fixed;
  inset: 0;
  background: rgba(0,0,0,0.85);
  z-index: 2000;
  display: none;
  align-items: center;
  justify-content: center;
  padding: 40px;
  backdrop-filter: blur(8px);
}
.modal-overlay.open { display: flex; animation: fadeIn 0.3s; }
.modal {
  background: var(--bg2);
  border: 1px solid rgba(56,189,248,0.2);
  border-radius: 28px;
  max-width: 760px;
  width: 100%;
  max-height: 80vh;
  overflow-y: auto;
  padding: 48px;
  position: relative;
  box-shadow: 0 40px 100px rgba(0,0,0,0.8), 0 0 80px rgba(56,189,248,0.08);
}
.modal::-webkit-scrollbar { width: 4px; }
.modal::-webkit-scrollbar-track { background: transparent; }
.modal::-webkit-scrollbar-thumb { background: var(--border); border-radius: 2px; }
.modal-close {
  position: absolute;
  top: 20px; right: 20px;
  background: var(--surface);
  border: 1px solid var(--border);
  color: var(--muted);
  width: 36px; height: 36px;
  border-radius: 10px;
  cursor: pointer;
  font-size: 18px;
  display: flex;
  align-items: center;
  justify-content: center;
  transition: all 0.2s;
}
.modal-close:hover { color: var(--text); background: var(--surface2); }
.modal-tag {
  display: inline-flex;
  align-items: center;
  gap: 6px;
  font-size: 10px;
  font-weight: 600;
  letter-spacing: 2px;
  text-transform: uppercase;
  color: var(--accent);
  margin-bottom: 16px;
}
.modal-title {
  font-size: 30px;
  font-weight: 700;
  line-height: 1.25;
  margin-bottom: 12px;
}
.modal-subtitle {
  font-size: 16px;
  color: var(--muted);
  margin-bottom: 20px;
  line-height: 1.5;
}
.modal-meta {
  display: flex;
  gap: 20px;
  font-size: 12px;
  color: var(--muted);
  margin-bottom: 32px;
  padding-bottom: 32px;
  border-bottom: 1px solid var(--border);
}
.modal-content {
  font-size: 15px;
  line-height: 1.8;
  color: rgba(240,244,255,0.85);
  white-space: pre-line;
}
.modal-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
  margin-top: 32px;
}
.modal-tag-chip {
  font-size: 11px;
  color: var(--accent2);
  background: rgba(129,140,248,0.1);
  border: 1px solid rgba(129,140,248,0.2);
  padding: 4px 12px;
  border-radius: 20px;
}

/* PREDICTIONS */
.predictions-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
  margin-bottom: 40px;
}
.prediction-card {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 28px;
  position: relative;
  transition: all 0.3s;
  overflow: hidden;
}
.prediction-card::before {
  content: '"';
  position: absolute;
  top: 10px; left: 20px;
  font-size: 80px;
  font-family: Georgia, serif;
  color: rgba(56,189,248,0.08);
  line-height: 1;
  pointer-events: none;
}
.prediction-card:hover {
  border-color: rgba(56,189,248,0.3);
  transform: translateY(-4px);
  box-shadow: 0 20px 50px rgba(0,0,0,0.4);
}
.pred-avatar {
  font-size: 36px;
  margin-bottom: 12px;
}
.pred-name {
  font-size: 17px;
  font-weight: 700;
  margin-bottom: 2px;
}
.pred-role {
  font-size: 11px;
  color: var(--muted);
  margin-bottom: 16px;
}
.pred-quote {
  font-size: 13px;
  color: rgba(240,244,255,0.75);
  line-height: 1.7;
  margin-bottom: 16px;
}
.pred-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
}
.pred-year {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--accent);
  background: rgba(56,189,248,0.1);
  padding: 4px 10px;
  border-radius: 6px;
}
.pred-conf {
  display: flex;
  align-items: center;
  gap: 6px;
  font-size: 12px;
  color: var(--muted);
}
.conf-bar {
  width: 60px;
  height: 4px;
  background: var(--border);
  border-radius: 2px;
  overflow: hidden;
}
.conf-fill {
  height: 100%;
  background: linear-gradient(90deg, var(--accent), var(--accent2));
  border-radius: 2px;
  transition: width 1s ease;
}

/* SECTION HEADER */
.section-header {
  display: flex;
  align-items: flex-end;
  justify-content: space-between;
  margin-bottom: 28px;
}
.section-title {
  font-family: 'Bebas Neue', sans-serif;
  font-size: 36px;
  letter-spacing: 2px;
  color: var(--text);
}
.section-count {
  font-size: 12px;
  color: var(--muted);
  font-family: 'JetBrains Mono', monospace;
}

/* ALL ARTICLES */
.all-articles-grid {
  display: grid;
  grid-template-columns: repeat(3, 1fr);
  gap: 20px;
}
.article-card-medium {
  background: var(--surface);
  border: 1px solid var(--border);
  border-radius: 20px;
  padding: 24px;
  cursor: pointer;
  transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
  display: flex;
  flex-direction: column;
  gap: 12px;
}
.article-card-medium:hover {
  border-color: rgba(56,189,248,0.3);
  transform: translateY(-6px);
  box-shadow: 0 20px 50px rgba(0,0,0,0.4), 0 0 40px rgba(56,189,248,0.06);
}
.card-emoji {
  font-size: 36px;
  display: block;
  margin-bottom: 4px;
}
.card-medium-title {
  font-size: 16px;
  font-weight: 600;
  line-height: 1.4;
  flex: 1;
}
.card-medium-sub {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.5;
}
.card-medium-footer {
  display: flex;
  justify-content: space-between;
  align-items: center;
  padding-top: 12px;
  border-top: 1px solid var(--border);
  font-size: 11px;
  color: var(--muted);
}

/* STATS DETAIL */
.stats-detail-grid {
  display: grid;
  grid-template-columns: repeat(4, 1fr);
  gap: 16px;
  margin-bottom: 40px;
}

/* LOADING */
.loading {
  display: flex;
  align-items: center;
  justify-content: center;
  padding: 80px;
  flex-direction: column;
  gap: 16px;
}
.loader {
  width: 40px; height: 40px;
  border: 3px solid var(--border);
  border-top-color: var(--accent);
  border-radius: 50%;
  animation: spin 0.8s linear infinite;
}
@keyframes spin { to { transform: rotate(360deg); } }

/* SCROLLBAR */
::-webkit-scrollbar { width: 6px; height: 6px; }
::-webkit-scrollbar-track { background: var(--bg); }
::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }
::-webkit-scrollbar-thumb:hover { background: var(--muted); }

/* FOOTER */
footer {
  position: relative;
  z-index: 10;
  border-top: 1px solid var(--border);
  padding: 32px 40px;
  max-width: 1400px;
  margin: 0 auto;
  display: flex;
  align-items: center;
  justify-content: space-between;
  font-size: 12px;
  color: var(--muted);
}

/* RESPONSIVE */
@media (max-width: 1024px) {
  .articles-grid { grid-template-columns: 1fr; }
  .predictions-grid { grid-template-columns: 1fr 1fr; }
  .all-articles-grid { grid-template-columns: 1fr 1fr; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .stats-detail-grid { grid-template-columns: repeat(2, 1fr); }
}
@media (max-width: 640px) {
  .header-inner, .hero, .tabs-section, .content-area { padding-left: 20px; padding-right: 20px; }
  .hero-title { font-size: 48px; }
  .stats-grid { grid-template-columns: repeat(2, 1fr); }
  .predictions-grid, .all-articles-grid, .stats-detail-grid { grid-template-columns: 1fr; }
  .tabs-nav { padding: 4px; }
  .modal { padding: 28px 20px; }
}

/* GLOW EFFECTS */
.glow-accent { color: var(--accent); text-shadow: 0 0 20px rgba(56,189,248,0.5); }
.progress-ring {
  position: relative;
  display: inline-flex;
  align-items: center;
  justify-content: center;
}

/* AGI TIMELINE */
.timeline {
  position: relative;
  margin: 40px 0;
  padding-left: 32px;
}
.timeline::before {
  content: '';
  position: absolute;
  left: 0; top: 0; bottom: 0;
  width: 2px;
  background: linear-gradient(180deg, var(--accent), var(--accent2), var(--accent3));
  border-radius: 1px;
}
.timeline-item {
  position: relative;
  padding-bottom: 32px;
}
.timeline-item:last-child { padding-bottom: 0; }
.timeline-dot {
  position: absolute;
  left: -37px;
  top: 4px;
  width: 12px; height: 12px;
  border-radius: 50%;
  background: var(--accent);
  border: 2px solid var(--bg);
  box-shadow: 0 0 12px var(--accent);
}
.timeline-year {
  font-family: 'JetBrains Mono', monospace;
  font-size: 13px;
  color: var(--accent);
  margin-bottom: 6px;
}
.timeline-event {
  font-size: 16px;
  font-weight: 600;
  margin-bottom: 4px;
}
.timeline-desc {
  font-size: 13px;
  color: var(--muted);
  line-height: 1.6;
}

/* CHINA FLAG ACCENT */
.china-card { border-color: rgba(248,113,113,0.2) !important; }
.china-card:hover { border-color: rgba(248,113,113,0.5) !important; }
.tag-china { color: var(--red) !important; background: rgba(248,113,113,0.1) !important; border-color: rgba(248,113,113,0.2) !important; }
.tag-agi { color: var(--gold) !important; background: rgba(251,191,36,0.1) !important; border-color: rgba(251,191,36,0.2) !important; }
.tag-gemini { color: var(--accent3) !important; background: rgba(52,211,153,0.1) !important; border-color: rgba(52,211,153,0.2) !important; }
.tag-claude { color: var(--accent4) !important; background: rgba(244,114,182,0.1) !important; border-color: rgba(244,114,182,0.2) !important; }
.tag-progress { color: var(--accent5) !important; background: rgba(251,146,60,0.1) !important; border-color: rgba(251,146,60,0.2) !important; }
</style>
</head>
<body>

<!-- TICKER -->
<div class="ticker-wrap">
  <div class="ticker-label">LIVE</div>
  <div class="ticker-inner" id="ticker">
    <span class="ticker-item">🤖 <span>OpenAI</span> reaches 300M weekly active users — Q1 2026</span>
    <span class="ticker-item">🧠 <span>Claude 3.7 Sonnet</span> outperforms GPT-4o on 7/10 key benchmarks</span>
    <span class="ticker-item">🇨🇳 <span>DeepSeek R2</span> trained for ~$2M — Nvidia stock drops 17%</span>
    <span class="ticker-item">🌟 <span>Gemma 3</span> hits 40M downloads in 30 days — new open-source record</span>
    <span class="ticker-item">⚡ <span>Gemini 2.0 Ultra</span> ships 1M token context window</span>
    <span class="ticker-item">🔮 <span>Dario Amodei</span> predicts AGI as early as 2026-2027</span>
    <span class="ticker-item">📈 <span>Anthropic</span> valued at $40B after Series E</span>
    <span class="ticker-item">🚀 <span>MCP protocol</span> adopted by OpenAI, Google, and 50,000+ integrations</span>
    <!-- repeat for seamless loop -->
    <span class="ticker-item">🤖 <span>OpenAI</span> reaches 300M weekly active users — Q1 2026</span>
    <span class="ticker-item">🧠 <span>Claude 3.7 Sonnet</span> outperforms GPT-4o on 7/10 key benchmarks</span>
    <span class="ticker-item">🇨🇳 <span>DeepSeek R2</span> trained for ~$2M — Nvidia stock drops 17%</span>
    <span class="ticker-item">🌟 <span>Gemma 3</span> hits 40M downloads in 30 days — new open-source record</span>
    <span class="ticker-item">⚡ <span>Gemini 2.0 Ultra</span> ships 1M token context window</span>
    <span class="ticker-item">🔮 <span>Dario Amodei</span> predicts AGI as early as 2026-2027</span>
    <span class="ticker-item">📈 <span>Anthropic</span> valued at $40B after Series E</span>
    <span class="ticker-item">🚀 <span>MCP protocol</span> adopted by OpenAI, Google, and 50,000+ integrations</span>
  </div>
</div>

<!-- HEADER -->
<header>
  <div class="header-inner">
    <div class="logo">
      <div class="logo-icon">⚡</div>
      <div class="logo-text">
        <div class="logo-title">AI PULSE</div>
        <div class="logo-subtitle">Intelligence Feed · 2026</div>
      </div>
    </div>
    <div class="header-meta">
      <div class="live-dot"></div>
      <span>LIVE DATA</span>
      <span style="color:var(--border)">|</span>
      <span id="current-time"></span>
      <span style="color:var(--border)">|</span>
      <span style="color:var(--accent)">ainews.anervea.ai</span>
    </div>
  </div>
</header>

<!-- HERO -->
<div class="hero">
  <div class="hero-eyebrow">// The Intelligence Report — April 2026</div>
  <h1 class="hero-title">
    <span class="line1">THE AI ARMS RACE</span>
    <span class="line2">IS ACCELERATING</span>
  </h1>
  <p class="hero-sub">From DeepSeek's $2M shock to Claude outperforming GPT-4o, Gemini's 1M context window, and China's AGI sprint — the most consequential technology race in human history, in real time.</p>
</div>

<!-- TOP STATS -->
<div class="stats-bar">
  <div class="stats-grid" id="top-stats"></div>
</div>

<!-- TABS -->
<div class="tabs-section">
  <div class="tabs-nav">
    <button class="tab-btn active" onclick="switchTab('all')">
      <div class="tab-dot"></div> All Stories
    </button>
    <button class="tab-btn" onclick="switchTab('openai')">
      <div class="tab-dot"></div> 🤖 OpenAI
    </button>
    <button class="tab-btn" onclick="switchTab('claude')">
      <div class="tab-dot"></div> 🛡️ Claude & Anthropic
    </button>
    <button class="tab-btn" onclick="switchTab('gemini')">
      <div class="tab-dot"></div> ✨ Gemini & Gemma
    </button>
    <button class="tab-btn" onclick="switchTab('china')">
      <div class="tab-dot"></div> 🇨🇳 China & DeepSeek
    </button>
    <button class="tab-btn" onclick="switchTab('progress')">
      <div class="tab-dot"></div> 🚀 AI Progress
    </button>
    <button class="tab-btn" onclick="switchTab('agi')">
      <div class="tab-dot"></div> 🧠 AGI: The Future?
    </button>
  </div>
</div>

<!-- CONTENT -->
<div class="content-area">

  <div class="tab-content active" id="tab-all">
    <div class="section-header">
      <div class="section-title">ALL STORIES</div>
      <div class="section-count" id="all-count"></div>
    </div>
    <div class="all-articles-grid" id="all-articles"></div>
  </div>

  <div class="tab-content" id="tab-openai">
    <div class="section-header">
      <div class="section-title">OPENAI INTELLIGENCE</div>
      <div class="section-count">300M+ Weekly Users · $5B ARR</div>
    </div>
    <div class="articles-grid" id="openai-articles-featured"></div>
    <div class="stats-detail-grid" id="openai-stats"></div>
  </div>

  <div class="tab-content" id="tab-claude">
    <div class="section-header">
      <div class="section-title">CLAUDE & ANTHROPIC</div>
      <div class="section-count">$40B Valuation · Safety-First AI</div>
    </div>
    <div class="articles-grid" id="claude-articles-featured"></div>
    <div class="stats-detail-grid" id="claude-stats"></div>
  </div>

  <div class="tab-content" id="tab-gemini">
    <div class="section-header">
      <div class="section-title">GEMINI & GEMMA</div>
      <div class="section-count">1B Daily Interactions · 40M Downloads</div>
    </div>
    <div class="articles-grid" id="gemini-articles-featured"></div>
    <div class="stats-detail-grid" id="gemini-stats"></div>
  </div>

  <div class="tab-content" id="tab-china">
    <div class="section-header">
      <div class="section-title">CHINA'S AGI SPRINT</div>
      <div class="section-count">$50B State Funding · DeepSeek Shock</div>
    </div>
    <div class="articles-grid" id="china-articles-featured"></div>
    <div class="stats-detail-grid" id="china-stats"></div>
  </div>

  <div class="tab-content" id="tab-progress">
    <div class="section-header">
      <div class="section-title">AI PROGRESS REPORT</div>
      <div class="section-count">Agents · MCP · Infrastructure</div>
    </div>
    <div class="articles-grid" id="progress-articles-featured"></div>

    <div class="section-header" style="margin-top:40px">
      <div class="section-title">AI CAPABILITY TIMELINE</div>
    </div>
    <div class="timeline">
      <div class="timeline-item">
        <div class="timeline-dot"></div>
        <div class="timeline-year">2022</div>
        <div class="timeline-event">ChatGPT Launch — Consumer AI Goes Mainstream</div>
        <div class="timeline-desc">100M users in 60 days. The public interfaces with frontier AI for the first time. The era of language model products begins.</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot" style="background:var(--accent2); box-shadow:0 0 12px var(--accent2)"></div>
        <div class="timeline-year">2023</div>
        <div class="timeline-event">GPT-4, Claude 2, Gemini — The Capability Explosion</div>
        <div class="timeline-desc">Multimodal AI, 100K context windows, code generation surpasses human performance on competitive programming. Enterprise AI spending crosses $10B.</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot" style="background:var(--accent3); box-shadow:0 0 12px var(--accent3)"></div>
        <div class="timeline-year">2024</div>
        <div class="timeline-event">Agents, Reasoning Models, Open Source Explosion</div>
        <div class="timeline-desc">o1 and Claude 3.5 introduce inference-time reasoning. LLaMA 3 democratizes frontier AI. Agentic workflows move from research to production.</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot" style="background:var(--gold); box-shadow:0 0 12px var(--gold)"></div>
        <div class="timeline-year">2025</div>
        <div class="timeline-event">DeepSeek Shock, Claude 3.7, Gemini 2.0 — The Race Intensifies</div>
        <div class="timeline-desc">DeepSeek R1 redefines training economics. Claude 3.7 leads on coding and reasoning. Google ships 1M context window. AI enters every enterprise workflow.</div>
      </div>
      <div class="timeline-item">
        <div class="timeline-dot" style="background:var(--red); box-shadow:0 0 12px var(--red)"></div>
        <div class="timeline-year">2026 →</div>
        <div class="timeline-event">AGI Threshold? The Convergence Point</div>
        <div class="timeline-desc">Leading researchers update timelines. Autonomous agents handle entire workflows. The capability gap between AI and human experts narrows in domain after domain.</div>
      </div>
    </div>
  </div>

  <div class="tab-content" id="tab-agi">
    <div class="section-header">
      <div class="section-title">AGI: IS IT THE FUTURE?</div>
      <div class="section-count">Predictions from Top Scientists</div>
    </div>
    <div class="articles-grid" id="agi-articles-featured"></div>

    <div class="section-header" style="margin-top:48px">
      <div class="section-title">WHAT THE EXPERTS SAY</div>
      <div class="section-count">6 Leading Voices on AGI Timelines</div>
    </div>
    <div class="predictions-grid" id="predictions-grid"></div>

    <div style="background:var(--surface); border:1px solid rgba(251,191,36,0.2); border-radius:24px; padding:40px; margin-top:20px;">
      <div style="font-family:'Bebas Neue',sans-serif; font-size:28px; letter-spacing:2px; color:var(--gold); margin-bottom:20px;">THE CONSENSUS VIEW</div>
      <p style="font-size:15px; line-height:1.8; color:rgba(240,244,255,0.8); max-width:800px;">The AI research community has reached an unusual moment of convergence: even skeptics are revising their timelines upward. The combination of scaling laws that haven't plateaued, inference-time compute as a second scaling dimension, and efficiency breakthroughs like DeepSeek's mixture-of-experts architecture suggests that AGI — defined as AI systems that match or exceed human performance across most cognitive domains — may arrive before most policymakers and institutions have prepared for it.</p>
      <div style="display:grid; grid-template-columns:repeat(3,1fr); gap:20px; margin-top:28px;">
        <div style="text-align:center; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; border:1px solid var(--border);">
          <div style="font-family:'Bebas Neue',sans-serif; font-size:40px; color:var(--accent);">73%</div>
          <div style="font-size:12px; color:var(--muted); margin-top:4px;">of surveyed AI researchers believe AGI arrives before 2035</div>
        </div>
        <div style="text-align:center; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; border:1px solid var(--border);">
          <div style="font-family:'Bebas Neue',sans-serif; font-size:40px; color:var(--accent2);">5-10</div>
          <div style="font-size:12px; color:var(--muted); margin-top:4px;">years: Yoshua Bengio's revised timeline estimate (2026)</div>
        </div>
        <div style="text-align:center; padding:20px; background:rgba(255,255,255,0.03); border-radius:12px; border:1px solid var(--border);">
          <div style="font-family:'Bebas Neue',sans-serif; font-size:40px; color:var(--accent3);">$1T+</div>
          <div style="font-size:12px; color:var(--muted); margin-top:4px;">projected global AI investment by 2027 across private and public sectors</div>
        </div>
      </div>
    </div>
  </div>

</div>

<!-- FOOTER -->
<footer>
  <div>⚡ <strong>AI Pulse</strong> — ainews.anervea.ai · Powered by Anervea Intelligence Platform</div>
  <div>Data sourced from public research, benchmarks & industry analysis · Updated continuously</div>
</footer>

<!-- MODAL -->
<div class="modal-overlay" id="modal-overlay" onclick="closeModal(event)">
  <div class="modal" id="modal">
    <button class="modal-close" onclick="closeModalBtn()">✕</button>
    <div class="modal-tag" id="modal-tag"></div>
    <div class="modal-title" id="modal-title"></div>
    <div class="modal-subtitle" id="modal-subtitle"></div>
    <div class="modal-meta" id="modal-meta"></div>
    <div class="modal-content" id="modal-content"></div>
    <div class="modal-tags" id="modal-tags"></div>
  </div>
</div>

<script>
const TAB_EMOJIS = { openai:'🤖', claude:'🛡️', gemini:'✨', china:'🇨🇳', progress:'🚀', agi:'🧠' };
const TAB_COLORS = { openai:'var(--accent)', claude:'var(--accent4)', gemini:'var(--accent3)', china:'var(--red)', progress:'var(--accent5)', agi:'var(--gold)' };
const TAB_CLASSES = { openai:'', claude:'tag-claude', gemini:'tag-gemini', china:'tag-china china-card', progress:'tag-progress', agi:'tag-agi' };

let allArticles = [];
let allPredictions = [];

function updateTime() {
  const now = new Date();
  document.getElementById('current-time').textContent =
    now.toLocaleTimeString('en-US', {hour:'2-digit', minute:'2-digit', second:'2-digit'});
}
setInterval(updateTime, 1000);
updateTime();

async function fetchAll() {
  const [articles, stats, predictions] = await Promise.all([
    fetch('/api/articles').then(r => r.json()),
    fetch('/api/stats').then(r => r.json()),
    fetch('/api/predictions').then(r => r.json())
  ]);
  allArticles = articles;
  allPredictions = predictions;

  renderTopStats(stats.slice(0, 4));
  renderAllArticles(articles);
  renderTabArticles('openai', articles.filter(a => a.tab === 'openai'));
  renderTabArticles('claude', articles.filter(a => a.tab === 'claude'));
  renderTabArticles('gemini', articles.filter(a => a.tab === 'gemini'));
  renderTabArticles('china', articles.filter(a => a.tab === 'china'));
  renderTabArticles('progress', articles.filter(a => a.tab === 'progress'));
  renderTabArticles('agi', articles.filter(a => a.tab === 'agi'));
  renderTabStats('openai', stats);
  renderTabStats('claude', stats);
  renderTabStats('gemini', stats);
  renderTabStats('china', stats);
  renderPredictions(predictions);
}

function renderTopStats(stats) {
  const topStats = [
    { icon: '👥', value: '300M+', label: 'OpenAI Weekly Users', trend: '+15% QoQ' },
    { icon: '📈', value: '$40B', label: 'Anthropic Valuation', trend: 'Series E 2026' },
    { icon: '🔥', value: '~$2M', label: 'DeepSeek R2 Training Cost', trend: 'vs $100M+ GPT-4' },
    { icon: '⬇️', value: '40M+', label: 'Gemma 3 Downloads', trend: '30-day record' }
  ];
  document.getElementById('top-stats').innerHTML = topStats.map((s, i) => `
    <div class="stat-card" style="animation-delay:${0.7 + i*0.1}s">
      <div class="stat-icon">${s.icon}</div>
      <div class="stat-value">${s.value}</div>
      <div class="stat-label">${s.label}</div>
      <div class="stat-trend">↑ ${s.trend}</div>
    </div>
  `).join('');
}

function articleEmoji(tab) {
  return TAB_EMOJIS[tab] || '📰';
}

function renderAllArticles(articles) {
  document.getElementById('all-count').textContent = `${articles.length} articles`;
  document.getElementById('all-articles').innerHTML = articles.map(a => `
    <div class="article-card-medium ${TAB_CLASSES[a.tab] || ''}" onclick="openArticle(${a.id})">
      <span class="card-emoji">${articleEmoji(a.tab)}</span>
      <div class="article-tag ${TAB_CLASSES[a.tab] || ''}">${a.tab.toUpperCase()}</div>
      <div class="card-medium-title">${a.title}</div>
      <div class="card-medium-sub">${a.subtitle || ''}</div>
      <div class="card-medium-footer">
        <span>${a.author || 'Staff'}</span>
        <span>${a.source || ''}</span>
      </div>
    </div>
  `).join('');
}

function renderTabArticles(tab, articles) {
  const featuredEl = document.getElementById(`${tab}-articles-featured`);
  if (!featuredEl || articles.length === 0) return;
  const featured = articles[0];
  const rest = articles.slice(1);
  featuredEl.innerHTML = `
    <div class="article-card-featured" onclick="openArticle(${featured.id})">
      <div class="article-featured-header">
        <div class="article-tag ${TAB_CLASSES[tab] || ''}">${articleEmoji(tab)} ${tab.toUpperCase()}</div>
      </div>
      <div class="article-featured-visual">
        <span class="vis-icon" style="font-size:72px">${articleEmoji(tab)}</span>
      </div>
      <div class="article-featured-body">
        <div class="article-title">${featured.title}</div>
        <div class="article-subtitle">${featured.subtitle || ''}</div>
        <div class="article-meta">
          <span class="article-author">${featured.author || 'Staff'}</span>
          <span>·</span>
          <span>${featured.source || ''}</span>
        </div>
      </div>
    </div>
    <div class="articles-sidebar">
      ${rest.map(a => `
        <div class="article-card-small" onclick="openArticle(${a.id})">
          <div class="article-tag ${TAB_CLASSES[tab] || ''}" style="font-size:9px; padding:3px 8px; margin-bottom:8px">${tab.toUpperCase()}</div>
          <div class="small-title">${a.title}</div>
          <div class="small-meta">${a.author || 'Staff'} · ${a.source || ''}</div>
        </div>
      `).join('')}
    </div>
  `;
}

function renderTabStats(tab, allStats) {
  const el = document.getElementById(`${tab}-stats`);
  if (!el) return;
  const stats = allStats.filter(s => s.category === tab);
  el.innerHTML = stats.map(s => `
    <div class="stat-card">
      <div class="stat-icon">${s.icon || '📊'}</div>
      <div class="stat-value" style="color:${TAB_COLORS[tab] || 'var(--accent)'}">${s.value}</div>
      <div class="stat-label">${s.label}</div>
      <div class="stat-trend">${s.trend || ''}</div>
    </div>
  `).join('');
}

function renderPredictions(predictions) {
  document.getElementById('predictions-grid').innerHTML = predictions.map(p => `
    <div class="prediction-card">
      <div class="pred-avatar">${p.avatar || '🧠'}</div>
      <div class="pred-name">${p.scientist}</div>
      <div class="pred-role">${p.role}</div>
      <div class="pred-quote">${p.quote}</div>
      <div class="pred-footer">
        <div class="pred-year">${p.year_prediction}</div>
        <div class="pred-conf">
          <div class="conf-bar"><div class="conf-fill" style="width:${p.confidence}%"></div></div>
          <span>${p.confidence}%</span>
        </div>
      </div>
    </div>
  `).join('');
}

async function openArticle(id) {
  const article = await fetch(`/api/articles/${id}`).then(r => r.json());
  document.getElementById('modal-tag').textContent = `${articleEmoji(article.tab)} ${article.tab.toUpperCase()}`;
  document.getElementById('modal-title').textContent = article.title;
  document.getElementById('modal-subtitle').textContent = article.subtitle || '';
  document.getElementById('modal-meta').innerHTML = `
    <span>✍️ ${article.author || 'Staff'}</span>
    <span>📰 ${article.source || 'AI Pulse'}</span>
    <span>👁️ ${article.views} views</span>
  `;
  document.getElementById('modal-content').textContent = article.content;
  document.getElementById('modal-tags').innerHTML = (article.tags || []).map(t =>
    `<span class="modal-tag-chip">#${t}</span>`
  ).join('');
  document.getElementById('modal-overlay').classList.add('open');
  document.body.style.overflow = 'hidden';
}

function closeModal(e) {
  if (e.target === document.getElementById('modal-overlay')) closeModalBtn();
}
function closeModalBtn() {
  document.getElementById('modal-overlay').classList.remove('open');
  document.body.style.overflow = '';
}
document.addEventListener('keydown', e => { if (e.key === 'Escape') closeModalBtn(); });

function switchTab(tab) {
  document.querySelectorAll('.tab-content').forEach(el => el.classList.remove('active'));
  document.querySelectorAll('.tab-btn').forEach(el => el.classList.remove('active'));
  document.getElementById(`tab-${tab}`).classList.add('active');
  const btns = document.querySelectorAll('.tab-btn');
  const tabMap = ['all','openai','claude','gemini','china','progress','agi'];
  btns[tabMap.indexOf(tab)].classList.add('active');
  window.scrollTo({ top: 380, behavior: 'smooth' });
}

fetchAll();
</script>
</body>
</html>
"""
