#!/usr/bin/env python3
"""
TikTok Viral Product Scanner
Scans TikTok hourly for new viral product videos using popular hashtags and sends them to a Telegram channel.
TikTok'ta ürünle ilgili popüler etiketleri saatlik olarak tarar, yeni viral olmaya başlayan videoları tespit eder ve Telegram'a gönderir.
"""

import requests
import json
import time
import logging
from datetime import datetime, timedelta
from typing import List, Dict, Optional
import os
from dataclasses import dataclass

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('tiktok_scanner.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

@dataclass
class VideoData:
    """Data class for TikTok video information"""
    video_id: str
    author: str
    description: str
    views: int
    create_time: datetime
    url: str

class TikTokScanner:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the TikTok scanner with configuration"""
        self.config = self.load_config(config_file)
        self.telegram_bot_token = self.config.get("telegram_bot_token")
        self.telegram_chat_id = self.config.get("telegram_chat_id")
        self.hashtags = self.config.get("hashtags", [])
        self.min_views = self.config.get("min_views", 10000)
        self.max_age_hours = self.config.get("max_age_hours", 1)
        self.processed_videos = set()
        
        # Validate configuration
        if not self.telegram_bot_token or not self.telegram_chat_id:
            raise ValueError("Telegram bot token and chat ID must be configured")
    
    def load_config(self, config_file: str) -> Dict:
        """Load configuration from JSON file"""
        try:
            with open(config_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except FileNotFoundError:
            logger.warning(f"Config file {config_file} not found, using environment variables")
            return {
                "telegram_bot_token": os.getenv("TELEGRAM_BOT_TOKEN"),
                "telegram_chat_id": os.getenv("TELEGRAM_CHAT_ID"),
                "hashtags": [
                    "tiktokmademebuyit", "amazonfinds", "viralproducts",
                    "musthaveproducts", "trendingproducts", "gadgettok",
                    "buyitnow", "problemSolved", "usefulgadgets",
                    "aliexpressfinds", "usefulproducts", "amazongems"
                ],
                "min_views": 10000,
                "max_age_hours": 1
            }
    
    def get_tiktok_data(self, hashtag: str) -> List[Dict]:
        """Fetch TikTok data for a specific hashtag"""
        try:
            # Multiple API endpoints to try (TikTok often changes these)
            urls = [
                f"https://www.tiktok.com/api/challenge/item_list/?challengeName={hashtag}&count=20&cursor=0",
                f"https://m.tiktok.com/api/challenge/item_list/?challengeName={hashtag}&count=20&cursor=0",
                f"https://t.tiktok.com/api/challenge/item_list/?challenge_name={hashtag}&count=20&cursor=0"
            ]
            
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
                "Accept": "application/json, text/plain, */*",
                "Accept-Language": "en-US,en;q=0.9",
                "Referer": "https://www.tiktok.com/",
                "Origin": "https://www.tiktok.com"
            }
            
            for url in urls:
                try:
                    logger.info(f"Trying to fetch data from: {url}")
                    response = requests.get(url, headers=headers, timeout=10)
                    
                    if response.status_code == 200:
                        data = response.json()
                        items = data.get("itemList", []) or data.get("items", [])
                        if items:
                            logger.info(f"Successfully fetched {len(items)} videos for #{hashtag}")
                            return items
                    
                    time.sleep(1)  # Rate limiting
                except requests.exceptions.RequestException as e:
                    logger.warning(f"Request failed for {url}: {e}")
                    continue
            
            logger.warning(f"All API endpoints failed for hashtag: {hashtag}")
            return []
            
        except Exception as e:
            logger.error(f"Error fetching TikTok data for #{hashtag}: {e}")
            return []
    
    def parse_video_data(self, video: Dict) -> Optional[VideoData]:
        """Parse video data from TikTok API response"""
        try:
            stats = video.get("stats", {})
            desc = video.get("desc", "No Description")[:200]  # Limit description length
            views = stats.get("playCount", 0) or stats.get("play_count", 0)
            create_time = video.get("createTime", 0) or video.get("create_time", 0)
            
            if create_time:
                create_dt = datetime.fromtimestamp(create_time)
            else:
                create_dt = datetime.now()
            
            video_id = video.get("id", "") or video.get("video_id", "")
            author_info = video.get("author", {})
            author = author_info.get("uniqueId", "") or author_info.get("unique_id", "")
            
            if not video_id or not author:
                return None
            
            url = f"https://www.tiktok.com/@{author}/video/{video_id}"
            
            return VideoData(
                video_id=video_id,
                author=author,
                description=desc,
                views=views,
                create_time=create_dt,
                url=url
            )
        
        except Exception as e:
            logger.error(f"Error parsing video data: {e}")
            return None
    
    def is_viral_candidate(self, video_data: VideoData) -> bool:
        """Check if video meets viral criteria"""
        # Check if video is recent enough
        age = datetime.now() - video_data.create_time
        if age > timedelta(hours=self.max_age_hours):
            return False
        
        # Check if video has enough views
        if video_data.views < self.min_views:
            return False
        
        # Check if we've already processed this video
        if video_data.video_id in self.processed_videos:
            return False
        
        return True
    
    def send_telegram_message(self, text: str) -> bool:
        """Send message to Telegram channel"""
        try:
            telegram_url = f"https://api.telegram.org/bot{self.telegram_bot_token}/sendMessage"
            payload = {
                "chat_id": self.telegram_chat_id,
                "text": text,
                "parse_mode": "Markdown",
                "disable_web_page_preview": False
            }
            
            response = requests.post(telegram_url, data=payload, timeout=10)
            
            if response.status_code == 200:
                logger.info("Message sent to Telegram successfully")
                return True
            else:
                logger.error(f"Failed to send Telegram message: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending Telegram message: {e}")
            return False
    
    def format_video_message(self, video_data: VideoData, hashtag: str) -> str:
        """Format video data into Telegram message"""
        views_formatted = f"{video_data.views:,}"
        time_formatted = video_data.create_time.strftime('%Y-%m-%d %H:%M')
        
        message = f"""🔥 *New Viral Product Video!*

📱 *Description:* {video_data.description}
👤 *Creator:* @{video_data.author}
👁️ *Views:* {views_formatted}
🏷️ *Hashtag:* #{hashtag}
🕒 *Posted:* {time_formatted}

🔗 [Watch Video]({video_data.url})

#ViralProducts #TikTokFinds"""
        
        return message
    
    def scan_hashtag(self, hashtag: str) -> int:
        """Scan a specific hashtag for viral videos"""
        logger.info(f"Scanning hashtag: #{hashtag}")
        videos_found = 0
        
        videos = self.get_tiktok_data(hashtag)
        
        for video in videos:
            video_data = self.parse_video_data(video)
            
            if video_data and self.is_viral_candidate(video_data):
                message = self.format_video_message(video_data, hashtag)
                
                if self.send_telegram_message(message):
                    self.processed_videos.add(video_data.video_id)
                    videos_found += 1
                    logger.info(f"Sent viral video: {video_data.video_id} by @{video_data.author}")
                
                # Rate limiting
                time.sleep(2)
        
        return videos_found
    
    def run_scan(self) -> None:
        """Run a complete scan of all hashtags"""
        start_time = datetime.now()
        logger.info("Starting TikTok viral product scan")
        
        total_videos = 0
        
        for hashtag in self.hashtags:
            try:
                videos_found = self.scan_hashtag(hashtag)
                total_videos += videos_found
                
                # Rate limiting between hashtags
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"Error scanning hashtag #{hashtag}: {e}")
                continue
        
        duration = datetime.now() - start_time
        logger.info(f"Scan completed in {duration.total_seconds():.1f}s. Found {total_videos} viral videos.")
        
        # Clean up old processed videos (keep only last 1000)
        if len(self.processed_videos) > 1000:
            self.processed_videos = set(list(self.processed_videos)[-500:])

def main():
    """Main function"""
    try:
        scanner = TikTokScanner()
        scanner.run_scan()
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        raise

if __name__ == "__main__":
    main()