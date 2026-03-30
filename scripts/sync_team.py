#!/usr/bin/env python3
"""Sync a shared team sheet into _data/team.yml and generated profile pages.

The script accepts either:
- a local CSV file, or
- a Google Sheets URL / published CSV URL

Photos are resolved from a local folder so the workflow stays reliable without
Google API credentials. If a public Google Drive folder URL is provided, the
script also tries a best-effort download into the local upload cache first.
If a matching photo is found, it is copied into assets/team_photos/ and linked
automatically from the generated site data.
"""

from __future__ import annotations

import argparse
import csv
import io
import json
import re
import shutil
import sys
import urllib.request
from pathlib import Path
from typing import Any


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_CONFIG = ROOT / "shared" / "team_sync.json"
DEFAULT_SOURCE = ROOT / "shared" / "team_sheet.csv"
DEFAULT_OUTPUT = ROOT / "_data" / "team.yml"
DEFAULT_PAGES_DIR = ROOT / "_pages" / "team"
DEFAULT_PHOTO_SOURCE = ROOT / "shared" / "team_photos_uploads"
DEFAULT_PHOTO_DEST = ROOT / "assets" / "team_photos"
DEFAULT_BIB = ROOT / "_bibliography" / "papers.bib"
DEFAULT_PLACEHOLDER = "/assets/img/prof_pic_color.png"
USER_AGENT = "ArcoLabTeamSync/1.0 (arcolab@unicampus.it)"

REQUIRED_COLUMNS = {
    "status",
    "name",
    "surname",
    "role",
    "title",
    "email",
    "external_url",
    "scholar_url",
    "orcid_url",
    "interests",
    "short_bio",
    "bio",
    "github_url",
    "linkedin_url",
}

ROLE_META = {
    "pi": {
        "group_label": "Principal Investigator",
        "card_label": "Principal Investigator",
        "sort": 0,
    },
    "faculty": {
        "group_label": "Faculty",
        "card_label": "Faculty",
        "sort": 1,
    },
    "researcher": {
        "group_label": "Researchers",
        "card_label": "Researcher",
        "sort": 2,
    },
    "postdoc": {
        "group_label": "Postdoctoral Researchers",
        "card_label": "Postdoctoral Researcher",
        "sort": 3,
    },
    "phd": {
        "group_label": "PhD Students",
        "card_label": "PhD Student",
        "sort": 4,
    },
    "student": {
        "group_label": "Students",
        "card_label": "Student",
        "sort": 5,
    },
    "collaborator": {
        "group_label": "Collaborators",
        "card_label": "Collaborator",
        "sort": 6,
    },
    "alumni": {
        "group_label": "Alumni",
        "card_label": "Alumnus",
        "sort": 7,
    },
}

PHOTO_EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")


def log(message: str) -> None:
    print(message, file=sys.stderr)


def load_config(path: Path) -> dict[str, Any]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def normalize_space(value: str) -> str:
    return re.sub(r"\s+", " ", value or "").strip()


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


def first_non_empty(*values: str) -> str:
    for value in values:
        if normalize_space(str(value)):
            return normalize_space(str(value))
    return ""


def canonical_url(value: str) -> str:
    value = normalize_space(value).strip().rstrip("/")
    return value.lower()


def is_google_scholar_url(value: str) -> bool:
    return "scholar.google." in canonical_url(value)


def truthy(value: str) -> bool:
    return str(value).strip().lower() in {"1", "true", "yes", "y"}


def slugify(value: str) -> str:
    value = normalize_space(value).lower()
    value = re.sub(r"[^a-z0-9]+", "-", value)
    return value.strip("-") or "member"


def normalize_role(value: str) -> str:
    key = normalize_space(value).lower()
    aliases = {
        "prof": "pi",
        "professor": "faculty",
        "faculty member": "faculty",
        "researchers": "researcher",
        "post-doc": "postdoc",
        "phd candidate": "phd",
        "phd candidates": "phd",
        "phd student": "phd",
        "phd students": "phd",
        "student": "student",
        "students": "student",
        "collaborators": "collaborator",
    }
    key = aliases.get(key, key)
    return key if key in ROLE_META else "researcher"


def split_list(value: str) -> list[str]:
    if not value:
        return []
    parts = [normalize_space(part) for part in value.split(";")]
    return [part for part in parts if part]


def yaml_quote(value: str) -> str:
    value = str(value)
    escaped = value.replace("\\", "\\\\").replace('"', '\\"')
    return f'"{escaped}"'


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
        raise ValueError("The team sheet is empty or missing a header row.")

    fieldnames = {name.strip() for name in reader.fieldnames if name}
    missing = REQUIRED_COLUMNS - fieldnames
    if missing:
        raise ValueError("Missing required CSV columns: " + ", ".join(sorted(missing)))

    rows: list[dict[str, str]] = []
    for row in reader:
        cleaned = {
            key.strip(): normalize_space(value)
            for key, value in row.items()
            if key
        }
        if any(cleaned.values()):
            rows.append(cleaned)
    return rows


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
        html = fetch_text(listing_url)
    except Exception as exc:  # noqa: BLE001
        log(f"Warning: could not fetch Google Drive folder listing: {exc}")
        return []

    files: list[dict[str, str]] = []
    seen_ids: set[str] = set()
    entry_pattern = re.compile(
        r'<a href="https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view[^"]*"[^>]*>.*?<div class="flip-entry-title">([^<]+)</div>',
        re.IGNORECASE | re.DOTALL,
    )
    fallback_pattern = re.compile(
        r'href="https://drive\.google\.com/file/d/([a-zA-Z0-9_-]+)/view[^"]*"[^>]*>.*?>([^<]+\.(?:png|jpe?g|webp))<',
        re.IGNORECASE | re.DOTALL,
    )

    for pattern in (entry_pattern, fallback_pattern):
        for match in pattern.finditer(html):
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


def download_drive_photos(folder_url: str, destination: Path) -> None:
    folder_url = normalize_space(folder_url)
    if not folder_url:
        return

    destination.mkdir(parents=True, exist_ok=True)
    files = parse_drive_folder_listing(folder_url)
    if not files:
        log("Warning: no downloadable files were discovered in the Google Drive photo folder.")
        return

    for file_info in files:
        filename = normalize_space(file_info["name"])
        if not filename.lower().endswith(PHOTO_EXTENSIONS):
            continue
        try:
            request = urllib.request.Request(
                file_info["download_url"],
                headers={"User-Agent": USER_AGENT},
            )
            with urllib.request.urlopen(request, timeout=30) as response:
                (destination / filename).write_bytes(response.read())
        except Exception as exc:  # noqa: BLE001
            log(f"Warning: failed to download Drive photo {filename}: {exc}")


def photo_candidates(name: str, surname: str) -> list[str]:
    bases = []
    joined = f"{name}_{surname}".lower()
    joined = re.sub(r"[^a-z0-9]+", "_", joined).strip("_")
    if joined:
        bases.append(joined)
    bases.append(slugify(f"{name} {surname}").replace("-", "_"))
    return list(dict.fromkeys(bases))


def find_photo_file(source_dir: Path, name: str, surname: str) -> Path | None:
    if not source_dir.exists():
        return None
    candidates = photo_candidates(name, surname)
    indexed_files = {
        path.name.lower(): path
        for path in source_dir.iterdir()
        if path.is_file()
    }
    for candidate in candidates:
        for extension in PHOTO_EXTENSIONS:
            key = f"{candidate}{extension}".lower()
            if key in indexed_files:
                return indexed_files[key]
    return None


def sync_photo(
    photo_source: Path,
    photo_dest: Path,
    name: str,
    surname: str,
) -> str:
    photo_dest.mkdir(parents=True, exist_ok=True)
    source = find_photo_file(photo_source, name, surname)
    if not source:
        source = find_photo_file(ROOT / "faces", name, surname)
    if not source:
        return DEFAULT_PLACEHOLDER

    target_name = f"{photo_candidates(name, surname)[0]}{source.suffix.lower()}"
    target = photo_dest / target_name
    shutil.copy2(source, target)
    return f"/assets/team_photos/{target_name}"


def normalize_person_string(value: str) -> str:
    value = normalize_space(value).lower()
    value = re.sub(r"[^a-z0-9 ]+", " ", value)
    return normalize_space(value)


def author_matches_member(author: str, name: str, surname: str) -> bool:
    author = normalize_person_string(author)
    name = normalize_person_string(name)
    surname = normalize_person_string(surname)
    if not author or not surname:
        return False
    if surname not in author:
        return False
    if name and name in author:
        return True
    given = name.split()[0] if name else ""
    return bool(given and given in author)


def parse_bibliography(path: Path) -> list[dict[str, str]]:
    if not path.exists():
        return []
    content = path.read_text(encoding="utf-8")
    entries: list[dict[str, str]] = []
    for match in re.finditer(r"@(?P<type>\w+)\{(?P<key>[^,]+),(?P<body>.*?)\n\}", content, re.DOTALL):
        body = match.group("body")
        entry = {
            "entry_type": match.group("type"),
            "key": normalize_space(match.group("key")),
        }
        for field_match in re.finditer(
            r"^\s*(?P<field>[a-zA-Z0-9_]+)\s*=\s*\{(?P<value>.*)\},?\s*$",
            body,
            re.MULTILINE,
        ):
            entry[field_match.group("field").lower()] = normalize_space(field_match.group("value"))
        entries.append(entry)
    return entries


def venue_for_entry(entry: dict[str, str]) -> str:
    return first_non_empty(entry.get("journal", ""), entry.get("booktitle", ""), entry.get("publisher", ""))


def selected_publications_for_member(
    bibliography: list[dict[str, str]],
    name: str,
    surname: str,
) -> list[dict[str, str]]:
    publications: list[dict[str, str]] = []
    for entry in bibliography:
        if entry.get("selected", "").lower() != "true":
            continue
        authors = split_list(entry.get("author", "").replace(" and ", ";"))
        if not any(author_matches_member(author, name, surname) for author in authors):
            continue
        publications.append(
            {
                "title": entry.get("title", ""),
                "venue": venue_for_entry(entry),
                "year": entry.get("year", ""),
                "doi_url": f"https://doi.org/{entry['doi']}" if entry.get("doi") else "",
                "url": entry.get("url", ""),
                "pdf": entry.get("pdf", ""),
                "code": entry.get("code", ""),
                "website": entry.get("website", ""),
            }
        )
    publications.sort(key=lambda item: (item.get("year", ""), item.get("title", "")), reverse=True)
    return publications


def build_member(
    row: dict[str, str],
    bibliography: list[dict[str, str]],
    photo_source: Path,
    photo_dest: Path,
) -> dict[str, Any]:
    name = normalize_space(row.get("name", ""))
    surname = normalize_space(row.get("surname", ""))
    full_name = normalize_space(f"{name} {surname}")
    role = normalize_role(row.get("role", ""))
    role_meta = ROLE_META[role]
    slug = slugify(full_name)
    interests = split_list(row.get("interests", ""))
    photo = sync_photo(photo_source, photo_dest, name, surname)
    selected_publications = selected_publications_for_member(bibliography, name, surname)

    return {
        "name": full_name,
        "given_name": name,
        "surname": surname,
        "slug": slug,
        "profile_path": f"/team/{slug}/",
        "role": role,
        "role_label": role_meta["card_label"],
        "role_group_label": role_meta["group_label"],
        "role_sort": role_meta["sort"],
        "title": row.get("title", ""),
        "email": row.get("email", ""),
        "photo": photo,
        "external_url": row.get("external_url", ""),
        "scholar_url": row.get("scholar_url", ""),
        "orcid_url": row.get("orcid_url", ""),
        "github_url": row.get("github_url", ""),
        "linkedin_url": row.get("linkedin_url", ""),
        "interests": interests,
        "short_bio": row.get("short_bio", ""),
        "bio": row.get("bio", ""),
        "selected_publications": selected_publications,
    }


def sort_key(member: dict[str, Any]) -> tuple[Any, ...]:
    return (
        member["role_sort"],
        member["surname"].lower(),
        member["given_name"].lower(),
    )


def write_yaml(members: list[dict[str, Any]], destination: Path) -> None:
    lines = [
        "# This file is generated by scripts/sync_team.py from shared/team_sheet.csv.",
        "# Manual edits will be overwritten the next time the sync script runs.",
    ]

    for index, member in enumerate(members, start=1):
        lines.append(f"- name: {yaml_quote(member['name'])}")
        lines.append(f"  given_name: {yaml_quote(member['given_name'])}")
        lines.append(f"  surname: {yaml_quote(member['surname'])}")
        lines.append(f"  slug: {member['slug']}")
        lines.append(f"  profile_path: {member['profile_path']}")
        lines.append(f"  role: {member['role']}")
        lines.append(f"  role_label: {yaml_quote(member['role_label'])}")
        lines.append(f"  role_group_label: {yaml_quote(member['role_group_label'])}")
        lines.append(f"  title: {yaml_quote(member['title'])}")
        lines.append(f"  email: {yaml_quote(member['email'])}")
        lines.append(f"  photo: {member['photo']}")
        lines.append(f"  external_url: {yaml_quote(member['external_url'])}")
        lines.append(f"  scholar_url: {yaml_quote(member['scholar_url'])}")
        lines.append(f"  orcid_url: {yaml_quote(member['orcid_url'])}")
        lines.append(f"  github_url: {yaml_quote(member['github_url'])}")
        lines.append(f"  linkedin_url: {yaml_quote(member['linkedin_url'])}")
        if member["interests"]:
            lines.append("  interests:")
            for interest in member["interests"]:
                lines.append(f"    - {yaml_quote(interest)}")
        else:
            lines.append("  interests: []")
        lines.append(f"  short_bio: {yaml_quote(member['short_bio'])}")
        lines.append(f"  bio: {yaml_quote(member['bio'])}")
        lines.append(f"  order: {index}")
        if member["selected_publications"]:
            lines.append("  selected_publications:")
            for publication in member["selected_publications"]:
                lines.append(f"    - title: {yaml_quote(publication['title'])}")
                lines.append(f"      venue: {yaml_quote(publication['venue'])}")
                lines.append(f"      year: {yaml_quote(publication['year'])}")
                lines.append(f"      doi_url: {yaml_quote(publication['doi_url'])}")
                lines.append(f"      url: {yaml_quote(publication['url'])}")
                lines.append(f"      pdf: {yaml_quote(publication['pdf'])}")
                lines.append(f"      code: {yaml_quote(publication['code'])}")
                lines.append(f"      website: {yaml_quote(publication['website'])}")
        else:
            lines.append("  selected_publications: []")

    destination.write_text("\n".join(lines) + "\n", encoding="utf-8")


def render_profile_page(member: dict[str, Any]) -> str:
    links = []
    if member["external_url"]:
        links.append(
            '        <a class="member-profile-link-btn member-profile-link-btn-primary" href="{{ member.external_url }}"><i class="fa-solid fa-building-columns"></i><span>Official Profile</span></a>'
        )
    if member["scholar_url"] and is_google_scholar_url(member["scholar_url"]) and canonical_url(member["scholar_url"]) != canonical_url(member["external_url"]):
        links.append(
            '        <a class="member-profile-link-btn member-profile-link-btn-scholar" href="{{ member.scholar_url }}"><i class="fa-solid fa-graduation-cap"></i><span>Google Scholar</span></a>'
        )
    if member["orcid_url"]:
        links.append(
            '        <a class="member-profile-link-btn member-profile-link-btn-orcid" href="{{ member.orcid_url }}"><i class="fa-solid fa-id-badge"></i><span>ORCID</span></a>'
        )
    if member["github_url"]:
        links.append(
            '        <a class="member-profile-link-btn member-profile-link-btn-github" href="{{ member.github_url }}"><i class="fa-brands fa-github"></i><span>GitHub</span></a>'
        )
    if member["linkedin_url"]:
        links.append(
            '        <a class="member-profile-link-btn member-profile-link-btn-linkedin" href="{{ member.linkedin_url }}"><i class="fa-brands fa-linkedin-in"></i><span>LinkedIn</span></a>'
        )
    links.append(
        '        <a class="member-profile-link-btn member-profile-link-btn-publications" href="/publications/?search={{ member.name | url_encode }}"><i class="fa-solid fa-book-open"></i><span>Browse Publications</span></a>'
    )
    links.append(
        '        <a class="member-profile-link-btn member-profile-link-btn-back" href="/team/"><i class="fa-solid fa-arrow-left"></i><span>Back to Team</span></a>'
    )

    return f"""---
layout: page
title: {member['name']}
permalink: /team/{member['slug']}/
description: Full profile and selected publications of {member['name']}.
---

{{% assign member = site.data.team | where: "slug", "{member['slug']}" | first %}}

<section class="member-profile">
  <div class="member-profile-hero">
    <div class="member-profile-media">
      <img src="{{{{ member.photo }}}}" alt="{{{{ member.name }}}}">
    </div>
    <div class="member-profile-copy">
      <p class="member-profile-kicker">{{{{ member.role_label }}}}</p>
      <h1>{{{{ member.name }}}}</h1>
      <p class="member-profile-role">{{{{ member.title }}}}</p>
      <p class="member-profile-bio">{{{{ member.bio }}}}</p>
      <div class="member-profile-tags">
        {{% for interest in member.interests %}}
          <span>{{{{ interest }}}}</span>
        {{% endfor %}}
      </div>
      <div class="member-profile-links">
{chr(10).join(links)}
      </div>
    </div>
  </div>

  <div class="member-profile-section">
    <h2>Selected Publications</h2>
    {{% if member.selected_publications and member.selected_publications != empty %}}
      {{% include member_selected_publications.liquid %}}
    {{% else %}}
      <p class="member-profile-footnote">Selected publications will appear here when they are marked as featured in the bibliography workflow.</p>
    {{% endif %}}

    {{% if member.scholar_url and member.scholar_url contains 'scholar.google.' %}}
      <p class="member-profile-footnote">
        Full publication list:
        <a href="{{{{ member.scholar_url }}}}">{{{{ member.scholar_url }}}}</a>
      </p>
    {{% else %}}
      <p class="member-profile-footnote">
        Browse all indexed publications for this author:
        <a href="/publications/?search={member['name'].replace(' ', '%20')}">/publications/?search={member['name']}</a>
      </p>
    {{% endif %}}
  </div>
</section>
"""


def write_pages(members: list[dict[str, Any]], destination: Path) -> None:
    destination.mkdir(parents=True, exist_ok=True)
    for member in members:
        page_path = destination / f"{member['slug']}.md"
        page_path.write_text(render_profile_page(member), encoding="utf-8")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        default="",
        help="Path to a local CSV, a Google Sheets URL, or a published Google Sheets CSV URL.",
    )
    parser.add_argument(
        "--config",
        default=str(DEFAULT_CONFIG),
        help="Optional JSON config file. Defaults to shared/team_sync.json.",
    )
    parser.add_argument(
        "--output",
        default=str(DEFAULT_OUTPUT),
        help="Target YAML file. Defaults to _data/team.yml.",
    )
    parser.add_argument(
        "--pages-dir",
        default=str(DEFAULT_PAGES_DIR),
        help="Directory where member profile pages are generated.",
    )
    parser.add_argument(
        "--photos-source",
        default="",
        help="Local folder containing uploaded team photos.",
    )
    parser.add_argument(
        "--photos-drive-folder",
        default="",
        help="Public Google Drive folder URL used to auto-download team photos.",
    )
    parser.add_argument(
        "--photos-dest",
        default=str(DEFAULT_PHOTO_DEST),
        help="Destination folder for site-ready team photos.",
    )
    parser.add_argument(
        "--bib",
        default=str(DEFAULT_BIB),
        help="Bibliography file used to compute selected publications.",
    )
    args = parser.parse_args()

    config = load_config(Path(args.config))
    source = first_non_empty(args.source, str(config.get("source", "")), str(DEFAULT_SOURCE))
    photos_source = Path(
        first_non_empty(args.photos_source, str(config.get("photos_source", "")), str(DEFAULT_PHOTO_SOURCE))
    )
    photos_drive_folder = first_non_empty(
        args.photos_drive_folder,
        str(config.get("photos_drive_folder", "")),
    )
    photos_dest = Path(args.photos_dest)
    bibliography = parse_bibliography(Path(args.bib))

    if photos_drive_folder:
        download_drive_photos(photos_drive_folder, photos_source)

    mirror_path = DEFAULT_SOURCE if re.match(r"^https?://", normalize_google_sheet_source(source)) else None
    rows = load_rows(source, mirror_path=mirror_path)
    members: list[dict[str, Any]] = []
    seen_slugs: set[str] = set()

    for row in rows:
        status = normalize_space(row.get("status", "")).lower()
        if status in {"draft", "hide", "ignore", "skip"}:
            continue
        member = build_member(row, bibliography, photos_source, photos_dest)
        if member["slug"] in seen_slugs:
            log(f"Skipping duplicate member slug: {member['slug']}")
            continue
        seen_slugs.add(member["slug"])
        members.append(member)

    members.sort(key=sort_key)

    output = Path(args.output)
    write_yaml(members, output)
    write_pages(members, Path(args.pages_dir))

    print(f"Wrote {len(members)} team profiles to {output} from {source}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
