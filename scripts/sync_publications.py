#!/usr/bin/env python3
"""Sync a shared publications sheet into _bibliography/papers.bib.

The script accepts either:
- a local CSV file, or
- a published Google Sheets CSV URL

It optionally enriches rows from Crossref, but always falls back to the sheet
values so the workflow remains usable offline or with incomplete metadata.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import html
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "shared" / "publications_sync.json"
DEFAULT_SOURCE = ROOT / "shared" / "publications_sheet.csv"
DEFAULT_OUTPUT = ROOT / "_bibliography" / "papers.bib"
DEFAULT_DATA_OUTPUT = ROOT / "_data" / "publications.yml"
USER_AGENT = "ArcoLabPublicationsSync/1.0 (arcolab@unicampus.it)"

FIELD_ORDER = [
    "title",
    "author",
    "journal",
    "booktitle",
    "school",
    "publisher",
    "volume",
    "number",
    "pages",
    "year",
    "month",
    "arxiv",
    "doi",
    "url",
    "abstract",
    "keywords",
    "projects",
    "pdf",
    "code",
    "website",
    "note",
    "selected",
]

REQUIRED_COLUMNS = {
    "status",
    "title",
    "doi",
    "authors",
    "year",
    "code",
    "website",
    "keywords",
    "selected",
}


def log(message: str) -> None:
    print(message, file=sys.stderr)


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_key_fragment(value: str) -> str:
    cleaned = re.sub(r"[^a-z0-9]+", "", value.lower())
    return cleaned or "entry"


def normalize_title_for_match(value: str) -> str:
    value = value.lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return normalize_space(value)


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y", "selected"}


def arxiv_id_from_doi(doi: str) -> str:
    doi = normalize_space(doi)
    match = re.match(r"^10\.48550/arxiv\.([A-Za-z0-9.\-_/]+)$", doi, re.IGNORECASE)
    if not match:
        return ""
    return match.group(1)


def authors_from_sheet(value: str) -> str:
    value = normalize_space(value)
    if not value:
        return ""
    if " and " in value:
        return value
    parts = [normalize_space(part) for part in value.split(";")]
    parts = [part for part in parts if part]
    return " and ".join(parts)


def normalize_keywords(value: str) -> str:
    if not value:
        return ""
    parts = re.split(r"[;,]", value)
    cleaned = [normalize_space(part) for part in parts if normalize_space(part)]
    unique: list[str] = []
    seen: set[str] = set()
    for item in cleaned:
        key = item.lower()
        if key not in seen:
            unique.append(item)
            seen.add(key)
    return "; ".join(unique)


def normalize_projects(value: str) -> str:
    if not value:
        return ""
    parts = re.split(r"[;,]", value)
    cleaned = [normalize_space(part) for part in parts if normalize_space(part)]
    unique: list[str] = []
    seen: set[str] = set()
    for item in cleaned:
        key = item.lower()
        if key not in seen:
            unique.append(item)
            seen.add(key)
    return "; ".join(unique)


def authors_from_crossref(author_list: list[dict[str, Any]]) -> str:
    authors = []
    for author in author_list or []:
        family = normalize_space(str(author.get("family", "")))
        given = normalize_space(str(author.get("given", "")))
        name = normalize_space(str(author.get("name", "")))
        if family and given:
            authors.append(f"{family}, {given}")
        elif family:
            authors.append(family)
        elif name:
            authors.append(name)
    return " and ".join(authors)


def first_year_from_crossref(message: dict[str, Any]) -> str:
    for key in ("published-print", "published-online", "issued"):
        block = message.get(key) or {}
        date_parts = block.get("date-parts") or []
        if date_parts and date_parts[0]:
            return str(date_parts[0][0])
    return ""


def infer_entry_type(crossref_type: str, sheet_value: str) -> str:
    sheet_value = normalize_space(sheet_value).lower()
    if sheet_value:
        return sheet_value

    mapping = {
        "journal-article": "article",
        "proceedings-article": "inproceedings",
        "proceedings": "proceedings",
        "book-chapter": "incollection",
        "dissertation": "phdthesis",
    }
    return mapping.get(crossref_type, "article")


def first_non_empty(*values: str) -> str:
    for value in values:
        if normalize_space(str(value)):
            return normalize_space(str(value))
    return ""


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
    return (
        "https://docs.google.com/spreadsheets/d/"
        f"{spreadsheet_id}/export?format=csv&gid={gid}"
    )


def fetch_json(url: str) -> dict[str, Any] | None:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=15) as response:
            return json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, urllib.error.HTTPError, TimeoutError) as exc:
        log(f"Warning: metadata lookup failed for {url}: {exc}")
        return None


def fetch_crossref_by_doi(doi: str) -> dict[str, Any] | None:
    doi = normalize_space(doi)
    if not doi:
        return None
    encoded = urllib.parse.quote(doi, safe="")
    payload = fetch_json(f"https://api.crossref.org/works/{encoded}")
    if not payload:
        return None
    return payload.get("message")


def fetch_openalex_by_doi(doi: str) -> dict[str, Any] | None:
    doi = normalize_space(doi)
    if not doi:
        return None
    encoded = urllib.parse.quote(f"https://doi.org/{doi}", safe="")
    return fetch_json(f"https://api.openalex.org/works/https://doi.org/{encoded}?mailto=arcolabucbm@gmail.com")


def abstract_from_openalex(abstract_index: dict[str, list[int]] | None) -> str:
    if not abstract_index:
        return ""
    positions: dict[int, str] = {}
    for word, indexes in abstract_index.items():
        for index in indexes:
            positions[int(index)] = word
    if not positions:
        return ""
    return normalize_space(" ".join(positions[index] for index in sorted(positions)))


def abstract_from_crossref(value: str) -> str:
    text = normalize_space(value)
    if not text:
        return ""
    text = re.sub(r"<[^>]+>", " ", html.unescape(text))
    return normalize_space(text)


def search_crossref_by_title(title: str) -> dict[str, Any] | None:
    title = normalize_space(title)
    if not title:
        return None
    query = urllib.parse.urlencode({"query.title": title, "rows": 5})
    payload = fetch_json(f"https://api.crossref.org/works?{query}")
    if not payload:
        return None
    items = payload.get("message", {}).get("items", [])
    if not items:
        return None

    target = normalize_title_for_match(title)
    for item in items:
        candidate_title = normalize_title_for_match(" ".join(item.get("title", [])))
        if candidate_title == target:
            return item
    return items[0]


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
        raise ValueError("The publications sheet is empty or missing a header row.")

    fieldnames = {name.strip() for name in reader.fieldnames if name}
    missing = REQUIRED_COLUMNS - fieldnames
    if missing:
        raise ValueError(
            "Missing required CSV columns: " + ", ".join(sorted(missing))
        )

    rows: list[dict[str, str]] = []
    for row in reader:
        cleaned = {key.strip(): normalize_space(value) for key, value in row.items() if key}
        if any(cleaned.values()):
            rows.append(cleaned)
    return rows


def build_key(row: dict[str, str], entry: dict[str, str]) -> str:
    if row.get("key"):
        return normalize_key_fragment(row["key"])

    author_field = entry.get("author", "")
    first_author = author_field.split(" and ")[0]
    if "," in first_author:
        surname = first_author.split(",", 1)[0]
    else:
        surname = first_author.split()[-1] if first_author else "paper"
    year = entry.get("year", "nodate")
    title_tokens = normalize_title_for_match(entry.get("title", "")).split()
    tail = "".join(title_tokens[:2]) or "paper"
    return f"{normalize_key_fragment(surname)}{normalize_key_fragment(year)}{normalize_key_fragment(tail)}"


def merge_row(row: dict[str, str], enrich: bool) -> dict[str, str]:
    doi_from_sheet = row.get("doi", "")
    arxiv_id = arxiv_id_from_doi(doi_from_sheet)
    metadata = None
    openalex_metadata = None
    if enrich and doi_from_sheet and not arxiv_id:
        metadata = fetch_crossref_by_doi(doi_from_sheet)
        openalex_metadata = fetch_openalex_by_doi(doi_from_sheet)
    if enrich and metadata is None and row.get("title") and not arxiv_id:
        metadata = search_crossref_by_title(row["title"])

    title_from_metadata = ""
    if metadata:
        title_from_metadata = normalize_space(" ".join(metadata.get("title", [])))

    entry_type = infer_entry_type(
        normalize_space(str((metadata or {}).get("type", ""))),
        row.get("entry_type", ""),
    )
    author = first_non_empty(
        authors_from_sheet(row.get("authors", "")),
        authors_from_crossref((metadata or {}).get("author", [])),
    )
    doi = first_non_empty(
        doi_from_sheet,
        normalize_space(str((metadata or {}).get("DOI", ""))),
    )
    url = f"https://doi.org/{doi}" if doi else ""
    if arxiv_id:
        url = f"https://arxiv.org/abs/{arxiv_id}"

    container_title = normalize_space(
        " ".join((metadata or {}).get("container-title", []))
    )
    publisher = normalize_space(str((metadata or {}).get("publisher", "")))

    entry = {
        "entry_type": entry_type or "article",
        "title": first_non_empty(row.get("title", ""), title_from_metadata),
        "author": author,
        "journal": first_non_empty(
            row.get("journal", ""),
            f"arXiv preprint arXiv:{arxiv_id}" if arxiv_id else "",
            container_title if entry_type == "article" else "",
        ),
        "booktitle": first_non_empty(
            row.get("booktitle", ""),
            container_title if entry_type != "article" else "",
        ),
        "school": row.get("school", ""),
        "publisher": first_non_empty(row.get("publisher", ""), publisher),
        "volume": first_non_empty(
            row.get("volume", ""),
            str((metadata or {}).get("volume", "")),
        ),
        "number": first_non_empty(
            row.get("number", ""),
            str((metadata or {}).get("issue", "")),
        ),
        "pages": first_non_empty(
            row.get("pages", ""),
            str((metadata or {}).get("page", "")),
        ),
        "year": first_non_empty(
            row.get("year", ""),
            first_year_from_crossref(metadata or {}),
        ),
        "month": row.get("month", ""),
        "arxiv": "",
        "doi": doi,
        "url": first_non_empty(row.get("url", ""), url),
        "abstract": first_non_empty(
            row.get("abstract", ""),
            abstract_from_crossref(str((metadata or {}).get("abstract", ""))),
            abstract_from_openalex((openalex_metadata or {}).get("abstract_inverted_index")),
        ),
        "keywords": normalize_keywords(row.get("keywords", "")),
        "projects": normalize_projects(row.get("projects", "")),
        "pdf": row.get("pdf", ""),
        "code": row.get("code", ""),
        "website": row.get("website", ""),
        "note": row.get("notes", ""),
        "selected": "true" if truthy(row.get("selected", "")) else "",
    }
    entry["key"] = build_key(row, entry)
    return entry


def escape_bibtex(value: str) -> str:
    return value.replace("\\", "\\\\").replace("\n", " ").strip()


def yaml_quote(value: str) -> str:
    value = str(value)
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


def render_entry(entry: dict[str, str]) -> str:
    lines = [f"@{entry['entry_type']}{{{entry['key']},"]
    for field in FIELD_ORDER:
        value = normalize_space(entry.get(field, ""))
        if value:
            lines.append(f"  {field}={{{escape_bibtex(value)}}},")
    if lines[-1].endswith(","):
        lines[-1] = lines[-1][:-1]
    lines.append("}")
    return "\n".join(lines)


def write_bibliography(entries: list[dict[str, str]], destination: Path) -> None:
    lines = [
        "---",
        "---",
        "",
        (
            "% This file is generated by scripts/sync_publications.py from "
            "shared/publications_sheet.csv."
        ),
        "% Manual edits will be overwritten the next time the sync script runs.",
        "",
    ]
    rendered = [render_entry(entry) for entry in entries]
    lines.append("\n\n".join(rendered))
    lines.append("")
    destination.write_text("\n".join(lines), encoding="utf-8")


def write_publications_data(entries: list[dict[str, str]], destination: Path) -> None:
    lines = [
        "# This file is generated by scripts/sync_publications.py from shared/publications_sheet.csv.",
        "# Manual edits will be overwritten the next time the sync script runs.",
    ]
    for entry in entries:
        doi_url = f"https://doi.org/{entry['doi']}" if entry.get("doi") else ""
        lines.append(f"- key: {yaml_quote(entry.get('key', ''))}")
        lines.append(f"  title: {yaml_quote(entry.get('title', ''))}")
        lines.append(f"  author: {yaml_quote(entry.get('author', ''))}")
        lines.append(f"  venue: {yaml_quote(first_non_empty(entry.get('journal', ''), entry.get('booktitle', ''), entry.get('publisher', '')))}")
        lines.append(f"  year: {yaml_quote(entry.get('year', ''))}")
        lines.append(f"  doi: {yaml_quote(entry.get('doi', ''))}")
        lines.append(f"  doi_url: {yaml_quote(doi_url)}")
        lines.append(f"  pdf: {yaml_quote(entry.get('pdf', ''))}")
        lines.append(f"  code: {yaml_quote(entry.get('code', ''))}")
        lines.append(f"  website: {yaml_quote(entry.get('website', ''))}")
        lines.append(f"  url: {yaml_quote(entry.get('url', ''))}")
        lines.append(f"  abstract: {yaml_quote(entry.get('abstract', ''))}")
        lines.append(f"  keywords: {yaml_quote(entry.get('keywords', ''))}")
        lines.append(f"  projects: {yaml_quote(entry.get('projects', ''))}")
    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default="",
        help="Path to a local CSV, a Google Sheets URL, or a published Google Sheets CSV URL.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Target BibTeX file. Defaults to _bibliography/papers.bib.",
    )
    parser.add_argument(
        "--data-output",
        default=str(DEFAULT_DATA_OUTPUT),
        help="Target YAML data file. Defaults to _data/publications.yml.",
    )
    parser.add_argument(
        "--no-enrich",
        action="store_true",
        help="Disable Crossref metadata lookup and use only the sheet values.",
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="Optional JSON config file. Defaults to shared/publications_sync.json.",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config))
    source = first_non_empty(
        args.source,
        str(config.get("source", "")),
        str(DEFAULT_SOURCE),
    )

    mirror_path = DEFAULT_SOURCE if re.match(r"^https?://", normalize_google_sheet_source(source)) else None
    rows = load_rows(source, mirror_path=mirror_path)
    entries: list[dict[str, str]] = []
    seen_identifiers: set[str] = set()

    for row in rows:
        status = normalize_space(row.get("status", "")).lower()
        if status in {"ignore", "draft", "skip"}:
            continue

        entry = merge_row(row, enrich=not args.no_enrich)
        if not entry.get("title"):
            log("Skipping a row with no resolvable title.")
            continue

        dedupe_key = entry.get("doi") or normalize_title_for_match(entry["title"])
        if dedupe_key in seen_identifiers:
            log(f"Skipping duplicate entry: {entry['title']}")
            continue
        seen_identifiers.add(dedupe_key)
        entries.append(entry)

    entries.sort(
        key=lambda item: (item.get("year", ""), item.get("key", "")),
        reverse=True,
    )
    output = Path(args.output)
    write_bibliography(entries, output)
    write_publications_data(entries, Path(args.data_output))

    print(f"Wrote {len(entries)} publications to {output} from {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
