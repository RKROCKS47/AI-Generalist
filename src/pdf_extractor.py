import os
import fitz

def extract_pdf_text(pdf_path: str) -> str:
    doc = fitz.open(pdf_path)
    pages = []
    for i, page in enumerate(doc):
        text = page.get_text("text")
        pages.append(f"\n--- PAGE {i + 1} ---\n{text}")
    doc.close()
    return "\n".join(pages)

def extract_pdf_images(pdf_path: str, output_dir: str, prefix: str) -> list[dict]:
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    images_meta = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        page_images = page.get_images(full=True)

        for image_index, img in enumerate(page_images, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]

            filename = f"{prefix}_page{page_index+1}_img{image_index}.{ext}"
            out_path = os.path.join(output_dir, filename)

            with open(out_path, "wb") as f:
                f.write(image_bytes)

            images_meta.append({
                "page": page_index + 1,
                "filename": filename,
                "path": out_path
            })

    doc.close()
    return images_meta
