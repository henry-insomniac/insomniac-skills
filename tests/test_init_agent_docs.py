from __future__ import annotations

import json
import subprocess
import shutil
import sys
import tempfile
from pathlib import Path
import unittest


REPO_ROOT = Path(__file__).resolve().parents[1]
SCRIPT = REPO_ROOT / "scripts" / "init_agent_docs.py"
NPM_WRAPPER = REPO_ROOT / "bin" / "init-agent-docs.js"


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

    def test_with_design_creates_design_guidance_entrypoint(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"

            result = self.run_init(target, "--with-design")

            self.assertEqual(result.returncode, 0, result.stderr)
            design = target / "DESIGN.md"
            self.assertTrue(design.is_file())
            design_text = design.read_text(encoding="utf-8")
            self.assertIn("version: alpha", design_text)
            self.assertIn("name:", design_text)
            self.assertIn("demo", design_text)

            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertIn("DESIGN.md", agents)

    def test_default_init_does_not_create_design_guidance(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"

            result = self.run_init(target)

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse((target / "DESIGN.md").exists())
            agents = (target / "AGENTS.md").read_text(encoding="utf-8")
            self.assertNotIn("DESIGN.md", agents)

    def test_with_design_preserves_existing_design_guidance_without_force(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"
            target.mkdir()
            design = target / "DESIGN.md"
            design.write_text("# Existing Design\n", encoding="utf-8")

            result = self.run_init(target, "--with-design")

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(design.read_text(encoding="utf-8"), "# Existing Design\n")
            self.assertIn("Skipped existing files", result.stdout)
            self.assertIn(str(design), result.stdout)

    def test_with_design_adds_design_guidance_to_long_term_context_index(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / "demo"

            result = self.run_init(target, "--with-design")

            self.assertEqual(result.returncode, 0, result.stderr)
            claude_readme = (target / ".claude" / "README.md").read_text(
                encoding="utf-8"
            )
            self.assertIn("DESIGN.md", claude_readme)

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


class InitAgentDocsNpmWrapperTests(unittest.TestCase):
    @unittest.skipUnless(shutil.which("node"), "node is required for npm wrapper tests")
    def test_node_wrapper_forwards_help_to_python_cli(self) -> None:
        result = subprocess.run(
            ["node", str(NPM_WRAPPER), "--help"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("Initialize AGENTS.md", result.stdout)
        self.assertIn("--with-design", result.stdout)

    @unittest.skipUnless(shutil.which("npm"), "npm is required for package tests")
    def test_npm_package_contains_runtime_files_only(self) -> None:
        result = subprocess.run(
            ["npm", "pack", "--dry-run", "--json"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        package = json.loads(result.stdout)[0]
        files = {item["path"] for item in package["files"]}

        self.assertIn("package.json", files)
        self.assertIn("bin/init-agent-docs.js", files)
        self.assertIn("scripts/init_agent_docs.py", files)
        self.assertIn("templates/agent-docs/AGENTS.md", files)
        self.assertIn("templates/agent-docs/DESIGN.md", files)
        self.assertIn("skills/registry.json", files)
        self.assertNotIn("tests/test_init_agent_docs.py", files)
        self.assertNotIn("server/insomniac_skills_analytics.py", files)
        self.assertNotIn("install.sh", files)
        self.assertFalse(
            any("__pycache__" in path or path.endswith(".pyc") for path in files)
        )

    @unittest.skipUnless(shutil.which("npm"), "npm is required for package tests")
    def test_npm_exec_runs_packaged_cli(self) -> None:
        result = subprocess.run(
            ["npm", "exec", "--package", ".", "--", "init-agent-docs", "--help"],
            cwd=REPO_ROOT,
            text=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--with-design", result.stdout)


if __name__ == "__main__":
    unittest.main()
