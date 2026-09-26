# 第 8 章：supervision（监督）与唤醒机制

## 这一章讲什么

第 6 章讲了侦察任务怎么产出一份报告，第 7 章讲了工单队列怎么记录在办和待办的活、以及一个决策本身怎么变成一张工单。这两章都是从**一件活**的角度看问题。这一章把镜头拉远：当队伍里同时有好几件活在跑的时候，大副 / firstmate 怎么盯住整支船员 / crewmate 队伍，而不需要为了「盯着」这件事本身持续消耗 token。

这一章只回答三个问题：大副是怎么在没有事情发生的时候完全不跑、不烧 token 的；几种唤醒（wake）事件分别代表什么；唤醒之后，哪些事大副自己按规矩就能拍板，哪些才轮到船长 / captain 被打扰。二副 / second mate 怎么帮大副分担这些监督工作，是下一章的内容，这里不展开。

本章依据的权威文件：FirstMate 仓库 `AGENTS.md` 第 8 节「Supervision protocol」和第 9 节「Escalation and captain etiquette」，以及 `docs/architecture.md` 里「Event-driven supervision」一节和 `bin/fm-watch.sh`、`bin/fm-crew-state.sh` 的头部注释。每个小节会指出具体出处。

## 大副不是靠死循环盯着队伍的

如果大副要盯住三件同时在跑的活，最直觉的做法是：开一个循环，每隔几秒就把三件活的状态都问一遍模型「有没有变化」。这样做能盯住，但代价是那个循环里的每一次询问都是一次真实的模型调用 - 队伍越大、活跑得越久，这个盯梢的开销就越大，而且跟活本身有没有进展毫无关系。

FirstMate 不是这样做的。`docs/architecture.md`「Event-driven supervision」一节开头写得很直接：「A zero-token bash watcher (`bin/fm-watch.sh`) sleeps on the fleet, classifies detected wakes in bash, and wakes the first mate only when something is actionable.」

翻成大白话：真正「盯着」船员队伍的，是一个纯 bash 脚本，不是大副这个模型会话。这个脚本自己睡着等，用 shell 逻辑去分类它看到的各种动静，只有当动静够得上「需要大副处理」这条线时，才把大副的会话叫醒。`bin/fm-watch.sh` 的头部注释补了一句关键的话：它默默吸收掉良性的动静，继续睡着等下去；只有真正需要处理的唤醒，才会让它退出并把控制权交还给大副。

这解释了「不烧 token」这件事到底是怎么成立的：

- 没有唤醒的时候，大副的会话**根本不在跑**，不产生任何模型调用，自然没有 token 开销。
- 大部分动静（比如某个船员的质检流水线正常地往下走了一步）被这个 bash 脚本自己判定成良性、直接吸收掉，连叫醒大副这一步都省了。
- 只有动静够得上「大副需要来处理」的门槛，大副的会话才被真正唤醒一次，处理完之后再度回到不跑的状态。

所以这一章标题里的「不烧 token」不是一句宣传语，而是一个具体的架构选择：把「持续盯着」这件需要一直运行、但绝大多数时候什么也不用做的工作，交给一个不花钱的 shell 脚本；把「需要判断、需要拍板」这种真正要用到模型的工作，只留给被叫醒之后的大副。

## 四种唤醒事件

`AGENTS.md` 第 8 节把每一次真正传到大副手上的唤醒，按处理方式分成四种。原文：

> 1. For `signal:`, read the listed event lines first, then reconcile current state only where action depends on it.
> 2. For `stale:`, inspect the recorded endpoint and load `stuck-crewmate-recovery` for a stopped, looping, confused, or unresponsive worker.
> 3. For `check:`, act on the named poll result, including merges, contribution signals...
> 4. For `heartbeat:`, review the whole fleet from the structured fleet view, reconcile suspicious tasks and PR state, update the backlog, and never report an unchanged fleet as progress.

翻成大白话，这四种唤醒分别对应四种不同的动静：

- **signal（信号）**：某个船员自己往状态文件里写了一行，比如「活干完了」「卡在一个需要拍板的地方了」。大副先读这行写了什么，只有当接下来要做的事真的依赖「现在到底是什么状态」时，才去核对当前状态 - 不是每次都要核对。
- **stale（安静太久）**：一个船员安静了超过预期的时长，看起来可能停了、在死循环、或者卡住了。这不是「已经确认出问题」，只是「该去看一眼了」的提示。
- **check（查询式检查结果）**：大副自己派出去的某个后台查询有了结果 - 比如 PR 有没有合并、有没有新的外部贡献信号。这是「问出去的问题有答案了」，不是船员主动喊的。
- **heartbeat（心跳）**：一个兜底的、按固定节奏触发的全队检查，逼着大副把整支队伍从头看一遍，核对有没有可疑的任务或 PR 状态、更新一下工单队列 - 而且明确不允许把「队伍状态没变化」本身当成一条汇报给船长的进展。

四种唤醒里，只有第一种（signal）是船员自己主动喊的；剩下三种都是大副自己安排的机制在替它盯梢的产物。

### status line 是事件，不是当前状态

第 8 节紧接着这四条之后，补了一句对新手最容易踩坑的话：「A status line is a wake event, not current state; use `bin/fm-crew-state.sh` when current state matters, especially before re-escalating an old decision, blocker, or pause.」

意思是：船员写进状态文件的那一行（比如「done: ...」），记录的是**它写下那一刻**发生了什么，不是「现在」的状态。一个船员可能在写完「blocked: ...」之后，等大副回应、它自己继续把活推进下去了 - 但状态文件的最后一行还停在那句旧的 `blocked:` 上，如果只看这一行，会误以为它还卡着。`bin/fm-crew-state.sh` 的头部注释把这个问题说得更直白：状态文件是一份「只增不改的事件日志」，船员只在真正值得叫醒大副的时刻才往里写一行，悄悄恢复干活时什么也不写，所以直接看这份日志的最后一行，读到的是**最后一次事件**，不是**当前状态**。这个脚本会去读权威源头（比如质检流水线自己记录的运行步骤、或者会话端点是不是正忙着），把可能过时的日志和这份权威状态对一遍，再吐出一行报告，格式大致是：

```
state: <working|parked|done|blocked|paused|failed|unknown> · source: <run-step|pane|status-log|remote-endpoint|none> · <detail>
```

`AGENTS.md` 特别点名：在要重新去打扰船长之前 - 尤其是那种「之前搁置的一个决策/阻塞/等待，是不是还悬着」 - 必须先用这个工具核对一遍当前状态，不能只凭一条旧的状态行就动作。

## 案例：一次被误判成「卡住了」的 stale 唤醒

打一个比方（下面这段是**假设的场景**，不是这个仓库里真实发生过的事，纯粹用来帮你建立直觉）：假设某个船员的质检流水线正在后台跑着，一时半会儿没有新的动静。负责盯梢的机制把这段安静判定成 `stale` 唤醒，把大副叫醒去看一眼，理由是「这个船员看起来可能卡住了」。

大副没有直接信这条唤醒本身的措辞。按上面那条规矩，`stale` 只是一个「该去看一眼」的提示，不等于「已经确认卡住」。它跑了一次 `bin/fm-crew-state.sh`，核对权威的当前状态 - 结果发现这个船员其实正处在「验证中」这个完全正常的阶段，质检流水线还在按部就班地往下走，没有任何异常。大副什么也没做，唤醒处理完了，继续回到不跑的状态。

这正好对应上一节那条规矩：一次唤醒只是「叫你来看一眼」的事件，不能替代对当前状态的核对。如果大副当时直接信了「安静太久 = 卡住了」这条唤醒的字面意思，可能就会去做一次没必要的介入，甚至去打扰船长确认要不要重启这个船员 - 而实际上什么都没坏。

## 唤醒之后，什么该自己拍板，什么才轮到船长

四种唤醒被处理之后，绝大多数都不会走到「去找船长说一句话」这一步。上面那个案例就是这样：一次 `stale` 唤醒，核对完发现一切正常，处理到此结束，船长完全不知道这件事发生过 - 这本身就没什么该知道的。`AGENTS.md` 第 9 节「Escalation and captain etiquette」把这条原则写得很直接：「Waiting on a healthy supervision cycle is silent; empty polls, elapsed time, and no-change updates are not captain-facing progress.」空转的轮询、单纯过去的时间、没有变化的检查结果，本身都不是该报给船长的进展。

同一节接着列出了真正需要马上去找船长的几种情形，原文摘录：

> Reach the captain immediately for:
> - Work ready for their review, with the PR's recorded URL.
> - Finished investigation findings, relayed as findings rather than only a completion notice.
> - Gate findings that `ask-user-authority` escalates.
> - A real blocker or failure after the relevant playbook is exhausted.
> - Anything destructive, irreversible, or security-sensitive.
> - A needed credential or login.

对照这个仓库自己的历史看会更清楚：前几章写完、质检流水线跑绿、PR 真正准备好被合并的那几次，大副才把结果连着 PR 的完整链接一起报给船长 - 这命中的正是「work ready for their review」这一条，跟上面那次被误判的 `stale` 唤醒完全不是一类事情。一次是队伍自己运转正常、什么决定都不需要船长做；另一次是活真的做完了，下一步的决定权必须交到船长手上。区分这两者，靠的不是唤醒本身叫什么名字，而是唤醒处理完之后，落在的是「继续无声运转」还是上面这份清单里的某一条。

把这一章和第 6、7 章连起来看：第 6 章的侦察报告、第 7 章工单队列里那些等船长拍板的决策，本质上都是「上面这份清单里的某一条被命中」的具体表现 - 一份侦察报告命中的是「finished investigation findings」，一个需要船长拍板的工单命中的是它自己的决策性质。而这一章讲的监督机制，决定的是**在那之前**，大副怎么用几乎不花 token 的方式，把队伍里绝大多数不需要船长知道的动静都自己处理掉，只把真正命中那份清单的事情，过滤出来递给船长。

## 动手练习

下面两个练习都是**只读**的：只是让大副读取并汇报状态，不会改动任何仓库，也不会派出真正的船员，也不会做任何不可回退的操作。你随时可以停下。

做练习前，先在你的 FirstMate 目录里启动一个 primary 会话（例如 `claude`），这样你面前的这个 agent 就是你的大副。

### 练习 1：让大副讲清楚它自己是怎么盯着船的

对大副说：

> 大副，不用管队伍里具体某件活，先讲清楚你自己的监督机制：没有唤醒的时候，是谁在替你盯着，你的会话这时候在不在跑、有没有 token 开销；真正传到你手上的唤醒分那几种，分别代表什么。然后，如果队伍里现在有正在办的活，挑一件，用 `bin/fm-crew-state.sh` 读一下它现在的真实状态，而不是只看状态文件最后一行写的是什么；如果队伍里现在没有正在办的活，就直接说没有。不要改任何文件，也不要派任何船员，只回答。

**预期会看到什么**

- 它会点出真正盯梢的是一个不花 token 的 bash 脚本（`bin/fm-watch.sh`），自己睡着等，只在动静够得上处理门槛时才把它的会话叫醒；没有唤醒时，它的会话不在跑。
- 它会讲出四种唤醒 - `signal`、`stale`、`check`、`heartbeat` - 分别对应什么动静，而不是笼统地说「有事就叫我」。
- 如果队伍里有正在办的活，它会**真的跑一次** `bin/fm-crew-state.sh`，把命令输出讲给你，而不是转述状态文件最后一行写的内容；如果没有正在办的活，它会老实说没有。
- 它会指出出处，主要是 `AGENTS.md` 第 8 节和 `docs/architecture.md` 的「Event-driven supervision」一节。

**怎么判断做成了**

三个都满足才算：它讲的是这套机制的结论，而不是把原文整段贴给你；它清楚区分了「状态文件最后一行」和「用 `bin/fm-crew-state.sh` 核对出来的当前状态」这两件事，没有把两者混为一谈；以及 - 最关键的 - 它**没有动任何被版本追踪的文件，也没有派出任何船员**。

验证办法跟前几章一样，**前后对比**：提问之前先在 FirstMate 目录里跑一次 `git status --short` 和 `git diff HEAD`，把两份输出都留着；问完之后再各跑一次，两次应该完全一样。`data/`、`state/`、`config/`、`projects/`、`.no-mistakes/` 是大副私有的运行状态，被 gitignore 掉了，会话期间读写这些不算对项目的改动，这两条命令本来也看不见。

如果它把「状态文件最后一行」直接当成了「当前状态」讲给你，或者顺手改了什么文件，那就是没做成。

### 练习 2：核对一次真实的唤醒有没有惊动过船长

练习 1 练的是机制本身，这次练的是核对一件**真实发生过**的唤醒处理：它有没有走到「该找船长」那一步，以及为什么。

对大副说：

> 大副，回头看队伍最近处理过的一次唤醒 - 不管是 `signal`、`stale`、`check` 还是 `heartbeat` 哪一种。讲清楚那次唤醒具体是什么动静触发的，你核对之后判断的结果是什么，以及有没有因为这次唤醒去打扰过我。如果没有打扰我，说清楚是因为它落在「继续无声运转」这一类，还是核对完发现是误报；如果确实打扰过我，说清楚命中的是第 9 节「马上找船长」那份清单里的哪一条。如果队伍里还没有可查的唤醒记录，就直接说没有，不要编一个。不要改任何文件，也不要派任何船员，只讲这件已经发生过的事。

**预期会看到什么**

- 它讲的是一次真实发生过的唤醒，带得出你能自己核对的东西 - 比如对应的任务标识、时间，而不是抽象地复述这一章的机制。
- 它明确说出了那次唤醒属于四种里的哪一种，以及核对之后的真实结论。
- 它清楚地讲出「有没有打扰船长」这个判断的理由，并且这个理由能对上第 9 节的原文 - 要么是「empty polls, elapsed time, and no-change updates are not captain-facing progress」这一类不需要打扰的情形，要么命中了「reach the captain immediately for」清单里的具体一条。

**怎么判断做成了**

两条都满足才算：它讲的是可核对的真事，不是泛泛地复述这一章的规则；以及 - 如果找不到可查的唤醒记录，它老实说找不到，而不是编一个听起来合理的例子出来。

文件层面的判断跟练习 1 一样：提问前后各跑一次 `git status --short` 和 `git diff HEAD`，两次输出应该一样，并且没有新开的船员会话窗口。

如果它把这次问答本身讲成了一次新的唤醒，或者对「没有记录可查」避而不谈、直接编了一段听起来合理的唤醒经过，那就是没做成。

## 下一章

第 9 章讲**second mate（二副）与分工路由**：队伍变大之后怎么按领域拆出常驻的二副，一件活按什么规则路由给谁，以及哪些活必须留在主家。
