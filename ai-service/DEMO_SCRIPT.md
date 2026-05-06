# DEMO SCRIPT — AI Developer 1
## Tool-122 Internal Audit Sampling Tool
## Demo Day: 9 May 2026

---

## MY ROLE
I am AI Developer 1. I built the entire AI microservice for this tool.
This includes all Flask endpoints, Groq integration, prompt templates,
security, caching and ChromaDB knowledge base.

---

## WHAT I BUILT (60 seconds)

"I built the AI brain of this tool. It is a Flask microservice
running on port 5000 that connects to Groq's LLaMA-3.3-70b model.

When an auditor creates a new audit item, my service automatically:
1. Generates a professional description with risk level
2. Produces 3 actionable recommendations
3. Creates a full formal audit report

All of this happens in seconds using AI."

---

## LIVE DEMO STEPS

### Step 1 — Start the AI service
Run in terminal:
python app.py

Show the panel saying:
- sentence-transformers model loaded
- ChromaDB seeded with 10 documents
- Running on http://127.0.0.1:5000

### Step 2 — Show /health endpoint
"Let me show you the health of my AI service"

Run:
Invoke-WebRequest -Uri "http://127.0.0.1:5000/health" -UseBasicParsing | Select-Object -ExpandProperty Content

Point out:
- status: ok
- model: llama-3.3-70b-versatile
- uptime_seconds
- avg_response_time_ms

### Step 3 — Live /describe demo
"Now let me create an audit item and watch the AI describe it"

Run:
Invoke-WebRequest -Uri "http://127.0.0.1:5000/describe" -Method POST -ContentType "application/json" -Body '{"item_name": "Accounts Payable Review", "department": "Finance", "sample_size": 50, "period": "Q1 2026", "notes": "Missing approval signatures"}' -UseBasicParsing | Select-Object -ExpandProperty Content

Point out:
- description field
- risk_level
- compliance_status
- key_observations
- is_fallback: false (real AI response)
- generated_at timestamp

### Step 4 — Live /recommend demo
"Now the AI generates 3 specific recommendations"

Run:
Invoke-WebRequest -Uri "http://127.0.0.1:5000/recommend" -Method POST -ContentType "application/json" -Body '{"item_name": "Accounts Payable Review", "department": "Finance", "risk_level": "High", "compliance_status": "Non-Compliant", "description": "Missing approval signatures found"}' -UseBasicParsing | Select-Object -ExpandProperty Content

Point out:
- 3 recommendations
- action_type: Immediate/Short-Term/Long-Term
- priority: Critical/High/Medium
- owner field

### Step 5 — Live /generate-report demo
"Finally the AI generates a complete formal audit report"

Run:
Invoke-WebRequest -Uri "http://127.0.0.1:5000/generate-report" -Method POST -ContentType "application/json" -Body '{"audit_title": "Q1 2026 Finance Audit", "department": "Finance", "period": "Q1 2026", "sample_size": 50, "items_reviewed": "Accounts Payable", "risk_summary": "High risk", "findings": "Missing approval signatures"}' -UseBasicParsing | Select-Object -ExpandProperty Content

Point out:
- title
- executive_summary
- audit_opinion
- key_items with severity
- recommendations

---

## TECH EXPLANATION (60 seconds)
"My AI service uses:
- Flask 3.x as the web framework
- Groq API with LLaMA-3.3-70b — completely free, no credit card
- Prompt engineering — I wrote 3 custom prompts that tell the AI
  exactly how to respond as an internal auditor
- Redis caching with SHA256 keys — same input never calls Groq twice
- sentence-transformers for embeddings
- ChromaDB as a vector database with 10 audit knowledge documents
- flask-limiter for rate limiting — 30 requests per minute
- Input sanitisation against prompt injection and SQL injection"

---

## SECURITY TALKING POINTS
"My service is secured with:
- Input sanitisation — blocks prompt injection and SQL injection
- Security headers on every response — X-Frame-Options, CSP, XSS Protection
- Rate limiting — 30 requests per minute per IP
- API keys in .env — never committed to GitHub
- Graceful fallback — never returns 500 even if Groq is down"

---

## Q&A ANSWERS

Q: What does your service do?
A: "It is the AI brain of the audit tool. It automatically generates
audit descriptions, recommendations and formal reports using Groq AI."

Q: What AI model did you use?
A: "LLaMA-3.3-70b through Groq API. It is completely free and very fast."

Q: What if the AI is unavailable?
A: "Every endpoint has a fallback response with is_fallback:true.
The service never crashes — it degrades gracefully."

Q: How did you secure the AI service?
A: "Input sanitisation, security headers, rate limiting and
API keys stored safely in .env file."