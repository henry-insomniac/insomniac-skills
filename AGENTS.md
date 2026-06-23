# Insomniac Skills Agent Guide

## 项目概述

`insomniac-skills` 是一个用于初始化项目级 Agent 协作文档的脚手架仓库。项目目标是把 `AGENTS.md`、`DESIGN.md`、`.claude` 长期上下文、架构说明、bug 修复记录、Git 协作规范和技术规范整理成可复用模板，让新项目可以快速建立一致的 Agent 协作基线。

当前仓库提供模板目录、初始化脚本、curl 安装入口和 npm wrapper。修改脚手架输出内容时，应优先修改 `templates/agent-docs/`；修改初始化行为时，更新 `scripts/init_agent_docs.py`；修改 npm 分发入口时，更新 `bin/init-agent-docs.js` 和 `package.json`。

## 详情索引

项目级细节统一维护在 `.claude` 目录：

- `.claude/README.md`：文档索引和维护规则。
- `.claude/project-architecture.md`：项目架构、目录职责和扩展方式。
- `.claude/skill-authoring.md`：skill 编写规范、结构建议和质量标准。
- `.claude/bug-fix-log.md`：bug 修复记录和复盘模板。
- `.claude/git-collaboration.md`：分支、提交、PR 和代码评审规范。
- `.claude/tech-stack.md`：项目相关技术栈、工具链和文档规范。

## 脚手架使用

curl 安装：

```bash
curl -fsSL https://yi-flow.com/insomniac-skills/install.sh | bash
```

系统级安装：

```bash
curl -fsSL https://yi-flow.com/insomniac-skills/install.sh | sudo bash
```

在本仓库中运行：

```bash
python3 scripts/init_agent_docs.py \
  --target /path/to/project \
  --project-name my-project \
  --description "一个示例项目"
```

默认不会覆盖目标项目已有文件。如需覆盖，显式添加 `--force`。预览写入内容可使用 `--dry-run`。

## Agent 工作原则

- 先阅读本文件和 `.claude/README.md`，再修改项目结构或新增规范。
- 新增或调整 skill 时，同步更新对应的架构说明、技术规范和必要示例。
- 新增或调整 `DESIGN.md` 输出时，同步更新模板、初始化脚本、README、架构说明和测试。
- 新增或调整 npm 包发布入口时，同步运行 wrapper 测试、`npm pack --dry-run --json` 和 npm exec 验证。
- 新增或调整 GitHub Pages 站点时，同步更新 `docs/`、`.github/workflows/pages.yml`、架构说明和技术规范。
- 保持改动聚焦，避免把无关重构、格式化或命名调整混入同一个变更。
- 记录重要决策的原因，尤其是目录结构、skill 接口、依赖工具和协作流程的变化。
- 修复问题后更新 `.claude/bug-fix-log.md`，包含现象、原因、修复方式和验证结果。

## 目录约定

建议目录演进方向：

```text
.
├── AGENTS.md
├── DESIGN.md
├── .claude/
│   ├── README.md
│   ├── project-architecture.md
│   ├── skill-authoring.md
│   ├── bug-fix-log.md
│   ├── git-collaboration.md
│   └── tech-stack.md
├── README.md
├── package.json
├── .github/
│   └── workflows/
│       └── pages.yml
├── bin/
│   └── init-agent-docs.js
├── docs/
│   ├── index.html
│   ├── styles.css
│   └── assets/
├── scripts/
│   └── init_agent_docs.py
└── templates/
    └── agent-docs/
        ├── AGENTS.md
        ├── DESIGN.md
        └── .claude/
```

在目录尚未实际创建前，不要假设它们存在。新增目录时应同时说明职责和维护方式。

## 维护要求

- 文档使用中文为主，必要的命令、文件名、API 名称保持英文原文。
- 模板应保持通用，不写入只适用于单个项目的真实路径、账号或业务细节。
- 初始化脚本应默认保护目标项目已有文件，覆盖行为必须显式开启。
- 引入外部依赖前，先说明用途、替代方案和维护成本。
- 涉及用户数据、密钥、账号状态或外部服务的流程，必须显式写出安全边界。
