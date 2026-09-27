#!/usr/bin/env python3
"""Drive a scripted headless onboarding interview against a seed project, then check the result.

Runs outside the framework checkout, feeds the fixture's ordered user turns one per round
regardless of what the agent asked, and decides success from the files on disk rather than
from anything the agent said. Requires the `claude` CLI; nothing else in this repository does.
"""

import argparse
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import uuid
from datetime import datetime, timezone
from pathlib import Path

from check_instance import SKILL_SOURCE, TEMPLATE, check_instance, load_expect, tree_digest
from install_skill import ROOT, install

FIXTURES = ROOT / "test_project"
# File tools only. Bash is deliberately absent: with --permission-prompts none anything that
# would prompt is denied, and a denied `ls` once made a trial agent abandon inspection instead
# of using the file tools. Onboarding only needs to read and write files.
ALLOWED_TOOLS = "Read Glob Grep Write Edit TodoWrite"


def snapshot(directory, skip_dirs=(".git", ".agents", ".claude")):
    out = {}
    for path in sorted(Path(directory).rglob("*")):
        if not path.is_file():
            continue
        rel = path.relative_to(directory)
        if any(part in skip_dirs for part in rel.parts):
            continue
        out[str(rel)] = path.read_bytes()
    return out


def delta(before, after):
    return {
        "created": sorted(set(after) - set(before)),
        "modified": sorted(k for k in set(after) & set(before) if after[k] != before[k]),
        "deleted": sorted(set(before) - set(after)),
    }


def capture_golden(project, seed_dir, run_log):
    """Replace the seed's golden instance with this run's output, plus its provenance.

    The golden is never hand-edited; a fresh capture is the only sanctioned change. The
    installed skill directories are excluded: they would duplicate template/product/ in the
    repository and drift from it. Asset immutability is exercised at test time instead.
    """
    golden = seed_dir / "golden"
    if golden.exists():
        shutil.rmtree(golden)
    shutil.copytree(project, golden, ignore=shutil.ignore_patterns(".agents", ".claude", ".git"))
    provenance = {
        "captured_at": datetime.now(timezone.utc).isoformat(),
        "seed": run_log["seed"],
        "claude_cli_version": run_log.get("claude_cli_version"),
        "model": run_log.get("model") or "default",
        "session_id": run_log.get("session_id"),
        "turns": len(run_log.get("turns", [])),
        "extra_turns_used": run_log.get("extra_turns_used", 0),
        "total_cost_usd": run_log.get("total_cost_usd"),
        "template_sha256": tree_digest(TEMPLATE),
        "skill_sha256": tree_digest(SKILL_SOURCE),
        "turns_sha256": tree_digest(seed_dir / "seed"),
        "note": (
            "Captured from a real scripted run. Never hand-edit the golden; recapture with "
            "scripts/run_onboarding_e2e.py --capture-golden and record the reason in "
            "test_project/README.md."
        ),
    }
    (seed_dir / "golden_provenance.json").write_text(json.dumps(provenance, indent=2) + "\n")
    return golden, provenance


def _guard_output_dir(path):
    path = Path(path).expanduser().resolve()
    if path == ROOT or ROOT in path.parents:
        raise ValueError(
            "Refusing to run inside the framework checkout: {}. Run output belongs outside "
            "the repository; the installer refuses an in-checkout target for the same reason.".format(path)
        )
    return path


def _claude_command(prompt, session, resume, model, budget):
    command = [
        "claude", "-p",
        "--output-format", "json",
        "--permission-mode", "acceptEdits",
        "--permission-prompts", "none",
        "--strict-mcp-config",
        "--setting-sources", "project",
        "--allowedTools", ALLOWED_TOOLS,
    ]
    if resume:
        command += ["--resume", session]
    else:
        command += ["--session-id", session]
    if model:
        command += ["--model", model]
    if budget:
        command += ["--max-budget-usd", str(budget)]
    return command + [prompt]


def run_turn(project, prompt, session, resume, model, budget, timeout, transcript, index):
    started = time.time()
    try:
        completed = subprocess.run(
            _claude_command(prompt, session, resume, model, budget),
            cwd=str(project), capture_output=True, text=True, timeout=timeout,
        )
    except subprocess.TimeoutExpired:
        (transcript / "turn-{:02d}.err".format(index)).write_text("timed out after {}s".format(timeout))
        return {"index": index, "exit_reason": "timeout", "seconds": timeout}

    (transcript / "turn-{:02d}.json".format(index)).write_text(completed.stdout or "")
    if completed.stderr:
        (transcript / "turn-{:02d}.err".format(index)).write_text(completed.stderr)

    record = {"index": index, "returncode": completed.returncode, "seconds": round(time.time() - started, 1)}
    try:
        payload = json.loads(completed.stdout)
    except (ValueError, TypeError):
        record["exit_reason"] = "unparseable output"
        return record
    record.update({
        "subtype": payload.get("subtype"),
        "is_error": payload.get("is_error"),
        "num_turns": payload.get("num_turns"),
        "cost_usd": payload.get("total_cost_usd"),
        "session_id": payload.get("session_id"),
        "result_head": (payload.get("result") or "")[:400],
    })
    if completed.returncode != 0:
        record["exit_reason"] = "nonzero exit {}".format(completed.returncode)
    elif payload.get("is_error"):
        record["exit_reason"] = "agent reported an error"
    elif payload.get("subtype") not in (None, "success"):
        record["exit_reason"] = "subtype {}".format(payload.get("subtype"))
    return record


def run(seed_name, out=None, keep=False, model=None, budget=None, timeout=1500,
        extra_turns=2, check=True, quiet=False, capture=False):
    seed_dir = FIXTURES / seed_name
    if not seed_dir.is_dir():
        raise ValueError("Unknown seed: {} (looked in {})".format(seed_name, FIXTURES))
    if shutil.which("claude") is None:
        raise ValueError("The `claude` CLI is not on PATH; the live onboarding run needs it.")

    turns_spec = json.loads((seed_dir / "turns.json").read_text(encoding="utf-8"))
    expect = load_expect(seed_dir / "expect.json")

    rundir = _guard_output_dir(out) if out else Path(tempfile.mkdtemp(prefix="product-os-e2e-"))
    rundir.mkdir(parents=True, exist_ok=True)
    project = rundir / "project"
    transcript = rundir / "transcript"
    transcript.mkdir(exist_ok=True)

    def say(message):
        if not quiet:
            print(message, flush=True)

    say("run dir: {}".format(rundir))
    shutil.copytree(seed_dir / "seed", project)
    install(project, "claude")

    version = subprocess.run(["claude", "--version"], capture_output=True, text=True).stdout.strip()
    session = str(uuid.uuid4())
    prompts = [turns_spec["trigger"]] + list(turns_spec["turns"])
    catch_all = turns_spec.get("catch_all")
    if catch_all:
        prompts.append(catch_all)

    run_log = {
        "seed": seed_name,
        "started_at": datetime.now(timezone.utc).isoformat(),
        "claude_cli_version": version,
        "model": model,
        "session_id": session,
        "turns": [],
        "extra_turns_used": 0,
    }
    exit_reason, cost, before = None, 0.0, snapshot(project)

    for index, prompt in enumerate(prompts, start=1):
        say("turn {}/{}: {}...".format(index, len(prompts), prompt[:60].replace("\n", " ")))
        record = run_turn(project, prompt, session, index > 1, model, budget, timeout, transcript, index)
        after = snapshot(project)
        record["delta"] = delta(before, after)
        record["prompt_head"] = prompt[:120]
        run_log["turns"].append(record)
        cost += record.get("cost_usd") or 0.0
        if record.get("exit_reason"):
            exit_reason = record["exit_reason"]
            break
        # Two consecutive answer turns that change nothing means the interview is not saving.
        if index > 1 and not any(record["delta"].values()):
            previous = run_log["turns"][-2]["delta"]
            if not any(previous.values()):
                exit_reason = "no files changed across two consecutive turns"
                break
        before = after

    run_log["total_cost_usd"] = round(cost, 4)
    findings = []
    # Check the files even when the run stalled. A stalled run that produced nothing must not
    # be able to report "0 errors" simply because the checker never ran.
    if check:
        findings = check_instance(project, expect, seed=seed_dir / "seed")
        run_log["checker_ran"] = True
    else:
        run_log["checker_ran"] = False
    if check and exit_reason is None:
        for _ in range(extra_turns):
            if not any(f.severity == "error" for f in findings) or not catch_all:
                break
            run_log["extra_turns_used"] += 1
            index = len(run_log["turns"]) + 1
            say("checker still reporting errors; nudge {}".format(run_log["extra_turns_used"]))
            record = run_turn(project, catch_all, session, True, model, budget, timeout, transcript, index)
            after = snapshot(project)
            record["delta"] = delta(before, after)
            record["prompt_head"] = "[nudge] " + catch_all[:100]
            run_log["turns"].append(record)
            cost += record.get("cost_usd") or 0.0
            before = after
            if record.get("exit_reason"):
                exit_reason = record["exit_reason"]
                break
            findings = check_instance(project, expect, seed=seed_dir / "seed")
        run_log["total_cost_usd"] = round(cost, 4)

    run_log["exit_reason"] = exit_reason
    run_log["findings"] = [f._asdict() for f in findings]
    run_log["errors"] = sum(1 for f in findings if f.severity == "error")
    run_log["warnings"] = sum(1 for f in findings if f.severity == "warning")
    (rundir / "run.json").write_text(json.dumps(run_log, indent=2) + "\n")

    if not quiet:
        for f in sorted(findings, key=lambda f: (f.check, f.path)):
            location = "{}: ".format(f.path) if f.path else ""
            print("{:<7} {:<30} {}{}".format(f.severity, f.check, location, f.message))
        if run_log["checker_ran"]:
            print("{} errors, {} warnings, ${} over {} turns".format(
                run_log["errors"], run_log["warnings"], run_log["total_cost_usd"], len(run_log["turns"])))
        else:
            print("checker did not run; ${} over {} turns".format(
                run_log["total_cost_usd"], len(run_log["turns"])))
        if exit_reason:
            print("STALLED after {}/{} scripted turns: {}. The instance is incomplete; any check "
                  "result above describes a partial run.".format(
                      len(run_log["turns"]), len(prompts), exit_reason))
        print("run dir: {}".format(rundir))

    status = 2 if exit_reason else (1 if run_log["errors"] else 0)
    if capture:
        if status != 0:
            say("not capturing a golden from a run that did not pass")
        else:
            golden, _ = capture_golden(project, seed_dir, run_log)
            say("captured golden at {}".format(golden))
    if status == 0 and not keep:
        shutil.rmtree(rundir, ignore_errors=True)
    return status, rundir, run_log


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--seed", default="new-web-app", help="Fixture seed name (default: %(default)s)")
    parser.add_argument("--out", help="Run directory; must be outside the framework checkout")
    parser.add_argument("--keep", action="store_true", help="Keep the run directory on success")
    parser.add_argument("--model", help="Model to pass to the CLI")
    parser.add_argument("--budget-usd", dest="budget", type=float, default=5.0,
                        help="Per-turn spend cap (default: %(default)s)")
    parser.add_argument("--turn-timeout", dest="timeout", type=int, default=1500,
                        help="Seconds allowed per turn. The turn that saves most of the instance "
                             "has been observed to need over 7 minutes (default: %(default)s)")
    parser.add_argument("--extra-turns", type=int, default=2,
                        help="Catch-all nudges allowed if the checker still errors (default: %(default)s)")
    parser.add_argument("--no-check", dest="check", action="store_false", help="Skip the checker")
    parser.add_argument("--capture-golden", dest="capture", action="store_true",
                        help="On a clean run, replace the seed's golden instance and provenance")
    parser.add_argument("--quiet", action="store_true")
    args = parser.parse_args(argv)
    try:
        status, _, _ = run(
            args.seed, out=args.out, keep=args.keep, model=args.model, budget=args.budget,
            timeout=args.timeout, extra_turns=args.extra_turns, check=args.check, quiet=args.quiet,
            capture=args.capture,
        )
    except (OSError, ValueError) as error:
        print("Run failed: {}".format(error), file=sys.stderr)
        return 2
    return status


if __name__ == "__main__":
    sys.exit(main())
