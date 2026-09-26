# 第 11 章：运行时与 harness 选择

## 这一章讲什么

第 9 到 11 章是路线图里「规模、离席、以及到底是哪个工具在跑你的船员」这条线，这一章是这条线的最后一站。前面几章讲的是队伍怎么拆分、怎么路由、离席时谁接手监督；这一章换一个更底层的问题：派出去的每一个船员 / crewmate，到底是被什么工具执行的，这个工具又跑在什么样的终端载体上。

这两件事经常被当成一回事，其实是两个正交（orthogonal，互不影响）的旋钮：**harness** 指跑在船员那份工作副本里的具体工具本身，比如 Claude Code；**运行时后端 / runtime backend** 指这个工具跑在什么样的终端会话载体上，比如一个 tmux 窗口。这一章讲清楚三件事：harness 和运行时后端为什么是两个独立的选择，默认情况下用的是什么，以及什么时候才值得为单独一件活指定别的 harness 或后端。

本章依据的权威文件是 `AGENTS.md` 第 4 节「Harness and runtime dispatch」和第 2 节「Layout and state」布局表里 `config/backend`、`config/crew-harness` 两行，`bin/fm-spawn.sh` 的头部注释，以及 `docs/configuration.md`「Harness support」一节。每一段引用都会标出处。

## harness 和运行时后端：两个正交的旋钮

`bin/fm-spawn.sh` 的头部注释把这两个东西写成了同一条命令里两个各自独立的参数：

> `fm-spawn.sh <task-id> <project-dir> --mode <no-mistakes|direct-PR|local-only> --yolo <on|off> [--branch-prefix <prefix>] [--harness <name>|harness|launch-command] [--model <name>] [--effort <level>] [--backend <name>]`

`--harness` 和 `--backend` 是两个不同的选项，互不依赖：改一个不需要跟着改另一个。这跟凭直觉理解的顺序可能有点反：很多人第一反应是「工具」和「跑在哪」应该是同一个设置，但这里从命令行参数的形状上就能看出来，FirstMate 把它们当成两件完全独立的事在管理。

`AGENTS.md` 第 4 节列出了 harness 这一侧可选的范围：

> The verified harnesses are `claude`, `codex`, `opencode`, `pi`, `pi-signed`, `grok`, `kimi`, `cursor`, and `omp`, plus `muse`, `gemini`, `rovo`, `agy`, and `devin` for crewmates and scouts only; never dispatch on an unverified adapter.

也就是说，harness 是一份经过验证的清单，`claude`、`codex`、`opencode`、`pi`、`pi-signed`、`grok`、`kimi`、`cursor`、`omp` 这九个对所有身份都可用，另外 `muse`、`gemini`、`rovo`、`agy`、`devin` 五个只对船员和侦察兵（scout）开放。清单之外的适配器，不管看起来多顺手，都不会被派上用场。

运行时后端这一侧，第 2 节布局表里 `config/backend` 这一行写的是：

> runtime session-provider backend override for new tasks; LOCAL, gitignored; absent = falls through to runtime auto-detection ..., then tmux; tmux is the verified reference backend, herdr has its own required CI lane, while zellij, orca, and cmux remain experimental with no dedicated real-backend CI lane

翻译过来：运行时后端管的是这个工具被塞进什么样的终端会话容器里去跑 - tmux 窗口是这里的参照实现（verified reference backend），herdr 有自己独立的必需 CI 测试通道，而 zellij、orca、cmux 目前还是实验性的，没有专门的真实后端 CI 通道兜底。这份清单本身，跟上面 harness 那份清单，是两份完全不相干的名单：`--harness` 和 `--backend` 这两个旋钮各自独立配置，改一个不需要跟着改另一个。但这不等于任意组合都能跑起来 - `fm-spawn` 在派出前仍会校验具体的 harness / 后端组合，遇到不支持的组合会直接拒绝。`docs/configuration.md`「Harness support」一节记录了一个具体例子：`fm-spawn.sh` 会在 preflight 阶段拒绝把 kimi 派到 cmux 或 Orca 后端上，因为回答 kimi 的 folder-trust 对话框需要一种这两个后端都不具备的、经过验证的仅视口（viewport-only）捕获能力。

## 默认情况下用什么

两边都有各自独立的默认值和兜底顺序。harness 这一侧，`AGENTS.md` 第 4 节写的路由优先级是：

> Routing precedence is an explicit per-task captain override, then the best-fit configured rule, then the configured default, then the static crewmate harness.

拆开看是一条从「这一件活单独说了什么」到「这个家一直以来配的是什么」的降级链条：先看你有没有对这一件活单独指定过；没有的话看有没有配置好的、跟这件活最匹配的规则；再没有就看有没有配置好的默认值；以上都没有，就落到最底层、静态配置的船员 harness（`config/crew-harness`，第 2 节布局表里写的是「crewmate harness override; ... absent or "default" = same as firstmate」- 不单独设置的话，跟大副自己用的 harness 一致）。

运行时后端这一侧，兜底顺序更简单，就是上一节引用过的那句：不设置 `config/backend` 的话，先落到运行时自动探测，探测不出结果的话再落到 tmux。两条链条彼此独立地往下降级，谁也不会去看另一边选了什么。

这个「不特意配置就一路落到静态默认值」的效果，能在这个教程仓库自己身上直接看到：从第 1 章到现在，这个仓库派出去的每一个船员用的都是同一个 harness - `claude`（Claude Code），跑在同一种运行时后端上。到目前为止没有一件活单独指定过别的 harness 或后端。原因很直接：写文档这件事从头到尾都是同质的，不需要任何特定工具才有的能力，静态默认值就已经够用，没有理由为哪一件活单独破例。

## 什么时候才值得为一件活单独指定

正因为默认路径已经够用，「单独指定」应该是例外，而不是顺手换着玩。`AGENTS.md` 第 4 节对单独指定后端划了一条明确的边界：

> Dispatch only on a backend that `fm-spawn` validates as spawn-capable; pass an explicit per-spawn `--backend` only under that exact task's own authority, never as later-task precedent.

两层意思：第一，只能派到 `fm-spawn` 自己验证过、确认能承载这个 harness 的后端上，不是随便指哪个都行。第二，也是更容易被忽略的一层 - 一次显式的 `--backend` 只对**这一件活自己**的授权范围有效，不会变成「以后这类活都这么办」的先例。也就是说，就算这一次为了某个特定需求指定了别的 harness 或后端，下一件活默认还是会走回静态配置，不会因为上一次这么干过就自动延续下去。

单独指定的正当理由，落在「这件活需要某个特定工具才具备的能力」这一类上 - 比如某个 harness 独有的一项功能是这件活非用不可的，而默认的静态 harness 并不具备。反过来，「随手试试另一个工具」「觉得换一个可能更快」都不构成理由。

同一节还写了一条配套的失败处理规矩，同样值得记住：

> A missing dependency, authentication failure, unsupported backend, or version refusal is a blocker; never silently retry on another backend.

也就是说，指定的 harness 或后端跑不起来 - 缺依赖、认证失败、后端不支持、版本被拒 - 这些情况下正确的动作是停下来报告成一个 blocker，而不是自己悄悄换一个后端接着跑。换后端本身不是问题，但换后端必须是一次可见的、有授权的决定，不能是遇到麻烦之后的自动补救动作。

## 动手练习

下面的练习是**只读**的：只是让大副读取信息、做推理并汇报，不会创建工单、不会派出真正的船员、不会改动任何被版本追踪的文件，也不会做任何不可回退的操作。你随时可以停下。

做练习前，先在你的 FirstMate 目录里启动一个 primary 会话，这样你面前的这个 agent 就是你的大副。

### 练习：核对这个教程仓库到目前为止的 harness / 后端选择，再推演一次单独指定

对大副说：

> 大副，我想核对两件事，都不是真的要你干活。第一件：这个 learn-firstmate 教程仓库从第 1 章写到现在，派出去的船员实际用的是哪个 harness、哪种运行时后端，是不是每一件活都一样，这是落到了静态默认值还是有哪一件活单独指定过。第二件，纯推演：假设未来有一件活，必须用到某个特定 harness 才有的一项能力，默认的船员 harness 没有这项能力，你会怎么处理 - 会不会单独指定一次 `--backend` 或者别的 harness，这次指定会不会变成以后同类活的先例，以及如果指定的后端起不来（比如认证失败）你会怎么办。请你分别说清楚，并点出你依据的是 `AGENTS.md` 哪一节。这只是核对和推演，不要真的创建工单，也不要派任何船员。

**预期会看到什么**

- 第一件事：它会说出这个仓库到目前为止所有船员用的都是同一个 harness（`claude`）、同一种运行时后端，且没有任何一件活单独指定过别的选择 - 这是落到了 `config/crew-harness` 和 `config/backend` 都缺省时的静态默认值，而不是巧合。
- 第二件事：它会讲清楚单独指定只在「这件活需要某个特定工具才有的能力」时才成立，且明确指出一次 `--backend` 的显式指定只对这一件活自己有效，不会变成以后同类活的先例；遇到认证失败这类情况，它会说要停下来报告成一个 blocker，而不是自己悄悄换一个后端重试。
- 它会点出出处：`AGENTS.md` 第 4 节「Harness and runtime dispatch」，以及第 2 节布局表里 `config/backend`、`config/crew-harness` 两行。

**怎么判断做成了**

三个都满足才算：它对这个仓库历史的描述是准确的（同一 harness、同一后端、没有单独指定过）；推演部分讲清楚了「单独指定不设先例」和「失败即 blocker、不悄悄换后端重试」这两条边界，而不是笼统地说「可以换一个试试」；以及 - 最关键的 - 它**没有创建任何工单，也没有派出任何船员**，你可以直接看一眼有没有新开的会话窗口来确认。

文件层面的验证办法跟前几章一样，**前后对比**：提问之前在 FirstMate 目录里跑一次 `git status --short` 和 `git diff HEAD`，把两份输出都留着；问完之后再各跑一次，两次应该完全一样。`data/`、`state/`、`config/`、`projects/`、`.no-mistakes/` 是大副私有的运行状态，被 gitignore 掉了，这两条命令本来也看不见，会话期间写这些不算数。

如果它把「单独指定一次 `--backend`」讲成了「以后这类活都会自动沿用这个选择」，或者把认证失败之类的问题讲成了「自己换个后端重试就行」，那就是没做成。

## 下一章

第 12 章讲 **Relay**：默认关闭的公开提及接入，开启它意味着授权了什么，以及哪些动作它永远不会自动替你做。
