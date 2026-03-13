import os
from dotenv import load_dotenv

load_dotenv()

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

UPLOAD_DIR = os.path.join(BASE_DIR, "data", "uploads")
EXTRACTED_IMG_DIR = os.path.join(BASE_DIR, "data", "extracted", "images")
EXTRACTED_JSON_DIR = os.path.join(BASE_DIR, "data", "extracted", "json")
REPORTS_DIR = os.path.join(BASE_DIR, "data", "reports")

for path in [UPLOAD_DIR, EXTRACTED_IMG_DIR, EXTRACTED_JSON_DIR, REPORTS_DIR]:
    os.makedirs(path, exist_ok=True)

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4.1-mini")
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key")
