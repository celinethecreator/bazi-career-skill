# 职途八字 · BaZi Career Explorer

**把职业困境变成值得验证的方向。**

一个应用型 Agent Skill：收集用户职业背景、职业卡点与自己的八字后，贯穿八字文化探索，借助宿主联网能力发现真实岗位，交付方向比较、能力缺口和行动计划。

版本：0.1.0（预览版）。这是 Skill 与本地辅助脚本，不是独立网页应用，也不自带大模型或搜索API。

## 五种使用场景

- 校招：专业和兴趣如何转成可投递岗位？
- 社招：已有经历能迁移到哪些岗位，为什么投递没反馈？
- 职业瓶颈：问题在能力、角色、组织还是发展路径？
- Offer选择：两份工作如何比较，哪些条款还要问清楚？
- 跳槽转型：适合探索什么方向，怎样低成本验证？

## 使用方式与能力要求

本项目以可安装的 Agent Skill 交付。支持导入 Skill 的宿主可加载整个 `skills/bazi-career` 目录，并使用宿主已有的模型。Skill 本身没有 API Key 配置。

| 你的工具具备什么能力 | 可以做到什么 |
|---|---|
| 支持 Skill 导入或项目级技能目录 | 加载完整的访谈、八字解读和方向探索流程 |
| 只有普通聊天界面 | 可上传或粘贴 SKILL.md 和相关 references，按提示词工作流试用 |
| 支持脚本和 Python 环境 | 可运行随附排盘脚本处理支持范围内的出生资料 |
| 支持联网搜索和打开网页 | 搜索岗位并核验招聘原页 |
| 无脚本或无联网 | 可直接提供四柱或排盘截图。岗位环节给搜索词，或者分析用户提交的 JD，标清核验状态 |

千问、DeepSeek 等可作为对话模型。能否一键安装、读附件、运行 Python 或联网，由具体使用的客户端或 Agent 平台决定。普通聊天入口可按上表手动试用。独立网页若要提供实时 AI 对话和岗位搜索，需另外配置推理与搜索能力。服务端统一配置时，用户无需提供自己的 Key。

## 安装步骤

以下终端命令适用于 macOS / Linux。也可以在仓库首页点 **Code → Download ZIP**，解压后找到 `skills/bazi-career`。

### 1. 下载并确认文件夹

```bash
git clone https://github.com/celinethecreator/bazi-career-skill.git
cd bazi-career-skill
ls skills/bazi-career
```

看到 `SKILL.md`、`references` 和 `scripts` 后，按你使用的工具选一种安装方式。

### 2. 安装到你的工具

**Codex（本机个人技能）**

```bash
mkdir -p ~/.agents/skills
cp -R skills/bazi-career ~/.agents/skills/
```

打开新的本机 Codex 对话，输入 `$bazi-career`。项目级安装可把同一个文件夹复制到目标项目的 `.agents/skills/`。[Codex 官方说明](https://learn.chatgpt.com/docs/build-skills)

**Claude Code（本机个人技能）**

```bash
mkdir -p ~/.claude/skills
cp -R skills/bazi-career ~/.claude/skills/
```

在 Claude Code 输入 `/bazi-career`。项目级安装可把同一个文件夹复制到目标项目的 `.claude/skills/`。[Claude Code 官方说明](https://code.claude.com/docs/en/skills)

**其他工具**：有 Skill 导入功能时，选择整个 `skills/bazi-career` 文件夹。普通聊天可上传 `SKILL.md` 和 `references/` 下的文件，请助手按文件里的流程试用。

### 云端聊天（DeepSeek / 豆包 / 千问 / Kimi 等）

1. 打开 [通用对话 TXT](cloud-chat.txt)，复制全部内容。
2. 在你平时使用的 AI 网页或 App 新建对话，粘贴并发送。如果客户端接受 TXT 文件，也可以上传后发送「请按这份材料开始访谈」。
3. 按助手的提问提供职业背景、卡点和已排好的四柱。实时岗位搜索取决于当前客户端是否能联网。

这份 TXT 是为普通聊天准备的独立版本，不用安装 Python 或填写 API Key。新对话需重新提供文本。支持原生 Skill 导入的 Agent 平台可改用完整的 `skills/bazi-career` 文件夹。原生安装、排盘脚本、附件读取和联网能力以客户端为准。

### 3. 第一次使用

> 使用职途八字。我目前做市场运营，想转型但不知道投哪些岗位。请先问我必要的信息，再结合我的八字和工作经历梳理方向。

已有四柱可以直接输入。宿主支持读图时，也可以上传排盘截图。实时岗位搜索需要宿主具备联网能力。

### 4. 可选：本地排盘依赖

只有需要按出生资料运行本地排盘脚本时，才需要 Python 3.9+。在下载后的仓库根目录运行：

```bash
python3 -m venv .venv
. .venv/bin/activate
python -m pip install -r requirements.txt
```

Windows PowerShell 可用 `py -m venv .venv`，再执行 `.\.venv\Scripts\Activate.ps1` 和 `python -m pip install -r requirements.txt`。运行排盘时，请助手使用该虚拟环境的 Python。

### 咨询第一步：职业背景、卡点与八字

推荐排盘项目：[6tail/lunar-python](https://github.com/6tail/lunar-python)。它是 MIT 许可的开源历法库，支持四柱和十神计算。本项目的本地排盘脚本已使用它。已有四柱或排盘截图可直接提交；没有现成命盘时，提供出生资料，由 Skill 调用本地脚本辅助排盘，并注明计算口径。

用户可以上传简历、粘贴摘录或口述经历。Agent 会从个人贡献与可观察结果里提炼亮点，并对照目标岗位的任务。

确认命盘后，访谈用与卡点相关的八字主题开启，再结合具体经历调整问题、方向与岗位搜索，帮助用户说清想保留的任务、想改变的环境和当前的现实底线。方法来源与原创中文对话见[职业探索访谈](skills/bazi-career/references/career-conversation.md)。

## 示例输入与交付

出生信息、职业访谈分别处理，职业搜索不携带出生信息。匿名Offer比较示例与查询示例位于 `examples/`，全部为虚构数据。

```bash
python skills/bazi-career/scripts/search_plan.py < examples/search-input.json
python skills/bazi-career/scripts/rank_options.py < examples/offer-input.json
python skills/bazi-career/scripts/chart.py < examples/birth-input.json
```

报告包括：卡点诊断、八字与经历对照、三个职业方向、岗位原页链接与核验状态、选择比较、7天与30天计划。模板在 `skills/bazi-career/references/report-template.md`。

## 能力与边界

| 能力 | 本版状态 |
|---|---|
| 五场景咨询流程 | 已提供工作指令与分场景框架 |
| 四柱与十神计算 | lunar-python 1.4.8适配器，限定中国大陆公历民用时间 |
| 不确定时辰 | 分钟级枚举不同候选盘，保留不确定性 |
| 八字到职业探索 | 传统主题→工作方式假设→经历支持与反例 |
| 实时岗位发现 | 由宿主搜索工具执行，要求打开原页核验 |
| 搜索计划与现实比较 | 有可运行脚本；比较权重需用户确认 |
| 真太阳时/农历/海外历史时区 | 本地脚本不支持，需外部核验 |
| 大运/流年/强弱喜用自动计算 | 未实现，不能伪称有确定结果 |
| 自动投递/招聘者联系 | 不执行 |

八字是传统文化解释框架，没有被科学验证能预测职业适配或职业结果。本工具服务个人探索；现实选择需要结合技能、资格、收入、工作条件与实际体验。排盘回归测试不验证命理预测有效性。不得将出生信息或命理输出用于招聘筛选、拒聘或晋升。

## 验证

```bash
python -m unittest discover -s tests -v
python tools/validate_release.py
```

测试覆盖上游公开排盘样例、时辰不确定、换日差异、输入边界、硬条件排除、未知值与权重校验、搜索隐私字段。`evals/scenarios.md` 提供真实宿主的行为验收任务；自动测试不等于联网端到端测试。

## 发布与贡献

仓库根目录放公开说明/许可证/测试，安装包位于 `skills/bazi-career`。在自己的 GitHub 新建仓库后，将本目录推送到目标仓库；本源码不附任何账号凭证。

请用虚构案例报告问题，注明宿主、场景、预期/实际行为和已删隐私的输出。详情见 CONTRIBUTING.md。

本项目原创咨询流程与脚本使用 MIT 许可证；依赖 lunar-python（MIT）与 PyYAML（MIT）。没有复制第三方命理 Skill 或古籍整理内容。依赖和灵感来源见 THIRD_PARTY_NOTICES.md。
