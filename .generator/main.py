import argparse
import datetime
import json
from pathlib import Path
from zoneinfo import ZoneInfo

from generator import HtmlGenerator
from slugs import SLUGS

ROOT_DIR = Path(__file__).parent.parent


def _resolve_slug(args: argparse.Namespace) -> str:
    if args.course:
        return SLUGS[args.course]
    return SLUGS["GIT"]


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate problem HTML files.")
    parser.add_argument(
        "problems", nargs="*", help="Problem folder names to generate (default: all)"
    )
    parser.add_argument(
        "--course",
        choices=sorted(SLUGS.keys()),
        help="Use a predefined slug by course key (GIT, ADG, PRAK)",
    )
    parser.add_argument(
        "--list-courses",
        action="store_true",
        help="Print available course keys and slugs, then exit",
    )
    args = parser.parse_args()
    if args.list_courses:
        for key in sorted(SLUGS):
            print(f"{key}: {SLUGS[key]}")
        raise SystemExit(0)
    problems = args.problems
    slug = _resolve_slug(args)

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
        params["slug"] = slug

        output_file = html_folder / Path(entry.name + ".html")

        generator.generate(template_file, params, output_file)

        print(f"Generated {entry.name}")
