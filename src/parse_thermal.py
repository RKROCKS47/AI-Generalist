import re
from src.utils import NA

THERMAL_BLOCK = re.compile(
    r"Thermal image\s*:\s*([A-Z0-9]+)\.JPG.*?"
    r"Hotspot\s*:\s*([0-9.]+)\s*°C.*?"
    r"Coldspot\s*:\s*([0-9.]+)\s*°C.*?"
    r"Emissivity\s*:\s*([0-9.]+)",
    re.I | re.S
)

def parse_thermal_findings(thermal_text: str) -> list[dict]:
    findings = []
    for match in THERMAL_BLOCK.finditer(thermal_text):
        image_id = match.group(1)
        hotspot = float(match.group(2))
        coldspot = float(match.group(3))
        emissivity = float(match.group(4))
        delta_c = round(hotspot - coldspot, 2)

        findings.append({
            "image_id": image_id,
            "hotspot_c": hotspot,
            "coldspot_c": coldspot,
            "delta_c": delta_c,
            "emissivity": emissivity,
            "mapped_area": NA,
            "interpretation": NA
        })
    return findings
