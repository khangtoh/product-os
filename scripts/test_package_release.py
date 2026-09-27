"""Checks for the release archives built by package_release.py."""

import tarfile
import tempfile
import unittest
from pathlib import Path

from install_skill import TEMPLATE
from package_release import archive_names, build, check


class PackageReleaseTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="product-os-package-")
        self.addCleanup(self.temp.cleanup)
        self.out = Path(self.temp.name) / "dist with spaces"
        self.version = (TEMPLATE / "README.md").read_text().split("Template version: ")[1].split(". ")[0]

    def test_builds_three_complete_archives(self):
        paths = build(self.out, self.version)
        self.assertEqual(sorted(p.name for p in paths), sorted(archive_names(self.version).values()))
        self.assertEqual(check(self.out, self.version), [])

    def test_archives_are_reproducible(self):
        first = {p.name: p.read_bytes() for p in build(self.out / "a", self.version)}
        second = {p.name: p.read_bytes() for p in build(self.out / "b", self.version)}
        self.assertEqual(first, second)

    def test_skill_archives_carry_each_runtime_form(self):
        build(self.out, self.version)
        names = archive_names(self.version)
        for runtime, top_level in (("codex", False), ("claude", True)):
            with tarfile.open(self.out / names[runtime]) as tar:
                skill = tar.extractfile("product-os/SKILL.md").read().decode()
                self.assertTrue(all(m.name == "product-os" or m.name.startswith("product-os/") for m in tar.getmembers()))
                self.assertTrue(all(m.mtime == 0 and m.uid == 0 for m in tar.getmembers()))
            front = skill.split("\n---\n", 1)[0].splitlines()
            self.assertEqual(any(line.startswith("argument-hint:") for line in front), top_level)

    def test_check_reports_a_wrong_version_or_damaged_archive(self):
        self.assertEqual(check(self.out, self.version), ["missing archive " + n for n in archive_names(self.version).values()])
        build(self.out, "9.9.9")
        self.assertEqual([p for p in check(self.out, "9.9.9") if "does not record" in p],
                         ["product-os-9.9.9-template.tar.gz: product/README.md does not record Template version: 9.9.9."])
        build(self.out, self.version)
        names = archive_names(self.version)
        with tarfile.open(self.out / names["codex"], "w:gz") as tar:
            tar.addfile(tarfile.TarInfo("product-os"))
        self.assertTrue(any("missing product-os/SKILL.md" in p for p in check(self.out, self.version)))


if __name__ == "__main__":
    unittest.main()
