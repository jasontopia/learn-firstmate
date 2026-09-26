# 第 2 章：如何提出一件活

## 这一章讲什么

第 1 章讲了三方分工和一件活从开口到落地合并要过的每一关。这一章把镜头拉近，只看第 0 关到第 1 关之间发生的事：你说的一句话，怎么被大副 / firstmate 变成一件可以派出去、也可以验收的活。

这一步定的东西，会决定后面每一关怎么走：这件活算谁的项目、产出是一份报告还是一个项目改动、走哪条交付路径、谁有权点头合并、以及流水线最后拿什么标准来判断这件活算不算做成了。这一章只讲这一步，不重复第 1 关之后的旅程 - 那是第 1 章已经走过的。

本章依据的权威文件，主要是 `AGENTS.md` 第 7 节「Task lifecycle」下的「Intake and authority」小节，按需引用 `bin/fm-brief.sh` 和 `bin/fm-project-mode.sh` 的头部注释。每个小节会指出具体出处。

## 大副在这一步要定三件事

一句话的请求进来之后，大副不会立刻去改代码，而是先做判断。判断结果落在三件事上：

1. **这是谁的项目。**
2. **产出形态是什么** - 报告还是项目改动，走哪条交付路径，谁有权合并。
3. **验收边界写在哪里** - 也就是这件活做成什么样才算做成了。

下面依次展开。

### 认项目

`AGENTS.md` 第 7 节「Intake and authority」原文：「Resolve the project independently for every request. An explicit project wins, a clear follow-up inherits its referent, and otherwise match the request against the registry, work under way, and project code or README. Proceed on one confident match while naming the project in plain language; ask one concise question when multiple or no projects plausibly match.」

翻成大白话：每一次请求都要独立判定项目归属，判定顺序是三层 - 你明确点了名的项目优先；如果这句话是接着上一句的追问，就沿用上一句认定的项目；两者都没有的话，才去拿这句话跟项目登记表、正在办的活、以及项目自己的代码和 README 做比对。只要有一个有把握的匹配，大副就直接推进，并且用平实的话说出它选了哪个项目 - 不会不声不响地就开始干。只有匹配不上或者匹配出好几个的时候，它才会停下来问你**一个**简洁的问题，而不是自己猜一个就上。

### 定交付形态：ship 还是 scout

同一小节接着定义了两种产出形态：「Ship is the default and produces a project change through the selected delivery mode... Scout produces knowledge in `data/<id>/report.md`, never a PR, and is appropriate for investigation, diagnosis, planning, reproduction, or audit work when the captain explicitly requests a separate knowledge or design deliverable or unresolved uncertainty could materially change whether or what to build.」

**ship**（出活）是默认，产出是一个真实的项目改动，走你选定的交付路径。**scout**（侦察）产出的是知识，落在 `data/<id>/report.md`，永远不开 PR - 适合调查、诊断、规划、复现、审计这类工作，前提是你明确要一份单独的知识或设计产出，或者眼下还有一处不确定会实质影响「要不要做、做成什么样」。

这里有一条边界值得单独说清楚：一份诊断报告、一个结论、一条建议，本身不等于「去改代码」的授权。同一小节写得很直接：「A diagnostic request, report, recommendation, or implementation-ready finding is evidence, not authorization to change code.」你读完一份侦察报告之后，还是得再说一句「照着做」，活才会真正进入 ship。反过来,如果一个已有的报告或既定证据已经能回答你的问题，大副也不会为了走流程再派一次侦察去重新调查一遍同一件事。

### 定交付路径：三选一，再加一个正交的合并姿态

同一小节接着定下更具体的东西：「Resolve every ship task's concrete delivery mode and yolo merge posture at intake. Pass the mode explicitly to the brief, and pass both values explicitly to the spawn and any scout promotion; each command refuses to guess the values it consumes. A current explicit captain instruction wins; otherwise the project's registry entry is the captain's standing posture, and dropping below its rigor needs a reason you can state.」

也就是说，交付路径和合并姿态这两个值，必须在立项这一刻就定死，而不是留到后面船员干活时再看着办 - 派工命令 `bin/fm-spawn.sh` 和把侦察升级成出活的 `bin/fm-promote.sh` 都要求这两个值显式传入，从不自己去猜。三条交付路径，出处是 `bin/fm-project-mode.sh` 的头部注释：

- **no-mistakes**：完整质检流水线 - 出活 -> `/no-mistakes` -> PR -> 配置好的合并权限方点头（默认）。
- **direct-PR**：不跑流水线，出活后直接用 gh-axi 推送并开 PR，等配置好的合并权限方点头。
- **local-only**：只在本地分支上出活，不推送、不开 PR，等配置好的合并权限方批准后，由大副走一条有守卫的本地快进合并。

`yolo`（合并姿态）是一个跟交付路径正交的开关，只管一件事 - 谁有权点头合并：关着，你批准每一次合并；开着，大副对绿色、且在授权范围内的活自己合并。这两个值**怎么定下来**，也有优先顺序：你当下明确说的话最优先；如果你没明确说，就用这个项目在登记表里的标准姿态；如果要比登记表里定的更松，大副得能说出一个理由。一个没登记过、或者压根没有登记表的项目，默认落在最严格的一档 - `no-mistakes` 加 `yolo` 关着，登记的缺口本身会上报给你。

### 定验收边界：写进简报的「船长意图」

前面两件事定完项目和形态之后，还差一件事：这件活做成什么样才算做成了。这个边界不是靠大副事后回忆你说过什么，而是写进派工前的任务简报（brief）里。`bin/fm-brief.sh` 的头部注释规定了简报里必须有的两段，且分开写：

一段是 `## Captain's intent`（船长意图）- 原文是「the captain's own ask plus the context needed to read it, including the substance of any report, decision, or PR the ask refers to, without added speaker labels or direct address」，也就是你自己的原话，加上读懂这句话所必需的上下文；如果你的话里提到了某份报告、某个决定、或者某个 PR 的具体条目，那些条目的**实际内容**也要写进来，而不是只留一个指针。另一段是 `## Firstmate spec`（大副规格）- 施工指令，这一段从来不算船长意图。

这两段为什么必须分开，第 1 章已经点过一句：质检流水线会把前一段当验收标准来读。这里补一句出处：`bin/fm-brief.sh` 的头部注释指出，`bin/fm-dod-lib.sh` 拥有把这两段喂给 `no-mistakes` 的 `--intent` 契约那份定义；派工命令还会拒绝任何留有占位符没填的简报，以及任何在「船长意图」段开头就带上对船长称呼或直接喊话的写法。

## 你怎么说，能少走弯路

把上面三件事倒过来看，就是你这边可以主动做的事：

- **想省一次追问，就把项目名字说出来，或者让这句话清楚地接着上一句。** 大副只在匹配不上或者匹配出好几个时才会停下来问你；一个明确点名的项目，或者一句清楚的追问，直接省掉这一步。
- **想清楚这活是要一份报告还是要真的改东西，就把这句话说明白。** 「帮我看看」和「去把它实现了」在大副眼里是两条完全不同的路 - 一个落 `data/<id>/report.md`，一个落项目改动加 PR。如果你自己也还没想清楚该不该做，大副会问你一句，而不是替你先斩后奏。
- **如果你想让这件活偏离这个项目登记的标准交付路径或合并姿态，就明说，并给个理由。** 沉默会被当成「用登记表里的标准姿态」；一句「这次直接开 PR 就行，不用走完整流水线」加一句理由，才会被当成有效的偏离。
- **如果你的话里引用了一份报告、一个决定、或者一个 PR 的某几条，把那几条的实际内容说出来，而不是只说「照着那份东西做」。** 验收标准只认写进简报里的话，一个孤零零的指针在流水线眼里等于没有上下文。
- **涉及合并、破坏性、不可逆、涉及安全的选择，点名说清楚要做的具体动作。** 这类选择永远停在你这里，一句宽泛的「你看着办」换不来授权 - 这也是第 1 章规矩二背后同一条道理在立项这一步的体现。

## 动手练习

下面两个练习都是**只读**的：只是让大副读取信息、做推理并汇报，不会创建工单、不会派出真正的船员、不会改动任何被版本追踪的文件，也不会做任何不可回退的操作。你随时可以停下。

做练习前，先在你的 FirstMate 目录里启动一个 primary 会话，这样你面前的这个 agent 就是你的大副。

### 练习 1：拿一句故意含糊的话试一次分类

对大副说：

> 大副，我要试一下你立项时怎么判断，不是真的要你干活。假设我只说了一句很含糊的话：「东西好像有点不对劲，帮我看看」- 没点名项目，也没说清楚是要一份报告还是要真的动手改。请你按平常立项的步骤，讲一遍你会怎么判断项目归属、会把它归成 ship 还是 scout、以及你会不会先停下来问我一个问题 - 如果会，那个问题是什么。这只是一次推演，不要真的创建工单，也不要派任何船员。

**预期会看到什么**

- 它会指出这句话在项目归属上是模糊的，因为既没有点名项目，也不是接着某个具体项目的追问。
- 它会说因为无法确认唯一匹配，按规矩会停下来问你**一个**简洁的问题，而不是自己挑一个项目就往下走。
- 它会指出「帮我看看」这类措辞本身也没有说清是要报告还是要真的动手改，所以形态判断（ship / scout）同样需要先问清楚，或者至少会指出这处不确定性。
- 它会点出出处：`AGENTS.md` 第 7 节 "Intake and authority"。

**怎么判断做成了**

三个都满足才算：它讲清楚了「为什么这句话触发追问」而不是替你瞎猜一个项目就往下推进；它给出了可核对的出处；以及 - 最关键的 - 它**没有创建任何工单，也没有派出任何船员**，你可以直接看一眼有没有新开的会话窗口来确认。

文件层面的验证办法跟第 1 章一样，**前后对比**：提问之前在 FirstMate 目录里跑一次 `git status --short` 和 `git diff HEAD`，把两份输出都留着；问完之后再各跑一次，两次应该完全一样。`data/`、`state/`、`config/`、`projects/`、`.no-mistakes/` 是大副私有的运行状态，被 gitignore 掉了，这两条命令本来也看不见，会话期间写这些不算数。

如果它没问就自己挑了个项目往下走，或者把这句含糊的话直接当成了 ship 的施工授权，那就是没做成。

### 练习 2：把一件已经落地的活，拆回它的立项决定

练习 1 练的是推演一件假想的活，这次练的是核对一件**真实发生过**的立项决定。这个仓库本身就有现成的材料：`AGENTS.md` 第 1 节的四条硬规矩讲过，一件活从开口到合并的每一步都要留痕，第 1 章写出来、合并成 PR 的那件活，以及给这个仓库加上真实 CI 检查的那件活，都是可以拿来核对的真实例子。

对大副说：

> 大副，回头看这个仓库已经做完的一件活 - 比如写出第一章《FirstMate 是什么》那次，或者给这个仓库加真实 CI 检查那次。讲清楚立项那一刻定下的三件事：这件活当时是怎么认定归属这个项目的，它被归成了 ship 还是 scout，走的是 no-mistakes、direct-PR 还是 local-only，yolo 合并姿态开没开，以及当初写进简报「船长意图」那段的验收边界大致是什么。如果这些记录已经不在了，就直接说清楚为什么找不到，而不是编一个说法。不要改任何文件，也不要派任何船员，只讲这件已经发生过的事。

**预期会看到什么**

- 它讲的是这两件真实活里的一件，带得出你能自己核对的东西 - 比如对应的 PR 链接或者提交记录，而不是抽象地复述规则。
- 它会明确区分项目归属、ship/scout 判断、交付路径、`yolo` 姿态、验收边界这几件事分别是什么，而不是笼统地说「按规矩走的」。
- 如果当初的工单笔记或简报因为清理、归档、或者只保留近期 Done 记录这类原因已经找不到完整原文，它会老实说找不到、说清楚可能的原因，而不是替你编一段听起来合理的「船长意图」。

**怎么判断做成了**

两条都满足才算：它讲的是可核对的真事，不是泛泛的规则复述；以及 - 找不到记录时它承认找不到，而不是编造。

文件层面的判断跟练习 1 一样：提问前后各跑一次 `git status --short` 和 `git diff HEAD`，两次输出应该一样，并且没有新开的船员会话窗口。

如果它把这次问答本身讲成了一件新的活并打算立项，或者对记录缺失避而不谈、直接编了一段验收边界出来，那就是没做成。

## 下一章

第 3 章讲**船员与隔离工作副本**：每个船员为什么要在自己的一份 git 工作副本里干活，并行的多件活为什么不会互相踩，出事时怎么看。
