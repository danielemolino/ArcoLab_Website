#!/usr/bin/env python3
"""Convert an OpenAlex CSV export into the site publications sheet format."""

from __future__ import annotations

import argparse
import csv
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "paolo_soda_openalex_publications_clean_final_authors_venues_normalized.csv"
DEFAULT_OVERLAY = ROOT / "shared" / "publications_sheet.csv"
DEFAULT_OUTPUT = ROOT / "shared" / "publications_sheet.csv"

OUTPUT_FIELDS = [
    "status",
    "title",
    "doi",
    "authors",
    "year",
    "code",
    "website",
    "keywords",
    "projects",
    "selected",
]

EXCLUDED_DOIS = {
    "10.1007/978-3-642-69977-1_86",
}

EXCLUDED_TITLES = {
    "Serum Insulin and Glucose Tolerance in Obese Patients with or Without Associated Arterial Hypertension",
}


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_title(value: str) -> str:
    value = normalize_space(value).lower()
    value = re.sub(r"[^a-z0-9]+", " ", value)
    return normalize_space(value)


def normalize_doi(value: str) -> str:
    value = normalize_space(value)
    value = re.sub(r"^https?://(dx\.)?doi\.org/", "", value, flags=re.IGNORECASE)
    value = re.sub(r"^doi:\s*", "", value, flags=re.IGNORECASE)
    return value


def is_truthy(value: str) -> bool:
    return normalize_space(value).lower() in {"1", "true", "yes", "y"}


def load_rows(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        raise FileNotFoundError(f"Missing source file: {path}")

    with path.open("r", encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if reader.fieldnames is None:
            raise ValueError(f"{path} is empty or missing a header row.")
        rows = []
        for row in reader:
            cleaned = {key.strip(): normalize_space(value) for key, value in row.items() if key}
            if any(cleaned.values()):
                rows.append(cleaned)
    return rows


def load_overlay(
    path: Path,
) -> tuple[dict[str, dict[str, str]], dict[str, dict[str, str]]]:
    by_doi: dict[str, dict[str, str]] = {}
    by_title: dict[str, dict[str, str]] = {}
    if not path.exists():
        return by_doi, by_title

    for row in load_rows(path):
        doi = normalize_doi(row.get("doi", "")).lower()
        title = normalize_title(row.get("title", ""))
        if doi:
            by_doi[doi] = row
        if title:
            by_title[title] = row
    return by_doi, by_title


def pick_overlay_row(source_row: dict[str, str], by_doi: dict[str, dict[str, str]], by_title: dict[str, dict[str, str]]) -> dict[str, str] | None:
    doi = normalize_doi(source_row.get("doi", "")).lower()
    if doi and doi in by_doi:
        return by_doi[doi]
    title = normalize_title(source_row.get("title", ""))
    if title and title in by_title:
        return by_title[title]
    return None


def overlay_value(overlay_row: dict[str, str] | None, field: str, fallback: str = "") -> str:
    if not overlay_row:
        return fallback
    value = normalize_space(overlay_row.get(field, ""))
    return value or fallback


def convert_row(source_row: dict[str, str], overlay_row: dict[str, str] | None) -> dict[str, str]:
    doi = normalize_doi(source_row.get("doi", ""))
    title = normalize_space(source_row.get("title", ""))
    if doi in EXCLUDED_DOIS or title in EXCLUDED_TITLES:
        return {}
    authors = normalize_space(source_row.get("authors", ""))
    year = normalize_space(source_row.get("year", ""))
    status = overlay_value(overlay_row, "status", "publish") or "publish"

    return {
        "status": status,
        "title": title,
        "doi": doi,
        "authors": authors,
        "year": year,
        "code": overlay_value(overlay_row, "code"),
        "website": overlay_value(overlay_row, "website"),
        "keywords": overlay_value(overlay_row, "keywords"),
        "projects": overlay_value(overlay_row, "projects"),
        "selected": "TRUE" if overlay_row and is_truthy(overlay_row.get("selected", "")) else "FALSE",
    }


def write_rows(rows: list[dict[str, str]], destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    with destination.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_FIELDS)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Path to the normalized OpenAlex CSV export.")
    parser.add_argument(
        "--overlay",
        default=str(DEFAULT_OVERLAY),
        help="Optional current publications sheet used to preserve manual fields.",
    )
    parser.add_argument("--output", default=str(DEFAULT_OUTPUT), help="Target CSV for the site publications sheet.")
    args = parser.parse_args()

    source_path = Path(args.source)
    overlay_path = Path(args.overlay)
    output_path = Path(args.output)

    source_rows = load_rows(source_path)
    overlay_by_doi, overlay_by_title = load_overlay(overlay_path)

    converted: list[dict[str, str]] = []
    matched_overlay = 0
    for source_row in source_rows:
        overlay_row = pick_overlay_row(source_row, overlay_by_doi, overlay_by_title)
        if overlay_row:
            matched_overlay += 1
        row = convert_row(source_row, overlay_row)
        if row:
            converted.append(row)

    converted.sort(key=lambda item: (item.get("year", ""), item.get("title", "")), reverse=True)
    write_rows(converted, output_path)

    print(f"Wrote {len(converted)} rows to {output_path} from {source_path}")
    print(f"Matched {matched_overlay} rows against the existing publications sheet at {overlay_path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
