# 高中学习台 · 六科知识点与错题练习

给高中生复习、查知识点、重做错题用的静态站点。纯前端，零外部依赖，离线可用。

**线上地址：** https://luofeicq.github.io/kb-site/

## 结构

```
index.html              门户：全站搜索 + 六科入口（每科两个板块）

math-knowledge.html     数学知识点（7 章）      math-mistakes.html     数学错题（8 道）
physics-knowledge.html  物理知识点（6 专题+附录） physics-mistakes.html  物理错题（11 道）
bio-knowledge.html      生物知识点（12 章）      bio-mistakes.html      生物错题（8 道）
chem-knowledge.html     化学知识点（13 章）      chem-mistakes.html     化学错题（8 道）
chinese-knowledge.html  语文知识点（6 章）       chinese-mistakes.html  语文错题（6 道）
english-knowledge.html  英语知识点（6 章）       english-mistakes.html  英语错题（6 道）

assets/base.css         全站基础样式（顶栏、版式、表格、搜索面板、六科配色）
assets/mistakes.css     错题页专用样式
assets/site.js          阅读进度条 / 返回顶部 / 锚点闪烁
assets/search.js        站内搜索组件（页面级 + 全站级共用）
assets/mistakes.js      错题练习逻辑（筛选 / 搜索 / 重做 / 标记掌握 / 进度）
assets/index.js         全站搜索索引（442 条，构建时自动生成，勿手改）

data/mistakes-*.js      六个科目的错题数据（可直接编辑）
_build/build_site.py    构建脚本：补锚点 id、注入切换条、生成错题页与全站索引
```

## 页面约定

每个学科都分两个板块，页面顶部有「知识点学习 / 错题练习」切换条：

- **知识点页**：左侧目录吸顶，滚动自动高亮；页内搜索（`/` 或 `Ctrl/Cmd + K`）；章节含知识主线、高频考点、易错辨析、口诀、例题精解、分层练习（答案折叠）。
- **错题页**：按专题筛选、按关键词搜索、点击展开解析、一键重做（先收起答案并居中定位）、标记「已掌握」。进度存在浏览器 localStorage，换设备不同步。

## 搜索

- `/` 或 `Ctrl/Cmd + K` 唤起，`↑↓` 选择，`Enter` 打开，`Esc` 关闭
- 首页搜全站（442 条：章 / 节 / 考点 / 错题），学科页只搜本页
- 整词优先，整词无果按两字片段兜底（「遗传规律」也能命中「遗传基本规律与伴性遗传」）
- 排序：标题命中 > 分组命中 > 词频

## 内容说明

物理错题来自真实错题本记录；其余五科的错题为按高考常见陷阱编排的典型例题，非原卷摘录。

## 修改与发布

```bash
cd H:/BaiduSyncdisk/kb-site

# 1. 改内容：知识点直接改 *-knowledge.html，错题改 data/mistakes-*.js
# 2. 重新构建索引与错题页（幂等，可反复执行）
python _build/build_site.py

# 3. 本地预览
python -m http.server 8000    # 打开 http://localhost:8000

# 4. 发布
git add -A && git commit -m "更新内容" && git push
```

推送后 GitHub Pages 约 25 秒自动重新发布。
