import datetime
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from generator import HtmlGenerator

TEMPLATE_NAME = "emojize_template.html"
SHARED_TEMPLATE_FOLDER = "../../_html_templates"
OUTPUT_FILE_NAME = "emojize.html"

# render_params = {
#     "id": "file-emojize",
#     "title": "Text in Emojis umwandeln",
#     "foldername": "emojize",
#     "filename": "emojize.py",
#     "asciicast_id": "pNLj959rH9uaiAm83BegRM1cM",
#     "check50_path": "HSDDigitalLabor/problems/git2025/emojize",
#     "submit50_path": "HSDDigitalLabor/problems/git2025/emojize",
#     "timestamp": datetime.datetime.now(tz=datetime.timezone.tzname("CEST")).strftime(
#         "%Y-%m-%d %H:%M:%S"
#     ),
# }

ROOT_DIR = Path(__file__).parent.parent

if __name__ == "__main__":
    problems = sys.argv[1:]

    now_cest = datetime.datetime.now(tz=ZoneInfo("Europe/Berlin"))
    formatted = now_cest.strftime("%Y-%m-%d %H:%M:%S")

    generator = HtmlGenerator()

    for entry in ROOT_DIR.iterdir():
        if entry.is_file() or entry.name.startswith((".", "_")):
            continue

        # problem folder must contain html dir
        html_folder = entry / "html"
        if not html_folder.is_dir():
            continue

        # if a list of problems was given, but current dir is not part of it -> skip
        if problems and entry.name not in problems:
            continue

        template_file = html_folder / "template.html"

        params_path = html_folder / "params.json"
        params = None
        with Path.open(params_path, encoding="utf-8") as f:
            params = json.load(f)

        if not params:
            print(f"Failed to create {entry.name}")
            continue

        params["timestamp"] = formatted

        output_file = html_folder / Path(entry.name + ".html")

        generator.generate(template_file, params, output_file)

        print(f"{entry.name}")
