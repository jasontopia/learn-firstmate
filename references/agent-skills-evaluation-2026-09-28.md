# 评估报告：addyosmani/agent-skills 对 FirstMate 是否有用，以及 2026-09-28 开始做一个新产品的推荐方式

调研日期：2026-09-28
调研对象：`addyosmani/agent-skills` commit `2686b620fc1fed2e8f60c704839c766b8594c6b6`（2026-09-25，插件版本 0.6.11）
对照对象：FirstMate commit `b3dbc67af3414006fff0f9eb5d5d016823a8bfa0`（本次 worktree 的 HEAD），no-mistakes v1.79.0（本机已安装版本）

> **参考资料，不是教程章节。** 这是一份 2026-09-28 的调研报告快照，回答 `addyosmani/agent-skills` 这套工程 skill 对 FirstMate 有没有用。它读的是下面列出的 commit：agent-skills `2686b62`、FirstMate `b3dbc67`、no-mistakes v1.79.0。文中的行号引用（如 `AGENTS.md:33`）都指向这些 commit，之后的版本可能已经变了。星数等数据也只代表当天。
>
> 收进本仓库时只做了必要的改动：术语按 [术语译法表](../GLOSSARY.md) 统一，去掉了只和某一位船长个人设置有关的内容。分析、表格、来源和结论保持原样。

---

## 0. 结论先行（TL;DR）

1. **agent-skills 和 FirstMate 不在同一层。** FirstMate 管的是"谁来做、在哪做、怎么交付、谁批准合并"（编排层 + 交付验证层）；agent-skills 管的是"单个 agent 在写代码时应该怎么想、怎么做"（工程纪律层）以及"做什么产品"（产品定义层）。两者**大部分是互补的**。
2. **但不能整套装进来、让 FirstMate 按它的"九步"跑。** agent-skills 默认假设"一个人坐在一个交互式会话前、每个阶段都亲自点头"，而 FirstMate 的 worker 是自主运行、不能直接跟使用者对话的。凡是 agent-skills 里涉及"停下来等人批准 / 自己做代码审查 / push、打 tag、开 PR、合并 / 部署 / 自建 git worktree / 往 AGENTS.md 加内容"的部分，都会和 FirstMate + no-mistakes 的契约**重复或冲突**（详见第 4.4 节，逐条带文件路径）。
3. **推荐方案（一个）：** 以 FirstMate + no-mistakes 为主干；从 agent-skills 里**挑选约 12 个"纯纪律型"skill**，按固定 commit **放进产品仓库本身**（项目级安装，不做全局安装）；产品定义阶段用 FirstMate 的 **scout + Lavish 看板**产出 SPEC（想法还很模糊时，先在一个普通对话里用 interview-me 把想法问清楚）；**代码审查只保留 no-mistakes 这一道**。FirstMate 本身**不需要改代码**，只需在本地 `config/brief-include.md` 加几行"适配说明"（第 5.3 节给出可直接用的文本）。
4. **竞争方案里没有任何一个能同时覆盖四层**（这也是 2026 年 6 月一篇 arXiv 对比论文的结论）。Superpowers、Matt Pocock's skills、agent-skills 属于同一类（工程纪律层）；Spec Kit、OpenSpec、Kiro、BMAD 属于"产品定义 / 规格驱动流程"类。对 FirstMate 来说，**agent-skills 是最适合"按需挑选"的纪律库**：粒度细、跨 harness、每个 skill 都有 eval，而且它"接管流程"的部分可以干净地剥离；Superpowers 自带编排（建 worktree、子 agent 驱动、分支收尾时的合并/PR 菜单），与 FirstMate 冲突最多。

---

## 1. 给 FirstMate 新手的概念速查

| 概念 | 含义 |
| --- | --- |
| **captain（船长）** | 使用者本人。FirstMate 的设计是：使用者只和 firstmate 一个 agent 说话。 |
| **firstmate（大副）** | 在 FirstMate 仓库里启动的主 agent 会话（Claude Code、Codex、Pi 等都可以）。它**不亲自改项目代码**，只负责接需求、派活、监督、汇报、在授权下合并（`AGENTS.md:23`、`AGENTS.md:31-44`）。 |
| **crewmate / worker（船员）** | firstmate 派出去干活的独立 agent，每个在自己的终端窗口和隔离的 git worktree 里运行。worker **不能直接和 captain 对话**，所有沟通都经过 firstmate（`AGENTS.md:39`）。 |
| **harness** | 跑船员的 agent 工具，也就是运行 agent 的具体工具，比如 Claude Code、Codex CLI、Pi、OpenCode。FirstMate 可以把不同任务派给不同 harness。 |
| **skill** | 一个 `SKILL.md` 文件（带 `name` 和 `description`），描述一种工作流程。harness 平时只把 **description** 放在上下文里，判断相关时才加载正文（Claude Code 官方文档：<https://code.claude.com/docs/en/skills>）。skill 是"软约束"：模型可能触发，也可能不触发。 |
| **brief（任务简报）** | firstmate 派活时写给 worker 的任务简报，由 `bin/fm-brief.sh` 生成，包含 `## Captain's intent`（使用者原话）、`## Firstmate spec`（构建要求）、规则、完成标准（Definition of done）。 |
| **ship / scout（交付任务 / 调研任务）** | 两种任务形态。ship 产出代码改动（PR 或本地分支）；scout 只产出报告 `data/<id>/report.md`，从不 push（`AGENTS.md:180-181`）。本报告就是一个 scout 的产物。 |
| **delivery mode（交付方式）** | 每个项目/任务选一种：`no-mistakes`（完整验证流水线后开 PR）、`direct-PR`（直接开 PR）、`local-only`（只在本地分支）（`docs/architecture.md:362-366`）。 |
| **no-mistakes** | 同一作者的独立工具（<https://github.com/kunchenguid/no-mistakes>）：一个本地 git 代理，在代码到达远端之前跑一条流水线：intent、rebase、review（AI 代码审查）、test、document、lint、push、PR、CI。worker 只负责"回答它的关卡"，修复由流水线自己做。 |
| **yolo** | 合并授权开关。关闭时每个 PR 都要 captain 亲口批准；打开时 firstmate 可以自己合并"全绿且在范围内"的 PR（`AGENTS.md:233`）。 |
| **needs-decision / blocked / paused** | worker 写进状态文件的事件。需要人拍板时写 `needs-decision`，firstmate 收到后替它去问 captain 或自己裁决。 |
| **Lavish 看板** | FirstMate 用来做可视化评审的 HTML 页面，船长可以在页面上批注、反馈，适合评审计划和设计。 |
| **backlog（待办队列）** | FirstMate 自己的待办队列（默认 `data/backlog.md`，通过 `bin/fm-tasks-axi.sh` 操作），记录"工作项"，不记录 agent。 |

---

## 2. 我做了什么（方法与证据来源）

- 把 agent-skills 克隆到 scout 的临时目录，读完全部 25 个 `skills/*/SKILL.md`（共 7,494 行、约 5.2 万词）、9 个 `.claude/commands/*.md`、4 个 `agents/*.md` persona、`hooks/`、`references/`、`docs/`（comparison、adoption-guide、getting-started）、`evals/README.md`、插件清单 `.claude-plugin/plugin.json`。
- 读 FirstMate：`AGENTS.md`、`VISION.md`、`README.md`、`docs/architecture.md`、`docs/configuration.md` 的相关节、`.agents/skills/`（29 个，全部是 firstmate 自己用的运维 skill）、`skills/`（只有 `stow`）、`bin/fm-brief.sh --help`、`bin/fm-dod-lib.sh`（完成标准的唯一 owner）、`bin/fm-ensure-agents-md.sh`、`.agents/skills/project-management/SKILL.md`、`.no-mistakes.yaml`，以及 `no-mistakes --help`、`no-mistakes axi run --help` 和 no-mistakes skill 正文。
- 竞品：用 `gh-axi repo view` / `gh-axi api repos/<r>` 取星数、创建时间、最近 push 时间（2026-09-28 当天），并浅克隆 Superpowers、Spec Kit、BMAD、OpenSpec、Matt Pocock's skills、Compound Engineering、gstack、GSD、Anthropic 官方插件目录读 README 和关键 skill；Kiro（闭源）、Codex skill 路径、Claude Code skill 路径、arXiv 对比论文通过网页一手资料核实。
- 没有改任何代码，没有 push，没有开 PR。

---

## 3. agent-skills 是什么

### 3.1 定位

一句话：**把资深工程师的工作流程写成 AI agent 能照着做的 skill 包**，覆盖从"想法"到"上线"的整个生命周期（`README.md`）。作者 Addy Osmani（Google Chrome 团队），2026-02-15 创建，截至 2026-09-28 约 9.97 万星、1.05 万 fork，最近一次 push 为 2026-09-26。MIT 许可。

每个 skill 的固定结构：Overview / When to Use / Process（步骤）/ Common Rationalizations（agent 常找的偷懒借口及反驳）/ Red Flags / Verification（完成的证据要求）（`docs/skill-anatomy.md`）。这是它最有价值的设计：**"反合理化表"专门堵 agent 跳步骤的借口。**

### 3.2 "九步开发流程"到底是什么

仓库里并没有一个叫"九步"的流程。它指的是 **9 个斜杠命令**，挂在 **6 个阶段**上（`README.md` 开头的图，`README.md:24`）：

```
DEFINE → PLAN → BUILD → VERIFY → REVIEW → SHIP
/spec    /plan   /build   /test    /review   /ship
```

| # | 命令 | 做什么 | 调用的 skill |
| --- | --- | --- | --- |
| 1 | `/spec` | 先问清需求，写 `SPEC.md`（目标、命令、目录结构、代码风格、测试策略、边界三档），等人确认 | spec-driven-development |
| 2 | `/plan` | 只读分析，拆成小的垂直切片任务，写 `tasks/plan.md` 和 `tasks/todo.md`，等人确认 | planning-and-task-breakdown |
| 3 | `/build` | 默认：实现"下一个"任务（先写失败测试 → 实现 → 全量测试 → 构建 → commit → 停下）；`/build auto`：人批准一次计划后连续做完所有任务 | incremental-implementation + test-driven-development |
| 4 | `/test` | TDD；修 bug 用 "Prove-It"（先写能复现 bug 的失败测试） | test-driven-development |
| 5 | `/constraints` | 访谈最多 4 个问题，写 `CONSTRAINTS.md`（质量门槛 + 具体检查命令），并防止 agent 偷偷降低门槛 | constraint-driven-development |
| 6 | `/review` | 五维代码审查（正确性、可读性、架构、安全、性能），按严重级别分类 | code-review-and-quality |
| 7 | `/webperf` | Web 性能审计（专项，仅 Web 应用） | web-performance-auditor persona |
| 8 | `/code-simplify` | 在不改变行为的前提下简化代码 | code-simplification |
| 9 | `/ship` | 并行派出 3 个审查 persona（code-reviewer、security-auditor、test-engineer），合并成 GO/NO-GO 决定 + 回滚计划 | shipping-and-launch |

另外，元 skill `using-agent-skills` 里还写了一个更细的 **16 步生命周期顺序**（`skills/using-agent-skills/SKILL.md` 的 "Lifecycle Sequence"），从 interview-me 一直到 shipping-and-launch。

### 3.3 全部 25 个 skill 一览（及其所在"层"）

"层"的定义见第 4.1 节。"建议"一栏是第 5 节推荐方案的预告。

| 阶段 | skill | 做什么 | 层 | 与 FirstMate 的关系 | 建议 |
| --- | --- | --- | --- | --- | --- |
| 元 | using-agent-skills | 路由到合适 skill；"先暴露假设、困惑就 STOP 等人回复" | L3 | 冲突：`Wait for resolution`（`:70`）会让自主 worker 干等 | 不装 |
| Define | interview-me | 一次问一个问题，直到 95% 把握理解需求 | L4 | 需要活人实时回答；worker 不能和 captain 对话 | 只给 captain 自己在普通对话里用 |
| Define | idea-refine | 发散/收敛地打磨想法，产出一页纸 | L4 | 调用 `AskUserQuestion`（`:69`），worker 里会卡住 | 只给 captain 自己用 |
| Define | spec-driven-development | 写 SPEC（六要素 + 成功标准 + 未决问题），每阶段人审 | L4 | 互补；"人审"映射到 scout 报告 + Lavish 评审 | 装（scout 用） |
| Define | constraint-driven-development | 定质量门槛并落成可执行检查 | L2/L3 | 互补（给 no-mistakes 提供要跑的命令），但要求往 AGENTS.md/CLAUDE.md 加一行（`:140`） | captain 自己跑一次，或作为明确授权的 ship 任务 |
| Plan | planning-and-task-breakdown | 拆垂直切片、验收标准、依赖顺序 | L1/L4 | 部分重叠：FirstMate backlog 才是跨任务的队列 | 装（scout 用于拆任务） |
| Build | incremental-implementation | 薄切片：实现 → 测试 → 验证 → commit | L3 | 互补 | 装 |
| Build | test-driven-development | 红-绿-重构；Prove-It 修 bug | L3 | 互补 | 装 |
| Build | context-engineering | 规则文件、上下文打包、可重启边界 | L3 | 多数内容是给写 AGENTS.md 的人看的；可重启边界思想与 FirstMate 一致 | 可选 |
| Build | source-driven-development | 框架用法必须查官方文档并引用 | L3 | 互补 | 装 |
| Build | doubt-driven-development | 对每个非平凡决定起一个新上下文的对抗审查，交互时必须提供跨模型（Gemini/Codex CLI）审查 | L2/L3 | 重复 no-mistakes 的 review；耗 token | 不装 |
| Build | frontend-ui-engineering | 组件、设计系统、WCAG 2.1 AA、避免"AI 味" UI | L3 | 互补 | 有 UI 时装 |
| Build | api-and-interface-design | 契约优先、Hyrum 定律、错误语义 | L3 | 互补 | 装 |
| Verify | browser-testing-with-devtools | 通过 Chrome DevTools MCP 看运行时 | L3 | 互补；FirstMate 自己用 `chrome-devtools-axi`，worker 环境需有 MCP 或改用 axi | 有 Web 时装 |
| Verify | debugging-and-error-recovery | 复现 → 定位 → 缩小 → 修根因 → 加护栏 | L3 | 互补（与 firstmate 的 `diagnostic-reasoning` 同一思路，那个是 firstmate 自己用的） | 装 |
| Review | code-review-and-quality | 五维审查，"合并前必须审查，无例外" | L2 | **重复** no-mistakes review；描述写着 "Use before merging any change" | 不装 |
| Review | code-simplification | 保持行为不变的简化 | L3 | 轻度重叠 no-mistakes review | 可选 |
| Review | security-and-hardening | OWASP、密钥、依赖审计、三档边界 | L3 | 互补 | 装 |
| Review | performance-optimization | 先测量再优化 | L3 | 互补 | 有性能需求时装 |
| Ship | git-workflow-and-versioning | 主干开发、原子 commit、分支命名、worktree、打 tag、写 changelog | L1/L2 | **冲突**（见 4.4 第 3 条） | 不装 |
| Ship | ci-cd-and-automation | 搭 CI、分支保护、自动合并、预览部署 | L2 | **冲突**：启用 auto-merge 会绕过合并授权（`:307`） | 只作为明确授权的 ship 任务 |
| Ship | deprecation-and-migration | 弃用、迁移、扩展/收缩式 schema 迁移 | L3 | 互补 | 后期再装 |
| Ship | documentation-and-adrs | ADR、API 文档、README、changelog | L3 | 基本互补；changelog 部分与 no-mistakes 的 document 步骤可能冲突 | 装（ADR 部分） |
| Ship | observability-and-instrumentation | 结构化日志、RED 指标、追踪、告警 | L3 | 互补 | 上线前装 |
| Ship | shipping-and-launch | 上线清单、灰度、回滚、错误预算 | L2+部署 | FirstMate 的交付止于"PR 合并"，部署不在其范围；部署是不可逆操作，必须 captain 亲自批准 | 只作为明确授权的任务 |

此外还有：4 个 persona（`agents/`，作为 Claude Code 子 agent 自动注册）、7 份参考清单（`references/`，含一份 Definition of Done）、若干 hook（`hooks/`，**插件默认不挂载**，见 `hooks/session-start.sh:5`）、一套三层 eval 框架（`evals/`，这是它相对 Superpowers 和 Pocock 的独特之处）。

### 3.4 它对 harness 的隐含假设

1. **有一个活人在同一个会话里随时回复。** spec 的四个阶段每阶段都"Human reviews"（`skills/spec-driven-development/SKILL.md:30`），plan 要"The human has reviewed and approved"（`skills/planning-and-task-breakdown/SKILL.md:253`），`/build` 默认做完一个任务就"Mark the task complete and stop"（`.claude/commands/build.md:25`），`/build auto` 也要"wait for an unambiguous affirmative"（`.claude/commands/build.md:34`）。
2. **主会话就是编排者。** `/ship` 要用 Agent 工具在同一轮里并行派 3 个子 agent（`.claude/commands/ship.md:11`）；doubt-driven 明确写着"designed for the main-session orchestrator"（`skills/doubt-driven-development/SKILL.md:44`）。
3. **harness 原生支持 skill 路由和斜杠命令**；不支持的 harness 才用 session-start hook 注入元 skill（`docs/getting-started.md:47` 警告不要出现"两个路由器"）。
4. **仓库里的文件是跨会话的交接物**：`SPEC.md`、`tasks/plan.md`、`tasks/todo.md`、`CONSTRAINTS.md`、`docs/ideas/`、`docs/intent/`。
5. **agent 自己管 git**：自建分支（`feature/<x>`）、自建 worktree、自己 push tag、自己决定 GO/NO-GO。
6. **skill 触发是概率性的。** 它自己的 eval 记录：在一个固定措辞下，review skill 7 次里触发 5 次，TDD skill 7 次里只触发 2 次（`evals/README.md:53`）。也就是说，**skill 能提高平均质量，但不能当硬性保证**。

---

## 4. 分层分析：FirstMate 已经覆盖什么，agent-skills 在哪里重叠、互补、冲突

### 4.1 四层模型

为了讲清楚"谁该管什么"，把"用 AI 开发产品"拆成四层：

| 层 | 回答的问题 | 典型内容 |
| --- | --- | --- |
| **L1 队伍编排** | 谁来做、并行怎么安排、在哪个隔离环境里做、做到一半挂了怎么办 | 派活、worktree 隔离、监督、持久化状态、backlog |
| **L2 交付与验证** | 一个改动怎么变成可合并的东西、谁审、谁批准合并 | 审查、测试、lint、文档、push、PR、CI、合并授权 |
| **L3 单个 worker 的工程纪律** | 写代码的那个 agent 应该怎么工作 | TDD、薄切片、调试方法、安全/性能/API/UI 的专业做法 |
| **L4 产品定义** | 到底要做什么、为谁做、做到什么程度算成功 | 访谈、PRD/SPEC、成功标准、不做清单、切片计划 |

### 4.2 FirstMate 在每一层的覆盖

| 层 | FirstMate 的覆盖 | 证据 |
| --- | --- | --- |
| L1 | **完整覆盖，而且是确定性脚本实现的。** 事件驱动的零 token 监督、每个任务独立 worktree、崩溃/重启无损、backlog、多 harness 调度、二副（secondmate） | `README.md:42-53`，`docs/architecture.md:9`、`:279`，`VISION.md` "A restart is a non-event" |
| L2 | **完整覆盖，通过 no-mistakes + 交付方式 + 合并守卫。** no-mistakes 模式下"review、fixes、tests、documentation、push、PR、CI 全部归 no-mistakes"，而且明确禁止在它之外再加人工审查关卡；合并必须经 `bin/fm-pr-merge.sh`，它会实时核对 PR 非草稿、可合并、所有检查全绿 | `AGENTS.md:222-224`，`docs/architecture.md:362-420`，`bin/fm-dod-lib.sh:341-460` |
| L3 | **有意不管。** worker 的完成标准只规定"在你的分支上 commit、何时报告 done、怎么驱动 no-mistakes"，不规定怎么设计、怎么测试、怎么写代码。FirstMate 自己的 29 个 `.agents/skills/` 全部是运维/监督用的（afk、bearings、ship-landing、validation-supervision 等），没有一个是教 worker 写代码的 | `bin/fm-dod-lib.sh:341-460`，`README.md:203-211`，`VISION.md:71` |
| L4 | **只有入口，没有方法。** FirstMate 期望 captain 带着"意图"来（`VISION.md`：把"说过一次的意图"变成被监督的工作），scout 可以产出"设计类交付物"并用 Lavish 评审，但没有规定 SPEC 应该长什么样、怎么访谈 | `AGENTS.md:181`，`VISION.md` 第 1 段 |

`VISION.md:71` 的原话是："firstmate is the command layer, not the workshop: validation belongs to no-mistakes, CI belongs to the forge, and merge policy belongs to the configured authority." 也就是说，**L3 的"车间工艺"是 FirstMate 有意留给 worker（以及项目自身）的**。

### 4.3 对照结论

| 层 | agent-skills 的内容 | 与 FirstMate 的关系 |
| --- | --- | --- |
| L1 | `git worktree add` 并行开发、`tasks/todo.md` 任务清单、`/build auto` 连续执行、`/ship` 的并行 persona | **重叠且更弱**：FirstMate 用确定性脚本做这些，agent-skills 靠提示词 |
| L2 | `/review`、`/ship` GO/NO-GO、code-review-and-quality、doubt-driven、ci-cd（含 auto-merge）、git-workflow（push tag） | **重叠或冲突**：与 no-mistakes 和合并授权正面相撞 |
| L3 | TDD、薄切片、调试、source-driven、安全、API、UI、性能、可观测性、文档/ADR | **纯互补**：正好填补 FirstMate 有意留白的地方 |
| L4 | interview-me、idea-refine、spec-driven、planning、constraint-driven | **互补但要改造交互方式**：它们要活人实时回答，而 FirstMate worker 不能直接问 captain |

### 4.4 具体冲突清单（worker 如果照做会出什么问题）

1. **"停下等人"会被 FirstMate 当成卡死。** `using-agent-skills` 要求困惑时"STOP ... Wait for resolution"（`skills/using-agent-skills/SKILL.md:70`），`/build` 默认做完一个任务就停（`.claude/commands/build.md:25`），interview-me 要"STOP YOUR TURN IMMEDIATELY"（`skills/interview-me/SKILL.md:130`），idea-refine 调用 `AskUserQuestion`（`skills/idea-refine/SKILL.md:69`）。而 FirstMate 的 worker 被告知"Work on your own; do not wait for a human"（`bin/fm-brief.sh:545`），需要人拍板时必须写 `needs-decision` 事件（`bin/fm-brief.sh:574`）；一个静默等待的窗口会被监督器按"疑似卡死"升级处理（`docs/architecture.md:9` 起的 stale/wedge 逻辑）。worker 也不能直接问 captain（`AGENTS.md:39`）。
2. **重复审查，违反"不在 no-mistakes 之外加审查关卡"。** `/review`、`/ship` 的三 persona 并行审查（`.claude/commands/ship.md:11`）、code-review-and-quality（"Every change gets reviewed before merge - no exceptions"）、doubt-driven 的对抗审查和跨模型审查（`skills/doubt-driven-development/SKILL.md:112-116`），与 `AGENTS.md:222-224`（"no-mistakes alone owns review ... Never hold work outside no-mistakes for a manual clean verdict, stack serial manual reviews"）直接冲突，并且白白消耗 token（`VISION.md:37` 把 token 效率列为一等公民）。
3. **git 操作冲突。** git-workflow-and-versioning 建议 `feature/<name>` 分支命名（`:141`），而 FirstMate 的 ship 分支名写死在完成标准里，spawn 会拒绝不一致的分支（`bin/fm-dod-lib.sh:43-45`）；建议自建 `git worktree add`（`:153`），而 worker 规则 7 明确禁止创建/删除 worktree；建议出问题时 `git reset --hard HEAD`（`:189`），而 no-mistakes 要求"Never abort-and-restart, reset, or replace the branch in a way that drops prior gate-fix commits"（`no-mistakes axi run --help`）；发布时 `git push origin v1.4.0` 打 tag（`:292`），而 no-mistakes 模式下"the pipeline owns the push"（`bin/fm-dod-lib.sh` no-mistakes 分支）。
4. **合并授权被绕过。** ci-cd-and-automation 建议"Auto-merge: If all checks pass and approved, merge automatically"（`skills/ci-cd-and-automation/SKILL.md:307`）。FirstMate 的铁律 2 是"没有 captain 明确同意不合并 PR"（`AGENTS.md:33`），`bin/fm-pr-merge.sh` 默认拒绝 `--auto`（`docs/architecture.md` "Delivery modes" 一节）。在仓库里打开 GitHub auto-merge 等于在 FirstMate 看不见的地方开了一个后门。`/ship` 自己下 GO/NO-GO 决定（`.claude/commands/ship.md:70-71`）也与"合并/部署由配置的授权方决定"重叠。
5. **往项目 AGENTS.md / CLAUDE.md 加内容。** constraint-driven-development 要求"add one line to AGENTS.md and CLAUDE.md"（`skills/constraint-driven-development/SKILL.md:140`，`.claude/commands/constraints.md:25`）。FirstMate 规定 worker 只能**更正错误信息**，不能**添加**缺失的知识，添加是人的刻意选择（`AGENTS.md:155`）；而且 FirstMate 约定 `CLAUDE.md` 是固定的两行 `@AGENTS.md` 指针（`bin/fm-ensure-agents-md.sh` 头部注释），往里加一行会破坏这个约定。
6. **两套任务清单。** planning-and-task-breakdown 默认把任务写进仓库里的 `tasks/todo.md`（`skills/planning-and-task-breakdown/SKILL.md:33`），`/build` 按它逐项勾选。FirstMate 的 backlog 才是派活的唯一队列（`AGENTS.md` 第 10 节）。如果多个 worker 并行改同一个 `tasks/todo.md`，会产生合并冲突和"谁说了算"的混乱。
7. **部署越界。** shipping-and-launch 的回滚步骤里直接写 `git revert <commit> && git push`（`skills/shipping-and-launch/SKILL.md:266`），灰度发布、开关功能都是对生产环境的操作。FirstMate 把"破坏性、不可逆、安全敏感"的动作都列为必须 captain 明确说出具体动作才能做（`AGENTS.md:235`、`AGENTS.md:346`、`AGENTS.md:418`）。

**不冲突、可以直接用的**：TDD、incremental-implementation 里"每个切片一个 commit"（在 worker 自己的 ship 分支上 commit 是 FirstMate 允许甚至要求的）、debugging、source-driven、security、API、UI、performance、observability、ADR。

---

## 5. FirstMate worker 使用这些 skill 的具体可行性

### 5.1 三种安装方式

| 方式 | 做法 | 优点 | 风险 |
| --- | --- | --- | --- |
| **A. 全局安装** | `/plugin install agent-skills@addy-agent-skills` 或 `npx skills add addyosmani/agent-skills -g` | 一次安装到处生效 | ① **firstmate 主会话本身也会加载**：25 个 skill 的 description（约 1,361 词，常驻上下文）加 9 个命令、4 个 persona 都会出现在监督者会话里，诸如"Use when making any code change""Use before merging any change"的描述会和 AGENTS.md 的"firstmate 不亲自改代码、不另加审查"相互拉扯；② 所有项目（包括 FirstMate 仓库自己的 worker）都会受影响；③ FirstMate 会把任务派给不同 harness（Claude、Codex、Pi……），全局安装要逐个 harness 装，行为不一致；④ 版本随插件自动更新，不可复现 |
| **B. 项目级安装（推荐）** | 把挑选出的 skill 目录按固定 commit 放进**产品仓库**：`.agents/skills/<name>/`（Codex、Pi、OpenCode、Cursor、Gemini 等读这里）和 `.claude/skills/<name>/`（Claude Code 读这里），可用 `npx skills add ... --skill <name> -a claude-code -a codex` 生成（默认 canonical 目录 + 符号链接） | 只影响这个产品；每个 worker 不论用哪个 harness 都看到同一份；版本锁定、升级走 PR、可审查；firstmate 主会话完全不受影响 | ① Grok（`.grok/skills/`）、Devin（`.devin/skills/`）等 harness 路径不同，如果调度到它们需要额外放一份；② 按单个 skill 安装时不会带上仓库级 `references/`（上游 issue #361），TDD 等 skill 引用的清单会缺失，可一并拷贝需要的清单；③ no-mistakes 流水线里的审查/测试/文档 agent 也会看到这些 skill（本仓库可以用 `disable_project_settings` 关掉项目设置，但那会连 AGENTS.md 一起关，产品仓库不建议这样做），需要观察 |
| **C. 写进 brief** | 利用 FirstMate 已有的 `config/brief-include.md`：该文件存在时，`bin/fm-brief.sh` 把它原样追加到每个 ship/scout brief 末尾的 `# Home brief additions`，且明确"服从 brief 其他所有章节"（`bin/fm-brief.sh --help`，`docs/configuration.md:890-897`） | 不改 FirstMate 代码；天然处于"低于交付契约"的优先级，正好用来写适配规则 | 作用于这个 FirstMate 目录下的所有项目（包括 FirstMate 自己），不能按项目区分；不会被二副继承；不适合放大段 skill 正文（每个 brief 都会变长） |

**结论：B + C 组合。** skill 正文走 B（放在产品仓库里，按需加载，不占常驻上下文太多）；"怎么把 skill 里的人机交互翻译成 FirstMate 语义"这几条短规则走 C（对所有 worker 生效，且优先级天然低于交付契约）。

### 5.2 推荐放进产品仓库的 skill（agent-skills@2686b62）

- **核心（建议从第一天就放）**：`test-driven-development`、`incremental-implementation`、`debugging-and-error-recovery`、`source-driven-development`、`security-and-hardening`、`api-and-interface-design`、`spec-driven-development`、`planning-and-task-breakdown`、`documentation-and-adrs`
- **按产品形态加**：`frontend-ui-engineering` + `browser-testing-with-devtools`（有 Web UI 时）、`performance-optimization`、`observability-and-instrumentation`（接近上线时）、`deprecation-and-migration`（后期）
- **不放**：`using-agent-skills`、`interview-me`、`idea-refine`、`doubt-driven-development`、`code-review-and-quality`、`git-workflow-and-versioning`、`ci-cd-and-automation`、`shipping-and-launch`、`constraint-driven-development`，以及全部斜杠命令、`agents/` persona、`hooks/`。其中 ci-cd、shipping、constraints 的**内容**仍然有用，但应该由 captain 明确发起一个专门任务来做，而不是让每个 worker 自动触发。

同一时间只用**一个** skill 库作为主路由（agent-skills 自己的 `docs/comparison.md:119` 也这么建议：叠加多个 meta-skill 会抢命令名、抢路由、互相冲突的 TDD 理念）。

### 5.3 FirstMate 需要改吗？

**不需要改任何代码或共享文件。** 需要做的只有两件本地配置/项目内容上的事：

1. 在本地 FirstMate 目录（home）新建 `config/brief-include.md`（gitignored、仅本机），内容建议如下（英文，因为 brief 是英文，worker 读英文最稳）：

```markdown
Engineering skills: when this project ships engineering skills (for example test-driven-development, incremental-implementation, debugging-and-error-recovery, security-and-hardening), use them for HOW you build. This brief's Rules and Definition of done still own delivery.
- A skill step that says to ask, wait for, or get approval from "the user" or "the human": append needs-decision per Rule 6 with your best recommendation and stop. Never idle waiting in the pane, and never use an interactive question tool.
- Do not run extra review passes (/review, /ship persona fan-out, doubt-driven or cross-model review): the delivery path owns validation.
- Do not create or remove worktrees, rename your ship branch, push, tag, open or merge PRs, enable auto-merge, change branch protection, or deploy, except where the Definition of done tells you to.
- Committing each verified slice on your ship branch is fine; once a no-mistakes run has started, never reset or rewrite commits.
- Do not add to AGENTS.md or CLAUDE.md, do not write CHANGELOG entries, and keep scratch plans (tasks/plan.md, tasks/todo.md) out of the PR unless the task asks for them.
```

2. 在产品仓库的 `AGENTS.md` 里写一小段"本项目的工程纪律"（例如：本项目用 TDD、每个 PR 控制在约 300 行以内、SPEC 在 `docs/SPEC.md`、质量门槛命令是什么）。按 FirstMate 规则，**AGENTS.md 的新增内容必须是人刻意决定的**（`AGENTS.md:155`）：由 captain 自己写，或者 captain 把原文明确交给一个 ship 任务去落地（属于"当前、明确、具体的 captain 指令"，`AGENTS.md` 最后一节 "Captain instruction precedence"）。

**可选的后续改进（不是现在必需的，记作 follow-up）：** 目前 `config/brief-include.md` 只能按 FirstMate 目录生效，不能按项目生效；如果以后同一个 FirstMate 目录里既有"用 agent-skills 的产品项目"又有"不用的项目"，可以考虑给 FirstMate 提一个"按项目的 brief 附加说明"特性。现阶段用不上。

### 5.4 风险汇总

| 风险 | 严重度 | 缓解 |
| --- | --- | --- |
| skill 让 worker 静默等人，被监督器当卡死反复升级 | 高 | brief-include 第 1 条规则；不放 interview-me/idea-refine/using-agent-skills |
| 重复审查、token 翻倍、违反"唯一审查关卡" | 中 | 不放 review/doubt 类 skill 和 `/ship`；brief-include 第 2 条 |
| git/合并/部署越权 | 高 | 不放 git-workflow、ci-cd、shipping；brief-include 第 3、4 条；FirstMate 的 `fm-pr-merge.sh` 和 no-mistakes 本身也有硬守卫 |
| 全局安装污染 firstmate 主会话 | 中 | 只做项目级安装 |
| skill 触发是概率性的，不能当保证 | 中 | 硬性要求放进 no-mistakes 能执行的命令（`.no-mistakes.yaml` 的 `commands`，例如 test/lint），skill 只负责提高平均质量 |
| 两套任务清单 | 低-中 | backlog 是唯一跨任务队列；`tasks/` 只作为 scout 报告的一部分或 worker 私下草稿 |
| 供应链（skill 本质是会被执行的提示词） | 低-中 | 锁定 commit、升级走 PR 审查、不挂载上游 hook |
| no-mistakes 流水线 agent 受项目 skill 影响 | 低 | 先观察前几次运行的审查结果；有问题再调整 `.no-mistakes.yaml` 的 review/test 指令 |

---

## 6. 竞争方案对比（截至 2026-09-28）

星数和最近 push 时间来自 `gh-axi repo view` / `gh-axi api repos/<r>`（2026-09-28 当天查询）。星数只是很粗的"关注度"指标，不等于实际使用量；agent-skills 自己的对比文档也刻意不引用星数（`docs/comparison.md:30`）。

| 方案 | 类型 / 主要层 | 核心流程 | 优点 | 缺点 | 与 FirstMate 的契合度 |
| --- | --- | --- | --- | --- | --- |
| **FirstMate + no-mistakes**（基线） | 编排 + 交付验证（L1/L2） | captain 意图 → brief → 隔离 worker → no-mistakes 流水线 → PR → 授权合并 | 确定性脚本实现、重启无损、多 harness、合并有硬守卫 | 有意不管 L3/L4 | - |
| **addyosmani/agent-skills**（9.97 万星，2026-09-26） | 纪律库（L3）+ 定义（L4），附带 L2 命令 | 6 阶段 9 命令，25 skill | 覆盖最广（安全、API、UI、性能、可观测、弃用）；反合理化表；唯一带全目录 eval 的；支持 10+ harness | 默认"每阶段人审"；L2 部分与 FirstMate 冲突；不在 Anthropic 官方插件市场（在作者自己的 marketplace） | **高（挑选使用）**：L3 部分可以干净剥离 |
| **obra/superpowers**（29.2 万星，2026-09-27） | 方法论（L3 为主，自带 L1/L2） | brainstorming → 建 worktree → writing-plans → 子 agent 逐任务开发 + 两段审查 → TDD → finishing-a-development-branch（合并/PR/保留/丢弃菜单） | 内环最深、最适合长时间自主运行；已进入 Claude 和 Codex 官方插件市场 | **自带编排**：建 worktree、子 agent 驱动、分支收尾菜单，与 FirstMate 冲突最多（它会识别外部管理的 detached-HEAD worktree 并不自建，但 FirstMate 的 ship 分支是具名分支，仍会出现"本地合并"选项） | 中：只适合借用 TDD、systematic-debugging、verification-before-completion |
| **mattpocock/skills**（27.1 万星，2026-09-24） | 纪律库（L3）+ 需求拷问（L4） | grill-me / grill-with-docs（一次一问的"拷问"）、tdd、to-spec、to-tickets、diagnosing-bugs | 小而可组合，明确"不接管流程"（README 原话批评 GSD/BMAD/Spec Kit"接管流程、夺走控制权"）；grilling 是需求澄清的标杆；在 Claude 官方市场 | Claude Code 优先；需要跑 setup 向导并绑定 issue tracker（与 FirstMate backlog 重叠）；Build 之后覆盖薄；无 eval | 中-高：理念最接近 FirstMate，可作为 agent-skills 的替代纪律库（二选一） |
| **github/spec-kit**（13.9 万星，v1.0.x，2026-09-28） | 规格驱动流程（L4，延伸到 L3） | constitution → specify → plan → tasks → implement → converge；另有 bug 修复、想法评估扩展 | GitHub 官方、文档完整、多 agent 支持、产物结构清晰 | 需要 Python/uv CLI；有自己的 implement/converge 阶段和可选的建分支 hook，与 FirstMate 交付重叠；对单人新产品偏重 | 中：可只用 constitution/specify/plan 产出 SPEC，由 FirstMate 负责之后的一切 |
| **Fission-AI/OpenSpec**（7.1 万星，2026-09-28） | 规格驱动（L4），偏存量项目 | `/opsx:propose` → `openspec/changes/<id>/`（proposal、specs 增量、design、tasks）→ apply → archive | 轻量、以"变更提案"为单位、对存量项目友好；spec 增量可被审阅 | 以"每个变更"为中心，对 0 到 1 的新产品定义帮助有限 | 中-高：一个 change 目录天然对应 FirstMate 的一个 ship 任务，适合产品长大后使用 |
| **Kiro**（AWS，闭源 IDE + CLI） | 规格驱动 IDE（L4 + 自带执行） | requirements.md → design.md → tasks.md；Quick Spec 可跳过审批 | 规格流程做进了产品界面 | 绑定 Kiro 自己的 IDE/CLI；星数等采用度无法从一手来源核实 | 低：它本身就是另一个 harness，不能作为 FirstMate worker 的 skill 使用（Kiro CLI 的 skill 目录是 `.kiro/skills/`，但不在 FirstMate 已验证的 harness 列表里） |
| **BMAD Method**（5.4 万星，v6.12.0，2026-09-28） | 多角色敏捷流程（L4 + L3） | 分析师 → PM → 架构师 → Scrum Master → 开发 → QA；BMad Loop 可无人值守跑一个 epic | 角色视角丰富、按规模调整深度、文档化上下文 | 仪式感重、学习曲线陡；BMad Loop 与 FirstMate 编排重叠 | 低-中：可借用其"产品简报/PRD/架构"模板 |
| **EveryInc/compound-engineering-plugin**（2.5 万星，2026-09-28） | 纪律库（L3）+ 知识沉淀 | brainstorm → plan → build → review → **capture learnings**（36 个 skill，14 个 host） | "每次改动后沉淀经验"的理念很好 | 自带 review 与规划流程，与 no-mistakes 重叠 | 中：FirstMate 自己的 `/stow` 已经在做运维知识沉淀 |
| **garrytan/gstack**（13.4 万星，2026-09-28） | 角色化"虚拟团队"（L2-L4） | office-hours、plan-ceo-review、plan-eng-review、review、qa、ship、land-and-deploy 等 23 个命令 | 面向创始人，产品评审视角强，QA 带真实浏览器 | 以 Claude Code 为主、安装需要 Bun；安装步骤要求往 CLAUDE.md 加一段；自带 ship/land-and-deploy，与合并授权冲突 | 低：可借鉴 plan-ceo-review 式的产品评审提问 |
| **Anthropic 官方插件**（claude-plugins-official，3.7 万星） | 单点工具（L2/L3） | `feature-dev`（7 阶段：发现、代码探索、澄清、架构、实现、质量审查、总结）、code-review、pr-review-toolkit、code-simplifier、frontend-design、ralph-loop 等 | 官方维护、质量稳定 | 都是 Claude Code 专用、单会话交互式；审查类与 no-mistakes 重叠 | 低-中：`frontend-design` 可单独用于 UI 质量 |
| **GSD（Get Shit Done）** | 规格驱动 + 上下文工程 | - | - | `gsd-build/get-shit-done` 已于 2026-05-31 归档，迁移到 `open-gsd/gsd-core`（未进一步核实新仓库现状） | 不评估 |

**研究界的判断。** 2026-06-03 的 arXiv 论文 *From Prompt to Process: a Process Taxonomy and Comparative Assessment of Frameworks Supporting AI Software Development Agents*（<https://arxiv.org/abs/2606.04967>）对 Spec Kit、OpenSpec、BMAD、GSD 等做了六维（规格、上下文、角色、执行、验证、可移植性）对比，结论是：持久化产物、工作契约、可追溯性和人工审查是减少歧义、协调 agent 的机制，但**没有任何一个框架完整覆盖六个维度**，深度和跨 agent 可移植性之间存在根本取舍。这和本报告的分层结论一致：**最好的组合不是找一个"全家桶"，而是每层选一个最强的、并且彼此不抢职责的部件。**

**"agentic engineering"视角下的关键区别。** 上表里除 FirstMate 外，几乎所有方案都假设"一个人 + 一个交互式 agent 会话"（最多在会话内派子 agent）。FirstMate 解决的是另一个问题："一个人 + 一支并行的自主 agent 队伍"。因此这些方案对 FirstMate 来说都不是替代品，只能作为 worker 内部的纪律或 scout 的产物格式来借用；其中"接管流程"越少的，越容易借用。

---

## 7. 最终建议：2026-09-28 开始做一个新产品，推荐这样做

### 7.1 对三个问题的直接回答

1. **FirstMate 现在是否已经足够？** 对"派活、隔离、监督、验证、合并"（L1/L2）来说**足够，而且比 agent-skills 更严格**（确定性脚本 + no-mistakes 硬关卡，而不是概率性触发的提示词）。对"想清楚做什么"（L4）和"worker 怎么写代码"（L3）来说**不够**，但这是 FirstMate 有意留白（`VISION.md:71`），应该由项目自带的内容来补。
2. **FirstMate 能否调用 agent-skills 并按它的九步走？** **能调用其中大部分纪律型 skill，但不应该按它的九步走。** 九步里的 `/spec`、`/plan` 可以映射成 FirstMate 的 scout + Lavish 评审；`/build`、`/test` 映射成 ship worker 内部的做法；`/review`、`/ship`、`/code-simplify` 由 no-mistakes 取代；`/constraints` 由 captain 一次性确定；真正的部署在 FirstMate 范围之外，要单独、明确地授权。
3. **直接用 FirstMate、装 agent-skills 按它走、还是更好的方式？** **选第三种：以 FirstMate + no-mistakes 为骨架，项目级挑选安装 agent-skills 的纪律型 skill，产品定义用 scout + Lavish 产出 SPEC。**

### 7.2 为什么是这个方案

- 它让每一层只有一个 owner：L1/L2 归 FirstMate + no-mistakes（确定性、可审计），L3 归项目内的 skill（可版本锁定、所有 harness 一致），L4 归 captain 的判断 + scout 的产出物。没有两个东西抢同一件事。
- 它不需要修改 FirstMate，风险最低、可逆（删掉 skill 目录和 brief-include 就回到原状）。
- 它和 FirstMate 的设计哲学一致：firstmate 是"指挥层，不是车间"；新能力以"可选、显式开启"的方式加入；token 精简。
- 它保留了 agent-skills 最有价值的东西（TDD、薄切片、反合理化、SPEC 结构、安全/API/UI 的专业做法），丢掉的只是和 FirstMate 重复的编排与审查。

### 7.3 具体的第一步行动序列

1. **（captain 自己，30 分钟以内，不涉及仓库）把想法问清楚。** 如果想法还模糊，在一个普通对话里（例如 Claude 应用）贴入 agent-skills 的 `interview-me` 方法（一次一问、每问附带猜测、最后复述"结果 / 用户 / 为什么现在 / 成功标准 / 约束 / 不做什么"），得到一页纸的意图说明。想法已经很清楚就跳过这一步。
2. **（通过 firstmate）新建项目。** 对 firstmate 说"新建一个项目 X"。firstmate 会按 `project-management` skill 提议仓库名、owner、可见性（默认 private）和交付姿态（默认 `no-mistakes-prod-only`：面向用户的改动走完整流水线，内部工具走 direct-PR），并在创建 GitHub 仓库前征得明确同意，然后克隆、登记、执行 `no-mistakes init`（`.agents/skills/project-management/SKILL.md` "Create a project" 与 "Initialize"）。建议 **yolo 先保持关闭**，每个 PR 都亲自看。
3. **（本地配置，一次性）写 `config/brief-include.md`。** 用第 5.3 节的文本。
4. **（ship 任务）把工程纪律放进产品仓库。** 对 firstmate 说："在 X 里从 addyosmani/agent-skills@2686b62 引入这些 skill 到 `.agents/skills` 和 `.claude/skills`：（第 5.2 节核心列表），并按我给的原文在 AGENTS.md 加一段工程纪律说明"（原文由 captain 提供）。走 no-mistakes → PR → captain 合并。
5. **（scout 任务）产出 SPEC。** 把第 1 步的一页纸交给 firstmate，明确说"先出一份产品 SPEC 作为设计交付物，用 Lavish 看板给我评审"。scout 按 `spec-driven-development` 的结构写：目标与用户、成功标准、不做清单、技术栈、命令、目录结构、测试策略、边界三档（总是做 / 先问 / 绝不做）、未决问题；多模块时先给"能力地图"；再按 `planning-and-task-breakdown` 给出第一个里程碑的垂直切片（每片约 100-300 行、带验收标准和依赖）。captain 在看板上批注，scout 迭代到 captain 明确批准。
6. **（ship 任务）落地 SPEC 和骨架。** 由 firstmate 把 scout 提升（promote）为 ship，或新派一个 ship：提交 `docs/SPEC.md`、项目骨架、测试和 lint 命令，并把这些命令写进产品仓库的 `.no-mistakes.yaml`（`commands`），让 no-mistakes 每次都真正跑测试和 lint。质量门槛（原 `/constraints` 的内容，例如"新增代码覆盖率 ≥ 80%、禁止新增 lint 抑制注释、gitleaks 扫描"）由 captain 在这一步的意图里直接说明，而不是让 worker 访谈。
7. **（firstmate backlog）按切片派活。** 把批准的切片逐条登记为 backlog 工作项（一片一个 ship 任务），没有依赖关系的并行派出。每个 worker 在自己的 worktree 里按 TDD + 薄切片写代码，no-mistakes 验证、开 PR，captain 决定是否合并。
8. **（稳定后）逐步放权与补齐上线能力。** 连续多次 PR 质量稳定后，再考虑给这个项目开启 `+yolo`。第一次面向真实用户之前，单独派任务做可观测性（observability-and-instrumentation）和上线清单（shipping-and-launch 的检查表部分）；真正的部署、分支保护、CI 自动合并这类动作，每一次都由 captain 明确授权。

### 7.4 什么情况会改变这个建议

- **想法本身还处在"值不值得做"的阶段**：先做产品验证（访谈用户、做原型），不要急着写 SPEC；此时 Spec Kit 的 "idea assessment" 扩展或 Pocock 的 `prototype` 更合适。
- **产品变成多人协作或多仓库**：OpenSpec 的"规格仓库 + 每个变更一个目录"会比单个 `SPEC.md` 更合适，而且一个 change 目录能直接对应一个 FirstMate ship 任务。
- **主要使用单一 harness 且希望 agent 长时间自主跑完一大块**：可以考虑在单个 worker 内借用 Superpowers 的 `subagent-driven-development`，但必须先剥掉它的 worktree 和分支收尾部分，否则与 FirstMate 冲突。
- **FirstMate 未来加入按项目的 brief 附加说明、或官方给出推荐的 L3 skill 集**：届时应改用官方机制。
- **发现 skill 让 no-mistakes 的审查结果变差或 token 成本明显上升**：退回"只用 FirstMate + 项目 AGENTS.md"的最小方案，skill 只保留 TDD 和 debugging 两个。

---

## 8. 附录：证据与来源

### 8.1 主要命令

```sh
git clone https://github.com/addyosmani/agent-skills.git   # HEAD 2686b620fc1f..., 2026-09-25, "chore(release): bump plugin manifests to 0.6.11"
wc -l skills/*/SKILL.md ...                                  # 25 个 skill，共 7,494 行
grep -nE "AskUserQuestion|git push|merge|wait for|Stop and ask|..." skills/*/SKILL.md .claude/commands/*.md agents/*.md
gh-axi repo view <owner/repo>                                # 星数、fork 数
gh-axi api repos/<owner/repo>                                # created_at / pushed_at / archived
git clone --depth 1 <competitor repos>                       # 读 README 与关键 skill
bin/fm-brief.sh --help                                       # FirstMate brief 契约
no-mistakes --version; no-mistakes axi run --help            # v1.79.0
```

### 8.2 仓库状态快照（2026-09-28）

| 仓库 | 星数 | 创建 | 最近 push | 读取的 commit |
| --- | --- | --- | --- | --- |
| addyosmani/agent-skills | 99,682 | 2026-02-15 | 2026-09-26 | 2686b62 |
| obra/superpowers | 292,469 | 2025-10-09 | 2026-09-27 | 8ca22db |
| mattpocock/skills | 271,277 | 2026-02-03 | 2026-09-24 | c55ee46 |
| anthropics/skills | 178,801 | 2025-09-22 | 2026-09-24 | 未克隆 |
| github/spec-kit | 139,266 | 2025-08-21 | 2026-09-28 | 8d3f64c（pyproject 1.0.13.dev0） |
| garrytan/gstack | 134,400 | 2026-03-11 | 2026-09-28 | d2a0bbc |
| Fission-AI/OpenSpec | 70,588 | 2025-08-05 | 2026-09-28 | 79b6aa9 |
| gsd-build/get-shit-done | 64,442 | 2025-12-14 | 2026-05-31（已归档） | bdcaab2 |
| bmad-code-org/BMAD-METHOD | 53,592 | 2025-04-13 | 2026-09-28 | 1cbcfa2（最新 tag v6.12.0） |
| anthropics/claude-plugins-official | 37,148 | 2025-11-20 | 2026-09-28 | fbe07fb |
| vercel-labs/skills（`npx skills`） | 32,698 | - | - | 读 README 的安装路径表 |
| eyaltoledano/claude-task-master | 28,103 | 2025-03-04 | 2026-04-28 | 未克隆 |
| EveryInc/compound-engineering-plugin | 25,310 | 2025-10-09 | 2026-09-28 | 5e3aee1 |
| kunchenguid/no-mistakes | 8,669 | 2026-04-05 | 2026-09-28 | 本机 v1.79.0 |
| kunchenguid/firstmate | 7,284 | 2026-06-12 | 2026-09-28 | b3dbc67 |
| buildermethods/agent-os | 5,454 | 2025-07-16 | 2026-08-29 | 未克隆 |

### 8.3 关键文件引用

- agent-skills：`README.md`（9 命令、25 skill、安装方式）、`.claude/commands/build.md:25,34,36`、`.claude/commands/ship.md:11,70-71`、`.claude/commands/constraints.md:25`、`skills/using-agent-skills/SKILL.md:70`、`skills/interview-me/SKILL.md:36,130`、`skills/idea-refine/SKILL.md:69`、`skills/spec-driven-development/SKILL.md:30,246`、`skills/planning-and-task-breakdown/SKILL.md:33,253`、`skills/git-workflow-and-versioning/SKILL.md:141,153,189,292,311`、`skills/ci-cd-and-automation/SKILL.md:304,307`、`skills/constraint-driven-development/SKILL.md:38,140`、`skills/doubt-driven-development/SKILL.md:44,112-116`、`skills/shipping-and-launch/SKILL.md:266`、`hooks/session-start.sh:5`、`evals/README.md:53`、`docs/getting-started.md:47`、`docs/comparison.md:30,119`、`.claude-plugin/plugin.json`。
- FirstMate：`AGENTS.md:23,33,39,41,155,180-181,185,222-224,233`、`VISION.md:37,71`、`README.md:36-53,203-211`、`docs/architecture.md`（"Worktrees, not branches in your checkout""No-mistakes gate authority boundary""Two task shapes""Delivery modes are explicit per task"）、`docs/configuration.md:890-897`、`bin/fm-brief.sh:545,574`（及 `--help`）、`bin/fm-dod-lib.sh:1-81,341-460`、`bin/fm-ensure-agents-md.sh`（头部注释与 `## Maintaining this file`）、`.agents/skills/project-management/SKILL.md`（Create a project / Initialize）、`.no-mistakes.yaml`。
- no-mistakes：`no-mistakes axi run --help`（`--yes` 行为、禁止 reset 丢弃修复 commit、`--intent` 要求）、本机 no-mistakes skill 正文（流水线步骤：intent、rebase、review、test、document、lint、push、PR、CI）。

### 8.4 网页一手来源

- Claude Code skill 存放位置与加载方式：<https://code.claude.com/docs/en/skills>
- Codex skill 存放位置（`.agents/skills`，从当前目录向上到仓库根）：<https://learn.chatgpt.com/docs/build-skills>
- Kiro specs（requirements/design/tasks，IDE + CLI，Quick Spec 无审批关卡）：<https://kiro.dev/docs/specs/>
- arXiv 2606.04967，*From Prompt to Process: a Process Taxonomy and Comparative Assessment of Frameworks Supporting AI Software Development Agents*（2026-06-03）：<https://arxiv.org/abs/2606.04967>
- `npx skills` 各 agent 的项目级/全局安装路径：<https://github.com/vercel-labs/skills>（README 安装路径表）
- 各竞品仓库：<https://github.com/obra/superpowers>、<https://github.com/mattpocock/skills>、<https://github.com/github/spec-kit>、<https://github.com/Fission-AI/OpenSpec>、<https://github.com/bmad-code-org/BMAD-METHOD>、<https://github.com/EveryInc/compound-engineering-plugin>、<https://github.com/garrytan/gstack>、<https://github.com/anthropics/claude-plugins-official>、<https://github.com/gsd-build/get-shit-done>

### 8.5 未能核实的内容

- Kiro 的实际采用度（闭源产品，没有可比的一手数据）。
- GSD 迁移后的新仓库 `open-gsd/gsd-core` 的现状。
- agent-skills 对比文档引用的 Superpowers vs agent-skills 实验（LinkedIn 文章，单人单任务实验，本报告未独立复现）。
- 各方案在真实 FirstMate 队伍里的效果：本报告是基于文本契约的分析，没有实际派 worker 做对照实验。如果需要量化证据，可以在一个试验项目里对同一批小任务做"装/不装 skill"的对照（观察 no-mistakes 审查发现数、返工轮数、token 消耗）。

---

## 9. 是否有应该交付（ship）的工作

没有发现 FirstMate 的缺陷。唯一可能的 FirstMate 改进（"按项目的 brief 附加说明"）在当前场景下不需要，记为可选 follow-up。建议后续实际动手的工作都在**新产品仓库**里，按第 7.3 节的顺序由 captain 发起。
