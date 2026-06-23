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
AGENT_OPS_TOP_LEVEL_FILES = {"CONTEXT-MAP.md", "CONTEXT.md"}
AGENT_OPS_TOP_LEVEL_DIRS = {".scratch", "docs"}
DESIGN_TOP_LEVEL_FILES = {"DESIGN.md"}


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
        "--with-agent-ops",
        action="store_true",
        help=(
            "Create Agent operating docs such as docs/agents/*, "
            "docs/adr/README.md, and CONTEXT.md."
        ),
    )
    parser.add_argument(
        "--with-design",
        action="store_true",
        help="Create a root DESIGN.md visual system guide for UI work.",
    )
    parser.add_argument(
        "--issue-tracker",
        choices=["auto", "github", "gitlab", "local", "manual"],
        default="manual",
        help=(
            "Issue tracker docs to generate with --with-agent-ops. "
            "Use auto to inspect the target git remote."
        ),
    )
    parser.add_argument(
        "--domain-layout",
        choices=["single", "multi", "claude-only"],
        default="single",
        help=(
            "Domain documentation layout to generate with --with-agent-ops. "
            "Use single for CONTEXT.md, multi for CONTEXT-MAP.md, or claude-only."
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


def is_agent_ops_template(relative_path: Path) -> bool:
    return (
        relative_path.name in AGENT_OPS_TOP_LEVEL_FILES
        or relative_path.parts[0] in AGENT_OPS_TOP_LEVEL_DIRS
    )


def is_design_template(relative_path: Path) -> bool:
    return relative_path.name in DESIGN_TOP_LEVEL_FILES


def is_local_issue_tracker_template(relative_path: Path) -> bool:
    return relative_path.parts[0] == ".scratch"


def is_context_template(relative_path: Path) -> bool:
    return relative_path == Path("CONTEXT.md")


def is_context_map_template(relative_path: Path) -> bool:
    return relative_path == Path("CONTEXT-MAP.md")


def agent_skills_block() -> str:
    return """## Agent skills

### Issue tracker

本项目的 issue、PRD 和任务流转规则见 `docs/agents/issue-tracker.md`。

### Triage labels

Agent 处理 issue 状态时，必须使用 `docs/agents/triage-labels.md` 中定义的 label 映射。

### Domain docs

理解项目领域语言、架构决策和长期上下文时，先阅读 `docs/agents/domain.md`。
"""


def design_guidance_block() -> str:
    return """## 设计系统

涉及 UI、前端、视觉样式、组件状态、响应式布局或设计还原时，先阅读根目录 `DESIGN.md`。该文件是项目视觉系统入口，记录颜色、字体、间距、组件和设计禁用项。
"""


def design_architecture_block() -> str:
    return """如果初始化时启用了 `--with-design`，还会生成：

```text
.
└── DESIGN.md
```

### `DESIGN.md`

`DESIGN.md` 是项目视觉系统入口，用于记录 UI 任务需要遵循的颜色、字体、间距、组件样式和设计禁用项。
"""


def design_tech_stack_block() -> str:
    return """## 设计系统规范

如果项目启用了 `DESIGN.md`，UI 相关任务应先读取根目录 `DESIGN.md`，并优先复用其中定义的颜色、字体、间距、圆角和组件规则。

如项目允许临时使用 Node.js，可用 Google DESIGN.md CLI 做结构检查：

```bash
npx @google/design.md lint DESIGN.md
```

该命令需要网络和 npm registry 访问；离线环境下应至少人工检查 front matter、token 引用和 Markdown section 顺序。
"""


def detect_issue_tracker(target_dir: Path, requested: str) -> str:
    if requested != "auto":
        return requested

    git_config = target_dir / ".git" / "config"
    if not git_config.is_file():
        return "manual"

    config_text = git_config.read_text(encoding="utf-8", errors="replace").lower()
    if "github.com" in config_text:
        return "github"
    if "gitlab" in config_text:
        return "gitlab"
    return "manual"


def issue_tracker_content(issue_tracker: str, project_name: str) -> str:
    if issue_tracker == "github":
        return """# Issue Tracker

本项目的 issue、PRD 和任务流转使用 GitHub Issues。Agent 应通过 `gh` CLI 操作 issue。

## 常用操作

- 创建 issue：`gh issue create --title "..." --body "..."`
- 读取 issue：`gh issue view <number> --comments`
- 列出 issue：`gh issue list --state open --json number,title,body,labels,comments`
- 评论 issue：`gh issue comment <number> --body "..."`
- 添加或移除 label：`gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- 关闭 issue：`gh issue close <number> --comment "..."`

仓库由当前目录的 `git remote -v` 推断。执行写入操作前，确认 `gh auth status` 已登录到正确账号。

## Agent 规则

- 当任务要求发布 PRD 或拆分 issue 时，创建 GitHub issue。
- 当任务引用 issue 编号时，使用 `gh issue view <number> --comments` 读取完整上下文。
- 涉及私有仓库、账号权限或敏感信息时，先确认安全边界。
"""

    if issue_tracker == "gitlab":
        return """# Issue Tracker

本项目的 issue、PRD 和任务流转使用 GitLab Issues。Agent 应通过 `glab` CLI 操作 issue。

## 常用操作

- 创建 issue：`glab issue create --title "..." --description "..."`
- 读取 issue：`glab issue view <number> --comments`
- 列出 issue：`glab issue list -F json`
- 评论 issue：`glab issue note <number> --message "..."`
- 添加或移除 label：`glab issue update <number> --label "..."` / `--unlabel "..."`
- 关闭 issue：`glab issue close <number>`

仓库由当前目录的 `git remote -v` 推断。执行写入操作前，确认 `glab auth status` 已登录到正确账号。

## Agent 规则

- 当任务要求发布 PRD 或拆分 issue 时，创建 GitLab issue。
- 当任务引用 issue 编号时，使用 `glab issue view <number> --comments` 读取完整上下文。
- GitLab 将 PR 称为 merge request；涉及 MR 时使用 `glab mr ...` 命令。
- 涉及私有仓库、账号权限或敏感信息时，先确认安全边界。
"""

    if issue_tracker == "local":
        return f"""# Issue Tracker

本项目的 issue、PRD 和任务流转使用 Local Markdown。相关文件保存在 `{project_name}` 仓库内的 `.scratch/`。

## 文件约定

- 一个需求或功能一个目录：`.scratch/<feature>/`
- PRD 写入：`.scratch/<feature>/PRD.md`
- 拆分后的 issue 写入：`.scratch/<feature>/issues/01-<topic>.md`
- triage 状态写在 issue 文件顶部的 `Status:` 行，状态值参考 `docs/agents/triage-labels.md`
- 评论和后续对话追加到文件末尾的 `## Comments` 区域

## Agent 规则

- 当任务要求发布 PRD 或拆分 issue 时，创建或更新 `.scratch/<feature>/` 下的 Markdown 文件。
- 当任务引用本地 issue 时，读取用户提供的文件路径。
- 不要把 `.scratch/` 当作临时垃圾目录；其中内容代表项目本地任务记录。
"""

    return f"""# Issue Tracker

`{project_name}` 的 issue、PRD 和任务流转位置尚未配置。

## 默认规则

- Agent 不应假设项目一定使用 GitHub、GitLab、Linear、Jira 或本地 Markdown。
- 创建、读取、关闭 issue 或写入 PRD 前，必须先确认项目真实使用的 issue tracker。
- 若项目后续决定使用 GitHub Issues、GitLab Issues 或本地 `.scratch/` 文件，应把具体命令和路径记录到本文件。

## 待维护内容

- issue tracker 类型：
- 创建 issue 的方式：
- 读取 issue 的方式：
- 评论或追加上下文的方式：
- 关闭或标记完成的方式：
"""


def domain_docs_content(domain_layout: str, project_name: str) -> str:
    if domain_layout == "claude-only":
        return f"""# Domain Docs

本项目使用 `claude-only` 长期上下文布局。Agent 在 `{project_name}` 中理解项目背景、架构和协作规则时，优先读取 `.claude/`。

## 读取顺序

1. 先阅读根目录 `AGENTS.md`。
2. 再阅读 `.claude/README.md`，按索引进入相关长期文档。
3. 如果存在 `docs/adr/`，阅读和当前改动相关的 ADR。

缺失的文件不代表错误。Agent 应基于已有文档工作，不要为了补齐形式而编造不存在的架构。

## 输出规则

- 输出 issue、PRD、测试名、提交说明或架构建议时，使用 `.claude/` 已记录的项目词汇。
- 如果需要的新概念不在上下文中，应在结果中说明这是待确认的领域词汇。
- 如果改动与现有 ADR 冲突，必须显式指出冲突点和需要重新决策的原因。
"""

    return f"""# Domain Docs

本项目使用 `{domain_layout}` 长期上下文布局。Agent 在 `{project_name}` 中理解项目背景、领域语言和架构决策时，应同时读取 `.claude/` 与领域上下文文件。

## 读取顺序

1. 先阅读根目录 `AGENTS.md`。
2. 再阅读 `.claude/README.md`，按索引进入相关长期文档。
3. 如果存在 `CONTEXT.md`，阅读其中的领域词汇和项目边界。
4. 如果存在 `CONTEXT-MAP.md`，按任务相关范围读取对应的 `CONTEXT.md`。
5. 如果存在 `docs/adr/`，阅读和当前改动相关的 ADR。

缺失的文件不代表错误。Agent 应基于已有文档工作，不要为了补齐形式而编造不存在的架构。

## 领域语言

- 输出 issue、PRD、测试名、提交说明或架构建议时，优先使用 `CONTEXT.md` 已定义的项目词汇。
- 如果需要的新概念不在上下文中，应在结果中说明这是待确认的领域词汇。
- 如果改动与现有 ADR 冲突，必须显式指出冲突点和需要重新决策的原因。
"""


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

    issue_tracker = detect_issue_tracker(target_dir, args.issue_tracker)

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
        "AGENT_SKILLS_BLOCK": agent_skills_block() if args.with_agent_ops else "",
        "DESIGN_GUIDANCE_BLOCK": design_guidance_block() if args.with_design else "",
        "DESIGN_ARCHITECTURE_BLOCK": (
            design_architecture_block() if args.with_design else ""
        ),
        "DESIGN_TECH_STACK_BLOCK": design_tech_stack_block() if args.with_design else "",
        "ISSUE_TRACKER_CONTENT": issue_tracker_content(issue_tracker, project_name),
        "DOMAIN_DOCS_CONTENT": domain_docs_content(args.domain_layout, project_name),
    }

    planned: list[tuple[Path, Path, str]] = []
    planned_skill_files: list[tuple[Path, Path]] = []
    existing: list[Path] = []

    for source in files:
        relative_path = source.relative_to(template_dir)
        if is_agent_ops_template(relative_path) and not args.with_agent_ops:
            continue
        if is_design_template(relative_path) and not args.with_design:
            continue
        if (
            is_local_issue_tracker_template(relative_path)
            and issue_tracker != "local"
        ):
            continue
        if is_context_template(relative_path) and args.domain_layout != "single":
            continue
        if is_context_map_template(relative_path) and args.domain_layout != "multi":
            continue
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
