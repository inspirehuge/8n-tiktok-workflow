#!/usr/bin/env python3
"""
TikTok Viral Bot - Automated Reddit to TikTok to Telegram Pipeline
Scrapes Reddit for product keywords, searches TikTok for viral videos, and sends to Telegram
"""

import requests
import json
import re
import time
import logging
import os
import random
from datetime import datetime, timedelta
from typing import List, Dict, Set, Optional
from urllib.parse import quote_plus
import asyncio
import threading
import schedule

from bs4 import BeautifulSoup
from playwright.async_api import async_playwright
import config

# Setup logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler(config.LOG_FILE),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)


class TikTokViralBot:
    def __init__(self):
        self.sent_videos = self.load_sent_videos()
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': random.choice(config.USER_AGENTS)
        })
        
    def load_sent_videos(self) -> Set[str]:
        """Load previously sent video URLs from file"""
        try:
            if os.path.exists(config.SENT_VIDEOS_FILE):
                with open(config.SENT_VIDEOS_FILE, 'r', encoding='utf-8') as f:
                    return set(line.strip() for line in f if line.strip())
            return set()
        except Exception as e:
            logger.error(f"Error loading sent videos: {e}")
            return set()
    
    def save_sent_video(self, video_url: str):
        """Save a video URL to prevent future duplicates"""
        try:
            with open(config.SENT_VIDEOS_FILE, 'a', encoding='utf-8') as f:
                f.write(f"{video_url}\n")
            self.sent_videos.add(video_url)
        except Exception as e:
            logger.error(f"Error saving sent video: {e}")
    
    def extract_keywords_from_title(self, title: str) -> List[str]:
        """Extract product-related keywords from Reddit post titles"""
        # Remove common Reddit formatting and noise words
        title = re.sub(r'\[.*?\]', '', title)  # Remove bracketed text
        title = re.sub(r'\(.*?\)', '', title)  # Remove parenthetical text
        
        # Split into words and filter
        words = re.findall(r'\b[a-zA-Z]{3,}\b', title.lower())
        
        # Filter out common stop words and Reddit-specific terms
        stop_words = {
            'the', 'and', 'for', 'are', 'but', 'not', 'you', 'all', 'can', 'had', 
            'her', 'was', 'one', 'our', 'out', 'day', 'get', 'has', 'him', 'his', 
            'how', 'its', 'new', 'now', 'old', 'see', 'two', 'who', 'boy', 'did',
            'reddit', 'post', 'this', 'that', 'with', 'have', 'from', 'they', 'know',
            'want', 'been', 'good', 'much', 'some', 'time', 'very', 'when', 'come',
            'here', 'just', 'like', 'long', 'make', 'many', 'over', 'such', 'take',
            'than', 'them', 'well', 'were', 'will', 'would', 'your', 'about', 'could',
            'there', 'other', 'after', 'first', 'never', 'these', 'think', 'where',
            'being', 'every', 'great', 'might', 'shall', 'still', 'those', 'under',
            'while', 'along', 'found', 'house', 'large', 'right', 'small', 'sound',
            'still', 'again', 'place', 'three', 'years', 'before', 'little', 'should',
            'world', 'going', 'number', 'people', 'called', 'during', 'really', 'though'
        }
        
        # Keep only meaningful keywords
        keywords = [word for word in words if word not in stop_words and len(word) > 3]
        
        # Return top 5 most relevant keywords
        return keywords[:5]
    
    def scrape_reddit_posts(self, subreddit: str) -> List[Dict]:
        """Scrape latest posts from a Reddit subreddit"""
        try:
            url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={config.MAX_POSTS_PER_SUBREDDIT}"
            
            response = self.session.get(url)
            response.raise_for_status()
            
            data = response.json()
            posts = []
            
            for post in data['data']['children']:
                post_data = post['data']
                title = post_data.get('title', '')
                
                if title:
                    keywords = self.extract_keywords_from_title(title)
                    if keywords:
                        posts.append({
                            'title': title,
                            'keywords': keywords,
                            'url': f"https://reddit.com{post_data.get('permalink', '')}",
                            'score': post_data.get('score', 0)
                        })
            
            logger.info(f"Scraped {len(posts)} posts from r/{subreddit}")
            return posts
            
        except Exception as e:
            logger.error(f"Error scraping r/{subreddit}: {e}")
            return []
    
    async def search_tiktok_videos(self, keyword: str) -> List[Dict]:
        """Search TikTok for videos using Playwright"""
        try:
            async with async_playwright() as p:
                browser = await p.chromium.launch(headless=True)
                context = await browser.new_context(
                    user_agent=random.choice(config.USER_AGENTS)
                )
                page = await context.new_page()
                
                search_url = config.TIKTOK_SEARCH_URL.format(keyword=quote_plus(keyword))
                logger.info(f"Searching TikTok for: {keyword}")
                
                await page.goto(search_url, wait_until='networkidle')
                await page.wait_for_timeout(3000)  # Wait for content to load
                
                videos = []
                
                # Extract video information from the page
                video_elements = await page.query_selector_all('[data-e2e="search-card-video"]')
                
                for element in video_elements[:10]:  # Limit to top 10 results
                    try:
                        # Extract video URL
                        link_element = await element.query_selector('a')
                        if not link_element:
                            continue
                            
                        video_url = await link_element.get_attribute('href')
                        if not video_url:
                            continue
                            
                        if not video_url.startswith('http'):
                            video_url = f"https://www.tiktok.com{video_url}"
                        
                        # Skip if already sent
                        if video_url in self.sent_videos:
                            continue
                        
                        # Extract title/description
                        title_element = await element.query_selector('[data-e2e="search-card-desc"]')
                        title = await title_element.inner_text() if title_element else "No title"
                        
                        # Extract author
                        author_element = await element.query_selector('[data-e2e="search-card-user-unique-id"]')
                        author = await author_element.inner_text() if author_element else "Unknown"
                        
                        # Extract view count (this might need adjustment based on TikTok's current structure)
                        views_element = await element.query_selector('[data-e2e="video-views"]')
                        views_text = await views_element.inner_text() if views_element else "0"
                        views = self.parse_view_count(views_text)
                        
                        # For now, we'll assume all videos are recent since TikTok doesn't always show exact timestamps
                        # In a production environment, you might want to implement more sophisticated date parsing
                        
                        video_info = {
                            'title': title.strip(),
                            'url': video_url,
                            'views': views,
                            'author': author.strip(),
                            'keyword': keyword,
                            'upload_time': datetime.now()  # Placeholder - would need more sophisticated parsing
                        }
                        
                        videos.append(video_info)
                        
                    except Exception as e:
                        logger.warning(f"Error extracting video info: {e}")
                        continue
                
                await browser.close()
                logger.info(f"Found {len(videos)} videos for keyword: {keyword}")
                return videos
                
        except Exception as e:
            logger.error(f"Error searching TikTok for {keyword}: {e}")
            return []
    
    def parse_view_count(self, views_text: str) -> int:
        """Parse view count from TikTok text (e.g., '1.2M' -> 1200000)"""
        try:
            views_text = views_text.lower().replace(',', '').strip()
            
            if 'k' in views_text:
                return int(float(views_text.replace('k', '')) * 1000)
            elif 'm' in views_text:
                return int(float(views_text.replace('m', '')) * 1000000)
            elif 'b' in views_text:
                return int(float(views_text.replace('b', '')) * 1000000000)
            else:
                return int(re.sub(r'[^\d]', '', views_text) or 0)
        except:
            return 0
    
    def filter_videos(self, videos: List[Dict]) -> List[Dict]:
        """Filter videos based on criteria"""
        filtered = []
        current_time = datetime.now()
        
        for video in videos:
            # Check view count
            if video['views'] < config.MIN_VIEWS:
                continue
            
            # Check if already sent
            if video['url'] in self.sent_videos:
                continue
            
            # For now, we'll assume all videos are recent since we're getting them from search
            # In production, you'd want more sophisticated date filtering
            
            filtered.append(video)
        
        logger.info(f"Filtered to {len(filtered)} videos meeting criteria")
        return filtered
    
    def send_telegram_message(self, video: Dict) -> bool:
        """Send a formatted message to Telegram"""
        try:
            message = f"""🔥 *New Viral Product Video*
🎬 {video['title']}
👁️ {video['views']:,} views
👤 @{video['author']}
🔗 [Watch on TikTok]({video['url']})"""

            data = {
                'chat_id': config.TELEGRAM_CHAT_ID,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': False
            }
            
            url = f"https://api.telegram.org/bot{config.TELEGRAM_BOT_TOKEN}/sendMessage"
            response = requests.post(url, json=data)
            response.raise_for_status()
            
            logger.info(f"Sent video to Telegram: {video['title'][:50]}...")
            return True
            
        except Exception as e:
            logger.error(f"Error sending to Telegram: {e}")
            return False
    
    async def process_keywords(self, keywords: List[str]) -> List[Dict]:
        """Process a list of keywords and return filtered videos"""
        all_videos = []
        
        for keyword in keywords:
            try:
                videos = await self.search_tiktok_videos(keyword)
                all_videos.extend(videos)
                
                # Add small delay between searches to be respectful
                await asyncio.sleep(2)
                
            except Exception as e:
                logger.error(f"Error processing keyword {keyword}: {e}")
                continue
        
        # Remove duplicates based on URL
        unique_videos = {}
        for video in all_videos:
            if video['url'] not in unique_videos:
                unique_videos[video['url']] = video
        
        return list(unique_videos.values())
    
    async def run_bot_cycle(self):
        """Run one complete cycle of the bot"""
        logger.info("Starting bot cycle...")
        
        try:
            # Step 1: Scrape Reddit posts
            all_keywords = []
            for subreddit in config.REDDIT_SUBREDDITS:
                posts = self.scrape_reddit_posts(subreddit)
                for post in posts:
                    all_keywords.extend(post['keywords'])
            
            # Remove duplicates and limit keywords
            unique_keywords = list(set(all_keywords))[:20]  # Limit to 20 keywords per cycle
            logger.info(f"Processing {len(unique_keywords)} unique keywords")
            
            if not unique_keywords:
                logger.warning("No keywords found from Reddit posts")
                return
            
            # Step 2: Search TikTok for videos
            videos = await self.process_keywords(unique_keywords)
            
            # Step 3: Filter videos
            filtered_videos = self.filter_videos(videos)
            
            if not filtered_videos:
                logger.info("No videos meeting criteria found")
                return
            
            # Step 4: Send to Telegram and track sent videos
            sent_count = 0
            for video in filtered_videos[:5]:  # Limit to 5 videos per cycle
                if self.send_telegram_message(video):
                    self.save_sent_video(video['url'])
                    sent_count += 1
                    
                    # Add delay between messages to avoid rate limiting
                    time.sleep(1)
            
            logger.info(f"Bot cycle completed. Sent {sent_count} videos to Telegram.")
            
        except Exception as e:
            logger.error(f"Error in bot cycle: {e}")
    
    def run_once(self):
        """Run the bot once (for manual trigger)"""
        asyncio.run(self.run_bot_cycle())
    
    def start_scheduler(self):
        """Start the scheduled execution"""
        logger.info(f"Starting scheduler - will run every {config.RUN_INTERVAL_MINUTES} minutes")
        
        # Schedule the job
        schedule.every(config.RUN_INTERVAL_MINUTES).minutes.do(self.run_once)
        
        # Run once immediately
        self.run_once()
        
        # Keep the scheduler running
        while True:
            schedule.run_pending()
            time.sleep(60)  # Check every minute


def main():
    """Main function to run the bot"""
    bot = TikTokViralBot()
    
    # Check if this is a manual run or scheduled run
    import sys
    if len(sys.argv) > 1 and sys.argv[1] == "--manual":
        logger.info("Running manual trigger...")
        bot.run_once()
    else:
        logger.info("Starting persistent bot with scheduler...")
        bot.start_scheduler()


if __name__ == "__main__":
    main()