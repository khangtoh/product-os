"""Behavior checks for the optional installer, not tests of interview wording."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from install_skill import ROOT, SKILL_SOURCE, TEMPLATE, install


def snapshot(directory):
    return {p.relative_to(directory): p.read_bytes() for p in directory.rglob("*") if p.is_file()}


class InstallSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="product-os-install-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve() / "project with spaces"
        self.project.mkdir()

    def test_installs_self_contained_skill_without_initializing_product(self):
        destination = install(self.project)
        self.assertEqual(destination, self.project / ".agents/skills/product-os")
        self.assertEqual((destination / "SKILL.md").read_bytes(), (SKILL_SOURCE / "SKILL.md").read_bytes())
        self.assertEqual(snapshot(destination / "assets/product"), snapshot(TEMPLATE))
        self.assertFalse((self.project / "product").exists())
        self.assertFalse((self.project / "PRODUCT.md").exists())
        self.assertFalse((self.project / "AGENTS.md").exists())

    def test_preserves_existing_context_and_other_skills(self):
        for name in ("PRODUCT.md", "AGENTS.md", "product/STATE.md", ".agents/skills/other/SKILL.md"):
            path = self.project / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("Existing local content: " + name)
        before = snapshot(self.project)
        install(self.project)
        after = snapshot(self.project)
        self.assertTrue(all(after[path] == content for path, content in before.items()))

    def test_refuses_reinstallation_without_changes(self):
        destination = install(self.project)
        (destination / "SKILL.md").write_text("Locally customized skill")
        before = snapshot(self.project)
        with self.assertRaises(ValueError):
            install(self.project)
        self.assertEqual(snapshot(self.project), before)

    def test_rejects_missing_project_and_framework_target(self):
        with self.assertRaises(ValueError):
            install(self.project / "missing")
        self.assertFalse((self.project / "missing").exists())
        with self.assertRaises(ValueError):
            install(ROOT)

    def test_refuses_symlinked_parent_and_dangling_destination(self):
        elsewhere = Path(self.temp.name) / "elsewhere"
        elsewhere.mkdir()
        (self.project / ".agents").symlink_to(elsewhere, target_is_directory=True)
        with self.assertRaises(ValueError):
            install(self.project)
        self.assertEqual(list(elsewhere.iterdir()), [])
        (self.project / ".agents").unlink()
        parent = self.project / ".agents/skills"
        parent.mkdir(parents=True)
        destination = parent / "product-os"
        destination.symlink_to(elsewhere / "absent", target_is_directory=True)
        with self.assertRaises(ValueError):
            install(self.project)
        self.assertTrue(destination.is_symlink())

    def test_failed_copy_does_not_leave_discoverable_partial_skill(self):
        with patch("install_skill.shutil.copytree", side_effect=OSError("Simulated copy failure")):
            with self.assertRaises(OSError):
                install(self.project)
        self.assertFalse((self.project / ".agents/skills/product-os").exists())


if __name__ == "__main__":
    unittest.main()
