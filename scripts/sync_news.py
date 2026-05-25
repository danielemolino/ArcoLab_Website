#!/usr/bin/env python3
"""Sync a shared news sheet into _data/news_feed.yml."""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import shutil
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "shared" / "news_sync.json"
DEFAULT_SOURCE = ROOT / "shared" / "news_sheet.csv"
DEFAULT_OUTPUT = ROOT / "_data" / "news_feed.yml"
DEFAULT_IMAGES_SOURCE = ROOT / "shared" / "news_images_uploads"
DEFAULT_IMAGES_DEST = ROOT / "assets" / "news"
USER_AGENT = "ArcoLabNewsSync/1.0 (arcolabucbm@gmail.com)"
IMAGE_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp", ".gif")

REQUIRED_COLUMNS = {
    "status",
    "date",
    "title",
    "summary",
    "category",
    "linkedin_url",
}


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def slugify(value: str) -> str:
    value = normalize_space(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "news-image"


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


def yaml_quote(value: str) -> str:
    value = str(value)
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def extension_from_content_type(content_type: str) -> str:
    content_type = content_type.split(";", 1)[0].strip().lower()
    return {
        "image/jpeg": ".jpg",
        "image/jpg": ".jpg",
        "image/png": ".png",
        "image/webp": ".webp",
        "image/gif": ".gif",
    }.get(content_type, "")


def image_filename_from_value(value: str, fallback_base: str) -> str:
    value = normalize_space(value)
    if not value:
        return ""
    if value.startswith("/assets/news/"):
        return Path(value).name
    parsed = urllib.parse.urlparse(value)
    if parsed.scheme in {"http", "https"}:
        filename = Path(urllib.parse.unquote(parsed.path)).name
        if Path(filename).suffix.lower() in IMAGE_EXTENSIONS:
            return filename
        return f"{fallback_base}.jpg"
    return Path(value).name


def sync_news_image(
    raw_value: str,
    date: str,
    title: str,
    images_source: Path,
    images_dest: Path,
) -> str:
    raw_value = normalize_space(raw_value)
    if not raw_value:
        return ""

    fallback_base = slugify(f"{date}-{title}")
    images_dest.mkdir(parents=True, exist_ok=True)

    parsed = urllib.parse.urlparse(raw_value)
    if parsed.scheme in {"http", "https"}:
        target_name = image_filename_from_value(raw_value, fallback_base)
        target = images_dest / target_name
        try:
            request = urllib.request.Request(raw_value, headers={"User-Agent": USER_AGENT})
            with urllib.request.urlopen(request, timeout=30) as response:
                data = response.read()
                detected_extension = extension_from_content_type(response.headers.get("Content-Type", ""))
            if Path(target_name).suffix.lower() not in IMAGE_EXTENSIONS and detected_extension:
                target_name = f"{fallback_base}{detected_extension}"
                target = images_dest / target_name
            target.write_bytes(data)
            return f"/assets/news/{target_name}"
        except Exception as exc:  # noqa: BLE001
            print(f"Warning: failed to download news image {raw_value}: {exc}", file=sys.stderr)
            return raw_value

    filename = image_filename_from_value(raw_value, fallback_base)
    if not filename:
        return ""
    source = images_source / filename
    target = images_dest / filename
    if source.exists():
        shutil.copy2(source, target)
        return f"/assets/news/{filename}"
    if target.exists():
        return f"/assets/news/{filename}"
    if raw_value.startswith("/assets/news/"):
        return raw_value
    print(f"Warning: news image not found: {filename}", file=sys.stderr)
    return f"/assets/news/{filename}"


def load_rows(source: str, mirror_path: Path | None = None) -> list[dict[str, str]]:
    source = normalize_google_sheet_source(source)
    if re.match(r"^https?://", source):
        request = urllib.request.Request(source, headers={"User-Agent": USER_AGENT})
        with urllib.request.urlopen(request, timeout=20) as response:
            raw = response.read().decode("utf-8-sig")
        if mirror_path is not None:
            mirror_path.write_text(raw, encoding="utf-8")
    else:
        raw = Path(source).read_text(encoding="utf-8-sig")

    reader = csv.DictReader(io.StringIO(raw))
    if reader.fieldnames is None:
        raise ValueError("The news sheet is empty or missing a header row.")

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


def write_yaml(items: list[dict[str, str]], destination: Path) -> None:
    lines = [
        "# This file is generated by scripts/sync_news.py from shared/news_sheet.csv.",
        "# Manual edits will be overwritten the next time the sync script runs.",
    ]
    for item in items:
        lines.append(f"- date: {yaml_quote(item.get('date', ''))}")
        lines.append(f"  title: {yaml_quote(item.get('title', ''))}")
        lines.append(f"  summary: {yaml_quote(item.get('summary', ''))}")
        lines.append(f"  category: {yaml_quote(item.get('category', ''))}")
        lines.append(f"  linkedin_url: {yaml_quote(item.get('linkedin_url', ''))}")
        lines.append(f"  image_url: {yaml_quote(item.get('image_url', ''))}")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default="", help="Path to a local CSV or Google Sheet URL.")
    parser.add_argument("--config", default=str(DEFAULT_CONFIG), help="JSON config file with the shared Google Sheet URL.")
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Target YAML file.")
    parser.add_argument("--images-source", default="", help="Local folder containing uploaded news images.")
    parser.add_argument("--images-dest", default=str(DEFAULT_IMAGES_DEST), help="Destination folder for site-ready news images.")
    args = parser.parse_args()

    config = load_config(Path(args.config))
    source = normalize_space(args.source) or normalize_space(str(config.get("source", ""))) or str(DEFAULT_SOURCE)
    images_source = Path(normalize_space(args.images_source) or normalize_space(str(config.get("images_source", ""))) or str(DEFAULT_IMAGES_SOURCE))
    images_dest = Path(args.images_dest)
    normalized_source = normalize_google_sheet_source(source)
    mirror_path = DEFAULT_SOURCE if re.match(r"^https?://", normalized_source) else None
    rows = load_rows(source, mirror_path=mirror_path)

    items = []
    for row in rows:
        status = normalize_space(row.get("status", "")).lower()
        if status in {"draft", "ignore", "skip"}:
            continue
        items.append(
            {
                "date": row.get("date", ""),
                "title": row.get("title", ""),
                "summary": row.get("summary", ""),
                "category": row.get("category", ""),
                "linkedin_url": row.get("linkedin_url", ""),
                "image_url": sync_news_image(
                    row.get("image_url", ""),
                    row.get("date", ""),
                    row.get("title", ""),
                    images_source,
                    images_dest,
                ),
            }
        )

    items.sort(key=lambda item: (item.get("date", ""), item.get("title", "")), reverse=True)
    output = Path(args.output)
    write_yaml(items, output)
    print(f"Wrote {len(items)} news entries to {output} from {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
