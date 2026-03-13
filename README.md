# AI-Generalist

AI-assisted Main DDR (Detailed Diagnostic Report) generator built with Flask.

This project takes two PDF inputs:
1. Inspection Report
2. Thermal Images Report

It extracts text, observations, thermal findings, and relevant images from both documents, then generates a structured client-ready Main DDR report.

---

## Overview

The goal of this project is to convert technical inspection documents into a structured and reliable Main DDR report.

The system is designed to:
- Extract relevant observations from inspection and thermal documents
- Combine information logically
- Avoid duplicate points where possible
- Handle missing or conflicting information safely
- Present the final report in clear client-friendly language
- Include relevant extracted images under area-wise observations

---

## Features

- Upload two input PDFs through a simple Flask web interface
- Extract text from Inspection Report and Thermal Report PDFs
- Extract relevant embedded images from both PDFs
- Parse property details such as property type, floors, inspection date, and inspector name
- Parse area-wise observations from inspection text
- Parse thermal analysis findings such as hotspot, coldspot, delta, and emissivity
- Generate a structured Main DDR report in HTML format
- Show `Not Available` when information is missing
- Avoid inventing facts not present in the source files

---

## DDR Output Sections

The generated report includes:

- Property Details
- Property Issue Summary
- Area-wise Observations
- Thermal Analysis Findings
- Probable Root Cause
- Severity Assessment
- Recommended Actions
- Additional Notes
- Missing Information
- Conflicts

---

## Tech Stack

- Python
- Flask
- PyMuPDF (`fitz`)
- Jinja2
- HTML/CSS

---

## Project Structure

```text
AI-Generalist/
│
├── app.py
├── config.py
├── requirements.txt
│
├── src/
│   ├── pdf_extractor.py
│   ├── image_extractor.py
│   ├── parse_inspection.py
│   ├── parse_thermal.py
│   ├── reasoning.py
│   ├── report_builder.py
│   ├── renderer.py
│   └── utils.py
│
├── templates/
│   ├── upload.html
│   └── report.html
│
├── static/
│   └── styles.css
│
├── data/
│   ├── uploads/
│   ├── extracted/
│   │   ├── images/
│   │   │   ├── inspection/
│   │   │   └── thermal/
│   │   └── json/
│   └── reports/
│
└── README.md
