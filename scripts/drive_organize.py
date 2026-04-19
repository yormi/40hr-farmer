#!/usr/bin/env python3
"""
Move non-image/non-video files from a Google Drive shared-drive folder
into a subfolder (_Documents & Other Files).

Usage:
    python scripts/drive_organize.py

Prerequisites:
    pip install google-api-python-client google-auth-oauthlib google-auth-httplib2

OAuth setup:
    1. Go to https://console.cloud.google.com/apis/credentials
    2. Create an OAuth 2.0 Client ID (Desktop app) — or reuse an existing one
    3. Download the JSON and save it as .secrets/oauth-client.json
    4. Enable the Google Drive API in the same project
"""

import json
import os
import sys
from pathlib import Path

from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

# ---------- Config ----------
REPO_ROOT = Path(__file__).resolve().parent.parent
SECRETS_DIR = REPO_ROOT / ".secrets"
CLIENT_SECRET_FILE = SECRETS_DIR / "oauth-client.json"
TOKEN_FILE = SECRETS_DIR / "drive-token.json"

SCOPES = ["https://www.googleapis.com/auth/drive"]

SOURCE_FOLDER_ID = "1mY0AZgZLRcCPrn7ilcH4MLO9WHux4uQt"
DEST_FOLDER_ID = "1S75UXDkzYflz2OjmYqn7GXwuUC2P4mdM"


# ---------- Auth ----------
def get_credentials():
    """Return valid Google credentials, prompting OAuth flow if needed."""
    creds = None

    if TOKEN_FILE.exists():
        creds = Credentials.from_authorized_user_file(str(TOKEN_FILE), SCOPES)

    if creds and creds.expired and creds.refresh_token:
        print("Refreshing expired token...")
        creds.refresh(Request())
    elif not creds or not creds.valid:
        if not CLIENT_SECRET_FILE.exists():
            print(f"ERROR: OAuth client credentials not found at {CLIENT_SECRET_FILE}")
            print()
            print("To fix this:")
            print("  1. Go to https://console.cloud.google.com/apis/credentials")
            print("  2. Create or download an OAuth 2.0 Desktop client JSON")
            print(f"  3. Save it as: {CLIENT_SECRET_FILE}")
            print("  4. Make sure the Google Drive API is enabled in that project")
            sys.exit(1)

        flow = InstalledAppFlow.from_client_secrets_file(
            str(CLIENT_SECRET_FILE), SCOPES
        )
        creds = flow.run_local_server(port=0)

    # Save token for next run
    SECRETS_DIR.mkdir(exist_ok=True)
    with open(TOKEN_FILE, "w") as f:
        f.write(creds.to_json())
    print(f"Token saved to {TOKEN_FILE}")

    return creds


# ---------- Drive helpers ----------
def list_files_in_folder(service, folder_id):
    """List all files (not folders) in a shared-drive folder, paginated."""
    all_files = []
    page_token = None

    while True:
        resp = service.files().list(
            q=f"'{folder_id}' in parents and mimeType != 'application/vnd.google-apps.folder'",
            fields="nextPageToken, files(id, name, mimeType)",
            pageSize=100,
            supportsAllDrives=True,
            includeItemsFromAllDrives=True,
            corpora="allDrives",
            pageToken=page_token,
        ).execute()

        all_files.extend(resp.get("files", []))
        page_token = resp.get("nextPageToken")
        if not page_token:
            break

    return all_files


def move_file(service, file_id, source_folder_id, dest_folder_id):
    """Move a file from source folder to dest folder on a shared drive."""
    service.files().update(
        fileId=file_id,
        addParents=dest_folder_id,
        removeParents=source_folder_id,
        supportsAllDrives=True,
        fields="id, parents",
    ).execute()


# ---------- Main ----------
def main():
    creds = get_credentials()
    service = build("drive", "v3", credentials=creds)

    print(f"\nListing files in source folder {SOURCE_FOLDER_ID}...")
    files = list_files_in_folder(service, SOURCE_FOLDER_ID)
    print(f"Found {len(files)} files (excluding subfolders)\n")

    moved = 0
    skipped = 0
    errors = []

    for f in files:
        mime = f.get("mimeType", "")
        name = f.get("name", "<unknown>")
        fid = f["id"]

        if mime.startswith("image/") or mime.startswith("video/"):
            print(f"  SKIP (media)  {name}  [{mime}]")
            skipped += 1
            continue

        # Move non-media file
        try:
            move_file(service, fid, SOURCE_FOLDER_ID, DEST_FOLDER_ID)
            print(f"  MOVED         {name}  [{mime}]")
            moved += 1
        except Exception as e:
            print(f"  ERROR         {name}  [{mime}]  -> {e}")
            errors.append((name, str(e)))

    print(f"\n--- Summary ---")
    print(f"  Total files:  {len(files)}")
    print(f"  Moved:        {moved}")
    print(f"  Skipped:      {skipped}")
    print(f"  Errors:       {len(errors)}")
    if errors:
        print("\nErrors detail:")
        for name, err in errors:
            print(f"  - {name}: {err}")


if __name__ == "__main__":
    main()
