#!/usr/bin/env python3
"""Validate public KG OS model assets statically. This does not run Cypher."""

import json
import re
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
F = chr(96) * 3


def check_model(d):
    for name in ("README.md", "ontology.md", "cypher.md", "tests/seed.cypher", "tests/expected.json"):
        if not (d / name).is_file():
            raise ValueError(f"missing {name}")

    source = (d / "ontology.md").read_text(encoding="utf-8")
    pattern = re.compile(
        rf"(?ms)^### (node|relationship):([A-Za-z_][A-Za-z0-9_]*)[^\n]*\n"
        rf"(?:[ \t]*\n)*[ \t]*{F}yaml[ \t]*\n(.*?)\n{F}[ \t]*$"
    )
    blocks = list(pattern.finditer(source))
    if not blocks or len(blocks) != source.count(f"{F}yaml"):
        raise ValueError("each YAML block must immediately follow a unique Definition heading")

    models = {}
    nodes = set()
    for match in blocks:
        kind, name, body = match.groups()
        ref = f"{kind}:{name}"
        if ref in models:
            raise ValueError(f"duplicate Definition {ref}")
        model = yaml.safe_load(body)
        if not isinstance(model, dict) or model.get("name") != name:
            raise ValueError(f"{ref}: YAML name/heading mismatch")
        if not isinstance(model.get("constraints"), list):
            raise ValueError(f"{ref}: missing constraints list")
        props = model.get("properties")
        if not isinstance(props, list) or not props:
            raise ValueError(f"{ref}: KG OS requires at least one Property")
        seen_props = set()
        for prop in props:
            if not isinstance(prop, dict) or not isinstance(prop.get("name"), str):
                raise ValueError(f"{ref}: invalid Property")
            pname = prop["name"]
            if pname in seen_props or not isinstance(prop.get("type"), str) or not prop["type"]:
                raise ValueError(f"{ref}: duplicate/missing Property type for {pname}")
            seen_props.add(pname)
            for flag in ("required", "unique"):
                if flag in prop and type(prop[flag]) is not bool:
                    raise ValueError(f"{ref}.{pname}: {flag} must be Boolean")
        if kind == "node":
            nodes.add(name)
        models[ref] = model

    for ref, model in models.items():
        if ref.startswith("relationship:"):
            for endpoint in ("from", "to"):
                dest = model.get(endpoint)
                if not isinstance(dest, str) or not dest.startswith("node:") or dest[5:] not in nodes:
                    raise ValueError(f"{ref}: unresolved {endpoint} endpoint {dest}")

    cypher = (d / "cypher.md").read_text(encoding="utf-8")
    qpattern = re.compile(rf"(?ms)^## Q([0-9]+)[^\n]*\n.*?^{F}cypher[ \t]*\n(.*?)^{F}[ \t]*$")
    qblocks = list(qpattern.finditer(cypher))
    if not qblocks or len(qblocks) != cypher.count(f"{F}cypher"):
        raise ValueError("each Qn section must contain exactly one Cypher block")
    queries = {}
    for q in qblocks:
        key = "Q" + q[1]
        statement = q[2].strip()
        if key in queries or not statement.startswith("MATCH ") or "RETURN " not in statement:
            raise ValueError(f"{key}: duplicate or invalid read-only query")
        queries[key] = statement
    if sorted(int(k[1:]) for k in queries) != list(range(1, len(queries) + 1)):
        raise ValueError("query identifiers must be Q1..Qn")

    seed = (d / "tests/seed.cypher").read_text(encoding="utf-8")
    if "Synthetic" not in seed or "CREATE" not in seed:
        raise ValueError("seed must contain labeled synthetic CREATE data")
    expected = json.loads((d / "tests/expected.json").read_text(encoding="utf-8"))
    cases = expected.get("cases") if isinstance(expected, dict) else None
    if not isinstance(cases, list) or not cases:
        raise ValueError("expected.json must provide cases")
    ids = set()
    for case in cases:
        cid = case.get("id")
        query = case.get("query")
        if not isinstance(cid, str) or not cid or cid in ids or query not in queries:
            raise ValueError(f"invalid/duplicate case {cid} or unknown query {query}")
        ids.add(cid)
        params = case.get("params")
        if not isinstance(params, dict) or set(params) != set(re.findall(r"\$([A-Za-z_][A-Za-z0-9_]*)", queries[query])):
            raise ValueError(f"{cid}: params do not match query placeholders")
        columns, rows = case.get("columns"), case.get("rows")
        if (not isinstance(columns, list) or not columns or
                any(not isinstance(x, str) or not x for x in columns) or
                len(set(columns)) != len(columns) or not isinstance(rows, list)):
            raise ValueError(f"{cid}: invalid result columns/rows")
        if any(not isinstance(row, list) or len(row) != len(columns) for row in rows):
            raise ValueError(f"{cid}: row width differs from columns")
    return f"{d.name}: {len(nodes)} nodes, {len(models)-len(nodes)} relationships, {len(queries)} queries, {len(cases)} expected cases"


def main():
    root = ROOT / "models"
    packages = sorted(p for p in root.iterdir() if p.is_dir()) if root.is_dir() else []
    if not packages:
        print("FAIL: no model packages", file=sys.stderr)
        return 1
    failed = False
    for package in packages:
        try:
            print("PASS static:", check_model(package))
        except (ValueError, KeyError, yaml.YAMLError, json.JSONDecodeError) as err:
            print(f"FAIL static: {package.name}: {err}", file=sys.stderr)
            failed = True
    if not failed:
        print("Structural checks only; KG OS/Lithograph runtime NOT executed.")
    return int(failed)


if __name__ == "__main__":
    sys.exit(main())
