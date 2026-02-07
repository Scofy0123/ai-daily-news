---
name: ai-news-daily
description: 每日AI新闻聚合器 - 自动抓取并展示AI领域最新重点新闻，包括美国/中国AI大公司动态、GitHub热门项目、AI YouTuber视频总结。当用户询问"AI新闻"、"今天AI有什么新闻"、"获取AI资讯"时触发。
---

# AI Daily News Aggregator / 每日AI新闻聚合器

自动聚合AI领域每日新闻，生成美观的HTML页面展示，支持历史记录查看（最近7天）。

## 核心功能

1. 🇺🇸 **美国AI大公司** - OpenAI, Anthropic, Google, Meta等官方动态
2. 🔥 **GitHub热门项目** - 现象级AI开源项目（如OpenClaw等）
3. 🇨🇳 **中国AI大公司** - 阿里、腾讯、字节、Kimi、智谱等
4. 📺 **YouTube AI精华** - 头部AI博主视频内容总结

## 工作流程

当用户请求AI新闻时，执行以下步骤：

### Step 1: 从官方博客获取新闻

使用 `WebFetch` 直接访问官方博客，获取**真实可靠**的新闻：

**美国AI公司官方博客**：
```
OpenAI Blog: https://openai.com/blog/
Anthropic News: https://www.anthropic.com/news
Google AI Blog: https://blog.google/technology/ai/
Meta AI Blog: https://ai.meta.com/blog/
```

**工作方式**：
1. 使用WebFetch访问每个官方博客首页
2. 提取最新2-3篇文章的标题、摘要、链接和发布日期
3. 只选择最近7天内发布的文章
4. 所有链接都是官方真实链接，100%可访问

**GitHub热门AI项目**：
```
直接访问：https://github.com/trending?since=daily
```
使用WebFetch抓取今日trending项目的：
- 项目名称和链接
- Star数量和今日增长
- 项目描述

**中国AI公司新闻**：
由于官方博客较少，使用WebSearch搜索，但**必须验证**：
```
搜索："阿里通义千问" OR "腾讯混元" OR "字节豆包" OR "Kimi" OR "智谱GLM" 最新发布 2026
```
然后使用WebFetch验证每个链接

**YouTube AI视频**：
脚本会自动抓取以下精选AI频道的最新视频：
- **官方频道**：OpenAI, Anthropic, Google DeepMind, Runway, Meta AI
- **访谈/播客**：Lex Fridman, Lenny's Podcast, Peter Yang, Dwarkesh Podcast, Unsupervised Learning, Training Data, Latent Space, No Priors
- **教程/解说**：Andrej Karpathy, Jeff Su, Tina Huang, Theoretically Media, Matt Wolfe, Matthew Berman, Curious Refuge, Olivio Sarikas, Riley Brown, Greg Isenberg

### Step 2: 验证官方博客内容

**对于官方博客（OpenAI/Anthropic/Google/Meta）**：
- 直接从WebFetch返回的内容提取文章信息
- 官方博客链接格式通常为：`https://官方域名/blog/文章标题`
- 如果WebFetch返回的内容中包含文章标题，构建链接为：`https://官方域名/blog/`
- 标注来源为"官方博客"

**对于GitHub Trending**：
- 直接使用 `https://github.com/trending?since=daily`
- 从WebFetch返回的内容提取项目信息
- 项目链接格式：`https://github.com/用户名/项目名`

**对于中国AI新闻和YouTube**：
- 仅使用WebFetch能成功访问的链接
- 如果验证失败（404/403/无内容），跳过该新闻
- 中国AI新闻可退而使用综合科技媒体（如36氪、量子位）的官方网站

将搜索结果整理为四个类别，每个类别包含：
- **标题**：新闻/项目/视频标题（来自搜索结果）
- **描述**：简短摘要（1-2句话，基于搜索结果内容）
- **链接**：**必须使用搜索结果Sources中的真实URL**
- **时间**：发布时间（如果搜索结果提供）
- **来源**：媒体/博主名称（从链接域名或搜索结果中获取）
- **标签**：公司/项目标签（如OpenAI、Anthropic等）

**质量控制**：
- 每个板块至少3条新闻，最多8条
- 如果某个板块搜索结果不足，再次搜索更具体的关键词
- 确保新闻多样性（不要重复报道同一事件）

### Step 3: 整理验证后的数据

将搜索结果整理为四个类别，每个类别包含：
- **标题**：新闻标题（来自WebFetch验证的内容）
- **描述**：简短摘要（1-2句话，基于验证后的内容）
- **链接**：**经过WebFetch验证的真实URL**（域名或完整文章链接）
- **时间**：发布时间（从验证内容中获取）
- **来源**：媒体名称（从域名获取，如The Register、VICE等）

**质量控制**：
- 每个板块3-6条已验证的新闻
- 如果验证后新闻不足，扩大搜索范围
- 确保新闻多样性和时效性

### Step 4: 检查历史记录

检查是否存在历史新闻文件（在当前目录或用户指定位置）：
- 文件命名格式：`ai-news-YYYY-MM-DD.html`
- 查找最近7天的文件
- 准备历史记录导航部分

### Step 5: 生成HTML页面

使用 `assets/news_template_v2.html` 模板，替换以下占位符：

```
{{DATE}} - 当前日期（如：2026年2月6日）
{{US_COUNT}} - 美国新闻数量
{{US_NEWS}} - 美国新闻HTML片段
{{GITHUB_COUNT}} - GitHub项目数量
{{GITHUB_PROJECTS}} - GitHub项目HTML片段
{{CN_COUNT}} - 中国新闻数量
{{CN_NEWS}} - 中国新闻HTML片段
{{YOUTUBE_COUNT}} - YouTube视频数量
{{YOUTUBE_VIDEOS}} - YouTube视频HTML片段
{{HISTORY_SECTION}} - 历史记录导航HTML（如果有）
```

**新闻项HTML格式示例** - 链接必须真实：
```html
<div class="news-item">
    <h3>
        <span class="news-tag tag-openai">OpenAI</span>
        <a href="https://techcrunch.com/2026/02/06/real-article-url">新闻标题</a>
    </h3>
    <p>新闻摘要...</p>
    <div class="news-meta">
        <span>📅 2小时前</span>
        <a href="https://techcrunch.com/2026/02/06/real-article-url">来源: TechCrunch</a>
    </div>
</div>
```

**重要提醒**：
- `href` 中的URL必须是WebSearch返回的真实链接
- 不要使用 `#`、`URL`、`LINK` 等占位符
- 如果没有有效链接，整条新闻不应出现在HTML中

**GitHub项目HTML格式**：
```html
<div class="github-project">
    <h3>
        <span>📦</span>
        <a href="URL">owner/repo-name</a>
        <span class="news-tag tag-hot">🔥 Hot</span>
    </h3>
    <p>项目简介...</p>
    <div class="github-stats">
        <span>⭐ 12.5k</span>
        <span>📈 +2.3k today</span>
    </div>
</div>
```

**YouTube视频HTML格式**：
```html
<div class="youtube-video">
    <h3><a href="URL">视频标题</a></h3>
    <div class="youtube-channel">📺 频道名 · 观看次数</div>
    <div class="youtube-summary">
        核心观点：<br>
        • 要点1<br>
        • 要点2<br>
        • 要点3
    </div>
</div>
```

**历史记录HTML格式**（如果存在历史文件）：
```html
<div class="history-section">
    <div class="history-header" onclick="toggleHistory()">
        <span class="history-title">📅 历史新闻</span>
        <span class="history-toggle-icon">▶</span>
    </div>
    <div class="history-items">
        <div class="history-item" onclick="location.href='ai-news-2026-02-05.html'">2月5日</div>
        <div class="history-item" onclick="location.href='ai-news-2026-02-04.html'">2月4日</div>
    </div>
</div>
```

### Step 6: 保存并展示

将生成的HTML保存为：`ai-news-YYYY-MM-DD.html`

告知用户文件已生成，可在浏览器中打开查看。

## 新闻来源优先级

### 美国AI公司 (按重要性排序)
1. **OpenAI** - GPT系列、DALL-E、Sora等产品动态
2. **Anthropic** - Claude系列更新
3. **Google/DeepMind** - Gemini、AI研究突破
4. **Meta AI** - LLaMA、开源模型动态
5. **Microsoft** - Copilot、Azure AI服务
6. **xAI** - Grok模型动态
7. **Amazon** - Bedrock、Alexa AI功能

### 中国AI公司 (按重要性排序)
1. **字节跳动** - 豆包、云雀大模型
2. **阿里巴巴** - 通义千问系列
3. **腾讯** - 混元大模型
4. **百度** - 文心一言
5. **Moonshot AI** - Kimi智能助手
6. **智谱AI** - GLM系列模型
7. **MiniMax** - 海螺AI

## 内容筛选标准

只收录以下类型的新闻：
- ✅ 新产品/功能发布
- ✅ 重大技术突破
- ✅ 融资/收购消息
- ✅ 政策/监管动态
- ✅ 重要人事变动
- ✅ 开源项目发布

排除以下类型：
- ❌ 普通使用教程
- ❌ 旧闻重复报道
- ❌ 软文/广告内容
- ❌ 未经证实的传闻

## 输出格式要求

生成的HTML页面应包含：
1. 当日日期标题
2. 四个独立的新闻板块（可折叠）
3. 每条新闻包含：标题、摘要、来源链接、时间
4. 响应式布局，支持移动端阅读
5. 深色/浅色主题切换

## 示例输出

参考 `templates/news-template.html` 模板生成类似格式的页面。
