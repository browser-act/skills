---
name: browser-act
description: "面向 AI Agent 的浏览器自动化 CLI，具备反检测隐身浏览、验证码破解和多浏览器并行能力。当用户需要与网站交互时使用，包括页面导航、填写表单、点击按钮、截图、数据提取、反爬网站抓取，或任何浏览器自动化任务。也适用于连接用户已有的 Chrome 会话、配置代理隐身浏览或运行并行浏览器会话。"
allowed-tools: Bash(browser-act:*)
metadata:
  author: BrowserAct
  version: "1.0.0"
---

# browser-act CLI 浏览器自动化

`browser-act` 是一个具备隐身和验证码破解能力的浏览器自动化 CLI。支持两种浏览器类型（Stealth 和 Real Chrome），提供导航、页面交互、数据提取、标签页/会话管理等命令。

所有命令默认输出人类可读的文本。使用 `--format json` 获取结构化 JSON 输出，适合 AI Agent 集成和脚本调用。

## 安装

```bash
# 已安装则升级，否则全新安装
uv tool upgrade browser-act-cli \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  --python 3.12 || uv tool install browser-act-cli \
  --index-url https://test.pypi.org/simple/ \
  --extra-index-url https://pypi.org/simple \
  --python 3.12
```

每次会话开始时运行此命令，确保使用最新版本。

**全局选项**（所有命令可用）：

| 选项 | 默认值 | 说明 |
|------|--------|------|
| `--session <name>` | `default` | 会话名称（隔离浏览器状态） |
| `--format <text\|json>` | `text` | 输出格式 |
| `--intent <desc>` | 无 | 调用方意图（用于分析） |
| `--no-auto-dialog` | 关闭 | 禁用 JavaScript 对话框自动处理（alert、confirm、prompt） |
| `--version` | | 显示版本 |
| `-h, --help` | | 显示帮助 |

## 认证

部分功能需要 BrowserAct API Key（Stealth 浏览器、验证码破解等）。Real Chrome 和基本页面操作无需 Key。

**方式一：交互式注册（推荐）**

```bash
# 第 1 步：获取注册链接
browser-act auth login
# 输出：注册 URL + 操作说明

# 第 2 步：检查注册状态（单次检查，不需要循环）
browser-act auth poll
# 成功返回 API Key，未完成则返回 pending 状态
```

**AI Agent 流程：** 调用 `auth login`，将注册链接展示给用户，然后每隔几秒调用 `auth poll` 直到返回成功。当剩余时间不足 10 分钟时，提醒用户尽快完成注册。

```bash
browser-act auth login
# → 向用户展示 URL，请求注册
browser-act auth poll  # 检查
browser-act auth poll  # 几秒后重试
browser-act auth poll  # ... 直到成功、过期或放弃
# ⚠ 剩余时间 < 10 分钟时提醒用户
```

**方式二：直接设置**

```bash
browser-act auth set <your_api_key>
```

**移除 API Key：**

```bash
browser-act auth clear
```

获取 API Key：https://www.browseract.com

**不需要**提前设置 API Key。当命令需要认证时，CLI 会返回包含设置说明的结构化错误。

## 浏览器选择

browser-act 支持两种浏览器类型，根据任务选择：

| 场景 | 使用 | 原因 |
|------|------|------|
| 目标网站有反爬/Bot 检测 | **Stealth** | 反检测指纹可绕过 Bot 检查 |
| 需要代理或隐私模式 | **Stealth** | Real Chrome 不支持 `--proxy` / `--mode` |
| 需要多个浏览器并行 | **Stealth** | 每个 Stealth 浏览器独立；创建多个并在不同会话中并行运行 |
| 需要用户日常浏览器的已有登录状态 | **Real Chrome** | 直接连接用户的 Chrome，使用已有 Cookie |
| 无 Bot 检测，无需登录 | 均可 | Stealth 更安全，Real Chrome 更简单 |

### Stealth 浏览器

带反检测指纹的本地浏览器，适合有 Bot 检测的网站。

```bash
# 创建
browser-act browser create "my-browser"
browser-act browser create "my-browser" --official-proxy US              # 官方代理（区域码，如 US、JP、DE）
browser-act browser create "my-browser" --proxy socks5://user:pass@host:port  # 自定义代理

# 更新
browser-act browser update <browser_id> --name "new-name"
browser-act browser update <browser_id> --proxy http://proxy:8080 --mode private

# 查看可用代理区域
browser-act browser regions                                 # 列出 --official-proxy 可用的区域码

# 列表 / 删除 / 清除 Profile
browser-act browser list                                    # 列出所有 Stealth 浏览器
browser-act browser list --page 2 --page-size 10            # 分页列表
browser-act browser delete <browser_id>
browser-act browser clear-profile <browser_id>
```

| 选项 | 说明 |
|------|------|
| `--desc` | 浏览器描述 |
| `--official-proxy <region>` | 官方代理，传入区域码（如 `US`、`JP`、`DE`）。**与 `--proxy` 互斥** |
| `--proxy <url>` | 自定义代理，需带协议（`http`、`https`、`socks4`、`socks5`），如 `socks5://user:pass@host:port`。**与 `--official-proxy` 互斥** |
| `--mode <normal\|private>` | `normal`（默认）：跨启动保留缓存、Cookie、登录状态。`private`：每次启动全新环境，不保存状态 |

Stealth 浏览器 `normal` 模式（默认）跨启动保留 Cookie、缓存和登录会话——登录一次即可复用，类似常规浏览器 Profile。

### Real Chrome

两种模式：自动连接运行中的 Chrome（默认），或使用 BrowserAct 托管的内核。

```bash
browser-act browser real open https://example.com                  # 自动连接运行中的 Chrome（已有登录/Cookie）
browser-act browser real open https://example.com --ba-kernel      # 使用 BrowserAct 提供的浏览器内核
```

两种浏览器类型都支持 `--headed` 显示浏览器界面（默认：无头模式），用于调试：

```bash
browser-act browser open <browser_id> https://example.com --headed
browser-act browser real open https://example.com --headed
browser-act browser real open https://example.com --ba-kernel --headed
```

## 核心工作流

每次浏览器自动化遵循此循环：**打开 → 检查 → 交互 → 验证**

1. **打开**：`browser-act browser open <browser_id> <url>`（Stealth）或 `browser-act browser real open <url>`（Real Chrome）
2. **检查**：`browser-act state` — 返回带索引编号的可交互元素
3. **交互**：使用 `state` 返回的索引（`browser-act click 5`、`browser-act input 3 "text"`）
4. **验证**：`browser-act state` 或 `browser-act screenshot` — 确认结果

```bash
# 示例：用户已提供凭证并要求你登录
browser-act browser open <browser_id> https://example.com/login
browser-act state
# 输出：[3] input "Email", [4] input "Password", [5] button "Sign In"

browser-act input 3 "user@example.com"
browser-act input 4 "password123"
browser-act click 5
browser-act wait stable
browser-act state    # 页面变化后必须重新检查

# 如果用户未提供凭证，不要填写表单——改用人机协助。
```

**重要：** 任何导致页面变化的操作（点击、导航、表单提交）之后，先执行 `wait stable` 再执行 `state` 获取最新元素索引。页面变化后旧索引失效。

## 策略组

策略组是一组规则，告诉你在浏览器自动化过程中何时采取特定行动。**每次任务开始时读取 `references/policies.md`**，并在整个任务过程中遵守。

该文件出厂包含预置规则。用户拥有完全控制权——可以禁用预置规则、修改阈值、或添加自定义规则。当用户要求修改策略时，直接更新该文件。不要自行创建、修改或删除策略——只在用户明确要求时才修改该文件。

**添加自定义规则示例：**

```markdown
## payment-confirmation
- enabled: true
- trigger: 到达付款或结算页面，即将产生扣款
- action: Request human assist
- note: 用户希望在完成购买前确认订单
```

## 人机协助

当策略触发且 action 为 `Request human assist` 时，调用 `human-assist-url` 获取远程访问链接并推送给用户。

```bash
browser-act human-assist-url --objective "请登录您的账号"
# → 返回 assist_url
```

**协助进行期间不要发送任何浏览器命令。** 等待用户在对话中确认已完成，然后继续任务。

## 命令链接

命令可以在单次 shell 调用中用 `&&` 链接。浏览器会话在命令之间保持，因此链接是安全的且比分开调用更高效。

```bash
# 打开 + 等待 + 检查，一次调用
browser-act browser open <browser_id> https://example.com && browser-act wait stable && browser-act state

# 链接多个交互
browser-act input 3 "user@example.com" && browser-act input 4 "password123" && browser-act click 5

# 导航并截图
browser-act navigate https://example.com/dashboard && browser-act wait stable && browser-act screenshot
```

**何时链接：** 当你不需要读取中间输出就能继续时使用 `&&`（如填写多个字段后点击）。当需要先解析输出时分开执行（如先 `state` 获取索引，再用索引交互）。

## 命令参考

### 导航

```bash
browser-act navigate <url>      # 导航到 URL
browser-act back                # 后退
browser-act forward             # 前进
browser-act reload              # 刷新页面
```

### 页面状态 & 交互

```bash
# 检查
browser-act state                         # 带索引编号的可交互元素
browser-act screenshot                    # 截图（自动路径）
browser-act screenshot ./page.png         # 截图到指定路径
browser-act screenshot --full             # 全页截图

# 交互（使用 state 返回的索引）
browser-act click <index>                 # 点击元素
browser-act hover <index>                 # 悬停元素
browser-act type "text"                   # 向当前聚焦元素输入文本
browser-act input <index> "text"          # 点击元素后输入文本
browser-act keys "Enter"                  # 发送键盘按键
browser-act scroll down                   # 向下滚动（默认 500px）
browser-act scroll up --amount 1000       # 向上滚动 1000px
```

### 数据提取

```bash
browser-act get title                     # 页面标题
browser-act get html                      # 完整页面 HTML
browser-act get text <index>              # 元素文本内容
browser-act get value <index>             # input/textarea 的值
browser-act get markdown                  # 页面转 Markdown
```

### JavaScript 执行

```bash
browser-act eval "document.title"         # 执行 JavaScript
```

### 标签页管理

```bash
browser-act tab list                      # 列出已打开的标签页
browser-act tab switch <tab_id>           # 切换到指定标签页
browser-act tab close                     # 关闭当前标签页
browser-act tab close <tab_id>            # 关闭指定标签页
```

### 等待

```bash
browser-act wait stable                   # 等待页面稳定（文档就绪 + 网络空闲，默认 30s）
browser-act wait stable --timeout 60000   # 自定义超时（毫秒）
```

### 网络检查

检查浏览器会话中所有打开标签页和 iframe 捕获的网络请求。请求全局追踪——切换标签页不会重置或过滤已捕获的数据。使用 `--filter` 缩小结果范围到特定页面或 API。

```bash
browser-act network requests                          # 列出所有捕获的请求（所有标签页）
browser-act network requests --filter api.example.com # 按 URL 子串过滤
browser-act network requests --type xhr,fetch         # 按资源类型过滤
browser-act network requests --method POST            # 按 HTTP 方法过滤
browser-act network requests --status 2xx             # 按状态码过滤（200、2xx、400-499）
browser-act network request <request_id>              # 单个请求的完整详情（含响应体）
browser-act network clear                             # 清除已追踪的请求
```

| 选项 | 说明 |
|------|------|
| `--filter <url>` | 按 URL 子串过滤 |
| `--type <types>` | 资源类型，逗号分隔（`xhr`、`fetch`、`document`、`script`、`stylesheet`、`image`、`font`、`media`、`websocket`、`ping`、`preflight`、`other`） |
| `--method <method>` | HTTP 方法（`GET`、`POST` 等） |
| `--status <code>` | 状态码（`200`）、类别（`2xx`）或范围（`400-499`） |
| `--clear` | 清除所有已追踪的请求（用于 `network requests` 命令） |

使用 `network request <request_id>` 获取单个请求的完整详情。详情视图包括：请求头、POST 数据（POST/PUT 请求）、响应头和响应体。二进制响应显示 `[base64, N chars]` 占位符。

**作用域说明：**
- **所有标签页和 iframe** 的请求汇入单个追踪器（上限 1,000 条）。
- 关闭标签页**不会**移除其之前捕获的请求。使用 `network clear` 重置。
- 多标签页工作时，使用 `--filter` 配合域名或路径隔离目标标签页。

### 网络模拟

模拟网络断开以测试离线行为、错误处理和恢复流程。

```bash
browser-act network offline on                # 模拟断网（所有请求失败）
browser-act network offline off               # 恢复网络连接
```

启用离线模式时：
- 所有网络请求以 `ERR_INTERNET_DISCONNECTED` 失败
- `navigator.onLine` 返回 `false`
- 浏览器触发 `offline` 事件
- Service Worker 缓存响应和 Cache API 读取仍然有效（绕过网络层）

禁用离线模式时：
- 网络完全恢复
- `navigator.onLine` 返回 `true`
- 浏览器触发 `online` 事件

**验证示例：**

```bash
browser-act eval "navigator.onLine"       # true
browser-act network offline on
browser-act eval "navigator.onLine"       # false
browser-act network offline off
browser-act eval "navigator.onLine"       # true
```

### 对话框管理

处理 JavaScript 对话框（alert、confirm、prompt）。默认情况下，browser-act 自动接受对话框。使用 `--no-auto-dialog` 禁用自动处理，改为手动处理。

```bash
browser-act dialog status                 # 检查是否有对话框打开
browser-act dialog accept                 # 接受（确定）当前对话框
browser-act dialog accept "some text"     # 带文本输入接受（用于 prompt 对话框）
browser-act dialog dismiss                # 取消当前对话框
```

**手动对话框流程：** 打开浏览器时传入 `--no-auto-dialog`，然后用 `dialog status` 检测对话框，用 `dialog accept` / `dialog dismiss` 处理。

### HAR 录制

捕获网络流量为 HAR（HTTP Archive）文件，用于调试、分析或回放。

```bash
browser-act network har start             # 开始录制网络流量
browser-act network har stop              # 停止并保存到默认路径（~/.browseract/har/）
browser-act network har stop ./trace.har  # 停止并保存到指定路径
```

在导航到目标页面之前开始录制。完成后停止——HAR 文件包含录制期间捕获的所有请求/响应。

### 验证码破解

当页面出现验证码挑战时，使用 `solve-captcha` 自动破解。这是 browser-act 服务的内置能力——直接运行命令即可。

```bash
browser-act solve-captcha                 # 破解当前页面的验证码
```

### 人机协助

```bash
browser-act human-assist-url --objective "..."                 # 发起协助，返回 assist_url（有效期 60 分钟）
```

完整流程参见上方[人机协助](#人机协助)章节。

## 并行自动化

使用独立会话并行运行多个浏览器。每个 `--session <name>` 创建隔离的浏览器上下文——不同会话的命令可以并发执行，互不冲突。

```bash
# 为每个任务创建 Stealth 浏览器
browser-act browser create "site-a" --desc "站点 A 的爬虫"
browser-act browser create "site-b" --desc "站点 B 的爬虫"

# 各自在独立会话中打开（并行运行）
browser-act --session site-a browser open <browser_id_a> https://site-a.com
browser-act --session site-b browser open <browser_id_b> https://site-b.com

# 独立交互（可并行运行）
browser-act --session site-a state
browser-act --session site-a click 3

browser-act --session site-b state
browser-act --session site-b click 5

# 清理
browser-act session close site-a
browser-act session close site-b
```

完成后务必关闭会话以释放资源。

## 会话管理

会话隔离浏览器状态。每个会话运行自己的后台服务。

```bash
# 使用命名会话
browser-act --session scraper navigate https://example.com
browser-act --session scraper state

# 列出活跃会话
browser-act session list

# 关闭会话
browser-act session close              # 关闭默认会话
browser-act session close scraper      # 关闭指定会话
browser-act session close --all        # 关闭所有会话
```

服务在一段时间不活跃后自动关闭。

## 站点笔记

浏览器自动化过程中积累的操作经验按域名存储在 `references/site-notes/` 中。

完成任务后，如果你发现了关于某个站点的有用模式（URL 结构、反爬行为、有效选择器、登录特点），将其写入对应文件。只写已验证的事实，不写猜测。

**文件格式：**

```markdown
---
domain: example.com
updated: 2026-03-28
---
## 平台特征
架构、反爬行为、登录要求、内容加载模式。

## 有效模式
已验证的 URL 模式、选择器、交互策略。

## 已知陷阱
什么会失败以及为什么。
```

**操作目标站点之前**，检查是否存在笔记文件并读取以获取先验知识。笔记带有日期——将其视为可能已变化的提示，而非保证。

## 系统命令

```bash
browser-act report-log                    # 上传日志以帮助诊断问题
browser-act feedback "message"            # 发送反馈以帮助改进此 Skill
```

如果你遇到问题或有改进 browser-act 的建议，使用 `feedback` 告诉我们。这直接帮助我们改进工具和此 Skill。

## 故障排除

- **`browser-act: command not found`** — 运行 `uv tool install browser-act-cli --index-url https://test.pypi.org/simple/ --extra-index-url https://pypi.org/simple --python 3.12`

## 参考文件

| 路径 | 说明 |
|------|------|
| `references/site-notes/{domain}.md` | 按站点积累的操作经验。操作已知站点前先读取。 |
| `references/policies.md` | 自动化策略（预置 + 自定义）。**每次任务开始时读取。** |
