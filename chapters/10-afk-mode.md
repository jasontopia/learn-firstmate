# 第 10 章：离席模式（afk）

## 这一章讲什么

你（船长 / captain）不可能一直守在屏幕前，但队伍不能因为你走开就没人管。这一章讲离席模式（afk）：你走开时谁接手监督；你说「离席」这句话是不是马上生效；离席期间大副 / firstmate 能凭你留下的话做到哪一步；遇到真正要紧的选择时它会不会停下来等你；你回来时它怎么先把这段时间的事交代清楚。

本章依据 FirstMate 仓库 `AGENTS.md` 第 8 节里的「Away-mode and quiet-mode stub」小节，以及 `/afk` 技能（`.agents/skills/afk/SKILL.md`）。这本教程写作期间船长一直在场，没有真正用过离席模式，所以本章没有真实案例，用到的场景都是假设的，会标出来。

## 你走开后谁在监督

原文是 "While `state/.afk` exists, the daemon owns supervision; do not arm a separate watcher."。

你走开后监督不会停，而是交给一个专门的守护进程（daemon）。只有它一个在管，大副不会再另外启动一个监控脚本做同样的事。你走开后，队伍仍然有人看着，只是换了一个看着它的。

## 说出 `/afk`，就已经生效

前面几章里，你说一句话，大副通常先讲清打算怎么做，再动手。离席模式不一样。原文是：

> `state/.afk-contract` is the away posture, written in the same turn as `/afk` before any other work, because `/afk` is itself the go: no read-back gates entry or waits for a go; entry announces hold-for-return only, and the away session acts on those words by its own judgment through the guarded scripts under standing authority, holding for the return on doubt.

意思是：你说 `/afk` 加上你交代的话，本身就是「开始」，不是「请你批准」。大副会在同一轮、做任何别的事之前，先把你的话原样记下来（`state/.afk-contract`），因为再等你确认，你可能已经走了、看不到屏幕了。它接着会告诉你：没把握的事会留着等你回来。然后它用自己的话把你交代的内容复述一遍，说明哪句话离席期间做不了。这些只是告知，不是在等你点头，你的话说完就已经生效。如果它理解错了，你再发一次 `/afk` 加上新的话就行。

## 离席期间大副能做到哪一步

上面那段原文的后半句划了范围：离席期间，大副根据你留下的话，用本来就允许用的、带保护的脚本做事，由它自己判断你的话管不管得到眼下这件事，拿不准就留着等你回来。

这里有两层意思：

- 它用的是本来就允许用的、带保护的现有流程，不会临时另搞一套做法。
- 你的话管不管得到眼下这件事，由它自己判断，不是机械地匹配关键词。拿不准时，答案总是等你回来，而不是「问题不大，我自己拿主意」。

## 离席不会放宽底线

原文写得很清楚：

> Away and quiet mode never expand approval authority for merges, ask-user findings, destructive actions, irreversible actions, or security-sensitive choices.

离席模式（`/afk`）和静默模式（`/quiet`）都不会让大副在合并、ask-user 类问题、破坏性操作、不可逆操作、涉及安全的选择这几类事上，拥有比你在场时更大的权限。

`/afk` 技能说得更直接：有破坏性、不可逆或涉及安全的操作，不管你走之前怎么说，都不能提前授权。ask-user 类问题照常按 `ask-user-authority` 的规矩处理，除非你留下的话正好回答了那个具体问题。其他需要你决定的事，都留着等你回来。所以，哪怕你临走前说过「遇到这种情况你就自己改」，只要那件事有破坏性、不可逆或涉及安全，大副仍然会留着等你。离席解决的是谁来盯着、一般的活怎么往前推，不会把这几道关也交出去。

## 你回来了：先交代，再干活

大副怎么知道你回来了？原文是：

> A marked message while away or quiet mode is active is internal escalation and does not exit that mode. Any other unmarked message means the captain returned in away mode (load `/afk`, run the return owner, and do not process that message as ordinary work until its durable catch-up gate clears)... Bias ambiguous input toward exit because a present captain takes precedence.

大副能分清两种消息：

- 一种是监督机制内部发来的、带特定标记的消息。这不算你回来，离席模式照旧。
- 另一种是任何不带标记的普通消息，哪怕只是随口一句、没带 `/afk`，都当作你回来了。

拿不准时，就当你回来了，因为你在场时以你为准。

判断你回来后，大副不会直接接着你那句话干活，而是先跑一遍回来后的交接流程，把离席期间发生的事交代清楚。交接完成之前，你那句话不当作普通的活来处理。

举个假设的例子：你交代了一句「按流程正常推进」就走了，回来后只问了句「现在几点了」。大副不会先回答几点，而是先讲清这段时间队伍做了什么、还有哪些事在等你，交代完才回答你几点了。

## 动手练习

这个练习是只读的，而且只在对话里推演：不创建也不修改 `state/.afk-contract`、`state/.afk` 这类文件，不真的运行 `/afk` 或相关脚本，不派船员，不改被 git 追踪的文件。

开始前，在你的 FirstMate 目录里启动一个主会话，这个会话里的 agent 就是你的大副。

### 练习：推演一次离席，但不真的进入离席模式

对大副说：

> 大副，我想跟你推演一下离席模式的规矩，不是真要你进入离席模式：不要创建或修改 `state/.afk-contract` 和 `state/.afk`，也不要真的运行 `/afk` 或相关脚本。假设我刚说了一句：「/afk，已经走完质检流水线的活，你就按原来的节奏往下推，其他都留着等我。」不要执行这句话，只在纸面上推演，回答四个问题。一：这段时间谁替你盯着队伍？二：我这句话要等你确认、我点头才算数，还是说完就生效了？三：如果这期间有一件活走完了质检流水线，你怎么处理？如果同时冒出一件必须强推、覆盖别人已提交历史才能推进的事，你会不会因为我说了「按原来的节奏往下推」就去做？四：推演到这里结束，之后我随口发一句不带 `/afk` 的话，比如「现在几点了」，你会直接回答，还是先做点别的？

**你应该看到**

- 第一问：由一个专门的守护进程接管监督，不会再另外启动一个监控脚本。
- 第二问：说完就生效，已经记下来了，不等你确认。它之后复述你的话只是告知，不是在等你点头；理解错了，你再发一次 `/afk` 纠正。
- 第三问：走完流水线、按原来节奏推进，是你的话管得到的，也走的是本来就允许的流程，它会自己判断往下推，不会特意来问你。但强推、覆盖别人历史是有破坏性、不可逆的操作，不会因为你那句话就放开，它会留着等你回来。
- 第四问：它会先把离席期间的事交代清楚，交代完才把「现在几点了」当普通问题回答。它还会指出，如果是监督机制内部发来的、带标记的消息，就不算你回来，不会触发交接。
- 说明出处：`AGENTS.md` 第 8 节「Away-mode and quiet-mode stub」，以及 `/afk` 技能。

**怎么检查**

- 第一问讲对了守护进程接管，而且不另外启动监控脚本。
- 第二问讲对了说完就生效，而不是「要先跟你确认」。
- 第三问两半都讲对：你授权范围内的活可以自己判断往下推；有破坏性、不可逆的操作不会因为你的话放开。少了后一半就不算对。
- 第四问讲对了先交代、再回答。
- 它没有说自己创建或修改了 `state/.afk-contract`、`state/.afk`，也没有真的运行 `/afk`。
- 跟第 1 章一样，提问前后各跑一次 `git status --short` 和 `git diff HEAD`，输出应该一样。`state/` 是你本机私有的目录，已经被 gitignore，这两条命令看不到它，所以还要在对话里确认大副没有动这些文件。

如果它说离席期间没人管，或者说 `/afk` 要先确认才算数，或者认为你说了「按原来的节奏往下推」连强推覆盖历史也能做，或者收到你那句话后直接回答、不先交代，就算没做成。

## 下一章

第 11 章讲 harness 与运行时后端：船员是用什么工具、在什么终端里跑的，默认怎么选，什么时候值得单独指定。
