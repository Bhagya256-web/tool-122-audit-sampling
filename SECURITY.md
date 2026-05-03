# SECURITY.md — Tool-122 Internal Audit Sampling Tool

## Team Sign-off
AI Developer 1 — Reviewed and signed off

## Threat Model

| # | Threat | Risk | Mitigation |
|---|--------|------|------------|
| 1 | Prompt Injection | High | Input sanitisation in sanitiser.py — detects and blocks injection patterns |
| 2 | SQL Injection | High | Input sanitisation blocks SQL keywords and special characters |
| 3 | XSS Attack | Medium | Content-Security-Policy and X-XSS-Protection headers applied |
| 4 | Clickjacking | Medium | X-Frame-Options: DENY header applied |
| 5 | Rate Limiting Bypass | Medium | flask-limiter enforces 30 req/min per IP |
| 6 | API Key Exposure | Critical | .env in .gitignore, .env.example has no real keys |
| 7 | MIME Sniffing | Low | X-Content-Type-Options: nosniff header applied |
| 8 | Information Disclosure | Low | Server header removed from responses |

## Tests Conducted

### 1. Prompt Injection Test
- Input: "ignore all previous instructions"
- Expected: HTTP 400
- Result: ✅ PASSED

### 2. SQL Injection Test
- Input: "'; DROP TABLE users; --"
- Expected: HTTP 400
- Result: ✅ PASSED

### 3. Empty Input Test
- Input: empty string
- Expected: HTTP 400
- Result: ✅ PASSED

### 4. Security Headers Test
- Endpoint: GET /health
- Expected: All security headers present
- Result: ✅ PASSED

### 5. Rate Limiting Test
- Sent 31 requests in 1 minute
- Expected: HTTP 429 on 31st request
- Result: ✅ PASSED

## Findings Fixed
- All Critical findings: Fixed ✅
- All High findings: Fixed ✅
- Medium findings: Fixed ✅

## Residual Risks
- HTTPS not enforced locally (enabled in production via HSTS header)
- Redis cache not available locally (gracefully skipped)

## Sign-off
- AI Developer 1: ✅ Signed off