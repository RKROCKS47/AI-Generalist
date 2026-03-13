import re
from src.utils import clean_text, NA, unique_keep_order

AREA_PATTERNS = [
    "Hall", "Bedroom", "Master Bedroom", "Kitchen", "Parking Area",
    "Common Bathroom", "Bathroom", "Balcony", "Terrace", "External Wall",
    "Passage", "Staircase"
]

ISSUE_KEYWORDS = [
    "dampness", "seepage", "leakage", "crack", "efflorescence",
    "spalling", "tile joint", "gaps", "hollowness", "plumbing issue",
    "paint", "vegetation", "moss", "water ingress"
]

def _match_areas(text: str) -> list[str]:
    found = []
    lower = text.lower()
    for area in AREA_PATTERNS:
        if area.lower() in lower:
            found.append(area)
    return unique_keep_order(found)

def _extract_between(text: str, start_pattern: str, end_pattern: str) -> str:
    pattern = re.compile(start_pattern + r"(.*?)" + end_pattern, re.I | re.S)
    m = pattern.search(text)
    return clean_text(m.group(1)) if m else NA

def parse_property_details(inspection_text: str) -> dict:
    return {
        "customer_name": _extract_between(inspection_text, r"Customer Name[:\s]*", r"Customer Full Address"),
        "address": _extract_between(inspection_text, r"Customer Full Address[:\s]*", r"E-Mail Address|Contact No\."),
        "property_type": _extract_between(inspection_text, r"Property Type[:\s]*", r"Floors|Inspection Date"),
        "floors": _extract_between(inspection_text, r"Floors[:\s]*", r"Year of Construction|Previous Structure Audit Done|Inspection Date"),
        "inspection_date": _extract_between(inspection_text, r"Date of Inspection[:\s]*", r"Time of Inspection|Inspected By"),
        "inspected_by": _extract_between(inspection_text, r"Inspected By[:\s]*", r"SECTION|2\.2 DESCRIPTION OF SITE|Property Type|$")
    }

def parse_impacted_areas(inspection_text: str) -> list[dict]:
    results = []
    lines = [clean_text(x) for x in inspection_text.splitlines() if clean_text(x)]

    for line in lines:
        lower = line.lower()
        if any(keyword in lower for keyword in ISSUE_KEYWORDS):
            matched = _match_areas(line)
            if matched:
                for area in matched:
                    results.append({
                        "area": area,
                        "observation": line
                    })

    grouped = {}
    for item in results:
        grouped.setdefault(item["area"], []).append(item["observation"])

    final = []
    for area, observations in grouped.items():
        final.append({
            "area": area,
            "inspection_observations": unique_keep_order(observations),
            "thermal_evidence": [],
            "supporting_images": [],
            "confidence": "Medium"
        })

    return final
