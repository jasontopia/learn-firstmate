# 第 7 章：backlog（工单）与船长决策

## 这一章讲什么

前面几章沿着**一件活**的旅程往下走：怎么提出它、怎么派工、怎么过质检、怎么合并。这一章把镜头切到旁边：大副 / firstmate 手上从来不止一件活，这些活怎么被记下来、排成队，而其中有一类活很特殊 —— 它不需要船员 / crewmate 去改任何代码，只需要**船长 / 你**说一句话。

这一章只讲三件事：backlog（工单队列）怎么分「在办」和「待办」；一个等你拍板的决策，为什么在系统眼里跟一件普通的活没有本质区别，只是被「挂起」等你；以及你的回答怎么把它关掉。怎么在不吵到你的前提下盯住整支队伍、什么事件会主动叫醒大副，这些是下一章的内容，这里不展开。

本章依据的权威文件是 `AGENTS.md` 第 10 节「Backlog contract」，按需引用 `bin/fm-tasks-axi.sh` 和 `bin/fm-captain-hold.sh` 的头部注释。每个小节会指出具体出处。

## backlog 是什么：活按状态分三档

`AGENTS.md` 第 10 节开头就定了 backlog 的位置：「The configured `tasks-axi` backend is the durable queue... It tracks work items only, never agents; persistent secondmates never appear as backlog items.」

翻成大白话：backlog（工单队列）是这支队伍手上所有活的**持久记录**，靠 `tasks-axi` 这套工具管理，落地文件默认是 `data/backlog.md`。它记的是**活本身**，不是船员这个人 —— 一个常驻的二副（secondmate）永远不会作为一个条目出现在这份队列里，队列里的每一行是一件事，不是一个人。

一件活在队列里只会落在三档之一，出处是 `docs/configuration.md`「Backlog backend」一节：「On the default markdown adapter, tasks-axi and manual edits produce the same `## In flight`, `## Queued`, and `## Done` sections.」

- **`## Queued`（待办）**：已经立了工单，但还没派出去。
- **`## In flight`（在办）**：已经派了船员，正在一份隔离工作副本里干活。
- **`## Done`（已完成）**：已经收工，只保留配置允许的近期条数，更老的挪进归档。

一件活从待办变在办、从在办变已完成，这两次转移在系统里**不是**大副手动去记的两个动作。同一节写得很直接：「When the automatic transition gate applies, dispatch and completion move the item themselves - `bin/fm-spawn.sh` and `bin/fm-teardown.sh` own those transitions and refuse rather than report success without them。」也就是说，派工命令 `bin/fm-spawn.sh` 和收尾命令 `bin/fm-teardown.sh` 自己把队列条目挪到该去的位置，而且如果没挪成功，它们会拒绝报告「这件活派出去了」或「这件活收工了」，而不是先斩后奏。

这样一来，大副真正要操心的，只剩三件事：**派工前把这件活立成工单**、**记录决策**、**把工单笔记维护成最新的**。同一节接着写：「Re-evaluate queued work after every teardown and heartbeat, dispatching items only when dependencies and time gates have cleared。」—— 每次有活收尾、或者每次心跳巡检，大副都要回头再看一眼待办区，把依赖和时间条件都已经解除的活派出去。这就是「队列」这个词在这里的实际含义：待办区不是一个静止的清单，而是每次有动静就要重新过一遍的东西。

## 一个决策本质上只是一张等船长拍板的工单

这一章要讲的核心概念，`AGENTS.md` 第 10 节只用一句话就定死了：「A decision is simply a task held for the captain.」

这句话值得多读一遍：**决策没有单独的类型**。它不是队列之外另开的一种东西，也不是聊天记录里的一句话就算数 —— 它就是一件普通的工单，只是被「挂起」（hold）在等你回答这一个状态上。这意味着一个等你拍板的问题，跟一件等船员去改代码的活，享受的是同一套记账规则：它会出现在队列里，它会被追踪，它不会因为「只是问一句话」就漏记或者忘掉。

同一节接着给出这件事具体怎么做：「create the task with `bin/fm-tasks-axi.sh add` when needed, then always hold it through `bin/fm-captain-hold.sh hold <id> --reason "<reason>"`, with `--until <date>` when the captain defers it。」

拆开看是两步：

1. **如果这件事还没有对应的工单，先用 `bin/fm-tasks-axi.sh add` 立一张。** 如果这件事本来就挂在某件正在办的活底下，就不用另开一张新的，直接挂起那件活本身就行 —— `bin/fm-captain-hold.sh` 的头部注释写得很明确：「Prefer holding the work item the question gates over minting a new row.」
2. **然后一定要用 `bin/fm-captain-hold.sh hold <id> --reason "<原因>"` 把它挂起。** 这一步不是可选项，「always」两个字说得很清楚。`--reason` 要写清楚为什么这件事需要你来定，而不是船员或大副自己就能判断的。如果你当下没法立刻回答、需要过阵子再看，就再加一个 `--until <date>`，把「以后再说」变成一个具体的日期，而不是一张长期悬着、没人知道什么时候该回头看的卡片。

还有一类容易被忽略的情况，同一节也点了出来：「When a main-side thread such as a pending captain decision or relay reminder is worth durable tracking, file it as its own work item and hold it through that wrapper.」也就是说，即便这件事没有对应哪个具体项目的具体任务 —— 比如一条纯粹发生在跟你对话主线里的、值得长期留痕的提醒或待决问题 —— 只要它值得追踪，也要单独立一张工单，用同一套挂起机制记下来，而不是让它只活在某一次对话的上下文里，问完就消失。

## 挂起之后：这张工单长什么样

`bin/fm-captain-hold.sh` 的头部注释里，`hold` 子命令的行为写得很具体：这一步会在工单正文里记一条 UTC 时间戳「Captain hold set:」。如果这件事重复被挂起，已有的时间戳不会被覆盖；如果一件之前已经解除挂起、又重新回来办的活被再次挂起，那算作开启一段新的等待周期。一件已经关闭的工单不会被重新打开去挂起 —— 它会被拒绝。

这几条细节背后是同一个原则：挂起状态本身要**如实反映历史**，而不是每次操作都把之前的痕迹抹掉重写。你后面回头去看一件决策是怎么走的，看到的应该是真实发生过的时间线,而不是最后一次操作留下的孤零零的一条记录。

## 船长的回答怎么把它关闭

工单被挂起之后，怎么解除？`bin/fm-captain-hold.sh` 头部注释里 `answer` 子命令的说明写得很直接：「`answer` records the captain's exact words and resolves the call in the same act... It closes a question with `tasks-axi done` - or, with `--release`, lifts the hold with `tasks-axi unhold` so a captain-gated WORK item resumes without closing。」

这句话里有一个容易被忽略、但其实是这一章最关键的细节：**记录你的原话，和关闭这张工单，是同一个动作**。不是先记录、再由某个人手动去点一下「关闭」；你的回答一落到工单正文里，`tasks-axi done` 就在同一次操作里把它标成已完成。你的这句话本身就是关闭这张工单的动作 —— 它既是答案，也是收尾。

这里还分两种情况，取决于挂起的是什么：

- 如果挂起的是一件**只为了等你拍板而单独立的工单**（比如「要不要给这个仓库配 CI」这种本身不需要船员去干活的问题），你的回答记录下来，这张工单就直接进「已完成」区。
- 如果挂起的是**一件本来就在办、只是卡在等你某个判断上的活**（比如一件正在推进但被某个开放问题拦住的工作项），`answer` 命令支持 `--release`：只解除挂起，让这件活回到该接着办的状态，而不把它整个标成完成 —— 因为活本身还没干完，只是不再等你了。

## 案例：从这个仓库自己的 PR 记录看这三件事怎么串在一起

这个仓库自己的交付历史里，能公开核对的那部分，正好把这三件事串在了一起。

第一章《FirstMate 是什么》交付的时候，质检流水线走到了 CI 关卡 —— 但当时这个仓库里还没有任何 CI 检查可跑，PR 上的检查列表是空的，流水线卡在「等检查变绿」这一步永远等不到结果。要不要给一个纯文档教程仓库配置真正的 CI，这是一个只有船长才该定的产品判断，不是随便哪个船员能自己拍板的事。这次挂起具体记的是哪一句 `--reason`、你当时回答的原话是什么，属于大副私有的运营记录，不在这个仓库的 GitHub 历史里，教程没法把它当作可核对的公开材料引用 —— 找不到出处的具体措辞，教程不去猜，猜了就是编。

公开、可核对的部分是它促成的结果：[PR #2「ci: 加一套零依赖的 markdown 链接与格式检查」](https://github.com/jasontopia/learn-firstmate/pull/2)先于[PR #1「docs: 搭建教程骨架并写出第一章《FirstMate 是什么》」](https://github.com/jasontopia/learn-firstmate/pull/1)合并进 `main`。按上一节讲的规则倒推：一张挂起的工单只会在船长的回答落地时关闭，所以这唯一说得通的解释是，那次挂起先被你的回答关闭，随后催生了 PR #2 这件新工单去真正配置 CI；CI 配好合并后，被卡住的第一章才能重新跑绿、合并为 PR #1。这也是编号在前的那件活（PR #1），反而要等编号在后的那件活（PR #2）先落地才能收尾的原因。

这一个例子对上了这一章讲的三件事里公开可查的那部分：一个决策以工单形式存在、被挂起等船长拍板，以及船长的回答怎么关闭它并催生后续的活 —— 挂起当时具体的原因文字和你回答的原话，则是私有运营记录，如实注明「找不到公开出处」比编一段读起来更完整的叙述更重要。

## 动手练习

下面这个练习是**只读**的：只是让大副去读队列和工单记录并汇报，不会创建工单、不会派出真正的船员、不会改动任何被版本追踪的文件，也不会做任何不可回退的操作。你随时可以停下。

做练习前，先在你的 FirstMate 目录里启动一个 primary 会话，这样你面前的这个 agent 就是你的大副。

### 练习：读一遍你自己的队列，找出所有挂起的工单

对大副说：

> 大副，不用派任何船员，只帮我读一遍现在的 backlog：现在「在办」和「待办」各有哪些活，分别是什么状态；有没有工单目前正被「挂起」等我拍板 —— 如果有，讲清楚每一张挂起的工单是为什么被挂起的、给了我什么样的选项或者在等什么。如果队列是空的，或者目前没有任何工单在挂起，就直接说没有，不要为了有话说而编一个出来。这只是读一遍现状，不要创建工单，也不要改任何东西。

**预期会看到什么**

- 它会按「在办 / 待办 / 已完成」这几档分类讲，而不是把所有条目混在一起报一遍。
- 对每一张目前被挂起的工单，它会说清楚挂起的原因（对应 `--reason` 记的那句话），以及你需要回答什么，而不是只说「有一件事在等你」。
- 如果眼下没有任何工单被挂起，它会直接说没有 —— 不会硬凑一个听起来像决策的东西出来给你看。
- 它会点出出处：`AGENTS.md` 第 10 节「Backlog contract」，以及它读的是 `tasks-axi`（或 `bin/fm-tasks-axi.sh`）报出来的实际队列状态，而不是凭印象讲。

**怎么判断做成了**

两条都满足才算：它讲的是队列的**真实当前状态**，你能自己拿它报的条目去对照 `bin/fm-tasks-axi.sh`（或者它落地的 `data/backlog.md`）核对是不是真有这些内容；以及 —— 如果它说某张工单被挂起了，它讲出的原因和选项经得起你追问「这是不是真的写在那张工单里」。

文件层面的验证跟前面几章一致，**前后对比**：提问之前在 FirstMate 目录里跑一次 `git status --short` 和 `git diff HEAD`，把两份输出都留着；问完之后再各跑一次，两次应该完全一样。`data/`、`state/`、`config/`、`projects/`、`.no-mistakes/` 是大副私有的运行状态，被 gitignore 掉了，这两条命令本来也看不见，会话期间读这些不算数。

如果它趁机替你把某张挂起的工单答了、或者顺手立了一张新工单，那就是没做成 —— 这个练习只要求它读和讲。

## 下一章

第 8 章讲 **supervision（监督）与唤醒机制**：大副怎么在不烧 token 的前提下盯住整支队伍，什么事件会把它叫醒，什么时候才该轮到你被打扰。
