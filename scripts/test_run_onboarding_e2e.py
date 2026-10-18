"""Guard checks for the live onboarding runner, plus the opt-in live run itself.

Importing this module must not require the `claude` CLI. The live test is skipped unless
PRODUCT_OS_E2E_LIVE=1, so the default suite stays offline, fast, and free.
"""

import json
import os
import unittest
from pathlib import Path

import run_onboarding_e2e
from install_skill import ROOT

LIVE = os.environ.get("PRODUCT_OS_E2E_LIVE") == "1"
SEED = "new-web-app"


class RunnerGuardTests(unittest.TestCase):
    """These run offline. They protect the repository from a stray run writing into it."""

    def test_output_inside_the_checkout_is_refused(self):
        for candidate in (ROOT, ROOT / "demo_project" / "runs", ROOT / "scripts"):
            with self.subTest(candidate=str(candidate)):
                with self.assertRaises(ValueError):
                    run_onboarding_e2e._guard_output_dir(candidate)
        self.assertFalse((ROOT / "demo_project" / "runs").exists(),
                         "the guard must refuse without creating the directory")

    def test_output_outside_the_checkout_is_allowed(self):
        resolved = run_onboarding_e2e._guard_output_dir(Path(os.environ.get("TMPDIR", "/tmp")) / "pos-e2e-guard")
        self.assertTrue(resolved.is_absolute())

    def test_bash_is_not_offered_to_the_agent(self):
        """A hermetic run uses file tools only; a denied Bash call once derailed a trial."""
        self.assertNotIn("Bash", run_onboarding_e2e.ALLOWED_TOOLS)
        for tool in ("Read", "Glob", "Grep", "Write", "Edit"):
            self.assertIn(tool, run_onboarding_e2e.ALLOWED_TOOLS)

    def test_every_turn_carries_the_permission_flags(self):
        """Flags are not assumed to persist across --resume, so each turn must repeat them."""
        for resume in (False, True):
            command = run_onboarding_e2e._claude_command("hi", "sid", resume, None, None)
            with self.subTest(resume=resume):
                for flag in ("--permission-mode", "--permission-prompts", "--allowedTools",
                             "--strict-mcp-config", "--output-format"):
                    self.assertIn(flag, command)
                self.assertIn("--resume" if resume else "--session-id", command)
                self.assertNotIn("--session-id" if resume else "--resume", command)

    def test_fixture_turns_are_ordered_and_complete(self):
        spec = json.loads((ROOT / "demo_project" / SEED / "turns.json").read_text(encoding="utf-8"))
        self.assertTrue(spec["trigger"])
        self.assertGreaterEqual(len(spec["turns"]), 5)
        self.assertTrue(spec.get("catch_all"), "a catch-all turn is needed to close the interview")


@unittest.skipUnless(LIVE, "Set PRODUCT_OS_E2E_LIVE=1 to run the live scripted onboarding "
                           "interview (needs the claude CLI; costs tokens; takes minutes)")
class LiveOnboardingTests(unittest.TestCase):
    def test_scripted_interview_produces_a_conforming_instance(self):
        status, rundir, log = run_onboarding_e2e.run(SEED, keep=True, quiet=True)
        errors = [f for f in log["findings"] if f["severity"] == "error"]
        self.assertIsNone(log["exit_reason"], "run stalled; see {}".format(rundir))
        self.assertEqual(errors, [], "checker errors; see {}".format(rundir))
        self.assertEqual(status, 0)


if __name__ == "__main__":
    unittest.main()
