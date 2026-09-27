# 第 11 章：harness 与运行时后端

## 这一章讲什么

前面几章讲队伍怎么分工、怎么分派、你走开时谁来监督。这一章讲一个更底层的问题：每个船员 / crewmate 到底是用什么工具在跑，这个工具又跑在什么终端里。

这是两件事，而且互不影响：

- **harness**：在船员的工作树里实际干活的 agent 工具，比如 Claude Code。
- **运行时后端**（runtime backend）：给这个工具提供会话窗口的终端工具，比如 tmux。

这一章讲清三件事：为什么这是两个独立的选择，默认用的是什么，什么时候才值得为某一件活单独指定。

本章依据 FirstMate 仓库 `AGENTS.md` 第 4 节「Harness and runtime dispatch」、第 2 节目录说明里 `config/backend` 和 `config/crew-harness` 两行、`bin/fm-spawn.sh` 开头的注释，以及 `docs/configuration.md` 的「Harness support」一节。

## 两个独立的选择

`bin/fm-spawn.sh` 的注释里，这两项是同一条命令里两个独立的参数：

> `fm-spawn.sh <task-id> <project-dir> --mode <no-mistakes|direct-PR|local-only> --yolo <on|off> [--branch-prefix <prefix>] [--harness <name>|harness|launch-command] [--model <name>] [--effort <level>] [--backend <name>]`

`--harness` 和 `--backend` 是两个参数，改一个不用跟着改另一个。

**harness 能选哪些。** `AGENTS.md` 第 4 节列了验证过的 harness：`claude`、`codex`、`opencode`、`pi`、`pi-signed`、`grok`、`kimi`、`cursor`、`omp` 这九个；另外 `muse`、`gemini`、`rovo`、`agy`、`devin` 五个只能用于船员和调研任务。清单以外的，不管看起来多顺手，都不会用来派活。

**运行时后端能选哪些。** 第 2 节对 `config/backend` 的说明是：tmux 是验证过的标准后端；herdr 有自己必须通过的 CI 测试；zellij、orca、cmux 还是实验性的，没有专门跑真实后端的 CI 测试。

两份清单互不相干，但不是任意组合都能跑。`fm-spawn.sh` 派出前会检查具体的组合，不支持的直接拒绝。`docs/configuration.md` 的「Harness support」一节举了一个例子：`fm-spawn.sh` 会在启动前的检查里拒绝把 kimi 派到 cmux 或 Orca 上，因为处理 kimi 的「是否信任此文件夹」对话框，需要一种经过验证的、只截取当前可见画面的能力，这两个后端都没有。

## 默认用什么

两边各有自己的默认值和兜底顺序。

**harness。** 第 4 节规定的顺序是：

1. 你对这一件活单独指定的。
2. 配置好的、跟这件活最匹配的规则。
3. 配置好的默认值。
4. 静态的船员 harness，也就是 `config/crew-harness`。第 2 节说明，这个文件不存在或写着 `default`，就跟大副自己用的 harness 一样。

**运行时后端。** 没设 `config/backend`，就用运行时自动检测的结果（大副自己正在哪种终端里跑）；检测不出来，就用 tmux。

两边各自往下找，谁也不看对方选了什么。所以一件活只要不需要某个工具特有的能力，也没人为它单独传 `--harness` 或 `--backend`，harness 就一路落到 `config/crew-harness`（没设就跟大副一样），后端就落到自动检测的结果或 tmux。写文档这类活，通常用默认值就够了。你的 FirstMate 实际用的是哪个 harness、哪种后端，下面的练习会让你直接问你的大副，这里不替你下结论。

## 什么时候值得单独指定

默认值已经够用，所以单独指定应该是例外。第 4 节对单独指定后端划了边界：

> Dispatch only on a backend that `fm-spawn` validates as spawn-capable; pass an explicit per-spawn `--backend` only under that exact task's own authority, never as later-task precedent.

两层意思：

- 只能派到 `fm-spawn` 验证过能用的后端上，不是想指哪个就指哪个。
- 单独传一次 `--backend`，只对这一件活有效，不会变成以后同类活的先例。下一件活默认还是走回配置好的设置。

单独指定的正当理由是：这件活需要某个工具特有的能力，默认的工具没有。「随手试试另一个」「觉得换一个可能更快」都不算理由。

同一节还规定了跑不起来时怎么办：

> A missing dependency, authentication failure, unsupported backend, or version refusal is a blocker; never silently retry on another backend.

缺依赖、认证失败、后端不支持、版本被拒，都算阻塞，要停下来报告，不能自己悄悄换一个后端重试。换后端本身没问题，但必须是一次看得见、有授权的决定，不能是遇到麻烦后的自动补救。

## 动手练习

这个练习是只读的：只让大副读资料、推演、汇报，不登记工单，不派船员，不改被 git 追踪的文件。

开始前，在你的 FirstMate 目录里启动一个主会话，这个会话里的 agent 就是你的大副。

### 练习：核对这个仓库用过的 harness 和后端，再推演一次单独指定

对大副说：

> 大副，我想核对两件事，都不是真要你干活。第一件：learn-firstmate 这个教程仓库从第 1 章写到现在，派出去的船员实际用的是哪个 harness、哪种运行时后端，每件活是不是都一样，是用的默认设置，还是有哪件活单独指定过。第二件，只推演：假设以后有一件活必须用到某个 harness 特有的能力，默认的船员 harness 没有，你会怎么处理？会不会为它单独指定 harness 或 `--backend`？这次指定会不会成为以后同类活的先例？如果指定的后端起不来，比如认证失败，你怎么办？请分别说清，并说明依据 `AGENTS.md` 哪一节。只核对和推演，不要登记工单，也不要派船员。

**你应该看到**

- 第一件：它如实说出这个仓库到现在实际用的 harness 和后端，每件活是否一样，是 `config/crew-harness` 和 `config/backend` 没设时的默认值，还是某件活单独指定过。以它自己查到的记录为准，这一章不预设答案。
- 第二件：它讲清只有这件活需要某个工具特有的能力时才单独指定；单独传一次 `--backend` 只对这一件活有效，不成为先例；认证失败这类情况要停下来报告阻塞，不自己悄悄换后端重试。
- 说明出处：`AGENTS.md` 第 4 节「Harness and runtime dispatch」，以及第 2 节里 `config/backend`、`config/crew-harness` 两行。

**怎么检查**

- 第一件讲的跟它实际查到的记录一致：用的是默认值还是单独指定过，都如实说，不想当然地说「肯定是默认的」。
- 第二件讲清了「单独指定不成为先例」和「起不来就报告阻塞，不悄悄换后端」这两条，而不是笼统一句「可以换一个试试」。
- 没有登记工单，也没有多出新的船员窗口。
- 跟第 1 章一样，提问前后各跑一次 `git status --short` 和 `git diff HEAD`，输出应该一样。

如果它说单独指定一次 `--backend` 以后同类活都会沿用，或者说认证失败就自己换个后端重试，就算没做成。

## 下一章

第 12 章讲 Relay：默认关着的公开提及功能，打开它等于同意了什么，哪些事它永远不会自己做。
