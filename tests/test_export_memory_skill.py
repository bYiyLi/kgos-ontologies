"""The published domain Skill must be self-contained and independent of KG OS."""

import tempfile
import unittest
from pathlib import Path

from scripts.export_memory_skill import ROOT, render_skill


class ExportMemorySkillTests(unittest.TestCase):
    def test_export_pins_one_commit_and_all_resources(self):
        with tempfile.TemporaryDirectory() as output:
            commit, folder = render_skill("HEAD", output)
            self.assertEqual(folder.name, "kgos-memory-standards")
            self.assertEqual(
                {p.relative_to(folder).as_posix() for p in folder.rglob("*") if p.is_file()},
                {"SKILL.md", "references/ontology.md", "references/cypher.md"},
            )
            skill = (folder / "SKILL.md").read_text(encoding="utf-8")
            self.assertTrue(skill.startswith("---\nname: kgos-memory-standards\n"))
            self.assertIn(f"blob/{commit}/models/ai-memory/skills/", skill)
            for path in ("ontology.md", "cypher.md"):
                self.assertIn(f"](references/{path})", skill)
                self.assertIn(f"blob/{commit}/models/ai-memory/{path}", (folder / "references" / path).read_text())
            self.assertNotIn("../../ontology.md", skill)
            with self.assertRaises(FileExistsError):
                render_skill(commit, output)

    def test_refuses_source_repository_output_and_invalid_ref(self):
        with self.assertRaisesRegex(ValueError, "outside"):
            render_skill("HEAD", ROOT / "models/ai-memory")
        with tempfile.TemporaryDirectory() as output:
            with self.assertRaisesRegex(ValueError, "ref must"):
                render_skill("--delete", output)


if __name__ == "__main__":
    unittest.main()
