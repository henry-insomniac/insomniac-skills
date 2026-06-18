from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "init_agent_docs.py"


class InitAgentDocsCliTests(unittest.TestCase):
    def run_init(self, target: Path, *args: str) -> subprocess.CompletedProcess[str]:
        return subprocess.run(
            [
                sys.executable,
                str(SCRIPT),
                "--target",
                str(target),
                "--project-name",
                "demo",
                "--description",
                "一个测试项目",
                *args,
            ],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def test_with_agent_ops_creates_agent_operating_docs(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"

            result = self.run_init(target, "--with-agent-ops")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / "AGENTS.md").is_file())
            self.assertTrue((target / "docs" / "agents" / "README.md").is_file())
            self.assertTrue(
                (target / "docs" / "agents" / "issue-tracker.md").is_file()
            )
            self.assertTrue(
                (target / "docs" / "agents" / "triage-labels.md").is_file()
            )
            self.assertTrue((target / "docs" / "agents" / "domain.md").is_file())
            self.assertTrue((target / "docs" / "agents" / "skill-usage.md").is_file())
            self.assertTrue((target / "docs" / "adr" / "README.md").is_file())
            self.assertTrue((target / "CONTEXT.md").is_file())

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("## Agent skills", agents)
            self.assertIn("docs/agents/issue-tracker.md", agents)

    def test_issue_tracker_auto_uses_github_remote(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            subprocess.run(["git", "init"], cwd=target, check=True, stdout=subprocess.PIPE)
            subprocess.run(
                [
                    "git",
                    "remote",
                    "add",
                    "origin",
                    "git@github.com:example/demo.git",
                ],
                cwd=target,
                check=True,
            )

            result = self.run_init(
                target,
                "--with-agent-ops",
                "--issue-tracker",
                "auto",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            issue_tracker = (
                target / "docs" / "agents" / "issue-tracker.md"
            ).read_text(encoding="utf-8")
            self.assertIn("GitHub Issues", issue_tracker)
            self.assertIn("gh issue create", issue_tracker)

    def test_issue_tracker_local_creates_scratch_workspace(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"

            result = self.run_init(
                target,
                "--with-agent-ops",
                "--issue-tracker",
                "local",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertTrue((target / ".scratch" / "README.md").is_file())
            issue_tracker = (
                target / "docs" / "agents" / "issue-tracker.md"
            ).read_text(encoding="utf-8")
            self.assertIn("Local Markdown", issue_tracker)
            self.assertIn(".scratch", issue_tracker)

    def test_issue_tracker_gitlab_uses_glab_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"

            result = self.run_init(
                target,
                "--with-agent-ops",
                "--issue-tracker",
                "gitlab",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            issue_tracker = (
                target / "docs" / "agents" / "issue-tracker.md"
            ).read_text(encoding="utf-8")
            self.assertIn("GitLab Issues", issue_tracker)
            self.assertIn("glab issue create", issue_tracker)

    def test_domain_layout_claude_only_does_not_create_context_file(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"

            result = self.run_init(
                target,
                "--with-agent-ops",
                "--domain-layout",
                "claude-only",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((target / "CONTEXT.md").exists())
            domain = (target / "docs" / "agents" / "domain.md").read_text(
                encoding="utf-8"
            )
            self.assertIn(".claude/README.md", domain)
            self.assertIn("claude-only", domain)

    def test_domain_layout_multi_creates_context_map(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"

            result = self.run_init(
                target,
                "--with-agent-ops",
                "--domain-layout",
                "multi",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((target / "CONTEXT.md").exists())
            self.assertTrue((target / "CONTEXT-MAP.md").is_file())
            domain = (target / "docs" / "agents" / "domain.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("multi", domain)
            self.assertIn("CONTEXT-MAP.md", domain)


if __name__ == "__main__":
    unittest.main()
