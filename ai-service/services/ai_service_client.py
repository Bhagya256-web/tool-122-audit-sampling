import logging
from services.groq_client import call_groq
from services.sanitiser import sanitise_input
import json
import os

logger = logging.getLogger(__name__)

DESCRIBE_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "describe_prompt.txt")
RECOMMEND_PROMPT_PATH = os.path.join(os.path.dirname(__file__), "..", "prompts", "recommend_prompt.txt")


def load_prompt(path: str) -> str:
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


class AiServiceClient:
    """
    Client that calls Groq directly for full analysis.
    Handles None gracefully — never crashes the caller.
    """

    def describe(self, item_name, department, sample_size, period, notes=""):
        try:
            prompt = load_prompt(DESCRIBE_PROMPT_PATH).format(
                item_name=item_name,
                department=department,
                sample_size=sample_size,
                period=period,
                notes=notes or "None provided",
            )
            raw = call_groq([{"role": "user", "content": prompt}], temperature=0.3)
            raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            return json.loads(raw)
        except Exception as e:
            logger.error(f"describe failed: {e}")
            return None

    def recommend(self, item_name, department, risk_level,
                  compliance_status, description, observations=""):
        try:
            prompt = load_prompt(RECOMMEND_PROMPT_PATH).format(
                item_name=item_name,
                department=department,
                risk_level=risk_level,
                compliance_status=compliance_status,
                description=description,
                observations=observations or "None provided",
            )
            raw = call_groq([{"role": "user", "content": prompt}], temperature=0.4)
            raw = raw.strip().lstrip("```json").lstrip("```").rstrip("```").strip()
            return json.loads(raw)
        except Exception as e:
            logger.error(f"recommend failed: {e}")
            return None

    def full_analysis(self, item_name, department, sample_size, period, notes=""):
        result = {}

        # Step 1 - Describe
        describe_result = self.describe(
            item_name=item_name,
            department=department,
            sample_size=sample_size,
            period=period,
            notes=notes,
        )

        if describe_result:
            result["description_analysis"] = describe_result
        else:
            result["description_analysis"] = None
            logger.warning("describe returned None — attaching null gracefully")

        # Step 2 - Recommend only if describe worked
        if describe_result and not describe_result.get("is_fallback"):
            recommend_result = self.recommend(
                item_name=item_name,
                department=department,
                risk_level=describe_result.get("risk_level", "Medium"),
                compliance_status=describe_result.get("compliance_status", "Requires Review"),
                description=describe_result.get("description", ""),
                observations=", ".join(describe_result.get("key_observations", [])),
            )
            result["recommendations"] = recommend_result
        else:
            result["recommendations"] = None
            logger.warning("Skipping recommend — describe failed or was fallback")

        return result