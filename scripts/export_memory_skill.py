#!/usr/bin/env python3
"""Export the optional AIMemory Skill from a pinned Git commit, outside KG OS."""

import argparse
import re
import subprocess
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MODEL = "models/ai-memory"
SKILL = "kgos-memory-standards"


def git(*args):
    return subprocess.check_output(["git", "-C", str(ROOT), *args], text=True)


def render_skill(ref, destination):
    """Create a self-contained domain Skill; never install into the core Plugin."""
    if not re.fullmatch(r"[A-Za-z0-9][A-Za-z0-9._/-]*", ref):
        raise ValueError("ref must be an unambiguous Git commit or tag")
    commit = git("rev-parse", "--verify", f"{ref}^{{commit}}").strip()
    if not re.fullmatch(r"[0-9a-f]{40}", commit):
        raise ValueError("ref did not resolve to an immutable Git commit")

    destination = Path(destination).expanduser().resolve()
    if destination == ROOT or ROOT in destination.parents:
        raise ValueError("output must be outside the public model repository")
    skill_dir = destination / SKILL
    if skill_dir.exists():
        raise FileExistsError(f"refusing to overwrite an existing Skill: {skill_dir}")

    def source(path):
        return git("show", f"{commit}:{MODEL}/{path}")

    skill = source(f"skills/{SKILL}/SKILL.md")
    if not skill.startswith("---\n") or f"name: {SKILL}\n" not in skill:
        raise ValueError("invalid canonical Skill frontmatter")
    resources = {
        "../../ontology.md": "references/ontology.md",
        "../../cypher.md": "references/cypher.md",
    }
    for old, new in resources.items():
        if skill.count(f"]({old})") != 1:
            raise ValueError(f"missing or ambiguous canonical resource link: {old}")
        skill = skill.replace(f"]({old})", f"]({new})")
    skill += (
        f"\n<!-- GENERATED from https://github.com/bYiyLi/kgos-ontologies/"
        f"blob/{commit}/{MODEL}/skills/{SKILL}/SKILL.md ; do not edit. -->\n"
    )

    # Read everything before creating output, then atomically publish the folder.
    content = {"SKILL.md": skill}
    for path in resources.values():
        original = path.removeprefix("references/")
        body = source(original)
        content[path] = (
            f"<!-- GENERATED from https://github.com/bYiyLi/kgos-ontologies/"
            f"blob/{commit}/{MODEL}/{original} ; do not edit. -->\n\n{body}"
        )
    destination.mkdir(parents=True, exist_ok=True)
    with tempfile.TemporaryDirectory(prefix=".memory-skill-", dir=destination) as staging:
        build = Path(staging) / SKILL
        (build / "references").mkdir(parents=True)
        for path, body in content.items():
            (build / path).write_text(body, encoding="utf-8")
        build.rename(skill_dir)
    return commit, skill_dir


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ref", required=True, help="source Commit or immutable tag")
    parser.add_argument("--output", required=True, help="parent directory outside this repository")
    args = parser.parse_args()
    commit, target = render_skill(args.ref, args.output)
    print(f"Exported independently installable {SKILL} at {commit} to {target}")


if __name__ == "__main__":
    main()
