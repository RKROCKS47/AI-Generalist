# core/report_builder.py
from pathlib import Path
from typing import Dict, Any

from jinja2 import Environment, FileSystemLoader, select_autoescape


class ReportBuilder:
    def __init__(self, templates_dir: str):
        self.env = Environment(
            loader=FileSystemLoader(templates_dir),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

    def render_ddr_html(self, ddr_data: Dict[str, Any]) -> str:
        template = self.env.get_template("ddr_report.html")
        return template.render(ddr=ddr_data)
