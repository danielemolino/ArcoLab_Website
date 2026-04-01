#!/usr/bin/env python3
"""Push the local publications CSV into the shared Google Sheet.

This is intentionally isolated from the rest of the site. It only:
- reads `shared/publications_sheet.csv`
- resolves spreadsheet id + gid from `shared/publications_sync.json`
- authenticates with a local Google service account JSON
- clears the target sheet tab
- writes the CSV rows back into the tab

Credentials are local-only and should not be committed.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parent.parent
DEFAULT_SOURCE = ROOT / "shared" / "publications_sheet.csv"
DEFAULT_SYNC_CONFIG = ROOT / "shared" / "publications_sync.json"
DEFAULT_CREDENTIALS = ROOT / "shared" / "google-service-account.json"
DEFAULT_KEYWORD_VOCAB = ROOT / "shared" / "publication_keyword_vocab.csv"
DEFAULT_PROJECTS_DIR = ROOT / "_projects"
SCOPES = ["https://www.googleapis.com/auth/spreadsheets"]


def fail(message: str) -> int:
    print(message, file=sys.stderr)
    return 1


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def extract_sheet_identifiers(source_url: str) -> tuple[str, int]:
    match = re.search(r"/spreadsheets/d/([a-zA-Z0-9-_]+)", source_url)
    if not match:
      raise ValueError("Could not extract spreadsheet id from publications_sync.json source URL.")
    spreadsheet_id = match.group(1)

    gid_match = re.search(r"[?#&]gid=([0-9]+)", source_url)
    gid = int(gid_match.group(1)) if gid_match else 0
    return spreadsheet_id, gid


def load_csv_values(path: Path) -> list[list[str]]:
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.reader(handle)
        return [row for row in reader]


def load_project_rows(projects_dir: Path) -> list[list[str]]:
    rows = [["project_id", "title", "state"]]
    for path in sorted(projects_dir.glob("*.md")):
        content = path.read_text(encoding="utf-8")
        if not content.startswith("---"):
            continue
        parts = content.split("---", 2)
        if len(parts) < 3:
            continue
        frontmatter_text = parts[1]
        title_match = re.search(r"^title:\s*(.+)$", frontmatter_text, re.MULTILINE)
        state_match = re.search(r"^project_state:\s*(.+)$", frontmatter_text, re.MULTILINE)
        title = title_match.group(1).strip().strip('"').strip("'") if title_match else path.stem
        state = state_match.group(1).strip().strip('"').strip("'") if state_match else ""
        rows.append(
            [
                path.stem,
                title,
                state,
            ]
        )
    return rows


def get_sheet_title(service, spreadsheet_id: str, gid: int) -> str:
    metadata = (
        service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id, fields="sheets(properties(sheetId,title))")
        .execute()
    )
    for sheet in metadata.get("sheets", []):
        props = sheet.get("properties", {})
        if int(props.get("sheetId", -1)) == gid:
            return props.get("title", "")
    raise ValueError(f"Could not find a sheet tab with gid={gid}.")


def ensure_sheet_title(service, spreadsheet_id: str, title: str) -> None:
    metadata = (
        service.spreadsheets()
        .get(spreadsheetId=spreadsheet_id, fields="sheets(properties(title))")
        .execute()
    )
    existing = {
        sheet.get("properties", {}).get("title", "")
        for sheet in metadata.get("sheets", [])
    }
    if title in existing:
        return
    service.spreadsheets().batchUpdate(
        spreadsheetId=spreadsheet_id,
        body={"requests": [{"addSheet": {"properties": {"title": title}}}]},
    ).execute()


def write_values(service, spreadsheet_id: str, sheet_title: str, values: list[list[str]]) -> None:
    target_range = f"'{sheet_title}'!A1:Z"
    service.spreadsheets().values().clear(
        spreadsheetId=spreadsheet_id,
        range=target_range,
        body={},
    ).execute()

    service.spreadsheets().values().update(
        spreadsheetId=spreadsheet_id,
        range=f"'{sheet_title}'!A1",
        valueInputOption="RAW",
        body={"values": values},
    ).execute()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", default=str(DEFAULT_SOURCE), help="Local CSV file to upload.")
    parser.add_argument(
        "--sync-config",
        default=str(DEFAULT_SYNC_CONFIG),
        help="JSON file containing the shared Google Sheet URL.",
    )
    parser.add_argument(
        "--credentials",
        default=str(DEFAULT_CREDENTIALS),
        help="Local Google service account JSON file.",
    )
    parser.add_argument(
        "--keyword-vocab",
        default=str(DEFAULT_KEYWORD_VOCAB),
        help="CSV file containing the controlled keyword vocabulary.",
    )
    parser.add_argument(
        "--projects-dir",
        default=str(DEFAULT_PROJECTS_DIR),
        help="Directory containing project pages used to derive project ids.",
    )
    args = parser.parse_args()

    source = Path(args.source)
    sync_config = Path(args.sync_config)
    credentials_path = Path(args.credentials)
    keyword_vocab = Path(args.keyword_vocab)
    projects_dir = Path(args.projects_dir)

    if not source.exists():
        return fail(f"Missing CSV source: {source}")
    if not sync_config.exists():
        return fail(f"Missing sync config: {sync_config}")
    if not credentials_path.exists():
        return fail(
            "Missing Google service account JSON.\n"
            f"Expected at: {credentials_path}\n"
            "Create a service account, download the JSON key, share the sheet with that account, and place the file there."
        )

    try:
        from google.oauth2.service_account import Credentials
        from googleapiclient.discovery import build
    except ImportError:
        return fail(
            "Missing Google API dependencies.\n"
            "Install them with:\n"
            "python3 -m pip install google-api-python-client google-auth"
        )

    sync_data = load_json(sync_config)
    source_url = sync_data.get("source", "")
    if not source_url:
        return fail("shared/publications_sync.json does not contain a `source` URL.")

    spreadsheet_id, gid = extract_sheet_identifiers(source_url)
    values = load_csv_values(source)
    keyword_values = load_csv_values(keyword_vocab) if keyword_vocab.exists() else []
    project_values = load_project_rows(projects_dir) if projects_dir.exists() else []

    credentials = Credentials.from_service_account_file(str(credentials_path), scopes=SCOPES)
    service = build("sheets", "v4", credentials=credentials, cache_discovery=False)

    sheet_title = get_sheet_title(service, spreadsheet_id, gid)
    write_values(service, spreadsheet_id, sheet_title, values)

    if keyword_values:
        ensure_sheet_title(service, spreadsheet_id, "keyword_vocab")
        write_values(service, spreadsheet_id, "keyword_vocab", keyword_values)

    if project_values:
        ensure_sheet_title(service, spreadsheet_id, "project_ids")
        write_values(service, spreadsheet_id, "project_ids", project_values)

    print(
        f"Pushed {max(len(values) - 1, 0)} publication rows from {source} "
        f"to spreadsheet {spreadsheet_id} (gid={gid}, sheet='{sheet_title}')."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
