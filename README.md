# insomniac-skills

Scaffold reusable project-level Agent collaboration docs and operating context.

中文文档: [README.zh-CN.md](README.zh-CN.md)

## Generated Files

By default, the CLI generates:

- `AGENTS.md`
- `.claude/README.md`
- `.claude/project-architecture.md`
- `.claude/skill-authoring.md`
- `.claude/bug-fix-log.md`
- `.claude/git-collaboration.md`
- `.claude/tech-stack.md`

With the design entrypoint enabled, it also generates:

- `DESIGN.md`

With Agent operating docs enabled, it also generates:

- `docs/agents/README.md`
- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`
- `docs/agents/domain.md`
- `docs/agents/skill-usage.md`
- `docs/adr/README.md`
- `CONTEXT.md` or `CONTEXT-MAP.md` (`claude-only` does not generate either file)
- `.scratch/README.md` (only when the issue tracker is `local`)

## Requirements

The npm package recommends the short `isk init` command, while keeping `insomniac-skills init-agent-docs` and direct `init-agent-docs` compatibility entries. All entries run the same Python standard-library script internally, so `python3` must be available on the user's machine.

The package requires Node.js 18 or newer.

## Install and Run

Run directly with npx:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "An example project"
```

Install globally:

```bash
npm install -g insomniac-skills
isk init \
  --name my-project \
  --desc "An example project"
```

Install in a project:

```bash
npm install -D insomniac-skills
npx isk init \
  --name my-project \
  --desc "An example project"
```

## Commands

Available commands after installation:

```bash
isk init [options]
insomniac-skills init [options]
insomniac-skills init-agent-docs [options]
init-agent-docs [options]
```

Use this command when you do not want to install the package first:

```bash
npx -p insomniac-skills isk init [options]
```

Show help:

```bash
npx -p insomniac-skills isk init --help
```

## Examples

Initialize basic Agent docs in the current directory:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "An example project"
```

Initialize into a specific target directory:

```bash
npx -p insomniac-skills isk init \
  --target /path/to/project \
  --name my-project \
  --desc "An example project"
```

Also generate `DESIGN.md`:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "An example project" \
  --design
```

Also generate Agent operating docs:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "An example project" \
  --ops \
  --issues \
  --domain-layout single
```

Preview files without writing:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --dry-run
```

Overwrite existing files:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --force
```

List installable skills:

```bash
npx -p insomniac-skills isk init --list-skills
```

Install core skills:

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --with-skills core
```

## Options

| Option | Default | Description |
| --- | --- | --- |
| `-h`, `--help` | - | Show help. |
| `--target TARGET` | `.` | Target project directory. |
| `--project-name PROJECT_NAME`, `--name NAME` | target directory name | Project name written into generated docs. |
| `--description DESCRIPTION`, `--desc DESC` | `这是一个需要维护长期 Agent 上下文的项目。` | Project description written into generated docs. |
| `--template-dir TEMPLATE_DIR` | bundled `templates/agent-docs` | Custom template directory. |
| `--skills-dir SKILLS_DIR` | bundled `skills` | Custom skills registry and skill source directory. |
| `--with-skills PROFILE_OR_SKILL` | - | Install an optional skill profile or single skill into `.agents/skills/`; can be repeated. |
| `--with-agent-ops`, `--ops` | off | Generate `docs/agents/*`, `docs/adr/README.md`, and `CONTEXT.md` or `CONTEXT-MAP.md` based on domain layout. |
| `--with-design`, `--design` | off | Generate root `DESIGN.md` and add UI-task guidance to Agent entry docs. |
| `--issue-tracker [auto\|github\|gitlab\|local\|manual]`, `--issues [TYPE]` | `manual` | Configure issue tracker docs for Agent operating rules; omitting the value is the same as `auto`. Only writes files when used with `--with-agent-ops` or `--ops`. |
| `--domain-layout single\|multi\|claude-only` | `single` | Configure domain context layout. `single` generates `CONTEXT.md`, `multi` generates `CONTEXT-MAP.md`, and `claude-only` skips `CONTEXT*`. |
| `--list-skills` | off | List available skill profiles and skills, then exit. |
| `--date DATE` | today | Initialization date, preferably `YYYY-MM-DD`. |
| `--force` | off | Overwrite existing files. Existing files are protected and skipped by default. |
| `--dry-run` | off | Show files that would be written without modifying the target project. |

## License

This project is released under the MIT License. See `LICENSE`.
