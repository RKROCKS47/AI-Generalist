# core/inspection_parser.py
import re
from typing import Dict, Any


class InspectionParser:
    def parse(self, raw_text: str) -> Dict[str, Any]:
        """
        Very conservative parser:
        - Attempts to extract property meta
        - Captures sectioned text blocks
        - Leaves many fields as 'Not Available' if not found
        """
        lines = [l.strip() for l in raw_text.splitlines() if l.strip()]
        text_joined = "\n".join(lines)

        property_details = self._extract_property_details(text_joined)
        sections = self._split_sections(text_joined)

        return {
            "property_details": property_details,
            "sections": sections,
        }

    def _extract_property_details(self, text: str) -> Dict[str, str]:
        def find_after(label: str) -> str:
            pattern = rf"{re.escape(label)}\s*(.+)"
            match = re.search(pattern, text, re.IGNORECASE)
            return match.group(1).strip() if match else "Not Available"

        return {
            "customer_name": find_after("Customer Name"),
            "flat_or_unit_no": find_after("Flat No"),
            "address": find_after("Customer Full Address"),
            "property_type": find_after("Property Type"),
            "structure_type": find_after("Type of structure"),
            "floors": find_after("Floors"),
            "age_years": find_after("Age Building years"),
            "inspection_date": find_after("Date of Inspection"),
            "inspected_by": find_after("Inspected By"),
        }

    def _split_sections(self, text: str) -> Dict[str, str]:
        """
        For reports similar to Main-DDR, where sections are labeled:
        'SECTION 1 INTRODUCTION', 'SECTION 2 GENERAL INFORMATION', etc. [file:1]
        """
        pattern = r"(SECTION\s+\d+\s+[A-Z][A-Z\s]+)"
        parts = re.split(pattern, text)
        sections = {}

        # parts = ["before", "SECTION 1 INTRODUCTION", "content1",
        #          "SECTION 2 GENERAL INFORMATION", "content2", ...]
        current_title = "FULL_TEXT"
        current_content = []

        for part in parts:
            if part.startswith("SECTION"):
                if current_content:
                    sections[current_title] = "\n".join(current_content).strip()
                current_title = part.strip()
                current_content = []
            else:
                current_content.append(part)

        if current_content:
            sections[current_title] = "\n".join(current_content).strip()

        return sections
