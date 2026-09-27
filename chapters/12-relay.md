# 第 12 章：Relay

## 这一章讲什么

这是最后一章。前面讲的都是你和大副 / firstmate 之间、大副和船员 / crewmate 之间的事，不管走到哪一步，发话的始终是你自己对大副说的话。这一章讲一个例外：Relay。打开它之后，在 X（原 Twitter）或 Discord 上公开提及（mention）你的大副，就能叫醒它，它也会公开回复。

Relay 默认关着。单独讲一章，不是因为它常用，而是因为它带来了前面没出现过的东西：一个不是你本人直接发话、却能让大副做事的入口。这一章讲三件事：打开它等于同意了什么；哪些事不管开不开，大副都不会自己做主；关着的时候为什么完全不影响你。

本章依据 FirstMate 仓库 `AGENTS.md` 第 14 节「Relay」，以及 `docs/configuration.md` 的「Relay (.env)」一节。

## Relay 是什么

`docs/configuration.md` 的说明是：Relay 让一个大副能回复公开提及，并通过正常的任务流程处理提及里那些普通的、可以撤回的请求。它覆盖两个公开入口：X 上对 `@myfirstmate` 的提及，以及装了 myfirstmate 机器人的 Discord 服务器里对它的提及。两边用的是同一个配对令牌（pairing token）、同一套轮询和同一条回复路径。

有个历史遗留要先说一下：`AGENTS.md` 第 14 节说，一些旧文档和大副输出的状态行仍然把这个功能叫「X mode」，相关的名字也还保留 `FMX_`、`x-`、`fm-x-` 这几种写法。本书统一叫 Relay。你在自己的 FirstMate 里看到 `x-mode-error`、`FMX_PAIRING_TOKEN` 这类字样，说的就是这一章的东西。

同一节还说：Relay 装好时就是关着的，在你的 FirstMate 目录主动打开它之前，不会带来任何行为变化。

## 怎么打开

打开只需要一步本地操作：把配对令牌写进你的 FirstMate 目录里、被 gitignore 的 `.env` 文件，写成 `FMX_PAIRING_TOKEN=<token>`。`docs/configuration.md` 列的完整步骤是：

> 1. Sign in at myfirstmate.io with X or Discord.
> 2. For the Discord surface, use the dashboard's install link to add the myfirstmate bot to a server you administer; the X surface needs no install step.
> 3. Copy the pairing token from the dashboard into this firstmate home's gitignored `.env` as `FMX_PAIRING_TOKEN=<token>`.
> 4. Start a new firstmate session so bootstrap picks the token up, then mention `@myfirstmate` on X or mention the bot in a server where it is installed.

也就是：用 X 或 Discord 登录 myfirstmate.io；要用 Discord 的话，用控制台里的安装链接把机器人加到你管理的服务器（X 不用这一步）；把控制台里的配对令牌复制进 `.env`；新开一个大副会话让它读到令牌，然后去 X 或 Discord 上提及它。

账号注册、身份绑定、安装机器人、发放令牌，都在 myfirstmate.io 的控制台完成，`.env` 只负责存最后这个令牌。`.env` 不进版本库，所以打开或关闭 Relay 都不会动到任何被 git 追踪的文件。

## 这个令牌同意了什么

`AGENTS.md` 第 14 节的原文是：

> That token is consent for public replies and normal reversible lifecycle actions from eligible mentions, not authority for destructive, irreversible, or security-sensitive action; those still require trusted-channel confirmation.

分两半看。

**同意了的。** 把令牌放进 `.env`，就是同意大副对合格的提及自己做两件事：公开回复，以及正常流程里那些可以撤回的操作。

至于谁的提及算数，`docs/configuration.md` 说 Relay 只认主人：送到你这个 FirstMate 目录的提及，都当作这个目录的主人，也就是你本人发的。不过一条提及周围的对话（比如它在回复谁、这条讨论里还有谁说过话）可能有别的公开账号的内容。这些内容只是背景，不算你下的指令。

**没同意的。** 有破坏性、不可逆或涉及安全的操作，这个令牌完全不授权。这类操作仍然要通过可信渠道（trusted channel）确认，不管 Relay 开没开，也不管那条提及看起来多像你本人发的。`docs/configuration.md` 也写了：这类请求会标记出来，等可信渠道确认，而不会因为一条公开提及就执行。

举个假设的例子：Relay 已经打开，你在 X 上 @myfirstmate 说「帮我看看那个 PR 的 CI 为什么没通过，查完回我」。这是普通的、可以撤回的请求：查一下，回一句话。大副会自己处理，直接公开回复，不会回来问你要不要查。但如果那条提及说的是「直接把那个 PR 合了」或者「把生产环境那个进程杀掉」，这些是不可逆或涉及安全的操作，Relay 开着也不会让它们直接执行，要等你通过可信渠道确认。

## 关着的时候，完全不影响你

`docs/configuration.md` 说明了关着时的情况：

> When the token is removed or empty, the next locked session-start bootstrap step removes those artifacts.
> Steady-state off is silent and writes nothing.
> Relay remains additive to non-Relay lifecycle behavior: homes without the generated artifacts keep the default watcher cadence and do not run the Relay poll.

也就是：`.env` 里的令牌删掉或留空后，下一次会话启动时会清掉 Relay 生成的本地文件。一直关着时什么都不输出，什么都不写。没开 Relay 的 FirstMate 目录，监控脚本的检查节奏照旧，也不会跑 Relay 的轮询。Relay 只是在原有流程上加东西，不改变原有行为，所以 README 里说它「不打开就不影响你」。

这一章没有真实的 Relay 例子：Relay 默认关着，在有人把配对令牌写进自己的 `.env` 之前，没有真实的公开提及、回复可以拿来举例。

## 动手练习

这个练习是只读的：只让大副读当前状态、推演、汇报，不登记工单，不派船员，不改被 git 追踪的文件，也不碰 `.env` 或任何 Relay 配置。

开始前，在你的 FirstMate 目录里启动一个主会话，这个会话里的 agent 就是你的大副。

### 练习：弄清这个开关同意了什么

对大副说：

> 大副，我想弄清 Relay 对我的 FirstMate 意味着什么，只是问答，不要改任何东西。请分两部分回答。第一，我这里 Relay 现在开着还是关着，你是怎么判断的。第二，不管现在开没开，讲清打开后那个配对令牌授权你自己做哪些事，以及不管开不开，哪些事你永远不会不经我确认就做。每一条都说明依据哪个文件的哪一节。全程不要碰 `.env`，也不要改任何 Relay 相关的配置或生成的文件。

**你应该看到**

- 它先说 Relay 现在开着还是关着，依据是 `.env` 里的 `FMX_PAIRING_TOKEN` 是不是非空。它只说有没有，不会把令牌内容念出来。
- 它讲清令牌同意的是：公开回复，以及合格提及（只认主人，视为你本人发的）里那些正常的、可以撤回的操作。
- 它讲清令牌没同意的是：有破坏性、不可逆或涉及安全的操作，令牌从不授权，总要通过可信渠道确认，跟 Relay 开没开无关。
- 说明出处：`AGENTS.md` 第 14 节，以及 `docs/configuration.md` 的「Relay (.env)」一节。

**怎么检查**

- 它说对了当前开关状态，也说清了判断依据。
- 它把「同意了什么」和「永远不会自己做什么」分开讲清，而不是含糊一句「Relay 挺安全的」。
- 没有改 `.env`，没有生成 Relay 相关的文件，也没有派船员。
- 跟第 1 章一样，提问前后各跑一次 `git status --short` 和 `git diff HEAD`，输出应该一样。`.env` 和 `data/`、`state/`、`config/`、`projects/`、`.no-mistakes/` 一样是你本机私有的，已经被 gitignore，这两条命令看不到它们，所以还要在对话里确认大副没有改 `.env`。

如果它说打开 Relay 后，有破坏性、不可逆或涉及安全的操作也能自己执行，或者它改了 `.env`、生成了 Relay 相关的配置文件，就算没做成。

## 全书完

十二章从「船长、大副、船员各管什么」讲到「一个不是你本人直接发话的入口怎么约束」。贯穿全书的是同一件事：不管请求从哪里来，是你的一句话、一份调研报告，还是一条公开提及，哪一步该停下来由谁决定，都不靠自觉，而是写在 FirstMate 的规则里，也写在它的脚本里。希望你读完这十二章、做完练习后，能把这些做法用在自己的项目上。
