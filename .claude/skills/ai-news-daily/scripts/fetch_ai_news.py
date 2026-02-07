#!/usr/bin/env python3
"""
AI新闻RSS抓取脚本
从预定义的RSS源抓取AI相关新闻
"""

import feedparser
import json
from datetime import datetime, timedelta
from typing import List, Dict
import re
import urllib.request

# RSS新闻源配置
RSS_SOURCES = {
    "us_companies": [
        "https://openai.com/blog/rss.xml",
        "https://www.anthropic.com/news/rss",
        "https://blog.google/technology/ai/rss/",
        "https://ai.meta.com/blog/rss/",
    ],
    "tech_news": [
        "https://techcrunch.com/tag/artificial-intelligence/feed/",
        "https://www.theverge.com/ai-artificial-intelligence/rss/index.xml",
        "https://venturebeat.com/category/ai/feed/",
    ],
    "china_ai": [
        "https://www.36kr.com/feed",
        "https://www.jiqizhixin.com/rss",
    ],
}

# YouTube Channels
YOUTUBE_CHANNELS = [
    {"name": "OpenAI", "url": "https://www.youtube.com/OpenAI/videos"},
    {"name": "Anthropic", "url": "https://www.youtube.com/@anthropic-ai/videos"},
    {"name": "Google DeepMind", "url": "https://www.youtube.com/@googledeepmind/videos"},
    {"name": "Runway", "url": "https://www.youtube.com/@Runwayml/videos"},
    {"name": "Meta AI", "url": "https://www.youtube.com/@AIatMeta/videos"},
    {"name": "Lex Fridman", "url": "https://www.youtube.com/@lexfridman/videos"},
    {"name": "Lenny's Podcast", "url": "https://www.youtube.com/@LennysPodcast/videos"},
    {"name": "Peter Yang", "url": "https://www.youtube.com/@peteryangyt/videos"},
    {"name": "Dwarkesh Podcast", "url": "https://www.youtube.com/@DwarkeshPatel/videos"},
    {"name": "Unsupervised Learning", "url": "https://www.youtube.com/channel/UCUl-s_Vp-Kkk_XVyDylNwLA/videos"},
    {"name": "Training Data", "url": "https://www.youtube.com/playlist?list=PLOhHNjZItNnMm5tdW61JpnyxeYH5NDDx8"},
    {"name": "Latent Space", "url": "https://www.youtube.com/@LatentSpacePod/videos"},
    {"name": "No Priors", "url": "https://www.youtube.com/@NoPriorsPodcast/videos"},
    {"name": "Andrej Karpathy", "url": "https://www.youtube.com/@AndrejKarpathy/videos"},
    {"name": "Jeff Su", "url": "https://www.youtube.com/@JeffSu/videos"},
    {"name": "Tina Huang", "url": "https://www.youtube.com/@TinaHuang1/videos"},
    {"name": "Theoretically Media", "url": "https://www.youtube.com/@TheoreticallyMedia/videos"},
    {"name": "Matt Wolfe", "url": "https://www.youtube.com/@mreflow/videos"},
    {"name": "Matthew Berman", "url": "https://www.youtube.com/@matthewberman/videos"},
    {"name": "Curious Refuge", "url": "https://www.youtube.com/@CuriousRefuge/videos"},
    {"name": "Olivio Sarikas", "url": "https://www.youtube.com/@OlivioSarikas/videos"},
    {"name": "Riley Brown", "url": "https://www.youtube.com/@RileyBrownAI/videos"},
    {"name": "Greg Isenberg", "url": "https://www.youtube.com/@GregIsenberg/videos"},
]

# GitHub trending - 需要通过API获取
GITHUB_API = "https://api.github.com/search/repositories"

# AI关键词过滤
AI_KEYWORDS = [
    "ai", "artificial intelligence", "machine learning", "deep learning",
    "neural network", "gpt", "llm", "large language model", "chatgpt",
    "openai", "anthropic", "claude", "gemini", "meta ai", "llama",
    "通义", "文心", "混元", "豆包", "kimi", "智谱", "大模型"
]


def is_ai_related(title: str, description: str = "") -> bool:
    """判断新闻是否与AI相关"""
    text = (title + " " + description).lower()
    return any(keyword in text for keyword in AI_KEYWORDS)


def fetch_rss_feed(url: str, max_items: int = 10) -> List[Dict]:
    """抓取单个RSS源"""
    try:
        feed = feedparser.parse(url)
        items = []

        for entry in feed.entries[:max_items]:
            # 获取发布时间
            published = entry.get('published_parsed') or entry.get('updated_parsed')
            if published:
                pub_date = datetime(*published[:6])
                # 只获取最近24小时的新闻
                if datetime.now() - pub_date > timedelta(days=1):
                    continue
            else:
                pub_date = None # 无法确定时间则保留，后续可能过滤

            title = entry.get('title', '')
            description = entry.get('summary', '') or entry.get('description', '')

            # 过滤AI相关内容
            if not is_ai_related(title, description):
                continue

            items.append({
                'title': title,
                'link': entry.get('link', ''),
                'description': clean_html(description[:200]),
                'published': pub_date.strftime('%Y-%m-%d %H:%M') if pub_date else '未知时间',
                'source': feed.feed.get('title', url),
            })

        return items
    except Exception as e:
        print(f"抓取RSS失败 {url}: {e}")
        return []


def clean_html(text: str) -> str:
    """清理HTML标签"""
    text = re.sub(r'<[^>]+>', '', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()


def fetch_youtube_latest(channels: List[Dict]) -> List[Dict]:
    """从YouTube频道抓取最新视频"""
    videos = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    }

    print("开始抓取YouTube频道...")
    for channel in channels:
        try:
            url = channel['url']
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=10) as response:
                html = response.read().decode('utf-8')
                
                # 提取视频ID和标题
                # 这种方法依赖于YouTube页面结构，可能会失效
                video_ids = re.findall(r'"videoId":"([^"]+)"', html)
                # 尝试更精确地匹配标题，避免匹配到其他推荐视频
                # 在列表页，通常是 title -> runs -> text
                titles = re.findall(r'"title":\{"runs":\[\{"text":"([^"]+)"\}\]', html)
                
                # 简单的去重和对齐
                if video_ids and titles:
                    # 获取第一个视频（通常是最新置顶或最新的）
                    # 注意：YouTube页面源码中的顺序不一定完全对应视觉顺序，但第一个videoId通常是主视频
                    
                    # 过滤掉可能的无效ID或广告
                    valid_videos = []
                    for vid, title in zip(video_ids, titles):
                        if len(vid) == 11: # YouTube video ID length
                            valid_videos.append((vid, title))
                    
                    if valid_videos:
                        vid_id, title = valid_videos[0]
                        # 对于播放列表，结构可能不同，但videoId总是存在的
                        
                        videos.append({
                            'title': title,
                            'link': f"https://www.youtube.com/watch?v={vid_id}",
                            'description': f"来自 {channel['name']} 的最新视频",
                            'published': 'Latest',
                            'source': channel['name']
                        })
                        print(f"  - {channel['name']}: {title}")
                else:
                    print(f"  - {channel['name']}: 未找到视频")

        except Exception as e:
            print(f"  - {channel['name']} 抓取失败: {e}")
            
    return videos


def categorize_news(items: List[Dict]) -> Dict[str, List[Dict]]:
    """将新闻分类"""
    categorized = {
        'us_companies': [],
        'china_companies': [],
        'general': [],
    }

    us_companies = ['openai', 'anthropic', 'google', 'meta', 'microsoft', 'amazon']
    china_companies = ['阿里', '腾讯', '字节', '百度', 'kimi', '智谱', 'alibaba', 'tencent', 'baidu']

    for item in items:
        text = (item['title'] + ' ' + item['description']).lower()

        if any(company in text for company in us_companies):
            categorized['us_companies'].append(item)
        elif any(company in text for company in china_companies):
            categorized['china_companies'].append(item)
        else:
            categorized['general'].append(item)

    return categorized


def fetch_all_news() -> Dict:
    """抓取所有新闻源"""
    all_news = {
        'us_companies': [],
        'china_companies': [],
        'general': [],
        'youtube': [], # 新增YouTube分类
        'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
    }

    # 抓取美国公司新闻
    for url in RSS_SOURCES['us_companies']:
        items = fetch_rss_feed(url)
        all_news['us_companies'].extend(items)

    # 抓取中国AI新闻
    for url in RSS_SOURCES['china_ai']:
        items = fetch_rss_feed(url)
        all_news['china_companies'].extend(items)

    # 抓取通用科技新闻并分类
    for url in RSS_SOURCES['tech_news']:
        items = fetch_rss_feed(url)
        categorized = categorize_news(items)
        all_news['us_companies'].extend(categorized['us_companies'])
        all_news['china_companies'].extend(categorized['china_companies'])
        all_news['general'].extend(categorized['general'])
        
    # 抓取YouTube新闻
    youtube_videos = fetch_youtube_latest(YOUTUBE_CHANNELS)
    all_news['youtube'].extend(youtube_videos)

    # 去重
    for category in ['us_companies', 'china_companies', 'general', 'youtube']:
        seen = set()
        unique_items = []
        for item in all_news[category]:
            if item['link'] not in seen:
                seen.add(item['link'])
                unique_items.append(item)
        all_news[category] = unique_items[:15]  # 每个类别最多15条

    return all_news


if __name__ == '__main__':
    news = fetch_all_news()
    print(json.dumps(news, ensure_ascii=False, indent=2))
