---
name: dayflow-review
description: Query and analyze Dayflow time tracking database. Generate daily/weekly summaries, productivity insights, time analysis, and export reports to Obsidian. Use when analyzing time usage, reviewing productivity patterns, or creating timeline summaries from the Dayflow app.
---

# Dayflow Review Skill

This skill provides guidance for querying the Dayflow SQLite database to analyze time tracking data, generate reports, and create Obsidian notes.

## Database Location

```bash
~/Library/Application Support/Dayflow/chunks.sqlite
```

**Associated WAL files** (Write-Ahead Logging mode):
- `chunks.sqlite-wal` — Uncommitted transactions
- `chunks.sqlite-shm` — Temporary shared memory index

## Key Tables & Schema

### Primary Analysis Table: `timeline_cards`

The main table for activity summaries. Each row represents a time block with categorized activity.

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `id` | INTEGER | Primary key | 1234 |
| `batch_id` | INTEGER | Links to `analysis_batches` | 456 |
| `day` | DATE | Activity date | "2026-01-13" |
| `start` | TEXT | Human-readable start | "2:30 PM" |
| `end` | TEXT | Human-readable end | "3:45 PM" |
| `start_ts` | INTEGER | Unix timestamp start | 1736784600 |
| `end_ts` | INTEGER | Unix timestamp end | 1736789100 |
| `title` | TEXT | Activity heading | "System design research" |
| `summary` | TEXT | Medium description | "Researching CRDT algorithms..." |
| `detailed_summary` | TEXT | Full breakdown | "Spent 45 minutes reading..." |
| `category` | TEXT | Broad classification | "Work", "Personal", "Distraction" |
| `subcategory` | TEXT | Specific type | "Research", "Social Media", "Email" |
| `metadata` | TEXT | JSON with app info | '{"primary": "github.com"}' |
| `is_deleted` | INTEGER | Soft delete flag | 0 (active) or 1 (deleted) |

**Always filter**: `WHERE is_deleted = 0`

### Supporting Tables

**`journal_entries`** - User intentions and AI reflections
- `day` (TEXT): Date in YYYY-MM-DD format
- `intentions` (TEXT): Morning goals
- `reflections` (TEXT): Evening thoughts
- `summary` (TEXT): AI-generated daily summary

**`analysis_batches`** - Processing groups (15-min intervals)
- `batch_start_ts`, `batch_end_ts`: Unix timestamps
- `status`: "pending", "processing", or "completed"
- `detailed_transcription`: Raw narrative before card splitting

**`chunks`** - 15-second video segments
- `start_ts`, `end_ts`: Unix timestamps
- `file_url`: Path to MP4 file
- `status`: "recording", "completed", or "deleted"

**`observations`** - Granular AI descriptions
- `start_ts`, `end_ts`: Unix timestamps
- `observation`: What was on screen
- `batch_id`: Links to analysis batch

## SQL Query Patterns

### Time Calculations

```sql
-- Duration in minutes
(end_ts - start_ts) / 60.0 AS minutes

-- Duration in hours (rounded to 2 decimals)
ROUND((end_ts - start_ts) / 3600.0, 2) AS hours

-- Percentage of day
ROUND((end_ts - start_ts) * 100.0 / (
  SELECT SUM(end_ts - start_ts)
  FROM timeline_cards
  WHERE day = '2026-01-13' AND is_deleted = 0
), 1) AS percentage
```

### Date/Time Handling

```sql
-- Convert Unix timestamp to readable datetime
datetime(start_ts, 'unixepoch', 'localtime')

-- Format timestamp as hour
strftime('%H:00', datetime(start_ts, 'unixepoch', 'localtime'))

-- Today's data
WHERE day = date('now')

-- Last 7 days
WHERE day >= date('now', '-7 days')

-- Specific week (ISO 8601)
WHERE strftime('%Y-W%W', day) = '2026-W02'

-- Date range
WHERE day BETWEEN '2026-01-06' AND '2026-01-12'
```

### JSON Extraction

```sql
-- Extract primary app from metadata
json_extract(metadata, '$.primary') AS primary_app

-- Multiple JSON fields
json_extract(metadata, '$.primary') AS main_app,
json_extract(metadata, '$.secondary') AS secondary_app
```

## Common Query Examples

### Daily Summary

```sql
-- Category breakdown with time and percentages
SELECT
  category,
  COUNT(*) AS sessions,
  ROUND(SUM(end_ts - start_ts) / 3600.0, 2) AS hours,
  ROUND(SUM(end_ts - start_ts) * 100.0 / (
    SELECT SUM(end_ts - start_ts)
    FROM timeline_cards
    WHERE day = date('now') AND is_deleted = 0
  ), 1) AS percentage
FROM timeline_cards
WHERE day = date('now') AND is_deleted = 0
GROUP BY category
ORDER BY hours DESC;

-- Timeline for the day
SELECT
  start,
  end,
  title,
  category,
  subcategory,
  ROUND((end_ts - start_ts) / 60.0, 1) AS minutes,
  json_extract(metadata, '$.primary') AS primary_app
FROM timeline_cards
WHERE day = date('now') AND is_deleted = 0
ORDER BY start_ts ASC;

-- Productivity score
SELECT
  ROUND(
    SUM(CASE WHEN category IN ('Work', 'Learning') THEN end_ts - start_ts ELSE 0 END) * 100.0 /
    NULLIF(SUM(end_ts - start_ts), 0)
  , 1) AS productivity_pct,
  ROUND(SUM(end_ts - start_ts) / 3600.0, 2) AS total_hours
FROM timeline_cards
WHERE day = date('now') AND is_deleted = 0;
```

### Weekly Analysis

```sql
-- Week totals by category
SELECT
  category,
  COUNT(*) AS sessions,
  ROUND(SUM(end_ts - start_ts) / 3600.0, 2) AS hours,
  ROUND(AVG(end_ts - start_ts) / 60.0, 1) AS avg_session_min
FROM timeline_cards
WHERE day >= date('now', '-7 days') AND is_deleted = 0
GROUP BY category
ORDER BY hours DESC;

-- Daily comparison for the week
SELECT
  day,
  strftime('%w', day) AS day_of_week,
  COUNT(*) AS sessions,
  ROUND(SUM(CASE WHEN category = 'Work' THEN end_ts - start_ts ELSE 0 END) / 3600.0, 2) AS work_hours,
  ROUND(SUM(CASE WHEN category = 'Distraction' THEN end_ts - start_ts ELSE 0 END) / 60.0, 1) AS distraction_min,
  ROUND(SUM(end_ts - start_ts) / 3600.0, 2) AS total_hours
FROM timeline_cards
WHERE day >= date('now', 'weekday 0', '-7 days') -- Start of week
  AND day <= date('now', 'weekday 0', '-1 days') -- End of week
  AND is_deleted = 0
GROUP BY day
ORDER BY day;
```

### Time Analysis

```sql
-- Most time spent activities (searchable)
SELECT
  title,
  category,
  subcategory,
  COUNT(*) AS occurrences,
  ROUND(SUM(end_ts - start_ts) / 3600.0, 2) AS total_hours,
  ROUND(AVG(end_ts - start_ts) / 60.0, 1) AS avg_duration_min,
  MIN(day) AS first_seen,
  MAX(day) AS last_seen
FROM timeline_cards
WHERE day >= date('now', '-30 days')
  AND is_deleted = 0
  -- Optional: AND title LIKE '%interview%'
  -- Optional: AND category = 'Work'
GROUP BY title
ORDER BY total_hours DESC
LIMIT 50;

-- Focus sessions (uninterrupted work blocks 30+ min)
SELECT
  day,
  start,
  end,
  ROUND((end_ts - start_ts) / 60.0, 1) AS duration_min,
  title,
  json_extract(metadata, '$.primary') AS primary_app
FROM timeline_cards
WHERE category = 'Work'
  AND is_deleted = 0
  AND (end_ts - start_ts) >= 1800  -- 30+ minutes
  AND day >= date('now', '-7 days')
ORDER BY (end_ts - start_ts) DESC;

-- Hourly distribution heatmap
SELECT
  CAST(strftime('%H', datetime(start_ts, 'unixepoch', 'localtime')) AS INTEGER) AS hour,
  category,
  COUNT(*) AS blocks,
  ROUND(SUM(end_ts - start_ts) / 60.0, 1) AS minutes
FROM timeline_cards
WHERE day >= date('now', '-7 days') AND is_deleted = 0
GROUP BY hour, category
ORDER BY hour, category;
```

### Insights & Alerts

```sql
-- Days with low productivity (<50%)
SELECT
  day,
  ROUND(SUM(end_ts - start_ts) / 3600.0, 2) AS total_hours,
  ROUND(
    SUM(CASE WHEN category IN ('Work', 'Learning') THEN end_ts - start_ts ELSE 0 END) * 100.0 /
    NULLIF(SUM(end_ts - start_ts), 0)
  , 1) AS productivity_pct
FROM timeline_cards
WHERE day >= date('now', '-14 days') AND is_deleted = 0
GROUP BY day
HAVING productivity_pct < 50
ORDER BY day DESC;

-- Excessive distraction periods (2+ hours per day)
SELECT
  day,
  COUNT(*) AS distraction_blocks,
  ROUND(SUM(end_ts - start_ts) / 3600.0, 2) AS distraction_hours,
  GROUP_CONCAT(DISTINCT json_extract(metadata, '$.primary'), ', ') AS top_distractors
FROM timeline_cards
WHERE category = 'Distraction'
  AND is_deleted = 0
  AND day >= date('now', '-7 days')
GROUP BY day
HAVING distraction_hours >= 2.0
ORDER BY day DESC;

-- Timeline gaps (missing recordings)
WITH timeline_gaps AS (
  SELECT
    day,
    end_ts AS current_end,
    LEAD(start_ts) OVER (PARTITION BY day ORDER BY start_ts) AS next_start,
    (LEAD(start_ts) OVER (PARTITION BY day ORDER BY start_ts) - end_ts) / 60.0 AS gap_minutes
  FROM timeline_cards
  WHERE is_deleted = 0 AND day >= date('now', '-7 days')
)
SELECT
  day,
  COUNT(*) AS gaps,
  ROUND(SUM(gap_minutes), 1) AS total_gap_minutes
FROM timeline_gaps
WHERE gap_minutes > 15  -- Significant gaps only
GROUP BY day
ORDER BY day DESC;
```

### Database Health & Management

```sql
-- Quick health check
SELECT
  'Timeline Cards' AS table_name,
  COUNT(*) AS total_rows,
  SUM(CASE WHEN is_deleted = 1 THEN 1 ELSE 0 END) AS soft_deleted,
  MIN(day) AS earliest_date,
  MAX(day) AS latest_date
FROM timeline_cards
UNION ALL
SELECT
  'Journal Entries',
  COUNT(*),
  0,
  MIN(day),
  MAX(day)
FROM journal_entries;

-- Check for unprocessed batches
SELECT
  COUNT(*) AS pending_batches,
  datetime(MIN(batch_start_ts), 'unixepoch', 'localtime') AS oldest_pending,
  datetime(MAX(batch_end_ts), 'unixepoch', 'localtime') AS newest_pending
FROM analysis_batches
WHERE status = 'pending';

-- Failed AI processing
SELECT
  created_at,
  provider,
  model,
  operation,
  error_message
FROM llm_calls
WHERE status = 'failure'
  AND created_at > datetime('now', '-24 hours')
ORDER BY created_at DESC
LIMIT 10;
```

## Creating Obsidian Notes

### Daily Review Note Template

Location: `/Users/hongyis/Vault/Dayflow/Daily/YYYY-MM-DD.md`

```markdown
---
title: "Dayflow Review - [DATE]"
created: [TIMESTAMP]
description: "Time tracking analysis for [WEEKDAY, DATE]"
tags:
  - dayflow
  - daily-review
  - time-tracking
updated: [TIMESTAMP]
---

# Dayflow Review - [WEEKDAY, DATE]

## Summary
- **Total Tracked**: [X] hours
- **Productivity**: [X]% ([X]h work + learning)
- **Distraction**: [X]% ([X]h)
- **Top Category**: [CATEGORY] ([X]h, [X]%)

## Category Breakdown
[Table with category, hours, sessions, percentage]

## Timeline
[Chronological list of activities with times and durations]

## Key Insights
[Productivity alerts, unusual patterns, focus sessions]

## Journal
**Intentions**: [From journal_entries]
**Reflections**: [From journal_entries]
```

### Weekly Review Note Template

Location: `/Users/hongyis/Vault/Dayflow/Weekly/YYYY-Wnn.md`

```markdown
---
title: "Week [N] Review - [DATE RANGE]"
created: [TIMESTAMP]
tags:
  - dayflow
  - weekly-review
updated: [TIMESTAMP]
---

# Week [N] Review

## Weekly Summary
[Total hours, productivity percentage, top categories]

## Daily Breakdown
[Table showing each day's metrics]

## Top Activities
[Ranked list of most time-consuming activities]

## Trends & Patterns
[Productivity trends, focus patterns, distraction analysis]
```

## Database Backup

To backup the database to the vault:

```bash
# Create backup directory if needed
mkdir -p ~/Vault/Dayflow/backups

# Copy database with date stamp
cp "~/Library/Application Support/Dayflow/chunks.sqlite" \
   "~/Vault/Dayflow/backups/chunks_$(date +%Y%m%d_%H%M%S).sqlite"

# Also copy WAL file if exists
cp "~/Library/Application Support/Dayflow/chunks.sqlite-wal" \
   "~/Vault/Dayflow/backups/chunks_$(date +%Y%m%d_%H%M%S).sqlite-wal" 2>/dev/null
```

## Usage Examples

When user asks for daily summary:
1. Query `timeline_cards` for today's data grouped by category
2. Calculate productivity percentage (Work + Learning vs Total)
3. Get timeline with start/end times and titles
4. Check `journal_entries` for intentions/reflections
5. Format as markdown table or bullet list

When user asks for weekly trends:
1. Query last 7 days of `timeline_cards`
2. Group by day and category for comparison
3. Calculate daily productivity percentages
4. Identify patterns (best/worst days, consistent distractions)
5. Create summary with charts/tables

When user asks about specific activity:
1. Search `title`, `summary`, or `detailed_summary` fields
2. Aggregate total time spent, frequency, time of day patterns
3. Show first/last occurrence
4. Compare to category averages

When user wants insights:
1. Look for productivity dips (days <50% productive)
2. Find excessive distraction periods (>2h/day)
3. Detect timeline gaps (missing recordings)
4. Check for failed processing in `analysis_batches`
5. Present as alerts with recommendations

## Important Notes

1. **Always filter soft deletes**: `WHERE is_deleted = 0`
2. **Unix timestamps**: Use `datetime(ts, 'unixepoch', 'localtime')` for conversion
3. **JSON fields**: Use `json_extract(metadata, '$.key')` for parsing
4. **Time math**: Divide seconds by 60 for minutes, 3600 for hours
5. **WAL mode**: Database may have uncommitted changes in .sqlite-wal file
6. **Busy timeout**: Set 5-second timeout when connecting: `PRAGMA busy_timeout = 5000`
7. **Date formats**: Use ISO 8601 for weeks (YYYY-Wnn), YYYY-MM-DD for dates

## Common Issues & Solutions

**Database locked**: Close Dayflow app or wait for sync
**Missing data**: Check if recordings exist in `chunks` table
**Timezone issues**: Always use `'localtime'` modifier
**JSON errors**: Handle malformed metadata with try/catch
**Performance**: Create indexes on frequently queried columns

## SQL Connection Example

```python
# /// script
# dependencies = []
# ///
import sqlite3
from pathlib import Path

db_path = Path.home() / "Library" / "Application Support" / "Dayflow" / "chunks.sqlite"
conn = sqlite3.connect(str(db_path), timeout=5.0)
conn.row_factory = sqlite3.Row  # Access columns by name
cursor = conn.cursor()

# Set pragmas for safety
cursor.execute("PRAGMA busy_timeout = 5000")
cursor.execute("PRAGMA journal_mode = WAL")

# Run query
cursor.execute("""
    SELECT category, ROUND(SUM(end_ts - start_ts) / 3600.0, 2) AS hours
    FROM timeline_cards
    WHERE day = date('now') AND is_deleted = 0
    GROUP BY category
""")

for row in cursor:
    print(f"{row['category']}: {row['hours']}h")

conn.close()
```

---

This skill provides all necessary information for Claude Code to dynamically query and analyze Dayflow time tracking data based on user requests. No pre-implementation needed - construct queries on demand using these patterns and examples.
