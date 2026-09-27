#!/usr/bin/env python3
"""Check relative Markdown links and heading anchors, standard library only.

    python3 scripts/check_links.py              # the repository
    python3 scripts/check_links.py --template   # an isolated copy of template/product/

The template check copies template/product/ alone into a temporary directory,
so links that only resolve inside this repository fail as they would after
adoption.

The implementation lives in check_instance.check_links, so the instance checker and this
entry point cannot disagree about what a resolving link is. It ignores fenced blocks and
inline code, where a link is an example of syntax rather than a link, and treats a link to
a directory that exists as resolving.
"""

import argparse
import shutil
import sys
import tempfile
from pathlib import Path

from check_instance import check_links

ROOT = Path(__file__).resolve().parents[1]


def broken_links(root):
    """Problem strings, in the format this script has always printed."""
    problems = []
    for finding in check_links(root):
        kind = "missing anchor" if "anchor" in finding.message else "missing target"
        target = finding.message.rsplit(": ", 1)[-1]
        problems.append("{} {}: {}".format(kind, finding.path, target))
    return problems


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--template", action="store_true", help="Check an isolated copy of template/product/")
    args = parser.parse_args(argv)
    if args.template:
        with tempfile.TemporaryDirectory(prefix="product-os-links-") as temp:
            copy = Path(temp) / "product"
            shutil.copytree(ROOT / "template" / "product", copy)
            problems = broken_links(Path(temp))
    else:
        problems = broken_links(ROOT)
    for problem in problems:
        print(problem, file=sys.stderr)
    print("{} link problem(s) in {}.".format(len(problems), "the isolated template" if args.template else "the repository"))
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
