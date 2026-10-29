"""AIMemory must remain a typed, traceable Property Graph model package."""

import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import ROOT, check_model


class MemoryModelTests(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.package = Path(tmp.name) / "ai-memory"
        shutil.copytree(ROOT / "models/ai-memory", self.package)

    def test_model_and_skill(self):
        summary = check_model(self.package)
        self.assertIn("4 nodes, 8 relationships, 1 domain", summary)
        self.assertIn("9 queries, 11 expected cases", summary)

    def test_domain_must_reference_existing_definition(self):
        path = self.package / "ontology.md"
        s = path.read_text(encoding="utf-8")
        path.write_text(s.replace('"node:MemoryCue"', '"node:Missing"', 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unresolved Definition"):
            check_model(self.package)

    def test_rejects_duplicate_domain_member(self):
        path = self.package / "ontology.md"
        s = path.read_text(encoding="utf-8")
        path.write_text(s.replace('  - "node:MemoryKind"', '  - "node:MemoryKind"\n  - "node:MemoryKind"', 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate Domain includes"):
            check_model(self.package)

    def test_nonrestricted_endpoint_must_be_explicit_null(self):
        path = self.package / "ontology.md"
        s = path.read_text(encoding="utf-8")
        path.write_text(s.replace('to: null\nproperties:', 'properties:', 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing to endpoint"):
            check_model(self.package)

    def test_skill_links_must_be_valid(self):
        path = self.package / "skills/kgos-memory-standards/SKILL.md"
        s = path.read_text(encoding="utf-8")
        path.write_text(s.replace("../../ontology.md", "../../missing.md", 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "missing resource"):
            check_model(self.package)


if __name__ == "__main__":
    unittest.main()
