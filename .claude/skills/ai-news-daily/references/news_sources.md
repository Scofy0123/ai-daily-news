# AI新闻源配置

## RSS新闻源列表

### 美国AI公司官方博客

- **OpenAI**: https://openai.com/blog/rss.xml
- **Anthropic**: https://www.anthropic.com/news/rss
- **Google AI Blog**: https://blog.google/technology/ai/rss/
- **Meta AI**: https://ai.meta.com/blog/rss/

### 科技媒体AI频道

- **TechCrunch AI**: https://techcrunch.com/tag/artificial-intelligence/feed/
- **The Verge AI**: https://www.theverge.com/ai-artificial-intelligence/rss/index.xml
- **VentureBeat AI**: https://venturebeat.com/category/ai/feed/

### 中国AI资讯

- **36氪**: https://www.36kr.com/feed
- **机器之心**: https://www.jiqizhixin.com/rss

## GitHub热门项目

使用GitHub Trending页面或API：
- Trending页面: https://github.com/trending?since=daily&spoken_language_code=en
- 筛选AI/ML相关标签

## YouTube AI频道

### 英文频道
- **AI Explained** (@ai-explained-) - AI技术深度分析
- **Two Minute Papers** (@TwoMinutePapers) - 论文快速解读
- **Matt Wolfe** (@mreflow) - AI工具和新闻
- **Fireship** (@Fireship) - 技术趋势快讯
- **TheAIGRID** (@TheAIGRID) - AI新闻聚合

### 中文频道
- **李沐** - AI论文解读
- **跟李沐学AI** - 深度学习课程
- **AI悦创** - AI工具教程

## 新闻筛选标准

### 优先收录
1. 新产品/功能发布
2. 重大技术突破
3. 融资/收购消息
4. 开源项目发布
5. 政策监管动态

### 排除内容
1. 普通教程文章
2. 重复旧闻
3. 软文广告
4. 未证实传闻

## 自定义RSS源

如需添加新的RSS源，在 `scripts/fetch_ai_news.py` 的 `RSS_SOURCES` 字典中添加URL。
