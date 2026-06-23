# 项目架构

## 项目定位

`insomniac-skills` 面向项目级 Agent 协作文档的初始化。它不是业务应用仓库，而是一个脚手架仓库，重点关注：

- 把 `AGENTS.md`、`DESIGN.md` 与 `.claude` 长期上下文整理为可复用模板。
- 为任意项目快速初始化架构、bug、Git 和技术规范文档。
- 可选初始化根目录 `DESIGN.md`，让 UI 任务拥有独立的视觉系统入口。
- 可选初始化 `docs/agents/`、`CONTEXT.md` / `CONTEXT-MAP.md` 和 `docs/adr/`，让 Agent 明确 issue tracker、triage label 和领域文档读取规则。
- 通过 npm wrapper 暴露同一份 Python CLI，让用户可用 `npx` 或 `npm install -g` 调用脚手架。
- 通过 GitHub Pages 提供开源项目主页，集中说明功能、命令参数、npm 用法、Agent 层和 skill 列表。
- 默认保护目标项目已有文件，避免脚手架误覆盖项目上下文。
- 为 Codex/Claude 类 Agent 提供清晰入口，降低协作成本。

可选 skill 安装层的架构图见 `skill-install-architecture.svg`。

## 建议目录结构

```text
.
├── AGENTS.md
├── DESIGN.md
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
├── .claude/
│   ├── README.md
│   ├── project-architecture.md
│   ├── skill-authoring.md
│   ├── bug-fix-log.md
│   ├── git-collaboration.md
│   └── tech-stack.md
├── tests/
│   └── test_init_agent_docs.py
├── scripts/
│   └── init_agent_docs.py
├── skills/
│   ├── registry.json
│   └── core/
├── server/
│   └── insomniac_skills_analytics.py
└── templates/
    └── agent-docs/
        ├── CONTEXT.md
        ├── CONTEXT-MAP.md
        ├── AGENTS.md
        ├── DESIGN.md
        ├── .scratch/
        │   └── README.md
        ├── docs/
        │   ├── agents/
        │   │   ├── README.md
        │   │   ├── issue-tracker.md
        │   │   ├── triage-labels.md
        │   │   ├── domain.md
        │   │   └── skill-usage.md
        │   └── adr/
        │       └── README.md
        └── .claude/
            ├── README.md
            ├── project-architecture.md
            ├── skill-authoring.md
            ├── bug-fix-log.md
            ├── git-collaboration.md
            └── tech-stack.md
```

## 目录职责

### `AGENTS.md`

Agent 入口文件。用于说明项目目标、协作原则和关键文档索引。任何 Agent 开始工作前都应先阅读该文件。

### `DESIGN.md`

可选的视觉系统入口。只有用户显式传入 `--with-design` 时才写入目标项目根目录。用于把颜色、字体、间距、圆角、组件样式和设计禁用项整理成 Agent 可读取的 UI 约束。

### `.claude/`

项目长期上下文目录。这里保存架构、规范、协作流程和故障记录，避免重要信息散落在对话或临时笔记中。

### `README.md`

脚手架的人类使用入口。说明初始化命令、覆盖策略、模板位置和维护方式。

### `package.json`

npm 分发入口。记录包名、版本、`bin` 命令映射、打包白名单和维护脚本。npm 包只应包含运行所需文件，不包含 `server/`、`tests/` 或 curl 安装脚本。

### `bin/init-agent-docs.js`

npm CLI wrapper。它不重新实现脚手架逻辑，只负责查找并调用 `scripts/init_agent_docs.py`，把参数原样传给 Python CLI。这样 npm、curl 和仓库内运行共享同一份核心实现。

### `docs/`

GitHub Pages 静态站点。用于对外介绍项目能力、npm 命令、完整参数、Agent 文档层、`DESIGN.md` 入口和 core skills 列表。该目录是开源项目主页，不参与 npm 包内容白名单。

### `.github/workflows/pages.yml`

GitHub Pages 部署 workflow。它在 `main` 分支上 `docs/**` 或 workflow 本身变更时，把 `docs/` 上传为 Pages artifact 并部署。

### `scripts/init_agent_docs.py`

初始化 CLI。负责读取模板、替换占位符，并写入目标项目。默认只初始化协作文档；当用户显式传入 `--with-skills` 时，才会把 registry 中的本地 skills 写入目标项目 `.agents/skills/`。

当前支持的初始化参数：

- `--with-design`：生成根目录 `DESIGN.md`，并在 `AGENTS.md` 与 `.claude/README.md` 中加入 UI 任务读取提示。
- `--with-agent-ops`：生成 `docs/agents/*`、`docs/adr/README.md`，并根据领域布局生成 `CONTEXT.md` 或 `CONTEXT-MAP.md`。
- `--issue-tracker manual|auto|github|gitlab|local`：生成 issue tracker 操作规则。`auto` 读取目标项目 `.git/config`，检测 GitHub 或 GitLab remote；`local` 额外生成 `.scratch/README.md`。
- `--domain-layout single|multi|claude-only`：选择领域上下文布局。`single` 生成 `CONTEXT.md`，`multi` 生成 `CONTEXT-MAP.md`，`claude-only` 只依赖 `AGENTS.md` 和 `.claude/`，不生成 `CONTEXT*`。

当前支持的 skill 安装参数：

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

其中 `docs/agents/` 参考 `setup-matt-pocock-skills` 的配置分层，但按本项目约定改写为中文、默认安全、兼容 `.claude/` 的 Agent 操作规则层。

### `tests/`

CLI 集成测试目录。测试通过 `python3 scripts/init_agent_docs.py` 的公共接口验证输出结构，不依赖脚本内部实现细节。

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
3. 脚本替换项目基础占位符和 Agent 操作规则动态占位符。
4. 如果启用 `--with-design`，脚本写入根目录 `DESIGN.md`，并渲染设计系统读取提示。
5. 如果启用 `--with-agent-ops`，脚本根据 `--issue-tracker` 和 `--domain-layout` 选择性写入 `docs/agents/*`、`docs/adr/README.md`、`CONTEXT.md`、`CONTEXT-MAP.md` 或 `.scratch/README.md`。
6. 脚本写入 `AGENTS.md` 和 `.claude/*`。
7. 若目标文件已存在，默认跳过；传入 `--force` 时才覆盖。

## npm 发布流程

1. 维护者更新 `scripts/init_agent_docs.py`、模板、skills 或 wrapper。
2. 运行 Python CLI 集成测试和 npm wrapper 测试。
3. 运行 `npm pack --dry-run --json`，确认包内容只包含运行所需文件。
4. 运行 `npm exec --package . -- init-agent-docs --help`，确认本地 npm 包入口可执行。
5. 登录 npm 后执行 `npm publish`。

当前 npm 包名规划为 `insomniac-skills`，CLI 命令名为 `init-agent-docs`。如果 npm registry 上包名被占用，应优先改包名而不是改命令名。

## GitHub Pages 发布流程

1. 修改 `docs/index.html`、`docs/styles.css` 或 `docs/assets/*`。
2. 本地检查静态页面链接、布局和命令文本。
3. 推送 `main` 后由 `.github/workflows/pages.yml` 自动部署。
4. 项目主页预期地址为 `https://henry-insomniac.github.io/insomniac-skills/`，实际地址以 GitHub Pages workflow 输出为准。

## 扩展原则

- 模板先保持通用，再由目标项目补充真实技术细节。
- `DESIGN.md` 模板只提供原创通用视觉基线，不内置第三方品牌、私有设计资产或真实业务细节。
- npm wrapper 必须保持薄层，不复制 Python CLI 逻辑，避免 npm 和 curl 入口行为漂移。
- GitHub Pages 站点只展示公开项目能力，不写入私有部署路径、账号、dashboard 凭据或服务器细节。
- 默认不覆盖已有文件，覆盖必须显式开启。
- 脚手架只初始化长期上下文，不替目标项目推断不存在的架构。
- Agent 操作规则层可以检测 GitHub/GitLab remote，但不会在默认 manual 模式假设 issue tracker。
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
| 2026-06-18 | 增加 Agent 操作规则层初始化 | 参考 `setup-matt-pocock-skills`，让目标项目明确 issue tracker、triage label 和领域文档读取规则 | 已新增 CLI 集成测试和 `--with-agent-ops` 参数 |
| 2026-06-23 | 增加可选 `DESIGN.md` 输出 | 为 UI 任务提供独立视觉系统入口，同时保持默认脚手架通用 | 已新增 `--with-design`、模板和 CLI 集成测试 |
| 2026-06-23 | 增加 npm wrapper 和 package 元数据 | 支持通过 npm/npx 使用同一份 Python CLI | 已新增 package metadata、Node wrapper、npm pack 和 npm exec 测试 |
| 2026-06-23 | 增加 GitHub Pages 开源项目主页 | 对外展示功能、命令参数、Agent 层和 skill 列表 | 已新增 `docs/` 静态站点和 Pages workflow |
