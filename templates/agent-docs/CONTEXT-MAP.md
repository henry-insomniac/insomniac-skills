# {{PROJECT_NAME}} Context Map

`{{PROJECT_NAME}}`：{{PROJECT_DESCRIPTION}}

本文件用于多上下文项目。Agent 应先阅读本文件，再按任务范围进入对应的 `CONTEXT.md`。

## 上下文索引

| 上下文 | 路径 | 说明 |
| --- | --- | --- |
| 待补充 | `path/to/context/CONTEXT.md` | 待补充 |

## 全局规则

- 根目录 `.claude/` 保存项目级长期协作上下文。
- `docs/adr/` 保存跨上下文架构决策。
- 各上下文目录可维护自己的 `CONTEXT.md` 和 `docs/adr/`。
- Agent 应只读取和当前任务相关的上下文，避免把一个模块的术语误套到另一个模块。
