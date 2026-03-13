# core/pdf_extractor.py
import os
from pathlib import Path
from typing import List, Dict, Any

import fitz  # PyMuPDF


class PDFExtractor:
    def __init__(self, output_image_dir: str):
        self.output_image_dir = Path(output_image_dir)
        self.output_image_dir.mkdir(parents=True, exist_ok=True)

    def extract(self, pdf_path: str) -> Dict[str, Any]:
        doc = fitz.open(pdf_path)
        pages_text: List[str] = []
        images_meta: List[Dict[str, Any]] = []

        for page_index in range(len(doc)):
            page = doc[page_index]
            pages_text.append(page.get_text("text"))

            for img_index, img in enumerate(page.get_images(full=True)):
                xref = img[0]
                base_image = doc.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_name = f"{Path(pdf_path).stem}_p{page_index}_i{img_index}.{image_ext}"
                image_path = self.output_image_dir / image_name

                with open(image_path, "wb") as f:
                    f.write(image_bytes)

                images_meta.append(
                    {
                        "page": page_index,
                        "name": image_name,
                        "path": str(image_path),
                        "width": base_image.get("width"),
                        "height": base_image.get("height"),
                    }
                )

        doc.close()
        return {
            "text": "\n\n".join(pages_text),
            "images": images_meta,
        }
