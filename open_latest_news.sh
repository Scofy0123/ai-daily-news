#!/bin/bash

# 1. 切换到项目根目录（假设脚本放在项目根目录）
cd "$(dirname "$0")"

echo "正在同步最新日报数据..."
# 2. 从 GitHub 拉取最新生成的 HTML 文件
git pull origin main

# 3. 寻找日期最新的 HTML 文件 (格式: ai-news-YYYY-MM-DD.html)
# 使用 ls 排序并取最后一个
LATEST_FILE=$(ls ai-news-*.html 2>/dev/null | sort -r | head -n 1)

if [ -n "$LATEST_FILE" ]; then
    echo "正在打开最新日报: $LATEST_FILE"
    # 4. 在默认浏览器中打开
    open "$LATEST_FILE"
else
    echo "未找到任何日报文件。请确认脚本已在项目根目录运行，或 GitHub Actions 已生成文件。"
fi
