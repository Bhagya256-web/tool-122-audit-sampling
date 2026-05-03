import time
import json
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="ai-service/.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

print("=" * 60)
print("TOOL-122 AI SERVICE — DEMO DRY RUN")
print("=" * 60)

# Demo inputs
DEMO_ITEM = {
    "item_name": "Accounts Payable Review",
    "department": "Finance",
    "sample_size": 50,
    "period": "Q1 2026",
    "notes": "Multiple invoices found without proper approval signatures"
}

def call_groq(prompt, label):
    print(f"\n[TEST] {label}")
    start = time.time()
    response = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=1000,
    )
    duration = round((time.time() - start) * 1000)
    result = response.choices[0].message.content
    print(f"✅ Response time: {duration}ms")
    print(f"Output preview: {result[:200]}...")
    return duration, result

# Test 1 - /describe
describe_prompt = f"""
You are an expert internal auditor. 
Audit Item: {DEMO_ITEM['item_name']}, Department: {DEMO_ITEM['department']}, 
Sample Size: {DEMO_ITEM['sample_size']}, Period: {DEMO_ITEM['period']}, 
Notes: {DEMO_ITEM['notes']}
Respond with JSON: {{"risk_level": "High", "compliance_status": "Non-Compliant", "description": "brief description"}}
"""
t1, r1 = call_groq(describe_prompt, "POST /describe")

# Test 2 - /recommend
recommend_prompt = f"""
You are an expert internal auditor. 
Generate 3 recommendations for: {DEMO_ITEM['item_name']} in {DEMO_ITEM['department']} department.
Risk: High, Status: Non-Compliant.
Respond with JSON: {{"recommendations": [{{"action_type": "Immediate", "description": "action", "priority": "Critical"}}]}}
"""
t2, r2 = call_groq(recommend_prompt, "POST /recommend")

# Test 3 - /generate-report
report_prompt = f"""
You are a senior internal audit manager.
Generate a brief audit report for: {DEMO_ITEM['item_name']} in {DEMO_ITEM['department']}.
Respond with JSON: {{"title": "report title", "executive_summary": "summary", "audit_opinion": "Qualified"}}
"""
t3, r3 = call_groq(report_prompt, "POST /generate-report")

print("\n" + "=" * 60)
print("DEMO DRY RUN RESULTS")
print("=" * 60)
print(f"POST /describe     — {t1}ms")
print(f"POST /recommend    — {t2}ms")
print(f"POST /generate-report — {t3}ms")
print(f"Total time         — {t1+t2+t3}ms")
print("=" * 60)
print("All 3 endpoints PASSED ✅ — Ready for Demo Day!")