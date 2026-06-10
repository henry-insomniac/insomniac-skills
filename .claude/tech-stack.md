# 技术栈与技术规范

## 当前状态

仓库当前以 Markdown 模板和 Python 标准库脚本为主，暂无外部运行时依赖、包管理器、测试框架或构建系统。

## 文档规范

- 主要文档使用 Markdown。
- 中文为主，命令、文件名、API、包名保留英文原文。
- 文件名使用小写短横线，顶层约定文件除外，例如 `AGENTS.md`。
- 文档标题层级从一个一级标题开始，不跳级。
- 命令、路径、环境变量使用反引号标记。

## 模板目录规范

- 脚手架模板位于 `templates/agent-docs/`。
- 模板中的路径结构应和目标项目输出结构一致。
- 模板支持 `{{PROJECT_NAME}}`、`{{PROJECT_DESCRIPTION}}` 和 `{{DATE}}`。
- 新增占位符必须同步更新 `scripts/init_agent_docs.py` 和 `README.md`。
- 模板内容应保持通用，不写入单个项目、账号或个人机器的真实细节。
- 初始化脚本会跳过 `.DS_Store`、`._*` 和 `__pycache__`，避免本地系统元数据污染输出。

## 脚本规范

当前初始化脚本为 `scripts/init_agent_docs.py`，仅使用 Python 标准库。

`install.sh` 是 curl 安装入口，使用 POSIX shell 编写，依赖 `python3`，下载阶段需要 `curl` 或 `wget`。

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
python3 scripts/init_agent_docs.py --target /tmp/agent-docs-test --project-name demo --description "一个测试项目" --force
python3 scripts/init_agent_docs.py --target /tmp/agent-docs-test --project-name demo --dry-run
sh install.sh
```

后续引入脚本或代码后，应补充对应验证命令，例如：

```bash
python -m pytest
npm test
npm run lint
```

实际命令以项目最终工具链为准。
