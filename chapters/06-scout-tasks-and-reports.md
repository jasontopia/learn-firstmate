# 第 6 章：scout（侦察）任务与调查报告

## 这一章讲什么

第 2 到 5 章沿着**一件活**的旅程往下走：一句话怎么变成工单、船员怎么在隔离工作副本里干活、质检流水线怎么把关、PR 怎么等你点头合并。这些活有一个共同前提：它们都是**去改代码**的活。

这一章开始换一条线。第 6 到 8 章讲的是从单件活扩展到一支队伍要处理的事，而这条线的第一站，是回到立项那一刻的一个分岔口：这件活到底该不该去改代码。大副 / firstmate 会把每一件请求归成两种形态之一 - **ship**（出活）或者**scout**（侦察）。第 2 章已经带过这个分岔口一句，这一章把镜头完全对准它：什么信号该选侦察，什么时候不该选，侦察的产出长什么样、存在哪里，以及 - 最重要的一条 - 一份调查报告本身为什么从来不等于「去改代码」的授权。

本章依据的权威文件是 `AGENTS.md` 第 7 节「Intake and authority」和「Scout outcome and promotion」两个小节，以及第 2 节的布局表。每一段引用都会标出处。

## ship 与 scout：两种产出形态

`AGENTS.md` 第 7 节「Intake and authority」原文：

> Ship is the default and produces a project change through the selected delivery mode; once implementation is authorized, dispatch a ship and keep any remaining bounded research inside it unless unresolved uncertainty could materially change whether or what to build.
> Scout produces knowledge in `data/<id>/report.md`, never a PR, and is appropriate for investigation, diagnosis, planning, reproduction, or audit work when the captain explicitly requests a separate knowledge or design deliverable or unresolved uncertainty could materially change whether or what to build.

翻成大白话：**ship**（出活）是默认选项，产出的是一个真实的项目改动，走你选定的交付路径，最后落成一个 PR（或者本地合并）。一旦这件活已经被授权去实现，大副就直接派出一件 ship，而且但凡还剩下一点边界不清楚的调查工作，只要它不足以动摇「要不要做、做成什么样」这个大方向，就留在这件 ship 内部顺手做掉 - 不会为了一点小的不确定性另外再拆出一件侦察活。

**scout**（侦察）产出的不是项目改动，而是知识：一份写在 `data/<id>/report.md` 里的调查报告，永远不会开 PR。适合的场景是调查、诊断、规划、复现、审计这类工作，触发条件是两个之一：要么你明确要一份单独的知识或设计产出，要么眼下还有一处**不确定性大到可能改变要不要做、或者做成什么样**。

这个「不确定性是否足以改变方向」是判断该不该派侦察的核心标尺，而不是「这件事看起来有点复杂」或者「我想让人先探探路」。一件活里普通的、边界清楚的调查 - 比如去读一下某个模块现在怎么实现的 - 是留在 ship 里顺手做的事，不构成单独派侦察的理由。

## 什么时候不该派侦察

比「什么时候该派侦察」更容易被忽略的，是「什么时候不该」。同一节接着写：

> If established evidence already answers an informational question, relay it without a design-only scout; when implementation intent is unclear, answer and ask one concise implementation question when useful rather than dispatching speculative design work. Never both present a likely-enough solution and launch a parallel design exercise that is not expected to change it. A diagnostic request, report, recommendation, or implementation-ready finding is evidence, not authorization to change code.

拆成三条：

- **已有的证据已经能回答你的问题时，不要为了走流程再派一次纯设计性的侦察。** 如果一份现成的报告、一次代码阅读、或者既定的结论已经够用，大副应该直接把答案讲给你听，而不是把同一个问题再包装成一件新的侦察工单去重新调查一遍。
- **你的实现意图还不清楚时，该做的是问你一句简洁的话，而不是先斩后奏地去跑一次投机性的设计调查。** 「这东西该怎么改」如果连要不要改都还没定，大副的动作是问，不是先派一支队伍把方案设计出来等你看。
- **不能一边给你一个大概率就是对的方案，一边又平行跑一次预期不会改变这个方案的设计侦察。** 这是在浪费一支队伍的产能去确认一件已经足够确定的事。

这三条背后是同一句话：**一份诊断请求、一份报告、一条建议、或者一个已经具备实现条件的发现，都是证据，不是「去改代码」的授权。** 报告能告诉你「情况是这样」，但从来不能替你说出「所以照着做」。

## 报告长什么样，存在哪里

`AGENTS.md` 第 2 节的布局表这样定义侦察的产出物：

> `<id>/report.md` scout task deliverable, written by the crewmate; survives teardown

拆开看有两层意思。第一层是位置和作者：报告写在这件侦察任务自己的 `data/<id>/report.md` 里，由执行这件侦察的船员 / crewmate 写出来。第二层，也是容易被忽略的一层：**报告跟船员的工作副本不是一回事**。工作副本是船员干活用的临时地方 - 一份一次性的、隔离的 git 检出，事情办完之后会被收回（teardown）；报告是留下来的东西，工作副本被收回之后，报告依然在。

`AGENTS.md` 第 7 节「Scout outcome and promotion」把这个先后顺序钉得更死：

> A completed scout must leave a self-contained report before its scratch worktree can be discarded; read and relay its findings, record the report as the Done artifact, and re-evaluate the queue. A report may recommend implementation but does not authorize it.

也就是说，一件侦察任务的工作副本能不能被收回，前提是这份**自成一体**的报告已经写好并留下 - 报告写不出来，工作副本就不能被扔掉。大副读完报告、把结论转述给你、把这份报告记成这件工单的 Done 产物，再重新评估队列里还有哪些活因为这份新知识而值得动一动。而这份报告，即便它明确建议了「应该这么实现」，也依然不构成授权 - **一份报告可以推荐实现，但不能授权实现**。

## 报告变成活：promotion，而不是重新立项

一份侦察报告读完之后，如果你确实决定照着做，下一步不是让大副凭空立一件新的 ship 工单去重复调查一遍。同一节接着写：

> When implementation is separately authorized, promote the existing scout through `bin/fm-promote.sh` rather than creating a duplicate task. The promoted worker must inventory scratch state, return to a clean default-branch base, carry over only intended fix changes, create the ship branch, and follow the project's selected delivery path while leaving scratch commits and debug edits behind and turning a reproduced bug into the regression test.

这里的关键词是「separately authorized」- **单独**授权。侦察本身完成时并没有带着实现的授权；你读完报告，另外说一句「照着做」，这件事才算被单独授权。授权之后，大副走的是 `bin/fm-promote.sh` 把这件已有的侦察**提升**成一件 ship，而不是另开一件新工单去凭空重做一遍。这个提升过程本身也有讲究：被提升的船员要先清点自己在侦察阶段留下的临时状态，退回到一份干净的默认分支基线，只把真正要带进实现里的改动搬过来，再开一条新的 ship 分支，照选定的交付路径走下去 - 侦察阶段的草稿提交、调试用的临时改动都留在原地不带过来；如果侦察阶段复现过一个 bug，那次复现要在提升之后变成一条回归测试，而不是原样搬过去的调试脚本。

打一个比方（下面这段是**假设的场景**，不是这个仓库里真实发生过的事，纯粹用来帮你建立直觉）：假设你怀疑某个接口偶尔超时，但不确定是网络问题还是代码里某处死锁，你让大副派一支队伍去查。这支队伍最后交给你的是一份报告，写着「复现到了，是第 43 行那把锁在特定顺序下会死锁，建议这样改」。你读完这份报告，这一刻你手上有的是一个**结论**，还没有任何代码改动发生。你说「那就照这个改」之后，大副才会把这件侦察提升成一件 ship，由船员把死锁复现步骤变成一条回归测试，再实现修复，走质检流水线，开 PR。报告本身，从头到尾都没有直接产出任何项目改动。

## 动手练习

下面的练习是**只读**的：只是让大副读取信息、做推理并汇报，不会创建工单、不会派出真正的船员、不会改动任何被版本追踪的文件，也不会做任何不可回退的操作。你随时可以停下。

做练习前，先在你的 FirstMate 目录里启动一个 primary 会话，这样你面前的这个 agent 就是你的大副。

### 练习：拿三句话分别试一次 ship / scout 判断

对大副说：

> 大副，我要试一下你立项时怎么在 ship 和 scout 之间判断，不是真的要你干活。我依次给你三句话，请你对每一句话分别说清楚：你会把它归成 ship 还是 scout，理由是什么，以及如果归成 scout，报告最后会落在哪个文件里。第一句：「我们那个登录接口好像偶尔会超时，原因不知道，你先别改，帮我查清楚是哪里的问题，写份报告给我」。第二句：「刚才那份关于登录超时的报告我看完了，就按报告里建议的方案改」。第三句：「README 里现在有没有提到这个项目支持 Windows，直接告诉我就行」。这只是一次推演，不要真的创建工单，也不要派任何船员。

**预期会看到什么**

- 第一句：归成 scout，理由是原因不明、且这处不确定性会实质影响该怎么修 - 这正是派侦察的触发条件；它会说出报告会落在 `data/<id>/report.md`，并且指出这件事完成后工作副本会被收回、但报告会留下来。
- 第二句：归成 ship，理由是报告已经给出结论、你也明确说了「照着做」，这是一次独立的授权；它会提到这一步走的是 `bin/fm-promote.sh` 把已有的侦察提升成 ship，而不是另开一件新工单重新调查。
- 第三句：它会指出这是一个已有证据（README 本身）就能直接回答的问题，应该直接把答案讲给你听，不需要派任何侦察去调查。
- 三句话的判断都会点出处：`AGENTS.md` 第 7 节「Intake and authority」和「Scout outcome and promotion」。

**怎么判断做成了**

三个都满足才算：三句话的 ship/scout 归类都对，且理由讲的是「不确定性是否会改变要不要做、做成什么样」而不是「事情听起来复杂/简单」；它准确讲出了报告的位置和「报告不等于授权，需要你另外说一句才会提升成 ship」这条边界；以及 - 最关键的 - 它**没有创建任何工单，也没有派出任何船员**，你可以直接看一眼有没有新开的会话窗口来确认。

文件层面的验证办法跟前几章一样，**前后对比**：提问之前在 FirstMate 目录里跑一次 `git status --short` 和 `git diff HEAD`，把两份输出都留着；问完之后再各跑一次，两次应该完全一样。`data/`、`state/`、`config/`、`projects/`、`.no-mistakes/` 是大副私有的运行状态，被 gitignore 掉了，这两条命令本来也看不见，会话期间写这些不算数。

如果它把第二句也判断成了需要重新派一件侦察，或者把第一句直接当成了可以动手改代码的授权，那就是没做成。

## 下一章

第 7 章讲**backlog（工单）与船长决策**：工单队列怎么记录在办和待办的活，一个等你拍板的决策为什么本身也是一张工单，以及它怎么被关闭。
