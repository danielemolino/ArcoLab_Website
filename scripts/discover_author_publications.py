#!/usr/bin/env python3
"""Discover candidate papers for one author or the whole Team using OpenAlex.

This script is intentionally isolated from the sync workflow:
- it does not modify the main publications CSV
- it only writes a separate candidate CSV
- it prefers published versions over arXiv when possible
- it excludes editorial, front-matter, correction, and abstract-like records

Typical usage:
python scripts/discover_author_publications.py --author "Paolo Soda"
python scripts/discover_author_publications.py --team
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import os
import re
import sys
import time
import urllib.parse
import urllib.request
from urllib.error import HTTPError
from dataclasses import dataclass
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_EXISTING = ROOT / "shared" / "publications_sheet.csv"
DEFAULT_OUTPUT = ROOT / "shared" / "discovered_publications.csv"
DEFAULT_TEAM_SOURCE = ROOT / "shared" / "team_sheet.csv"
DEFAULT_TEAM_OUTPUT = ROOT / "shared" / "discovered_team_publications.csv"
USER_AGENT = "ArcoLabPublicationDiscovery/1.0 (arcolabucbm@gmail.com)"
OPENALEX_BASE = "https://api.openalex.org"
CROSSREF_BASE = "https://api.crossref.org"
OPENALEX_API_KEY_ENV = "OPENALEX_API_KEY"
REQUEST_INTERVAL_SECONDS = 0.35
LAST_REQUEST_AT = 0.0
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
    "matched_members",
    "publication_type",
    "venue",
]

EXCLUDED_WORK_TYPES = {
    "book",
    "dataset",
    "dissertation",
    "editorial",
    "erratum",
    "libguides",
    "letter",
    "paratext",
    "peer-review",
    "reference-entry",
    "retraction",
    "standard",
    "other",
}

EXCLUDED_TITLE_PATTERNS = (
    re.compile(r"^(?:editorial|preface|foreword|title page|copyright page|table of contents)\b", re.I),
    re.compile(r"^(?:proceedings of|introduction to the special issue|special issue on)\b", re.I),
    re.compile(r"\b(?:correction|corrigendum|erratum|retraction|withdrawn)\s*(?:to|of|:)\b", re.I),
    re.compile(r"^(?:p|po|pos|oc|sat|fri|mo|tu|we|th)\s*[-.]?\s*\d", re.I),
    re.compile(r"^[a-z]{1,4}\d{2,4}\s*[-:]\s*\d", re.I),
    re.compile(r"^\d{2,5}[a-z]?(?:\s+|\s*[:.-])", re.I),
    re.compile(r"\b(?:abstract only|conference abstract|extended abstract|poster|plenary panel report)\b", re.I),
    re.compile(r"^(?:summary|figure|table|appendix|supplementary|supplement)\b", re.I),
)


def log(message: str) -> None:
    print(message, file=sys.stderr)


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


def normalize_title(value: str) -> str:
    value = normalize_space(value).lower()
    return re.sub(r"[^a-z0-9]+", " ", value).strip()


def normalize_doi(value: str) -> str:
    value = normalize_space(value).lower()
    value = re.sub(r"^https?://doi\.org/", "", value, flags=re.I)
    return value.rstrip(".,;:) ")


def request_json(url: str) -> dict[str, Any]:
    global LAST_REQUEST_AT

    if url.startswith(OPENALEX_BASE):
        api_key = os.environ.get(OPENALEX_API_KEY_ENV, "").strip()
        if api_key:
            separator = "&" if "?" in url else "?"
            url = f"{url}{separator}api_key={urllib.parse.quote(api_key)}"

    request = urllib.request.Request(
        url,
        headers={
            "User-Agent": USER_AGENT,
            "Accept": "application/json",
        },
    )
    for attempt in range(4):
        elapsed = time.monotonic() - LAST_REQUEST_AT
        if elapsed < REQUEST_INTERVAL_SECONDS:
            time.sleep(REQUEST_INTERVAL_SECONDS - elapsed)
        LAST_REQUEST_AT = time.monotonic()
        try:
            with urllib.request.urlopen(request, timeout=30) as response:
                return json.loads(response.read().decode("utf-8"))
        except HTTPError as exc:
            if exc.code not in {429, 500, 502, 503, 504} or attempt == 3:
                raise
            retry_after = exc.headers.get("Retry-After", "")
            try:
                delay = max(1, min(int(retry_after), 30))
            except ValueError:
                delay = min(2**attempt, 30)
            log(f"Warning: HTTP {exc.code}; retrying in {delay}s")
            time.sleep(delay)
    raise RuntimeError(f"Request failed after retries: {url}")


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
            doi = normalize_doi(row.get("doi", ""))
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


def extract_orcid(value: str) -> str:
    match = re.search(r"\b\d{4}-\d{4}-\d{4}-\d{3}[\dX]\b", value or "", re.I)
    return match.group(0).lower() if match else ""


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


def find_best_author(query: str, orcid_url: str = "") -> AuthorCandidate:
    orcid = extract_orcid(orcid_url)
    if orcid:
        params = urllib.parse.urlencode(
            {"filter": f"orcid:{orcid}", "per-page": 5, "mailto": "arcolabucbm@gmail.com"}
        )
        try:
            payload = request_json(f"{OPENALEX_BASE}/authors?{params}")
            result = (payload.get("results") or [None])[0]
            if result:
                author_id = str(result.get("id", "")).rsplit("/", 1)[-1]
                if author_id:
                    return AuthorCandidate(
                        author_id=author_id,
                        display_name=normalize_space(str(result.get("display_name", query))),
                        score=1000,
                    )
        except Exception as exc:  # noqa: BLE001
            log(f"Warning: OpenAlex ORCID lookup failed for '{query}': {exc}")

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


def excluded_work_reason(work: dict[str, Any]) -> str:
    work_type = normalize_space(str(work.get("type", ""))).lower()
    if work_type in EXCLUDED_WORK_TYPES:
        return f"type:{work_type}"

    title = normalize_space(str(work.get("title", "")))
    doi = normalize_doi(str(work.get("doi", "")))
    if re.search(r"\.(?:s|mm)\d+$", doi, re.I):
        return "supplement"
    landing = normalize_space(str((work.get("primary_location", {}) or {}).get("landing_page_url", "")))
    if re.search(r"/(?:posters?|abstracts?)(?:/|$)", landing, re.I):
        return "poster-or-abstract-url"
    for pattern in EXCLUDED_TITLE_PATTERNS:
        if pattern.search(title):
            return "title-pattern"
    return ""


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
    doi = normalize_doi(str(work.get("doi", "")))
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
        "matched_members": "",
        "publication_type": normalize_space(str(work.get("type", ""))),
        "venue": extract_venue(work),
    }


def dedupe_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    deduped: list[dict[str, str]] = []

    def priority(row: dict[str, str]) -> int:
        return {
            "article": 4,
            "review": 4,
            "conference-paper": 3,
            "preprint": 2,
        }.get(row.get("publication_type", ""), 1)

    def merge_members(first: dict[str, str], second: dict[str, str]) -> None:
        members = {
            normalize_space(item)
            for item in (first.get("matched_members", "") + ";" + second.get("matched_members", "")).split(";")
            if normalize_space(item)
        }
        first["matched_members"] = "; ".join(sorted(members))

    for row in rows:
        doi = normalize_doi(row.get("doi", ""))
        title = normalize_title(row.get("title", ""))
        key = f"doi:{doi}" if doi else f"title:{title}"
        if not key or key in {"title:"}:
            continue

        exact = next(
            (
                existing
                for existing in deduped
                if (doi and normalize_doi(existing.get("doi", "")) == doi)
                or (not doi and normalize_title(existing.get("title", "")) == title)
            ),
            None,
        )
        fuzzy = None
        if exact is None and title:
            fuzzy = next(
                (
                    existing
                    for existing in deduped
                    if title_similarity(title, normalize_title(existing.get("title", ""))) >= 0.94
                ),
                None,
            )

        existing = exact or fuzzy
        if existing is None:
            deduped.append(row)
            continue

        merge_members(existing, row)
        if priority(row) > priority(existing):
            row["matched_members"] = existing["matched_members"]
            index = deduped.index(existing)
            deduped[index] = row
    return deduped


def title_similarity(first: str, second: str) -> float:
    if not first or not second:
        return 0.0
    return SequenceMatcher(None, first, second).ratio()


def title_is_known(title: str, existing_titles: set[str]) -> bool:
    title = normalize_title(title)
    if not title:
        return False
    if title in existing_titles:
        return True
    return any(title_similarity(title, known) >= 0.96 for known in existing_titles)


def write_rows(path: Path, rows: list[dict[str, str]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=OUTPUT_COLUMNS)
        writer.writeheader()
        writer.writerows(rows)


def load_team_members(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle)
        if not reader.fieldnames:
            raise ValueError(f"Team source is empty or missing headers: {path}")
        members = []
        for row in reader:
            status = normalize_space(row.get("status", "")).lower()
            if status and status not in {"publish", "published", "active"}:
                continue
            given_name = normalize_space(row.get("name", ""))
            surname = normalize_space(row.get("surname", ""))
            display_name = normalize_space(f"{given_name} {surname}")
            if display_name:
                members.append(
                    {
                        "name": display_name,
                        "orcid_url": normalize_space(row.get("orcid_url", "")),
                    }
                )
        return members


def candidate_rows_for_author(
    member_name: str,
    orcid_url: str,
    existing_dois: set[str],
    existing_titles: set[str],
    include_known: bool,
    max_pages: int,
) -> tuple[AuthorCandidate, list[dict[str, str]], dict[str, int]]:
    author = find_best_author(member_name, orcid_url)
    works = fetch_author_works(author.author_id, max_pages=max_pages)
    candidate_rows: list[dict[str, str]] = []
    filtered: dict[str, int] = {}

    for work in works:
        reason = excluded_work_reason(work)
        if reason:
            filtered[reason] = filtered.get(reason, 0) + 1
            continue

        raw_title = normalize_title(str(work.get("title", "")))
        raw_doi = normalize_doi(str(work.get("doi", "")))
        if not include_known and ((raw_doi and raw_doi in existing_dois) or title_is_known(raw_title, existing_titles)):
            continue

        row = work_to_row(work)
        if not row["title"] or not row["year"]:
            continue
        if not include_known:
            if normalize_doi(row["doi"]) in existing_dois or title_is_known(row["title"], existing_titles):
                continue
        row["matched_members"] = member_name
        candidate_rows.append(row)

    return author, candidate_rows, filtered


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    source_group = parser.add_mutually_exclusive_group(required=True)
    source_group.add_argument("--author", help='Author name, e.g. "Paolo Soda".')
    source_group.add_argument(
        "--team",
        action="store_true",
        help="Discover candidates for every active member in the Team sheet.",
    )
    parser.add_argument(
        "--existing",
        default=str(DEFAULT_EXISTING),
        help="Existing publications CSV used to exclude already-known papers.",
    )
    parser.add_argument(
        "--output", default="", help="Output CSV for discovered candidate papers."
    )
    parser.add_argument(
        "--team-source",
        default=str(DEFAULT_TEAM_SOURCE),
        help="Team CSV used with --team.",
    )
    parser.add_argument(
        "--max-pages",
        type=int,
        default=8,
        help="Maximum OpenAlex pages per author (200 works per page).",
    )
    parser.add_argument(
        "--include-known",
        action="store_true",
        help="Do not exclude papers already present in the main publications CSV.",
    )
    args = parser.parse_args()

    if not os.environ.get(OPENALEX_API_KEY_ENV, "").strip():
        parser.error(
            "OpenAlex now requires an API key. Create a free key at "
            "https://openalex.org/settings/api and set OPENALEX_API_KEY before running this command."
        )

    existing_dois, existing_titles = load_existing_publications(Path(args.existing))
    output = Path(args.output or (DEFAULT_TEAM_OUTPUT if args.team else DEFAULT_OUTPUT))

    candidate_rows: list[dict[str, str]] = []
    failures: list[str] = []
    filtered_total: dict[str, int] = {}

    if args.team:
        members = load_team_members(Path(args.team_source))
        for member in members:
            try:
                author, rows, filtered = candidate_rows_for_author(
                    member["name"],
                    member["orcid_url"],
                    existing_dois,
                    existing_titles,
                    args.include_known,
                    args.max_pages,
                )
                candidate_rows.extend(rows)
                for reason, count in filtered.items():
                    filtered_total[reason] = filtered_total.get(reason, 0) + count
                print(f"Checked {member['name']} -> {author.display_name} ({len(rows)} candidates)")
                time.sleep(0.5)
            except Exception as exc:  # noqa: BLE001
                failures.append(f"{member['name']}: {exc}")
                log(f"Warning: could not check {member['name']}: {exc}")
    else:
        author, candidate_rows, filtered = candidate_rows_for_author(
            args.author,
            "",
            existing_dois,
            existing_titles,
            args.include_known,
            args.max_pages,
        )
        filtered_total = filtered

    candidate_rows = dedupe_rows(candidate_rows)
    candidate_rows.sort(key=lambda row: (row["year"], row["title"]), reverse=True)

    if failures:
        print("No CSV written because the Team audit was incomplete.")
        return 2

    write_rows(output, candidate_rows)

    scope = "the active Team" if args.team else args.author
    print(f"Discovered {len(candidate_rows)} candidate papers for {scope}.")
    print(f"Filtered {sum(filtered_total.values())} editorial/front-matter/non-paper records.")
    if filtered_total:
        print("Filter summary: " + ", ".join(f"{key}={value}" for key, value in sorted(filtered_total.items())))
    print(f"Wrote candidate CSV to {output}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
