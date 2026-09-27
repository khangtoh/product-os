"""Behavior checks for the optional installer, not tests of interview wording."""

import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch

from install_skill import ROOT, SKILL_SOURCE, TEMPLATE, claude_skill, install


def snapshot(directory):
    return {p.relative_to(directory): p.read_bytes() for p in directory.rglob("*") if p.is_file()}


class InstallSkillTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="product-os-install-")
        self.addCleanup(self.temp.cleanup)
        self.project = Path(self.temp.name).resolve() / "project with spaces"
        self.project.mkdir()

    def test_bundled_contract_preserves_compatibility_layers(self):
        contract = (TEMPLATE / "PRODUCT.md").read_text()
        lines = contract.splitlines()

        self.assertEqual(lines.count("# Product name"), 1)
        self.assertIn("productmd: 1", lines)
        self.assertIn("productos: 1", lines)
        self.assertIn("$type: Product", lines)
        self.assertIn("$context: https://schema.org.ai", lines)
        self.assertNotIn("register:", lines)

        required_headings = [
            "## Register",
            "## Users",
            "## Problem",
            "## Product Purpose",
            "## Brand Personality",
            "## Anti-references",
            "## Design Principles",
            "## Accessibility & Inclusion",
            "## Platform",
            "## Boundaries",
            "## Stack",
            "## Core Experience and Requirements",
            "## Desired Outcomes",
            "## Operating Principles",
            "## Human and Agent Control",
            "## Evolution Loop",
        ]
        positions = [lines.index(heading) for heading in required_headings]
        self.assertEqual(positions, sorted(positions))

    def test_installs_self_contained_skill_without_initializing_product(self):
        [destination] = install(self.project)
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
        [destination] = install(self.project)
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


    def test_source_keeps_argument_hint_under_metadata(self):
        lines = (SKILL_SOURCE / "SKILL.md").read_text().split("\n---\n", 1)[0].splitlines()
        self.assertFalse(any(line.startswith("argument-hint:") for line in lines))
        self.assertEqual(lines[lines.index("metadata:") + 1], '  argument-hint: "[init|resume|orient] [target or question]"')

    def test_claude_install_hoists_argument_hint_for_the_slash_menu(self):
        [destination] = install(self.project, "claude")
        self.assertEqual(destination, self.project / ".claude/skills/product-os")
        installed = (destination / "SKILL.md").read_text()
        source = (SKILL_SOURCE / "SKILL.md").read_text()
        frontmatter, body = installed[4:].split("\n---\n", 1)
        self.assertIn('argument-hint: "[init|resume|orient] [target or question]"', frontmatter.splitlines())
        self.assertNotIn("metadata:", frontmatter.splitlines())
        self.assertEqual(body, source[4:].split("\n---\n", 1)[1])
        self.assertEqual(snapshot(destination / "assets/product"), snapshot(TEMPLATE))
        self.assertFalse((self.project / ".agents").exists())

    def test_claude_hoist_keeps_other_metadata_and_ignores_hintless_skills(self):
        text = '---\nname: x\ndescription: d\nmetadata:\n  argument-hint: "[a]"\n  version: "1"\n---\n\nBody\n'
        self.assertEqual(claude_skill(text), '---\nname: x\ndescription: d\nargument-hint: "[a]"\nmetadata:\n  version: "1"\n---\n\nBody\n')
        plain = "---\nname: x\ndescription: d\n---\n\nBody\n"
        self.assertEqual(claude_skill(plain), plain)

    def test_both_installs_each_runtime_form(self):
        codex, claude = install(self.project, "both")
        self.assertEqual((codex / "SKILL.md").read_bytes(), (SKILL_SOURCE / "SKILL.md").read_bytes())
        self.assertEqual((claude / "SKILL.md").read_text(), claude_skill((SKILL_SOURCE / "SKILL.md").read_text()))

    def test_both_refuses_without_writing_when_either_destination_exists(self):
        existing = self.project / ".claude/skills/product-os/SKILL.md"
        existing.parent.mkdir(parents=True)
        existing.write_text("Locally customized skill")
        before = snapshot(self.project)
        with self.assertRaises(ValueError):
            install(self.project, "both")
        self.assertEqual(snapshot(self.project), before)
        self.assertFalse((self.project / ".agents").exists())

    def test_rejects_unknown_agent(self):
        with self.assertRaises(ValueError):
            install(self.project, "cursor")
        self.assertEqual(list(self.project.iterdir()), [])


if __name__ == "__main__":
    unittest.main()
