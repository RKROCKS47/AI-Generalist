# web/routes.py
import os
from pathlib import Path
from typing import Tuple

from flask import (
    Blueprint,
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    send_file,
)

from core.pdf_extractor import PDFExtractor
from core.inspection_parser import InspectionParser
from core.thermal_parser import ThermalParser
from core.llm_client import LLMClient
from core.ddr_reasoner import DDRReasoner
from core.report_builder import ReportBuilder


bp = Blueprint("main", __name__)


def _save_upload(file_storage, subdir: str) -> str:
    upload_root = Path("uploads") / subdir
    upload_root.mkdir(parents=True, exist_ok=True)
    filename = file_storage.filename
    path = upload_root / filename
    file_storage.save(path)
    return str(path)


@bp.route("/", methods=["GET"])
def index():
    return render_template("upload.html")


@bp.route("/generate_ddr", methods=["POST"])
def generate_ddr():
    inspection_file = request.files.get("inspection_pdf")
    thermal_file = request.files.get("thermal_pdf")

    if not inspection_file or not thermal_file:
        return "Both inspection and thermal PDFs are required", 400

    inspection_path = _save_upload(inspection_file, "inspection")
    thermal_path = _save_upload(thermal_file, "thermal")

    # Extraction
    inspection_extractor = PDFExtractor(output_image_dir="uploads/extracted_images/inspection")
    thermal_extractor = PDFExtractor(output_image_dir="uploads/extracted_images/thermal")

    inspection_raw = inspection_extractor.extract(inspection_path)
    thermal_raw = thermal_extractor.extract(thermal_path)

    # Parsing
    inspection_parser = InspectionParser()
    thermal_parser = ThermalParser()

    inspection_data = inspection_parser.parse(inspection_raw["text"])
    thermal_data = thermal_parser.parse(thermal_raw["text"])

    # LLM Reasoning
    llm_client = LLMClient(model="gpt-4.1-mini")  # choose model as needed
    reasoner = DDRReasoner(llm_client)

    ddr_json = reasoner.generate_ddr(
        inspection_data=inspection_data,
        thermal_data=thermal_data,
        inspection_images=inspection_raw["images"],
        thermal_images=thermal_raw["images"],
    )

    # Render HTML
    report_builder = ReportBuilder(templates_dir="templates")
    html_content = report_builder.render_ddr_html(ddr_json)

    output_dir = Path("generated_reports/html")
    output_dir.mkdir(parents=True, exist_ok=True)
    report_filename = f"ddr_{Path(inspection_path).stem}.html"
    report_path = output_dir / report_filename
    report_path.write_text(html_content, encoding="utf-8")

    return html_content  # or render_template("ddr_report.html", ddr=ddr_json)


def init_routes(app: Flask):
    app.register_blueprint(bp)
