---
name: obsidian-rest-api
description: Interact with Obsidian vault via Local REST API plugin. Use when the user needs to create, read, update, delete, or search notes in their Obsidian vault, work with periodic notes (daily/weekly/monthly), execute Obsidian commands, or manage their knowledge base programmatically. Enables automation and integration between Claude Code and Obsidian.
---

# Obsidian Local REST API Integration

This skill enables programmatic interaction with an Obsidian vault through the Local REST API plugin.

## Prerequisites

The user must have:
1. Obsidian installed with the "Local REST API" plugin enabled
2. The plugin configured and running (typically on https://127.0.0.1:27124)
3. API key stored in Fish environment variable: `OBSIDIAN_REST_API_KEY`
4. `uv` installed for dependency management

## Base Configuration

```python
# /// script
# dependencies = ["requests"]
# ///
import os
import requests
from urllib.parse import quote

# Get API key from Fish environment
API_KEY = os.environ.get('OBSIDIAN_REST_API_KEY')
BASE_URL = "https://127.0.0.1:27124"

# Default headers for all requests
HEADERS = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# Disable SSL warnings for local development
requests.packages.urllib3.disable_warnings()
```

## Core API Endpoints

### Vault Operations

**List all notes in vault:**
```python
# /// script
# dependencies = ["requests"]
# ///
response = requests.get(
    f"{BASE_URL}/vault/",
    headers=HEADERS,
    verify=False
)
files = response.json()
```

**Read a note:**
```python
# /// script
# dependencies = ["requests"]
# ///
# Path should be URL-encoded
note_path = quote("path/to/note.md")
response = requests.get(
    f"{BASE_URL}/vault/{note_path}",
    headers=HEADERS,
    verify=False
)
content = response.text
```

**Create a new note:**
```python
# /// script
# dependencies = ["requests"]
# ///
note_path = quote("path/to/new-note.md")
content = "# New Note\n\nContent here"

response = requests.put(
    f"{BASE_URL}/vault/{note_path}",
    headers=HEADERS,
    data=content.encode('utf-8'),
    verify=False
)
```

**Update entire note:**
```python
# /// script
# dependencies = ["requests"]
# ///
note_path = quote("path/to/note.md")
new_content = "# Updated Content\n\nNew text"

response = requests.put(
    f"{BASE_URL}/vault/{note_path}",
    headers=HEADERS,
    data=new_content.encode('utf-8'),
    verify=False
)
```

**Patch/insert content into note:**
```python
# /// script
# dependencies = ["requests"]
# ///
# Insert content at a specific heading
note_path = quote("path/to/note.md")
patch_data = {
    "heading": "## Target Heading",
    "content": "New content to insert",
    "mode": "append"  # or "prepend", "replace"
}

response = requests.patch(
    f"{BASE_URL}/vault/{note_path}",
    headers=HEADERS,
    json=patch_data,
    verify=False
)
```

**Delete a note:**
```python
# /// script
# dependencies = ["requests"]
# ///
note_path = quote("path/to/note.md")
response = requests.delete(
    f"{BASE_URL}/vault/{note_path}",
    headers=HEADERS,
    verify=False
)
```

### Periodic Notes

**Get today's daily note:**
```python
# /// script
# dependencies = ["requests"]
# ///
response = requests.get(
    f"{BASE_URL}/periodic/daily/",
    headers=HEADERS,
    verify=False
)
daily_note = response.json()
```

**Create/update today's daily note:**
```python
# /// script
# dependencies = ["requests"]
# ///
content = "# Daily Note\n\n## Tasks\n- [ ] Task 1"
response = requests.put(
    f"{BASE_URL}/periodic/daily/",
    headers=HEADERS,
    data=content.encode('utf-8'),
    verify=False
)
```

**Get specific date's note:**
```python
# /// script
# dependencies = ["requests"]
# ///
# Format: YYYY-MM-DD
date = "2025-01-21"
response = requests.get(
    f"{BASE_URL}/periodic/daily/{date}",
    headers=HEADERS,
    verify=False
)
```

**Weekly and monthly notes:**
```python
# /// script
# dependencies = ["requests"]
# ///
# Current week
response = requests.get(
    f"{BASE_URL}/periodic/weekly/",
    headers=HEADERS,
    verify=False
)

# Current month
response = requests.get(
    f"{BASE_URL}/periodic/monthly/",
    headers=HEADERS,
    verify=False
)
```

### Active File

**Get currently active file:**
```python
# /// script
# dependencies = ["requests"]
# ///
response = requests.get(
    f"{BASE_URL}/active/",
    headers=HEADERS,
    verify=False
)
active_file = response.json()
```

**Update active file:**
```python
# /// script
# dependencies = ["requests"]
# ///
content = "Updated content for active file"
response = requests.put(
    f"{BASE_URL}/active/",
    headers=HEADERS,
    data=content.encode('utf-8'),
    verify=False
)
```

### Search

**Simple search:**
```python
# /// script
# dependencies = ["requests"]
# ///
params = {"query": "search term"}
response = requests.post(
    f"{BASE_URL}/search/simple/",
    headers=HEADERS,
    json=params,
    verify=False
)
results = response.json()
```

**Advanced search (Dataview query):**
```python
# /// script
# dependencies = ["requests"]
# ///
query = """
LIST
FROM "folder"
WHERE contains(file.name, "keyword")
"""

response = requests.post(
    f"{BASE_URL}/search/",
    headers=HEADERS,
    data=query.encode('utf-8'),
    verify=False
)
results = response.json()
```

### Commands

**List available commands:**
```python
# /// script
# dependencies = ["requests"]
# ///
response = requests.get(
    f"{BASE_URL}/commands/",
    headers=HEADERS,
    verify=False
)
commands = response.json()
```

**Execute a command:**
```python
# /// script
# dependencies = ["requests"]
# ///
command_id = "editor:toggle-checklist-status"
response = requests.post(
    f"{BASE_URL}/commands/{quote(command_id)}/",
    headers=HEADERS,
    verify=False
)
```

### Open Files

**Open a file in Obsidian:**
```python
# /// script
# dependencies = ["requests"]
# ///
note_path = quote("path/to/note.md")
response = requests.post(
    f"{BASE_URL}/open/{note_path}",
    headers=HEADERS,
    verify=False
)
```

## Best Practices

### Error Handling

Always wrap API calls in try-except blocks:

```python
# /// script
# dependencies = ["requests"]
# ///
try:
    response = requests.get(
        f"{BASE_URL}/vault/note.md",
        headers=HEADERS,
        verify=False,
        timeout=5
    )
    response.raise_for_status()
    content = response.text
except requests.exceptions.RequestException as e:
    print(f"API request failed: {e}")
```

### Path Handling

- Always URL-encode paths that contain spaces or special characters
- Paths are relative to vault root
- Use forward slashes (/) even on Windows
- Include `.md` extension

```python
# /// script
# dependencies = ["requests"]
# ///
from urllib.parse import quote

# Correct
path = quote("Daily Notes/2025-01-21.md")

# Handles spaces and special characters
path = quote("Projects/My Project (2025)/notes.md")
```

### Content Encoding

When sending content, encode as UTF-8 bytes:

```python
# /// script
# dependencies = ["requests"]
# ///
content = "# Note with émojis 🎉"
response = requests.put(
    url,
    headers=HEADERS,
    data=content.encode('utf-8'),  # Important!
    verify=False
)
```

### Checking API Availability

Before making requests, verify the API is accessible:

```python
# /// script
# dependencies = ["requests"]
# ///
def check_obsidian_api():
    try:
        response = requests.get(
            f"{BASE_URL}/",
            headers=HEADERS,
            verify=False,
            timeout=2
        )
        return response.status_code == 200
    except:
        return False

if not check_obsidian_api():
    print("Obsidian Local REST API is not accessible")
    print("Make sure Obsidian is running with the plugin enabled")
```

## Common Workflows

### Create a new note with template

```python
# /// script
# dependencies = ["requests"]
# ///
def create_note_from_template(path, title, tags=None):
    tags = tags or []
    tag_str = " ".join(f"#{tag}" for tag in tags)
    
    content = f"""---
title: {title}
created: {datetime.now().isoformat()}
tags: {tags}
---

# {title}

{tag_str}

## Notes

"""
    
    response = requests.put(
        f"{BASE_URL}/vault/{quote(path)}",
        headers=HEADERS,
        data=content.encode('utf-8'),
        verify=False
    )
    return response.status_code == 200
```

### Append to daily note

```python
# /// script
# dependencies = ["requests"]
# ///
def append_to_daily_note(content):
    # Get current daily note
    response = requests.get(
        f"{BASE_URL}/periodic/daily/",
        headers=HEADERS,
        verify=False
    )
    
    if response.status_code == 200:
        current = response.text
        updated = current + "\n\n" + content
        
        requests.put(
            f"{BASE_URL}/periodic/daily/",
            headers=HEADERS,
            data=updated.encode('utf-8'),
            verify=False
        )
```

### Search and update notes

```python
# /// script
# dependencies = ["requests"]
# ///
def update_notes_matching(search_term, old_text, new_text):
    # Search for notes
    results = requests.post(
        f"{BASE_URL}/search/simple/",
        headers=HEADERS,
        json={"query": search_term},
        verify=False
    ).json()
    
    # Update each matching note
    for result in results:
        path = result['path']
        content = requests.get(
            f"{BASE_URL}/vault/{quote(path)}",
            headers=HEADERS,
            verify=False
        ).text
        
        updated = content.replace(old_text, new_text)
        
        requests.put(
            f"{BASE_URL}/vault/{quote(path)}",
            headers=HEADERS,
            data=updated.encode('utf-8'),
            verify=False
        )
```

## Natural Language Search Handlers

When the user asks to "find notes about X from [time period]" or similar date-based queries:

1.  **Interpret the Date**: Use Python to calculate the specific start/end dates from the natural language (e.g., "last week", "yesterday", "Oct 2024").
2.  **Fetch & Filter Strategy**:
    *   First, use `/search/simple` with the topic keyword to get a list of candidate files.
    *   Second, iterate through the results and fetch their content/metadata.
    *   Third, parse the date from either the file's Frontmatter (e.g., `created`, `date`, `creation_date`) OR the file's last modified time if frontmatter is missing.
    *   Finally, filter the list against the calculated date range in memory.

### Example: Filter by Date Range

```python
# /// script
# dependencies = ["requests"]
# ///
from datetime import datetime, timedelta

def search_notes_by_date_range(query, start_date, end_date):
    # 1. Search for keywords
    search_response = requests.post(
        f"{BASE_URL}/search/simple/",
        headers=HEADERS,
        json={"query": query},
        verify=False
    )
    candidates = search_response.json()
    
    matches = []
    
    # 2. Iterate and filter
    for note in candidates:
        # Fetch full note content
        note_content = requests.get(
            f"{BASE_URL}/vault/{quote(note['path'])}",
            headers=HEADERS,
            verify=False
        ).text
        
        # Parse date from Frontmatter (simplified example)
        # You should likely use a yaml parser or regex here
        # This example assumes a 'created: YYYY-MM-DD' field
        created_date = None
        for line in note_content.split('\n')[:20]:
            if line.startswith('created:'):
                try:
                    date_str = line.split(':', 1)[1].strip()
                    created_date = datetime.strptime(date_str, '%Y-%m-%d')
                    break
                except:
                    pass
        
        # Fallback: Check if filename contains date (YYYY-MM-DD)
        if not created_date:
           # logic to parse date from filename...
           pass

        # 3. Compare dates
        if created_date and start_date <= created_date <= end_date:
            matches.append(note)
            
    return matches
```

## Troubleshooting

**"Authorization required" error:**
- Verify `OBSIDIAN_REST_API_KEY` is set in Fish: `echo $OBSIDIAN_REST_API_KEY`
- Check the API key in Obsidian plugin settings matches

**SSL/Certificate errors:**
- Use `verify=False` for local development
- The plugin uses self-signed certificates

**Connection refused:**
- Ensure Obsidian is running
- Check the plugin is enabled and started
- Verify the port in plugin settings (default: 27124)
- Check if using HTTP or HTTPS (default: HTTPS)

**404 Not Found:**
- Verify the note path is correct and includes `.md` extension
- Check path is URL-encoded for special characters
- Confirm the file exists in the vault

**500 Internal Server Error:**
- Check Obsidian console for plugin errors
- Verify request payload format matches API expectations
- Review plugin logs in Obsidian settings

## API Reference

For complete API documentation including all endpoints and parameters, fetch the OpenAPI spec:

```python
# /// script
# dependencies = ["requests"]
# ///
response = requests.get(
    f"{BASE_URL}/openapi.yaml",
    headers=HEADERS,
    verify=False
)
openapi_spec = response.text
```

## Security Notes

- API key provides full access to your vault - keep it secure
- Never commit the API key to version control
- The API is bound to localhost by default (127.0.0.1)
- Use HTTPS to ensure encrypted communication even locally
- Consider setting API key permissions if the plugin supports it
