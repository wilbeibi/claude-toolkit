#!/usr/bin/env python3
"""Offline checks for load_skill.py: read commands against this checkout, link/unlink/sync in a throwaway HOME."""

import json
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPT = Path(__file__).resolve().parent / "load_skill.py"
ROOT = SCRIPT.parents[3]
SKILLS = ROOT / "skills"
fails = 0


def check(cond: bool, msg: str) -> None:
    global fails
    print(("ok   " if cond else "FAIL ") + msg)
    if not cond:
        fails += 1


def run(*args: str, home: Path | None = None, cwd: Path | None = None) -> subprocess.CompletedProcess:
    env = {**os.environ, **({"HOME": str(home)} if home else {})}
    return subprocess.run([sys.executable, str(SCRIPT), *args], capture_output=True, text=True, env=env, cwd=cwd)


def test_read() -> None:
    r = run("list")
    names = {line[2:].split()[0] for line in r.stdout.splitlines() if line.strip()}
    on_disk = {p.name for p in SKILLS.iterdir() if (p / "SKILL.md").is_file()}
    check(r.returncode == 0 and names == on_disk, f"list shows every skills/*/SKILL.md ({len(names)} of {len(on_disk)})")
    check(all(line[0] in "*+ " for line in r.stdout.splitlines()), "rows start with an install marker")
    r = run("list", "catalog")
    check(r.returncode == 0 and "load-skill" in r.stdout, "list QUERY filters by description substring")
    r = run("list", "zzz-no-such-thing")
    check(r.returncode == 1 and "no skill matches" in r.stdout, "list with no match exits 1")
    r = run("get", "load-skill")
    first = r.stdout.splitlines()[0] if r.stdout else ""
    check(r.returncode == 0 and Path(first).is_file() and first.endswith("load-skill/SKILL.md"), "get prints an existing SKILL.md path")
    check("scripts/load_skill.py" in r.stdout, "get lists the skill's other files")
    r = run("get", "zzz-no-such-thing")
    check(r.returncode == 1 and "run `list`" in r.stderr, "get of unknown skill exits 1 with a hint")


def test_links() -> None:
    with tempfile.TemporaryDirectory() as tmp:
        home = Path(tmp)
        canon = home / ".agents" / "skills"
        claude = home / ".claude" / "skills"
        (home / ".codex" / "skills").mkdir(parents=True)
        claude.mkdir(parents=True)
        (claude / "gone").symlink_to("../../.agents/skills/gone")
        canon.mkdir(parents=True)
        (canon / "foo").mkdir()
        (canon / "foo" / "SKILL.md").write_text("---\nname: foo\ndescription: x\n---\n")
        (home / ".agents" / ".skill-lock.json").write_text(json.dumps({"version": 3, "skills": {
            "show-me": {"source": "wilbeibi/wilbeibi-skills"}, "impeccable": {"source": "pbakaus/impeccable"}}}))

        r = run("link", "show-me", "grill-me", home=home)
        check(r.returncode == 0, f"link exits 0\n{r.stderr}")
        check((canon / "show-me").is_symlink() and (canon / "show-me").resolve() == SKILLS / "show-me", "global link lands in ~/.agents/skills")
        check(os.readlink(claude / "show-me") == "../../.agents/skills/show-me", "agent dir gets relative link")
        check((home / ".codex" / "skills" / "foo").is_symlink(), "pre-existing unmanaged skill propagates too")
        check(not (claude / "gone").is_symlink(), "broken agent link removed")
        r = run("link", "show-me", home=home)
        check("already linked" in r.stdout, "relink is a no-op")
        r = run("list", home=home)
        marks = {line[2:].split()[0]: line[0] for line in r.stdout.splitlines()}
        check(marks["show-me"] == "*" and marks["write-skill"] == " ", "list marks global skills with *")
        r = run("link", "zzz-no-such-thing", home=home)
        check(r.returncode == 1, "link of unknown skill fails")

        r = run("sync", home=home)
        lock = json.loads((home / ".agents" / ".skill-lock.json").read_text())
        check(set(lock["skills"]) == {"impeccable"}, "sync drops own entries from lockfile, keeps third-party")
        r = run("sync", home=home)
        check("already consistent" in r.stdout, "second sync is a no-op")

        r = run("unlink", "grill-me", home=home)
        check(not (canon / "grill-me").exists() and not (claude / "grill-me").is_symlink(), "unlink removes canonical and agent links")
        r = run("unlink", "foo", home=home)
        check(r.returncode == 1 and (canon / "foo").is_dir(), "unlink refuses a real directory")

        proj = home / "proj"
        proj.mkdir()
        r = run("link", "-p", "write-skill", home=home, cwd=proj)
        check((proj / ".agents" / "skills" / "write-skill").resolve() == SKILLS / "write-skill"
              and (proj / ".claude" / "skills" / "write-skill").is_symlink(), "project link lands in ./.agents and ./.claude")
        check(not (canon / "write-skill").exists(), "project link does not touch the global set")
        r = run("list", home=home, cwd=proj)
        marks = {line[2:].split()[0]: line[0] for line in r.stdout.splitlines()}
        check(marks["write-skill"] == "+", "list marks project skills with +")
        r = run("unlink", "-p", "write-skill", home=home, cwd=proj)
        check(not (proj / ".agents" / "skills" / "write-skill").exists(), "project unlink removes both links")


def main() -> int:
    test_read()
    test_links()
    print(f"{'PASS' if not fails else 'FAIL'}: {fails} failure(s)")
    return 1 if fails else 0


if __name__ == "__main__":
    sys.exit(main())
