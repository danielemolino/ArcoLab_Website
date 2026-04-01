#!/usr/bin/env python3
"""Discover candidate publications for an author using OpenAlex.

This script is intentionally isolated from the sync workflow:
- it does not modify the main publications CSV
- it only writes a separate candidate CSV
- it prefers peer-reviewed versions over arXiv when possible

Typical usage:
python3 scripts/discover_author_publications.py --author "Paolo Soda"
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import sys
import urllib.parse
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXISTING = ROOT / "shared" / "publications_sheet.csv"
DEFAULT_OUTPUT = ROOT / "shared" / "discovered_publications.csv"
USER_AGENT = "ArcoLabPublicationDiscovery/1.0 (arcolabucbm@gmail.com)"
OPENALEX_BASE = "https://api.openalex.org"
CROSSREF_BASE = "https://api.crossref.org"
PREFERRED_KEYWORDS = [
    "medical imaging",
    "multimodal learning",
    "generative AI",
    "foundation models",
    "clinical prediction",
    "explainability",
    "radiomics",
    "oncology",
    "COVID-19",
    "industrial AI",
]
OUTPUT_COLUMNS = [
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


def log(message: str) -> None:
    print(message, file=sys.stderr)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_title(value: str) -> str:
    value = normalize_space(value).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def request_json(url: str) -> dict[str, Any]:
    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    with urllib.request.urlopen(request, timeout=30) as response:
        return json.loads(response.read().decode("utf-8"))


def csv_escape(value: str) -> str:
    return normalize_space(value)


def load_existing_publications(path: Path) -> tuple[set[str], set[str]]:
    if not path.exists():
        return set(), set()
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        dois = set()
        titles = set()
        for row in reader:
            doi = normalize_space(row.get("doi", ""))
            title = normalize_title(row.get("title", ""))
            if doi:
                dois.add(doi.lower())
            if title:
                titles.add(title)
        return dois, titles


@dataclass
class AuthorCandidate:
    author_id: str
    display_name: str
    score: int


def score_author(result: dict[str, Any], query: str) -> int:
    display_name = normalize_space(str(result.get("display_name", "")))
    institutions = " ".join(
        normalize_space(str(institution.get("display_name", "")))
        for institution in (result.get("last_known_institutions") or [])
    ).lower()
    q = normalize_space(query).lower()
    score = 0
    if display_name.lower() == q:
        score += 100
    elif q in display_name.lower():
        score += 50
    if "campus bio-medico" in institutions or "unicampus" in institutions:
        score += 40
    if "rome" in institutions:
        score += 10
    works_count = int(result.get("works_count", 0) or 0)
    score += min(works_count, 30)
    return score


def find_best_author(query: str) -> AuthorCandidate:
    params = urllib.parse.urlencode({"search": query, "per-page": 10, "mailto": "arcolabucbm@gmail.com"})
    payload = request_json(f"{OPENALEX_BASE}/authors?{params}")
    results = payload.get("results", [])
    if not results:
        raise RuntimeError(f"No OpenAlex author found for '{query}'.")

    candidates = []
    for item in results:
        author_id = str(item.get("id", "")).rsplit("/", 1)[-1]
        if not author_id:
            continue
        candidates.append(
            AuthorCandidate(
                author_id=author_id,
                display_name=normalize_space(str(item.get("display_name", ""))),
                score=score_author(item, query),
            )
        )

    if not candidates:
        raise RuntimeError(f"No usable OpenAlex author id found for '{query}'.")
    candidates.sort(key=lambda item: item.score, reverse=True)
    return candidates[0]


def fetch_author_works(author_id: str, max_pages: int = 8) -> list[dict[str, Any]]:
    cursor = "*"
    works: list[dict[str, Any]] = []
    for _ in range(max_pages):
        params = urllib.parse.urlencode(
            {
                "filter": f"author.id:{author_id}",
                "per-page": 200,
                "cursor": cursor,
                "mailto": "arcolabucbm@gmail.com",
            }
        )
        payload = request_json(f"{OPENALEX_BASE}/works?{params}")
        works.extend(payload.get("results", []))
        meta = payload.get("meta", {})
        next_cursor = meta.get("next_cursor")
        if not next_cursor or next_cursor == cursor:
            break
        cursor = next_cursor
    return works


def crossref_exact_match(title: str) -> dict[str, Any] | None:
    params = urllib.parse.urlencode({"query.title": title, "rows": 5, "mailto": "arcolabucbm@gmail.com"})
    payload = request_json(f"{CROSSREF_BASE}/works?{params}")
    items = payload.get("message", {}).get("items", [])
    target = normalize_title(title)
    for item in items:
        candidate_title = normalize_title(" ".join(item.get("title", [])))
        if candidate_title == target:
            return item
    return None


def prefer_peer_reviewed_doi(title: str, doi: str) -> str:
    doi = normalize_space(doi)
    if not doi:
        return ""
    if not doi.lower().startswith("10.48550/arxiv."):
        return doi
    try:
        crossref_item = crossref_exact_match(title)
    except Exception as exc:  # noqa: BLE001
        log(f"Warning: Crossref lookup failed for '{title}': {exc}")
        return doi
    if not crossref_item:
        return doi
    candidate_doi = normalize_space(str(crossref_item.get("DOI", "")))
    if candidate_doi and not candidate_doi.lower().startswith("10.48550/arxiv."):
        return candidate_doi
    return doi


def extract_authors(work: dict[str, Any]) -> str:
    authors = []
    for authorship in work.get("authorships", []) or []:
        author = authorship.get("author", {}) or {}
        name = normalize_space(str(author.get("display_name", "")))
        if name:
            authors.append(name)
    return "; ".join(authors)


def extract_venue(work: dict[str, Any]) -> str:
    primary = work.get("primary_location", {}) or {}
    source = primary.get("source", {}) or {}
    return normalize_space(str(source.get("display_name", "")))


def infer_keywords(work: dict[str, Any]) -> str:
    haystack = " ".join(
        [
            normalize_space(str(work.get("title", ""))),
            normalize_space(str(work.get("abstract_inverted_index", ""))),
            " ".join(normalize_space(str(topic.get("display_name", ""))) for topic in (work.get("topics") or [])),
            " ".join(normalize_space(str(concept.get("display_name", ""))) for concept in (work.get("concepts") or [])),
            extract_venue(work),
        ]
    ).lower()

    rules = [
        ("radiomics", ["radiomics"]),
        ("oncology", ["oncology", "cancer", "tumor", "tumour", "breast", "lung"]),
        ("COVID-19", ["covid", "sars-cov-2", "chest x-ray"]),
        ("foundation models", ["foundation model", "vision-language", "vlm", "transformer"]),
        ("generative AI", ["generative", "gan", "diffusion", "image-to-image", "synthesis"]),
        ("multimodal learning", ["multimodal", "multi-modal", "fusion"]),
        ("explainability", ["explainability", "interpretable", "interpretability"]),
        ("clinical prediction", ["prognosis", "prediction", "outcome", "survival", "risk"]),
        ("medical imaging", ["mri", "ct", "x-ray", "radiology", "imaging", "mammography"]),
        ("industrial AI", ["agriculture", "industrial", "ndvi", "satellite", "remote sensing"]),
    ]

    found: list[str] = []
    for keyword, triggers in rules:
        if any(trigger in haystack for trigger in triggers):
            found.append(keyword)

    unique = []
    seen = set()
    for keyword in found:
        if keyword not in seen and keyword in PREFERRED_KEYWORDS:
            unique.append(keyword)
            seen.add(keyword)
    return "; ".join(unique[:3])


def work_to_row(work: dict[str, Any]) -> dict[str, str]:
    title = normalize_space(str(work.get("title", "")))
    doi = normalize_space(str(work.get("doi", "")))
    doi = re.sub(r"^https?://doi\.org/", "", doi, flags=re.IGNORECASE)
    doi = prefer_peer_reviewed_doi(title, doi)
    primary_location = work.get("primary_location", {}) or {}
    landing = normalize_space(str(primary_location.get("landing_page_url", "")))
    pdf = normalize_space(str((primary_location.get("pdf_url", "") or "")))
    if doi and not landing:
        landing = f"https://doi.org/{doi}"
    return {
        "status": "publish",
        "title": title,
        "doi": doi,
        "authors": extract_authors(work),
        "year": str(work.get("publication_year", "") or ""),
        "code": "",
        "website": landing if not pdf else "",
        "keywords": infer_keywords(work),
        "projects": "",
        "selected": "FALSE",
    }


def dedupe_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    deduped: list[dict[str, str]] = []
    seen_dois: set[str] = set()
    seen_titles: set[str] = set()
    for row in rows:
        doi = normalize_space(row.get("doi", "")).lower()
        title = normalize_title(row.get("title", ""))
        if doi and doi in seen_dois:
            continue
        if title and title in seen_titles:
            continue
        if doi:
            seen_dois.add(doi)
        if title:
            seen_titles.add(title)
        deduped.append(row)
    return deduped


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--author", required=True, help='Author name, e.g. "Paolo Soda".')
    parser.add_argument(
        "--existing",
        default=str(DEFAULT_EXISTING),
        help="Existing publications CSV used to exclude already-known papers.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Output CSV for discovered candidate papers.",
    )
    parser.add_argument(
        "--include-known",
        action="store_true",
        help="Do not exclude papers already present in the main publications CSV.",
    )
    args = parser.parse_args()

    existing_dois, existing_titles = load_existing_publications(Path(args.existing))
    author = find_best_author(args.author)
    works = fetch_author_works(author.author_id)

    candidate_rows = []
    for work in works:
        row = work_to_row(work)
        title_key = normalize_title(row["title"])
        doi_key = normalize_space(row["doi"]).lower()
        if not args.include_known:
            if doi_key and doi_key in existing_dois:
                continue
            if title_key and title_key in existing_titles:
                continue
        if not row["title"] or not row["year"]:
            continue
        candidate_rows.append(row)

    candidate_rows = dedupe_rows(candidate_rows)
    candidate_rows.sort(key=lambda row: (row["year"], row["title"]), reverse=True)
    write_rows(Path(args.output), candidate_rows)

    print(
        f"Discovered {len(candidate_rows)} candidate publications for {author.display_name} "
        f"(OpenAlex author id {author.author_id})."
    )
    print(f"Wrote candidate CSV to {args.output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
