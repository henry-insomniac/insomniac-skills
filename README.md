# insomniac-skills

用于初始化项目级 Agent 协作文档的脚手架。

脚手架会在目标项目中生成：

- `AGENTS.md`
- `.claude/README.md`
- `.claude/project-architecture.md`
- `.claude/skill-authoring.md`
- `.claude/bug-fix-log.md`
- `.claude/git-collaboration.md`
- `.claude/tech-stack.md`

启用 Agent 操作规则层后，还会生成：

- `docs/agents/README.md`
- `docs/agents/issue-tracker.md`
- `docs/agents/triage-labels.md`
- `docs/agents/domain.md`
- `docs/agents/skill-usage.md`
- `docs/adr/README.md`
- `CONTEXT.md` 或 `CONTEXT-MAP.md`（`claude-only` 不生成）
- `.scratch/README.md`（仅当 issue tracker 选择 `local`）

## 使用方式

### curl 安装

普通用户安装：

```bash
curl -fsSL https://yi-flow.com/insomniac-skills/install.sh | bash
```

系统级安装：

```bash
curl -fsSL https://yi-flow.com/insomniac-skills/install.sh | sudo bash
```

安装统计看板：

```text
https://yi-flow.com/insomniac-skills/dashboard
```

看板启用了 Basic Auth。服务器上的凭据保存在：

```text
/root/insomniac-skills-dashboard-credentials.txt
```

安装后可在任意项目目录使用：

```bash
init-agent-docs \
  --project-name my-project \
  --description "这是一个示例项目"
```

### 仓库内直接运行

在本仓库中运行：

```bash
python3 scripts/init_agent_docs.py \
  --target /path/to/project \
  --project-name my-project \
  --description "一个示例项目"
```

默认不会覆盖目标项目已有文件。如需覆盖：

```bash
python3 scripts/init_agent_docs.py \
  --target /path/to/project \
  --project-name my-project \
  --description "一个示例项目" \
  --force
```

预览将写入哪些文件：

```bash
python3 scripts/init_agent_docs.py \
  --target /path/to/project \
  --project-name my-project \
  --dry-run
```

### Agent 操作规则层

参考 `setup-matt-pocock-skills` 的项目配置思路，脚手架可以额外初始化 Agent 处理 issue、triage label 和领域上下文时需要读取的规则文件：

```bash
python3 scripts/init_agent_docs.py \
  --target /path/to/project \
  --project-name my-project \
  --description "一个示例项目" \
  --with-agent-ops \
  --issue-tracker auto \
  --domain-layout single
```

`--issue-tracker` 支持：

- `manual`：默认值，不假设项目使用哪种 issue tracker，写入待确认模板。
- `auto`：读取目标项目 `.git/config`，检测 GitHub 或 GitLab remote。
- `github`：生成 GitHub Issues / `gh` CLI 规则。
- `gitlab`：生成 GitLab Issues / `glab` CLI 规则。
- `local`：生成本地 Markdown 规则，并创建 `.scratch/README.md`。

`--domain-layout` 支持：

- `single`：默认值，生成根目录 `CONTEXT.md`。
- `multi`：生成根目录 `CONTEXT-MAP.md`，用于多上下文项目。
- `claude-only`：只使用 `AGENTS.md` 和 `.claude/` 作为长期上下文，不生成 `CONTEXT.md`。

### 可选安装 skills

默认安装只生成协作文档，不会安装任何 skill。查看可选 profile 和 skill：

```bash
init-agent-docs --list-skills
```

安装本项目维护的 `core` skills：

```bash
init-agent-docs \
  --project-name my-project \
  --description "这是一个示例项目" \
  --with-skills core
```

`core` profile 当前包含：

- `agent-docs-bootstrap`：初始化或修复项目级 Agent 协作文档。
- `template-maintainer`：维护 `templates/agent-docs/` 和生成文档契约。
- `skill-author`：创建、更新或审查 Agent Skill。
- `bug-fix-recorder`：修复问题后沉淀 `.claude/bug-fix-log.md`。
- `repo-onboarding`：进入陌生仓库时做事实型项目梳理。
- `security-boundary-review`：审查脚本、安装器、skill 和外部服务安全边界。
- `release-packaging`：维护安装脚本、发布包和安装验证。
- `agent-handoff`：把完成或暂停的 Agent 工作整理成交接摘要。

skills 会写入目标项目的：

```text
.agents/skills/
```

已有 skill 文件默认跳过。如需覆盖，显式添加 `--force`。当前仅内置本项目维护的 `core` profile，第三方开源 skills 应先进入 registry 审计、锁定版本和许可证后再提供安装入口。

## 模板位置

模板文件位于：

```text
templates/agent-docs/
```

模板支持以下占位符：

- `{{PROJECT_NAME}}`
- `{{PROJECT_DESCRIPTION}}`
- `{{DATE}}`
- `{{AGENT_SKILLS_BLOCK}}`
- `{{ISSUE_TRACKER_CONTENT}}`
- `{{DOMAIN_DOCS_CONTENT}}`

## 维护方式

- 修改脚手架输出内容时，优先修改 `templates/agent-docs/`。
- 修改初始化行为时，更新 `scripts/init_agent_docs.py`。
- 修改内置 skills 或 registry 时，同步更新 `skills/registry.json` 和 `.claude/skill-authoring.md`。
- 修改安装行为时，更新 `install.sh`。
- 调整项目架构或技术规范时，同步更新 `.claude/` 中的长期文档。
- 修改 CLI 行为后，更新或补充 `tests/` 中的集成测试。

## 安全策略

- 安装脚本和安装包公开访问，但由 nginx 做 IP 级限流。
- dashboard 需要 Basic Auth。
- 非 `GET` / `HEAD` 请求会被 nginx 拒绝。
- 统计事件最多保留 20,000 条，最多保留 180 天。
- dashboard 中展示的 IP 会脱敏，完整 IP 仅保存在服务器 SQLite 数据库中用于归属地解析和去重。
- 第三方 skills 不应默认安装；安装前必须审计 `SKILL.md`、脚本、外部网络访问、文件写入、许可证和版本锁定信息。
