#!/usr/bin/env python3
"""Initialize Agent project documentation from templates."""

from __future__ import annotations

import argparse
import datetime as dt
import json
from pathlib import Path
import shutil
import sys


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_TEMPLATE_DIR = REPO_ROOT / "templates" / "agent-docs"
DEFAULT_SKILLS_DIR = REPO_ROOT / "skills"


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
        "--skills-dir",
        default=str(DEFAULT_SKILLS_DIR),
        help="Skills directory. Defaults to this repository's skills directory.",
    )
    parser.add_argument(
        "--with-skills",
        action="append",
        default=[],
        metavar="PROFILE_OR_SKILL",
        help=(
            "Install an optional skill profile or skill into .agents/skills. "
            "Can be repeated. Example: --with-skills core"
        ),
    )
    parser.add_argument(
        "--list-skills",
        action="store_true",
        help="List available skill profiles and skills, then exit.",
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


def load_skill_registry(skills_dir: Path) -> dict:
    registry_path = skills_dir / "registry.json"
    if not registry_path.is_file():
        raise FileNotFoundError(f"Skill registry not found: {registry_path}")
    with registry_path.open(encoding="utf-8") as file:
        return json.load(file)


def print_skill_registry(registry: dict) -> None:
    profiles = registry.get("profiles", {})
    skills = registry.get("skills", [])

    print("Available skill profiles:")
    if profiles:
        for name, data in sorted(profiles.items()):
            description = data.get("description", "")
            print(f"  {name}: {description}")
    else:
        print("  (none)")

    print("\nAvailable skills:")
    if skills:
        for skill in sorted(skills, key=lambda item: item["name"]):
            name = skill["name"]
            profile = skill.get("profile", "-")
            source = skill.get("source", "-")
            audit_status = skill.get("audit_status", "-")
            print(f"  {name} [{profile}] {audit_status} {source}")
    else:
        print("  (none)")


def resolve_requested_skills(registry: dict, requested: list[str]) -> list[dict]:
    if not requested:
        return []

    profiles = registry.get("profiles", {})
    skills = {skill["name"]: skill for skill in registry.get("skills", [])}
    resolved_names: list[str] = []

    for item in requested:
        if item in profiles:
            resolved_names.extend(profiles[item].get("skills", []))
        elif item in skills:
            resolved_names.append(item)
        else:
            known_profiles = ", ".join(sorted(profiles)) or "(none)"
            known_skills = ", ".join(sorted(skills)) or "(none)"
            raise ValueError(
                f"Unknown skill profile or skill: {item}\n"
                f"Known profiles: {known_profiles}\n"
                f"Known skills: {known_skills}"
            )

    unique_names = list(dict.fromkeys(resolved_names))
    return [skills[name] for name in unique_names]


def resolve_local_skill_dir(skills_dir: Path, skill: dict) -> Path:
    source = skill.get("source", "")
    if not source.startswith("local:"):
        raise ValueError(
            f"Unsupported skill source for {skill.get('name', '<unknown>')}: {source}"
        )
    relative_source = source.removeprefix("local:")
    return (skills_dir / relative_source).resolve()


def iter_template_files(template_dir: Path) -> list[Path]:
    ignored_names = {".DS_Store"}

    def should_include(path: Path) -> bool:
        if not path.is_file():
            return False
        if path.name in ignored_names or path.name.startswith("._"):
            return False
        return "__pycache__" not in path.parts

    return sorted(path for path in template_dir.rglob("*") if should_include(path))


def iter_skill_files(skill_dir: Path) -> list[Path]:
    ignored_names = {".DS_Store"}

    def should_include(path: Path) -> bool:
        if not path.is_file():
            return False
        if path.name in ignored_names or path.name.startswith("._"):
            return False
        return "__pycache__" not in path.parts

    return sorted(path for path in skill_dir.rglob("*") if should_include(path))


def main() -> int:
    args = parse_args()
    skills_dir = Path(args.skills_dir).expanduser().resolve()

    if args.list_skills:
        try:
            print_skill_registry(load_skill_registry(skills_dir))
        except (FileNotFoundError, json.JSONDecodeError) as error:
            print(error, file=sys.stderr)
            return 2
        return 0

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

    try:
        registry = load_skill_registry(skills_dir)
        requested_skills = resolve_requested_skills(registry, args.with_skills)
    except (FileNotFoundError, json.JSONDecodeError, ValueError) as error:
        print(error, file=sys.stderr)
        return 2

    values = {
        "PROJECT_NAME": project_name,
        "PROJECT_DESCRIPTION": args.description,
        "DATE": args.date,
    }

    planned: list[tuple[Path, Path, str]] = []
    planned_skill_files: list[tuple[Path, Path]] = []
    existing: list[Path] = []

    for source in files:
        relative_path = source.relative_to(template_dir)
        destination = target_dir / relative_path
        if destination.exists() and not args.force:
            existing.append(destination)
            continue
        content = source.read_text(encoding="utf-8")
        planned.append((source, destination, render_template(content, values)))

    for skill in requested_skills:
        skill_dir = resolve_local_skill_dir(skills_dir, skill)
        if not skill_dir.is_dir():
            print(f"Skill directory not found: {skill_dir}", file=sys.stderr)
            return 2
        for source in iter_skill_files(skill_dir):
            relative_path = source.relative_to(skill_dir)
            destination = target_dir / ".agents" / "skills" / skill["name"] / relative_path
            if destination.exists() and not args.force:
                existing.append(destination)
                continue
            planned_skill_files.append((source, destination))

    if existing:
        print("Skipped existing files. Re-run with --force to overwrite:")
        for path in existing:
            print(f"  {path}")

    if args.dry_run:
        print("Dry run. Files that would be written:")
        for _, destination, _ in planned:
            print(f"  {destination}")
        for _, destination in planned_skill_files:
            print(f"  {destination}")
        return 0

    for _, destination, content in planned:
        destination.parent.mkdir(parents=True, exist_ok=True)
        destination.write_text(content, encoding="utf-8")
        print(f"Wrote {destination}")

    for source, destination in planned_skill_files:
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        print(f"Wrote {destination}")

    installed_skills = sorted(
        {
            destination.relative_to(target_dir / ".agents" / "skills").parts[0]
            for _, destination in planned_skill_files
        }
    )
    if installed_skills:
        print("Installed skills:")
        for skill_name in installed_skills:
            print(f"  {target_dir / '.agents' / 'skills' / skill_name}")

    print(
        f"Initialized Agent docs for {project_name} in {target_dir}"
        if planned or planned_skill_files
        else "No files written."
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
