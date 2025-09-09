import os
import datetime

from jinja2 import Environment
from jinja2 import FileSystemLoader


TEMPLATE_NAME = 'faces_template.html'
OUTPUT_FILE_NAME = 'faces.html'

render_params = {
    "id": "faces",
    "title": "Emoticons zu Emojis umwandeln",
    "foldername": "faces",
    "filename": "faces.py",
    "asciicast_id": "6czzIos2pDdpLNtkGYxuHVofv",
    "check50_path": "HSDDigitalLabor/problems/git2025/faces",
    "submit50_path": "HSDDigitalLabor/problems/git2025/faces",
    "timestamp": datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
}

class HtmlGenerator(object):
    def __init__(self, template_name):
        self.template_name = template_name
        self.env = Environment(loader=FileSystemLoader('../../html_templates'))

    def _build_path(self, suffix):
        # Build the full file path based on our current directory
        current_directory = os.getcwd()
        return os.path.join(current_directory, suffix)

    def generate(self):
        # Get Jinja template
        template_path = os.path.join(os.getcwd(), self.template_name)
        with open(template_path, 'r', encoding='utf-8') as f:
            template_source = f.read()
        template = self.env.from_string(template_source)
        with open(self._build_path(OUTPUT_FILE_NAME), 'w', encoding='utf-8') as html_file:
            html = template.render(render_params)
            html_file.write(html)

if __name__ == '__main__':
    print("Generating HTML...")
    html_generator = HtmlGenerator(TEMPLATE_NAME)
    html_generator.generate()