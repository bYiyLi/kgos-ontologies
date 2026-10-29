"""Guard the validator against accepting malformed models and expected results."""

import json
import shutil
import tempfile
import unittest
from pathlib import Path

from scripts.validate import ROOT, check_model


class ValidatorTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.package = Path(self.tmp.name) / "vlog"
        shutil.copytree(ROOT / "models/vlog", self.package)

    def test_real_package(self):
        result = check_model(self.package)
        self.assertIn("6 nodes, 7 relationships", result)

    def test_rejects_broken_relationship_endpoint(self):
        path = self.package / "ontology.md"
        contents = path.read_text(encoding="utf-8")
        self.assertIn('to: "node:Concept"', contents)
        path.write_text(contents.replace('to: "node:Concept"', 'to: "node:Missing"', 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "unresolved to endpoint"):
            check_model(self.package)

    def test_rejects_unmatched_query_params(self):
        path = self.package / "tests/expected.json"
        data = json.loads(path.read_text(encoding="utf-8"))
        data["cases"][0]["params"]["unexpected"] = "x"
        path.write_text(json.dumps(data, ensure_ascii=False), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "params do not match"):
            check_model(self.package)

    def test_rejects_duplicate_property(self):
        path = self.package / "ontology.md"
        contents = path.read_text(encoding="utf-8")
        item = '  - name: "eventKey"'
        self.assertIn(item, contents)
        path.write_text(contents.replace(item, item + '\n    type: "STRING"\n' + item, 1), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "duplicate/missing Property"):
            check_model(self.package)


if __name__ == "__main__":
    unittest.main()
