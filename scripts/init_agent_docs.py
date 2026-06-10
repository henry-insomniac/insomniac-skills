#!/usr/bin/env python3
"""Initialize Agent project documentation from templates."""

from __future__ import annotations

import argparse
import datetime as dt
import os
from pathlib import Path
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE_DIR = REPO_ROOT / "templates" / "agent-docs"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Initialize AGENTS.md and .claude project documentation."
    )
    parser.add_argument(
        "--target",
        default=".",
        help="Target project directory. Defaults to current working directory.",
    )
    parser.add_argument(
        "--project-name",
        help="Project name. Defaults to target directory name.",
    )
    parser.add_argument(
        "--description",
        default="这是一个需要维护长期 Agent 上下文的项目。",
        help="Project description used in generated documents.",
    )
    parser.add_argument(
        "--template-dir",
        default=str(DEFAULT_TEMPLATE_DIR),
        help="Template directory. Defaults to this repository's agent-docs template.",
    )
    parser.add_argument(
        "--date",
        default=dt.date.today().isoformat(),
        help="Initialization date. Defaults to today.",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help="Overwrite existing generated files.",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Show files that would be written without changing the target.",
    )
    return parser.parse_args()


def render_template(text: str, values: dict[str, str]) -> str:
    rendered = text
    for key, value in values.items():
        rendered = rendered.replace("{{" + key + "}}", value)
    return rendered


def iter_template_files(template_dir: Path) -> list[Path]:
    ignored_names = {".DS_Store"}

    def should_include(path: Path) -> bool:
        if not path.is_file():
            return False
        if path.name in ignored_names or path.name.startswith("._"):
            return False
        return "__pycache__" not in path.parts

    return sorted(path for path in template_dir.rglob("*") if should_include(path))


def main() -> int:
    args = parse_args()
    template_dir = Path(args.template_dir).expanduser().resolve()
    target_dir = Path(args.target).expanduser().resolve()
    project_name = args.project_name or target_dir.name

    if not template_dir.is_dir():
        print(f"Template directory not found: {template_dir}", file=sys.stderr)
        return 2

    files = iter_template_files(template_dir)
    if not files:
        print(f"Template directory is empty: {template_dir}", file=sys.stderr)
        return 2

    values = {
        "PROJECT_NAME": project_name,
        "PROJECT_DESCRIPTION": args.description,
        "DATE": args.date,
    }

    planned: list[tuple[Path, Path, str]] = []
    existing: list[Path] = []

    for source in files:
        relative_path = source.relative_to(template_dir)
        destination = target_dir / relative_path
        if destination.exists() and not args.force:
            existing.append(destination)
            continue
        content = source.read_text(encoding="utf-8")
        planned.append((source, destination, render_template(content, values)))

    if existing:
        print("Skipped existing files. Re-run with --force to overwrite:")
        for path in existing:
            print(f"  {path}")

    if args.dry_run:
        print("Dry run. Files that would be written:")
        for _, destination, _ in planned:
            print(f"  {destination}")
        return 0

    for _, destination, content in planned:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        print(f"Wrote {destination}")

    print(
        f"Initialized Agent docs for {project_name} in {target_dir}"
        if planned
        else "No files written."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
