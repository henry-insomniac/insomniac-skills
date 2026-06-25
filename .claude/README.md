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
- 调整可安装 skill profile 或 registry 字段时，同步更新 `skill-authoring.md`、`README.md` 和 `README.zh-CN.md`。
- 调整初始化 CLI 参数、模板占位符或输出结构时，同步更新 `project-architecture.md`、`tech-stack.md`、`README.md` 和 `README.zh-CN.md`。
- 调整 `DESIGN.md` 模板、`--with-design` 参数或设计系统输出规则时，同步更新 `project-architecture.md`、`tech-stack.md`、`README.md`、`README.zh-CN.md` 和测试。
- 调整 npm wrapper、`package.json`、包内容白名单或发布脚本时，同步更新 `project-architecture.md`、`tech-stack.md`、`README.md`、`README.zh-CN.md` 和 npm wrapper 测试。
- 调整 GitHub Pages 开源项目主页时，同步更新 `project-architecture.md`、`tech-stack.md` 和站点验证记录。
- 修复 bug 后，同步更新 `bug-fix-log.md`。
- 调整协作流程时，同步更新 `git-collaboration.md`。
- 引入新语言、运行时、包管理器、测试框架或格式化工具时，同步更新 `tech-stack.md`。

## 当前状态

仓库当前已具备基础脚手架能力：

- `templates/agent-docs/` 保存输出模板。
- `scripts/init_agent_docs.py` 负责把模板初始化到目标项目。
- `bin/init-agent-docs.js` 和 `bin/insomniac-skills.js` 提供 npm package 的 CLI wrapper，调用同一份 Python 初始化脚本；`isk init` 是推荐短入口。
- `package.json` 保存 npm 包名、英文 description、bin 映射、打包白名单和维护脚本。
- `docs/` 保存 GitHub Pages 静态项目主页。
- `.github/workflows/pages.yml` 负责把 `docs/` 部署到 GitHub Pages。
- `tests/` 通过 CLI 集成测试验证初始化输出结构。
- `--with-design` 可选生成根目录 `DESIGN.md`，并在 Agent 入口和长期上下文索引中加入 UI 任务读取提示。
- `--with-agent-ops` 可选生成 `docs/agents/`、`CONTEXT.md` / `CONTEXT-MAP.md`、`docs/adr/` 和本地 `.scratch/` 工作区说明。
- `skills/core/` 保存本项目维护的可选 core skills。
- `skills/registry.json` 保存可安装 skill 和 profile 元数据。
- `README.md` 提供英文 GitHub/npm 主入口，并链接 `README.zh-CN.md` 中文文档。
