# insomniac-skills

用于初始化项目级 Agent 协作文档和操作上下文的脚手架。

English README: [README.md](README.md)

## 生成内容

默认会在目标项目中生成：

- `AGENTS.md`
- `.claude/README.md`
- `.claude/project-architecture.md`
- `.claude/skill-authoring.md`
- `.claude/bug-fix-log.md`
- `.claude/git-collaboration.md`
- `.claude/tech-stack.md`

启用设计系统入口后，还会生成：

- `DESIGN.md`

启用 Agent 操作规则层后，还会生成：

- `docs/agents/README.md`
- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`
- `docs/agents/domain.md`
- `docs/agents/skill-usage.md`
- `docs/adr/README.md`
- `CONTEXT.md` 或 `CONTEXT-MAP.md`（`claude-only` 不生成）
- `.scratch/README.md`（仅当 issue tracker 选择 `local`）

## 前置条件

npm 包推荐使用短命令 `isk init`，同时保留 `insomniac-skills init-agent-docs` 和 `init-agent-docs` 兼容入口。所有入口内部都调用同一份 Python 标准库脚本，因此用户机器需要安装 `python3`。

该 npm 包需要 Node.js 18 或更高版本。

## 安装与运行

直接通过 npx 运行：

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "一个示例项目"
```

全局安装后运行：

```bash
npm install -g insomniac-skills
isk init \
  --name my-project \
  --desc "一个示例项目"
```

项目内安装后运行：

```bash
npm install -D insomniac-skills
npx isk init \
  --name my-project \
  --desc "一个示例项目"
```

## 系统命令

安装后可用的系统命令：

```bash
isk init [options]
insomniac-skills init [options]
insomniac-skills init-agent-docs [options]
init-agent-docs [options]
```

无需安装时，推荐直接使用：

```bash
npx -p insomniac-skills isk init [options]
```

查看帮助：

```bash
npx -p insomniac-skills isk init --help
```

## 常用示例

在当前目录初始化基础 Agent 文档：

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "一个示例项目"
```

初始化到指定项目目录：

```bash
npx -p insomniac-skills isk init \
  --target /path/to/project \
  --name my-project \
  --desc "一个示例项目"
```

同时生成 `DESIGN.md`：

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "一个示例项目" \
  --design
```

同时生成 Agent 操作规则层：

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --desc "一个示例项目" \
  --ops \
  --issues \
  --domain-layout single
```

预览将写入哪些文件，不实际修改：

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --dry-run
```

覆盖已有文件：

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --force
```

查看可安装 skill：

```bash
npx -p insomniac-skills isk init --list-skills
```

安装 core skills：

```bash
npx -p insomniac-skills isk init \
  --name my-project \
  --with-skills core
```

## 全部参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `-h`, `--help` | - | 显示帮助信息。 |
| `--target TARGET` | `.` | 目标项目目录。 |
| `--project-name PROJECT_NAME`, `--name NAME` | 目标目录名 | 项目名称，会写入生成文档。 |
| `--description DESCRIPTION`, `--desc DESC` | `这是一个需要维护长期 Agent 上下文的项目。` | 项目描述，会写入生成文档。 |
| `--template-dir TEMPLATE_DIR` | 包内 `templates/agent-docs` | 自定义模板目录。 |
| `--skills-dir SKILLS_DIR` | 包内 `skills` | 自定义 skills registry 和 skill 源目录。 |
| `--with-skills PROFILE_OR_SKILL` | - | 安装可选 skill profile 或单个 skill 到 `.agents/skills/`，可重复传入。 |
| `--with-agent-ops`, `--ops` | 关闭 | 生成 `docs/agents/*`、`docs/adr/README.md`，并按领域布局生成 `CONTEXT.md` 或 `CONTEXT-MAP.md`。 |
| `--with-design`, `--design` | 关闭 | 生成根目录 `DESIGN.md`，并在 Agent 入口中加入 UI 任务读取提示。 |
| `--issue-tracker [auto\|github\|gitlab\|local\|manual]`, `--issues [TYPE]` | `manual` | 配置 Agent 操作规则层中的 issue tracker 文档；不带值时等同 `auto`。只有配合 `--with-agent-ops` 或 `--ops` 才会写入对应文件。 |
| `--domain-layout single\|multi\|claude-only` | `single` | 配置领域上下文布局。`single` 生成 `CONTEXT.md`，`multi` 生成 `CONTEXT-MAP.md`，`claude-only` 不生成 `CONTEXT*`。 |
| `--list-skills` | 关闭 | 列出可用 skill profiles 和 skills 后退出。 |
| `--date DATE` | 今天 | 初始化日期，格式建议使用 `YYYY-MM-DD`。 |
| `--force` | 关闭 | 覆盖目标项目已有文件。默认保护已有文件并跳过。 |
| `--dry-run` | 关闭 | 只显示将写入的文件，不修改目标项目。 |

## 许可证

本项目使用 MIT License。详见 `LICENSE`。
