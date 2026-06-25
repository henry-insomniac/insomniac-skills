# Bug 修复记录

本文件用于记录重要 bug、回归、排障结论和修复验证。轻微拼写或纯格式调整不需要记录。

## 记录模板

```markdown
## YYYY-MM-DD - 问题标题

### 现象

用户或系统看到的具体问题。

### 影响

说明影响范围、严重程度和是否阻塞主要流程。

### 原因

定位到的根因。避免只写“逻辑错误”。

### 修复

说明改了什么文件、什么逻辑，以及为什么这样修。

### 验证

列出执行过的命令、手动检查或回归测试。

### 后续

可选。记录需要补充的测试、文档或重构。
```

## 修复记录

## 2026-06-26 - npm 发布拒绝覆盖已发布版本

### 现象

执行 `npm publish` 时，npm 报错：`You cannot publish over the previously published versions: 0.1.5.`。

### 影响

GitHub 已包含新的英文 README、中文 README 和 npm description，但 npm registry 仍停留在 `0.1.5`，导致 npm 页面和安装包元数据没有更新。

### 原因

`0.1.5` 已经发布到 npm registry。npm 版本是不可覆盖的，同一个版本号不能再次发布，即使包内容发生了变化。

### 修复

将 `package.json` 版本从 `0.1.5` 提升到 `0.1.6`，作为 README 双语拆分和 npm description 更新的发布版本。

### 验证

- `npm view insomniac-skills versions --json`
- `git diff --check`
- `npm test`
- `npm run pack:check`

### 后续

当前机器执行 `npm whoami` 返回 `E401 Unauthorized`，需要恢复 npm 登录后再执行 `npm publish`。

## 2026-06-23 - CLI 命令和常用参数过长

### 现象

初始化命令需要输入 `insomniac-skills init-agent-docs --project-name ... --description ... --with-design --issue-tracker --with-agent-ops`，单词过长，不便记忆和日常使用。

### 影响

脚手架虽然可用，但高频入口不够顺手，用户容易输错命令或混淆包名、子命令和参数名。

### 原因

CLI 只暴露了描述性长命令和长参数，没有为高频路径提供短别名。

### 修复

更新 CLI：

- 新增 npm bin `isk`，作为推荐短入口。
- `insomniac-skills` wrapper 新增 `init` 子命令，等同 `init-agent-docs`。
- `scripts/init_agent_docs.py` 新增短参数：`--name`、`--desc`、`--design`、`--issues`、`--ops`。
- 保留 `insomniac-skills init-agent-docs`、`init-agent-docs` 和所有原长参数。
- 同步更新 README、站点参数展示、架构说明、技术栈说明和测试。

### 验证

- RED：`python3 -m unittest tests.test_init_agent_docs.InitAgentDocsNpmWrapperTests.test_package_wrapper_dispatches_short_init_command`
- RED：`python3 -m unittest tests.test_init_agent_docs.InitAgentDocsNpmWrapperTests.test_npm_exec_runs_short_package_command`
- RED：`python3 -m unittest tests.test_init_agent_docs.InitAgentDocsCliTests.test_short_init_options_generate_design_and_agent_ops_docs`
- GREEN：完整测试和 npm 打包验证。

## 2026-06-23 - npm 全局安装后缺少包名主命令

### 现象

执行 `npm install -g insomniac-skills` 后，用户运行 `insomniac-skills init-agent-docs ...`，zsh 报错：`command not found: insomniac-skills`。

### 影响

虽然 npm 包已安装并暴露 `init-agent-docs` 直接命令，但用户按包名调用主命令时无法使用脚手架，造成安装成功但命令不可用的体验。

### 原因

`package.json` 的 `bin` 只注册了 `init-agent-docs`，没有注册 `insomniac-skills`。文档也只说明直接命令，没有覆盖用户自然尝试的包名主命令。

### 修复

更新 npm wrapper：

- 新增 `bin/insomniac-skills.js`，支持 `insomniac-skills init-agent-docs ...`。
- 新增 `bin/run-init-agent-docs.js`，让包名主命令和直接命令共享同一份 Python CLI 调用逻辑。
- 保留 `init-agent-docs ...` 直接命令。
- 在 `package.json` 中注册 `insomniac-skills` bin，并将版本更新到 `0.1.4`。
- 同步更新 README、站点参数展示、架构说明、技术栈说明和 npm wrapper 测试。

### 验证

- `python3 -m unittest tests/test_init_agent_docs.py`
- `npm pack --dry-run --json`
- `npm exec --package . -- insomniac-skills init-agent-docs --help`

## 2026-06-23 - 裸 `--issue-tracker` 参数无法解析

### 现象

执行 `npx -p insomniac-skills init-agent-docs --project-name btc-center --description "BTC信息聚合" --with-design --issue-tracker --with-agent-ops` 时，CLI 报错：`argument --issue-tracker: expected one argument`。

### 影响

用户把 `--issue-tracker` 当作启用 issue tracker 文档的开关使用时，初始化流程被 argparse 阻断，无法生成 Agent 操作规则层。

### 原因

`scripts/init_agent_docs.py` 将 `--issue-tracker` 定义为必须带值的选项。虽然默认未传时仍是 `manual`，但显式传入裸参数时没有兼容为自动检测。

### 修复

更新 `scripts/init_agent_docs.py`：

- 为 `--issue-tracker` 增加 `nargs="?"`。
- 设置 `const="auto"`，让裸 `--issue-tracker` 等同 `--issue-tracker auto`。
- 保持不传 `--issue-tracker` 时默认仍为 `manual`。

同步更新 README、站点参数表、架构说明和技术栈验证命令。

### 验证

- `python3 -m py_compile scripts/init_agent_docs.py`
- `python3 -m unittest tests/test_init_agent_docs.py`
- 本地执行裸 `--issue-tracker` 初始化命令，确认可生成 `docs/agents/issue-tracker.md`。

## 2026-06-10 - 跳过 macOS 元数据模板文件

### 现象

将脚手架打包部署到 Linux 服务器后，执行 `init-agent-docs` 时报 `UnicodeDecodeError`。

### 影响

服务器端 CLI 无法完成初始化，阻塞全局部署后的使用。

### 原因

macOS 打包时可能携带 `.DS_Store`、`._*` 或缓存目录等系统元数据。初始化脚本递归读取模板目录中的所有文件，误把非模板元数据文件按 UTF-8 文本读取。

### 修复

更新 `scripts/init_agent_docs.py`：

- 跳过 `.DS_Store`。
- 跳过 `._*` AppleDouble 文件。
- 跳过 `__pycache__`。
- 显式使用 UTF-8 读写模板文件。

### 验证

- 本地执行 `python3 -m py_compile scripts/init_agent_docs.py`。
- 本地执行脚手架初始化临时目录，确认没有残留 `{{...}}` 占位符。
- 重新部署服务器后执行 `init-agent-docs --target /tmp/init-agent-docs-smoke --project-name smoke-project --description "一个服务器验证项目" --force`，确认生成成功。

## 已知风险

- 仓库当前处于初始化阶段，尚未建立自动化测试、格式化和 lint 流程。
- 后续新增可执行脚本后，需要补充对应的验证命令和失败处理规范。
