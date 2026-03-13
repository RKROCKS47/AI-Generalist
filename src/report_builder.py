import os
from src.pdf_extract import extract_pdf_text, extract_pdf_images
from src.parse_inspection import parse_property_details, parse_impacted_areas
from src.parse_thermal import parse_thermal_findings
from src.reasoning import generate_ddr_json
from src.utils import save_json, IMAGE_NA

def _attach_images_to_areas(area_items: list[dict], inspection_images: list[dict], thermal_images: list[dict]) -> list[dict]:
    for idx, area in enumerate(area_items):
        linked_images = []

        if idx < len(inspection_images):
            linked_images.append(os.path.relpath(inspection_images[idx]["path"]).replace("\\", "/"))
        else:
            linked_images.append(IMAGE_NA)

        if idx < len(thermal_images):
            linked_images.append(os.path.relpath(thermal_images[idx]["path"]).replace("\\", "/"))
        else:
            linked_images.append(IMAGE_NA)

        area["supporting_images"] = linked_images

    return area_items

def build_report(inspection_pdf_path: str, thermal_pdf_path: str, extracted_img_dir: str, extracted_json_dir: str) -> dict:
    inspection_img_dir = os.path.join(extracted_img_dir, "inspection")
    thermal_img_dir = os.path.join(extracted_img_dir, "thermal")

    inspection_text = extract_pdf_text(inspection_pdf_path)
    thermal_text = extract_pdf_text(thermal_pdf_path)

    inspection_images = extract_pdf_images(inspection_pdf_path, inspection_img_dir, "inspection")
    thermal_images = extract_pdf_images(thermal_pdf_path, thermal_img_dir, "thermal")

    property_details = parse_property_details(inspection_text)
    area_wise_observations = parse_impacted_areas(inspection_text)
    thermal_findings = parse_thermal_findings(thermal_text)

    area_wise_observations = _attach_images_to_areas(
        area_wise_observations, inspection_images, thermal_images
    )

    extraction_bundle = {
        "property_details": property_details,
        "area_wise_observations": area_wise_observations,
        "thermal_analysis_findings": thermal_findings,
        "raw_inspection_excerpt": inspection_text[:15000],
        "raw_thermal_excerpt": thermal_text[:15000]
    }

    save_json(os.path.join(extracted_json_dir, "extracted_bundle.json"), extraction_bundle)

    ddr_json = generate_ddr_json(extraction_bundle)
    save_json(os.path.join(extracted_json_dir, "ddr_output.json"), ddr_json)

    return ddr_json
