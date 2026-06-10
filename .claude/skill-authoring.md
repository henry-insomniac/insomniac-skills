# Skill 编写规范

## 基本目标

每个 skill 都应该把一个可重复工作流描述清楚，让 Agent 能在合适场景下稳定执行，并让维护者能审查其边界、风险和输出质量。

## 当前分发策略

本仓库默认仍是 Agent 协作文档脚手架。skills 是可选安装层：

- 默认执行 `init-agent-docs` 时，不安装任何 skill。
- 用户显式传入 `--with-skills core` 时，才把本项目维护的 core skills 写入目标项目 `.agents/skills/`。
- 第三方开源 skills 不直接默认安装；必须先进入 `skills/registry.json`，记录来源、版本、许可证、权限边界和审计状态。
- registry 使用 JSON 而不是 YAML，原因是当前项目坚持 Python 标准库实现，避免引入 PyYAML 依赖。

## 内置 core skills

当前 core profile 包含：

- `agent-docs-bootstrap`：初始化或修复项目级 Agent 协作文档。
- `template-maintainer`：维护 `templates/agent-docs/` 和生成文档契约。
- `skill-author`：创建、更新或审查 Agent Skill。
- `bug-fix-recorder`：修复问题后沉淀 `.claude/bug-fix-log.md`。
- `repo-onboarding`：进入陌生仓库时做事实型项目梳理。
- `security-boundary-review`：审查脚本、安装器、skill 和外部服务安全边界。
- `release-packaging`：维护安装脚本、发布包和安装验证。
- `agent-handoff`：把完成或暂停的 Agent 工作整理成交接摘要。

这些 skills 必须保持无外部网络、无账号依赖、无第三方代码。若未来某个 core skill 需要脚本或网络访问，应先从 core 中移出或显式记录权限变化。

## 推荐结构

每个 skill 建议使用以下结构：

```text
skills/<skill-name>/
├── SKILL.md
├── scripts/
├── templates/
└── references/
```

只有在确实需要时才创建 `scripts/`、`templates/` 和 `references/`。

## `SKILL.md` 推荐内容

```markdown
# Skill Name

## 何时使用

说明触发条件、适用任务和不适用场景。

## 输入

说明需要用户提供的信息、可从仓库读取的信息，以及必须确认的风险点。

## 工作流

按顺序列出执行步骤。步骤应可操作，不写空泛原则。

## 输出

说明最终交付物、文件位置、报告格式或命令结果。

## 验证

说明如何检查结果是否正确。

## 风险与边界

说明权限、数据、网络、外部服务和破坏性操作边界。
```

## 命名规范

- skill 目录名使用小写短横线：`release-notes`、`bug-diagnosis`。
- 脚本文件名描述动作：`collect_context.py`、`render_report.ts`。
- 模板文件名描述用途：`pr-description.md`、`incident-review.md`。

## 编写原则

- 触发条件必须具体，避免“任何时候都可使用”的描述。
- 工作流使用命令式步骤，避免只有理念没有操作。
- 能用仓库上下文判断的事情，不要求用户重复提供。
- 涉及修改文件、提交、推送、发布、删除数据时，必须写清楚前置检查。
- 对不确定或高风险步骤，明确要求先停下来确认。

## 质量检查

新增或修改 skill 后，至少检查：

- 是否能从 `AGENTS.md` 或 `.claude/README.md` 找到相关说明。
- 是否已同步 `skills/registry.json` 中的 profile、权限和审计状态。
- 是否存在清晰的触发条件和不适用场景。
- 是否说明了输入、输出和验收标准。
- 是否避免硬编码个人路径、密钥、账号或临时状态。
- 是否把大段可复用内容放入模板或脚本，而不是堆在主说明里。

## 示例 skill 骨架

```markdown
# Example Skill

## 何时使用

当用户需要完成某类重复任务，并且该任务有稳定输入、流程和输出时使用。

## 工作流

1. 读取项目上下文。
2. 确认任务范围和风险点。
3. 执行必要命令或文件修改。
4. 验证结果。
5. 汇报变更、验证方式和后续建议。

## 输出

提供修改文件、验证命令和关键结论。
```
