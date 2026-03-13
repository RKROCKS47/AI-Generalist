import re
from collections import defaultdict

NA = "Not Available"

AREAS = [
    "hall", "bedroom", "master bedroom", "kitchen", "parking", "bathroom",
    "common bathroom", "balcony", "terrace", "external wall", "passage", "staircase"
]

ISSUE_KEYWORDS = [
    "dampness", "wall crack", "crack", "plumbing leakage", "leakage", "seepage",
    "tile joint", "gaps", "efflorescence", "paint spalling", "hollowness", "vegetation"
]

def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def find_first(pattern: str, text: str, default=NA, flags=re.I):
    m = re.search(pattern, text, flags)
    return normalize_whitespace(m.group(1)) if m else default

def parse_property_details(text: str) -> dict:
    return {
        "customer_name": find_first(r"Customer Name[:\s]+(.+?)Customer Full Address", text),
        "address": find_first(r"Customer Full Address[:\s]+(.+?)E-Mail Address", text),
        "property_type": find_first(r"Property Type[:\s]+(.+?)(?:Floors|Inspection Date)", text),
        "floors": find_first(r"Floors[:\s]+(.+?)(?:Year of Construction|Previous Structural audit done|Inspection Date)", text),
        "inspection_date": find_first(r"(?:Date of Inspection|Inspection Date and Time)[:\s]+(.+?)(?:Time of Inspection|Inspected By|Property Type)", text),
        "inspected_by": find_first(r"Inspected By[:\s]+(.+?)(?:SECTION|2\.2|Property Type|$)", text),
    }

def extract_area_observations(text: str) -> list[dict]:
    lines = [normalize_whitespace(x) for x in text.splitlines() if x.strip()]
    area_map = defaultdict(list)

    for line in lines:
        lower = line.lower()
        if any(issue in lower for issue in ISSUE_KEYWORDS):
            matched_areas = [a.title() for a in AREAS if a in lower]
            if matched_areas:
                for area in matched_areas:
                    area_map[area].append(line)

    result = []
    for area, obs in area_map.items():
        result.append({
            "area": area,
            "inspection_observations": list(dict.fromkeys(obs)),
            "thermal_evidence": [],
            "supporting_images": [],
            "confidence": "Medium"
        })
    return result

def parse_thermal_readings(text: str) -> list[dict]:
    pattern = re.compile(
        r"Thermal image\s*:\s*([A-Z0-9]+)\.JPG.*?Hotspot\s*:\s*([0-9.]+)\s*°C.*?"
        r"Coldspot\s*:\s*([0-9.]+)\s*°C.*?Emissivity\s*:\s*([0-9.]+)",
        re.I | re.S
    )

    findings = []
    for m in pattern.finditer(text):
        image_id = m.group(1)
        hotspot = float(m.group(2))
        coldspot = float(m.group(3))
        emissivity = float(m.group(4))
        delta = round(hotspot - coldspot, 2)

        findings.append({
            "image_id": image_id,
            "hotspot_c": hotspot,
            "coldspot_c": coldspot,
            "delta_c": delta,
            "emissivity": emissivity,
            "interpretation": NA,
            "mapped_area": NA
        })
    return findings
import re
from collections import defaultdict

NA = "Not Available"

AREAS = [
    "hall", "bedroom", "master bedroom", "kitchen", "parking", "bathroom",
    "common bathroom", "balcony", "terrace", "external wall", "passage", "staircase"
]

ISSUE_KEYWORDS = [
    "dampness", "wall crack", "crack", "plumbing leakage", "leakage", "seepage",
    "tile joint", "gaps", "efflorescence", "paint spalling", "hollowness", "vegetation"
]

def normalize_whitespace(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()

def find_first(pattern: str, text: str, default=NA, flags=re.I):
    m = re.search(pattern, text, flags)
    return normalize_whitespace(m.group(1)) if m else default

def parse_property_details(text: str) -> dict:
    return {
        "customer_name": find_first(r"Customer Name[:\s]+(.+?)Customer Full Address", text),
        "address": find_first(r"Customer Full Address[:\s]+(.+?)E-Mail Address", text),
        "property_type": find_first(r"Property Type[:\s]+(.+?)(?:Floors|Inspection Date)", text),
        "floors": find_first(r"Floors[:\s]+(.+?)(?:Year of Construction|Previous Structural audit done|Inspection Date)", text),
        "inspection_date": find_first(r"(?:Date of Inspection|Inspection Date and Time)[:\s]+(.+?)(?:Time of Inspection|Inspected By|Property Type)", text),
        "inspected_by": find_first(r"Inspected By[:\s]+(.+?)(?:SECTION|2\.2|Property Type|$)", text),
    }

def extract_area_observations(text: str) -> list[dict]:
    lines = [normalize_whitespace(x) for x in text.splitlines() if x.strip()]
    area_map = defaultdict(list)

    for line in lines:
        lower = line.lower()
        if any(issue in lower for issue in ISSUE_KEYWORDS):
            matched_areas = [a.title() for a in AREAS if a in lower]
            if matched_areas:
                for area in matched_areas:
                    area_map[area].append(line)

    result = []
    for area, obs in area_map.items():
        result.append({
            "area": area,
            "inspection_observations": list(dict.fromkeys(obs)),
            "thermal_evidence": [],
            "supporting_images": [],
            "confidence": "Medium"
        })
    return result

def parse_thermal_readings(text: str) -> list[dict]:
    pattern = re.compile(
        r"Thermal image\s*:\s*([A-Z0-9]+)\.JPG.*?Hotspot\s*:\s*([0-9.]+)\s*°C.*?"
        r"Coldspot\s*:\s*([0-9.]+)\s*°C.*?Emissivity\s*:\s*([0-9.]+)",
        re.I | re.S
    )

    findings = []
    for m in pattern.finditer(text):
        image_id = m.group(1)
        hotspot = float(m.group(2))
        coldspot = float(m.group(3))
        emissivity = float(m.group(4))
        delta = round(hotspot - coldspot, 2)

        findings.append({
            "image_id": image_id,
            "hotspot_c": hotspot,
            "coldspot_c": coldspot,
            "delta_c": delta,
            "emissivity": emissivity,
            "interpretation": NA,
            "mapped_area": NA
        })
    return findings
