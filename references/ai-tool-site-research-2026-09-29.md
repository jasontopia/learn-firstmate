# 调研报告：先做哪个 AI 工具小网站

> **参考资料，不是教程章节。** 这是一份 2026-09-29 的调研报告快照，回答用 FirstMate 做新产品时先做哪个 AI 工具小网站。文中的搜索趋势、收入、融资、价格、许可证等数据和市场事实都只代表当天，之后可能已经变了。

- 调研日期：2026-09-29（所有网页访问日期均为 2026-09-29，除非另注）
- 任务类型：调研任务（scout task），只产出报告，不改代码、不开 PR
- 背景：按上一份评估报告（[agent-skills 对 FirstMate 有没有用](agent-skills-evaluation-2026-09-28.md)）的结论，新产品以 FirstMate + no-mistakes 为开发主干、由 AI agent 队伍开发。本报告是"先想清楚做什么"这一步。
- 证据等级标注（第 9 节来源表里逐条标注）：
  - **A** = 我直接打开原网页 / 调用公开接口核实过；
  - **B** = 只看到搜索引擎摘要，没有打开原文；
  - **C** = 第三方估算（流量、收入估算网站等），可靠性有限；
  - **推断** = 我根据数据做的判断或计算，正文中会写明"推断"。

---

## 0. 结论先行

### 推荐方向：AI 扒谱网站

**一句话：把一段录音或一首歌，变成"你能直接弹 / 唱"的谱**（旋律 + 和弦的 lead sheet、分难度的简易钢琴谱），在浏览器里看谱、播放，导出 PDF / MusicXML / MIDI。

### 为什么是它（5 条证据）

1. **痛点真实，而且已经有人为此花钱。**
   - 人工扒谱的市场价大约是每分钟音乐 $5-40（Fiverr、AirGigs 等报价，个别高达 €80/分钟）【B】。
   - Reddit 的 r/piano 不允许发求谱帖，求谱被分流到 r/transcribe（约 2.1 万成员，年增约 12%）【A】；那里的规则写明"4 分钟的冷门动漫钢琴曲没人免费帮你扒，请给悬赏，行情 $5-30 甚至更多"【B】。
   - 自动化工具已有人付费：Klangio 2025 年收入约 $110 万（GetLatka 估算，10 人团队）【C】，其 Piano2Notes 页面自称完成过 400 万次转写【A】；Songscription 2025-11 融资 $500 万，上线 5 个月 15 万用户【A】。
2. **需求在涨，而且集中在付费能力强的市场。**
   - Google Trends（美国，近 12 个月对比前 12 个月）："sheet music ai" +187%，"piano transcription" +168%，"audio to sheet music" +140%，"youtube to sheet music" +98%【推断：我用 Google Trends 公开数据计算】。
   - 搜索来源国家排前面的是美国、澳大利亚、韩国、新西兰、加拿大、新加坡、英国。对比之下，"bank statement converter" 的搜索主要来自印度、巴基斯坦、南非、斯里兰卡【A：Google Trends 地区数据】。
3. **通用聊天 AI 替代不了。** 要用专门的音频模型（音源分离、音高 / 节拍 / 和弦识别）再加上记谱工程，ChatGPT / Gemini 不能直接给出可用的谱。这层门槛能挡住"一个周末套个 API"的克隆潮。反面证据：简单套壳类方向里，2025-2026 年才进场的银行流水转换克隆站，在 TrustMRR 上核实的近 30 天收入只有 $0-433【A】。
4. **天然是网站形态。** 上传文件、看谱、播放、下载，都在浏览器里完成，不需要 App。对比：AI 卡牌预评级的搜索更热，但竞品几乎都是手机 App（见第 5 节）。
5. **一人 + AI agent 做得出来，单位经济好。**
   - 关键组件都有可商用许可的开源模型，许可证已逐个核实【A】：demucs（MIT）、basic-pitch（Apache-2.0）、CREPE（MIT）、beat_this（MIT，含权重）、BTC 和弦识别（MIT）、ByteDance 钢琴转写（README 标注 Apache 2.0）、music21 和 OpenSheetMusicDisplay（BSD-3）。
   - 每首歌的 GPU 成本估算 $0.02-0.08【推断，依据 Replicate 公开价格】，对比 $2.99/首的定价，毛利很高。

### 产品雏形

| 项 | 建议 |
| --- | --- |
| 目标用户（第一批） | 英语市场的业余钢琴学习者（成人初中级为主）和私人钢琴老师："听到一首想弹的歌，但没有谱，或者谱太难" |
| 核心功能（MVP） | 上传 mp3 / wav / m4a（≤8 分钟），约 1-2 分钟得到：① 旋律 + 和弦记号的 lead sheet；② 两档难度的简易钢琴谱（右手旋律、左手和弦），可选在音符上标音名；浏览器内看谱、播放；导出 PDF / MusicXML / MIDI |
| 定价思路 | 免费看前 30 秒的完整结果（整首给低清预览）；单首 $2.99、10 首包 $14.99；订阅 $9.99/月（约 60 分钟音频）；教师档 $19.99/月。参照：Klangio 年付约 $8.49/月、月付 $19.99【B，竞品博客】，单首约 $4【B，用户评价】；La Touche Musicale 的 BandConvert €9-29/月【B】 |
| 第一获客渠道 | 真实"求谱"社区冷启动（r/transcribe 等，严格遵守各社区的自我推广规则），同时从第 1 天起铺 SEO 长尾工具页（如 "mp3 to piano sheet music"、"song to easy piano sheet music"、"audio to lead sheet"）。短视频演示作辅助。X 只用来 build in public，不当主渠道（目标用户不在 X 上） |

### 必须正视的风险（这不是蓝海）

- **MuseScore 刚推出免费版。** MuseScore（全球最大曲谱社区之一，Tranco 全球排名 #4,943）2026-08-17 宣布免费的 Audio-to-Score 测试版：识别独奏钢琴和木吉他，约 3 分钟上限，可贴 YouTube 链接，结果要在 MuseScore 里编辑【A】。
  - **所以本方案不把"钢琴录音逐音转写"当主打**，主打 MuseScore 不做的"任意一首歌 → 你这个水平能弹的版本"。
- **Songscription 的 SEO 攻势。** Songscription（融资 $500 万）在我查过的几乎每个扒谱关键词结果页里都有程序化 SEO 页面，也已上线 "piano arrangement generator" 页面【A/B】；"按难度自动调整"在它的路线图上【A】。
  - 正面拼头部大词会很难。具体切入点应在第 1 周技术验证之后、写 SPEC 时定稿（候选切入点见 6.4）。
- **版权。** 把有版权的歌改编成谱属于衍生作品，是灰色地带；Klangio、Songscription、Chordify 都在做。
  - 对策：MVP 只接受用户自己上传的音频；条款限定个人使用；不做公开曲库和分享；不做"某某歌曲的谱"这类 SEO 页；不做 YouTube 链接下载（违反 YouTube 服务条款）。
- **质量是主观的。** 编配好不好弹、好不好听，需要懂音乐的人判断。
  - 对策：找 3-5 位钢琴老师做盲评，并事先写好放弃线（见第 7 节）。

**综合评分**：67/100。入围的另外 5 个方向在 61-64 之间（第 5 节）。分差不大。起决定作用的是"有付费证据 + 高付费能力市场 + 通用 AI 替代不了 + 网站形态"这个组合，其他候选同时凑不齐。

---

## 1. 我做了什么：方法、工具与拿不到的信号

### 1.1 步骤

1. **看 2026 年"小工具赚钱"的真实分布。** 用 TrustMRR（Marc Lou 做的"收入经支付平台 API 核实"的创业项目数据库）的公开统计页、分类页、公开发现接口和单个项目的公开 Markdown 页，看成功和失败的分布。
2. **列候选长名单。** 列了约 40 个 AI 相关的工具网站想法（技术类 + 垂直行业类）。
3. **粗筛。** 用 Google Trends（通过 `pytrends` 调用公开接口）给约 90 个关键词算"相对热度 + 同比"，并用 Google 自动补全挖长尾。
4. **细筛。** 入围的方向逐个查痛点（论坛 / Reddit / 评测）、竞品与定价、付费证据（核实收入、融资、定价页）、竞品流量（Tranco 公开排名、HypeStat 估算）、谁在搜索结果页排名。
5. **深挖推荐方向。** 查了关键词簇、竞品、大平台动向（MuseScore、Moises、Suno）、开源模型许可、GPU 价格。

### 1.2 SEO 数据：拿到了什么、怎么拿的

| 信号 | 来源 | 可靠性说明 |
| --- | --- | --- |
| 相对搜索热度、同比、地区分布、相关查询 | Google Trends（`pytrends`，美国 / 全球，近 5 年周数据） | 官方数据，但只有相对值 |
| 绝对月搜索量（锚点） | Exploding Topics 公开主题页：virtual staging 8.1K，ai transcription 14.8K，ai interior design 22.2K，chatpdf 201K，ai notetaker 6.6K | 页面没写口径（通常是美国 Google 月搜索量）。用它换算时我发现不自洽：按 Trends 比例，ai transcription 应是 virtual staging 的 7.06 倍、ai interior design 应是 4.64 倍，而 Exploding Topics 给的是 1.83 倍和 2.74 倍，**直接换算会高估 1.7-3.9 倍**。所以正文的"量级区间" = 相对倍数 × 8.1K ÷ (1.7~3.9)，只能当数量级看 |
| 长尾词 / 用户怎么问 | Google 自动补全公开接口（英 / 日 / 韩 / 繁中 / 简中） | 真实用户查询，但没有量 |
| "People also ask" | **没拿到**（Google 结果页需要 JS） | 用"how to / can ai / is there"开头的自动补全代替 |
| 谁在结果页排名 | WebSearch 工具返回的前 10 条（搜索引擎未注明，美国地区），外加一次 Brave 结果页（随后被限流） | 只能近似 Google |
| 竞品流量 | Tranco 公开排名（学术界常用，综合 CrUX、Cloudflare Radar、Umbrella 等，列表 N2PGW，2026-08-30 至 09-28）；HypeStat 页面（引用 Semrush 估算） | Tranco 较稳；HypeStat 与 Tranco 互相矛盾（HypeStat 说 bankstatementconverter.com 每月约 12.3 万访问、docuclipper.com 约 2.8K，但 Tranco 里 docuclipper.com 排 #685,983，bankstatementconverter.com 却不在前 100 万），只作旁证 |
| 核实收入 | TrustMRR（连接 Stripe / Lemon Squeezy 等 API 计算） | 可靠，但只覆盖主动上榜的项目，有自选偏差 |

**本次拿不到的信号**：Google 结果页原貌、"People also ask"、Ahrefs / Semrush 的绝对搜索量、关键词难度（KD）、点击单价（CPC）、排名页的域名权重、Similarweb 流量。

原因：
- 本机 headless Chrome 启动即崩溃（`FATAL:base/path_service.cc:264] Failed to get the path for 1001`），浏览器工具不可用；
- Ahrefs / Semrush 免费工具需要 JS + 人机验证或注册；
- Similarweb 对脚本返回空的 HTTP 202；
- 按规则不注册、不付费。

**付费 SEO 工具（Ahrefs / Semrush，一个月约 $100-150）能补上的**：
- 每个词的准确月搜索量（美国 / 全球）、KD、CPC（能看出商业意图强弱）；
- 结果页是否出现 AI Overview；
- 竞品每个页面的自然流量和排名词；
- 排名页的外链与域名权重（能判断"寄生垃圾页排在前面"到底有多好超越）。

**建议在写 SPEC 前花一个月订阅费把第 6.3 节的关键词表补齐。**

---

## 2. 2026 年"小工具赚大钱"模式核查

### 2.1 成功案例（都有来源）

| 案例 | 事实 | 来源等级 |
| --- | --- | --- |
| Bank Statement Converter（香港，单人） | 把 PDF 银行流水转成 Excel；superframeworks 案例报道 $38k MRR（抓取摘要显示约 2023-10 发布）；早期靠 Google 广告（起初亏钱），后靠博客和"某银行 statement converter"这类长尾 SEO | A（案例文章） |
| SEOBOT | TrustMRR 核实：近 30 天 $39,045，累计 $1,883,346；创始人 X 粉丝 116,621 | A |
| TrustMRR AI 分类头部 | Chatbase MRR $864k、AEO Engine（AI SEO 代运营）$130k、Composer.AI $72k、LLM Gateway $79k、AI Interview Copilot $27k（页面显示值） | A |
| OpenClaw 套壳潮（2026-01/02） | 开源 AI 助手 OpenClaw 爆红后，"一键部署"套壳站几天内赚钱：SimpleClaw 创始人在 X 上称"上线 5 天 $17k MRR"并挂牌 $225 万出售；TrustMRR 核实 SetupClaw 累计 $14,028、ClawWrapper $10,280（2026-02-12 文章时点） | A（文章），B（X 帖转引） |

### 2.2 失败与饱和信号（同样有来源）

| 信号 | 事实 | 来源等级 |
| --- | --- | --- |
| 整体分布 | TrustMRR 自述收录 15,000+ 项目，AI 分类 4,040 个。按收入分档：$0-1k 占 67.6%，$1k-10k 占 16.8%，$10k-100k 占 10.5%，$100k-1M 占 4.1%，$1M+ 占 1.0%（页面未注明口径，推断为累计收入）。用 Stripe 的项目累计收入中位数只有 $253 | A |
| 新上榜项目 | 公开发现接口里最近加入的 25 个项目，21 个近 30 天收入不足 $1,000，其中 7 个为 $0 | A |
| 晚进场的克隆 | 银行流水转换克隆站：bankstatemently.com（2025-09 上线）近 30 天 $433、累计 $1,420；bank-statementconverter.com（2025-05）$51 / $1,249；convertbankstatement.com（2025-11）$0 / $136；bankstatementconverter.online（2026-05）$60 / $61 | A |
| 追热点的套壳 | OpenClaw 专题：188 个项目近 30 天合计 $133,518，平均每个约 $710/月（推断：合计 ÷ 项目数）。当时的分析文章就指出"没有护城河，官方一出一键安装，90% 会消失" | A |
| 新模型名词站 | nano-banana.love（中国团队，2026-01-19 上线，蹭 Google "Nano Banana" 图像模型的名字）累计收入 $0 | A |
| 有流量不等于有收入 | Vibe App Scanner：创始人称 3 个月 125 万次 Google 展示、DR 33（已接 Search Console），但近 30 天收入 $940，累计 $5,358。AI 搜索可见度工具 LLM Signal 累计 $310 | A |
| AI 产品留存差 | RevenueCat 2026 年报告：AI 应用年留存 21.1%（非 AI 为 30.7%），但转化率高 52%、每用户收入高 41% | B |
| SEO 流量被 AI 摘要吃掉 | Ahrefs 2026-02 研究：出现 AI Overview 的词，排名第 1 的页面点击率下降 58%（2023-12 到 2025-12） | B |
| 影响收入的因素 | TrustMRR 统计：收入与创始人 X 粉丝数相关系数 r=0.25（n=5,576），与项目年龄 r=0.47（n=6,876），与域名权重 r=0.43（n=6,218） | A |

### 2.3 结论与由此得出的选择标准（推断）

- "做个小工具就赚很多钱"**是真的，但存活者偏差极大**。赚到钱的项目有三类共同点：
  - 进场早，并且占住一个肯付钱的专业人群（Bank Statement Converter 2021 年进场）；
  - 或者自带受众（SEOBOT 创始人 11 万粉丝）；
  - 或者骑上一波热点，但窗口只有几周（OpenClaw 套壳）。
- 晚进场的克隆、蹭新模型名字的站、大厂有免费版的方向，核实收入普遍接近 0。
- 收入和"时间 + 域名权重"相关，说明 SEO 是慢变量：新站要按 6-12 个月的节奏预期，冷启动需要 SEO 之外的渠道。
- 由此，第 3 节的标准特意加重了"可进入性"（晚进场会不会被挤死）和"通用 AI / 大平台能不能免费替代"，并把"网站形态是否合适"单列为门槛。

---

## 3. 选择标准与评分方法

每项 1-5 分，乘以权重后加总，满分 100。

| # | 标准 | 权重 | 5 分的样子 | 1 分的样子 | 主要证据类型 |
| --- | --- | --- | --- | --- | --- |
| A | 痛点与付费证据 | 20 | 已有人为同样的事付钱（人工服务价、核实收入、融资、定价页），用户是专业 / 半专业人群 | 只有"听起来有用"，没有付费证据 | TrustMRR、定价页、服务报价、融资新闻、论坛 |
| B | 搜索需求与趋势 | 15 | 工具意图的词簇量级大，并且同比上涨 | 量很小或在下降 | Google Trends、自动补全、Exploding Topics 锚点 |
| C | 可进入性（竞争） | 25 | 结果页弱（寄生页、旧帖），没有免费大厂，晚进场者也有收入 | 结果页被大厂或几十个同名站占满，晚进场者核实收入约 0 | 结果页观察、Tranco、TrustMRR 克隆收入 |
| D | 抗通用 AI 替代 | 10 | ChatGPT / Gemini 做不了（要专门模型或专门输出格式） | 把文件丢给聊天机器人就能搞定 | 能力判断 + 社区在推荐什么 |
| E | 一人 + agent 可行性 | 15 | 2-4 周出 MVP，有可商用开源组件，质量能用客观指标回归测试 | 需要大量领域专家、复杂合规或长销售周期 | 开源许可、技术路线 |
| F | 单位经济 | 5 | 单次成本低于售价的 5% | 成本占售价很大一部分 | 模型 / GPU 价格 |
| G | 法律 / 平台风险（分高 = 风险低） | 10 | 用户自己的数据、没有监管、不依赖某个平台的条款 | 强监管、侵权风险大、会被平台一刀切 | 法规、平台条款、案例 |

**门槛（不计分，但不满足就淘汰或降级）**："只做网站"是否天然合适（竞品和用户习惯是不是 App 为主）；必须和 AI 相关；不做伦理灰色的方向（如绕过 AI 检测、去水印）。

---

## 4. 候选长名单与淘汰理由

表中"US 相对倍数"= 该词近 12 个月的 Google Trends 美国热度 ÷ 锚点词 "virtual staging"；"同比"= 近 12 个月对比前 12 个月。都是我的计算，原始数据见附录 A。

| # | 候选 | 类型 | 关键信号 | 结论 |
| --- | --- | --- | --- | --- |
| 1 | **AI 扒谱 / 编配（音频→乐谱）** | 垂直：音乐 | 词簇量大且上涨（见 6.3）；付费证据强 | **入围 → 推荐** |
| 2 | **AI 卡牌预评级（宝可梦 / 球星卡）** | 垂直：收藏 | "card grading" 10.91×、+69%；"ai card grading" 0.75×、+562%；PSA 暂停低价档 | **入围**（App 形态占优，降级） |
| 3 | **老文档 / 手写识读（家谱、家书）** | 垂直：档案 | "handwriting to text" 1.44×、-14%；"transkribus" +579% | **入围** |
| 4 | **银行流水 PDF→Excel** | 垂直：会计 | 美国 0.05-0.22×；全球 0.65-0.70×；已被克隆站挤满 | **入围**（作为"已被验证但已饱和"的对照） |
| 5 | **PDF 无障碍 AI 修复** | B2B 合规 | "make pdf accessible" 0.25×、+713%；"pdf accessibility checker" +464% | **入围** |
| 6 | **Vibe coding 应用安全体检** | 技术：开发者 | "supabase security" 2.09×、+841%；"lovable security" +750% | **入围** |
| 7 | AI 搜索可见度（GEO / AEO）检测 | 技术：营销 | "generative engine optimization" 2.74×、+151% | 淘汰：结果页前排是 Ahrefs、Semrush、Similarweb、Search Atlas 的免费工具；Otterly（$29-489/月）、Peec、Profound 等有融资；独立小站 LLM Signal 核实累计仅 $310 |
| 8 | AI humanizer / AI 检测 | 通用 | "ai humanizer" 30×、"ai detector" 255× | 淘汰：伦理灰色（帮学生绕过检测），大站占据 |
| 9 | AI 头像 / AI logo / AI 简历 | 消费 | -29% / -52% / -32% | 淘汰：需求下降，已饱和（Rezi 等） |
| 10 | YouTube 总结 / 和 PDF 聊天 | 通用 | -35% / 被 ChatGPT、Gemini 内置 | 淘汰：大平台内置 |
| 11 | NotebookLM 幻灯片 → 可编辑 PPT | AI 新痛点 | NotebookLM 2026-02-18 已原生导出 PPTX（图片层）；NoteSlide（Codia）、DeckEdit、CopySlides 等已入场 | 淘汰：窗口期短、平台随时补齐 |
| 12 | OpenClaw / 新模型名词站 | 追热点 | 平均约 $710/月；nano-banana 站 $0 | 淘汰：窗口按周计，品牌侵权风险 |
| 13 | PDF 保留排版翻译 | 通用 | "pdf translator" 1.88×、+159% | 淘汰：DeepL、Google、Adobe、沉浸式翻译等占据 |
| 14 | 图片翻译 / 漫画翻译 | 通用 | 1.39×、+4% / 0.34×、+70% | 淘汰：Google Lens 免费；漫画有版权灰色 |
| 15 | AI 室内设计 / 虚拟样板间 | 垂直：房产 | 4.64×、+103% | 淘汰：InteriorAI 等早已饱和 |
| 16 | AI 平面图生成 | 垂直：房产 | "floor plan ai" 2.61×、+268% | 淘汰：需求意图混杂，Maket 等已融资，输出质量难保证 |
| 17 | AI 商品图 | 垂直：电商 | 1.03×、+426% | 淘汰：Photoroom、Pebblely，以及 Amazon / Shopify 内置 |
| 18 | 房源文案生成 | 垂直：房产 | 0.26×、+647% | 淘汰：ChatGPT 直接可替代 |
| 19 | 收据 / 发票 → Excel | 垂直：会计 | 0.21×、+441% | 淘汰：报销 / 记账软件内置，同银行流水一样拥挤 |
| 20 | SOAP / 心理咨询笔记 | 垂直：医疗 | 量很小 | 淘汰：受 HIPAA 监管，已被融资公司占据 |
| 21 | 学生评语 / 教案 / 练习卷生成 | 垂直：教育 | -24% / -77% / -54% | 淘汰：下降，MagicSchool 等免费替代 |
| 22 | llms.txt 生成器 | 技术 | 1.16×、+312% | 淘汰：免费工具多，付费意愿低 |
| 23 | 字幕翻译（SRT） | 通用 | 0.04× | 淘汰：量小、免费工具多 |
| 24 | AI Excel 公式 | 技术 | 数据不可靠（与大词同组） | 淘汰：Copilot / Gemini 已内置到 Excel / Sheets |
| 25 | 老照片修复 / 去背景 / 放大 | 消费 | 未单独测 | 淘汰：极度饱和（remove.bg 等） |
| 26 | 中文用户的"音频转简谱" | 垂直：音乐 | 中文 Google 搜索量小；国内已有"乐谱全能王"、"爱扒谱"等 | 暂缓：作为推荐方向的后续市场（见 6.4） |
| 27 | 房屋验房报告解读、医疗账单申诉等 | 垂直：消费 | 未深挖 | 暂缓：一次性使用、法律 / 建议责任风险 |

---

## 5. 入围方向对比

### 5.1 证据对比

| 方向 | 痛点证据 | 付费证据 | 需求与趋势（美国） | 竞争与结果页 |
| --- | --- | --- | --- | --- |
| **AI 扒谱 / 编配** | r/piano 禁止求谱，求谱去 r/transcribe（约 2.1 万人，建议给 $5-30+ 悬赏）；Songscription CEO："大多数音乐人找不到自己想弹的那首歌的谱" | 人工 $5-40/分钟；Klangio 约 $110 万/年（估算）；Songscription 融资 $500 万、15 万用户；Klangio Studio $8.49-19.99/月 | "song to sheet music" 1.91×、+36%；"sheet music ai" 1.89×、+187%；"piano transcription" +168%；来源国集中在高收入国家 | Songscription 程序化 SEO 页面几乎遍布结果页；Klangio 9 种语言；**MuseScore 免费测试版（2026-08-17）**；其余多为寄生垃圾页和旧帖；品牌词量小（klangio 0.07×、songscription 0.06×） |
| **AI 卡牌预评级** | PSA 2026-02 涨价（Value $32.99、Regular $79.99），2026-06-02 起暂停 Value 各档（约 1,000 万张积压）；送评拿不到 10 分就亏 | 工具价 $1-5/次，或 CardGrade $4.99/月起；**没有找到核实收入** | "card grading" 10.91×；"ai card grading" +562%；"pokemon card scanner" 1.17× | cardgrade.io、gradepokemon.com、pregradecards.com、cardgrading.app、tcgrader.com、pokeinvest.io 等，另有多款 App（CGA、Gemix、PSA Card Scanner）；**没有一家进入 Tranco 前 100 万**（分散、尚无赢家） |
| **老文档 / 手写识读** | 家谱爱好者读不懂旧字体（Kurrent / Sütterlin）；"transkribus" 美国 +579% | Transkribus Scholar €99/年；Handwriting OCR £19-49/月，自称 5 万+ 用户，融资 $180 万 | "handwriting to text" 1.44×、-14%；全球搜索集中在巴基斯坦、印度、埃塞俄比亚（学生、低付费能力）；家谱细分词量很小 | 结果页被 Taskade、Nanonets、Aspose、WPS、revise.io 等大站工具页占据；家谱社区在教大家用**免费的 Gemini 3** 转录 |
| **银行流水 PDF→Excel** | 会计 / 记账员手录流水；Capitec 等银行不提供 CSV 导出 | Bank Statement Converter 单人 $38k MRR；DocuClipper $20-360/月，自称服务 1 万+ 财务团队 | 美国 0.05-0.22×；全球 0.65-0.70×（印度、巴基斯坦、南非为主） | **已饱和**：Brave 的一页结果里出现 10+ 个近似域名（bankconv、bankstatementconverters.ai、bankstatementwizard、statementconvert 等）；"按银行名"长尾页也已被 DocuClipper 等占住；晚进场克隆站近 30 天 $0-433 |
| **PDF 无障碍修复** | 美国 ADA Title II 要求州 / 地方政府与公立高校的网页和文档达到 WCAG 2.1 AA，DOJ 2026-04-20 把期限延到 2027-04-26（人口 ≥5 万）和 2028-04-26；欧盟 EAA 自 2025-06-28 生效 | 人工修复 $2-15/页（多为 $5-8）；AI 修复 $0.5-2/页 | "make pdf accessible" 0.25×、+713%；"pdf accessibility checker" 0.11×、+464%（绝对量小） | Adobe Acrobat 自动标签；CommonLook、Equidox、AbleDocs、Continual Engine 等老牌厂商；高校普遍已部署 Anthology Ally |
| **Vibe coding 安全体检** | Moltbook 事件（Wiz 2026-02-02）：前端暴露 Supabase 密钥且没开 RLS，150 万个 API key 泄露；1,072 个 vibe 应用中 98% 有漏洞、16% 有严重漏洞（2026-06-02 研究） | Vibe App Scanner 近 30 天 $940（$19 深度扫描、$99/月） | "supabase security" 2.09×、+841%；"lovable security" 0.35×、+750% | Lovable 自带安全扫描和 AI 安全审查（结果页前排都是 lovable.dev）、Supabase Security Advisor；多个独立扫描站 |

### 5.2 可行性对比（一人 + AI agent）

| 方向 | MVP 规模 | 单次成本 vs 价格（推断） | 法律 / 平台风险 | 首批用户从哪来 |
| --- | --- | --- | --- | --- |
| AI 扒谱 / 编配 | 2-4 周：网页 + GPU 推理服务 + 记谱渲染 | 约 $0.02-0.08/首 vs $2.99/首 | 中：改编的版权灰色；YouTube 条款；MuseScore 免费版 | 求谱社区、SEO 长尾、短视频 |
| AI 卡牌预评级 | 1-2 周：居中测量（计算机视觉）+ 视觉模型 | <$0.02/次 vs $1-5/次 | 低-中：准确度难验证（社区普遍怀疑）；PSA 2021 年已收购 AI 评级公司 Genamint，可能自己下场；**App 形态占优，与"只做网站"冲突** | r/PokemonTCG 等收藏社区 |
| 老文档识读 | 约 1 周：调用多模态大模型 | <$0.01/页 vs £0.05-0.15/页 | 低 | 家谱论坛和 Facebook 群 |
| 银行流水 | 1-2 周 | <$0.01/页 vs $0.1-0.3/页 | 中：金融数据隐私、准确性责任 | SEO（已被占满） |
| PDF 无障碍 | 4-8 周：PDF/UA 标签结构复杂，要能过 veraPDF / PAC 校验 | 约 $0.06/页 vs $0.5-2/页 | 高：合规宣传有责任（FTC 2025 年就因"AI 能让网站完全合规"的误导宣传罚了 accessiBe $100 万）；B2G 采购周期长；DOJ 延期公告自己提到"生成式 AI 修复能力有限" | 高校 / 政府工作人员的搜索 |
| Vibe 安全体检 | 1-3 周 | 低 vs $19/次 | 高：未授权扫描别人的网站有法律风险；漏报有责任；平台内置 | X、Indie Hackers |

### 5.3 评分（权重见第 3 节）

| 方向 | A 付费 ×20 | B 需求 ×15 | C 可进入 ×25 | D 抗替代 ×10 | E 可行 ×15 | F 经济 ×5 | G 风险 ×10 | **总分** | 门槛 |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| **AI 扒谱 / 编配** | 4 | 4 | 2 | 5 | 3 | 4 | 3 | **67** | 网站形态合适 |
| AI 卡牌预评级 | 3 | 5 | 2 | 3 | 3 | 4 | 4 | 64 | **App 为主，不合适** |
| 老文档识读 | 3 | 3 | 2 | 2 | 5 | 5 | 4 | 63 | 合适 |
| 银行流水 | 5 | 3 | 1 | 3 | 4 | 5 | 3 | 63 | 合适 |
| PDF 无障碍 | 5 | 3 | 2 | 4 | 2 | 4 | 2 | 61 | 合适（偏 B2B） |
| Vibe 安全体检 | 2 | 4 | 3 | 3 | 4 | 4 | 2 | 61 | 合适 |

打分理由要点：

- **扒谱 C 只给 2 分**，因为 MuseScore 免费版加 Songscription 的 SEO 覆盖。**E 给 3 分**，因为编配质量需要音乐判断。
- **卡牌 A 给 3 分**，因为没有找到任何预评级工具的核实收入。**E 给 3 分**，因为从手机照片判断表面瑕疵很难被证明准确。
- **老文档 D 给 2 分**，因为免费的 Gemini 3 已足够好，家谱社区在直接教大家用。
- **银行流水 C 给 1 分**，因为有 TrustMRR 克隆站收入作证。
- **PDF 无障碍 E 和 G 都是 2 分**：技术复杂度高，合规责任重。
- **Vibe 安全 A 给 2 分**：有流量（125 万次展示）却只有约 $940/月。

**如何读这张表**：分差在 3-6 分之间，评分本身是结构化判断，不是精确测量。推荐扒谱，靠的是它在"付费证据 + 付费能力强的市场 + 通用 AI 做不了 + 网站形态"四点上同时成立。另外两个方向可作为后备：如果愿意做 B2B、接受更长的销售周期，PDF 无障碍是后备；如果能接受以手机网页为主、并能拿到"准确度"的硬证据，卡牌预评级是后备。

---

## 6. 推荐方向深挖：AI 扒谱 / 编配网站

### 6.1 用户与痛点

- **谁**：业余乐器学习者（钢琴最多），尤其是成人初中级学习者；私人音乐老师（给学生准备不同难度的材料）；歌手、吉他手、教会敬拜团（需要 lead sheet：旋律 + 和弦）。
- **场景**：听到一首想弹的歌（流行、动漫、K-pop、影视配乐，或 Suno 等 AI 生成的歌），网上没谱、谱要花钱，或者谱太难；自己扒谱要几个小时。
- **证据**：
  - r/piano 规定不许发求谱帖，引导到 r/transcribe【B】；r/transcribe 约 2.1 万人，话题前几位是 Help、Transcription、Piano、Song【A】；其规则写明免费请人扒 4 分钟的曲子通常没人理，建议悬赏 $5-30+【B】。
  - 自动补全里大量"怎么做"类问题：how to turn a song into sheet music (online free)、can ai make sheet music from a song、is there an app that turns music into sheet music、how to get sheet music for any song【A：自动补全】。
  - "easy piano version of …" 后面跟的全是具体歌名（Fur Elise、Hallelujah、Golden、Bohemian Rhapsody…），说明"要简单版"是高频需求；"easy piano sheet music with letters"（带音名的简易谱）也在补全里【A】。

### 6.2 付费证据

| 证据 | 数字 | 等级 |
| --- | --- | --- |
| 人工扒谱价 | 单旋律约 $5/分钟；钢琴中高难度 $15-20/分钟；合唱 $30/分钟；专业扒谱 $20-40/分钟；有服务商报 €15-80/分钟；AirGigs 上单首 $20-120 | B |
| Klangio（德国，2018 年起） | 2025 年收入约 $110 万、10 人（GetLatka 估算，页面注明非自报）；Piano2Notes 页面称完成 400 万次转写；Trustpilot 4/5（95 条评价），有用户建议按次买（约 $4/首）而不是订阅 | C / A / B |
| Songscription（斯坦福团队） | 2025-06 上线，2025-11 融资 $500 万（Reach Capital 领投），15 万用户、150 个国家；定价页：免费每次 30 秒，Plus 每月 60 分钟，Pro 每月 300 分钟（具体价格需 JS 渲染，未抓到） | A |
| La Touche Musicale（PianoConvert 等） | BandConvert €9-29/月（每月 10-300 次） | B |
| 大众市场参照 | Chordify（把歌转成和弦）订阅约 $2-8/月，Tranco #16,317；Moises Tranco #35,675；MuseScore #4,943。说明"把一首歌变成能弹的东西"有大众级受众 | B / A |

### 6.3 关键词清单（需求与竞争证据）

- **区间换算**：相对倍数 × 8.1K ÷ (1.7~3.9)，只表示数量级，**不是精确搜索量**。
- **结果页观察**来自 WebSearch 前 10 条，是近似。

| 关键词 | 意图 | US 相对倍数 / 同比 | 美国月量级（推断区间） | 结果页观察 | 优先级 |
| --- | --- | --- | --- | --- | --- |
| song to sheet music (converter) | 工具 | 1.91× / +36% | 约 4-9K | ScoreCloud、Songscription（多页）、La Touche、futuretools，外加 2 个寄生垃圾页 | P1（头部，难） |
| sheet music ai | 工具 / 泛 | 1.89× / +187% | 约 4-9K | 博客、rankmyai 榜单、arXiv、Songscription、寄生垃圾页 | P1 |
| audio to sheet music (converter / ai / free) | 工具 | 0.45× / +140% | 约 1-2K | ScoreCloud、Lunaverus（AnthemScore）、notation.com、Songscription，外加 3 个寄生垃圾页 | P1 |
| mp3 to sheet music (piano / free) | 工具 | 0.22× / +60% | 约 0.5-1K | AppFollow（Piano2Notes）、AlternativeTo、2009 年 Apple 论坛旧帖、Ivory、Songscription，外加 3 个寄生垃圾页 | **P1（结果页最弱）** |
| piano arrangement (ai) | 工具 | 0.79× / +60% | 约 1.6-3.8K | Songscription 已有 "piano arrangement generator" 页 | P1（主打） |
| youtube to sheet music | 工具 | 0.82× / +98% | 约 1.7-3.9K | La Touche 的 Chrome 扩展、Songscription、Scriptor，外加寄生垃圾页 | P2（MVP 不做链接下载，只做"方法"内容页） |
| piano transcription (ai) | 工具 | 0.48× / +168% | 约 1-2.3K | 未单独查 | P2 |
| mp3 to midi / midi to sheet music | 工具 | 0.74× / -2%；0.29× / +14% | 约 1.5-3.5K；约 0.6-1.4K | 未单独查 | P2（MIDI 导出页、免费小工具引流） |
| easy piano sheet music | 以找具体曲目为主 | 3.61× / +16% | 约 7-17K | 以曲谱站为主 | P2（用"把任何歌变简易版"切入，不做具体歌名页） |
| lead sheet (maker / generator ai) | 工具 / 泛 | 8.68× / +32%（混有"铅板"等无关意思） | 不可靠 | 未单独查 | P2 |
| transpose sheet music | 工具 | 0.14× / +73% | 约 0.3-0.7K | 未单独查 | P3 |
| chords from audio | 工具 | 0.05× / +267% | 很小 | 未单独查 | P3 |
| 品牌词 klangio / songscription | 导航 | 0.07× / 0.06× | 很小 | - | 说明市场尚未被品牌锁定 |

**长尾补充**（自动补全，有真实查询但无量）：

- 英文：voice memo to sheet music、violin audio to sheet music、audio to lead sheet、music sheet generator from audio / youtube / video、song to piano sheet music ai、piano audio to sheet music ai、guitar tab from audio (ai)、best ai music transcription (reddit)、anthemscore free alternative、songscription reddit / cost、klangio cost。
- **本地化机会（推断）**：
  - 韩语：악보 변환 사이트、mp3 악보 변환 사이트、음원 악보 변환 ai、피아노 악보 만들어 주는 ai。
  - 日语：耳コピ ai（無料 / ピアノ / midi）、音源 楽譜化 ai、採譜 ai 無料、楽譜作成 ai。
  - 繁中：扒譜 ai、扒譜軟體、扒譜網站。
  - 用美国 WebSearch 搜日语和韩语词，结果里没有本地语言的专门网页工具（日语结果是 2021 年京都大学的研究新闻和 Chord ai App）。但 Klangio 已有 ja / ko / zh-hans 等 9 种语言页面，所以本地化是加分项，不是护城河。

**地区（Google Trends，近 12 个月）**：

- "song to sheet music"：美国、澳大利亚、韩国、新西兰、加拿大、新加坡、英国、香港。
- "sheet music ai"：韩国、新加坡、美国、荷兰、中国、澳大利亚、香港。
- "piano transcription"：中国、韩国、新加坡、香港、美国。

### 6.4 竞品与空位

| 竞品 | 定位 | 强项 | 弱点 / 空位（推断，部分来自竞品自己的对比文，有偏向） |
| --- | --- | --- | --- |
| MuseScore Audio-to-Score（免费测试版，2026-08-17） | 独奏钢琴、木吉他逐音转写，约 3 分钟上限，支持 YouTube / Audio.com 链接 | 免费，背靠全球最大曲谱社区，自研模型 | 只转"录音里的钢琴 / 吉他"，不从一首完整的歌生成可弹的版本；有时长上限；结果要在 MuseScore 生态里编辑 |
| Songscription（$500 万融资） | 钢琴、吉他、贝斯、鼓、小提琴、长笛、萨克斯、小号、人声；有 lead sheet / 编配页面 | 质量口碑、程序化 SEO、Guitar Pro 导出 | 没有自助 API、DAW 插件和手机 App（自述）；语言上只见英语和西语（我检查 /ja、/ko 都跳回英文首页，/es 存在）；"按难度调整"尚在规划 |
| Klangio（Piano2Notes 等） | 按乐器拆成多个 App，加 Transcription Studio、API、插件 | 覆盖广，9 种语言 | 按 App 分别订阅，多乐器时贵；免费只有 20 秒；有订阅和客服相关的差评 |
| La Touche Musicale / ScoreCloud / AnthemScore / Ivory / Scriptor | 各有侧重 | 各自的存量用户 | 规模小 |
| Moises、Suno Studio | 音源分离、和弦；Suno 2026-08 在 Studio 里提供 MIDI 导出 | 用户基数大 | 都不输出乐谱（Moises 给的是音频；Suno 的 MIDI 只是粗略音符网格，没有记谱） |

**候选切入点**（按我建议的优先级，第 1 周技术验证后在 SPEC 里定稿）：

1. **"能弹版"**：任意歌曲 → 旋律 + 和弦 → 两档难度的简易钢琴谱，可标音名（针对 "easy piano"、"with letters" 这类需求；MuseScore 不做，Songscription 尚未做难度分级）。
2. **lead sheet**：给歌手、吉他手、教会敬拜团的旋律 + 和弦谱。和 ① 共用同一条处理管线。
3. **本地化长尾**：日语、韩语、繁体中文（高付费能力市场，本地语言结果页偏弱）。之后再考虑简谱输出（面向华语用户；中国大陆市场涉及支付、备案和国内应用竞争，不建议作为首发）。

### 6.5 MVP 范围

**做（MVP）**：

- 上传 mp3 / wav / m4a（≤8 分钟）→ 生成：
  - lead sheet（旋律 + 和弦记号）；
  - 简易钢琴谱两档（右手旋律；左手分别为和弦根音 / 柱式和弦）；
  - 可切换音名标注。
- 浏览器内看谱与播放（OpenSheetMusicDisplay）；导出 PDF / MusicXML / MIDI。
- 免费预览（前 30 秒完整结果 + 整首低清预览）；按首付费、次数包、月订阅。
- 邮箱登录（魔法链接）、历史记录（只对自己可见）。
- 10-20 个 SEO 工具页（按 6.3 的 P1 / P2 词），加一个"怎么把歌变成谱"的指南页。
- 基础质量反馈（"这段错了"一键报告），用来积累评测数据。

**不做（MVP 之后再说）**：

- YouTube / TikTok 链接下载（违反平台条款，技术上还会被封）；
- 多乐器逐音转写、吉他谱、鼓谱；
- 完整的在线打谱编辑器（先支持导出 MusicXML 到 MuseScore 里改）；
- 手机 App、教师后台、API、简谱、日韩繁中本地化（第二阶段）；
- 公开曲库、分享页、按具体歌名的 SEO 页（版权风险）。

### 6.6 技术路线与工期（一人 + AI agent）

**处理管线（组件和许可已核实，见附录 D）**：

1. demucs 分离人声和伴奏（MIT）。
2. 旋律音高：CREPE（MIT）或 basic-pitch（Apache-2.0），再做音符切分。
3. 节拍 / 小节：beat_this（MIT，代码和权重都是 MIT；作者提示部分训练数据有版权或受限许可，需自行评估），或 all-in-one（MIT）。
4. 和弦：BTC-ISMIR19（MIT）。
5. 用 music21（BSD-3）按难度规则生成编配和 MusicXML / MIDI。
6. 渲染：OpenSheetMusicDisplay（BSD-3）；PDF 可用 Verovio（LGPL-3.0，作为库或服务调用即可）。
7. 可选"钢琴录音逐音转写"模式：ByteDance piano_transcription（README 标注 Apache 2.0）。

**避开**：madmom 的模型文件（CC BY-NC-SA 4.0，**不可商用**）；YourMT3（GPL-3.0）。

**部署**：网页（任意主流全栈框架）+ 无服务器 GPU（Replicate / Modal 一类，按秒计费）+ 任务队列 + 对象存储 + 支付（Merchant of Record 类服务）。

**为什么适合 FirstMate + no-mistakes 的 agent 开发（推断）**：

- 组件能用客观指标回归测试：用 mir_eval 在固定测试集上算音符 / 和弦 / 节拍准确率，agent 可以反复迭代而不需要人每次盯着。
- 网页、推理服务、编配规则、SEO 页面可以拆成互相独立的并行任务。

**工期估算（推断）**：

| 周 | 内容 |
| --- | --- |
| 第 1 周 | 技术验证：用 30 首常见流行歌跑通管线，请 3-5 位钢琴老师盲评 |
| 第 2-3 周 | 网页、支付、导出、SEO 页 |
| 第 4 周 | 上线、冷启动 |

### 6.7 单位经济（推断）

- **GPU**：Replicate T4 价格 $0.000225/秒（$0.81/小时），L40S $0.000975/秒【A】。一首 4 分钟的歌，分离 + 音高 + 节拍 + 和弦估计需要 T4 上 60-90 秒，约 $0.014-0.02；Replicate 上托管的 ByteDance 钢琴模型，页面标注每次约 $0.078【A】，可作悲观上限。所以每首成本约 $0.02-0.08。
- **支付费**：Merchant of Record 类服务常见费率约 5% + $0.5/笔（需在 SPEC 阶段按所选服务核实）。$2.99 单首扣掉约 $0.65，所以要主推 $14.99 的 10 首包和订阅，降低手续费占比。
- **结论**：在正常使用下毛利约 70-90%。成本风险主要来自重度订阅用户，用每月分钟数封顶。

### 6.8 获客计划

| 阶段 | 渠道 | 说明 |
| --- | --- | --- |
| 冷启动（前 50 个用户） | 真实求谱社区 | r/transcribe 的求谱帖可以直接用工具产出结果去帮忙，前提是遵守该版关于自我推广的规则；另有钢琴学习类子版、钢琴老师 Facebook 群。目标是拿反馈，不是刷量 |
| 同步开始 | SEO 长尾 | 6.3 表的 P1 词，尤其是结果页最弱的 "mp3 to sheet music"；再加"怎么做"类问题的指南页。按 TrustMRR 数据，SEO 收入随时间和域名权重上升，按 6-12 个月的节奏预期 |
| 辅助 | 短视频 | YouTube Shorts / TikTok：把一段热门旋律 30 秒变成简易谱，演示前后对比 |
| 辅助 | X、Indie Hackers | build in public，也用于和其他开发者交流；不指望从这里来付费用户 |
| 第二阶段 | 本地化 | 日语、韩语、繁中长尾页 |

### 6.9 主要风险与对策

| 风险 | 严重度 | 对策 |
| --- | --- | --- |
| MuseScore 免费 Audio-to-Score 扩展到"任意歌曲 → 简易版" | 高 | 主打 MuseScore 暂不做的"能弹版 + 难度 + 音名 + lead sheet"；持续关注它的更新日志；准备好退路（第 7 节） |
| Songscription 抢先做难度分级，加上程序化 SEO 覆盖 | 高 | 不和它拼头部大词；做结果页弱的长尾和本地化；用按首付费和不强推订阅作差异 |
| 编配质量不过关（主观） | 高 | 第 1 周盲评并设放弃线；组件级客观指标回归；产品上允许导出后自行修改 |
| 版权（改编有版权的歌） | 中 | 只处理用户上传的音频；条款限定个人学习使用；不做公开曲库、分享和歌名 SEO 页；设 DMCA 投诉处理流程；上线前请律师看一次条款 |
| YouTube 等平台条款 | 中 | MVP 不做链接下载 |
| 模型许可 | 中 | 只用 MIT / Apache / BSD 组件，逐个记录许可和训练数据说明 |
| 留存（AI 产品流失快） | 中 | 用次数包和按首付费匹配"偶尔用一次"的真实使用频率；教师档做成持续需求 |
| 创始人自己不懂音乐 | 中 | 招 3-5 位老师当种子用户和评审；报告质量的反馈闭环 |
| 从中国收款 | 中 | 优先考虑 Paddle、Lemon Squeezy、Creem、Dodo Payments 这类 Merchant of Record（TrustMRR 统计里独立开发者常用）；是否支持中国大陆个人 / 公司主体和提现方式，要在 SPEC 阶段逐家核实。先做海外市场，避开国内生成式 AI 与网站备案的合规问题 |

---

## 7. 什么会改变这个推荐

以下任一情况出现，应该回到第 5 节换方向或调整切入点：

1. **第 1 周盲评不过线。** 30 首测试歌里，钢琴老师评为"稍作修改就能用"的不到 60%，就把 MVP 退回到"钢琴录音逐音转写 + 自动简化"（ByteDance 模型成熟度更高），或者换后备方向。
2. **MuseScore 或 Songscription 推出免费的"任意歌曲 → 分难度简易版"。** 那时切入点改为本地化市场，或者重新评估。
3. **付费 SEO 工具的数据显示词簇比推断的小很多。** 比如美国工具意图的词加起来不到 5K/月，就降低预期，或改为以社区和短视频为主的打法。
4. **律师认为"歌曲 → 改编谱"服务版权风险高。** 那就收窄到"你自己的演奏 / 创作"和公版曲目（古典、赞美诗等），或换方向。
5. **创始人有现成的行业人脉或受众**（比如认识很多会计师、老师、收藏者）。TrustMRR 数据显示受众和渠道对收入影响明显，这时应优先选能用上这层关系的方向。
6. **愿意做 B2B、接受更长销售周期、追求更高客单价。** PDF 无障碍修复是更合适的后备（美国 2027 / 2028 期限加欧盟 EAA）。

---

## 8. 下一步：把它变成产品 SPEC

建议顺序（对应上一份报告里的 FirstMate 流程）：

1. **拍板方向。** 采纳本推荐 / 改选入围的其他方向 / 先补数据。方向尚待决定。
2. **技术验证（1 周，调研任务）。** 用开源管线跑 30 首测试歌，产出样例谱、组件准确率、每首耗时和成本、许可清单；同时实测 MuseScore、Songscription、Klangio 的免费额度，建立对比基线（需要注册账号，本次调研按规定没做）。
3. **补 SEO 数据（可选，约一个月订阅费）。** 用 Ahrefs 或 Semrush 补齐 6.3 表的准确搜索量、KD、CPC 和 AI Overview 出现情况。
4. **写 SPEC（调研任务 + Lavish 看板评审）。** 内容：
   - 目标用户与使用场景；
   - MVP 范围（沿用 6.5）；
   - 定价与付费墙；
   - 成功指标，例如上线 60 天内 50 个付费用户、预览到付费转化 ≥2%、盲评可用率 ≥70%；
   - 放弃线（沿用第 7 节）；
   - 数据与隐私（音频保留多久）；
   - 条款要点。
5. **开发。** 按 SPEC 拆成若干交付任务（ship task），经 no-mistakes 质检流水线（pipeline）交付；上线后按 6.8 冷启动。

---

## 9. 来源（访问日期均为 2026-09-29）

证据等级：A = 直接打开或调用核实；B = 仅搜索摘要；C = 第三方估算。

### 9.1 模式核查与 TrustMRR

| # | 来源 | 用于 | 等级 |
| --- | --- | --- | --- |
| 1 | https://trustmrr.com/llms.txt | TrustMRR 自述：15,000+ 项目、核实方式 | A |
| 2 | https://trustmrr.com/stats | 收入分档、各支付平台中位数、相关系数 | A |
| 3 | https://trustmrr.com/category/ai | AI 分类 4,040 个；头部项目 MRR | A |
| 4 | https://trustmrr.com/api/ai/discovery | 最近加入的 25 个项目收入 | A |
| 5 | https://trustmrr.com/startup/vibe-app-scanner.md | 收入 $940 / 30 天，定价，125 万次展示（创始人自述） | A |
| 6 | https://trustmrr.com/startup/llm-signal.md | 累计 $310 | A |
| 7 | https://trustmrr.com/startup/aeo-engine.md 、https://trustmrr.com/startup/seobot.md 、https://trustmrr.com/startup/rankai.md | 收入与粉丝数 | A |
| 8 | https://trustmrr.com/startup/bankstatemently.md 、https://trustmrr.com/startup/bank-statement-converter-pro.md 、https://trustmrr.com/startup/convertbankstatement.md 、https://trustmrr.com/startup/bank-statement-converter.md | 银行流水克隆站收入 | A |
| 9 | https://trustmrr.com/startup/nano-banana-ai.md | 追热点站收入 | A |
| 10 | https://trustmrr.com/special-category/openclaw | 188 个项目合计 $133,518 / 30 天 | A |
| 11 | https://www.thetoolnerd.com/p/the-openclaw-wrapper-bubble-how-10-penclaw-startupso （2026-02-12） | OpenClaw 套壳潮 | A |
| 12 | https://superframeworks.com/blog/bankconverter | Bank Statement Converter $38k MRR 与获客方式 | A |
| 13 | https://founderreports.com/interview/bank-statement-converter/ | 早期 $16k MRR | B |
| 14 | https://techcrunch.com/2026/03/10/ai-powered-apps-struggle-with-long-term-retention-new-report-shows | RevenueCat 2026 AI 应用留存 | B |
| 15 | https://ahrefs.com/blog/ai-overviews-reduce-clicks/ （及转载 https://www.medianama.com/2026/02/223-google-ai-overviews-click-through-rates-58-study/） | AI Overview 使第 1 名点击率 -58% | B |

### 9.2 推荐方向（音乐）

| # | 来源 | 用于 | 等级 |
| --- | --- | --- | --- |
| 16 | https://www.mu.se/posts/musescore-audio-score-features （2026-08-17） | MuseScore 免费 Audio-to-Score 测试版 | A |
| 17 | https://www.musicbusinessworldwide.com/songscription-raises-5m-in-funding-as-shazam-for-sheet-music-platform-reaches-150k-users/ | Songscription 融资、用户数、CEO 原话 | A |
| 18 | https://techcrunch.com/2025/06/30/songscription-launches-an-ai-powered-shazam-for-sheet-music | Songscription 团队与训练数据 | A |
| 19 | https://www.songscription.ai/pricing | 各档额度（价格未渲染） | A |
| 20 | https://www.songscription.ai/blog/songscription-vs-klangio （2026-05-31，竞品撰写） | Klangio Studio $8.49 / $19.99 | A（内容有偏向） |
| 21 | https://www.songscription.ai/blog/musescore-vs-songscription 、https://www.songscription.ai/piano-arrangement-generator | 竞品定位、编配页 | A / B |
| 22 | https://klang.io/piano2notes/ | 400 万次转写、输入输出格式 | A |
| 23 | https://getlatka.com/companies/klang.io | Klangio 约 $110 万 / 年（估算） | C |
| 24 | https://uk.trustpilot.com/review/klang.io | 评分与订阅相关评价 | B |
| 25 | https://gummysearch.com/r/transcribe/ | r/transcribe 约 2.1 万人 | A |
| 26 | r/transcribe 规则（经搜索摘要，镜像 https://red.applefritter.com/r/transcribe） | 悬赏行情 $5-30+；r/piano 引导求谱 | B |
| 27 | https://airgigs.com/Music-Transcription-Services/102900/Transcribe-audio-to-sheet-music 、https://latouchemusicale.crunch.help/en/band-convert/what-is-the-price-of-a-sheet-music-transcription-bandconvert 、https://fiverr.com/sam_sheet3/professionally-transcribe-piano-audio-and-midi-into-sheet-music | 人工扒谱价格、BandConvert 订阅价 | B |
| 28 | https://replicate.com/bytedance/piano-transcription 、https://replicate.com/pricing | 每次约 $0.078；GPU 按秒价格 | A |
| 29 | GitHub API / 原始 LICENSE：spotify/basic-pitch、facebookresearch/demucs、marl/crepe、CPJKU/beat_this、jayg996/BTC-ISMIR19、mir-aidj/all-in-one、cuthbertLab/music21、opensheetmusicdisplay/opensheetmusicdisplay、rism-digital/verovio、mimbres/YourMT3、CPJKU/madmom（LICENSE）、bytedance/piano_transcription（README） | 许可核实 | A |
| 30 | https://blog.dubspot.com/suno-studio-2-0 | Suno Studio 2.0 MIDI 导出、无乐谱 | B |
| 31 | https://www.songscription.ai/blog/songscription-vs-moises | Moises 不输出乐谱（竞品撰写） | B |
| 32 | https://www.guitarchalk.com/chordify-review/ | Chordify 价格 | B |

### 9.3 其他入围方向

| # | 来源 | 用于 | 等级 |
| --- | --- | --- | --- |
| 33 | https://cardgrade.io/ 、https://gradepokemon.com/ 、https://pregradecards.com/grading-pokemon 、https://cardgrading.app/ai-grading-app 、https://www.tcgrader.com/ 、https://www.pokeinvest.io/card-grading | 卡牌预评级竞品 | B |
| 34 | https://allvintagecards.com/psa-grading-costs/ 、https://www.misprint.com/posts/how-long-does-psa-grading-take-2026 | PSA 2026 涨价、暂停 Value 档、约 1,000 万积压 | B |
| 35 | https://www.sportscollectorsdaily.com/psa-grading-buys-genamint/ | PSA 收购 Genamint | B |
| 36 | https://www.cardboardconnection.com/the-2026-grading-boom-why-you-can-no-longer-afford-to-guess | 预评级工具定价 $1-5 / 次、准确度讨论 | B |
| 37 | https://www.transkribus.org/plans | Transkribus 价格 | A |
| 38 | https://www.handwritingocr.com/ | Handwriting OCR 价格、5 万+ 用户 | A |
| 39 | https://www.vcbacked.co/company/handwriting-ocr | Handwriting OCR 融资 $180 万 | B |
| 40 | https://ancestorsandai.buzzsprout.com/2525649/episodes/18422484-ep-20-how-to-transcribe-handwritten-genealogy-documents-with-free-ai-gemini-3-tutorial | 家谱社区教用免费 Gemini 3 | B |
| 41 | https://www.docuclipper.com/pricing/ | DocuClipper 价格、1 万+ 团队 | A |
| 42 | https://www.docuclipper.com/blog/convert-capitec-bank-statement-to-excel/ | 按银行名的长尾页已被占 | B |
| 43 | Brave 搜索结果页 "bank statement converter"（https://search.brave.com/search?q=bank+statement+converter） | 10+ 个近似域名 | A |
| 44 | https://www.federalregister.gov/documents/2026/04/20/2026-07663/extension-of-compliance-dates-for-nondiscrimination-on-the-basis-of-disability-accessibility-of-web 、https://upcea.edu/doj-extends-accessibility-deadline-to-april-2027-policy-matters-april-2026/ | ADA Title II 延期、DOJ 提到生成式 AI 的局限 | B |
| 45 | https://www.fruition.net/ai-platforms/pdf-accessibility 、https://testparty.ai/product/pdf-to-accessible-html 、https://venngage.com/blog/pdf-accessibility-cost/ 、https://www.cni.org/wp-content/uploads/2025/12/CNI_Project_Tressler.pdf | PDF 修复价格 | B |
| 46 | https://techcrunch.com/2025/01/03/ftc-orders-ai-accessibility-startup-accessibe-to-pay-1m-for-misleading-advertising | FTC 罚 accessiBe $100 万 | B |
| 47 | https://testparty.ai/blog/eaa-pdf-accessibility 、https://www.axes4.com/en/blog/post/2025/the-european-accessibility-act-explained-simply | 欧盟 EAA 时间线与豁免 | B |
| 48 | https://www.wiz.io/blog/exposed-moltbook-database-reveals-millions-of-api-keys （2026-02-02） | Moltbook 泄露 | A |
| 49 | https://www.symbioticsec.ai/blog/we-scanned-1-072-vibe-coded-apps-98-had-security-flaws （2026-06-02） | 98% 有漏洞 | A |
| 50 | https://lovable.dev/blog/secure-vibe-coding | Lovable 自带安全扫描 | B |
| 51 | https://otterly.ai/pricing | Otterly $29-489 / 月 | A |
| 52 | https://ahrefs.com/free-ai-visibility 、https://www.semrush.com/free-tools/ai-search-visibility-checker/ | 大厂免费 AI 可见度工具 | B |
| 53 | https://codia.ai/blog/convert-notebooklm-to-powerpoint-2026 | NotebookLM 2026-02-18 原生 PPTX 导出（竞品撰写） | B |

### 9.4 SEO 数据源

| # | 来源 | 用于 | 等级 |
| --- | --- | --- | --- |
| 54 | Google Trends（经 `pytrends` 调用 trends.google.com 公开接口） | 相对热度、同比、地区、相关查询 | A（原始数据），推断（换算） |
| 55 | Google 自动补全 `https://suggestqueries.google.com/complete/search?client=firefox&hl=<lang>&gl=<geo>&q=<query>` | 长尾词 | A |
| 56 | https://explodingtopics.com/topic/virtual-staging （及 ai-transcription、ai-interior-design、chatpdf、ai-notetaker） | 绝对量锚点 | A（数字），C（口径未知） |
| 57 | https://tranco-list.eu/list/N2PGW/1000000 （2026-08-30 至 09-28） | 竞品流量排名 | A |
| 58 | https://hypestat.com/info/klang.io 等 | 竞品流量估算（klang.io 约 25.6 万 / 月，scorecloud.com 约 26.9 万，melodyscanner.com 约 17 万，transkribus.org 约 20.5 万，bankstatementconverter.com 约 12.3 万） | C |

### 9.5 事实与推断的区分

- **已核实的事实**：等级为 A 的条目。
- **只见过摘要的事实**：等级 B。结论方向上与多个来源一致，但具体数字写 SPEC 前应打开原文复核，尤其是 PSA 价格、DOJ 期限和人工扒谱价格。
- **估算**：等级 C，包括 Klangio 的收入和 HypeStat 的流量。
- **本报告的推断**：
  - 所有"美国月量级"区间；
  - 第 5 节的全部打分；
  - 每首 GPU 成本和毛利；
  - MVP 工期；
  - "本地化结果页偏弱"；
  - 各候选的"空位"判断。

---

## 附录 A：Google Trends 原始结果（美国，近 5 年周数据，锚点 "virtual staging"）

计算方法（脚本在调研时的临时目录，已随任务清理；逻辑如下）：

```python
from pytrends.request import TrendReq
pt = TrendReq(hl='en-US', tz=0, timeout=(10, 30))
# 每组 = 锚点 + 4 个词，保证组间可比
pt.build_payload(['virtual staging', kw1, kw2, kw3, kw4], timeframe='today 5-y', geo='US')
df = pt.interest_over_time()
last12 = df.tail(52).mean(); prev12 = df.iloc[-104:-52].mean()
ratio = last12[kw] / last12['virtual staging']   # 相对倍数
yoy   = last12[kw] / prev12[kw] - 1              # 同比
```

| 关键词 | 相对倍数 | 同比 | | 关键词 | 相对倍数 | 同比 |
| --- | --- | --- | --- | --- | --- | --- |
| song to sheet music | 1.91 | +36% | | card grading | 10.91 | +69% |
| sheet music ai | 1.89 | +187% | | ai card grading | 0.75 | +562% |
| youtube to sheet music | 0.82 | +98% | | pokemon card scanner | 1.17 | +101% |
| piano arrangement | 0.79 | +60% | | card centering tool | 0.17 | +136% |
| mp3 to midi | 0.74 | -2% | | ai grading（补全显示多为卡牌） | 3.89 | +219% |
| piano transcription | 0.48 | +168% | | handwriting to text | 1.44 | -14% |
| audio to sheet music | 0.45 | +140% | | handwriting ocr | 0.41 | +350% |
| midi to sheet music | 0.29 | +14% | | cursive to text | 0.44 | +5% |
| mp3 to sheet music | 0.22 | +60% | | transkribus | 0.14 | +579% |
| transpose sheet music | 0.14 | +73% | | kurrent | 0.12 | +216% |
| music transcription software | 0.05 | +140% | | bank statement to excel | 0.22 | +58% |
| chords from audio | 0.05 | +267% | | bank statement converter | 0.05 | +135% |
| easy piano | 15.46 | +21% | | receipt to excel | 0.21 | +441% |
| easy piano sheet music | 3.61 | +16% | | make pdf accessible | 0.25 | +713% |
| lead sheet（含无关义） | 8.68 | +32% | | pdf accessibility checker | 0.11 | +464% |
| klangio | 0.07 | - | | alt text generator | 0.12 | -35% |
| songscription | 0.06 | - | | supabase security | 2.09 | +841% |
| generative engine optimization | 2.74 | +151% | | lovable security | 0.35 | +750% |
| ai visibility（多义） | 10.75 | +173% | | llms.txt | 1.16 | +312% |
| pdf translator | 1.88 | +159% | | chat with pdf | 2.10 | +227% |
| image translator | 1.39 | +4% | | manga translator | 0.34 | +70% |
| ai interior design | 4.64 | +103% | | ai transcription | 7.06 | +121% |
| floor plan ai | 2.61 | +268% | | ai product photography | 1.03 | +426% |
| real estate listing description | 0.26 | +647% | | ai menu generator | 0.58 | +200% |
| ai headshot | 3.16 | -29% | | ai logo generator | 2.91 | -52% |
| ai resume builder | 2.30 | -32% | | youtube summarizer | 0.73 | -35% |
| report card comments | 0.74 | -24% | | ai quiz generator | 0.30 | -4% |
| ai worksheet generator | 0.09 | -54% | | ai lesson plan generator | 0.01 | -77% |
| ai humanizer | 30.03 | +34% | | pdf to excel | 13.49 | +35% |

**全球口径**（同样以 "virtual staging" 为锚点）：

| 关键词 | 相对倍数 | 同比 |
| --- | --- | --- |
| bank statement converter | 0.65 | +28% |
| bank statement to excel | 0.70 | +35% |
| handwriting to text | 2.02 | -2% |
| transkribus | 0.45 | +38% |
| audio to sheet music | 0.51 | +167% |
| pdf translator | 5.28 | +63% |
| supabase security | 2.89 | +580% |
| generative engine optimization | 3.40 | +372% |

**数据不可靠（同组里有超大词，小词分辨率不够）**：ai excel formula、invoice ocr、ai image translator、ai subtitle generator。

**量太小为 0**：soap note generator、transcribe handwriting、old handwriting translator、psa pre grade、hum to sheet music、pdf / image to editable ppt。

**地区（近 12 个月，Google Trends 按国家）**：

| 关键词 | 排名前列的国家 |
| --- | --- |
| bank statement converter | 印度 100、巴基斯坦 47、南非 47、斯里兰卡 30、尼泊尔 21、阿联酋 / 马来西亚 / 孟加拉 / 肯尼亚 17、英国 13、澳大利亚 8 |
| handwriting to text | 巴基斯坦 100、印度 96、埃塞俄比亚 86、尼泊尔 82、新加坡 72、肯尼亚 65 |
| audio to sheet music | 韩国 100、新加坡 71、加拿大 / 以色列 / 新西兰 / 香港 / 美国 / 澳大利亚 / 荷兰 42 |
| song to sheet music | 美国 100、澳大利亚 81、韩国 75、新西兰 75、加拿大 68、新加坡 62、英国 50、香港 50 |

## 附录 B：自动补全样本（节选）

| 查询 | 补全 |
| --- | --- |
| how to convert audio to sheet | how to convert audio to sheet music (musescore) / is there an app that converts audio to sheet music / how to convert mp3 to sheet music free |
| can ai make sheet music | can ai make sheet music from a song / can suno ai make sheet music / ai make sheet music from audio |
| easy piano version of | fur elise / hallelujah / moonlight sonata / golden / bohemian rhapsody / … |
| 악보 변환 | 악보 변환 사이트 / 악보 변환 ai / mp3 악보 변환 사이트 |
| 耳コピ ai | 耳コピ ai 無料 / midi / ギター / ピアノ |
| ai grading | ai grading cards / ai grading pokemon / ai grading app pokemon |
| bank statement converter | … free / to excel / ai / to csv / pdf to excel；pdf bank statement to tally xml（印度会计软件） |
| transkribus | transkribus pricing / transkribus alternative / transkribus reddit |

## 附录 C：竞品流量（Tranco 列表 N2PGW，名次越小越大）

| 名次 | 网站 |
| --- | --- |
| 4,943 | musescore.com |
| 10,640 | turboscribe.ai |
| 16,317 | chordify.net |
| 26,219 | chatbase.co |
| 35,675 | moises.ai |
| 107,701 | tryprofound.com |
| 122,031 | soundslice.com |
| 139,418 | otterly.ai |
| 190,825 | peec.ai |
| 191,252 | transkribus.org |
| 315,204 | klang.io |
| 484,020 | songscription.ai |
| 685,983 | docuclipper.com |
| 750,820 | scorecloud.com |
| 920,269 | pokeinvest.io |

**不在前 100 万**：bankstatementconverter.com、handwritingocr.com、vibeappscanner.com、melodyscanner.com、anthemscore.com、cardgrade.io、gradepokemon.com、pregradecards.com、cardgrading.app、tcgrader.com。

## 附录 D：开源组件许可核实结果

| 组件 | 用途 | 许可 | 备注 |
| --- | --- | --- | --- |
| facebookresearch/demucs | 音源分离 | MIT | 约 1.04 万星 |
| spotify/basic-pitch | 音高 → 音符 | Apache-2.0 | 2025-11 仍在更新 |
| marl/crepe | 单音高追踪 | MIT | |
| CPJKU/beat_this | 节拍 / 小节 | MIT（代码和权重） | 部分训练数据有版权或受限许可，需自行评估 |
| mir-aidj/all-in-one | 节拍、段落结构 | MIT | |
| jayg996/BTC-ISMIR19 | 和弦识别 | MIT | 2020 年后未更新 |
| bytedance/piano_transcription | 钢琴逐音转写 | README 标注 Apache 2.0 | Replicate 托管，约 $0.078/次 |
| cuthbertLab/music21 | 乐谱处理 / 编配 | BSD-3-Clause | |
| opensheetmusicdisplay | 浏览器渲染 | BSD-3-Clause | |
| rism-digital/verovio | 渲染 / 导出 | LGPL-3.0 | 作为库或服务调用 |
| CPJKU/madmom | 节拍 / 和弦 | 代码 BSD；**模型文件 CC BY-NC-SA 4.0，不可商用** | 避开 |
| mimbres/YourMT3 | 多乐器转写 | GPL-3.0 | 避开或需法律评估 |

## 附录 E：主要命令记录

```bash
# TrustMRR 公开数据
curl -sL https://trustmrr.com/llms.txt
curl -sL https://trustmrr.com/api/ai/discovery
curl -sL https://trustmrr.com/stats           # 解析 HTML 文本
curl -sL https://trustmrr.com/category/ai
curl -sL https://trustmrr.com/startup/<slug>.md

# Google 自动补全（英文；日/韩/繁中/简中把 hl、gl 换成 ja/jp、ko/kr、zh-TW/tw、zh-CN/cn）
curl "https://suggestqueries.google.com/complete/search?client=firefox&hl=en&gl=us&q=<query>"

# Google Trends：见附录 A 的 pytrends 代码（相关查询和地区用 related_queries() 与 interest_by_region()）

# Exploding Topics 锚点：抓取 https://explodingtopics.com/topic/<slug>，解析 scoreTagTop 里的 Volume

# Tranco
curl -sL -o tranco.zip https://tranco-list.eu/top-1m.csv.zip && unzip tranco.zip
grep ",klang.io$" top-1m.csv

# 许可
gh-axi api repos/<owner>/<repo>
curl -sL https://raw.githubusercontent.com/CPJKU/madmom/main/LICENSE
```

失败记录：
- `chrome-devtools-axi open …` 返回 `BRIDGE_NOT_READY`；直接运行 headless Chrome 报 `FATAL:base/path_service.cc:264] Failed to get the path for 1001`，浏览器类工具不可用。
- Google / Startpage / DuckDuckGo 的结果页用 curl 拿不到有效结果；Bing 返回的地域和查询都不对；Brave 可用一次后返回 429。
- Similarweb 返回空的 HTTP 202；Semrush 的公开域名页返回 404。
