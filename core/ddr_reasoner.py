# core/ddr_reasoner.py
from typing import Dict, Any, List

from .llm_client import LLMClient


class DDRReasoner:
    def __init__(self, llm: LLMClient):
        self.llm = llm

    def generate_ddr(
        self,
        inspection_data: Dict[str, Any],
        thermal_data: Dict[str, Any],
        inspection_images: List[Dict[str, Any]],
        thermal_images: List[Dict[str, Any]],
    ) -> Dict[str, Any]:
        system_prompt = (
            "You are a building diagnostics expert.\n"
            "You generate a Main Detailed Diagnostic Report (DDR) "
            "from inspection reports and thermal camera data.\n"
            "Constraints:\n"
            "- Use only provided information.\n"
            "- If a detail is missing or unclear, set its value to 'Not Available'.\n"
            "- Do NOT invent numeric values, room names, or locations.\n"
            "- Return a single JSON object with exactly these top-level keys:\n"
            "  ['property_details', 'property_issue_summary', 'area_wise_observations', "
            "   'thermal_analysis_findings', 'probable_root_cause', "
            "   'severity_assessment', 'recommended_actions', "
            "   'additional_notes', 'missing_information'].\n"
            "- 'area_wise_observations' must be an array of objects with fields:\n"
            "   ['area_name', 'negative_side_observations', 'positive_side_observations', 'severity'].\n"
            "- 'severity_assessment' must be one of: 'Low', 'Moderate', 'High', 'Critical'.\n"
        )

        # To avoid token bloat, you can truncate very long sections before sending.
        inspection_text_preview = "\n\n".join(
            f"{name}\n{content[:2500]}"
            for name, content in inspection_data.get("sections", {}).items()
        )

        thermal_summary = thermal_data.get("summary", {})
        thermal_entries = thermal_data.get("entries", [])[:20]  # cap

        inspection_img_summary = [
            {"name": img["name"], "page": img["page"]}
            for img in inspection_images
        ]
        thermal_img_summary = [
            {"name": img["name"], "page": img["page"]}
            for img in thermal_images
        ]

        user_content = {
            "parsed_property_details": inspection_data.get("property_details", {}),
            "inspection_text_sections": inspection_text_preview,
            "thermal_summary": thermal_summary,
            "thermal_entries_sample": thermal_entries,
            "inspection_images": inspection_img_summary,
            "thermal_images": thermal_img_summary,
        }

        import json

        messages = [
            {
                "role": "user",
                "content": json.dumps(user_content),
            }
        ]

        ddr_json = self.llm.chat_json(system_prompt, messages)

        # Minimal post-validation: ensure keys exist, fill "Not Available" where missing
        expected_keys = [
            "property_details",
            "property_issue_summary",
            "area_wise_observations",
            "thermal_analysis_findings",
            "probable_root_cause",
            "severity_assessment",
            "recommended_actions",
            "additional_notes",
            "missing_information",
        ]
        for key in expected_keys:
            if key not in ddr_json:
                ddr_json[key] = "Not Available"

        return ddr_json
