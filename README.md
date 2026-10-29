# KG OS Ontologies

**Reusable, versioned Property Graph ontology models for KG OS.**

This public repository contains optional, documented reference models for agents and people building knowledge worlds with [KG OS](https://github.com/bYiyLi/kg-releases). Models are **not built into the KG OS Kernel**, are not installed automatically, and do not change an existing Knowledge Base just because they appear here.

[简体中文](README.zh-CN.md)

## Available models

| Model | Purpose | Definition source | Queries and tests |
| --- | --- | --- | --- |
| [VLog event ontology](models/vlog/README.md) | Events, involved entities, classifications, places, time intervals, sources and verifications | [Ontology](models/vlog/ontology.md) | [Cypher examples](models/vlog/cypher.md) · [fixtures](models/vlog/tests/) |
| [AIMemory ontology](models/ai-memory/README.md) | Long-term memory types, topics, cues, sources, events and supersession | [Ontology](models/ai-memory/ontology.md) | [Cypher](models/ai-memory/cypher.md) · [tests](models/ai-memory/tests/) · [Skill](models/ai-memory/skills/kgos-memory-standards/SKILL.md) |

The collection contains **two** reusable models, not a general-purpose upper ontology or a catalogue of all KG OS domains. Additional models should be added only when they solve a demonstrated use case and can be validated.

## How to use a model

1. Read the model README and the precise version of its `ontology.md` and `cypher.md`. For reproducibility, use a Git Tag or immutable Commit URL rather than an unpinned `main` link.
2. Inspect your own KG OS Instance, Branch, pinned State, Ontology and related Knowledge. Answer the concrete questions the model should support.
3. Reuse definitions already compatible with your world. Adapt **only the needed** Node / Relationship Definitions, properties, constraints and indexes. A named Domain groups definitions; it does not isolate Knowledge or create a Branch.
4. Review identity, relationship direction, data impact, permissions and the proposed change. Obtain the authorization required to alter your Ontology, migrate Knowledge or create a Branch.
5. Use the **actual** `kgos_docs` contract to apply authorized changes, reread the resulting State and run relevant queries. The fenced YAML blocks in `ontology.md` are individual Definition bodies, **not an executable bulk patch**.

The models do not automatically establish the truth of a source, the causal meaning of an edge, or the applicability of one world's schema to another.

## Versioning and model ownership

`models/<name>/ontology.md` is the canonical definition source of that public model. Query examples and synthetic test fixtures live alongside it. If a domain has a `skills/<skill-name>/SKILL.md`, that file is the **only editable domain Skill source**. Published Tags are immutable references to the complete, matched package. The KG OS Plugin may carry **generated, pinned snapshots** of the model and Skill, but must not keep a second independently edited version.

## Validation

The standard check validates Markdown code blocks, parses the KG OS YAML Definitions, checks references and expected Cypher fixture shapes:

```sh
python3 -m pip install -r requirements-test.txt
python3 scripts/validate.py
python3 -m unittest discover -s tests -p 'test_*.py'
```

This is a **static** check, not a KG OS runtime test. The first VLog model was derived from the existing KG OS VLog Skill and its synthetic, real-Lithograph integration test fixtures; runtime compatibility should be retested for the exact source revision before claiming a new runtime-verified release. CI runs static validation on pushes and pull requests.

## Contributing and license

See [CONTRIBUTING.md](CONTRIBUTING.md) for current contribution policy. Model assets derived from KG OS retain the [AGPL-3.0-only license](LICENSE). They are reference materials; choosing a model never grants permission to access, export, or alter someone else's Knowledge.

KG OS product distribution: [bYiyLi/kg-releases](https://github.com/bYiyLi/kg-releases).
