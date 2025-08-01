"""Configuration settings for the TikTok Viral Bot"""

# Telegram Bot Configuration
TELEGRAM_BOT_TOKEN = "8358172003:AAGSxIY9ejRF8o_nG-mhIY6ZXany7hq9XqM"
TELEGRAM_CHAT_ID = "-1002197208879"

# Reddit Configuration
REDDIT_SUBREDDITS = [
    "shutupandtakemymoney",
    "BuyItForLife"
]

# TikTok Search Configuration
TIKTOK_SEARCH_URL = "https://www.tiktok.com/search?q={keyword}"

# Filtering Criteria
MIN_VIEWS = 10000
MAX_VIDEO_AGE_HOURS = 48
MAX_POSTS_PER_SUBREDDIT = 10

# File Paths
SENT_VIDEOS_FILE = "sent_videos.txt"
LOG_FILE = "bot.log"

# Scheduling
RUN_INTERVAL_MINUTES = 15

# User Agents for web scraping
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
]