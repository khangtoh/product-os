#!/usr/bin/env python3
"""Install the project-local ProductOS skill using only the standard library."""

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = ROOT / "skills" / "product-os"
TEMPLATE = ROOT / "template" / "product"


def install(project):
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError("The target project must be an existing directory.")
    if project == ROOT or ROOT in project.parents:
        raise ValueError("Choose a target outside the ProductOS framework checkout.")
    for required in (SKILL_SOURCE / "SKILL.md", TEMPLATE / "ONBOARDING.md", TEMPLATE / "MODEL.md"):
        if not required.is_file():
            raise ValueError("Incomplete framework checkout: missing {}".format(required))

    # Do not follow project-local skill directory symlinks into another location.
    for parent in (project / ".agents", project / ".agents" / "skills"):
        if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
            raise ValueError("Expected a real directory at {}".format(parent))
    destination = project / ".agents" / "skills" / "product-os"
    if destination.exists() or destination.is_symlink():
        raise ValueError(
            "Skill destination already exists: {}. Preserve any local edits and move "
            "that skill folder aside before reinstalling; project context is separate.".format(destination)
        )

    destination.parent.mkdir(parents=True, exist_ok=True)
    destination.mkdir()  # Exclusive creation also refuses a concurrent installation.
    try:
        # The small entrypoint is maintained once; all project templates come from
        # the canonical copy boundary. No network, activation, or project edits.
        shutil.copy2(SKILL_SOURCE / "SKILL.md", destination / "SKILL.md")
        shutil.copytree(TEMPLATE, destination / "assets" / "product")
    except BaseException:
        shutil.rmtree(destination)
        raise
    return destination


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Existing target project directory")
    args = parser.parse_args()
    try:
        destination = install(args.project)
    except (OSError, ValueError) as error:
        print("Installation failed: {}".format(error), file=sys.stderr)
        return 1
    print("Installed ProductOS skill at {}".format(destination))
    print("Open the target project in Codex and invoke $product-os init.")
    print("If the skill is not listed, start a new session. Product context has not been created yet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
