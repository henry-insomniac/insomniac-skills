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

## 使用方式

### npm / npx 使用

npm 包提供 `init-agent-docs` 命令，内部仍调用 Python 标准库脚本，因此用户机器需要安装 `python3`。

直接通过 npx 运行：

```bash
npx -p insomniac-skills init-agent-docs \
  --project-name my-project \
  --description "这是一个示例项目"
```

全局安装后运行：

```bash
npm install -g insomniac-skills
init-agent-docs \
  --project-name my-project \
  --description "这是一个示例项目"
```

项目内安装后运行：

```bash
npm install -D insomniac-skills
npx init-agent-docs \
  --project-name my-project \
  --description "这是一个示例项目"
```
