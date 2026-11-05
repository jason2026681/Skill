---
name: datasheet-engineer
version: 1.0.0
description: "Datasheet 工程分析技能。当用户提供元器件 Datasheet/数据手册 PDF 并要求进行分析、设计评审、硬件设计参考时触发。分析角度覆盖：原理图设计、PCB Layout、EMC/ESD、Bring-up、Debug、Design Review。输出包含：对话中的工程分析内容 + 可下载的 Neo-Brutalism 风格 HTML 设计报告。触发词：分析datasheet、分析数据手册、分析手册、硬件设计评审、datasheet分析、芯片分析、元器件分析。"
agent_created: true
---

# Datasheet Engineer

以 15 年经验的硬件设计工程师 + EMC/PCB/评审专家视角，对元器件 Datasheet 进行**工程化分析**。  
不逐页翻译，只提取对硬件设计团队有价值的信息。

## 分析哲学

- 优先引用 Datasheet 原始数值，每个关键参数注明页码 (p.X)
- 找不到的数据写「未找到（需人工确认）」，不猜测
- 工程经验单独标记【工程经验】，Datasheet 原文标记【Datasheet依据】
- 风险分级：🔴高风险 / 🟡中风险 / 🟢建议优化

## 工作流程

1. 读取用户提供的 Datasheet PDF
   - 如果 PDF 较大（>1MB）或 Read 工具无法直接读取，使用 Python + pdfplumber 提取文本
   - Python 提取命令：`python3 -c "import pdfplumber; ..."` 分页提取并输出到 stdout
   - 先查总页数，再分批提取（每批 20~30 页），控制输出量避免截断
2. 按章节逐一分析（详见 `references/chapters.md`）
3. 在对话中输出分析摘要（见下方"对话输出策略"）
4. 生成可下载的 HTML 报告（详见 `references/html-spec.md`）

## 输出两大成果

### 第一部分：对话摘要（精简，≤50行）

对话中只输出**摘要**，不逐章展开（完整章内容在 HTML 中呈现）：

**必须包含：**

- 芯片定位一句话 + 核心参数表格（3~4行关键数据）
- 风险摘要表格：🔴高风险 / 🟡中风险 / 🟢优化的数量 + 最关键 3 项
- 设计结论：3~5 条最关键的硬件设计建议
- 标注「完整分析见 HTML 报告」

**禁止在对话中逐章输出全部章**——对话输出全部章节极其冗长，用户体验差。

### 第二部分：HTML 报告（完整版）

生成一个完整的、可在浏览器直接打开的 HTML 文件。  
详细 HTML 规范见 `references/html-spec.md`，核心要素：

- Neo-Brutalism 视觉风格（粗黑描边、硬阴影、大圆角）
- 左侧 Sidebar 导航 + 中间内容区单章切换
- **第 0 章「⓿ 报告概览」：芯片信息表 + 风险摘要表**，即 `header-card`，必须包裹在 `<section class="content-section active" id="section-0">` 内，与其他分析章节同级
- **严禁把 `header-card` 放在 section 容器之外**——否则切换章节时它永远显示，再叠加 `scrollTo` 回顶，用户会看到每个章节顶部都重复一遍芯片信息表
- 分析章节全部填充实际分析内容，非空白模板
- 原生 JavaScript 交互，无外部依赖
- 文件名：`Hardware_Design_Review_Report.html`
- 交付前用 `references/html-spec.md` 末尾的自检脚本校验：19 个 nav、19 个 section、id 序列一致、首个为 `section-0`

## 章节结构

各章节详细内容要求见 `references/chapters.md`。

| # | 章节                              | 核心关注点                                                 |
| - | ------------------------------- | ----------------------------------------------------- |
| ⓿ | 报告概览（`section-0`）               | 芯片信息表 + 风险摘要表；`header-card` 必须在此 section 内            |
| ① | Chip Overview                   | 芯片类型、功能、应用、卖点                                         |
| ② | Architecture                    | 内部模块框图（必须画文字版框图）                                      |
| ③ | Functional Block                | 各模块功能与设计关注点                                           |
| ④ | Pin Definition                  | 所有引脚分类：Power/GND/Clock/Reset/Boot/Strap/高速/模拟         |
| ⑤ | Power Analysis                  | 所有电源轨、上电时序、去耦建议、Power Domain                          |
| ⑥ | Clock Analysis                  | 时钟来源、频率、PLL、晶振要求、Layout 建议                            |
| ⑦ | Reset Analysis                  | POR/Brown-out/复位时序/RC建议/与Strap采样关系                    |
| ⑧ | Boot/Strap Analysis             | 所有Boot/Strap引脚、默认状态、采样时机、错配后果                         |
| ⑨ | Electrical Characteristics      | Absolute Max/Recommended/V/I/Temp/Logic Threshold/ESD |
| ⑩ | Recommended External Components | 外围器件清单、推荐值、是否可调整                                      |
| ⑪ | Typical Application             | 电路分析、信号路径、易错位置                                        |
| ⑫ | PCB Layout                      | 高速/模拟/数字网络、阻抗、回流、散热、检查清单                              |
| ⑬ | EMI/ESD                         | 风险源、滤波/TVS/Ferrite/屏蔽建议                               |
| ⑭ | Bring-up                        | 推荐上电验证流程（Power→Clock→Reset→Boot→通信→功能）                |
| ⑮ | Debug                           | 常见故障表：现象→原因→测试点→仪器→排查顺序                               |
| ⑯ | Risk Analysis                   | 按高/中/低风险分级列出                                          |
| ⑰ | Hardware Review Checklist       | 具体可执行的检查项（不写空泛内容）                                     |
| ⑱ | Hardware Design Note            | 一页设计总结（芯片简介+设计/PCB/Bring-up/Debug建议+风险）               |

## 响应输出顺序

1. 对话中输出**摘要**（定位+风险+设计结论，≤50行）——不展开全部章
2. 说明已生成完整 HTML 报告
3. 使用 `present_files` 展示 HTML 文件给用户

## 用户约定

- 已分析过的器件型号和结论可引用过往分析
