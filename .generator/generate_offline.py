"""Generate an offline-ready copy of all problem pages in a self-contained folder.

Creates OUTPUT_DIR (default: _html_output/) with:
  - index.html      – overview page with links to all problem pages
  - {problem}.html  – standalone Bootstrap HTML page per problem
    - assets/         – shared images, .cast, .mp4 files

Moodle image URLs (https://mdl.hs-duesseldorf.de/draftfile.php/...)
are replaced with the corresponding local filenames found in each
problem's html/ subfolder.

Usage:
    python .generator/generate_offline.py              # → _html_output/
    python .generator/generate_offline.py my_output   # → my_output/
"""

import argparse
import datetime
import json
import re
import shutil
from jinja2 import ChoiceLoader, DictLoader
from pathlib import Path
from urllib.parse import unquote
from zoneinfo import ZoneInfo

from generator import HtmlGenerator
from slugs import SLUGS

ROOT_DIR = Path(__file__).parent.parent
DEFAULT_OUTPUT_DIR = "_html_output"

ASSET_EXTENSIONS = frozenset({
    ".png",
    ".jpg",
    ".jpeg",
    ".gif",
    ".webp",
    ".svg",
    ".mp4",
    ".cast",
})

MOODLE_URL_RE = re.compile(
    r"https://mdl\.hs-duesseldorf\.de/draftfile\.php/[^\s\"'<>]+",
    re.IGNORECASE,
)

BOOTSTRAP_CDN = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/css/bootstrap.min.css"
)
BOOTSTRAP_JS = (
    "https://cdn.jsdelivr.net/npm/bootstrap@5.3.3/dist/js/bootstrap.bundle.min.js"
)

_PAGE_WRAPPER = """\
<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>{title}</title>
  <link rel="stylesheet" href="{bootstrap}">
  <link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/@fortawesome/fontawesome-free@6.7.2/css/all.min.css">
  <style>
    pre {{ overflow-x: auto; }}
  </style>
</head>
<body>
<main class="container py-4">
    <p class="text-muted mb-4"><a href="{back_href}">&larr; Zurück zur Übersicht</a></p>
{body}
</main>
</body>
</html>"""


def _normalize_slug(slug: str) -> str:
    return slug if slug.endswith("/") else slug + "/"


# ── Moodle URL → local filename resolution ─────────────────────────────────────


def _resolve_moodle_url(url: str, html_dir: Path) -> str | None:
    """Map a Moodle draftfile URL to a local filename in html_dir.

    Tries three strategies in order:
      1. Exact URL-decoded filename match.
      2. Strip Moodle copy suffixes like " (1)" before extension.
      3. Stem-based match (first asset file whose stem matches).

    Returns the local filename on success, or None if no match is found.
    """
    raw = url.rstrip("/").split("/")[-1]
    decoded = unquote(raw)

    # 1. Exact match
    if (html_dir / decoded).exists():
        return decoded

    # 2. Strip Moodle copy suffix, e.g. "file (1).png" → "file.png"
    cleaned = re.sub(r"\s*\(\d+\)(?=\.[^.]+$)", "", decoded)
    if cleaned != decoded and (html_dir / cleaned).exists():
        return cleaned

    # 3. Stem-based fallback: find first asset whose stem matches
    target_stem = re.sub(r"\s*\(\d+\)$", "", Path(decoded).stem).lower()
    for f in sorted(html_dir.iterdir()):
        if (
            f.is_file()
            and f.suffix.lower() in ASSET_EXTENSIONS
            and f.stem.lower() == target_stem
        ):
            return f.name

    return None


def _replace_moodle_urls(html: str, html_dir: Path) -> tuple[str, list[str]]:
    """Replace Moodle URLs in *html* with local filenames.

    Returns ``(modified_html, list_of_unresolved_urls)``.
    """
    unresolved: list[str] = []

    def replacer(m: re.Match) -> str:
        local = _resolve_moodle_url(m.group(), html_dir)
        if local is not None:
            return local
        unresolved.append(m.group())
        return m.group()

    return MOODLE_URL_RE.sub(replacer, html), unresolved


# ── Asset copying ──────────────────────────────────────────────────────────────


def _copy_assets(html_dir: Path, assets_dir: Path) -> None:
    """Copy all asset files from *html_dir* to shared *assets_dir* (skip unchanged)."""
    assets_dir.mkdir(parents=True, exist_ok=True)
    for f in html_dir.iterdir():
        if f.is_file() and f.suffix.lower() in ASSET_EXTENSIONS:
            dest = assets_dir / f.name
            if not dest.exists() or dest.stat().st_mtime < f.stat().st_mtime:
                shutil.copy2(f, dest)


# ── HTML page wrapping ─────────────────────────────────────────────────────────


def _wrap_in_page(body: str, title: str, back_href: str = "index.html") -> str:
    return _PAGE_WRAPPER.format(
        title=title,
        bootstrap=BOOTSTRAP_CDN,
        back_href=back_href,
        body=body,
    )


def _rewrite_local_asset_links(html: str, html_dir: Path, asset_prefix: str) -> str:
    """Rewrite local asset src/href/poster links to the shared assets folder."""
    asset_files = {
        f.name
        for f in html_dir.iterdir()
        if f.is_file() and f.suffix.lower() in ASSET_EXTENSIONS
    }
    if not asset_files:
        return html

    attr_re = re.compile(
        r'(?P<attr>\b(?:src|href|poster)\s*=\s*)(?P<q>["\'])(?P<val>[^"\']+)(?P=q)',
        re.IGNORECASE,
    )

    def repl(m: re.Match) -> str:
        attr = m.group("attr")
        q = m.group("q")
        val = m.group("val")
        lower = val.lower()

        if lower.startswith((
            "http://",
            "https://",
            "data:",
            "mailto:",
            "#",
            "javascript:",
        )):
            return m.group(0)

        if val.startswith(asset_prefix):
            return m.group(0)

        candidate = Path(unquote(val)).name
        if candidate in asset_files:
            return f"{attr}{q}{asset_prefix}{candidate}{q}"

        return m.group(0)

    return attr_re.sub(repl, html)


# ── Index page generation ──────────────────────────────────────────────────────

_PROG0_ENTRIES = [
    {
        "title": "Scratch: Binärzähler",
        "href": "binary_count.html",
        "folder": "binary_count",
    },
    {
        "title": "GitHub-Benutzerkonto erstellen",
        "href": "create_github.html",
        "folder": "create_github",
    },
    {
        "title": "MathWorks-Account erstellen",
        "href": "create_mathworks.html",
        "folder": "create_mathworks",
    },
    {
        "title": "CS50-Subscription",
        "href": "cs50_subscription.html",
        "folder": "cs50_subscription",
    },
]

_GIT_GROUPS: dict[str, list[str]] = {
    "Programmieraufgabe 1": [
        "willkommen",
        "hello",
        "strings",
        "playback",
        "faces",
        "einstein",
        "emojize",
        "tip",
    ],
    "Programmieraufgabe 2": [
        "extensions",
        "luhn",
        "divide-integers",
        "nadel",
        "interpreter",
        "zahlenjagd",
        "tip",
        "playback",
    ],
    "Programmieraufgabe 3": [
        "palindrom",
        "linear",
        "binary",
        "insert",
        "iban",
        "hackers",
    ],
    "Programmieraufgabe 4": [
        "bogo",
        "bubble",
        "merge",
        "run_back",
        "rotate",
        "intervals",
    ],
    "Programmieraufgabe 5": [
        "neuner",
        "sudoku1",
        "sudoku2",
        "zeilen",
        "stufen",
        "einsen",
    ],
}

_ADG_GROUPS: dict[str, list[str]] = {
    "Programmieraufgabe 6": [
        "linkedFind",
        "linkedInsert",
        "linkedAfter",
        "linkedRemove",
        "linkedMerge",
        "linkedStack",
    ],
}

# 13 easiest problems for the PRAK course (Einführung + first 3 of Strings & Zahlen)
_PRAK_PROBLEMS: list[str] = [
    "willkommen",
    "hello",
    "strings",
    "einstein",
    "emojize",
    "extensions",
    "faces",
    "tip",
    "playback",
    "luhn",
    "zahlenjagd",
    "iban",
]


def _card(title: str, href: str, folder: str) -> str:
    return (
        f'      <div class="col">\n'
        f'        <a href="{href}" style="text-decoration:none;color:inherit">\n'
        f'          <div class="card h-100 border">\n'
        f'            <div class="card-body">\n'
        f'              <h6 class="card-title mb-1">{title}</h6>\n'
        f'              <span class="badge bg-secondary" style="font-size:.7em;font-family:monospace">{folder}</span>\n'
        f"            </div>\n"
        f"          </div>\n"
        f"        </a>\n"
        f"      </div>"
    )


def _subsection(heading: str, cards: list[str]) -> str:
    inner = "\n".join(cards)
    return (
        f'    <h5 style="border-left:3px solid #6c757d;padding-left:.6rem;color:#495057" class="mb-3 mt-4">{heading}</h5>\n'
        f'    <div class="row row-cols-1 row-cols-md-3 g-3 mb-4">\n'
        f"{inner}\n"
        f"    </div>"
    )


def _group_html(
    groups: dict[str, list[str]], params: dict, link_prefix: str = ""
) -> str:
    parts = []
    for heading, folders in groups.items():
        cards = [
            _card(params[f]["title"], f"{link_prefix}{f}.html", f)
            for f in folders
            if f in params
        ]
        if cards:
            parts.append(_subsection(heading, cards))
    return "\n\n".join(parts)


def _generate_index(
    params: dict,
    timestamp: str,
    active_course: str = "ADG",
    tab_prefixes: dict[str, str] | None = None,
    visible_courses: list[str] | None = None,
) -> str:
    tab_prefixes = tab_prefixes or {"ADG": "", "GIT": "", "PRAK": ""}

    def prog0_section(link_prefix: str, course: str) -> str:
        prog_cards = "\n".join(
            _card(e["title"], f"{link_prefix}{e['href']}", e["folder"])
            for e in _PROG0_ENTRIES
            if course == "GIT" or e["href"] != "create_mathworks.html"
        )
        return (
            f'    <h2 class="section-heading mb-4">Vorbereitung &ndash; Programmieraufgabe 0</h2>\n'
            f'    <div class="row row-cols-1 row-cols-md-3 g-3 mb-5">\n'
            f"{prog_cards}\n"
            f"    </div>\n"
        )

    def git_section(link_prefix: str) -> str:
        return (
            f'    <h2 class="section-heading mb-4">GIT II &ndash; Aufgaben 2025</h2>\n'
            f"{_group_html(_GIT_GROUPS, params, link_prefix=link_prefix)}\n"
        )

    def adg_section(link_prefix: str) -> str:
        return (
            f'    <h2 class="section-heading mb-4">ADG &ndash; Aufgaben 2025</h2>\n'
            f"{_group_html(_GIT_GROUPS, params, link_prefix=link_prefix)}\n"
            f"{_group_html(_ADG_GROUPS, params, link_prefix=link_prefix)}\n"
        )

    def prak_section(link_prefix: str) -> str:
        prak_cards = "\n".join(
            _card(params[f]["title"], f"{link_prefix}{f}.html", f)
            for f in _PRAK_PROBLEMS
            if f in params
        )
        return (
            f'    <h2 class="section-heading mb-4">Praktikumsaufgaben</h2>\n'
            f'    <div class="row row-cols-1 row-cols-md-3 g-3">\n'
            f"{prak_cards}\n"
            f"    </div>\n"
        )

    tab_adg = prog0_section(tab_prefixes.get("ADG", ""), "ADG") + adg_section(
        tab_prefixes.get("ADG", "")
    )
    tab_git = prog0_section(tab_prefixes.get("GIT", ""), "GIT") + git_section(
        tab_prefixes.get("GIT", "")
    )
    tab_prak = prog0_section(tab_prefixes.get("PRAK", ""), "PRAK") + prak_section(
        tab_prefixes.get("PRAK", "")
    )

    all_courses = ["ADG", "GIT", "PRAK"]
    if visible_courses:
        seen: set[str] = set()
        normalized = []
        for c in visible_courses:
            if c in all_courses and c not in seen:
                normalized.append(c)
                seen.add(c)
        courses = normalized or all_courses
    else:
        courses = all_courses

    if active_course not in courses:
        active_course = courses[0]

    labels = {"ADG": "ADG", "GIT": "GIT", "PRAK": "PRAK"}
    pane_ids = {"ADG": "tab-git-adg", "GIT": "tab-git", "PRAK": "tab-prak"}
    button_ids = {
        "ADG": "tab-git-adg-btn",
        "GIT": "tab-git-btn",
        "PRAK": "tab-prak-btn",
    }
    contents = {"ADG": tab_adg, "GIT": tab_git, "PRAK": tab_prak}

    nav_items: list[str] = []
    pane_items: list[str] = []
    for course in courses:
        is_active = course == active_course
        btn_class = "nav-link active" if is_active else "nav-link"
        pane_class = "tab-pane fade show active" if is_active else "tab-pane fade"
        nav_items.append(
            f"""    <li class="nav-item" role="presentation">\n"""
            f'''      <button class="{btn_class}" id="{button_ids[course]}" data-bs-toggle="tab"\n'''
            f"""              data-bs-target="#{pane_ids[course]}" type="button" role="tab">{labels[course]}</button>\n"""
            f"""    </li>"""
        )
        pane_items.append(
            f'''    <div class="{pane_class}" id="{pane_ids[course]}" role="tabpanel">\n'''
            f"""{contents[course]}\n"""
            f"""    </div>"""
        )

    nav_html = "\n".join(nav_items)
    panes_html = "\n\n".join(pane_items)

    return f"""<!DOCTYPE html>
<html lang="de">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Programmieraufgaben – GIT II / ADG 2025</title>
  <link rel="stylesheet" href="{BOOTSTRAP_CDN}">
  <style>
    body {{ background-color: #f8f9fa; }}
    .section-heading {{ border-left: 4px solid #0d6efd; padding-left: .75rem; }}
  </style>
</head>
<body>
<div class="container py-5">

  <div class="mb-4">
    <h1 class="display-5 fw-bold">Programmieraufgaben Übersicht</h1>
    <p class="lead text-muted">BA 1WS EI/IT/WI &ndash; HSD Hochschule Düsseldorf &nbsp;|&nbsp; 2025</p>
    <hr>
  </div>

  <!-- Tab navigation -->
  <ul class="nav nav-tabs mb-4" id="courseTabs" role="tablist">
{nav_html}
  </ul>

  <!-- Tab content -->
  <div class="tab-content" id="courseTabsContent">
{panes_html}
  </div>

  <footer class="text-muted text-end mt-5" style="font-size:.75em">
    <hr>
    HSD Hochschule Düsseldorf &ndash; BA 1WS EI/IT/WI &ndash; GIT II / ADG 2025
    &nbsp;|&nbsp; generated {timestamp}
  </footer>

</div>
<script src="{BOOTSTRAP_JS}"></script>
</body>
</html>"""


def _generate_offline_set(
    output_dir: Path,
    slug: str,
    timestamp: str,
    gen: HtmlGenerator,
    assets_dir: Path,
    course_key: str,
    back_href: str = "index.html",
    asset_prefix: str = "assets/",
) -> dict[str, dict]:
    output_dir.mkdir(parents=True, exist_ok=True)
    all_params: dict[str, dict] = {}

    # ── Regular problem folders ────────────────────────────────────────────
    for entry in sorted(ROOT_DIR.iterdir()):
        if entry.is_file() or entry.name.startswith((".", "_")):
            continue
        if entry.name == "Programmieraufgabe_0":
            continue  # handled separately below

        html_dir = entry / "html"
        if not html_dir.is_dir():
            continue

        template_file = html_dir / "template.html"
        params_path = html_dir / "params.json"
        if not template_file.exists() or not params_path.exists():
            print(f"  skip  {entry.name} (no template/params)")
            continue

        with params_path.open(encoding="utf-8") as f:
            params = json.load(f)
        params["timestamp"] = timestamp
        params["slug"] = slug
        all_params[entry.name] = params

        # Render template fragment
        body = gen.render(template_file, params)

        # Replace Moodle image URLs with local filenames
        body, unresolved = _replace_moodle_urls(body, html_dir)
        for url in unresolved:
            print(f"  WARN  {entry.name}: unresolved Moodle URL: {url}")

        body = _rewrite_local_asset_links(body, html_dir, asset_prefix)

        # Write full standalone HTML page
        (output_dir / f"{entry.name}.html").write_text(
            _wrap_in_page(body, params.get("title", entry.name), back_href=back_href),
            encoding="utf-8",
        )

        # Copy all asset files from html/ to shared assets folder
        _copy_assets(html_dir, assets_dir)

        print(f"  ok    {entry.name}")

    # ── Programmieraufgabe_0 (pre-generated HTML fragments) ───────────────
    prog0_html_dir = ROOT_DIR / "Programmieraufgabe_0" / "html"
    if prog0_html_dir.is_dir():
        for html_file in sorted(prog0_html_dir.glob("*.html")):
            if course_key != "GIT" and html_file.name == "create_mathworks.html":
                continue
            body = html_file.read_text(encoding="utf-8")
            body, unresolved = _replace_moodle_urls(body, prog0_html_dir)
            for url in unresolved:
                print(
                    f"  WARN  Programmieraufgabe_0/{html_file.name}: unresolved URL: {url}"
                )
            title = html_file.stem.replace("_", " ").title()
            body = _rewrite_local_asset_links(body, prog0_html_dir, asset_prefix)
            (output_dir / html_file.name).write_text(
                _wrap_in_page(body, title, back_href=back_href),
                encoding="utf-8",
            )
            print(f"  ok    Programmieraufgabe_0/{html_file.name}")
        _copy_assets(prog0_html_dir, assets_dir)

    return all_params


# ── Entry point ────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Generate offline HTML copy of all problems."
    )
    parser.add_argument(
        "output_dir",
        nargs="?",
        default=DEFAULT_OUTPUT_DIR,
        help="Output directory name relative to repo root (default: %(default)s)",
    )
    parser.add_argument(
        "--courses",
        nargs="+",
        choices=sorted(SLUGS.keys()),
        help="Generate subfolders for selected course keys (e.g. --courses GIT ADG PRAK)",
    )
    parser.add_argument(
        "--list_courses",
        action="store_true",
        help="Print available course keys and slugs, then exit",
    )
    args = parser.parse_args()
    if args.list_courses:
        for key in sorted(SLUGS):
            print(f"{key}: {SLUGS[key]}")
        raise SystemExit(0)
    output_dir = ROOT_DIR / args.output_dir
    output_dir.mkdir(parents=True, exist_ok=True)

    now = datetime.datetime.now(tz=ZoneInfo("Europe/Berlin"))
    timestamp = now.strftime("%Y-%m-%d %H:%M:%S")

    # Use absolute path for template folder so the script works from any cwd
    gen = HtmlGenerator(str(ROOT_DIR / "_html_templates"))
    # Suppress Moodle-specific sections that are irrelevant offline
    gen.env.loader = ChoiceLoader([
        DictLoader({"how_to_mark_in_moodle.html": ""}),
        gen.env.loader,
    ])

    # Multi-course mode (default: all courses)
    selected: list[str] = []
    seen: set[str] = set()
    source_courses = args.courses if args.courses else list(SLUGS.keys())
    for c in source_courses:
        if c not in seen:
            selected.append(c)
            seen.add(c)

    assets_dir = output_dir / "assets"
    index_params: dict[str, dict] | None = None
    for course in selected:
        course_dir = output_dir / course.lower()
        slug = _normalize_slug(SLUGS[course])
        print(f"\n=== Generating {course} in {course_dir.name}/ with slug {slug} ===")
        index_params = _generate_offline_set(
            course_dir,
            slug,
            timestamp,
            gen,
            assets_dir=assets_dir,
            course_key=course,
            back_href="../index.html",
            asset_prefix="../assets/",
        )

    if index_params is not None:
        prefixes = {course: f"{course.lower()}/" for course in selected}
        (output_dir / "index.html").write_text(
            _generate_index(
                index_params,
                timestamp,
                active_course=selected[0],
                tab_prefixes=prefixes,
                visible_courses=selected,
            ),
            encoding="utf-8",
        )
        print("  ok    index.html")

    print(f"\nOutput → {output_dir}")
