# 术语译法表

全书的术语统一按这张表翻译，同一个词只用一种译法。第一次出现时中英文并列，比如「工作树（worktree）」，之后只用中文。

命令名、脚本名、配置名、工具名一律保留原样，比如 `no-mistakes`、`yolo`、`bin/fm-spawn.sh`、`tasks-axi`、tmux。表里没有的词，按同样的原则来：中文里自然、准确，能直接说清楚做什么就不另造新词。

## 角色

| 英文原词 | 译法 |
| --- | --- |
| captain | 船长 |
| firstmate | 大副 |
| crewmate | 船员 |
| secondmate | 二副 |
| fleet / crew | 队伍 |

## 任务与交付

| 英文原词 | 译法 |
| --- | --- |
| ship task | 交付任务 |
| scout task | 调研任务 |
| intake | 立项 |
| brief | 任务简报（brief） |
| Captain's intent / Firstmate spec | 船长意图 / 大副规格 |
| charter / charter brief | 职责简报 |
| backlog / backlog item | 待办队列（backlog）/ 工单 |
| In flight / Queued / Done | 在办 / 待办 / 已完成 |
| delivery mode | 交付方式 |
| delivery posture | 交付方式和合并权限 |
| yolo posture | yolo 开关 |
| merge authority | 合并权限 |
| pipeline | 质检流水线 |
| respond to gates | 流水线停下来等回复时作答 |
| finding (ask-user) | ask-user 类问题 |
| accepted design / accepted intent | 已确认的设计 |
| CI green / red | CI 全部通过 / CI 没通过 |
| arm merge poll | 开始定期查看 PR 是否已合并 |
| landed / unlanded | 已合入 / 还没合入 |
| teardown | 收尾清理 |
| promote (scout → ship) | 转成交付任务 |
| escalate | 交给大副 / 来问你（按对象说） |
| hold (captain hold) | 挂起 |
| blocker | 阻塞 |

## 目录与会话

| 英文原词 | 译法 |
| --- | --- |
| worktree | 工作树 |
| primary checkout | 主仓库目录 |
| isolation assertion | 隔离检查 |
| endpoint | 会话窗口 |
| primary session | 主会话 |
| home（firstmate home） | FirstMate 目录 |
| main home | 主 FirstMate 目录 |
| harness | harness（跑船员的 agent 工具，比如 Claude Code） |
| runtime backend | 运行时后端（提供会话窗口的终端工具，比如 tmux） |
| status line / status file | 状态行 / 状态文件 |
| volatile state | 临时状态 |

## 监督

| 英文原词 | 译法 |
| --- | --- |
| supervision | 监督 |
| wake | 唤醒 |
| watcher | 监控脚本 |
| daemon | 守护进程 |
| heartbeat | 心跳 |
| stale | 久无动静 |
| away mode / afk | 离席模式（afk） |
| quiet mode | 静默模式 |
| return (from afk) | 回来 |

## 分派与 Relay

| 英文原词 | 译法 |
| --- | --- |
| routing | 分派 |
| scope（secondmate scope） | 负责范围 |
| parent channel | 上报渠道 |
| Relay | Relay（保留英文） |
| mention | 提及 |
| pairing token | 配对令牌 |
| trusted channel | 可信渠道 |

## 常用动词和形容词

| 英文原词 | 译法 |
| --- | --- |
| reconcile | 据此调整 |
| orthogonal | 无关 / 互不影响 |
| dispatch / spawn | 派出（派工） |
| verified | 验证过的 |
