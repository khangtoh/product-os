#!/usr/bin/env python3
"""Build the ProductOS release archives using only the standard library.

Called by the shared release kit (see release.config.json):

    python3 scripts/package_release.py --out dist --version X.Y.Z
    python3 scripts/package_release.py --check dist --version X.Y.Z

Each archive is reproducible: sorted entries, fixed timestamps and owners.
The skill archives hold exactly what install_skill.py writes for that runtime,
so extracting one into a project's skill directory equals running the installer.
"""

import argparse
import gzip
import io
import sys
import tarfile
import tempfile
from pathlib import Path

from install_skill import ROOT, TEMPLATE, install

RUNTIME_DIRS = {"codex": ".agents", "claude": ".claude"}


def archive_names(version):
    return {
        "codex": "product-os-{}-codex-skill.tar.gz".format(version),
        "claude": "product-os-{}-claude-skill.tar.gz".format(version),
        "template": "product-os-{}-template.tar.gz".format(version),
    }


def _write_archive(path, source, prefix):
    """Tar `source` as `prefix/...` with deterministic metadata and gzip header."""
    buffer = io.BytesIO()
    with tarfile.open(fileobj=buffer, mode="w", format=tarfile.PAX_FORMAT) as tar:
        for item in [source] + sorted(source.rglob("*")):
            if item.is_symlink():
                raise ValueError("Refusing to package a symlink: {}".format(item))
            name = prefix if item == source else "{}/{}".format(prefix, item.relative_to(source).as_posix())
            info = tar.gettarinfo(str(item), arcname=name)
            info.mtime = 0
            info.uid = info.gid = 0
            info.uname = info.gname = ""
            info.mode = 0o755 if item.is_dir() else 0o644
            if item.is_dir():
                tar.addfile(info)
            else:
                with item.open("rb") as handle:
                    tar.addfile(info, handle)
    with open(path, "wb") as raw:
        with gzip.GzipFile(filename="", mode="wb", fileobj=raw, mtime=0) as gz:
            gz.write(buffer.getvalue())


def build(out, version):
    out = Path(out).resolve()
    out.mkdir(parents=True, exist_ok=True)
    names = archive_names(version)
    with tempfile.TemporaryDirectory(prefix="product-os-package-") as temp:
        project = Path(temp) / "project"
        project.mkdir()
        for destination in install(project, "both"):
            runtime = "claude" if destination.parent.parent.name == ".claude" else "codex"
            _write_archive(out / names[runtime], destination, "product-os")
    _write_archive(out / names["template"], TEMPLATE, "product")
    return [out / name for name in names.values()]


def _members(path):
    with tarfile.open(path, "r:gz") as tar:
        return {member.name: (tar.extractfile(member).read() if member.isfile() else None) for member in tar.getmembers()}


def check(out, version):
    """Confirm each archive holds a complete package for its runtime."""
    out = Path(out).resolve()
    names = archive_names(version)
    template_files = sorted(p.relative_to(TEMPLATE).as_posix() for p in TEMPLATE.rglob("*") if p.is_file())
    missing = [name for name in names.values() if not (out / name).is_file()]
    if missing:
        return ["missing archive {}".format(name) for name in missing]
    problems = []
    for runtime in ("codex", "claude"):
        members = _members(out / names[runtime])
        skill = members.get("product-os/SKILL.md")
        if skill is None:
            problems.append("{}: missing product-os/SKILL.md".format(names[runtime]))
            continue
        front = skill.decode("utf-8").split("\n---\n", 1)[0].splitlines()
        top_level_hint = any(line.startswith("argument-hint:") for line in front)
        if top_level_hint != (runtime == "claude"):
            problems.append("{}: argument-hint is in the wrong place for {}".format(names[runtime], runtime))
        for relative in template_files:
            if members.get("product-os/assets/product/" + relative) != (TEMPLATE / relative).read_bytes():
                problems.append("{}: assets/product/{} differs from the template".format(names[runtime], relative))
    members = _members(out / names["template"])
    for relative in template_files:
        if members.get("product/" + relative) != (TEMPLATE / relative).read_bytes():
            problems.append("{}: product/{} differs from the template".format(names["template"], relative))
    version_line = "Template version: {}.".format(version)
    if version_line.encode() not in (members.get("product/README.md") or b""):
        problems.append("{}: product/README.md does not record {}".format(names["template"], version_line))
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--out", help="Directory to write the archives into")
    group.add_argument("--check", metavar="DIR", help="Verify archives previously written to DIR")
    parser.add_argument("--version", required=True, help="Release version, as in VERSION")
    args = parser.parse_args()
    if args.out:
        for path in build(args.out, args.version):
            print("Wrote {}".format(path.relative_to(ROOT) if ROOT in path.parents else path))
        return 0
    problems = check(args.check, args.version)
    for problem in problems:
        print("Package check failed: {}".format(problem), file=sys.stderr)
    if not problems:
        print("All three archives hold complete packages for {}.".format(args.version))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
