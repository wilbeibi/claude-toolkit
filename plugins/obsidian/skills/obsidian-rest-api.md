---
name: obsidian-rest-api
description: Interact with Obsidian vault via Local REST API plugin. Use when the user needs to automate note creation, bulk updates, date-filtered searches, or Obsidian commands. Prefer simple file access for trivial queries.
---

# Obsidian Local REST API

## Summary
Use this skill primarily for reading, search, and advanced filtering (date ranges, commands). If the user just needs a single note or quick lookup, avoid the API and read the file directly. Only use write endpoints when the user explicitly requests updates.

## Details

Prerequisites:
1. Obsidian with Local REST API plugin enabled
2. API running at https://127.0.0.1:27124
3. API key in `OBSIDIAN_REST_API_KEY`
4. `uv` installed

Python template (uv style):
```python
# /// script
# dependencies = ["requests"]
# ///
import os
import requests
from urllib.parse import quote

API_KEY = os.environ.get("OBSIDIAN_REST_API_KEY")
BASE_URL = "https://127.0.0.1:27124"
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}
requests.packages.urllib3.disable_warnings()
```

Response filtering:
- Prefer `jq` when responses are large JSON arrays.
- For small payloads, filter in Python to avoid extra dependencies.

Natural language date search:
1. Convert the date phrase to `start_date` and `end_date`.
2. `POST /search/simple` with the topic keyword.
3. Read each candidate note and parse a date from frontmatter (`created`, `date`) or file metadata.
4. Filter by date range.

Frontmatter parse example:
```python
# /// script
# dependencies = ["requests"]
# ///
from datetime import datetime

created_date = None
for line in note_content.split("\n")[:20]:
    if line.startswith("created:"):
        date_str = line.split(":", 1)[1].strip()
        created_date = datetime.strptime(date_str, "%Y-%m-%d")
        break
```

## Reference
Key endpoints (read-first):
- Read note: `GET /vault/{path}`
- Search: `POST /search/simple`, `POST /search` (Dataview)
- Periodic read: `GET /periodic/daily`, `GET /periodic/daily/{YYYY-MM-DD}`
- Active file read: `GET /active`
- Commands list/run: `GET /commands`, `POST /commands/{id}`
- Open file: `POST /open/{path}`

Write endpoints exist (`PUT/PATCH/DELETE /vault/{path}`, `PUT /periodic/daily`, `PUT /active`) but only use them when the user explicitly asks to modify notes.

Minimal calls:
```python
# /// script
# dependencies = ["requests"]
# ///
note_path = quote("path/to/note.md")
response = requests.get(f"{BASE_URL}/vault/{note_path}", headers=HEADERS, verify=False)
```
```python
# /// script
# dependencies = ["requests"]
# ///
response = requests.post(
    f"{BASE_URL}/search/simple/",
    headers=HEADERS,
    json={"query": "keyword"},
    verify=False
)
```

Troubleshooting:
- 401: check API key
- SSL: use `verify=False` for local certs
- 404: ensure `.md` extension and URL-encoded path
