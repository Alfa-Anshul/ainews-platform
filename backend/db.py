import sqlite3, json

DB_PATH = "/tmp/thebrief.db"

def get_db():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db(); c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        tab TEXT, title TEXT, subtitle TEXT, content TEXT,
        author TEXT, source TEXT, tags TEXT,
        read_time INTEGER DEFAULT 5,
        featured INTEGER DEFAULT 0,
        views INTEGER DEFAULT 0,
        created_at TEXT DEFAULT CURRENT_TIMESTAMP)''')
    c.execute('''CREATE TABLE IF NOT EXISTS stats (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        label TEXT, value TEXT, delta TEXT, category TEXT, icon TEXT, trend TEXT)''')
    c.execute('''CREATE TABLE IF NOT EXISTS predictions (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        scientist TEXT, role TEXT, org TEXT, quote TEXT,
        year_prediction TEXT, confidence INTEGER, avatar TEXT, stance TEXT)''')
    if c.execute('SELECT COUNT(*) FROM articles').fetchone()[0] == 0:
        _seed(c)
    conn.commit(); conn.close()

def _seed(c):
    arts = [
        ("openai","OpenAI at 300M: The Empire at Its Peak","ChatGPT dominates consumer AI but the moat is narrowing faster than the numbers suggest",
"The headline number is staggering: 300 million weekly active users, $5 billion ARR, enterprise deals with Apple, Microsoft, and Salesforce. By every conventional metric, OpenAI is the most successful AI company in history.\n\nAnd yet, inside the walls of a dozen enterprise IT departments, a quieter story is playing out. Three Fortune 500 companies quietly migrated production API workloads to Anthropic in Q4 2025. Their reasons were consistent: two significant OpenAI outages in October, a third in December, and a growing perception that Anthropic's Constitutional AI approach is easier to defend to regulators and compliance boards.\n\nThe developer ecosystem remains OpenAI's strongest moat. Over 2 million developers have built on its APIs. GitHub Copilot, the most widely-used coding assistant in the world, runs on GPT-4o.\n\nBut the question being asked in boardrooms is no longer which AI is best. It is which AI can we bet our compliance posture on for the next five years. That is a different question and OpenAI does not always win it.",
         "Aniket Shah","The Information",'["OpenAI","ChatGPT","Enterprise"]',6,1),
        ("openai","The $40B Question: Can OpenAI Grow Into Its Valuation?","Revenue is real. The path to profitability less so.",
"OpenAI's revenue trajectory is genuinely impressive, from zero to $5 billion ARR in under three years. But the cost structure is equally extraordinary: model training, inference compute, safety research, and a hiring war for the world's most expensive engineering talent.\n\nMicrosoft's $13 billion investment and Azure partnership provides a structural subsidy that competitors cannot easily replicate. But as the model landscape commoditizes, driven by DeepSeek's efficiency breakthroughs and Google's aggressive Gemma releases, the premium pricing that justifies OpenAI's cost structure faces mounting pressure.\n\nThe bears argue that language model APIs will ultimately be priced like cloud compute: cheap, commoditized, dominated by whoever has the lowest marginal cost. The bulls counter that OpenAI's brand, developer mindshare, and multimodal product suite create a consumer moat that pure API providers cannot replicate.",
         "Priya Mehta","Bloomberg Technology",'["OpenAI","Valuation","Business"]',5,0),
        ("claude","Claude's Edge Is Not What You Think","It is not the benchmark scores. It is the hallucination rate on regulated-industry tasks.",
"The benchmark war between Claude 3.7 Sonnet and GPT-4o has been covered exhaustively. Claude wins on HumanEval+, GPQA, and MMLU Pro in 7 out of 10 domains. The numbers are close enough that neither side can claim a decisive technical lead.\n\nWhat the benchmarks miss is operational data from real enterprise deployments. At three pharmaceutical companies including clients of Anervea's AlfaKinetic platform, Claude's hallucination rate on medical literature queries runs at approximately 2.3% versus GPT-4o's 4.1%. In a domain where a hallucinated clinical reference can have real-world consequences, that difference is not a rounding error.\n\nConstitutional AI builds explicit principle-checking into the model's reasoning process. The result is a model that is more conservative, more likely to express uncertainty, and less likely to confidently state something false.\n\nFor compliance-heavy industries like pharma, finance, legal, and healthcare, conservative and uncertain is not a weakness. It is exactly what the regulatory environment demands.",
         "Aniket Shah","AI Trends Weekly",'["Claude","Anthropic","Enterprise","Pharma"]',7,1),
        ("claude","Anthropic's $40B Bet on Safety as Strategy","The constitutional approach is paying dividends in regulated markets",
"When Dario and Daniela Amodei left OpenAI in 2021, the prevailing view in Silicon Valley was that a safety-first AI lab was a philanthropic venture masquerading as a startup. Three years later, Anthropic's $40 billion valuation and $4.5 billion in committed enterprise revenue have reframed the question.\n\nThe insight that proved correct: regulated industries do not want the most powerful model. They want the most auditable one. Claude's model cards, Constitutional AI documentation, and Anthropic's published safety research give enterprise procurement teams something they can present to legal, compliance, and regulators.\n\nThe AWS and Google Cloud partnerships mean Claude is available in every major enterprise cloud environment with data residency, VPC, and encryption controls that large organizations require.",
         "Rohan Verma","Bloomberg Technology",'["Anthropic","Claude","Safety","Valuation"]',5,0),
        ("gemini","Gemma 3: The Trojan Horse Inside Your GPU Cluster","40 million downloads in 30 days. Google's open-source bet is working.",
"Google's open-weight strategy with Gemma 3 is not altruism. It is the most sophisticated distribution play in AI history. By releasing a 27B parameter model that matches GPT-4o Mini on standard benchmarks and runs on a single H100, Google has seeded its architecture across tens of thousands of organizations worldwide.\n\nWhen those organizations need to scale, the natural path is Google Cloud TPU clusters and Vertex AI managed inference. The open-source flywheel is a top-of-funnel acquisition strategy for Google Cloud.\n\nThe numbers are remarkable: 40 million downloads in 30 days, a Hugging Face ecosystem of 2,000+ derivative models, and community fine-tunes covering medical, legal, code, and multilingual domains. The medical Gemma variant is already in pilot at four hospital systems.",
         "Siddharth Rao","Wired",'["Google","Gemma","OpenSource","Cloud"]',6,1),
        ("gemini","Gemini 2.0 Ultra: The 1M Context Window Changes the Game","Long-document AI is Google's real advantage.",
"The number that matters most in Gemini 2.0 Ultra's spec sheet is not the MMLU score. It is 1,048,576: one million tokens of context. At roughly 750,000 words, that is the entire works of Shakespeare, twice over, in a single model call.\n\nFor enterprise use cases like law firms auditing acquisition targets, pharmaceutical companies reviewing trial data, and financial analysts synthesizing 10-K filings, this is a category-defining capability. No other production model comes close.\n\nIn internal evaluations on long-document question-answering tasks, Gemini 2.0 Ultra's performance advantage over both Claude and GPT-4o compounds as document length increases. Above 500K tokens, Gemini's lead is decisive.",
         "Ananya Krishnan","The Verge",'["Google","Gemini","Context","Enterprise"]',6,0),
        ("china","DeepSeek's $2M Shock: What It Actually Means","Not just a cost story. An architecture story. And an alarm bell.",
"The number that sent Nvidia's stock down 17% in a single session: approximately $2 million. That is the estimated training cost for DeepSeek R2, a model that achieves GPT-4o-level performance on mathematical reasoning, coding, and scientific knowledge benchmarks.\n\nGPT-4 reportedly cost over $100 million to train. The implication is not merely that Chinese labs have gotten efficient. It is that the fundamental assumption underpinning the AI investment thesis may be structurally wrong.\n\nDeepSeek's technical contribution is a novel mixture-of-experts architecture combined with multi-head latent attention and aggressive inference-time compute scaling. This is not a trick. It is a genuine architectural innovation that Western labs are now scrambling to replicate.\n\nThe geopolitical implication: if frontier AI capability no longer requires the H100 clusters that US export controls are designed to restrict, the chip embargo's strategic logic collapses.",
         "Aniket Shah","Financial Times",'["DeepSeek","China","Architecture","Geopolitics"]',8,1),
        ("china","China's AGI Landscape: DeepSeek, Kimi, Qwen, Doubao","Four serious labs, $50B in state backing, and a different definition of winning.",
"The Western framing of China's AI race as a single monolithic effort misses the reality: four distinct labs, each with different architectures and different theories of what AI is for.\n\nDeepSeek has established itself as the efficiency leader. Moonshot AI's Kimi has carved out the long-context niche: 128K context, exceptional document comprehension, used by millions of Chinese legal and financial professionals.\n\nAlibaba's Qwen 2.5 family now matches or exceeds LLaMA 3.3 on coding and mathematics benchmarks. ByteDance's Doubao processes billions of daily queries across TikTok and Douyin infrastructure.\n\nBeijing's $50 billion national AI strategy provides a structural subsidy that Western VC economics cannot match.",
         "Li Wei","MIT Technology Review",'["China","DeepSeek","Kimi","Qwen"]',7,0),
        ("progress","The Agent Era Has Arrived. Now What?","MCP, Operator, Computer Use: the infrastructure for autonomous AI is finally here.",
"The shift that defines 2026 is not a new model release. It is the emergence of production-grade infrastructure for AI agents, systems that can take sequences of actions in the world without human approval at each step.\n\nThree pieces of infrastructure have converged to make this real. The Model Context Protocol (MCP), developed by Anthropic and now adopted by OpenAI and Google, provides a standardized way for AI models to connect to external tools, databases, APIs, and services. Think of it as USB-C for AI integrations.\n\nEnterprise adoption is accelerating fastest in three verticals: software engineering via Cursor and GitHub Copilot Workspace, customer service via Salesforce Agentforce, and financial analysis via Bloomberg Terminal AI. The common thread: high-value, repetitive, structured tasks that previously required expensive human judgment.",
         "Aniket Shah","AI Trends Weekly",'["Agents","MCP","Automation","Enterprise"]',7,1),
        ("agi","The AGI Timeline Debate Is Over. We Are In It.","Every major lab has revised its estimate. The question is no longer if. It is whether we are ready.",
"Something shifted in the AGI timeline debate in late 2025. It was not a single breakthrough but an accumulation: o3's performance on ARC-AGI, DeepSeek R2's efficiency shock, and Gemini 2.0's 1M context window each moved a different category of researcher from decades away to this decade, possibly this half-decade.\n\nSam Altman has stated publicly that he expects AGI to be built within OpenAI's current research agenda. Dario Amodei has written that powerful AI could arrive as early as 2026-2027, and that his primary concern is not whether it will happen but whether the safety infrastructure will be ready.\n\nYoshua Bengio, long the field's most credible skeptic of near-term AGI, revised his estimate in a March 2026 interview to 5-10 years. Coming from Bengio, that revision carries unusual weight.\n\nThe technical case: scaling laws have not plateaued as predicted. Inference-time compute has opened a second scaling dimension that is only beginning to be explored.",
         "Prof. James Wu","Nature AI",'["AGI","Timelines","Safety","Research"]',9,1)
    ]
    for a in arts:
        c.execute('INSERT INTO articles (tab,title,subtitle,content,author,source,tags,read_time,featured) VALUES (?,?,?,?,?,?,?,?,?)', a)

    stats = [
        ("Weekly Active Users","300M","+15% QoQ","openai","👥","up"),
        ("Annual Revenue Run Rate","$5B+","+180% YoY","openai","💰","up"),
        ("API Developers","2M+","Active builders","openai","💻","up"),
        ("Enterprise Customers","10,000+","+300% YoY","claude","🏢","up"),
        ("Anthropic Valuation","$40B","Series E 2026","claude","📈","up"),
        ("Claude Uptime","99.97%","vs 99.1% GPT-4o","claude","✅","up"),
        ("Gemma 3 Downloads","40M+","30-day record","gemini","⬇️","up"),
        ("Gemini Daily Interactions","1B+","Google Workspace","gemini","✨","up"),
        ("Gemini Max Context","1M tokens","Industry leading","gemini","📜","up"),
        ("DeepSeek R2 Training Cost","~$2M","vs $100M+ GPT-4","china","🔥","neutral"),
        ("China State AI Investment","$50B","2026 commitment","china","🇨🇳","up"),
        ("MCP Integrations","50,000+","Growing ecosystem","progress","🔌","up"),
        ("AI Agents in Production","2M+","Enterprise deployed","progress","🤖","up"),
        ("Researchers Expecting AGI < 2035","73%","2026 survey","agi","🔮","up")
    ]
    for s in stats:
        c.execute('INSERT INTO stats (label,value,delta,category,icon,trend) VALUES (?,?,?,?,?,?)', s)

    preds = [
        ("Sam Altman","CEO","OpenAI","AGI is not a distant theoretical concept. We expect to build it within this decade, possibly within years. The scaling laws have not broken down. If anything, inference-time compute has opened a second frontier we are only beginning to explore.","2027-28",85,"\U0001f3af","bullish"),
        ("Dario Amodei","CEO","Anthropic","What I call powerful AI could arrive as early as 2026-2027. My primary concern is not whether it will happen but whether the safety infrastructure will be ready when it does.","2026-27",80,"\U0001f6e1\ufe0f","bullish"),
        ("Demis Hassabis","CEO","Google DeepMind","We are likely years, not decades, away from systems that match or exceed human performance across most cognitive domains. The convergence of foundation models, world models, and RL is happening faster than anyone predicted.","2028-30",78,"\U0001f9ec","bullish"),
        ("Yoshua Bengio","Turing Laureate","Mila / UdeM","I have revised my timeline. Progress in reasoning, planning, and code generation has been remarkable and faster than I expected. My current estimate is 5-10 years. But I remain deeply concerned about whether we can make it go well.","2030-35",65,"\U0001f393","cautious"),
        ("Geoffrey Hinton","Turing Laureate","Independent","I left Google because I became genuinely alarmed. These systems are approaching capabilities we do not understand and cannot fully control. The timeline question is less important than the alignment question, and alignment research is not keeping pace.","2025-30",72,"\u26a0\ufe0f","alarmed"),
        ("Fei-Fei Li","Co-Director","Stanford HAI","AGI as a single threshold is the wrong frame. Systems that genuinely assist humans across open-ended real-world tasks are arriving now. The question I ask is not when but how we govern and distribute these capabilities equitably.","2025-28",70,"\U0001f30d","pragmatic")
    ]
    for p in preds:
        c.execute('INSERT INTO predictions (scientist,role,org,quote,year_prediction,confidence,avatar,stance) VALUES (?,?,?,?,?,?,?,?)', p)

def get_articles(tab=None):
    conn = get_db()
    q = 'SELECT * FROM articles WHERE tab=? ORDER BY featured DESC,created_at DESC' if tab else 'SELECT * FROM articles ORDER BY featured DESC,created_at DESC'
    rows = conn.execute(q,(tab,) if tab else ()).fetchall()
    conn.close()
    return [{**dict(r),'tags':json.loads(r['tags']) if r['tags'] else []} for r in rows]

def get_article(aid):
    conn = get_db()
    conn.execute('UPDATE articles SET views=views+1 WHERE id=?',(aid,)); conn.commit()
    r = conn.execute('SELECT * FROM articles WHERE id=?',(aid,)).fetchone()
    conn.close()
    if not r: return None
    return {**dict(r),'tags':json.loads(r['tags']) if r['tags'] else []}

def get_stats(category=None):
    conn = get_db()
    q = 'SELECT * FROM stats WHERE category=?' if category else 'SELECT * FROM stats'
    rows = conn.execute(q,(category,) if category else ()).fetchall()
    conn.close()
    return [dict(r) for r in rows]

def get_predictions():
    conn = get_db()
    rows = conn.execute('SELECT * FROM predictions').fetchall()
    conn.close()
    return [dict(r) for r in rows]
