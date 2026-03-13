import os
from flask import Flask, render_template, request, redirect, url_for, send_file, flash
from werkzeug.utils import secure_filename

from config import SECRET_KEY, UPLOAD_DIR, EXTRACTED_IMG_DIR, EXTRACTED_JSON_DIR, REPORTS_DIR
from src.report_builder import build_report
from src.renderer import render_report_html

app = Flask(__name__)
app.secret_key = SECRET_KEY

@app.route("/", methods=["GET"])
def index():
    return render_template("upload.html")

@app.route("/generate", methods=["POST"])
def generate():
    inspection_file = request.files.get("inspection_pdf")
    thermal_file = request.files.get("thermal_pdf")

    if not inspection_file or not thermal_file:
        flash("Please upload both PDF files.")
        return redirect(url_for("index"))

    inspection_filename = secure_filename(inspection_file.filename)
    thermal_filename = secure_filename(thermal_file.filename)

    inspection_path = os.path.join(UPLOAD_DIR, inspection_filename)
    thermal_path = os.path.join(UPLOAD_DIR, thermal_filename)

    inspection_file.save(inspection_path)
    thermal_file.save(thermal_path)

    ddr_json = build_report(
        inspection_pdf_path=inspection_path,
        thermal_pdf_path=thermal_path,
        extracted_img_dir=EXTRACTED_IMG_DIR,
        extracted_json_dir=EXTRACTED_JSON_DIR
    )

    html_path = os.path.join(REPORTS_DIR, "main_ddr_report.html")
    render_report_html(ddr_json, "templates", html_path)

    return send_file(html_path)

if __name__ == "__main__":
    app.run(debug=True)
