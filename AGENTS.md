# Repository execution rules

This repository publishes **optional reference KG OS Property Graph ontology models**. Do not add Kernel, Agent runtimes, deployment services, private Knowledge, credentials or production data.

## Ownership

- `README.md` and `README.zh-CN.md`: public introduction, scope, safe reuse workflow.
- `models/<name>/ontology.md`: **canonical Definition YAML and model semantics** for that model.
- `models/<name>/cypher.md`: read-only competency-question queries for the matching model version.
- `models/<name>/tests/`: synthetic test fixtures and expected results, not production facts.
- `models/<name>/skills/<skill-name>/SKILL.md` (optional): the single canonical domain-specific Skill source; consumer Plugins may carry generated pinned snapshots.
- `scripts/validate.py` and `.github/workflows/validate.yml`: structural validation and its CI entrypoint.
- `CONTRIBUTING.md`: current contribution policy.

Do not maintain a second hand-edited copy of a model or domain Skill in KG OS or another repo. Consumers may carry **pinned generated snapshots** of an exact public Commit. Never silently change a shipped Tag or claim compatibility from static validation alone.

## Task discipline

Read existing model semantics, names, identities, relationships, current status and impacted fixtures before editing. For additions: justify the actual competency questions, identity, positive and negative scenarios, constraints, indexes, domain boundaries and representative queries. Avoid speculative abstractions. Models must remain opt-in and must not require a particular Branch or Domain.

Run from repository root:

```sh
python3 -m pip install -r requirements-test.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
git diff --check
```

Real KG OS/Lithograph integration tests must run in an **isolated** database with explicit model version and fixture, and must be reported separately from static checks. Inspect actual Git status/diff before any authorized commit/push. Preserve unrelated changes. Creating Tags, publishing, and changing licensing are separate actions requiring authority.
