import os
import fitz

def extract_images_from_pdf(pdf_path: str, output_dir: str, prefix: str) -> list[str]:
    os.makedirs(output_dir, exist_ok=True)
    doc = fitz.open(pdf_path)
    saved = []

    for page_index in range(len(doc)):
        page = doc[page_index]
        images = page.get_images(full=True)

        for img_index, img in enumerate(images, start=1):
            xref = img[0]
            base_image = doc.extract_image(xref)
            image_bytes = base_image["image"]
            ext = base_image["ext"]
            file_name = f"{prefix}_p{page_index+1}_img{img_index}.{ext}"
            out_path = os.path.join(output_dir, file_name)

            with open(out_path, "wb") as f:
                f.write(image_bytes)

            saved.append(out_path)

    doc.close()
    return saved
