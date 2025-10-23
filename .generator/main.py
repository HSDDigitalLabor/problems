import datetime
import json
import sys
from pathlib import Path
from zoneinfo import ZoneInfo

from generator import HtmlGenerator

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
        if not template_file.exists() or not params_path.exists():
            print(f"Skipping {entry.name}, no template or params file")
            continue

        params = None
        with Path.open(params_path, encoding="utf-8") as f:
            params = json.load(f)

        if not params:
            print(f"Failed to create {entry.name}")
            continue

        params["timestamp"] = formatted

        output_file = html_folder / Path(entry.name + ".html")

        generator.generate(template_file, params, output_file)

        print(f"Generated {entry.name}")
