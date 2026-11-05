# 18 章节详细内容要求

## ① Chip Overview（芯片定位）

输出表格：

| 项目 | 内容 |
|------|------|
| 芯片类型 | |
| 主要功能 | |
| 典型应用 | |
| 支持协议/标准 | |
| 核心卖点 | |
| 替代型号（如有） | |

最后输出【设计结论】。

---

## ② Architecture（芯片架构）

分析内部模块组成、数据流、模拟/数字模块、外围依赖。

**必须绘制文字版框图**，使用 `<pre class="diagram">`：

```
Power  →  LDO  →  Core
                    ↓
              MAC / SoC
                    ↓
              RMII  →  PHY  →  Transformer  →  RJ45
```

最后总结最值得重点关注的模块。

---

## ③ Functional Block（功能模块）

输出表格（不要重复 Architecture）：

| 模块 | 功能 | 设计关注点 |
|------|------|-----------|

---

## ④ Pin Definition（引脚）

输出表格：

| Pin | 名称 | 类型 | 功能 | 原理图连接建议 | 注意事项 |

必须分类标记：Power / Ground / Clock / Reset / Boot / Strap / 高速信号 / 模拟信号。
高风险引脚增加 badge。

---

## ⑤ Power Analysis（供电分析）

输出所有 Power Rail：

| 电源 | 电压 | 用途 | 是否必须 | 去耦建议 | 页码 |

继续分析：内部LDO、外部LDO、上电时序、掉电要求、Power Domain、电源纹波敏感点、Layout要点。
最后输出【供电设计建议】。

---

## ⑥ Clock Analysis（时钟）

整理：Clock来源、PLL、输入/输出频率、晶振要求、精度、Layout建议。

| 项目 | 参数 | Datasheet依据 | 设计意义 |
|------|------|--------------|---------|

最后输出【Clock设计重点】。

---

## ⑦ Reset Analysis（复位）

分析：Reset Pin、POR、Brown-out、Reset Timing、RC建议、与Strap采样关系。

| 项目 | Datasheet要求 | 页码 | 设计意义 |
|------|-------------|------|---------|

最后输出【Reset设计重点】。

---

## ⑧ Boot / Strap Analysis（引导/配置）

整理所有 Boot/Strap Pin：

| Boot/Strap Pin | 复用功能 | 默认状态 | 推荐上下拉 | 采样时机 | 错误配置后果 | 风险 |

---

## ⑨ Electrical Characteristics（关键电气参数）

| 参数 | Min | Typ | Max | 单位 | 页码 | 设计意义 |
|------|-----|-----|-----|------|------|---------|

重点关注：Absolute Maximum / Recommended Operating / Power / Current / Temperature / Logic Threshold / Timing / ESD Rating。

---

## ⑩ Recommended External Components（外围器件）

| 器件 | 推荐值 | 作用 | 是否关键 | 是否可调整 | 页码 |
|------|--------|------|---------|-----------|------|

涵盖：电容、电阻、晶振、Ferrite Bead、TVS、Magnetics、Pull-up/down、Bootstrap Resistor。

---

## ⑪ Typical Application（典型应用电路）

分析外围器件作用、启动路径、信号路径、稳定性影响因素、易错位置。

| 电路位置 | 器件/网络 | 作用 | 设计风险 | 检查建议 |
|----------|----------|------|---------|---------|

最后输出【原理图设计重点】。

---

## ⑫ PCB Layout

整理：高速/模拟/数字网络、阻抗控制、长度匹配、地设计、回流路径、散热、推荐布局顺序。

| Layout对象 | 设计要求 | 风险 | 检查方式 |
|-----------|---------|------|---------|

最后输出【Layout Checklist】。

---

## ⑬ EMI / ESD

分析：ESD/EMI等级、滤波、TVS、Ferrite、参考地、屏蔽、Cable辐射路径。

| 风险源 | 可能问题 | 设计建议 | 验证方式 |
|--------|---------|---------|---------|

总结最容易EMI不过的地方。

---

## ⑭ Bring-up（上电验证）

| Step | 项目 | 验证内容 | 测试点 | 判定标准 |
|------|------|---------|--------|---------|

必须覆盖：Power → Clock → Reset → Boot/Strap → 通信 → 功能验证 → 异常回退测试。

---

## ⑮ Debug（调试）

| 常见故障 | 可能原因 | 建议测试点 | 建议测量仪器 | 推荐Debug顺序 |
|---------|---------|-----------|------------|-------------|

覆盖：上电异常、时钟异常、通信异常、功能异常、EMI/ESD异常、量产异常。

---

## ⑯ Risk Analysis（风险分析）

按风险等级分类输出：

| 风险等级 | 风险项 | 原因 | 后果 | 规避措施 |
|---------|--------|------|------|---------|

分类：
- 🔴 高风险
- 🟡 中风险
- 🟢 建议优化

包含：Datasheet易遗漏信息、默认配置陷阱、限制条件、官方Warning。

---

## ⑰ Hardware Review Checklist（硬件评审检查表）

| 检查项 | 风险 | Datasheet依据 | 人工确认方式 |
|--------|------|-------------|------------|

必须写具体检查项，例如：
- √ RBIAS 是否采用 1% 精度？
- √ 去耦电容是否靠近 Pin？
- √ Strap 是否满足采样时间？
- √ 晶振负载电容是否正确？
- √ 差分线阻抗是否满足要求？
- √ Reset 释放时序是否满足？

---

## ⑱ Hardware Design Note（硬件设计说明）

一页设计总结，作为项目设计文档，包括：
- 芯片简介
- 设计建议
- PCB 建议
- Bring-up 建议
- Debug 建议
- 主要风险

精简、工程风格，不写营销文案。
