# 项目架构

## 项目定位

`insomniac-skills` 面向项目级 Agent 协作文档的初始化。它不是业务应用仓库，而是一个脚手架仓库，重点关注：

- 把 `AGENTS.md` 与 `.claude` 长期上下文整理为可复用模板。
- 为任意项目快速初始化架构、bug、Git 和技术规范文档。
- 默认保护目标项目已有文件，避免脚手架误覆盖项目上下文。
- 为 Codex/Claude 类 Agent 提供清晰入口，降低协作成本。

可选 skill 安装层的架构图见 `skill-install-architecture.svg`。

## 建议目录结构

```text
.
├── AGENTS.md
├── README.md
├── .claude/
│   ├── README.md
│   ├── project-architecture.md
│   ├── skill-authoring.md
│   ├── bug-fix-log.md
│   ├── git-collaboration.md
│   └── tech-stack.md
├── scripts/
│   └── init_agent_docs.py
├── skills/
│   ├── registry.json
│   └── core/
├── server/
│   └── insomniac_skills_analytics.py
└── templates/
    └── agent-docs/
        ├── AGENTS.md
        └── .claude/
            ├── README.md
            ├── project-architecture.md
            ├── bug-fix-log.md
            ├── git-collaboration.md
            └── tech-stack.md
```

## 目录职责

### `AGENTS.md`

Agent 入口文件。用于说明项目目标、协作原则和关键文档索引。任何 Agent 开始工作前都应先阅读该文件。

### `.claude/`

项目长期上下文目录。这里保存架构、规范、协作流程和故障记录，避免重要信息散落在对话或临时笔记中。

### `README.md`

脚手架的人类使用入口。说明初始化命令、覆盖策略、模板位置和维护方式。

### `scripts/init_agent_docs.py`

初始化 CLI。负责读取模板、替换占位符，并写入目标项目。默认只初始化协作文档；当用户显式传入 `--with-skills` 时，才会把 registry 中的本地 skills 写入目标项目 `.agents/skills/`。

当前支持的 skill 相关参数：

- `--list-skills`：列出可用 profile 和 skill。
- `--with-skills PROFILE_OR_SKILL`：安装指定 profile 或单个 skill，可重复传入。
- `--skills-dir PATH`：指定 registry 和 skill 源目录。

已有文件默认跳过，`--force` 才覆盖。

### `skills/`

可选 skill 分发目录。它不是默认输出内容，只有用户显式选择 profile 或 skill 时才写入目标项目。

- `skills/registry.json`：记录 profile、skill 来源、版本、许可证、适用 Agent surface、权限边界和审计状态。
- `skills/core/`：本项目维护的项目级 Agent 协作基础 skills，无外部网络、无账号依赖、无第三方代码。

### `templates/agent-docs/`

脚手架输出模板。模板应保持项目通用，避免写死本仓库或个人机器的细节。

### `server/insomniac_skills_analytics.py`

服务器端发布与统计服务。它负责：

- 返回 `install.sh`。
- 返回 `insomniac-skills.tar.gz`。
- 记录安装脚本调用量和安装包下载量。
- 根据调用 IP 缓存归属地信息。
- 提供 `/insomniac-skills/dashboard` 可视化看板。

## 公网安全策略

- 安装脚本和安装包保持公开，方便 `curl | bash` 使用。
- nginx 对 `/insomniac-skills/install.sh` 和 `/insomniac-skills/insomniac-skills.tar.gz` 做 IP 级限流。
- nginx 对 dashboard 做 Basic Auth，凭据保存在服务器 `/root/insomniac-skills-dashboard-credentials.txt`。
- nginx 拒绝非 `GET` / `HEAD` 请求。
- analytics 服务只监听 `127.0.0.1:18084`，不直接暴露公网。
- SQLite 事件表最多保留 20,000 条、最多 180 天，避免恶意请求撑爆磁盘。
- dashboard 只展示脱敏 IP，完整 IP 仅用于归属地解析和独立 IP 统计。

## 初始化流程

1. 用户指定目标项目目录、项目名和项目描述。
2. `scripts/init_agent_docs.py` 读取 `templates/agent-docs/`。
3. 脚本替换 `{{PROJECT_NAME}}`、`{{PROJECT_DESCRIPTION}}` 和 `{{DATE}}`。
4. 脚本写入 `AGENTS.md` 和 `.claude/*`。
5. 若目标文件已存在，默认跳过；传入 `--force` 时才覆盖。

## 扩展原则

- 模板先保持通用，再由目标项目补充真实技术细节。
- 默认不覆盖已有文件，覆盖必须显式开启。
- 脚手架只初始化长期上下文，不替目标项目推断不存在的架构。
- 新增模板占位符时，必须同步更新脚本和 `README.md`。
- 对外部工具、账号、网络、密钥有依赖的流程必须写明前置条件和失败处理。
- 第三方开源 skills 不默认安装；必须先进入 registry，记录来源、版本、许可证、权限边界和审计状态，再通过显式 profile 或 skill 名称安装。

## 架构变更记录

| 日期 | 变更 | 原因 | 验证 |
| --- | --- | --- | --- |
| 2026-06-10 | 初始化项目文档结构 | 建立 Agent 协作和 skill 维护基线 | 已创建 `AGENTS.md` 与 `.claude` 文档 |
| 2026-06-10 | 增加 Agent 文档脚手架 | 支持初始化任意项目的 `AGENTS.md` 和 `.claude` 文档 | 已创建模板目录与初始化脚本 |
| 2026-06-10 | 增加 curl 安装和统计看板 | 使用域名安装入口，记录调用量和 IP 归属地 | 已部署 nginx 转发、systemd 服务和 dashboard |
| 2026-06-10 | 增加可选 core skills 分发层 | 在不改变默认安全行为的前提下支持安装项目级 Agent 协作 skills | 已新增 `skills/registry.json`、`skills/core/` 和 CLI skill 参数 |
