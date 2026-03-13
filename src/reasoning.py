import json
from openai import OpenAI
from config import OPENAI_API_KEY, OPENAI_MODEL

SYSTEM_PROMPT = """
You are a senior AI engineer and building diagnostics assistant.

You receive structured evidence from:
1. inspection report extraction
2. thermal report extraction

Your job:
- Produce a client-friendly Main DDR JSON
- Never invent facts
- If any field is missing, write "Not Available"
- If an expected image is unavailable, use "Image Not Available"
- If information conflicts, mention it in conflicts
- Avoid duplicate points
- Use cautious language for thermal interpretation
- Thermal anomalies may indicate moisture or leakage, but do not state certainty unless supported by inspection evidence

Return valid JSON only with these top-level keys exactly:
property_details
property_issue_summary
area_wise_observations
thermal_analysis_findings
probable_root_cause
severity_assessment
recommended_actions
additional_notes
missing_information
conflicts
"""

def generate_ddr_json(payload: dict) -> dict:
    if not OPENAI_API_KEY:
        raise RuntimeError("OPENAI_API_KEY is missing")

    client = OpenAI(api_key=OPENAI_API_KEY)

    response = client.chat.completions.create(
        model=OPENAI_MODEL,
        temperature=0.1,
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {
                "role": "user",
                "content": json.dumps(payload, ensure_ascii=False, indent=2)
            }
        ]
    )

    content = response.choices[0].message.content
    return json.loads(content)
