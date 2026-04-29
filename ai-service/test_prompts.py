import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="ai-service/.env")

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

test_input = """
You are an expert internal auditor with 15+ years of experience.

Audit Item Details:
- Item Name: Accounts Payable Review
- Department: Finance
- Sample Size: 50
- Period: Q1 2026
- Additional Notes: Multiple invoices found without proper approval signatures

Respond ONLY with a valid JSON object:
{
  "description": "2-3 sentence professional description",
  "risk_level": "Low | Medium | High | Critical",
  "risk_justification": "One sentence explaining the risk level",
  "compliance_status": "Compliant | Partially Compliant | Non-Compliant | Requires Review",
  "key_observations": ["observation 1", "observation 2", "observation 3"],
  "suggested_focus_areas": ["area 1", "area 2"]
}
"""

response = client.chat.completions.create(
    model="llama-3.3-70b-versatile",
    messages=[{"role": "user", "content": test_input}],
    temperature=0.3,
    max_tokens=1000,
)

print(response.choices[0].message.content)