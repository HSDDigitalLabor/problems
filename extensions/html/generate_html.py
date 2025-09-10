import os
import datetime

from jinja2 import Environment
from jinja2 import FileSystemLoader


TEMPLATE_NAME = "extensions_template.html"
SHARED_TEMPLATE_FOLDER = "../../_html_templates"
OUTPUT_FILE_NAME = "extensions.html"

render_params = {
    "id": "file-extensions",
    "title": "Dateierweiterungen",
    "foldername": "extensions",
    "filename": "extensions.py",
    "asciicast_id": "TzIkO4zM3XTEPsszr6PfEmCTN",
    "check50_path": "HSDDigitalLabor/problems/git2025/extensions",
    "submit50_path": "HSDDigitalLabor/problems/git2025/extensions",
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
}


class HtmlGenerator(object):
    def __init__(self, template_name, shared_template_folder):
        self.template_name = template_name
        self.env = Environment(loader=FileSystemLoader(shared_template_folder))

    def _build_path(self, suffix):
        # Build the full file path based on our current directory
        current_directory = os.getcwd()
        return os.path.join(current_directory, suffix)

    def generate(self):
        # Get Jinja template
        template_path = os.path.join(os.getcwd(), self.template_name)
        with open(template_path, "r", encoding="utf-8") as f:
            template_source = f.read()
        template = self.env.from_string(template_source)
        with open(
            self._build_path(OUTPUT_FILE_NAME), "w", encoding="utf-8"
        ) as html_file:
            html = template.render(render_params)
            html_file.write(html)


if __name__ == "__main__":
    print("Generating HTML...")
    html_generator = HtmlGenerator(TEMPLATE_NAME, SHARED_TEMPLATE_FOLDER)
    html_generator.generate()
