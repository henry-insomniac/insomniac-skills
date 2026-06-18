# Local Agent Workspace

`.scratch/` 用于保存 `{{PROJECT_NAME}}` 的本地 Markdown issue、PRD 和任务拆分记录。

## 目录约定

```text
.scratch/
└── <feature>/
    ├── PRD.md
    └── issues/
        └── 01-<topic>.md
```

## 维护规则

- 一个需求、修复或项目切片使用一个 `<feature>` 目录。
- PRD 写入对应目录的 `PRD.md`。
- 可执行 issue 写入 `issues/`，文件名前缀使用两位序号。
- issue 顶部使用 `Status:` 标记 triage 状态。
- 对话补充、决策变化和验收反馈追加到 `## Comments`。
