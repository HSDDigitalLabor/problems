from pathlib import Path

from jinja2 import Environment, FileSystemLoader


class HtmlGenerator:
    def __init__(self, shared_template_folder="_html_templates"):
        self.SHARED_TEMPLATE_FOLDER = shared_template_folder
        self.env = Environment(loader=FileSystemLoader(self.SHARED_TEMPLATE_FOLDER))

    def render(self, template_path: Path | str, params: dict) -> str:
        """Render a template with params and return the result as a string."""
        template_path = Path(template_path)
        with Path.open(template_path, encoding="utf-8") as f:
            template_source = f.read()
        template = self.env.from_string(template_source)
        return template.render(params)

    def generate(
        self, template_path: Path | str, params: dict, output_file_name: Path | str
    ):
        output_file_name = Path(output_file_name)
        html = self.render(template_path, params)
        with Path.open(output_file_name, "w", encoding="utf-8") as html_file:
            html_file.write(html)
