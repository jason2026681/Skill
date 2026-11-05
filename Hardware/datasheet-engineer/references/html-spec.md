# HTML 报告规范

生成一个完整的、纯静态的 HTML 文件，可在浏览器直接打开。

## 整体结构

```
<!DOCTYPE html>
<html>
<head><style> (all CSS) </style></head>
<body>
  左侧 Sidebar（1 个「报告概览」导航 + 18 章节导航 = 共 19 个按钮）
  中间 Main Content（仅当前选中章节可见，其他 display:none）
    ├─ section-0：报告概览（芯片信息表 + 风险摘要表）
    └─ section-1 ~ section-18：18 个分析章节
  <script> (all JS) </script>
</body>
</html>
```

**禁止：** 外部 CSS/JS/字体/图片资源，Markdown 混入 HTML。

## 【强制】header-card 必须作为 section-0 存在

`header-card`（含标题区 + 芯片信息表 + 风险摘要表）**必须**包裹在 section 容器内，作为第 0 章「报告概览」，与 18 个分析章节同级，通过同一套 JS 切换显示。

```html
<!-- 正确 -->
<main class="main">
  <section class="content-section active" id="section-0">
    <div class="header-card">
      <h1 class="report-title">Hardware Design Review Report</h1>
      ...
    </div>
  </section>
  <section class="content-section" id="section-1">...</section>
</main>

<!-- 错误：header-card 直接放在 main 下，会导致每个章节顶部都重复出现 -->
<main class="main">
  <div class="header-card">...</div>   <!-- ❌ 禁止 -->
  <section class="content-section active" id="section-1">...</section>
</main>
```

**违规后果：** 因为切换逻辑只对 `.content-section` 生效，放在 section 外的 `header-card` 永远不会被隐藏；再叠加导航点击时的 `window.scrollTo({top:0})`，用户会看到「每点一章，先出现一遍芯片信息表」，误认为是内容重复。

**配套要求：**
1. Sidebar 必须有 19 个 `.nav-item`，第一个为「⓿ 报告概览 · 芯片信息」，`data-target="section-0"`，并带 `active` 类（页面默认打开概览）。
2. `section-0` 同样带 `active` 类；`section-1` **不再**带 `active`。
3. 章节编号从「①」开始，与「⓿」形成连续视觉序列，不要占用 ⓿。
4. 页脚 `<footer class="foot">` 允许放在所有 section 之外（属正常页脚，不算重复内容），内容不得包含「Copyright / © / 版权所有」等版权字样。


## Neo-Brutalism 视觉风格

### 核心要素
- body 背景：浅色 (#FFF7E8 或 #F7F4FF)
- 卡片：粗黑边框 3~4px + 硬阴影 6~8px 0 #111 + 大圆角 18~24px
- 标题：大字号 + 粗体 + 黑色描边感
- 表格：黑色边框，th 使用高饱和色背景 (如 #FFD84D)
- 禁止：无边框卡片、轻阴影、玻璃拟态、低对比灰

### 关键 CSS 变量

```css
body {
  margin: 0;
  background: #FFF7E8;
  color: #111;
  font-family: Arial, "Microsoft YaHei", sans-serif;
}

.page {
  min-height: 100vh;
  display: grid;
  grid-template-columns: 320px 1fr;
  gap: 24px;
  padding: 24px;
}
```

## 布局：两列 Grid

### 左侧 Sidebar（~320px）

```css
.sidebar {
  position: sticky;
  top: 24px;
  height: calc(100vh - 48px);
  overflow-y: auto;
  background: #FFFFFF;
  border: 4px solid #111;
  border-radius: 24px;
  box-shadow: 8px 8px 0 #111;
  padding: 18px;
}
```

导航按钮：
```css
.nav-item {
  width: 100%;
  border: 3px solid #111;
  border-radius: 16px;
  padding: 12px 14px;
  margin-bottom: 10px;
  background: #F7F4FF;
  color: #111;
  cursor: pointer;
  text-align: left;
  font-weight: 900;
  box-shadow: 4px 4px 0 #111;
}

.nav-item.active {
  background: #FFD84D;
  transform: translate(-2px, -2px);
  box-shadow: 6px 6px 0 #111;
}
```

章节列表（共 19 个导航按钮：1 个概览 + 18 个分析章节）：
```
⓿ 报告概览 · 芯片信息      ← data-target="section-0"，带 active（默认显示）
① Chip Overview
② Architecture
③ Functional Block
④ Pin Definition
⑤ Power Analysis
⑥ Clock Analysis
⑦ Reset Analysis
⑧ Boot / Strap Analysis
⑨ Electrical Characteristics
⑩ Recommended External Components
⑪ Typical Application
⑫ PCB Layout
⑬ EMI / ESD
⑭ Bring-up
⑮ Debug
⑯ Risk Analysis
⑰ Hardware Review Checklist
⑱ Hardware Design Note
```

导航按钮 HTML 示例（注意第 1 个是 section-0）：
```html
<button class="nav-item active" data-target="section-0">⓿ 报告概览 · 芯片信息</button>
<button class="nav-item" data-target="section-1">① Chip Overview</button>
```

### 中间 Main Content

```css
.main { min-width: 0; }

.header-card, .content-card, .metric-card {
  background: #FFFFFF;
  border: 4px solid #111;
  border-radius: 24px;
  box-shadow: 8px 8px 0 #111;
}

.content-section { display: none; }
.content-section.active { display: block; }
```

## 第 0 章：报告概览（section-0 内容）

即 `header-card` 的内容，**只在 ⓿ 概览章显示**，不得外置。包含：

1. **标题区域：**
   - 主标题：Hardware Design Review Report
   - 副标题：Datasheet Engineering Analysis for Hardware Design / PCB Layout / Bring-up / Debug

2. **芯片信息卡片：**

| 项目 | 内容 |
|------|------|
| 芯片/器件型号 | |
| 厂商 | |
| Datasheet版本 | |
| 文档日期 | |
| 分析日期 | |
| 适用项目 | |
| 分析人 | |

3. **风险摘要卡片：**

| 风险类型 | 数量 | 重点关注 |
|----------|------|---------|
| 🔴 高风险 | | |
| 🟡 中风险 | | |
| 🟢 建议优化 | | |
| 人工确认项 | | |

> 可选增强：在标题下方用 `.chip-pill` 徽章行快速展示芯片特性标签与风险计数（例：`2.4G Wi-Fi + BLE + SLE SoC`、`🔴 高风险 8 项`），提升概览页的信息密度。

## 每个分析章节内容结构（section-1 ~ section-18）

每个 section 必须包含：
1. 章节标题
2. 章节说明（≤300字）
3. 关键表格（1~3个，使用 HTML `<table>`）
4. Datasheet依据 callout
5. 工程经验 callout（如适用）
6. 风险提示（如适用）
7. 【设计结论】

## Callout 样式

```css
.callout {
  padding: 16px 18px;
  border-radius: 16px;
  border: 3px solid #111;
  margin: 16px 0;
}

.callout.ds {
  background: #E8F4FD;
  border-left: 8px solid #2563EB;
}

.callout.exp {
  background: #FFF3CD;
  border-left: 8px solid #F59E0B;
}

.callout.risk {
  background: #FFE0E0;
  border-left: 8px solid #DC2626;
}

.design-conclusion {
  background: #E8FFE8;
  border: 3px solid #111;
  border-left: 8px solid #16A34A;
  border-radius: 16px;
  padding: 16px 18px;
  margin: 16px 0;
}
```

## Risk Badge 样式

```css
.badge {
  display: inline-block;
  padding: 4px 12px;
  border-radius: 12px;
  border: 2px solid #111;
  font-weight: 900;
  font-size: 13px;
}

.badge.danger  { background: #FF6B6B; }   /* 🔴 高风险 */
.badge.warning { background: #FFD84D; }    /* 🟡 中风险 */
.badge.success { background: #51CF66; }    /* 🟢 建议优化 */
.badge.info    { background: #74C0FC; }    /* 人工确认 */
```

## 文字框图样式

```css
pre.diagram {
  background: #F4F4F4;
  border: 3px solid #111;
  border-radius: 16px;
  padding: 18px;
  font-family: 'Courier New', monospace;
  font-size: 14px;
  line-height: 1.8;
  overflow-x: auto;
  white-space: pre;
}
```

## 表格样式

```css
table {
  width: 100%;
  border-collapse: collapse;
  background: #FFFFFF;
  border: 3px solid #111;
  margin: 12px 0;
}

th, td {
  border: 2px solid #111;
  padding: 10px 12px;
}

th {
  background: #FFD84D;
  font-weight: 900;
}
```

## JavaScript 交互

原生 JS，无框架依赖。点击 Sidebar 按钮切换内容：

```js
const navItems = document.querySelectorAll('.nav-item');
const sections = document.querySelectorAll('.content-section');

navItems.forEach(item => {
  item.addEventListener('click', () => {
    const target = item.dataset.target;

    navItems.forEach(i => i.classList.remove('active'));
    item.classList.add('active');

    sections.forEach(section => {
      section.classList.remove('active');
    });

    document.getElementById(target).classList.add('active');
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
});
```

导航按钮需要 `data-target` 属性，对应 section id：
```html
<button class="nav-item active" data-target="section-0">⓿ 报告概览 · 芯片信息</button>
<button class="nav-item" data-target="section-1">① Chip Overview</button>
```

内容区（注意 header-card 在 section-0 内部）：
```html
<section class="content-section active" id="section-0">
  <div class="header-card">...</div>
</section>
<section class="content-section" id="section-1">...</section>
<section class="content-section" id="section-2">...</section>
```

**默认选中 section-0**（报告概览页）。`section-0` 与第一个 nav 按钮同时带 `active` 类，其余 section 不带。

## 交付前自检（必须执行）

生成 HTML 后用脚本校验以下三项，全部通过才算完成：

| 检查项 | 期望值 |
|--------|--------|
| `.nav-item` 数量 | **19** |
| `.content-section` 数量 | **19** |
| nav 的 `data-target` 序列 与 section 的 `id` 序列 | **完全一致**，且第一个为 `section-0` |

```python
import re

s = open('Hardware_Design_Review_Report.html', encoding='utf-8').read()

# 先剥离 HTML 注释，避免注释里出现的 header-card / section 字样造成误判
clean = re.sub(r'<!--.*?-->', '', s, flags=re.S)

navs = re.findall(r'data-target="([^"]+)"', clean)
ids  = re.findall(r'<section class="content-section[^"]*" id="([^"]+)"', clean)

assert len(navs) == 19, f'nav 数量应为 19，实际 {len(navs)}'
assert len(ids) == 19, f'section 数量应为 19，实际 {len(ids)}'
assert navs == ids, 'nav 的 data-target 与 section id 序列不一致'
assert ids[0] == 'section-0', '缺少报告概览章（section-0）'

# header-card 必须出现在 section-0 内部，且不得出现在 main 与首个 section 之间
main_body = re.search(r'<main class="main">(.*?)</main>', clean, re.S)
assert main_body, '未找到 <main> 容器'
body = main_body.group(1)
assert body.lstrip().startswith('<section'), 'main 下第一层元素必须是 section，不能是裸 header-card'
assert 'header-card' in body.split('</section>', 1)[0], 'header-card 不在 section-0 内部'

# active 唯一性：默认只能打开一章，且必须是 section-0
active_secs = re.findall(r'<section class="content-section active" id="([^"]+)"', clean)
assert active_secs == ['section-0'], f'带 active 的 section 应仅为 section-0，实际 {active_secs}'
active_navs = re.findall(r'<button class="nav-item active" data-target="([^"]+)"', clean)
assert active_navs == ['section-0'], f'带 active 的 nav 应仅为 section-0，实际 {active_navs}'

print('自检通过：19 nav / 19 section / id 一致 / active 唯一且为 section-0 / header-card 位于 section-0 内')
```

**注意：** 必须先剥离注释再匹配。生成 HTML 时若在 section 附近写了「原 header-card 独立成章」这类注释，未剥离会对 `header-card` 的位置检查产生误报。

## 响应式布局（移动端）

```css
@media (max-width: 960px) {
  .page {
    grid-template-columns: 1fr;
  }

  .sidebar {
    position: relative;
    top: 0;
    height: auto;
  }

  .nav-list {
    display: flex;
    overflow-x: auto;
    gap: 10px;
  }

  .nav-item {
    white-space: nowrap;
    min-width: max-content;
  }
}
```

## 页码引用

统一格式：`p.5` / `p.12` / `p.52`

## 注意事项

- 每个章节如果资料中没有对应信息，保留章节但写「未找到（需人工确认）」
- 所有 critical 数据必须填实，不要留空位
- HTML 内容必须完整填充分析内容，不要输出空模板
