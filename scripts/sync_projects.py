#!/usr/bin/env python3
"""Sync the shared projects sheet into project pages and _data/projects.yml."""

from __future__ import annotations

import argparse
import csv
import html
import io
import json
import re
import shutil
import urllib.request
from datetime import datetime
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "shared" / "projects_sync.json"
DEFAULT_SOURCE = ROOT / "shared" / "projects_sheet.csv"
DEFAULT_OUTPUT = ROOT / "_data" / "projects.yml"
DEFAULT_PROJECTS_DIR = ROOT / "_projects"
DEFAULT_IMAGES_SOURCE = ROOT / "shared" / "project_images_uploads"
DEFAULT_IMAGES_DEST = ROOT / "assets" / "projects"
USER_AGENT = "ArcoLabProjectsSync/1.0 (arcolabucbm@gmail.com)"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")

FIELD_ORDER = [
    "status",
    "name",
    "slug",
    "full_title",
    "project_state",
    "project_type",
    "img",
    "collaborators",
    "start_year",
    "end_year",
    "overview",
    "grant_number",
    "research_directions",
    "project_filter",
    "official_page",
    "description",
    "focus_areas",
]

REQUIRED_COLUMNS = {
    "status",
    "name",
    "full_title",
    "collaborators",
    "start_year",
    "end_year",
    "overview",
    "grant_number",
    "research_directions",
    "project_filter",
}

SKIP_STATUSES = {"draft", "ignore", "skip"}


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def log(message: str) -> None:
    print(message)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def slugify(value: str) -> str:
    value = normalize_space(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-")


def split_list(value: str) -> list[str]:
    return [normalize_space(item) for item in re.split(r"\s*;\s*", value or "") if normalize_space(item)]


def split_paragraphs(value: str) -> list[str]:
    chunks = re.split(r"\s*\|\|\s*|\n\s*\n", value or "")
    return [normalize_space(chunk) for chunk in chunks if normalize_space(chunk)]


def normalize_google_sheet_source(source: str) -> str:
    source = normalize_space(source)
    if not source.startswith("https://docs.google.com/spreadsheets/d/"):
        return source
    if "output=csv" in source or "/gviz/tq?" in source:
        return source
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", source)
    if not match:
        return source
    spreadsheet_id = match.group(1)
    gid_match = re.search(r"[?#&]gid=([0-9]+)", source)
    gid = gid_match.group(1) if gid_match else "0"
    return f"https://docs.google.com/spreadsheets/d/{spreadsheet_id}/export?format=csv&gid={gid}"


def drive_folder_id(source: str) -> str:
    source = normalize_space(source)
    patterns = (
        r"/folders/([a-zA-Z0-9_-]+)",
        r"[?&]id=([a-zA-Z0-9_-]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, source)
        if match:
            return match.group(1)
    return ""


def drive_file_id(source: str) -> str:
    source = normalize_space(source)
    patterns = (
        r"/file/d/([a-zA-Z0-9_-]+)",
        r"[?&]id=([a-zA-Z0-9_-]+)",
    )
    for pattern in patterns:
        match = re.search(pattern, source)
        if match:
            return match.group(1)
    return ""


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", errors="ignore")


def parse_drive_folder_listing(folder_url: str) -> list[dict[str, str]]:
    folder_id = drive_folder_id(folder_url)
    if not folder_id:
        return []

    listing_url = f"https://drive.google.com/embeddedfolderview?id={folder_id}#list"
    try:
        listing_html = fetch_text(listing_url)
    except Exception as exc:  # noqa: BLE001
        log(f"Warning: could not fetch Google Drive project image folder listing: {exc}")
        return []

    files: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    patterns = (
        re.compile(
            r'<a href="https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view[^"]*"[^>]*>.*?<div class="flip-entry-title">([^<]+)</div>',
            re.IGNORECASE | re.DOTALL,
        ),
        re.compile(
            r'href="https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view[^"]*"[^>]*>.*?>([^<]+\.(?:png|jpe?g|webp))<',
            re.IGNORECASE | re.DOTALL,
        ),
    )
    for pattern in patterns:
        for match in pattern.finditer(listing_html):
            file_id = match.group(1)
            filename = normalize_space(match.group(2))
            if not filename or file_id in seen_ids:
                continue
            seen_ids.add(file_id)
            files.append(
                {
                    "id": file_id,
                    "name": filename,
                    "download_url": f"https://drive.google.com/uc?export=download&id={file_id}",
                }
            )
    return files


def download_drive_images(folder_url: str, destination: Path) -> None:
    folder_url = normalize_space(folder_url)
    if not folder_url:
        return

    destination.mkdir(parents=True, exist_ok=True)
    files = parse_drive_folder_listing(folder_url)
    if not files:
        log("Warning: no downloadable files were discovered in the Google Drive project image folder.")
        return

    for file_info in files:
        filename = normalize_space(file_info["name"])
        if not filename.lower().endswith(IMAGE_EXTENSIONS):
            continue
        try:
            request = urllib.request.Request(file_info["download_url"], headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                (destination / filename).write_bytes(response.read())
        except Exception as exc:  # noqa: BLE001
            log(f"Warning: failed to download Drive project image {filename}: {exc}")


def yaml_quote(value: str) -> str:
    escaped = str(value).replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def csv_join(items: list[str]) -> str:
    return "; ".join(item for item in items if item)


def load_rows(source: str, mirror_path: Path | None = None) -> list[dict[str, str]]:
    normalized_source = normalize_google_sheet_source(source)
    if re.match(r"^https?://", normalized_source):
        request = urllib.request.Request(normalized_source, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8-sig")
        if mirror_path is not None:
            mirror_path.write_text(raw, encoding="utf-8")
    else:
        raw = Path(normalized_source).read_text(encoding="utf-8-sig")

    reader = csv.DictReader(io.StringIO(raw))
    if reader.fieldnames is None:
        raise ValueError("The projects sheet is empty or missing a header row.")

    fieldnames = {name.strip() for name in reader.fieldnames if name}
    missing = REQUIRED_COLUMNS - fieldnames
    if missing:
        raise ValueError("Missing required CSV columns: " + ", ".join(sorted(missing)))

    rows = []
    for row in reader:
        cleaned = {key.strip(): normalize_space(value) for key, value in row.items() if key}
        if any(cleaned.values()):
            rows.append(cleaned)
    return rows


def clean_yaml_scalar(value: str) -> str:
    value = normalize_space(value)
    if len(value) >= 2 and value[0] == value[-1] and value[0] in {"'", '"'}:
        value = value[1:-1]
    return value


def parse_frontmatter(path: Path) -> tuple[dict[str, Any], str]:
    content = path.read_text(encoding="utf-8")
    if not content.startswith("---"):
        return {}, content
    parts = content.split("---", 2)
    if len(parts) < 3:
        return {}, content
    frontmatter = parts[1]
    body = parts[2]
    data: dict[str, Any] = {}
    current_key = ""
    for raw_line in frontmatter.splitlines():
        if not raw_line.strip():
            continue
        key_match = re.match(r"^([A-Za-z0-9_]+):\s*(.*)$", raw_line)
        if key_match:
            current_key = key_match.group(1)
            value = key_match.group(2)
            data[current_key] = clean_yaml_scalar(value) if value else []
            continue
        item_match = re.match(r"^\s*-\s*(.*)$", raw_line)
        if item_match and current_key:
            data.setdefault(current_key, [])
            if isinstance(data[current_key], list):
                data[current_key].append(clean_yaml_scalar(item_match.group(1)))
    return data, body


def html_to_text(value: str) -> str:
    value = re.sub(r"<[^>]+>", " ", value)
    return normalize_space(html.unescape(value))


def extract_overview(body: str) -> str:
    match = re.search(r"<h2>Overview</h2>(.*?)(?:</div>\s*<aside|</div>\s*</div>)", body, re.DOTALL)
    if not match:
        return ""
    paragraphs = [html_to_text(item) for item in re.findall(r"<p>\s*(.*?)\s*</p>", match.group(1), re.DOTALL)]
    return " || ".join(paragraph for paragraph in paragraphs if paragraph)


def years_from_timeline(timeline: str) -> tuple[str, str]:
    years = re.findall(r"\b(20[0-9]{2}|19[0-9]{2})\b", timeline or "")
    if not years:
        return "", ""
    if len(years) == 1:
        return years[0], years[0]
    return years[0], years[-1]


def bootstrap_rows(projects_dir: Path) -> list[dict[str, str]]:
    rows = []
    for path in sorted(projects_dir.glob("*.md")):
        frontmatter, body = parse_frontmatter(path)
        if not frontmatter:
            continue
        timeline = str(frontmatter.get("timeline", ""))
        start_year, end_year = years_from_timeline(timeline)
        name = str(frontmatter.get("title", path.stem))
        rows.append(
            {
                "status": "publish",
                "name": name,
                "slug": path.stem,
                "full_title": str(frontmatter.get("full_title", name)),
                "project_state": str(frontmatter.get("project_state", "")),
                "project_type": str(frontmatter.get("project_type", "")),
                "img": str(frontmatter.get("img", "")),
                "collaborators": csv_join(frontmatter.get("collaborators", [])),
                "start_year": start_year,
                "end_year": end_year,
                "overview": extract_overview(body),
                "grant_number": str(frontmatter.get("grant_number", "")),
                "research_directions": csv_join(frontmatter.get("highlights", [])),
                "project_filter": str(frontmatter.get("project_filter", path.stem)),
                "official_page": str(frontmatter.get("official_page", "")),
                "description": str(frontmatter.get("description", "")),
                "focus_areas": csv_join(frontmatter.get("focus_areas", [])),
            }
        )
    rows.sort(key=lambda item: item["name"].lower())
    return rows


def write_csv(rows: list[dict[str, str]], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=FIELD_ORDER)
        writer.writeheader()
        for row in rows:
            writer.writerow({field: row.get(field, "") for field in FIELD_ORDER})


def infer_project_state(row: dict[str, str]) -> str:
    explicit = normalize_space(row.get("project_state", "")).lower()
    if explicit in {"active", "ended"}:
        return explicit
    end_year = normalize_space(row.get("end_year", ""))
    if end_year.isdigit():
        return "active" if int(end_year) >= datetime.now().year else "ended"
    return "active"


def timeline_for(row: dict[str, str]) -> str:
    start_year = normalize_space(row.get("start_year", ""))
    end_year = normalize_space(row.get("end_year", ""))
    if start_year and end_year:
        return start_year if start_year == end_year else f"{start_year}-{end_year}"
    return start_year or end_year


def image_filename_from_value(value: str, fallback_slug: str) -> str:
    value = normalize_space(value)
    if not value:
        return ""
    if value.startswith("/assets/projects/"):
        return Path(value).name
    if re.match(r"^https?://", value):
        if "drive.google.com" in value:
            file_id = drive_file_id(value)
            if file_id:
                return f"{fallback_slug}.jpg"
        return Path(value.split("?", 1)[0]).name
    return Path(value).name


def sync_project_image(
    raw_value: str,
    slug: str,
    images_source: Path,
    images_dest: Path,
) -> str:
    raw_value = normalize_space(raw_value)
    if not raw_value:
        return ""

    images_dest.mkdir(parents=True, exist_ok=True)
    if re.match(r"^https?://", raw_value) and "drive.google.com" in raw_value:
        file_id = drive_file_id(raw_value)
        target_name = image_filename_from_value(raw_value, slug)
        if file_id and target_name:
            target = images_dest / target_name
            try:
                request = urllib.request.Request(
                    f"https://drive.google.com/uc?export=download&id={file_id}",
                    headers={"User-Agent": USER_AGENT},
                )
                with urllib.request.urlopen(request, timeout=30) as response:
                    target.write_bytes(response.read())
                return f"/assets/projects/{target_name}"
            except Exception as exc:  # noqa: BLE001
                log(f"Warning: failed to download Drive project image for {slug}: {exc}")

    filename = image_filename_from_value(raw_value, slug)
    if not filename:
        return raw_value
    source = images_source / filename
    target = images_dest / filename
    if source.exists():
        shutil.copy2(source, target)
        return f"/assets/projects/{filename}"
    if target.exists():
        return f"/assets/projects/{filename}"
    if raw_value.startswith("/assets/projects/"):
        return raw_value
    log(f"Warning: project image not found for {slug}: {filename}")
    return f"/assets/projects/{filename}"


def project_from_row(
    row: dict[str, str],
    index: int,
    images_source: Path,
    images_dest: Path,
) -> dict[str, Any]:
    name = normalize_space(row.get("name", ""))
    project_filter = normalize_space(row.get("project_filter", "")) or slugify(name)
    slug = normalize_space(row.get("slug", "")) or project_filter
    full_title = normalize_space(row.get("full_title", "")) or name
    overview = split_paragraphs(row.get("overview", ""))
    focus_areas = split_list(row.get("focus_areas", ""))
    research_directions = split_list(row.get("research_directions", ""))
    description = normalize_space(row.get("description", "")) or (overview[0] if overview else full_title)
    return {
        "name": name,
        "slug": slug,
        "full_title": full_title,
        "project_state": infer_project_state(row),
        "project_type": normalize_space(row.get("project_type", "")),
        "img": sync_project_image(row.get("img", ""), slug, images_source, images_dest),
        "collaborators": split_list(row.get("collaborators", "")),
        "timeline": timeline_for(row),
        "start_year": normalize_space(row.get("start_year", "")),
        "end_year": normalize_space(row.get("end_year", "")),
        "overview": overview,
        "grant_number": normalize_space(row.get("grant_number", "")),
        "research_directions": research_directions,
        "project_filter": project_filter,
        "official_page": normalize_space(row.get("official_page", "")),
        "description": description,
        "focus_areas": focus_areas,
        "url": f"/projects/{slug}/",
    }


def write_project_data(projects: list[dict[str, Any]], destination: Path) -> None:
    lines = [
        "# This file is generated by scripts/sync_projects.py from shared/projects_sheet.csv.",
        "# Manual edits will be overwritten the next time the sync script runs.",
    ]
    for project in projects:
        lines.append(f"- name: {yaml_quote(project['name'])}")
        lines.append(f"  slug: {yaml_quote(project['slug'])}")
        lines.append(f"  title: {yaml_quote(project['name'])}")
        lines.append(f"  full_title: {yaml_quote(project['full_title'])}")
        lines.append(f"  project_state: {yaml_quote(project['project_state'])}")
        lines.append(f"  project_type: {yaml_quote(project['project_type'])}")
        lines.append(f"  img: {yaml_quote(project['img'])}")
        lines.append(f"  timeline: {yaml_quote(project['timeline'])}")
        lines.append(f"  start_year: {yaml_quote(project['start_year'])}")
        lines.append(f"  end_year: {yaml_quote(project['end_year'])}")
        lines.append(f"  grant_number: {yaml_quote(project['grant_number'])}")
        lines.append(f"  project_filter: {yaml_quote(project['project_filter'])}")
        lines.append(f"  official_page: {yaml_quote(project['official_page'])}")
        lines.append(f"  description: {yaml_quote(project['description'])}")
        lines.append(f"  url: {yaml_quote(project['url'])}")
        lines.append("  collaborators:")
        for collaborator in project["collaborators"]:
            lines.append(f"    - {yaml_quote(collaborator)}")
        lines.append("  focus_areas:")
        for focus in project["focus_areas"]:
            lines.append(f"    - {yaml_quote(focus)}")
        lines.append("  research_directions:")
        for direction in project["research_directions"]:
            lines.append(f"    - {yaml_quote(direction)}")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def write_project_page(project: dict[str, Any], projects_dir: Path) -> None:
    path = projects_dir / f"{project['slug']}.md"
    lines = [
        "---",
        "layout: page",
        f"title: {yaml_quote(project['name'])}",
        f"full_title: {yaml_quote(project['full_title'])}",
        f"permalink: {yaml_quote(project['url'])}",
        f"description: {yaml_quote(project['description'])}",
        f"img: {yaml_quote(project['img'])}",
        f"project_state: {yaml_quote(project['project_state'])}",
        f"project_type: {yaml_quote(project['project_type'])}",
        f"timeline: {yaml_quote(project['timeline'])}",
        f"grant_number: {yaml_quote(project['grant_number'])}",
        f"official_page: {yaml_quote(project['official_page'])}",
        "focus_areas:",
    ]
    for focus in project["focus_areas"]:
        lines.append(f"  - {yaml_quote(focus)}")
    lines.append("collaborators:")
    for collaborator in project["collaborators"]:
        lines.append(f"  - {yaml_quote(collaborator)}")
    lines.append("highlights:")
    for direction in project["research_directions"]:
        lines.append(f"  - {yaml_quote(direction)}")
    lines.extend(
        [
            f"project_filter: {yaml_quote(project['project_filter'])}",
            "---",
            "",
            '{% assign project_publications = site.data.publications | where_exp: "item", "item.projects contains page.project_filter" %}',
            "",
            '<section class="project-profile">',
            '  <div class="project-profile-hero">',
            '    <div class="project-profile-media">',
            '      <img src="{{ page.img | relative_url }}" alt="{{ page.title }}">',
            "    </div>",
            '    <div class="project-profile-copy">',
            "      <p class=\"project-profile-kicker\">{{ page.project_type }}</p>",
            "      <h1>{{ page.title }}</h1>",
            "      <p class=\"project-profile-lead\">{{ page.description }}</p>",
            '      <div class="project-profile-tags">',
            "        {% for item in page.focus_areas %}",
            "          <span>{{ item }}</span>",
            "        {% endfor %}",
            "      </div>",
            '      <div class="member-profile-links">',
            "        <a class=\"about-hero-btn about-hero-btn-primary about-inline-btn\" href=\"{{ '/publications/' | relative_url }}?project={{ page.project_filter | url_encode }}\">View Publications</a>",
            "        {% if page.official_page and page.official_page != '' %}",
            "          <a class=\"about-hero-btn about-hero-btn-secondary\" href=\"{{ page.official_page }}\" target=\"_blank\" rel=\"noopener\">Official Project Page <span aria-hidden=\"true\">&rarr;</span></a>",
            "        {% endif %}",
            "        <a class=\"about-hero-btn about-hero-btn-secondary\" href=\"{{ '/projects/' | relative_url }}\">Back to Projects <span aria-hidden=\"true\">&rarr;</span></a>",
            "      </div>",
            "    </div>",
            "  </div>",
            "",
            '  <div class="project-profile-grid">',
            '    <div class="project-profile-section">',
            "      <h2>Overview</h2>",
        ]
    )
    for paragraph in project["overview"]:
        lines.append(f"      <p>{html.escape(paragraph)}</p>")
    lines.extend(
        [
            "    </div>",
            "",
            '    <aside class="project-profile-panel">',
            "      {% if page.timeline and page.timeline != '' %}",
            '        <div class="project-profile-panel-block">',
            "          <h3>Timeline</h3>",
            "          <p>{{ page.timeline }}</p>",
            "        </div>",
            "      {% endif %}",
            "      {% if page.grant_number and page.grant_number != '' %}",
            '        <div class="project-profile-panel-block">',
            "          <h3>Grant</h3>",
            "          <p>{{ page.grant_number }}</p>",
            "        </div>",
            "      {% endif %}",
            "      {% if page.collaborators and page.collaborators != empty %}",
            '        <div class="project-profile-panel-block">',
            "          <h3>Collaborators</h3>",
            '          <ul class="project-profile-list">',
            "            {% for organization in page.collaborators %}",
            "              <li>{{ organization }}</li>",
            "            {% endfor %}",
            "          </ul>",
            "        </div>",
            "      {% endif %}",
            "    </aside>",
            "",
            "  </div>",
            "",
            '  <div class="project-profile-section">',
            "    <h2>Research Directions</h2>",
            '    <ul class="project-profile-list">',
            "      {% for item in page.highlights %}",
            "        <li>{{ item }}</li>",
            "      {% endfor %}",
            "    </ul>",
            "  </div>",
            "",
            '  <div class="project-profile-section">',
            "    <h2>Related Publications</h2>",
            "    {% if project_publications and project_publications != empty %}",
            "      {% include publication_cards.liquid publications=project_publications %}",
            "    {% else %}",
            '      <div class="publications project-related-publications">',
            '        <ol class="bibliography">',
            "          <li>",
            '            <div class="row">',
            '              <div class="col-sm-10">',
            '                <div class="title">Project-linked publications</div>',
            '                <div class="periodical">No publications are linked to this project yet. Once project tags are assigned in the publications workflow, related outputs will appear here automatically.</div>',
            '                <div class="links">',
            "                  <a href=\"{{ '/publications/' | relative_url }}?project={{ page.project_filter | url_encode }}\" class=\"btn btn-sm z-depth-0\" role=\"button\">Browse Publications</a>",
            "                </div>",
            "              </div>",
            "            </div>",
            "          </li>",
            "        </ol>",
            "      </div>",
            "    {% endif %}",
            "  </div>",
            "</section>",
            "",
        ]
    )
    projects_dir.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines), encoding="utf-8")


def sync_from_rows(
    rows: list[dict[str, str]],
    output: Path,
    projects_dir: Path,
    images_source: Path,
    images_dest: Path,
) -> list[dict[str, Any]]:
    projects = []
    for index, row in enumerate(rows):
        status = normalize_space(row.get("status", "")).lower()
        if status in SKIP_STATUSES:
            continue
        project = project_from_row(row, index, images_source, images_dest)
        if not project["name"]:
            continue
        projects.append(project)

    projects.sort(key=lambda item: item["name"].lower())
    write_project_data(projects, output)
    for project in projects:
        write_project_page(project, projects_dir)
    return projects


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="", help="Path to a local CSV or Google Sheet URL.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="JSON config file with the shared Google Sheet URL.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Target project YAML file.")
    parser.add_argument("--projects-dir", default=str(DEFAULT_PROJECTS_DIR), help="Target project page directory.")
    parser.add_argument(
        "--images-source",
        default="",
        help="Local folder containing uploaded project images.",
    )
    parser.add_argument(
        "--images-drive-folder",
        default="",
        help="Public Google Drive folder URL used to auto-download project images.",
    )
    parser.add_argument(
        "--images-dest",
        default=str(DEFAULT_IMAGES_DEST),
        help="Destination folder for site-ready project images.",
    )
    parser.add_argument(
        "--bootstrap-from-pages",
        action="store_true",
        help="Create the local CSV from the current _projects pages before syncing.",
    )
    args = parser.parse_args()
    config = load_config(Path(args.config))
    images_source = Path(normalize_space(args.images_source) or normalize_space(str(config.get("images_source", ""))) or str(DEFAULT_IMAGES_SOURCE))
    images_drive_folder = normalize_space(args.images_drive_folder) or normalize_space(str(config.get("images_drive_folder", "")))
    images_dest = Path(args.images_dest)

    if images_drive_folder:
        download_drive_images(images_drive_folder, images_source)

    source_path = Path(args.source) if args.source else DEFAULT_SOURCE
    if args.bootstrap_from_pages:
        rows = bootstrap_rows(Path(args.projects_dir))
        write_csv(rows, source_path)
        print(f"Wrote {len(rows)} project rows to {source_path} from {args.projects_dir}")
    else:
        source = normalize_space(args.source) or normalize_space(str(config.get("source", ""))) or str(DEFAULT_SOURCE)
        normalized_source = normalize_google_sheet_source(source)
        mirror_path = DEFAULT_SOURCE if re.match(r"^https?://", normalized_source) else None
        rows = load_rows(source, mirror_path=mirror_path)

    projects = sync_from_rows(rows, Path(args.output), Path(args.projects_dir), images_source, images_dest)
    print(f"Wrote {len(projects)} projects to {args.output} and {args.projects_dir}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
