# core/thermal_parser.py
import re
from typing import List, Dict, Any


class ThermalParser:
    def parse(self, raw_text: str) -> Dict[str, Any]:
        entries: List[Dict[str, Any]] = []

        # Each “Thermal image ...” block
        pattern = (
            r"Thermal image\s+([A-Z0-9_.]+).*?"
            r"Hotspot\s+([\d.]+)\s*C.*?"
            r"Coldspot\s+([\d.]+)\s*C.*?"
            r"Emissivity\s+([\d.]+).*?"
            r"Reflected temperature\s+([\d.]+)\s*C"
        )

        for match in re.finditer(pattern, raw_text, re.DOTALL):
            image_name, hotspot, coldspot, emissivity, tref = match.groups()
            entries.append(
                {
                    "image_name": image_name,
                    "hotspot_c": float(hotspot),
                    "coldspot_c": float(coldspot),
                    "delta_c": float(hotspot) - float(coldspot),
                    "emissivity": float(emissivity),
                    "reflected_temp_c": float(tref),
                }
            )

        # Aggregate stats (helps LLM reason briefly)
        if entries:
            avg_delta = sum(e["delta_c"] for e in entries) / len(entries)
        else:
            avg_delta = None

        return {
            "entries": entries,
            "summary": {
                "count": len(entries),
                "avg_delta_c": avg_delta,
            },
        }
