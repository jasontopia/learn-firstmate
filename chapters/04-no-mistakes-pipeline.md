# 第 4 章：no-mistakes 质检流水线

## 这一章讲什么

第 1 章说过，交付路径选定 no-mistakes 时，「review、修复、测试、文档、push、开 PR、CI 全部由 no-mistakes 独占」，流水线自己应用每一处修复，船员的角色是回应关卡，不是自己动手修。第 2 章讲的是立项那一步怎么把交付路径定下来。这一章把镜头对准 no-mistakes 这道关卡本身：它到底查什么、它自己能修到什么程度、什么情况下它会停下来不敢自己拍板、以及轮到大副 / firstmate 拍板时，它照什么规矩答。

本章依据的权威材料：no-mistakes 这个技能自身的一句话说明，以及 `AGENTS.md` 第 7 节「Task lifecycle」下的「Validate」小节和「Selected delivery path and merge authority」小节。「什么时候该问、问了该怎么答」这条判断规则的唯一出处是 `ask-user-authority` 这个技能 - `AGENTS.md` 第 7 节原话是「Load ask-user-authority before deciding any ask-user finding」，也就是说这条决策逻辑本身不在 `AGENTS.md` 里重复，而是单独交给这个技能定义。每个小节会指出具体出处。

## 流水线查什么、自己修什么

no-mistakes 这个技能的一句话说明写得很直接：「Validate your code changes through the no-mistakes pipeline - automated code review, tests, lint, docs, push, PR, and CI - before they reach the configured push target.」翻成大白话：自动代码审查、跑测试、跑 lint、查文档、push、开 PR、盯 CI，这一整条链路在你的改动落到配置好的推送目标之前一次跑完。

`AGENTS.md` 第 7 节「Selected delivery path and merge authority」把这条边界钉得更死：「When no-mistakes is selected, no-mistakes alone owns review, fixes, tests, documentation, push, PR, and CI」- 选定 no-mistakes 之后，这条链路上的每一步都只由它一家管，不会再叠加一个独立的人工审查关卡。第 1 章说过同一件事的另一半：流水线自己应用每一处修复，派去干活的船员在这条流水线里只负责回应关卡，不负责自己动手改代码去满足审查意见。

也就是说，「查什么」和「谁修」是同一件事的两面：流水线跑出来的每一条发现，只要它自己判断得出该怎么改，就自己改、自己提交、自己推进到下一关 - 不用等船员，也不等你。

## 什么时候它自己修不了，要停下来问人

流水线并不是每条发现都敢自己拍板。`AGENTS.md` 第 7 节「Validate」原话：「An ask-user finding returns as needs-decision; firstmate loads ask-user-authority and either decides or escalates per that skill.」也就是说，流水线遇到一类叫 ask-user 的发现时，不会自己选一个答案往下走，而是把这次运行的状态标成 needs-decision - 停在原地等一个决定 - 然后交给大副去判断。

这个决定**不归船员**。同一小节接着写：「The task worker that starts a no-mistakes run drives the pipeline and owns every no-mistakes axi run and no-mistakes axi respond call through the next gate or outcome. Firstmate never invokes no-mistakes axi respond for a crew-owned run.」意思是：启动这次 no-mistakes 运行的那个船员，负责一路把 `no-mistakes axi run` 和 `no-mistakes axi respond` 这两个命令喂下去，直到跑到下一关或者跑出结果；但轮到 ask-user 这一类发现，船员**不能自己回答**，必须原样把发现交给大副。这跟第 1 章讲过的规矩是同一件事在这里的体现：实现这件活的那个 worker 从不回答自己提出的发现。

## 大副怎么答：自己拍板还是升级给你

轮到大副接手判断的时候，规矩不是「大副想怎么答都行」。这条判断逻辑唯一的出处是 `ask-user-authority` 这个技能，原文写得很清楚：「Firstmate always applies this judgment, decides any finding that is unambiguous toward the accepted design, and escalates only genuinely ambiguous, expanding, or destructive findings. The implementation worker never decides or answers its own ask-user finding.」

这里的「accepted design」指的是这件活已经拍板、写进验收标准的那个设计 - 也就是第 2 章讲过的船长意图，加上你事后追加过的任何明确指示。判断一条发现该不该自己拍板，大副拿这个已拍板范围当尺子量，而不是凭感觉。拆开看，只有下面这几种情况大副才会往上交给你，其余一律自己拍板：

- 这次修复会实质性扩大交付契约 - 加一条新的保证、一个新子系统、一个新抽象、一个新的兼容面等等，而这些都不是已拍板范围里要的。
- 这是一个产品或架构判断，而已拍板范围里压根没定过这件事该怎么选。
- 同一个主题的发现反复出现 - 也就是一轮一轮地修，始终没修到根上。
- 这个选择本身是破坏性的、不可逆的，或者涉及安全。

除了这几种情况，大副会自己判断这条发现该怎么修 - 哪怕这个修复本身实现起来很复杂，只要它是已拍板范围之内的直接修正，就不升级给你。判断完之后，大副把决定喂回流水线，原话是「Send the same worker one exact decision naming the decision key, step, action, affected finding IDs, instructions where needed, and exact response command, passing --resolve-key so the worker's open decision record closes at answer time.」也就是这份决定必须点名：哪一条决策记录、哪一关、批准还是别的动作、影响哪几条发现 ID、需要的话给出具体做法，以及船员该敲的那条确切的 `no-mistakes axi respond` 命令。

## 一个真实发生过的例子

第 2 章写出来、合并成 PR 的那次活，交付路径就是 no-mistakes。那次运行在 test 这一关上出过一条 ask-user 发现：这次改动只是纯 markdown 文档，没有可交互的产品界面，流水线问的是「this change has no live-validatable surface; proceed without live validation?」- 要不要跳过现场验证直接往下走。

大副判断这条发现不涉及任何契约扩大：它既没有要求新增保证或新子系统，也不是一个悬而未决的产品判断，更谈不上破坏性或不可逆 - 单纯是一份文档改动确实没有能跑起来验证的界面。按 `ask-user-authority` 的规矩，这属于「unambiguous toward the accepted design」，大副自己拍板批准，指示船员执行 `no-mistakes axi respond --step test --action approve --reason '...'`，没有升级给船长。这也是本章前面两条规矩合在一起的样子：流水线自己判断不了，停下来问；大副接手后判断这条发现够不够格自己拍板，够格就直接答，不够格才会来找你。

## 动手练习

下面两个练习都是**只读**的：只是让大副读取信息、做推理并汇报，不会创建工单、不会启动真正的 no-mistakes 运行、不会派出真正的船员，也不会做任何不可回退的操作。你随时可以停下。

做练习前，先在你的 FirstMate 目录里启动一个 primary 会话，这样你面前的这个 agent 就是你的大副。

### 练习 1：拿两条假设的发现，测一次大副的判断

对大副说：

> 大副，我要试一下你在 no-mistakes 的 ask-user 发现上怎么拍板，不是真的要你跑流水线。假设有两条虚构的 ask-user 发现，都不需要你真的去查任何一件正在办的活：第一条是「测试里发现一个已批准设计中就该有的边界条件没覆盖，要不要现在补上这条回归测试」；第二条是「审查建议给这个功能加一层全局的持续监控和告警子系统，原本的验收标准里没有提过这个」。请你分别讲一遍，按 ask-user-authority 的规矩，你会自己拍板还是升级给我，以及为什么。这只是一次推演，不要去启动任何 no-mistakes 运行，也不要派任何船员。

**预期会看到什么**

- 第一条（补一条已批准设计要求的回归测试），它会判断为自己可以直接拍板 - 因为这是已拍板范围内的直接修正，不涉及任何契约扩大。
- 第二条（加一层原本没要求过的持续监控子系统），它会判断为必须升级给你 - 因为这加了一个已拍板范围之外的新子系统和持续监控要求，属于契约扩大。
- 它讲的判断依据是「这次修复会不会扩大交付契约」，而不是笼统地说「这个比较复杂 / 比较简单」。
- 它会点出出处：`ask-user-authority` 技能。

**怎么判断做成了**

三个都满足才算：两条发现给出的判断方向是对的（第一条自己拍板、第二条升级）；它讲出的理由落在「契约有没有被扩大」这条判断标准上，而不是别的标准；以及 - 最关键的 - 它**没有启动任何 no-mistakes 运行，也没有派出任何船员**，你可以直接看一眼有没有新开的会话窗口或者新的运行记录来确认。

文件层面的验证办法跟前面几章一样，**前后对比**：提问之前在 FirstMate 目录里跑一次 `git status --short` 和 `git diff HEAD`，把两份输出都留着；问完之后再各跑一次，两次应该完全一样。`data/`、`state/`、`config/`、`projects/`、`.no-mistakes/` 是大副私有的运行状态，被 gitignore 掉了，这两条命令本来也看不见，会话期间写这些不算数。

如果它把第二条也判断成了可以自己拍板，或者干脆真的去跑了一次 no-mistakes，那就是没做成。

### 练习 2：把一件真实发生过的 ask-user 决定拆回它的判断过程

练习 1 练的是推演两条假想的发现，这次练的是核对一条**真实发生过**的 ask-user 决定。

对大副说：

> 大副，回头看第 2 章那次活交付时，no-mistakes 在 test 这一关出过的那条 ask-user 发现 - 问的是这次改动没有可交互的验证界面、要不要跳过现场验证。讲清楚当时你是怎么按 ask-user-authority 判断这条发现该自己拍板还是该升级给我的，判断依据具体是哪几条，以及你最后给船员的确切指示是什么。如果这段记录已经不在了，就直接说清楚为什么找不到，而不是编一个说法。不要改任何文件，也不要派任何船员，只讲这件已经发生过的事。

**预期会看到什么**

- 它讲的是这次真实发生过的事，能带出你可以自己核对的东西 - 比如对应的 PR、或者当时给船员的确切 `no-mistakes axi respond` 指示。
- 它会明确说出判断落在「不涉及契约扩大、不是悬而未决的产品判断、不是反复出现的同主题发现、不涉及破坏性或不可逆」这几条上，而不是笼统地说「这个可以自己定」。
- 如果相关记录已经找不全，它会老实说找不到、说清楚可能的原因，而不是替你编一段听起来合理的判断过程。

**怎么判断做成了**

两条都满足才算：它讲的是可核对的真事，而且判断依据对得上 `ask-user-authority` 的标准；以及 - 找不到记录时它承认找不到，而不是编造。

文件层面的判断跟练习 1 一样：提问前后各跑一次 `git status --short` 和 `git diff HEAD`，两次输出应该一样，并且没有新开的船员会话窗口。

如果它把这次问答讲成了一次新的 no-mistakes 运行并打算真的跑一次，或者对记录缺失避而不谈、直接编了一段判断过程出来，那就是没做成。

## 下一章

第 5 章讲 **PR 与合并权限**：为什么默认必须你点头才合并，yolo 姿态放开了什么、没放开什么，以及红色 CI 为什么依然不能合。
