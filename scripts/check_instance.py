#!/usr/bin/env python3
"""Check a ProductOS instance against the rules MODEL.md states, using only the standard library.

This validates the observable result of the onboarding procedure: canonical homes, required-area
coverage, record metadata and lifecycle, preserved project content, and resolving links. It does
not judge interview wording. Lifecycle and record-type rules are parsed from the canonical
template MODEL.md rather than restated here, so that file stays the single source of truth.
"""

import argparse
import collections
import hashlib
import json
import re
import sys
from datetime import date
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "template" / "product"
SKILL_SOURCE = ROOT / "skills" / "product-os"
SKILL_PARENTS = ((".agents", "skills"), (".claude", "skills"))

Finding = collections.namedtuple("Finding", "check severity path message")

CHECKS = (
    "expect_wellformed",
    "required_paths_exist",
    "forbidden_paths_absent",
    "seed_preserved",
    "no_unexpected_paths",
    "skill_assets_untouched",
    "adoption_stamp_set",
    "blank_markers_reduced",
    "product_table_filled",
    "platform_section_standalone",
    "roadmap_now_has_rows",
    "state_checkpoint_resolved",
    "local_contract_is_pointer",
    "root_agents_pointer",
    "no_empty_record_dirs",
    "front_matter_valid",
    "no_premature_states",
    "no_fabricated_measurement",
    "deferrals_recorded",
    "traceability",
    "coverage_destinations_nonblank",
    "relative_links_resolve",
    "no_example_leakage",
)

REQUIRED_AREAS = (
    "identity-and-vision",
    "users-and-problem",
    "core-experience",
    "initial-requirements",
    "boundaries",
    "success",
    "priorities",
    "starting-point",
)

# States that setup alone cannot justify. Keys are record types from MODEL's lifecycle table.
PREMATURE_STATES = {
    "outcome": ("achieved", "missed"),
    "feature": ("released", "evaluated", "retired"),
    "experiment": ("running", "analyzing", "concluded"),
    "cycle": ("completed",),
    "incident": ("resolved",),
}


# --------------------------------------------------------------------------- parsing helpers


def tree_digest(root):
    """Stable digest of a directory's relative paths and contents.

    The captured good instance is only meaningful against the template it was produced from.
    This lets a test fail loudly when the template moves on, rather than letting a stale
    capture keep passing.
    """
    digest = hashlib.sha256()
    for rel, path in _relative_files(Path(root), set()):
        digest.update(str(rel).encode("utf-8"))
        digest.update(b"\0")
        digest.update(path.read_bytes())
        digest.update(b"\0")
    return digest.hexdigest()


def _read(path):
    try:
        return path.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError):
        return ""


def _table_rows(text, heading):
    """Data rows of the first pipe table under `heading`, each a list of stripped cells."""
    rows = []
    for line in _section(text, heading).splitlines():
        line = line.strip()
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip("|").split("|")]
        if all(set(c) <= set("- :") and c for c in cells):
            continue  # separator
        rows.append(cells)
    return rows[1:] if rows else []  # drop the header row


def _section(text, heading):
    """Body text under an exact heading line, up to the next heading of the same or higher level."""
    level = len(heading) - len(heading.lstrip("#"))
    out, collecting = [], False
    for line in text.splitlines():
        if line.strip() == heading:
            collecting = True
            continue
        if collecting:
            stripped = line.lstrip("#")
            hashes = len(line) - len(stripped)
            if line.startswith("#") and 0 < hashes <= level:
                break
            out.append(line)
    return "\n".join(out)


def _headings(text):
    return [m.group(0).strip() for m in re.finditer(r"(?m)^#{1,6} +.*$", text)]


def _slug(heading):
    text = heading.lstrip("#").strip().lower()
    text = re.sub(r"[`*\[\]()]", "", text)
    text = re.sub(r"[^\w\s-]", "", text)
    return re.sub(r"\s+", "-", text).strip("-")


def model_rules(template=TEMPLATE):
    """Record types, ID prefixes, directories, and allowed states, parsed from MODEL.md."""
    text = _read(template / "MODEL.md")
    types, prefixes, directories, states = [], {}, {}, {}
    for cells in _table_rows(text, "## Record types"):
        if len(cells) < 3:
            continue
        name = cells[0].strip("`").strip().lower()
        sample = cells[1].strip("`").strip()
        directory = cells[2].strip("`").strip().rstrip("/")
        if not name:
            continue
        types.append(name)
        if "-" in sample:
            prefixes[name] = sample.split("-")[0]
        if directory:
            directories[name] = directory
    for cells in _table_rows(text, "## Lifecycle"):
        if len(cells) < 2:
            continue
        name = cells[0].strip("`").strip().lower()
        allowed = tuple(s.strip().strip("`") for s in cells[1].split(",") if s.strip())
        if name and allowed:
            states[name] = allowed
    return {"types": tuple(types), "prefixes": prefixes, "directories": directories, "states": states}


def _front_matter(text):
    if not text.startswith("---"):
        return None
    end = text.find("\n---", 3)
    if end == -1:
        return None
    fields = {}
    for line in text[3:end].splitlines():
        if ":" in line and not line.startswith((" ", "\t", "#")):
            key, _, value = line.partition(":")
            fields[key.strip()] = value.strip()
    return fields


def _blank_counterpart(rel, product_dir, template):
    """The blank template file a produced instance file was copied from, if any."""
    rel = Path(rel)
    if str(rel).startswith(product_dir + "/"):
        candidate = template / rel.relative_to(product_dir)
    else:
        candidate = template / rel.name  # a promoted root contract
    return candidate if candidate.is_file() else None


def _authored_blocks(current, blank):
    """Paragraphs present in `current` but not verbatim in the blank template.

    Content checks must never be satisfied by the template's own instructional prose. The
    blank REQUIREMENTS.md, for example, tells the reader to record a deferral's owner and
    discovery action; that sentence is guidance, not a recorded deferral.
    """
    blank_blocks = {b.strip() for b in re.split(r"\n\s*\n", blank) if b.strip()}
    return [b for b in re.split(r"\n\s*\n", current) if b.strip() and b.strip() not in blank_blocks]


def _relative_files(root, skip_dirs):
    for path in sorted(root.rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(root)
        if any(part in skip_dirs for part in rel.parts):
            continue
        yield rel, path


# --------------------------------------------------------------------------- link checking


def _without_code(text):
    """Text with fenced blocks and inline code removed.

    A link inside backticks or a fenced block is an example of link syntax, not a link. Scanning
    it produces false reports in any document that shows Markdown to the reader.
    """
    text = re.sub(r"(?ms)^ {0,3}(```+|~~~+).*?^ {0,3}\1[^\n]*$", "", text)
    text = re.sub(r"(?s)``.*?``", "", text)
    return re.sub(r"`[^`\n]*`", "", text)


def check_links(root, skip_dirs=(".git", ".agents", ".claude", "node_modules")):
    """Relative Markdown links and heading anchors that do not resolve."""
    findings = []
    link = re.compile(r"\[[^\]]*\]\(([^)\s]+)\)")
    anchors = {}

    def anchors_of(path):
        if path not in anchors:
            anchors[path] = {_slug(h) for h in _headings(_without_code(_read(path)))}
        return anchors[path]

    for rel, path in _relative_files(Path(root), set(skip_dirs)):
        if path.suffix != ".md":
            continue
        for target in link.findall(_without_code(_read(path))):
            if re.match(r"^[a-zA-Z][a-zA-Z0-9+.-]*:", target) or target.startswith("//"):
                continue
            filepart, _, fragment = target.partition("#")
            if filepart:
                dest = (path.parent / filepart).resolve()
                if not dest.exists():
                    findings.append(Finding(
                        "relative_links_resolve", "error", str(rel),
                        "link target does not exist: {}".format(target)))
                    continue
                if dest.is_dir():
                    # A directory link renders as a listing; it needs no README inside it.
                    continue
            else:
                dest = path
            if fragment and dest.suffix == ".md" and _slug(fragment) not in anchors_of(dest):
                findings.append(Finding(
                    "relative_links_resolve", "error", str(rel),
                    "heading anchor does not resolve: {}".format(target)))
    return findings


# --------------------------------------------------------------------------- the checks


def load_expect(path):
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported expect schema_version: {!r}".format(data.get("schema_version")))
    return data


def _expect_problems(expect):
    findings, known = [], set(CHECKS)
    for name in expect.get("skip_checks", ()):
        if name not in known:
            findings.append(Finding("expect_wellformed", "error", "",
                                    "skip_checks names an unknown check: {}".format(name)))
    for area in expect.get("coverage", {}):
        if area not in REQUIRED_AREAS:
            findings.append(Finding("expect_wellformed", "error", "",
                                    "coverage names an unknown required area: {}".format(area)))
    missing = [a for a in REQUIRED_AREAS if a not in expect.get("coverage", {})]
    if missing:
        findings.append(Finding("expect_wellformed", "error", "",
                                "coverage omits required areas: {}".format(", ".join(missing))))
    return findings


def check_instance(project, expect, template=TEMPLATE, seed=None, skill_source=SKILL_SOURCE):
    """Return Findings for the instance at `project`. Never raises on content.

    A missing project directory is a bad argument, not a finding: reporting it as dozens of
    absent-file errors would hide a simple typo.
    """
    project = Path(project).resolve()
    if not project.is_dir():
        raise ValueError("No such instance directory: {}".format(project))
    template = Path(template)
    rules = model_rules(template)
    skipped = set(expect.get("skip_checks", ()))
    findings = list(_expect_problems(expect))

    product_dir = expect.get("product_dir", "product")
    contract = expect.get("canonical_contract", "PRODUCT.md")

    def add(check, severity, path, message):
        if check not in skipped:
            findings.append(Finding(check, severity, path, message))

    def text_of(rel):
        return _read(project / rel)

    # --- paths -------------------------------------------------------------
    for rel in expect.get("must_exist", ()):
        if not (project / rel).is_file():
            add("required_paths_exist", "error", rel, "required file is missing")

    for rel in expect.get("must_not_exist", ()):
        if (project / rel).exists():
            add("forbidden_paths_absent", "error", rel,
                "must not exist after setup; create a record directory with its first real record")

    if seed:
        seed = Path(seed)
        for rel in expect.get("seed_preserved", ()):
            original, current = seed / rel, project / rel
            if not current.exists():
                add("seed_preserved", "error", rel, "pre-existing project file was removed")
            elif original.is_file() and original.read_bytes() != current.read_bytes():
                add("seed_preserved", "error", rel, "pre-existing project file was modified")

    # --- installed skill assets -------------------------------------------
    installed = [project.joinpath(*parents, "product-os") for parents in SKILL_PARENTS]
    installed = [p for p in installed if p.is_dir()]
    if not installed:
        add("skill_assets_untouched", "warning", "",
            "no installed skill found; asset immutability was not exercised")
    for skill in installed:
        rel_skill = skill.relative_to(project)
        expected = {rel: path.read_bytes() for rel, path in _relative_files(template, set())}
        assets = skill / "assets" / "product"
        actual = {rel: path.read_bytes() for rel, path in _relative_files(assets, set())} if assets.is_dir() else {}
        for rel in sorted(set(expected) | set(actual)):
            if rel not in actual:
                add("skill_assets_untouched", "error", str(rel_skill / "assets" / "product" / rel),
                    "blank skill asset was deleted")
            elif rel not in expected:
                add("skill_assets_untouched", "error", str(rel_skill / "assets" / "product" / rel),
                    "file was written into the installed skill assets")
            elif expected[rel] != actual[rel]:
                add("skill_assets_untouched", "error", str(rel_skill / "assets" / "product" / rel),
                    "blank skill asset was modified; save answers in project-owned files")
        entry = skill / "SKILL.md"
        source_entry = Path(skill_source) / "SKILL.md"
        if source_entry.is_file() and entry.is_file():
            source_text = source_entry.read_text(encoding="utf-8")
            # The installer rewrites the entry point for runtimes that need the argument hint at
            # the top level of the frontmatter, so accept either the source or that transform.
            accepted = {source_text}
            try:
                from install_skill import claude_skill
                accepted.add(claude_skill(source_text))
            except Exception:
                pass
            if entry.read_text(encoding="utf-8") not in accepted:
                add("skill_assets_untouched", "error", str(rel_skill / "SKILL.md"),
                    "skill entry point was modified")

    # --- filled versus blank ----------------------------------------------
    today = date.today().isoformat()
    for rel in expect.get("filled", ()):
        current = text_of(rel)
        if not current:
            continue  # absence is reported by required_paths_exist
        counterpart = _blank_counterpart(rel, product_dir, template)
        blank = _read(counterpart) if counterpart else ""

        stamp = re.search(r"(?m)^Updated:.*$", current)
        blank_stamp = re.search(r"(?m)^Updated:.*$", blank)
        if blank_stamp is not None:
            if stamp is None:
                add("adoption_stamp_set", "error", rel, "the 'Updated:' line was removed")
            elif stamp.group(0).strip() == blank_stamp.group(0).strip():
                add("adoption_stamp_set", "error", rel, "'Updated:' still holds the template placeholder")
            else:
                found = re.search(r"\d{4}-\d{2}-\d{2}", stamp.group(0))
                if found and found.group(0) > today:
                    add("adoption_stamp_set", "error", rel,
                        "'Updated:' is a future date: {}".format(found.group(0)))
        if blank:
            marker = re.compile(r"\bunknown\b", re.I)
            if len(marker.findall(current)) >= len(marker.findall(blank)):
                add("blank_markers_reduced", "error", rel,
                    "no fewer 'unknown' placeholders than the blank template; the required area looks unaddressed")

    # --- the canonical contract -------------------------------------------
    contract_text = text_of(contract)
    if contract_text:
        rows = _table_rows(contract_text, "## Purpose and identity")
        if not rows:
            add("product_table_filled", "error", contract, "no '## Purpose and identity' table found")
        for cells in rows:
            if len(cells) < 2:
                continue
            field, value = cells[0], cells[1]
            if not value or value.lower() == "unknown":
                add("product_table_filled", "error", contract,
                    "identity row still unresolved: {}".format(field))

        if "## Platform" not in _headings(contract_text):
            add("platform_section_standalone", "error", contract,
                "the standalone '## Platform' heading is missing; platform must not be folded "
                "into boundaries or constraints")
        else:
            body = _section(contract_text, "## Platform").strip()
            if not body:
                add("platform_section_standalone", "error", contract, "'## Platform' section is empty")
            elif body.lower() == "unknown":
                add("platform_section_standalone", "error", contract,
                    "'## Platform' still holds the template placeholder")

    # --- roadmap ----------------------------------------------------------
    roadmap_rel = "{}/ROADMAP.md".format(product_dir)
    roadmap = text_of(roadmap_rel)
    if roadmap:
        present = _headings(roadmap)
        for horizon in ("## Now", "## Next", "## Later"):
            if horizon not in present:
                add("roadmap_now_has_rows", "error", roadmap_rel,
                    "horizon heading is missing: {}".format(horizon))
        if "## Now" in present and not _table_rows(roadmap, "## Now"):
            add("roadmap_now_has_rows", "error", roadmap_rel,
                "'## Now' has no data rows; the current priority was not recorded")

    # --- state checkpoint --------------------------------------------------
    state_rel = "{}/STATE.md".format(product_dir)
    state = text_of(state_rel)
    blank_state = _read(template / "STATE.md")
    if state and blank_state:
        heading = "## Onboarding checkpoint"
        body = _section(state, heading)
        blank_body = _section(blank_state, heading)
        if not body.strip():
            add("state_checkpoint_resolved", "error", state_rel,
                "the '{}' section is empty".format(heading))
        for blank_bullet in re.findall(r"(?m)^- (.+)$", blank_body):
            if blank_bullet.strip() in body:
                add("state_checkpoint_resolved", "error", state_rel,
                    "checkpoint still holds its template value: {}".format(blank_bullet[:60]))
        if "No onboarding session recorded." in body:
            add("state_checkpoint_resolved", "error", state_rel,
                "checkpoint still says no onboarding session was recorded")
        if not re.search(r"\[[^\]]+\]\([^)]+\)", body):
            add("state_checkpoint_resolved", "error", state_rel,
                "checkpoint records no link to the saved answers")
        # Substance, not shape: the template offers bullets, but a table conveys the same
        # coverage and is not a defect. Require the topics MODEL asks the checkpoint to carry.
        topics = (
            ("coverage", r"(?i)coverage|required area|saved where|saved in"),
            ("completion", r"(?i)\bcomplete|\bincomplete|\bremaining\b|outstanding"),
            ("deferrals", r"(?i)defer|no deferrals"),
            ("readiness", r"(?i)readiness|\bready\b|depend|blocks|blocked"),
        )
        for name, pattern in topics:
            if not re.search(pattern, body):
                add("state_checkpoint_resolved", "error", state_rel,
                    "checkpoint does not address {}".format(name))

    # --- local contract pointer -------------------------------------------
    pointer = expect.get("pointer")
    if pointer:
        rel = pointer["path"]
        body = text_of(rel)
        if body:
            lines = [line for line in body.splitlines() if line.strip()]
            limit = pointer.get("max_lines", 25)
            if len(lines) > limit:
                add("local_contract_is_pointer", "error", rel,
                    "{} non-blank lines; a navigation pointer should stay under {}".format(len(lines), limit))
            if "## Purpose and identity" in _headings(body):
                add("local_contract_is_pointer", "error", rel,
                    "still carries the full contract table; it should point at the canonical contract")
            target = pointer.get("target", contract)
            if not re.search(r"\]\([^)]*{}\)".format(re.escape(Path(target).name)), body):
                add("local_contract_is_pointer", "error", rel,
                    "no relative link to the canonical contract {}".format(target))

    # --- root agent instructions ------------------------------------------
    agent_texts = {rel: text_of(rel) for rel in expect.get("agent_files", ()) if (project / rel).is_file()}
    if not agent_texts:
        add("root_agents_pointer", "error", "", "no root agent instructions found")
    else:
        joined = "\n".join(agent_texts.values())
        if Path(contract).name not in joined:
            add("root_agents_pointer", "error", ", ".join(sorted(agent_texts)),
                "agent instructions do not name the canonical contract {}".format(contract))
        if "STATE.md" not in joined:
            add("root_agents_pointer", "error", ", ".join(sorted(agent_texts)),
                "agent instructions do not point at the current-state record")
    if seed:
        for rel in expect.get("agent_files", ()):
            original = Path(seed) / rel
            if not original.is_file():
                continue
            current = text_of(rel)
            for line in _read(original).splitlines():
                if line.strip() and line.strip() not in current:
                    add("root_agents_pointer", "error", rel,
                        "pre-existing instruction was lost: {}".format(line.strip()[:60]))

    # --- records -----------------------------------------------------------
    records, seen_ids = [], {}
    product_root = project / product_dir
    if product_root.is_dir():
        for rel, path in _relative_files(product_root, {"templates"}):
            if path.suffix != ".md" or len(rel.parts) < 2:
                continue
            fields = _front_matter(_read(path))
            if fields is not None:
                records.append(("{}/{}".format(product_dir, rel), fields))

        for record_type, directory in rules["directories"].items():
            candidate = product_root / directory
            if not candidate.is_dir():
                continue
            has_record = any(
                _front_matter(_read(p)) is not None
                for p in candidate.glob("*.md")
            )
            if not has_record:
                add("no_empty_record_dirs", "error", "{}/{}".format(product_dir, directory),
                    "record directory holds no record; create the directory with its first real record")

    for rel, fields in records:
        record_type = fields.get("type", "")
        if fields.get("schema_version") != "1":
            add("front_matter_valid", "error", rel,
                "schema_version must be 1, found {!r}".format(fields.get("schema_version")))
        if record_type not in rules["types"]:
            add("front_matter_valid", "error", rel, "unknown record type: {!r}".format(record_type))
        record_id = fields.get("id", "")
        expected_prefix = rules["prefixes"].get(record_type)
        if not record_id:
            add("front_matter_valid", "error", rel, "record has no id")
        else:
            canonical = expected_prefix and re.match(
                r"^{}-\d{{2,3}}$".format(re.escape(expected_prefix)), record_id)
            legacy = re.match(r"^[A-Z]{2,4}-\d{3}$", record_id) or \
                re.match(r"^[A-Z]{2,4}-\d{8}-\d{2}$", record_id)
            if not canonical and not legacy:
                add("front_matter_valid", "error", rel,
                    "malformed id {!r}; MODEL specifies {}-01 form".format(
                        record_id, expected_prefix or record_type.title()))
            elif not canonical:
                add("front_matter_valid", "warning", rel,
                    "id {!r} uses the legacy abbreviated form; new records use {}-01".format(
                        record_id, expected_prefix or record_type.title()))
            if record_id in seen_ids:
                add("front_matter_valid", "error", rel,
                    "id {!r} is already used by {}".format(record_id, seen_ids[record_id]))
            else:
                seen_ids[record_id] = rel
            if not Path(rel).name.startswith(record_id):
                add("front_matter_valid", "warning", rel,
                    "filename does not start with its id {!r}".format(record_id))
        if not fields.get("title"):
            add("front_matter_valid", "error", rel, "record has no title")
        for key in ("created", "updated"):
            value = fields.get(key, "")
            if not value:
                add("front_matter_valid", "error", rel, "{} is empty".format(key))
            elif not re.match(r"^\d{4}-\d{2}-\d{2}$", value):
                add("front_matter_valid", "error", rel, "{} is not ISO YYYY-MM-DD: {!r}".format(key, value))
        status = fields.get("status", "")
        allowed = rules["states"].get(record_type)
        if allowed and status not in allowed:
            add("front_matter_valid", "error", rel,
                "status {!r} is not allowed for {}; MODEL allows {}".format(
                    status, record_type, ", ".join(allowed)))
        elif status in PREMATURE_STATES.get(record_type, ()):
            add("no_premature_states", "error", rel,
                "status {!r} cannot be justified by setup alone".format(status))

    # --- fabricated measurement -------------------------------------------
    metrics_rel = "{}/METRICS.md".format(product_dir)
    metrics = text_of(metrics_rel)
    if metrics:
        for cells in _table_rows(metrics, "## Metric registry"):
            if cells and cells[0]:
                add("no_fabricated_measurement", "warning", metrics_rel,
                    "metric registry row {!r} was added during setup; confirm it is measured, "
                    "not invented".format(cells[0]))
    for rel, fields in records:
        if fields.get("type") != "outcome":
            continue
        for line in _read(project / rel).splitlines():
            if not re.search(r"(?i)\b(baseline|current value)\b", line):
                continue
            # Strip what is legitimately numeric in prose before looking for a measurement:
            # ISO dates, record ids, and source references are not measurements.
            scrubbed = re.sub(r"\d{4}-\d{2}-\d{2}|\b[A-Z]{2,4}-\d{2,4}\b|`[^`]*`", "", line)
            if not re.search(r"\d", scrubbed):
                continue
            if re.search(r"(?i)unknown|not measured|no measurement|no baseline|none|unmeasured|"
                         r"not yet|no observation|n/?a", line):
                continue
            add("no_fabricated_measurement", "warning", rel,
                "baseline line carries a measurement: {}".format(line.strip()[:70]))

    # --- deferrals ---------------------------------------------------------
    deferral_paths = []
    for entry in expect.get("traceability", ()):
        stems = [s.lower() for s in list(entry.get("all_of", ())) + list(entry.get("any_of", ()))]
        if any("defer" in s for s in stems):
            deferral_paths.extend(entry.get("any_of_paths", []) or [entry.get("path")])
    if deferral_paths:
        found_owner = found_action = False
        for rel in [p for p in deferral_paths if p]:
            counterpart = _blank_counterpart(rel, product_dir, template)
            blank = _read(counterpart) if counterpart else ""
            for block in _authored_blocks(text_of(rel), blank):
                if not re.search(r"(?i)defer", block):
                    continue
                if re.search(r"(?i)\bowner\b|\bowns\b|\bI will\b|\bwill own\b", block):
                    found_owner = True
                if re.search(r"(?i)discovery|next action|follow[- ]?up|investigat|inspect|scope|study|measure", block):
                    found_action = True
        if not found_owner:
            add("deferrals_recorded", "error", ", ".join(p for p in deferral_paths if p),
                "a deferral is recorded without an owner")
        if not found_action:
            add("deferrals_recorded", "error", ", ".join(p for p in deferral_paths if p),
                "a deferral is recorded without a discovery action")

    # --- traceability ------------------------------------------------------
    for entry in expect.get("traceability", ()):
        paths = entry.get("any_of_paths") or ([entry["path"]] if entry.get("path") else [])
        haystacks = []
        for rel in paths:
            body = text_of(rel)
            if entry.get("section"):
                body = _section(body, entry["section"])
            haystacks.append(body.lower())
        combined = "\n".join(haystacks)
        where = " or ".join(paths) + (" under {}".format(entry["section"]) if entry.get("section") else "")
        for stem in entry.get("all_of", ()):
            if stem.lower() not in combined:
                add("traceability", "error", paths[0] if paths else "",
                    "[{}] supplied fact not found in {}: {!r}".format(entry.get("id"), where, stem))
        any_of = entry.get("any_of", ())
        if any_of and not any(stem.lower() in combined for stem in any_of):
            add("traceability", "error", paths[0] if paths else "",
                "[{}] none of {} found in {}".format(entry.get("id"), list(any_of), where))

    # --- coverage ----------------------------------------------------------
    for area, destinations in expect.get("coverage", {}).items():
        for rel in destinations:
            target = project / rel
            if target.is_dir():
                if not any(_front_matter(_read(p)) is not None for p in target.glob("*.md")):
                    add("coverage_destinations_nonblank", "error", rel,
                        "required area {!r} has no record in this directory".format(area))
            elif not target.is_file():
                add("coverage_destinations_nonblank", "error", rel,
                    "required area {!r} has no saved destination".format(area))
            elif not _read(target).strip():
                add("coverage_destinations_nonblank", "error", rel,
                    "required area {!r} destination is empty".format(area))

    # --- leakage and stray files -------------------------------------------
    allowed = set(expect.get("must_exist", ())) | set(expect.get("seed_preserved", ()))
    allowed |= set(expect.get("filled", ())) | set(expect.get("may_stay_blank", ()))
    allowed |= {str(Path(product_dir) / rel) for rel, _ in _relative_files(template, set())}
    allowed |= {rel for rel, _ in records}
    for rel, path in _relative_files(project, {".git", ".agents", ".claude", "node_modules"}):
        rel_str = str(rel)
        if rel_str in allowed:
            continue
        if seed and (Path(seed) / rel).is_file():
            continue
        add("no_unexpected_paths", "warning", rel_str, "file was not expected after setup")

    for rel, path in _relative_files(project, {".git", ".agents", ".claude", "node_modules"}):
        if path.suffix != ".md":
            continue
        body = _read(path)
        if "**Fictional example.**" in body:
            add("no_example_leakage", "error", str(rel),
                "a fictional example marker was copied into project context")
        if re.search(r"(?m)^# ProductOS development plan|^# Changelog", body):
            add("no_example_leakage", "error", str(rel),
                "framework maintenance content was copied into project context")

    findings.extend(f for f in check_links(project) if f.check not in skipped)
    return findings


# --------------------------------------------------------------------------- CLI


def _report(findings, as_json):
    if as_json:
        print(json.dumps([f._asdict() for f in findings], indent=2))
    else:
        for f in sorted(findings, key=lambda f: (f.check, f.path)):
            location = "{}: ".format(f.path) if f.path else ""
            print("{:<7} {:<30} {}{}".format(f.severity, f.check, location, f.message))
        errors = sum(1 for f in findings if f.severity == "error")
        warnings = sum(1 for f in findings if f.severity == "warning")
        print("{} error{}, {} warning{}".format(
            errors, "" if errors == 1 else "s", warnings, "" if warnings == 1 else "s"))
    return 1 if any(f.severity == "error" for f in findings) else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--project", required=True, help="Instance to check")
    parser.add_argument("--expect", help="Per-seed expectation JSON")
    parser.add_argument("--seed", help="Seed directory the project started from")
    parser.add_argument("--links-only", action="store_true", help="Only check relative links")
    parser.add_argument("--json", action="store_true", dest="as_json", help="Machine-readable output")
    args = parser.parse_args(argv)

    if not Path(args.project).is_dir():
        print("No such instance directory: {}".format(args.project), file=sys.stderr)
        return 2
    if args.links_only:
        return _report(check_links(args.project), args.as_json)
    if not args.expect:
        parser.error("--expect is required unless --links-only is given")
    try:
        expect = load_expect(args.expect)
    except (OSError, ValueError, json.JSONDecodeError) as error:
        print("Could not load expectations: {}".format(error), file=sys.stderr)
        return 2
    try:
        findings = check_instance(args.project, expect, seed=args.seed)
    except ValueError as error:
        print("Could not check the instance: {}".format(error), file=sys.stderr)
        return 2
    return _report(findings, args.as_json)


if __name__ == "__main__":
    sys.exit(main())
