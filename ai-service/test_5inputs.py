import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv(dotenv_path="ai-service/.env")
client = Groq(api_key=os.getenv("GROQ_API_KEY"))

tests = [
    "Payroll Processing - HR dept - employees paid twice",
    "IT Access Controls - IT dept - former employees still have access",
    "Inventory Count - Warehouse - physical count differs from system",
    "Travel Expense Claims - Sales - receipts missing for claims",
]

for i, note in enumerate(tests, 2):
    prompt = f"You are an expert internal auditor. Audit item: {note}. Respond ONLY with JSON: {{\"risk_level\": \"Low|Medium|High|Critical\", \"compliance_status\": \"Compliant|Partially Compliant|Non-Compliant|Requires Review\"}}"
    r = client.chat.completions.create(
        model="llama-3.3-70b-versatile",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.3,
        max_tokens=100,
    )
    print(f"Test {i}: {r.choices[0].message.content}")