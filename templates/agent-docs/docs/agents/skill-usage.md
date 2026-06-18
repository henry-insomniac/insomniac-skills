# Skill Usage

本文件记录项目级 Agent skills 的使用方式和组合建议。

## 默认原则

- 优先遵守 `AGENTS.md` 和 `.claude/README.md` 中的项目级规则。
- 使用 skill 前先确认触发条件是否匹配当前任务。
- 涉及 issue、triage、PRD 或长期领域上下文时，先读取 `docs/agents/` 中的对应规则。
- 涉及用户数据、密钥、账号状态或外部服务时，必须先确认安全边界。

## 常见组合

- 新需求：先明确需求和公共接口，再生成 PRD 或 issue。
- Bug 修复：先复现和定位，再修复并更新 `.claude/bug-fix-log.md`。
- 架构调整：先读取 `.claude/project-architecture.md` 和相关 ADR，再提出方案。
- 测试优先开发：先确认可观察行为，再按 red-green-refactor 小步推进。
