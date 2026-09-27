#!/usr/bin/env python3
"""Install the project-local ProductOS skill using only the standard library."""

import argparse
import shutil
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SKILL_SOURCE = ROOT / "skills" / "product-os"
TEMPLATE = ROOT / "template" / "product"


# Where each agent runtime discovers a project-local skill.
RUNTIMES = {"codex": ".agents", "claude": ".claude"}
AGENTS = ("codex", "claude", "both")


def claude_skill(text):
    """Hoist the argument hint for Claude Code, which shows it inline after `/product-os `.

    The source keeps `argument-hint` under `metadata:` because the Agent Skills
    spec, which Codex follows, has no top-level key for it.
    """
    head, marker, body = text[4:].partition("\n---\n")
    if not text.startswith("---\n") or not marker:
        return text
    lines = head.split("\n")
    hints = [line for line in lines if line.startswith("  argument-hint:")]
    if not hints:
        return text
    lines.remove(hints[0])
    metadata = lines.index("metadata:") if "metadata:" in lines else -1
    if metadata >= 0 and not (metadata + 1 < len(lines) and lines[metadata + 1].startswith("  ")):
        del lines[metadata]
    lines.insert(next(i for i, line in enumerate(lines) if line.startswith("description:")) + 1, hints[0].strip())
    return "---\n" + "\n".join(lines) + marker + body


def install(project, agent="codex"):
    if agent not in AGENTS:
        raise ValueError("Unknown agent {!r}; expected one of: {}.".format(agent, ", ".join(AGENTS)))
    project = Path(project).expanduser().resolve()
    if not project.is_dir():
        raise ValueError("The target project must be an existing directory.")
    if project == ROOT or ROOT in project.parents:
        raise ValueError("Choose a target outside the ProductOS framework checkout.")
    for required in (
        SKILL_SOURCE / "SKILL.md",
        TEMPLATE / "ONBOARDING.md",
        TEMPLATE / "EXECUTION.md",
        TEMPLATE / "MODEL.md",
        TEMPLATE / "LOOP.md",
    ):
        if not required.is_file():
            raise ValueError("Incomplete framework checkout: missing {}".format(required))

    runtimes = list(RUNTIMES) if agent == "both" else [agent]
    destinations = []
    # Check every destination before writing any, so a refusal changes nothing.
    for runtime in runtimes:
        # Do not follow project-local skill directory symlinks into another location.
        root = project / RUNTIMES[runtime]
        for parent in (root, root / "skills"):
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                raise ValueError("Expected a real directory at {}".format(parent))
        destination = root / "skills" / "product-os"
        if destination.exists() or destination.is_symlink():
            raise ValueError(
                "Skill destination already exists: {}. Preserve any local edits and move "
                "that skill folder aside before reinstalling; project context is separate.".format(destination)
            )
        destinations.append((runtime, destination))

    created = []
    try:
        for runtime, destination in destinations:
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.mkdir()  # Exclusive creation also refuses a concurrent installation.
            created.append(destination)
            # The small entrypoint is maintained once; all project templates come from
            # the canonical copy boundary. No network, activation, or project edits.
            if runtime == "claude":
                text = (SKILL_SOURCE / "SKILL.md").read_text(encoding="utf-8")
                (destination / "SKILL.md").write_text(claude_skill(text), encoding="utf-8")
            else:
                shutil.copy2(SKILL_SOURCE / "SKILL.md", destination / "SKILL.md")
            shutil.copytree(TEMPLATE, destination / "assets" / "product")
    except BaseException:
        for destination in created:
            shutil.rmtree(destination)
        raise
    return [destination for _, destination in destinations]


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, help="Existing target project directory")
    parser.add_argument(
        "--agent", choices=AGENTS, default="codex",
        help="Runtime to install for: codex (.agents/skills, default), claude (.claude/skills), or both",
    )
    args = parser.parse_args()
    try:
        destinations = install(args.project, args.agent)
    except (OSError, ValueError) as error:
        print("Installation failed: {}".format(error), file=sys.stderr)
        return 1
    for destination in destinations:
        print("Installed ProductOS skill at {}".format(destination))
    if args.agent != "claude":
        print("Open the target project in Codex and invoke $product-os init.")
    if args.agent != "codex":
        print("Open the target project in Claude Code and invoke /product-os init.")
    print("If the skill is not listed, start a new session. Product context has not been created yet.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
