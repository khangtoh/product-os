#!/usr/bin/env python3
"""Check relative Markdown links and heading anchors, standard library only.

    python3 scripts/check_links.py              # the repository
    python3 scripts/check_links.py --template   # an isolated copy of template/product/

The template check copies template/product/ alone into a temporary directory,
so links that only resolve inside this repository fail as they would after
adoption.
"""

import argparse
import re
import shutil
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
LINK = re.compile(r"\]\(([^)\s]+)\)")
HEADING = re.compile(r"^#+ (.+)$", re.M)


def slug(heading):
    heading = re.sub(r"[^\w\- ]", "", heading.strip().lower())
    return heading.replace(" ", "-")


def broken_links(root):
    problems = []
    for page in sorted(p for p in root.rglob("*.md") if ".git" not in p.parts):
        for target in LINK.findall(page.read_text(encoding="utf-8")):
            if re.match(r"^[a-z][a-z0-9+.-]*:", target):
                continue
            path, _, anchor = target.partition("#")
            destination = (page.parent / path).resolve() if path else page
            where = "{}: {}".format(page.relative_to(root), target)
            if not destination.exists():
                problems.append("missing target " + where)
            elif anchor and destination.suffix == ".md":
                if anchor not in {slug(h) for h in HEADING.findall(destination.read_text(encoding="utf-8"))}:
                    problems.append("missing anchor " + where)
    return problems


def main():
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--template", action="store_true", help="Check an isolated copy of template/product/")
    args = parser.parse_args()
    if args.template:
        with tempfile.TemporaryDirectory(prefix="product-os-links-") as temp:
            copy = Path(temp) / "product"
            shutil.copytree(ROOT / "template" / "product", copy)
            problems = broken_links(copy)
    else:
        problems = broken_links(ROOT)
    for problem in problems:
        print(problem, file=sys.stderr)
    print("{} link problem(s) in {}.".format(len(problems), "the isolated template" if args.template else "the repository"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
