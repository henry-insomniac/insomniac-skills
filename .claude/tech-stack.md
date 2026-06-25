# 技术栈与技术规范

## 当前状态

仓库当前以 Markdown 模板、JSON registry、Python 标准库脚本和 Python `unittest` 集成测试为主。npm 仅作为分发 wrapper，核心脚手架逻辑仍由 `scripts/init_agent_docs.py` 实现。

## 文档规范

- 主要文档使用 Markdown。
- 项目长期上下文文档中文为主，命令、文件名、API、包名保留英文原文。
- 根 `README.md` 是 GitHub/npm 默认展示的英文主文档，必须链接 `README.zh-CN.md`；中文版本维护在 `README.zh-CN.md`。
- 文件名使用小写短横线，顶层约定文件除外，例如 `AGENTS.md`。
- 文档标题层级从一个一级标题开始，不跳级。
- 命令、路径、环境变量使用反引号标记。

## 模板目录规范

- 脚手架模板位于 `templates/agent-docs/`。
- 模板中的路径结构应和目标项目输出结构一致。
- 模板支持 `{{PROJECT_NAME}}`、`{{PROJECT_DESCRIPTION}}`、`{{DATE}}`、`{{AGENT_SKILLS_BLOCK}}`、`{{DESIGN_GUIDANCE_BLOCK}}`、`{{DESIGN_ARCHITECTURE_BLOCK}}`、`{{DESIGN_TECH_STACK_BLOCK}}`、`{{ISSUE_TRACKER_CONTENT}}` 和 `{{DOMAIN_DOCS_CONTENT}}`。
- 新增占位符必须同步更新 `scripts/init_agent_docs.py`、`README.md` 和 `README.zh-CN.md`。
- 模板内容应保持通用，不写入单个项目、账号或个人机器的真实细节。
- 初始化脚本会跳过 `.DS_Store`、`._*` 和 `__pycache__`，避免本地系统元数据污染输出。
- `DESIGN.md` 属于可选设计系统入口，默认不写入；启用 `--with-design` 后生成，并在入口文档中加入 UI 任务读取提示。
- `docs/agents/`、`CONTEXT.md`、`CONTEXT-MAP.md`、`docs/adr/README.md` 和 `.scratch/README.md` 属于可选 Agent 操作规则层，默认不写入；启用 `--with-agent-ops` 后按参数选择性生成。

## Skill registry 规范

- 可安装 skills 位于 `skills/`。
- `skills/registry.json` 使用 JSON，便于 `scripts/init_agent_docs.py` 只依赖 Python 标准库读取。
- 本地 skill 来源相对 `skills/` 目录解析，使用 `local:<skills-dir-relative-path>`，例如 `local:core/agent-docs-bootstrap`。
- registry 条目必须记录 `name`、`profile`、`source`、`version`、`license`、`surfaces`、`permissions`、`checksum` 和 `audit_status`。
- 第三方 skills 必须锁定版本或 commit，并在安装前审计脚本、网络访问、文件写入、凭据读取和许可证。

## 脚本规范

当前初始化脚本为 `scripts/init_agent_docs.py`，仅使用 Python 标准库。

`install.sh` 是 curl 安装入口，使用 POSIX shell 编写，依赖 `python3`，下载阶段需要 `curl` 或 `wget`。

`bin/init-agent-docs.js` 和 `bin/insomniac-skills.js` 是 npm CLI wrapper，使用 Node.js 标准库调用 `scripts/init_agent_docs.py`。`isk init` 是推荐短入口，`insomniac-skills init-agent-docs` 和 `init-agent-docs` 是兼容入口。wrapper 不应复制模板渲染、skills 安装或 issue tracker 检测逻辑；共享执行逻辑应放在 `bin/run-init-agent-docs.js`。

`package.json` 负责 npm 包名、英文 `description`、`bin` 映射、`files` 白名单、MIT license 元数据和维护脚本。npm 包不应包含 `server/`、`tests/`、curl 安装脚本或部署凭据。`README.md` 和 `README.zh-CN.md` 都应进入 `files` 白名单。

`docs/` 是 GitHub Pages 静态站点，使用原生 HTML/CSS，不需要前端构建工具。`.github/workflows/pages.yml` 使用 GitHub 官方 Pages Actions 部署该目录。

服务器发布入口使用 `https://yi-flow.com/insomniac-skills/install.sh`。安装统计服务位于 `server/insomniac_skills_analytics.py`，部署后由 nginx 将 `/insomniac-skills/` 转发到本机服务端口。

公网安全相关配置：

- nginx rate limit 配置位于 `/etc/nginx/conf.d/insomniac-skills-rate-limit.conf`。
- dashboard Basic Auth 文件位于 `/etc/nginx/.insomniac-skills-dashboard.htpasswd`。
- dashboard 明文凭据仅保存在服务器 `/root/insomniac-skills-dashboard-credentials.txt`。
- systemd 服务名为 `insomniac-skills-analytics.service`。

后续引入脚本时，优先遵守：

- 简单自动化优先使用 shell 或 Python。
- 需要类型约束、复杂 CLI 或与前端生态集成时再考虑 TypeScript。
- 脚本必须支持从仓库根目录运行，或在文档中明确工作目录。
- 脚本失败时应返回非零退出码，并输出可定位问题的信息。
- 不在脚本中硬编码个人绝对路径。

## 依赖规范

新增依赖前需要说明：

- 依赖解决什么问题。
- 是否已有系统工具或标准库可替代。
- 是否会增加安装、运行或维护成本。
- 是否需要网络、账号或密钥。

## 安全规范

- 不提交 `.env`、密钥、令牌、Cookie、账号凭据。
- 示例配置使用 `.env.example` 或文档片段，不使用真实值。
- 涉及外部 API 的 skill 必须说明鉴权方式和权限边界。
- 涉及文件删除、发布、推送、远程写入的操作必须有明确前置检查。

## 验证规范

在没有自动化测试前，文档变更至少执行：

```bash
git status --short
```

脚手架行为变更至少执行：

```bash
python3 -m unittest discover -s tests
python3 scripts/init_agent_docs.py --target /tmp/agent-docs-test --project-name demo --description "一个测试项目" --force
python3 scripts/init_agent_docs.py --target /tmp/agent-docs-test --project-name demo --description "一个测试项目" --with-design --force
python3 scripts/init_agent_docs.py --target /tmp/agent-docs-test --project-name demo --description "一个测试项目" --with-agent-ops --issue-tracker auto --domain-layout single --force
python3 scripts/init_agent_docs.py --target /tmp/agent-docs-test --project-name demo --description "一个测试项目" --with-agent-ops --issue-tracker --domain-layout single --force
python3 scripts/init_agent_docs.py --target /tmp/agent-docs-test --project-name demo --dry-run
python3 scripts/init_agent_docs.py --list-skills
python3 scripts/init_agent_docs.py --target /tmp/agent-docs-test --project-name demo --with-skills core --force
npm test
npm run pack:check
npm exec --package . -- isk init --help
npm exec --package . -- init-agent-docs --help
npm exec --package . -- insomniac-skills init-agent-docs --help
python3 -m http.server 4173 --directory docs
sh install.sh
```

如果当前环境允许临时访问 npm registry，可额外验证生成的设计系统结构：

```bash
npx @google/design.md lint /tmp/agent-docs-test/DESIGN.md
```

后续引入脚本或代码后，应补充对应验证命令，例如：

```bash
python -m pytest
npm test
npm run lint
```

实际命令以项目最终工具链为准。
