# AI Service — Tool-122 Internal Audit Sampling Tool

## Overview
This is the AI microservice for the Internal Audit Sampling Tool. It is built with Python 3.11 and Flask 3.x, and uses the Groq API (LLaMA-3.3-70b) to generate audit descriptions, recommendations, and reports.

## Tech Stack
- Python 3.11
- Flask 3.x
- Groq API (LLaMA-3.3-70b-versatile)
- Redis 7 (optional — for caching)
- flask-limiter (30 req/min rate limiting)

## Prerequisites
- Python 3.11 installed
- Groq API key (free at https://console.groq.com)
- Redis (optional)

## Setup Instructions

### 1. Clone the repository
```bash
git clone https://github.com/Bhagya256-web/tool-122-audit-sampling
cd tool-122-audit-sampling/ai-service
```

### 2. Install dependencies
```bash
pip install -r requirements.txt
```

### 3. Create .env file
```bash
cp .env.example .env
```
Edit `.env` and add your Groq API key:

### 4. Run the service
```bash
python app.py
```
Service runs on http://localhost:5000

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| GROQ_API_KEY | Yes | Your Groq API key from console.groq.com |
| REDIS_URL | No | Redis URL for caching (default: memory://) |
| FLASK_ENV | No | development or production |

## API Reference

### GET /health
Check service health, uptime and average response time.

**Response:**
```json
{
  "status": "ok",
  "model": "llama-3.3-70b-versatile",
  "uptime_seconds": 245,
  "avg_response_time_ms": 17077.84,
  "groq_avg_response_time_ms": 5177.2,
  "total_requests_tracked": 1
}
```

---

### POST /describe
Generate a professional audit description for an audit item.

**Request:**
```json
{
  "item_name": "Accounts Payable Review",
  "department": "Finance",
  "sample_size": 50,
  "period": "Q1 2026",
  "notes": "Missing approval signatures"
}
```

**Response:**
```json
{
  "description": "Professional audit description...",
  "risk_level": "High",
  "risk_justification": "Explanation of risk level",
  "compliance_status": "Non-Compliant",
  "key_observations": ["observation 1", "observation 2"],
  "suggested_focus_areas": ["area 1", "area 2"],
  "is_fallback": false,
  "from_cache": false,
  "generated_at": "2026-04-14T10:00:00+00:00"
}
```

---

### POST /recommend
Generate 3 actionable audit recommendations.

**Request:**
```json
{
  "item_name": "Accounts Payable Review",
  "department": "Finance",
  "risk_level": "High",
  "compliance_status": "Non-Compliant",
  "description": "Multiple invoices found without approval signatures",
  "observations": "12 out of 50 invoices missing signatures"
}
```

**Response:**
```json
{
  "recommendations": [
    {
      "action_type": "Immediate",
      "description": "Specific action to take",
      "priority": "Critical",
      "expected_outcome": "What will improve",
      "owner": "Finance Manager"
    }
  ],
  "is_fallback": false,
  "generated_at": "2026-04-14T10:00:00+00:00"
}
```

---

### POST /generate-report
Generate a complete formal audit report.

**Request:**
```json
{
  "audit_title": "Q1 2026 Finance Audit",
  "department": "Finance",
  "period": "Q1 2026",
  "sample_size": 50,
  "items_reviewed": "Accounts Payable, Payroll",
  "risk_summary": "Medium to High risk",
  "findings": "Missing signatures, duplicate payments"
}
```

**Response:**
```json
{
  "title": "Q1 2026 Finance Audit Report",
  "executive_summary": "High level summary...",
  "overview": "Detailed scope and methodology...",
  "key_items": [
    {
      "item": "Finding name",
      "detail": "Explanation",
      "severity": "High"
    }
  ],
  "recommendations": [
    {
      "action_type": "Immediate",
      "description": "Recommendation",
      "priority": "Critical"
    }
  ],
  "conclusion": "Closing paragraph...",
  "audit_opinion": "Qualified",
  "is_fallback": false,
  "generated_at": "2026-04-14T10:00:00+00:00"
}
```

## Security
- All inputs are sanitised against prompt injection and SQL injection
- Rate limiting: 30 requests per minute per IP
- Security headers applied to all responses
- API keys stored in .env (never committed to GitHub)
- See SECURITY.md for full threat model

## Fallback Behaviour
If the Groq API is unavailable, all endpoints return a fallback response with:
```json
{
  "is_fallback": true
}
```
The service never returns HTTP 500 due to AI unavailability.