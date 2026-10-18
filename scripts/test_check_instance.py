"""Behavior checks for the instance checker. These prove the checker is not vacuous.

The load-bearing test builds both sides from `template/product/` at runtime, so it cannot
go stale. The mutation suite needs a captured good instance and skips until one exists.
"""

import json
import re
import shutil
import tempfile
import unittest
from pathlib import Path

from check_instance import (
    CHECKS,
    _section,
    SKILL_SOURCE,
    REQUIRED_AREAS,
    TEMPLATE,
    check_instance,
    check_links,
    load_expect,
    model_rules,
    tree_digest,
)
from install_skill import ROOT, install

FIXTURES = ROOT / "demo_project"
# The mutation suite is written against this seed's layout, so it names the seed explicitly
# rather than taking the first one discovered: adding a seed must not silently repoint it.
MUTATION_SEED = "new-web-app"
SEEDS = tuple(sorted(p.name for p in FIXTURES.iterdir() if p.is_dir() and (p / "expect.json").is_file())) \
    if FIXTURES.is_dir() else ()

# Checks with no mutation case, each for a stated reason.
NO_NEGATIVE_CASE = {
    # Reported only when the expectation file itself is malformed, which its own test covers.
    "expect_wellformed",
    # A warning-only heuristic; proven by test_stray_file_is_reported_as_a_warning instead.
    "no_unexpected_paths",
}


def _errors(findings):
    return {f.check for f in findings if f.severity == "error"}


def _fired(findings):
    """Check ids reported at any severity. Some checks are warnings by design."""
    return {f.check for f in findings}


class ModelRuleParsingTests(unittest.TestCase):
    """The checker derives its rules from MODEL.md; if that parsing breaks, checks silently weaken."""

    def test_record_types_and_states_parse_from_the_template(self):
        rules = model_rules()
        self.assertEqual(len(rules["types"]), 10, rules["types"])
        for name in ("outcome", "feature", "experiment", "cycle", "incident", "runbook"):
            self.assertIn(name, rules["types"])
            self.assertIn(name, rules["states"], "no lifecycle states parsed for " + name)
            self.assertIn(name, rules["prefixes"], "no id prefix parsed for " + name)
        self.assertEqual(rules["prefixes"]["outcome"], "Outcome")
        self.assertEqual(rules["directories"]["incident"], "operations/incidents")
        self.assertIn("achieved", rules["states"]["outcome"])
        self.assertNotIn("shipped", rules["states"]["outcome"])


class CheckRegistryTests(unittest.TestCase):
    """CHECKS drives the coverage test, so a dead or typo'd id would weaken it silently."""

    def test_checks_tuple_matches_the_ids_the_checker_emits(self):
        source = (Path(__file__).parent / "check_instance.py").read_text(encoding="utf-8")
        emitted = set(re.findall(r'(?:add|Finding)\(\s*"([a-z_]+)"', source))
        self.assertEqual(emitted - set(CHECKS), set(),
                         "the checker emits ids that are absent from CHECKS")
        self.assertEqual(set(CHECKS) - emitted, set(),
                         "CHECKS lists ids the checker never emits")

    def test_check_ids_are_unique(self):
        self.assertEqual(len(CHECKS), len(set(CHECKS)))


class CheckerArgumentTests(unittest.TestCase):
    def test_missing_instance_directory_raises_rather_than_reporting_findings(self):
        expect = load_expect(FIXTURES / MUTATION_SEED / "expect.json")
        with self.assertRaises(ValueError):
            check_instance(Path("/definitely-not-here"), expect)


class RepositoryHygieneTests(unittest.TestCase):
    def test_repository_relative_links_resolve(self):
        self.assertEqual(check_links(ROOT), [])

    def test_isolated_template_links_resolve(self):
        with tempfile.TemporaryDirectory(prefix="product-os-links-") as temp:
            copy = Path(temp) / "product"
            shutil.copytree(TEMPLATE, copy)
            self.assertEqual(check_links(Path(temp)), [])

    def test_link_check_ignores_code_but_not_prose(self):
        """Documenting link syntax must not report a broken link; a real one still must."""
        with tempfile.TemporaryDirectory(prefix="product-os-linkcode-") as temp:
            page = Path(temp) / "a.md"
            page.write_text(
                "# T\n\nreal: [x](missing.md)\n\ninline: `[y](also-missing.md)`\n\n"
                "```\n[z](nope.md)\n```\n\nanchor in code: `[a](a.md#no-such-heading)`\n",
                encoding="utf-8")
            targets = [f.message for f in check_links(Path(temp))]
            self.assertEqual(len(targets), 1, "expected only the prose link to report: {}".format(targets))
            self.assertIn("missing.md", targets[0])

    def test_template_and_skill_carry_no_fixture_leakage(self):
        for name in ("PocketGarden", "pocketgarden", "Mira"):
            for tree in (TEMPLATE, ROOT / "skills"):
                hits = [str(p.relative_to(ROOT)) for p in tree.rglob("*.md")
                        if name in p.read_text(encoding="utf-8")]
                self.assertEqual(hits, [], "fictional fixture name {!r} leaked into {}".format(name, hits))


class ExpectationSpecTests(unittest.TestCase):
    def test_seeds_are_discovered(self):
        self.assertTrue(SEEDS, "no fixture seeds with an expect.json were found")

    def test_expect_specs_are_wellformed(self):
        known = set(CHECKS)
        for seed in SEEDS:
            with self.subTest(seed=seed):
                expect = load_expect(FIXTURES / seed / "expect.json")
                self.assertEqual(expect["seed"], seed)
                for name in expect.get("skip_checks", ()):
                    self.assertIn(name, known, "skip_checks names an unknown check")
                for name in expect.get("bare_install_reports", ()):
                    self.assertIn(name, known, "bare_install_reports names an unknown check")
                self.assertFalse(
                    set(expect.get("bare_install_reports", ())) & set(expect.get("skip_checks", ())),
                    "a check cannot be both skipped and required of a bare install")
                self.assertEqual(
                    sorted(expect.get("coverage", {})), sorted(REQUIRED_AREAS),
                    "coverage must map exactly MODEL's eight required areas")
                ids = [entry.get("id") for entry in expect.get("traceability", ())]
                self.assertTrue(all(ids), "every traceability entry needs an id")
                self.assertEqual(len(ids), len(set(ids)), "traceability ids must be unique")
                for entry in expect.get("traceability", ()):
                    self.assertTrue(
                        entry.get("path") or entry.get("any_of_paths"),
                        "traceability entry {} names no path".format(entry.get("id")))
                    self.assertTrue(
                        entry.get("all_of") or entry.get("any_of"),
                        "traceability entry {} names no stems".format(entry.get("id")))

    def test_turns_match_the_example_walkthrough(self):
        """The fixture duplicates the walkthrough's turns; drift must fail loudly, not silently."""
        walkthrough = re.sub(r"\s+", " ", (ROOT / "examples" / "onboarding.md").read_text(encoding="utf-8"))
        for seed in SEEDS:
            spec_path = FIXTURES / seed / "turns.json"
            spec = json.loads(spec_path.read_text(encoding="utf-8"))
            if spec.get("source") != "examples/onboarding.md":
                continue
            for turn in spec["turns"]:
                with self.subTest(seed=seed, turn=turn[:40]):
                    self.assertIn(
                        re.sub(r"\s+", " ", turn).strip(), walkthrough,
                        "scripted turn no longer appears in examples/onboarding.md; "
                        "re-derive {}".format(spec_path.relative_to(ROOT)))


class BareInstallTests(unittest.TestCase):
    """The load-bearing test: a blank instance must fail, and both sides come from template/."""

    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix="product-os-bare-")
        self.addCleanup(self.temp.cleanup)

    def _bare_instance(self, seed):
        project = Path(self.temp.name).resolve() / "project"
        shutil.copytree(FIXTURES / seed / "seed", project)
        install(project, "claude")
        shutil.copytree(TEMPLATE, project / "product")
        return project

    def test_bare_install_fails_checker(self):
        for seed in SEEDS:
            with self.subTest(seed=seed):
                project = self._bare_instance(seed)
                expect = load_expect(FIXTURES / seed / "expect.json")
                findings = check_instance(project, expect, seed=FIXTURES / seed / "seed")
                reported = _errors(findings)
                self.assertTrue(reported, "a blank instance produced no errors")
                # Per-seed, because layouts differ: an established-contract seed keeps its local
                # contract canonical, so the pointer check does not apply there.
                expected = set(expect.get("bare_install_reports", ()))
                self.assertTrue(expected, "expect.json names no bare_install_reports")
                missing = expected - reported
                self.assertEqual(missing, set(), "blank instance did not trip: {}".format(sorted(missing)))
                shutil.rmtree(project)

    def test_stray_file_is_reported_as_a_warning(self):
        """no_unexpected_paths has no mutation row, so it is proven here instead."""
        seed = MUTATION_SEED
        project = self._bare_instance(seed)
        expect = load_expect(FIXTURES / seed / "expect.json")
        (project / "product" / "NOTES.md").write_text("scratch\n", encoding="utf-8")
        findings = check_instance(project, expect, seed=FIXTURES / seed / "seed")
        warnings = {(f.check, f.path) for f in findings if f.severity == "warning"}
        self.assertIn(("no_unexpected_paths", "product/NOTES.md"), warnings,
                      "a stray file must be reported: {}".format(sorted(warnings)))

    def test_bare_install_keeps_skill_assets_intact(self):
        seed = MUTATION_SEED
        project = self._bare_instance(seed)
        expect = load_expect(FIXTURES / seed / "expect.json")
        findings = check_instance(project, expect, seed=FIXTURES / seed / "seed")
        self.assertNotIn("skill_assets_untouched", _errors(findings),
                         "a fresh install must leave the blank assets untouched")


class GoldenProvenanceTests(unittest.TestCase):
    """A captured instance is only meaningful against the template it came from."""

    def setUp(self):
        self.provenance = FIXTURES / MUTATION_SEED / "golden_provenance.json"
        if not self.provenance.is_file():
            self.skipTest("no captured golden yet; run scripts/run_onboarding_e2e.py --capture-golden")

    def test_provenance_matches_the_current_template(self):
        recorded = json.loads(self.provenance.read_text(encoding="utf-8"))
        for key, root in (("template_sha256", TEMPLATE), ("skill_sha256", SKILL_SOURCE),
                          ("turns_sha256", FIXTURES / MUTATION_SEED / "seed")):
            with self.subTest(key=key):
                self.assertEqual(
                    recorded.get(key), tree_digest(root),
                    "the captured golden is stale for {}. Recapture with "
                    "`python3 scripts/run_onboarding_e2e.py --seed {} --capture-golden` and note "
                    "the reason in demo_project/README.md.".format(key, MUTATION_SEED))

    def test_provenance_records_how_it_was_produced(self):
        recorded = json.loads(self.provenance.read_text(encoding="utf-8"))
        for key in ("captured_at", "claude_cli_version", "model", "turns", "total_cost_usd"):
            self.assertTrue(recorded.get(key) is not None, "provenance is missing " + key)

    def test_golden_excludes_installed_skill_directories(self):
        golden = FIXTURES / MUTATION_SEED / "golden"
        for parent in (".agents", ".claude"):
            self.assertFalse((golden / parent).exists(),
                             "the golden must not duplicate the installed skill assets")


class MutationTests(unittest.TestCase):
    """Each named check must reject a specific corruption of a known-good instance."""

    seed = MUTATION_SEED

    @classmethod
    def setUpClass(cls):
        cls.golden = FIXTURES / cls.seed / "golden"
        if not cls.golden or not (cls.golden / "PRODUCT.md").is_file():
            raise unittest.SkipTest(
                "no captured golden instance yet; run scripts/run_onboarding_e2e.py and commit its output")

    def _mutated(self, mutate):
        temp = tempfile.TemporaryDirectory(prefix="product-os-mutate-")
        self.addCleanup(temp.cleanup)
        project = Path(temp.name) / "project"
        shutil.copytree(self.golden, project)
        install(project, "claude")
        mutate(project)
        expect = load_expect(FIXTURES / self.seed / "expect.json")
        return check_instance(project, expect, seed=FIXTURES / self.seed / "seed")

    def test_golden_passes_checker(self):
        findings = self._mutated(lambda project: None)
        errors = [f for f in findings if f.severity == "error"]
        self.assertEqual(errors, [], "the captured golden must pass: {}".format(
            [(f.check, f.path, f.message) for f in errors]))

    def test_mutations_are_rejected(self):
        for check, description, mutate in MUTATIONS:
            with self.subTest(check=check, mutation=description):
                self.assertIn(check, _fired(self._mutated(mutate)),
                              "{} did not report: {}".format(check, description))

    def test_every_check_has_a_negative_case(self):
        covered = {check for check, _, _ in MUTATIONS} | NO_NEGATIVE_CASE
        covered |= {"skill_assets_untouched", "relative_links_resolve"}
        missing = set(CHECKS) - covered
        self.assertEqual(missing, set(),
                         "these checks have no mutation proving they fire: {}".format(sorted(missing)))


# --------------------------------------------------------------------------- mutations


def _edit(project, rel, replace, with_, count=1):
    path = project / rel
    body = path.read_text(encoding="utf-8")
    assert replace in body, "mutation precondition missing in {}: {!r}".format(rel, replace[:60])
    path.write_text(body.replace(replace, with_, count) if count > 0
                    else body.replace(replace, with_), encoding="utf-8")


def _blank_platform(project):
    path = project / "PRODUCT.md"
    body = path.read_text(encoding="utf-8")
    path.write_text(re.sub(r"(?ms)^## Platform\n.*?(?=^## )", "## Platform\n\nunknown\n\n", body, count=1),
                    encoding="utf-8")


def _remove_platform_heading(project):
    path = project / "PRODUCT.md"
    body = path.read_text(encoding="utf-8")
    body = re.sub(r"(?ms)^## Platform\n.*?(?=^## )", "", body, count=1)
    path.write_text(body + "\n\nPlatform: web app.\n", encoding="utf-8")


def _restore_template_file(rel):
    def mutate(project):
        source = TEMPLATE / Path(rel).relative_to("product")
        shutil.copy2(source, project / rel)
    return mutate


def _restore_template_stamp(project):
    blank = (TEMPLATE / "VISION.md").read_text(encoding="utf-8")
    stamp = re.search(r"(?m)^Updated:.*$", blank).group(0)
    path = project / "product" / "VISION.md"
    body = path.read_text(encoding="utf-8")
    path.write_text(re.sub(r"(?m)^Updated:.*$", stamp, body, count=1), encoding="utf-8")


def _future_stamp(project):
    path = project / "product" / "VISION.md"
    body = path.read_text(encoding="utf-8")
    path.write_text(re.sub(r"(?m)^Updated:.*$", "Updated: 2999-01-01", body, count=1), encoding="utf-8")


def _blank_contract_section(project):
    """Revert a canonical contract section to its placeholder."""
    path = project / "PRODUCT.md"
    body = path.read_text(encoding="utf-8")
    replaced = re.sub(r"(?ms)^## Users\n.*?(?=^## )", "## Users\n\nUnknown.\n\n", body, count=1)
    assert replaced != body, "mutation precondition missing: '## Users' section"
    path.write_text(replaced, encoding="utf-8")


def _empty_now_table(project):
    path = project / "product" / "ROADMAP.md"
    body = path.read_text(encoding="utf-8")
    now = re.search(r"(?ms)^## Now\n(.*?)(?=^## )", body)
    kept = re.sub(r"(?m)^\|(?![\s-]*\|[\s-]*\|).*$\n?", "", now.group(1))
    path.write_text(body.replace(now.group(1), kept, 1), encoding="utf-8")


def _rename_now(project):
    _edit(project, "product/ROADMAP.md", "## Now", "## Current")


def _blank_state_checkpoint(project):
    blank = (TEMPLATE / "STATE.md").read_text(encoding="utf-8")
    section = re.search(r"(?ms)^## Onboarding checkpoint\n.*?(?=^## )", blank).group(0)
    path = project / "product" / "STATE.md"
    body = path.read_text(encoding="utf-8")
    current = re.search(r"(?ms)^## Onboarding checkpoint\n.*?(?=^## )", body)
    assert current, "golden STATE.md has no onboarding checkpoint section"
    path.write_text(body.replace(current.group(0), section, 1), encoding="utf-8")


def _local_contract_becomes_full(project):
    shutil.copy2(project / "PRODUCT.md", project / "product" / "PRODUCT.md")


def _drop_agents_pointer(project):
    path = project / "AGENTS.md"
    body = path.read_text(encoding="utf-8")
    path.write_text(re.sub(r"(?ms)^##+ .*[Pp]roduct context.*?(?=^#|\Z)", "", body, count=1), encoding="utf-8")


def _drop_seed_agents_line(project):
    path = project / "AGENTS.md"
    seed_lines = [l for l in (FIXTURES / MutationTests.seed / "seed" / "AGENTS.md")
                  .read_text(encoding="utf-8").splitlines() if l.strip().startswith("-")]
    _edit(project, "AGENTS.md", seed_lines[0], "")


def _modify_seed_source(project):
    (project / "src" / "search.js").write_text("// tampered\n", encoding="utf-8")


def _empty_record_dir(project):
    (project / "product" / "experiments").mkdir(parents=True, exist_ok=True)


def _stray_file(project):
    (project / "product" / "NOTES.md").write_text("scratch\n", encoding="utf-8")


def _first_record(project, record_type="outcome"):
    for path in sorted((project / "product").rglob("*.md")):
        body = path.read_text(encoding="utf-8")
        if body.startswith("---") and "type: {}".format(record_type) in body:
            return path
    return None


def _record_field(field, value, record_type="outcome"):
    def mutate(project):
        path = _first_record(project, record_type)
        assert path, "golden has no {} record to mutate".format(record_type)
        body = path.read_text(encoding="utf-8")
        body = re.sub(r"(?m)^{}:.*$".format(field), "{}: {}".format(field, value), body, count=1)
        path.write_text(body, encoding="utf-8")
    return mutate


def _duplicate_record_id(project):
    path = _first_record(project)
    assert path, "golden has no outcome record to duplicate"
    shutil.copy2(path, path.parent / (path.stem + "-copy.md"))


def _fabricate_baseline(project):
    path = _first_record(project)
    assert path, "golden has no outcome record"
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\nBaseline: 62% retrieval success (n=40)\n")


def _metrics_row(project):
    """Invent a measured metric row, inside whichever registry table the instance has."""
    path = project / "product" / "METRICS.md"
    body = path.read_text(encoding="utf-8")
    invented = ("| Metric-99 | Retrieval success | Share of sessions finding an article "
                "| analytics | 62% / 30d | 80% / 30d | owner | active |")
    separator = re.search(r"(?m)^\|(?:[\s:-]*\|)+[\s:-]*$", _section(body, "## Metric registry")) \
        if "## Metric registry" in body else None
    if separator:
        line = separator.group(0)
        path.write_text(body.replace(line, line + "\n" + invented, 1), encoding="utf-8")
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write("\n## Metric registry\n\n"
                     "| ID | Name | Definition | Source | Baseline | Target | Owner | Status |\n"
                     "| --- | --- | --- | --- | --- | --- | --- | --- |\n" + invented + "\n")


def _deferral_paths():
    """Every path the spec's deferral-stemmed entries name, so the mutation cannot miss one."""
    expect = load_expect(FIXTURES / MUTATION_SEED / "expect.json")
    paths = []
    for entry in expect.get("traceability", ()):
        stems = list(entry.get("all_of", ())) + list(entry.get("any_of", ()))
        if any("defer" in s.lower() for s in stems):
            paths.extend(entry.get("any_of_paths") or ([entry["path"]] if entry.get("path") else []))
    return sorted(set(paths))


def _strip_deferrals(project):
    for rel in _deferral_paths():
        path = project / rel
        if not path.is_file():
            continue
        body = path.read_text(encoding="utf-8")
        path.write_text(re.sub(r"(?i)defer\w*", "settled", body), encoding="utf-8")


def _break_traceability(project):
    # Every occurrence and every case, or a surviving mention keeps the check satisfied: the
    # traceability match is case-insensitive.
    path = project / "product" / "REQUIREMENTS.md"
    body = path.read_text(encoding="utf-8")
    replaced = re.sub(r"(?i)keyboard", "pointing device", body)
    assert replaced != body, "mutation precondition missing: 'keyboard' in REQUIREMENTS.md"
    path.write_text(replaced, encoding="utf-8")


def _delete_required_file(project):
    (project / "product" / "REQUIREMENTS.md").unlink()


def _forbidden_dir(project):
    (project / "product" / "features").mkdir(parents=True, exist_ok=True)
    (project / "product" / "features" / "FEAT-001-x.md").write_text(
        "---\nschema_version: 1\nid: FEAT-001\ntype: feature\ntitle: x\nstatus: proposed\n"
        "owner: unassigned\ncreated: 2026-09-27\nupdated: 2026-09-27\nrelated: []\n---\n", encoding="utf-8")


def _leak_example(project):
    shutil.copy2(ROOT / "examples" / "onboarding.md", project / "product" / "walkthrough.md")


MUTATIONS = (
    ("platform_section_standalone", "Platform body reverted to the placeholder", _blank_platform),
    ("platform_section_standalone", "Platform heading removed, text folded in elsewhere", _remove_platform_heading),
    ("contract_sections_resolved", "contract section reverted to its placeholder", _blank_contract_section),
    ("adoption_stamp_set", "Updated line reverted to the template placeholder", _restore_template_stamp),
    ("adoption_stamp_set", "Updated line set to a future date", _future_stamp),
    ("blank_markers_reduced", "VISION reverted to the blank template", _restore_template_file("product/VISION.md")),
    ("coverage_destinations_nonblank", "required destination deleted", _delete_required_file),
    ("required_paths_exist", "required file deleted", _delete_required_file),
    ("roadmap_now_has_rows", "Now table emptied of data rows", _empty_now_table),
    ("roadmap_now_has_rows", "Now heading renamed", _rename_now),
    ("state_checkpoint_resolved", "checkpoint reverted to template values", _blank_state_checkpoint),
    ("local_contract_is_pointer", "local contract replaced by the full contract", _local_contract_becomes_full),
    ("root_agents_pointer", "product-context pointer removed", _drop_agents_pointer),
    ("root_agents_pointer", "pre-existing instruction line dropped", _drop_seed_agents_line),
    ("seed_preserved", "seed source file modified", _modify_seed_source),
    ("no_empty_record_dirs", "empty record directory created", _empty_record_dir),
    ("forbidden_paths_absent", "forbidden record directory created", _forbidden_dir),
    ("front_matter_valid", "record status outside MODEL's set", _record_field("status", "shipped")),
    ("front_matter_valid", "record id blanked", _record_field("id", "")),
    ("front_matter_valid", "record created date not ISO", _record_field("created", "09/27/2026")),
    ("front_matter_valid", "schema_version bumped", _record_field("schema_version", "2")),
    ("front_matter_valid", "record id duplicated", _duplicate_record_id),
    ("no_premature_states", "outcome marked achieved", _record_field("status", "achieved")),
    ("no_fabricated_measurement", "numeric baseline invented", _fabricate_baseline),
    ("no_fabricated_measurement", "metric registry row invented", _metrics_row),
    ("deferrals_recorded", "deferrals stripped", _strip_deferrals),
    ("traceability", "supplied requirement removed", _break_traceability),
    ("no_example_leakage", "fictional example copied into product context", _leak_example),
)


if __name__ == "__main__":
    unittest.main()
