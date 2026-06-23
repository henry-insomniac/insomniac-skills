# insomniac-skills

用于初始化项目级 Agent 协作文档的脚手架。

A scaffold for initializing project-level Agent collaboration documents.

## 生成内容 / Generated Files

默认会在目标项目中生成：

By default, the CLI generates:

- `AGENTS.md`
- `.claude/README.md`
- `.claude/project-architecture.md`
- `.claude/skill-authoring.md`
- `.claude/bug-fix-log.md`
- `.claude/git-collaboration.md`
- `.claude/tech-stack.md`

启用设计系统入口后，还会生成：

With the design entrypoint enabled, it also generates:

- `DESIGN.md`

启用 Agent 操作规则层后，还会生成：

With Agent operating docs enabled, it also generates:

- `docs/agents/README.md`
- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`
- `docs/agents/domain.md`
- `docs/agents/skill-usage.md`
- `docs/adr/README.md`
- `CONTEXT.md` 或 `CONTEXT-MAP.md` (`claude-only` 不生成 / not generated for `claude-only`)
- `.scratch/README.md` (仅当 issue tracker 选择 `local` / only when issue tracker is `local`)

## 前置条件 / Requirements

npm 包推荐使用短命令 `isk init`，同时保留 `insomniac-skills init-agent-docs` 和 `init-agent-docs` 兼容入口。所有入口内部都调用同一份 Python 标准库脚本，因此用户机器需要安装 `python3`。

The npm package recommends the short `isk init` command, while keeping `insomniac-skills init-agent-docs` and direct `init-agent-docs` compatibility entries. All entries run the same Python standard-library script internally, so `python3` must be available on the user's machine.

## 安装与运行 / Install and Run

直接通过 npx 运行：

Run directly with npx:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "这是一个示例项目"
```

全局安装后运行：

Install globally:

```bash
npm install -g insomniac-skills
isk init \
  --name my-project \
  --desc "这是一个示例项目"
```

项目内安装后运行：

Install in a project:

```bash
npm install -D insomniac-skills
npx isk init \
  --name my-project \
  --desc "这是一个示例项目"
```

## 系统命令 / Command

安装后可用的系统命令是：

After installation, the system command is:

```bash
isk init [options]
insomniac-skills init [options]
insomniac-skills init-agent-docs [options]
init-agent-docs [options]
```

无需安装时，推荐直接用：

Without installation, use:

```bash
npx -p insomniac-skills isk init [options]
```

查看帮助：

Show help:

```bash
npx -p insomniac-skills isk init --help
```

## 常用示例 / Examples

在当前目录初始化基础 Agent 文档：

Initialize basic Agent docs in the current directory:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "这是一个示例项目"
```

初始化到指定项目目录：

Initialize into a specific target directory:

```bash
npx -p insomniac-skills isk init \
  --target /path/to/project \
  --name my-project \
  --desc "这是一个示例项目"
```

同时生成 `DESIGN.md`：

Also generate `DESIGN.md`:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "这是一个示例项目" \
  --design
```

同时生成 Agent 操作规则层：

Also generate Agent operating docs:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "这是一个示例项目" \
  --ops \
  --issues \
  --domain-layout single
```

预览将写入哪些文件，不实际修改：

Preview files without writing:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --dry-run
```

覆盖已有文件：

Overwrite existing files:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --force
```

查看可安装 skill：

List installable skills:

```bash
npx -p insomniac-skills isk init --list-skills
```

安装 core skills：

Install core skills:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --with-skills core
```

## 全部参数 / Options

| 参数 / Option | 默认值 / Default | 说明 / Description |
| --- | --- | --- |
| `-h`, `--help` | - | 显示帮助信息。 / Show help. |
| `--target TARGET` | `.` | 目标项目目录。 / Target project directory. |
| `--project-name PROJECT_NAME`, `--name NAME` | 目标目录名 / target directory name | 项目名称，会写入生成文档。 / Project name written into generated docs. |
| `--description DESCRIPTION`, `--desc DESC` | `这是一个需要维护长期 Agent 上下文的项目。` | 项目描述，会写入生成文档。 / Project description written into generated docs. |
| `--template-dir TEMPLATE_DIR` | 包内 `templates/agent-docs` / bundled `templates/agent-docs` | 自定义模板目录。 / Custom template directory. |
| `--skills-dir SKILLS_DIR` | 包内 `skills` / bundled `skills` | 自定义 skills registry 和 skill 源目录。 / Custom skills registry and skill source directory. |
| `--with-skills PROFILE_OR_SKILL` | - | 安装可选 skill profile 或单个 skill 到 `.agents/skills/`，可重复传入。 / Install an optional skill profile or single skill into `.agents/skills/`; can be repeated. |
| `--with-agent-ops`, `--ops` | 关闭 / off | 生成 `docs/agents/*`、`docs/adr/README.md`，并按领域布局生成 `CONTEXT.md` 或 `CONTEXT-MAP.md`。 / Generate `docs/agents/*`, `docs/adr/README.md`, and `CONTEXT.md` or `CONTEXT-MAP.md` based on domain layout. |
| `--with-design`, `--design` | 关闭 / off | 生成根目录 `DESIGN.md`，并在 Agent 入口中加入 UI 任务读取提示。 / Generate root `DESIGN.md` and add UI-task guidance to Agent entry docs. |
| `--issue-tracker [auto\|github\|gitlab\|local\|manual]`, `--issues [TYPE]` | `manual` | 配置 Agent 操作规则层中的 issue tracker 文档；不带值时等同 `auto`。只有配合 `--with-agent-ops` / `--ops` 才会写入对应文件。 / Configure issue tracker docs for Agent operating rules; omitting the value is the same as `auto`. Only writes files when used with `--with-agent-ops` / `--ops`. |
| `--domain-layout single\|multi\|claude-only` | `single` | 配置领域上下文布局。`single` 生成 `CONTEXT.md`，`multi` 生成 `CONTEXT-MAP.md`，`claude-only` 不生成 `CONTEXT*`。 / Configure domain context layout. `single` generates `CONTEXT.md`, `multi` generates `CONTEXT-MAP.md`, and `claude-only` skips `CONTEXT*`. |
| `--list-skills` | 关闭 / off | 列出可用 skill profiles 和 skills 后退出。 / List available skill profiles and skills, then exit. |
| `--date DATE` | 今天 / today | 初始化日期，格式建议使用 `YYYY-MM-DD`。 / Initialization date, preferably `YYYY-MM-DD`. |
| `--force` | 关闭 / off | 覆盖目标项目已有文件。默认保护已有文件并跳过。 / Overwrite existing files. Existing files are protected and skipped by default. |
| `--dry-run` | 关闭 / off | 只显示将写入的文件，不修改目标项目。 / Show files that would be written without modifying the target project. |

## 许可证 / License

本项目使用 MIT License。详见 `LICENSE`。

This project is released under the MIT License. See `LICENSE`.
