#!/usr/bin/env python3
"""Discover, load, and link skills from wilbeibi/wilbeibi-skills without a manifest.

Which skills a host or project has is just which symlinks exist; this tool
creates, lists, and repairs them. Reads come from the local checkout when this
script runs inside one (the normal case), else from a cached GitHub tarball.
Stdlib only.

  list [QUERY]          every skill with description; * = global here, + = in this project
  get NAME              path to NAME/SKILL.md and its files; use once, install nothing
  link NAME...          make NAME global on this host (~/.agents/skills + each agent dir)
  link NAME... -p       make NAME visible in this project only (./.agents/skills, ./.claude/skills)
  unlink NAME... [-p]   undo link
  sync                  after git pull: repair agent-dir links, drop broken ones,
                        stop `npx skills update` from writing through our symlinks
"""

import argparse
import io
import json
import os
import shutil
import sys
import tarfile
import time
import urllib.error
import urllib.request
from pathlib import Path

REPO = os.environ.get("LOAD_SKILL_REPO", "wilbeibi/wilbeibi-skills")
REF = os.environ.get("LOAD_SKILL_REF", "main")
CACHE = Path(os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")) / "load-skill"
MAX_AGE = 24 * 3600
HOME = Path.home()
CANONICAL = HOME / ".agents" / "skills"
LOCK = HOME / ".agents" / ".skill-lock.json"
# user-level skill dirs that mirror CANONICAL via relative symlinks (pi's is one level deeper)
AGENT_DIRS = [HOME / ".claude" / "skills", HOME / ".codex" / "skills", HOME / ".pi" / "agent" / "skills", HOME / ".hermes" / "skills"]
PROJECT_DIRS = [Path(".agents") / "skills", Path(".claude") / "skills"]


def die(msg: str) -> None:
    print(f"load_skill: {msg}", file=sys.stderr)
    sys.exit(1)


# -- source resolution --------------------------------------------------------

def checkout_skills_dir() -> Path | None:
    here = Path(__file__).resolve()
    for parent in here.parents:
        if (parent / ".git").exists() and (parent / "skills").is_dir():
            return parent / "skills"
    return None


def fetch_skills_dir(refresh: bool) -> Path:
    dest = CACHE / REPO.replace("/", "__") / REF
    stamp = dest / ".fetched"
    if not refresh and stamp.is_file() and time.time() - stamp.stat().st_mtime < MAX_AGE:
        return dest / "skills"
    url = f"https://codeload.github.com/{REPO}/tar.gz/{REF}"
    try:
        with urllib.request.urlopen(url, timeout=30) as r:
            data = r.read()
    except (urllib.error.URLError, OSError) as e:
        if (dest / "skills").is_dir():
            print(f"load_skill: fetch failed ({e}); using cached copy", file=sys.stderr)
            return dest / "skills"
        die(f"fetch {url} failed: {e}")
    tmp = dest.with_name(dest.name + ".tmp")
    shutil.rmtree(tmp, ignore_errors=True)
    tmp.mkdir(parents=True)
    with tarfile.open(fileobj=io.BytesIO(data), mode="r:gz") as tar:
        members = []
        for m in tar.getmembers():
            parts = Path(m.name).parts
            if len(parts) > 2 and parts[1] == "skills":
                m.name = str(Path(*parts[1:]))
                members.append(m)
        tar.extractall(tmp, members=members, filter="data")
    shutil.rmtree(dest, ignore_errors=True)
    tmp.rename(dest)
    (dest / ".fetched").touch()
    return dest / "skills"


def frontmatter(skill_md: Path) -> dict[str, str]:
    out: dict[str, str] = {}
    lines = skill_md.read_text().splitlines()
    if not lines or lines[0].strip() != "---":
        return out
    key = None
    for line in lines[1:]:
        if line.strip() == "---":
            break
        if line[:1].isspace() and key:
            out[key] += " " + line.strip()
        elif ":" in line:
            key, _, val = line.partition(":")
            key = key.strip()
            out[key] = val.strip().strip('"').strip("'")
    return out


# -- link management ----------------------------------------------------------

def set_link(link: Path, target: Path, log: list[str]) -> None:
    """Point link at target, replacing a stale symlink; refuse to clobber real files."""
    if link.is_symlink():
        if Path(os.readlink(link)) == target:
            return
        link.unlink()
    elif link.exists():
        die(f"{link} exists and is not a symlink; remove it first")
    link.parent.mkdir(parents=True, exist_ok=True)
    link.symlink_to(target)
    log.append(f"{link} -> {target}")


def propagate(log: list[str]) -> None:
    """Mirror every CANONICAL entry into each existing agent dir; drop broken links."""
    for agent_dir in AGENT_DIRS:
        if not agent_dir.is_dir():
            continue
        prefix = Path(os.path.relpath(CANONICAL, agent_dir))
        for entry in sorted(CANONICAL.iterdir()):
            if not entry.name.startswith("."):
                set_link(agent_dir / entry.name, prefix / entry.name, log)
        for link in sorted(agent_dir.iterdir()):
            if link.is_symlink() and not link.exists():
                link.unlink()
                log.append(f"removed broken {link}")


def scrub_lock(log: list[str]) -> None:
    if not LOCK.is_file():
        return
    data = json.loads(LOCK.read_text())
    ours = [k for k, v in data.get("skills", {}).items() if v.get("source") == REPO]
    if ours:
        for k in ours:
            del data["skills"][k]
        LOCK.write_text(json.dumps(data, indent=2) + "\n")
        log.append(f"dropped {len(ours)} {REPO} entries from {LOCK}")


def cmd_link(skills: Path, names: list[str], project: bool) -> int:
    log: list[str] = []
    if skills.is_relative_to(CACHE):
        print(f"load_skill: linking into the tarball cache ({CACHE}); a git checkout is sturdier", file=sys.stderr)
    for name in names:
        src = skills / name
        if not (src / "SKILL.md").is_file():
            die(f"no skill {name!r} in {REPO}@{REF}; run `list`")
        if project:
            for d in PROJECT_DIRS:
                set_link(Path.cwd() / d / name, src, log)
        else:
            set_link(CANONICAL / name, src, log)
    if not project:
        propagate(log)
    print("\n".join(log) if log else "already linked")
    return 0


def cmd_unlink(names: list[str], project: bool) -> int:
    log: list[str] = []
    for name in names:
        links = [Path.cwd() / d / name for d in PROJECT_DIRS] if project else [CANONICAL / name]
        for link in links:
            if link.is_symlink():
                link.unlink()
                log.append(f"removed {link}")
            elif link.exists():
                die(f"{link} is a real directory, not a link; leaving it")
    if not project:
        propagate(log)
    print("\n".join(log) if log else "nothing to unlink")
    return 0


def cmd_sync() -> int:
    log: list[str] = []
    CANONICAL.mkdir(parents=True, exist_ok=True)
    scrub_lock(log)
    propagate(log)
    print("\n".join(log) if log else "links already consistent")
    return 0


# -- read commands ------------------------------------------------------------

def cmd_list(skills: Path, query: str | None) -> int:
    q = (query or "").lower()
    rows = []
    for d in sorted(skills.iterdir()):
        md = d / "SKILL.md"
        if not md.is_file():
            continue
        desc = frontmatter(md).get("description", "")
        if q and q not in d.name.lower() and q not in desc.lower():
            continue
        mark = "*" if (CANONICAL / d.name).exists() else "+" if any((Path.cwd() / p / d.name).exists() for p in PROJECT_DIRS) else " "
        rows.append(f"{mark} {d.name:22} {desc}")
    if not rows:
        print(f"no skill matches {query!r}; run `list` with no query to see all")
        return 1
    print("\n".join(rows))
    return 0


def cmd_get(skills: Path, name: str) -> int:
    d = skills / name
    md = d / "SKILL.md"
    if not md.is_file():
        die(f"no skill {name!r} in {REPO}@{REF}; run `list`")
    print(md)
    for p in sorted(p for p in d.rglob("*") if p.is_file() and p != md and "__pycache__" not in p.parts):
        print(f"  {p.relative_to(d)}")
    return 0


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--refresh", action="store_true", help="re-download even if the cache is fresh")
    ap.add_argument("--remote", action="store_true", help="ignore the local checkout, use GitHub")
    sub = ap.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("list"); p.add_argument("query", nargs="?")
    p = sub.add_parser("get"); p.add_argument("name")
    p = sub.add_parser("link"); p.add_argument("names", nargs="+"); p.add_argument("-p", "--project", action="store_true")
    p = sub.add_parser("unlink"); p.add_argument("names", nargs="+"); p.add_argument("-p", "--project", action="store_true")
    sub.add_parser("sync")
    args = ap.parse_args()

    if args.cmd == "sync":
        return cmd_sync()
    if args.cmd == "unlink":
        return cmd_unlink(args.names, args.project)
    skills = None if args.remote else checkout_skills_dir()
    if skills is None:
        skills = fetch_skills_dir(args.refresh)
    if args.cmd == "list":
        return cmd_list(skills, args.query)
    if args.cmd == "get":
        return cmd_get(skills, args.name)
    return cmd_link(skills, args.names, args.project)


if __name__ == "__main__":
    sys.exit(main())
