import os
from jinja2 import Environment, FileSystemLoader, select_autoescape

def render_report_html(ddr_json: dict, templates_dir: str, output_path: str) -> str:
    env = Environment(
        loader=FileSystemLoader(templates_dir),
        autoescape=select_autoescape(["html", "xml"])
    )
    template = env.get_template("report.html")
    html = template.render(report=ddr_json)

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(html)

    return output_path
