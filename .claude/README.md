# .claude 文档索引

`.claude` 目录保存本项目的长期上下文，供人类维护者和 Agent 在开发、排障、评审时快速理解项目约定。

## 文档列表

- `project-architecture.md`：项目定位、目录职责、脚手架结构和扩展原则。
- `skill-authoring.md`：skill 的编写格式、质量要求和常见模式。当前作为扩展参考保留。
- `bug-fix-log.md`：bug 修复记录、复盘模板和已知问题。
- `git-collaboration.md`：分支命名、提交信息、PR、评审和发布约定。
- `tech-stack.md`：当前技术栈、推荐工具链、脚本和文档规范。

## 维护规则

- 修改项目结构时，同步更新 `project-architecture.md`。
- 新增、删除或重命名 skill 时，同步更新 `skill-authoring.md` 中的相关约定或示例。
- 调整可安装 skill profile 或 registry 字段时，同步更新 `skill-authoring.md` 和 `README.md`。
- 调整初始化 CLI 参数、模板占位符或输出结构时，同步更新 `project-architecture.md`、`tech-stack.md` 和 `README.md`。
- 修复 bug 后，同步更新 `bug-fix-log.md`。
- 调整协作流程时，同步更新 `git-collaboration.md`。
- 引入新语言、运行时、包管理器、测试框架或格式化工具时，同步更新 `tech-stack.md`。

## 当前状态

仓库当前已具备基础脚手架能力：

- `templates/agent-docs/` 保存输出模板。
- `scripts/init_agent_docs.py` 负责把模板初始化到目标项目。
- `tests/` 通过 CLI 集成测试验证初始化输出结构。
- `--with-agent-ops` 可选生成 `docs/agents/`、`CONTEXT.md` / `CONTEXT-MAP.md`、`docs/adr/` 和本地 `.scratch/` 工作区说明。
- `skills/core/` 保存本项目维护的可选 core skills。
- `skills/registry.json` 保存可安装 skill 和 profile 元数据。
- `README.md` 提供使用入口。
