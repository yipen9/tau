---
title: "Tau 学习手册 — 设计说明"
---

本文是《学习手册.md》的写作规格。手册正文在仓库根目录 `学习手册.md`，按本文执行。

手册代码块里的中文注释必须讲「在数据流里的位置 / 为什么这样写 / 对应哪条不变量」，禁止只标「下一行是 if」。later 硬化（取消补 tool result、push 持久化、steering 注入点、adapter 的 overflow 挂起等）要配带注释的片段，不能只列名词。第三、四部不得把七段模板压成「1–2 / 4–7」。

读者对象：会 Python、想按 Tau 官方阶段从 0 搞懂 coding agent 怎么搭起来的人。不假设读过 Pi，不假设熟悉 Textual。

# 定位

一本按 `dev-notes` 官方阶段、对着 **HEAD 源码** 从 0 往上装概念的施工日志。

它同时是：

- 教材：每一层讲清数据怎么流、为什么这样拆、打开源码时哪些函数在干活
- 地图：章序 = 官方 Phase 0–25，每章绑一篇（或一组）phase 笔记

它不是：

- 用户使用手册（那是 `website/content/`）
- 另写一套可运行的 mini-Tau
- 按 git 提交 checkout 考古
- 把每个 `.py` 全文粘进 Markdown

真实仓库实现文件不改。中文教学注释只出现在手册的代码块里。

# 材料角色

| 角色 | 材料 | 干什么 |
|---|---|---|
| 课程大纲 | `dev-notes/design/00-roadmap.md` + `dev-notes/architecture/index.md` | 章序 = Phase 0–25（含 17.5、20.x、24、25） |
| 每章骨架 | 对应 `phase-N-*.md` 以及相关 ADR / design 文 | 问题、边界、What was added、later hardening、How later phases use it |
| 正文的肉 | HEAD 上笔记点名的模块 | 原理段落 + 带中文注释的核心相关代码 + 走查 + 测试 |
| git | 不进正文 | 考古不是学习路径；读者始终停在 HEAD |

读者始终停在当前仓库 HEAD。不要求 `git checkout` 或 worktree。

「从 0 构建」的含义：按笔记阶段顺序，把每一层的合同装进脑子，再用 HEAD 代码证明合同还在、后来怎么长胖。不是从空目录敲出第二份 Tau。

# 交付物

仓库根目录一份：

```text
学习手册.md
```

单文件。部用 `#`，章用 `##`，文首放可点击目录。预估很长（十几万字量级）；靠目录和固定七段模板跳读，不靠拆文件。

# 语言与口径

- 正文中文。
- 代码保持仓库原样英文标识符、类型名、文件路径。
- 手册代码块里的注释用中文，讲「在数据流里的位置 / 为什么这样写 / 对应笔记哪个概念」，不讲「下一行是 if」。
- 事件名、API 名 **以 HEAD 为准**。若笔记使用旧名（例如 `MessageDeltaEvent`），用一句「笔记里的旧名对应现在的 X」对齐，然后按 HEAD 讲。
- 运行测试一律 `uv run pytest ...`。

# 单章模板（固定七段）

每章标题：`## Phase N — 短名`。标题下立刻给出笔记路径。

## 1. 这一层要解决什么

改编对应 `phase-N-*.md` 的开头和 “Why it exists”。写清：没有这一层时上一层缺什么。3–8 段，可以比笔记展开，但仍不写实现细节。

## 2. 边界

- 它不知道什么
- 依赖上一层什么
- 禁止渗进哪一层
- 关键不变量（append-only、事件是合同、loop 不存会话等）

## 3. 原理与核心代码（本章主体，必须厚）

这是「从 0 构建」的主教材。笔记只定骨架；这里要把相关核心代码讲全，并用原理段落把因果写透。

### 原理段落（每章至少覆盖）

1. **问题从哪来**
2. **数据流**：输入 → 内部步骤 → 输出/事件，配文字流程图
3. **为什么是这个边界**：若把 CLI / 路径 / Textual 塞进来会怎样
4. **和 Pi / 前后层的映射**
5. **关键不变量**
6. **失败路径**：未知工具、provider 报错、取消、max_turns 等，与主路径同等重要
7. **具体走查**：用「用户说 read README.md」或该章等价场景，把事件/状态逐步走一遍

这些段落写在代码之前或夹在代码之间，不要只在注释里带一句。

### 核心代码范围

「相关」= 笔记点名的模块里，**实现这一层合同的函数/类型，含支撑它的私有助手**。

- 不是整仓库倾销。
- 也不是只留 40 行骨架。
- HEAD 里后来长胖的参数可以留在贴出的签名里，用注释标成「后来的钩子，见第 5 段」，不要假装函数只有笔记当年的 5 个参数。
- 函数太长时按阶段拆成多个代码块，块与块之间插入原理段。

代码块头标注：

```text
# 摘自 src/.../file.py :: symbol（HEAD，按 Phase N 笔记讲解）
```

### 抽取规则

| 情况 | 做法 |
|---|---|
| 笔记点名的核心类型/函数，HEAD 仍短 | 可贴接近完整的当前定义，加中文注释 |
| HEAD 已明显长胖（`loop.py`、`session.py`、`cli.py`） | 按合同把主路径讲全（含私有助手），真实签名保留并注释 later 参数 |
| 文件是 UI 细节（主题、resize、picker、OAuth 屏） | 只精读笔记标明的接缝（adapter / state / 命令入口），接缝本身要讲透 |
| 笔记事件名与 HEAD 不一致 | 以 HEAD 为准，一句对齐旧名 |
| 测试 | 贴 1 个最能锁住合同的测试的关键断言，说明它锁的是哪条序列；不贴整个测试文件 |

## 4. 对照仓库

精确到符号，固定三行：

```text
实现    path :: symbol
测试    tests/... :: test_name
笔记    dev-notes/architecture/phase-N-....md
```

可列多个符号。读者应能按这张表打开文件。

## 5. 后来长出了什么

不是清单，也不是一句话。读者打开 HEAD 会看见比笔记当年更长的文件，这一段要告诉他们：**哪些长胖必须停在这一层、为什么、不停在这里会坏什么**。

每个 later 点写够三段：

1. 它解决的具体失败（取消后悬空 tool call、TUI 拆掉消费者导致丢盘……）
2. 为什么钩子只能长在这一层（loop 无状态所以注入点在 loop、队列却属于 harness）
3. 带中文注释的 HEAD 片段，或指向已经在第 3 段讲过的符号

讲解顺序仍是：先合同，后长胖。不要把 Phase 21 的扩展系统提前讲成本章主体。没有 later 的短章（如 Phase 25）写清「刻意不再长」和原因，不要空着。

## 6. 怎么验证

给出确切命令，例如：

```bash
uv run pytest tests/test_agent_loop.py -q
```

说明这条测试锁住的是哪条事件序列或哪条不变量。

## 7. 下一层怎么接

不是一句话预告。写清三件事，让读者合上本章就能开始下一章：

1. 本章交出去的**合同对象**（类型、函数、不变量）
2. 下一章缺的那一块（没有它，本章的对象还不能被谁用）
3. 下一章打开源码时先找的符号

章与章之间靠这段衔接，不要靠章首重复「上一层做了 X」。不要写 git SHA、不要写「首次落地提交」。考古不是学习路径。

# 篇幅按部控制

| 部 | 阶段 | 厚度 |
|---|---|---|
| 第一部 | 0–6 | 最厚。核心函数讲全 + 原理走查 + 测试断言 |
| 第二部 | 7–12 | 同样厚。TUI 以 adapter / `TuiState` 为主，不贴整份 `app.py` |
| 第三部 | 13–20.4 | 有原理和核心代码，但每个子阶段聚焦笔记点名的模块，不旁路扫完整个 `cli.py` |
| 第四部 | 21–25 | 21 / 22 / 24 按核心模块讲全；23 只讲 adapter 边界 + 2–3 个仍走事件的 polish 例子；25 较短但「不写入 session」必须配代码 |

Phase 28 RPC 不进正文。附录「下一步」里点明：同一套 `CodingSession` 事件可以再接一个无头前端，用来证明边界成立。

# 开篇要写什么

- Tau 同时是工具和教材
- 三层：`tau_coding → tau_agent → tau_ai`
- 事件是合同：harness 发、前端只消费
- 本手册怎么跟：笔记骨架 → 原理 → 带注释的 HEAD 核心代码 → 打开源码对照 → 跑测试
- `website/`（用户指南）vs `dev-notes/`（施工日记）vs `src/`（实现）
- 可点击目录

# 章节与核心符号

下列符号是该章第 3 段的最低覆盖面。写手册时若 HEAD 重命名，以当时 HEAD 为准并在章内说明。

## 第一部 — 核心循环

### Phase 0 — 地基

笔记：`dev-notes/design/00-roadmap.md`、`01-architecture.md`

- `pyproject.toml`：三包、`tau = tau_coding.cli:app`、Python 版本
- `src/tau_coding/cli.py` 的 `--version` 路径

原理：为什么先拆三包；为什么第一行能跑的命令不是 TUI。

### Phase 1 — 消息、工具、事件

笔记：`phase-1-core-types-and-events.md`、`design/05-core-types-and-events.md`

- `UserMessage` / `AssistantMessage` / `ToolResultMessage` / `ToolCall`
- `TextContent` / `ThinkingContent`（若 HEAD 已有，标成 later 或本章类型的一部分，按笔记「当时合同 vs 现在」处理）
- `AgentTool` / `AgentToolResult`
- `AgentStartEvent` / `AgentEndEvent` / `TurnStartEvent` / `TurnEndEvent`
- `MessageStartEvent` / `MessageUpdateEvent` / `MessageEndEvent`
- `ToolExecutionStartEvent` / `ToolExecutionUpdateEvent` / `ToolExecutionEndEvent`

原理：transcript 是什么；一轮 assistant 为何同时有文本和 tool call；UI 为什么不能听原始 chunk。

走查：用户说「读 README.md」时这些类型怎么串起来。

测试：`tests/test_agent_types.py`

### Phase 2 — Provider 层

笔记：`phase-2-ai-provider-layer.md`

- `ModelProvider`
- `FakeProvider`
- `stream_response()`
- `tau_ai` 的 provider 事件（以及 HEAD 中 `tau_agent.provider_events` 若已上移，讲清现在事件住在哪一层）
- `openai_compatible.py` 的适配主路径：组请求、读 delta、拼 tool_call、结束成 `AssistantMessage`

原理：供应商差异必须停在 `tau_ai`；fake provider 如何让 loop 可测。

测试：`tests/test_tau_ai.py`

### Phase 3 — 纯 Agent Loop

笔记：`phase-3-agent-loop.md`、`design/02-agent-loop.md`

- `run_agent_loop`
- `_assistant_events`
- `_execute_tool_call`
- `_run_tool`
- `_provider_context`

原理：无状态循环；调用方拥有 `messages`；provider 事件 → agent 事件；未知工具 / 异常隔离 / max_turns。

走查：纯文本回合的事件序列；`read` 后再回答的事件序列。

第 5 段：steering / follow-up 注入点；`before_tool_call` / `after_tool_call`（说明是给扩展预留，不在本章展开扩展系统）。

测试：`tests/test_agent_loop.py`，优先 `test_agent_loop_streams_canonical_nested_events` 一类锁事件序列的测试。

### Phase 4 — AgentHarness

笔记：`phase-4-agent-harness.md`、`design/harness.md`

- `AgentHarnessConfig`
- `AgentHarness.prompt` / `continue_`
- `subscribe` / `EventListener`
- `SimpleCancellationToken`
- 队列字段（steering / follow-up）作为第 5 段或签名注释

原理：loop 无会话，harness 才是有状态大脑；取消边界为什么在这层。

测试：`tests/test_agent_harness.py`

### Phase 5 — 四个编码工具

笔记：`phase-5-coding-tools.md`、`design/03-tools.md`

- `create_read_tool` / `create_write_tool` / `create_edit_tool` / `create_bash_tool`
- `create_coding_tools`
- 每个工具如何变成带 JSON schema 的 `AgentTool`

原理：具体工具为何在 `tau_coding` 而不在 `tau_agent`；模型只看见 schema 和结果文本。

测试：`tests/test_coding_tools.py`

### Phase 6 — Print-mode CLI

笔记：`phase-6-print-mode-cli.md`

- `cli.py` 的 `-p` / `--prompt` 路径：解析参数 → 解析 provider → 建 tools → 组 prompt → 跑（现在的）`CodingSession` 或笔记描述的早期 harness 路径
- 必须讲清笔记原路径 vs HEAD 现状（后来改走 `CodingSession`）

原理：为什么先有 print、再有 TUI；同一套事件如何打到 stdout。

测试：`tests/test_cli.py`

## 第二部 — 真正的 coding agent

### Phase 7 — Session 树 + JSONL

笔记：`phase-7-session-tree.md`、`design/04-sessions.md`

- session entry 类型（`MessageEntry`、`LeafEntry`、`SessionInfoEntry`、`ModelChangeEntry` 等）
- `JsonlSessionStorage`
- `SessionState.from_entries()`
- parent / leaf 回放

原理：append-only；文件 = 耐久历史，replay = 当前视图；为 compaction / branch 留下的不变量。

测试：`tests/test_session.py`

### Phase 8 — CodingSession

笔记：`phase-8-coding-session.md`

- `CodingSessionConfig` / `CodingSession.load`
- `prompt` / `continue_`
- 跑完后 append `MessageEntry` + `LeafEntry`
- 早期命令缝（为 Phase 15 做铺垫，不把 registry 提前讲完）

原理：Pi 的 AgentSession；harness 仍不认磁盘路径。

测试：`tests/test_coding_session.py`

### Phase 9 — Skills 与 Prompt Templates

笔记：`phase-9-skills-prompts.md`

- `resources.py` 路径与 frontmatter
- `skills.py` 加载与 `/skill:name` 展开
- `prompt_templates.py` 的 `{{ var }}`

原理：Markdown 资源如何变成给模型的文本，而不是新的运行时框架。

测试：`tests/test_skills.py`、`tests/test_prompt_templates.py`

### Phase 10 — System Prompt 组装

笔记：`phase-10-system-prompt.md`

- `system_prompt.py` 的拼装顺序：identity → tools → snippets / guidelines → skills → project context → date / cwd

原理：为什么必须有一个共享 builder，而不是 CLI 和 session 各写一份。

测试：`tests/test_system_prompt.py`

### Phase 11 — Print / JSON / Transcript 渲染

笔记：`phase-11-print-event-rendering.md`

- `FinalTextRenderer`
- `JsonEventRenderer`
- `TranscriptRenderer`
- `PrintOutputMode`

原理：渲染在 `tau_coding`；三种模式只是同一事件流的三种消费者。

测试：`tests/test_rendering.py`

### Phase 12 — Textual TUI（adapter 边界）

笔记：`phase-12-textual-tui.md`、`dev-notes/adr/0001-use-textual-for-tui.md`

- `TuiEventAdapter`
- `TuiState` / `ChatItem`
- `run_tui_app` 如何接到 `CodingSession`
- Escape 取消如何走到 harness token

**不**贴整份 `src/tau_coding/tui/app.py`。

原理：TUI 不能依赖 `tau_agent.loop` 的内部结构；只消费事件。

走查：一条 assistant delta 如何变成屏幕上的一行。

测试：`tests/test_tui_adapter.py`、`tests/test_tui_app.py`（挑锁边界的，不扫全部 UI 测试）

## 第三部 — 产品化

### Phase 13 — Tau home 与 `.agents`

笔记：`phase-13-paths-agents-resources.md`

- `TauPaths`
- user / project 资源根
- 自动加载进 session 的入口

测试：`tests/test_paths.py`、`tests/test_resources.py`

### Phase 14 — Session Manager 与 Resume

笔记：`phase-14-session-manager-resume.md`

- `SessionManager`
- `CodingSessionRecord`
- 创建 / 列表 / 按 id 查找 / touch
- CLI / TUI resume 入口（接缝，不写尽 UI）

测试：`tests/test_session_manager.py`

### Phase 15 — Slash Command Registry

笔记：`phase-15-slash-command-registry.md`

- `SlashCommand` / `CommandContext` / `CommandResult` / `CommandRegistry`
- `CodingSession.handle_command` 如何委托
- 内置 `/help` `/exit` 一类如何注册

测试：`tests/test_commands.py`

### Phase 16 — 资源发现与诊断

笔记：`phase-16-resource-discovery.md`

- `ResourceDiagnostic`
- 带诊断的 skill / prompt loader
- 坏文件不能打死 session

测试：`tests/test_resources.py`、`tests/test_skills.py`

### Phase 17 — TUI 自动补全

笔记：`phase-17-tui-autocomplete.md`

- `CompletionItem` / `CompletionState` / `build_completion_state`
- slash commands、`/skill:`、prompt templates

文件路径补全若 HEAD 已有，放第 5 段。

测试：`tests/test_tui_autocomplete.py`

### Phase 17.5 — Transcript 换行

笔记：`phase-17-5-transcript-wrapping.md`

- 换行 / resize 与 transcript widget 状态
- 为什么不改 harness

### Phase 18 — Provider 配置

笔记：`phase-18-provider-config-foundation.md`

- `ProviderSettings` / `OpenAICompatibleProviderConfig` / `ProviderSelection`
- `~/.tau/providers.json`
- 与环境变量的优先级
- 切换命令接缝

测试：`tests/test_provider_config.py`

### Phase 19 — 项目上下文

笔记：`phase-19-context-discovery.md`

- `discover_project_context`
- `AGENTS.md` 发现顺序
- `/context` `/reload`

测试：`tests/test_context.py`

### Phase 20 — 安装与文档

笔记：`phase-20-installation-docs.md`

偏产品：用户怎么拿到 `tau` 命令、first-run。代码少，但要把「可安装工具」和「可 import 的三包」分开讲。

### Phase 20.1 — Context 记账

笔记：`phase-20-1-context-accounting.md`

- `ContextUsageEstimate`
- `CodingSession.context_usage`
- sidebar 如何跟同一事件流刷新（接缝）

测试：`tests/test_context_window.py`

### Phase 20.2 — Thinking 模式

笔记：`phase-20-2-thinking-controls.md`

- `tau_coding.thinking` 档位
- session 级设置
- 模型不支持时隐藏控件、不乱发 `reasoning_effort`

测试：`tests/test_thinking.py`

### Phase 20.3 — Skill 调用

笔记：`phase-20-3-skill-invocation.md`

- system prompt 里的 `<available_skills>`
- `/skill:` 必达
- 与「模型自己去 read 技能文件」的关系

### Phase 20.4 — Session 导出

笔记：`phase-20-4-session-export.md`

- `session_export.py` 主路径
- HTML / JSONL
- 树结构如何原样出去

测试：`tests/test_session_export.py`

## 第四部 — 扩展与打磨

### Phase 21 — Extensions

笔记：`phase-21-extensions.md`

- 发现顺序与加载（`*.py` / `extension.py` / manifest）
- `ExtensionAPI`：`register_tool` / `register_command` / `on` / `send_user_message` / `append_entry`
- 负载钩子：`tool_call` / `tool_result` / `input`
- 如何只用 `AgentHarness.subscribe`、executor wrapping、`CommandRegistry`、`CustomEntry`
- 失败变成 `ResourceDiagnostic`
- 走查：`examples/extensions/hello_tool.py`

明确：**不改 `tau_agent`。** 笔记里的非目标（marketplace、自定义 entry renderer 等）一句划界，不展开。

测试：`tests/test_extensions.py`、`tests/test_example_extensions.py`

### Phase 22 — Compaction

笔记：`phase-22-compaction-foundation.md`

- `CompactionEntry`
- `SessionState.from_entries()` 如何替换消息但仍保留 JSONL
- `context_window.py` 估计、summarize、阈值
- `/compact` 与自动 compact
- 不变量：`session file = durable history`，`SessionState.messages = reconstructed active context`

测试：相关 session / context_window / commands 测试

### Phase 23 — TUI polish（代表性）

笔记：`phase-23-tui-polish.md`

重申 adapter 边界。只选 2–3 个例子，证明 polish 仍走事件 / `TuiState`，不改 loop：

- 成功 tool 输出预览（截断显示、完整结果仍在 session）
- assistant Markdown / 代码高亮（renderer-only）
- 按消息选择复制

不逐条 UI 微调，不贴 `app.py` 里的 picker / login 屏。

### Phase 24 — Session tree branching

笔记：`phase-24-session-tree-branching.md`

- `/tree` picker 的数据从哪来
- `Enter` 移动 leaf；`S` 经 `branch_summary`
- `LeafEntry` 导航为什么是结构变更而不是改 transcript
- `BranchSummaryEntry` 回放成用户上下文摘要

测试：session / TUI tree 相关测试中锁不变量的那些

### Phase 25 — `/system`

笔记：`phase-25-system-command.md`

- registry 中的 `/system`
- `CodingSession.system_prompt`
- print mode 在打 provider 之前处理本地命令
- TUI 内联展示

必须用代码证明：不 append user/assistant/custom entry，不触发 provider，不改 JSONL（除既有元数据）。

测试：`tests/test_commands.py`、`tests/test_coding_session.py`、`tests/test_cli.py` 中与 `/system` 相关的用例

# 附录要写什么

- 怎么跑测试、对着哪一层
- 打开一个 HEAD 文件时怎么用本章符号当地图
- 可选 git SHA 表（Phase 0–12 的首次落地提交足够；后期提交很碎，不强求一一对应）
- Phase 28 RPC：同一套 session 事件再接一个无头前端
- 最短阅读路径：概念 → Phase 1 类型 → Phase 2 fake provider → Phase 3 loop → Phase 4 harness → Phase 5 工具 → Phase 8 session → Phase 12 adapter

# 明确不写进手册正文的

- 把 `src/tau_coding/tui/app.py` 当教材通读
- OAuth 各家实现细节、模型目录 JSON、安装脚本内部
- 主题色、footer 文案、sidebar logo 等纯视觉 polish（Phase 23 已限定例子）
- 另起一个可运行的 mini 包
- 要求读者切换 git 历史
- 修改 `src/` 给源码加注释

# 写作时的质量标准

写完一章后自检：

1. 没读过 Pi 的人能否讲清这一层解决什么、不知道什么
2. 打开 HEAD 对应文件，手册点名的符号是否都还在（或已注明改名）
3. 是否有数据流、失败路径、至少一次走查
4. 核心相关函数是否讲到私有助手，而不是只留 while True 骨架
5. later 段是否配了代码，且没有抢下一章的主体
6. 是否给出可运行的 `uv run pytest ...`

全书完成后：目录可跳转；Phase 3 / 8 / 12 / 21 / 22 五章作为抽检章，必须达到上述标准。
