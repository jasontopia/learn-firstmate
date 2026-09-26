# 第 12 章：Relay

## 这一章讲什么

这是这本教程的最后一章。前面十一章讲的都是你和大副之间的对话，或者大副和船员之间的调度 - 无论走到哪一关，说话的入口始终是你自己敲给大副的那句话。这一章讲一个例外：**Relay**（公开提及接入），一个让大副能够被 X（原 Twitter）或 Discord 上的公开提及唤醒、并直接公开回复的开关。

这个开关默认是关的。它单独占一章，不是因为它常用，而是因为它牵扯到这本教程之前从没出现过的东西 - 一个不是你本人、却能触发大副做事的入口。所以这一章要讲清楚三件事：这个入口打开之后，那句「同意」到底同意了什么；哪些动作无论开不开，大副都永远不会自己拍板；以及为什么在它关着的时候，这一切都不会碰到你。

本章依据的权威文件是 `AGENTS.md` 第 14 节「Relay」，以及 `docs/configuration.md` 中「Relay (.env)」一节。每一段引用都会标出处。

## Relay 是什么

`AGENTS.md` 第 14 节开头这样定义它：

> Relay is the public-mention integration older docs and some emitted lines still call "X mode"; its identifiers keep the `FMX_`, `x-`, and `fm-x-` spellings.
> Relay ships inert and causes no behavior change until the home opts in by placing `FMX_PAIRING_TOKEN` in its gitignored `.env`.

**Relay**（公开提及接入）让一份 FirstMate 安装能够被公开平台上的一句提及唤醒。`docs/configuration.md` 补充了它具体覆盖哪些平台：

> Relay lets a firstmate instance answer public mentions and act on normal reversible mention requests through firstmate's normal lifecycle.
> It covers both public surfaces the relay supports: `@myfirstmate` mentions on X, and mentions of the myfirstmate bot in a Discord server where it is installed.

也就是说，Relay 覆盖两个公开入口 - X 上 `@myfirstmate` 的提及，以及安装了 myfirstmate 机器人的 Discord 服务器里对它的提及 - 用的是同一套配对、同一条轮询、同一条回复路径。

这里有个命名上的历史包袱值得先说清楚：一部分较老的文档和大副自己写出来的状态行，仍然把这个功能叫「X mode」，相关的标识符也还留着 `FMX_`、`x-`、`fm-x-` 这几种写法。这本教程之后统一用 Relay 这个名字，但如果你在自己那份 FirstMate 安装里看到 `x-mode-error`、`FMX_PAIRING_TOKEN` 这类字样，知道它们说的就是这一章讲的同一件事。

`AGENTS.md` 这两句话里最关键的词是「inert」（惰性）：Relay 出厂就是关着的，而且关着的时候不只是「没人给你发提及」，是**这份代码路径本身完全不运行**，直到这份 FirstMate 安装（术语叫「home」）主动打开它。

## 打开它，动的是什么

打开的动作本身很小：把配对令牌（pairing token）写进这份 FirstMate 安装自己的、被 gitignore 掉的 `.env` 文件里的 `FMX_PAIRING_TOKEN` 这一行。`docs/configuration.md` 把整套开启步骤写在「Relay (.env)」一节：

> 1. Sign in at myfirstmate.io with X or Discord.
> 2. For the Discord surface, use the dashboard's install link to add the myfirstmate bot to a server you administer; the X surface needs no install step.
> 3. Copy the pairing token from the dashboard into this firstmate home's gitignored `.env` as `FMX_PAIRING_TOKEN=<token>`.
> 4. Start a new firstmate session so bootstrap picks the token up, then mention `@myfirstmate` on X or mention the bot in a server where it is installed.

这四步之外没有第二个开关。同一节说得很直接：账号创建、身份绑定、机器人安装、令牌发放这些事都在 myfirstmate.io 那个网站的仪表盘上办完，`.env` 只负责接住最后那一个令牌。这份文件不属于你的项目仓库，也从不入版本库 - 打开或关闭 Relay，从头到尾都不会碰到任何一个被版本追踪的文件。

## 那一个令牌到底同意了什么

这是这一章最重要的一句话，出自 `AGENTS.md` 第 14 节：

> That token is consent for public replies and normal reversible lifecycle actions from eligible mentions, not authority for destructive, irreversible, or security-sensitive action; those still require trusted-channel confirmation.

拆成两半读。

**同意的部分：** 把令牌放进 `.env`，等于你同意大副对**合法的提及**（eligible mentions）自主做两件事 - 公开回复，以及走它平时正常流程里那些**可逆**的动作。`docs/configuration.md` 还补了一句关于「谁算合法提及」的判断依据：

> The relay uses owner-only routing: a mention delivered to a home is from that home's owner/captain, while its surrounding conversation context may still include other public accounts.

也就是说，Relay 用的是「按所有者路由」：一条送到你这份 FirstMate 安装的提及，认定它就是来自这份安装的所有者本人 - 也就是你，船长。这句里也提了一个容易忽略的细节：一条提及**周围的对话上下文**（比如它是回复谁、这条线索上还有谁说过什么）可能包含别的公开账号说的话；这些话只是背景，不是船长本人下的指令。

**没同意的部分：** 破坏性、不可逆、涉及安全的动作，这个令牌完全不构成授权。这三类动作依然要走**可信渠道确认**（trusted-channel confirmation）- 不管 Relay 开没开，也不管这条提及看起来多像是船长本人发的。

打个比方帮助建立直觉（下面这段是**假设的场景**，不是这个仓库或这份教程用的这套 FirstMate 安装里真实发生过的事）：假设 Relay 已经打开，船长在 X 上 `@myfirstmate` 说「帮我看看那个 PR 的 CI 为什么红了，查完直接回我」。这是一次正常、可逆的请求 - 查一下状态、回一句话 - 大副会自主处理并直接公开回复，不会跑回来问你「要不要我查」。但如果那条提及说的是「直接把那个 PR 合了」或者「把生产环境那个进程杀了」，这两个都是不可逆或涉及安全的动作，Relay 打开也不会让它们自动发生 - 大副会在公开回复里说这件事已经报给船长确认，然后走可信渠道等你点头，而不是从一条公开提及直接执行。

## 关着的时候，完全不受影响

`AGENTS.md` 第 14 节开头那句「Relay ships inert」不是一句空话，`docs/configuration.md` 把「关着」具体落到了状态层面：

> When the token is removed or empty, the next locked session-start bootstrap step removes those artifacts.
> Steady-state off is silent and writes nothing.
> Relay remains additive to non-Relay lifecycle behavior: homes without the generated artifacts keep the default watcher cadence and do not run the Relay poll.

翻成大白话：`.env` 里没有那个令牌，大副每次开机时的例行检查都不会为 Relay 生成任何本地文件，稳定态下的「关」是**静默的、不写任何东西的**；没开 Relay 的这份安装，监督节奏跟平时完全一样，也根本不会去跑那条 Relay 轮询。「Relay 是加法，不是改动现有行为」这句话就是 README 学习路线图里说「默认关着，不开就完全不影响你」的出处。

这一章没有引用任何一次真实发生过的 Relay 事件：Relay 默认关着，只有船长主动把配对令牌写进自己那份 FirstMate 安装的 `.env`（`FMX_PAIRING_TOKEN`）才会生效，在没人这么做之前，就不存在任何一次真实的公开提及、回复或跟进可以拿来当例子。

## 动手练习

下面的练习是**只读**的：只是让大副读取当前状态、做推理并汇报，不会创建工单、不会派出真正的船员、不会改动任何被版本追踪的文件，也不会碰 `.env` 或任何 Relay 配置。你随时可以停下。

做练习前，先在你的 FirstMate 目录里启动一个 primary 会话，这样你面前的这个 agent 就是你的大副。

### 练习：搞清楚这一个开关到底同意了什么

对大副说：

> 大副，我要搞清楚 Relay 这个开关对我这份 FirstMate 安装意味着什么，这只是一次问答，不要真的去改任何东西。请分两部分回答：第一，直接告诉我这份安装现在 Relay 是开着还是关着，你是怎么判断出来的；第二，不管现在开没开，讲清楚如果打开它，那个配对令牌到底自动授权你做哪些事，以及不管开不开，哪些动作你永远不会不经我确认就自己执行。请指出你说的每一句依据是哪个文件的哪一节。全程不要碰 `.env`，也不要改动任何 Relay 相关的配置或生成文件。

**预期会看到什么**

- 大副会先给出这份安装当前 Relay 的开关状态（开或关），并说明判断依据是 `.env` 里那个 `FMX_PAIRING_TOKEN` 是不是非空 - 它会汇报「有没有」这个结论，而不会把令牌本身的内容念出来。
- 它会讲清楚令牌同意的是什么：公开回复，以及来自合法提及（按所有者路由认定为你本人）的正常可逆动作。
- 它会讲清楚令牌没同意的是什么：破坏性、不可逆、涉及安全的动作从来不由这个令牌授权，永远要走可信渠道确认，跟 Relay 开没开无关。
- 它会指出出处：`AGENTS.md` 第 14 节，以及 `docs/configuration.md` 的「Relay (.env)」一节。
- 它没有修改 `.env`，没有生成任何 Relay 相关的本地文件，也没有派出任何船员。

**怎么判断做成了**

三个都满足才算：它准确报告了当前的开关状态并说清楚判断依据；它把「同意了什么」和「永远不会自动做什么」讲成了两件分开的事，而不是含糊地说一句「Relay 比较安全」；以及 - 最关键的 - 它**没有改动任何文件**，也没有派出任何船员。

验证办法跟前几章一样，**前后对比**：提问之前在 FirstMate 目录里跑一次 `git status --short` 和 `git diff HEAD`，把两份输出都留着；问完之后再各跑一次，两次应该完全一样。`data/`、`state/`、`config/`、`projects/`、`.no-mistakes/` 和 `.env` 都是大副私有的运行状态，被 gitignore 掉了，这两条命令本来也看不见它们，会话期间读取（不是写入）这些也不算数。

如果它把「破坏性/不可逆/涉及安全的动作」也说成了打开 Relay 就能自动执行，或者它去改了 `.env`、生成了 Relay 相关的配置文件，那就是没做成。

## 全书完

十二章走到这里，这本教程从「船长、大副、船员各自是谁」讲到了「一个不是船长本人、却能触发大副做事的入口该怎么被约束」。中间穿过的是同一条线：无论请求从哪里来 - 你的一句话，一份侦察报告，一条公开提及 - 决定权在哪一步该停在谁手上，从来不是靠自觉，而是写进了权威文件、也写进了工具本身。希望你读完这十二章、做完每一章的动手练习之后，能把这套判断直接用在自己的真实项目上。
