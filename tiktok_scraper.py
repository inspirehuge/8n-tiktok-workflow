import os
import time
import logging
import requests
from typing import List, Dict, Any, Optional
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup
import json
import re
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class TikTokScraper:
    def __init__(self):
        """Initialize TikTok scraper."""
        load_dotenv()
        
        # Configuration
        self.min_views = int(os.getenv('MIN_TIKTOK_VIEWS', '10000'))  # Minimum views for viral content
        self.max_results = int(os.getenv('MAX_TIKTOK_RESULTS', '10'))  # Max results per search
        
        # Initialize Chrome driver options
        self.chrome_options = Options()
        self.chrome_options.add_argument('--headless')  # Run in background
        self.chrome_options.add_argument('--no-sandbox')
        self.chrome_options.add_argument('--disable-dev-shm-usage')
        self.chrome_options.add_argument('--disable-gpu')
        self.chrome_options.add_argument('--window-size=1920,1080')
        self.chrome_options.add_argument('--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        
        # Product-related keywords for filtering
        self.product_keywords = [
            'product', 'review', 'unboxing', 'test', 'try', 'works', 'helps',
            'relief', 'solution', 'device', 'tool', 'gadget', 'item', 'buy',
            'purchase', 'amazon', 'link', 'shop', 'store', 'brand', 'recommend',
            'cushion', 'pillow', 'support', 'brace', 'wrap', 'pad', 'mat',
            'cream', 'gel', 'oil', 'supplement', 'vitamin', 'medicine',
            'stretcher', 'roller', 'massager', 'therapy', 'treatment'
        ]
        
        logger.info("TikTokScraper initialized successfully")
    
    def _setup_driver(self) -> webdriver.Chrome:
        """Set up Chrome WebDriver."""
        try:
            service = Service(ChromeDriverManager().install())
            driver = webdriver.Chrome(service=service, options=self.chrome_options)
            return driver
        except Exception as e:
            logger.error(f"Failed to setup Chrome driver: {e}")
            raise
    
    def _extract_view_count(self, view_text: str) -> int:
        """Extract numeric view count from text."""
        if not view_text:
            return 0
        
        # Remove non-numeric characters except K, M, B
        view_text = view_text.upper().replace(',', '')
        
        # Extract number and multiplier
        match = re.search(r'(\d+\.?\d*)\s*([KMB]?)', view_text)
        if not match:
            return 0
        
        number = float(match.group(1))
        multiplier = match.group(2)
        
        if multiplier == 'K':
            return int(number * 1000)
        elif multiplier == 'M':
            return int(number * 1000000)
        elif multiplier == 'B':
            return int(number * 1000000000)
        else:
            return int(number)
    
    def _is_product_related(self, title: str, description: str) -> bool:
        """Check if video is product-related."""
        combined_text = f"{title} {description}".lower()
        
        # Check for product keywords
        for keyword in self.product_keywords:
            if keyword in combined_text:
                return True
        
        # Check for product-related patterns
        product_patterns = [
            r'\b(this|the|my)\s+\w*\s+(product|item|device|tool)',
            r'\b(buy|purchase|get|order)\s+\w*\s+(this|it|here)',
            r'\b(link\s+in\s+bio|check\s+description)',
            r'\b(amazon|shop|store|website)',
            r'\b(review|unbox|test|try)',
            r'\b(works|helps|relief|solution)'
        ]
        
        for pattern in product_patterns:
            if re.search(pattern, combined_text):
                return True
        
        return False
    
    def search_tiktok(self, query: str) -> List[Dict[str, Any]]:
        """Search TikTok for videos related to the query."""
        driver = None
        videos = []
        
        try:
            driver = self._setup_driver()
            
            # Format search query for TikTok URL
            search_query = query.replace(' ', '%20')
            url = f"https://www.tiktok.com/search?q={search_query}"
            
            logger.info(f"Searching TikTok for: {query}")
            driver.get(url)
            
            # Wait for content to load
            time.sleep(5)
            
            # Scroll to load more videos
            for _ in range(3):
                driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
                time.sleep(2)
            
            # Parse the page source
            soup = BeautifulSoup(driver.page_source, 'html.parser')
            
            # Find video elements (TikTok structure may change)
            video_elements = soup.find_all('div', {'data-e2e': 'search_top-item'}) or \
                           soup.find_all('div', class_=re.compile(r'.*video.*item.*'))
            
            if not video_elements:
                # Try alternative selectors
                video_elements = soup.find_all('a', href=re.compile(r'/video/'))[:self.max_results]
            
            for element in video_elements[:self.max_results]:
                try:
                    video_data = self._extract_video_data(element, driver.current_url)
                    if video_data and self._is_valid_video(video_data):
                        videos.append(video_data)
                except Exception as e:
                    logger.warning(f"Failed to extract video data: {e}")
                    continue
            
            logger.info(f"Found {len(videos)} relevant videos for query: {query}")
            
        except Exception as e:
            logger.error(f"Error searching TikTok for '{query}': {e}")
        
        finally:
            if driver:
                driver.quit()
        
        return videos
    
    def _extract_video_data(self, element, current_url: str) -> Optional[Dict[str, Any]]:
        """Extract video data from HTML element."""
        try:
            # Try to find video link
            link_elem = element.find('a', href=re.compile(r'/video/'))
            if not link_elem:
                link_elem = element.find('a')
            
            if not link_elem:
                return None
            
            video_url = link_elem.get('href', '')
            if video_url.startswith('/'):
                video_url = f"https://www.tiktok.com{video_url}"
            
            # Extract title/description
            title_elem = element.find('span') or element.find('div')
            title = title_elem.get_text(strip=True) if title_elem else ''
            
            # Try to find view count
            view_elem = element.find(text=re.compile(r'\d+[KMB]?\s*(view|like)'))
            views = 0
            if view_elem:
                views = self._extract_view_count(view_elem)
            
            # Extract author if available
            author_elem = element.find('span', text=re.compile(r'@\w+'))
            author = author_elem.get_text(strip=True) if author_elem else 'Unknown'
            
            return {
                'title': title[:200],  # Limit title length
                'url': video_url,
                'views': views,
                'author': author,
                'description': title,  # Use title as description for now
                'platform': 'TikTok',
                'extracted_at': time.strftime('%Y-%m-%d %H:%M:%S')
            }
            
        except Exception as e:
            logger.warning(f"Failed to extract video data: {e}")
            return None
    
    def _is_valid_video(self, video_data: Dict[str, Any]) -> bool:
        """Check if video meets criteria for viral product content."""
        # Check minimum views
        if video_data['views'] < self.min_views:
            return False
        
        # Check if product-related
        if not self._is_product_related(video_data['title'], video_data['description']):
            return False
        
        # Check if URL is valid
        if not video_data['url'] or 'tiktok.com' not in video_data['url']:
            return False
        
        return True
    
    def find_products_for_problems(self, problems: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find TikTok products for a list of Reddit problems."""
        matches = []
        
        for problem in problems:
            try:
                search_query = problem.get('search_query', '')
                if not search_query:
                    continue
                
                logger.info(f"Searching for products for: {problem['reddit_title'][:50]}...")
                
                # Search TikTok for relevant videos
                videos = self.search_tiktok(search_query)
                
                # Create matches
                for video in videos:
                    match = {
                        'reddit_title': problem['reddit_title'],
                        'reddit_url': problem['reddit_url'],
                        'reddit_category': problem['category'],
                        'reddit_subreddit': problem['subreddit'],
                        'reddit_score': problem['score'],
                        'tiktok_title': video['title'],
                        'tiktok_url': video['url'],
                        'tiktok_views': video['views'],
                        'tiktok_author': video['author'],
                        'description': video['description'],
                        'category': problem['category'],
                        'source': f"Reddit + TikTok",
                        'match_score': self._calculate_match_score(problem, video),
                        'date': time.strftime('%Y-%m-%d'),
                        'search_query': search_query
                    }
                    matches.append(match)
                
                # Add delay between searches to avoid rate limiting
                time.sleep(3)
                
            except Exception as e:
                logger.error(f"Failed to find products for problem: {e}")
                continue
        
        # Sort by match score and views
        matches.sort(key=lambda x: (x['match_score'], x['tiktok_views']), reverse=True)
        
        logger.info(f"Found {len(matches)} product matches")
        return matches
    
    def _calculate_match_score(self, problem: Dict[str, Any], video: Dict[str, Any]) -> float:
        """Calculate relevance score between Reddit problem and TikTok video."""
        score = 0.0
        
        # Base score from Reddit popularity
        score += min(problem['score'] / 100, 1.0) * 0.3
        
        # Base score from TikTok views
        score += min(video['views'] / 100000, 1.0) * 0.3
        
        # Category match bonus
        problem_text = f"{problem['reddit_title']} {problem.get('reddit_content', '')}".lower()
        video_text = f"{video['title']} {video['description']}".lower()
        
        # Keyword overlap
        problem_words = set(problem_text.split())
        video_words = set(video_text.split())
        overlap = len(problem_words.intersection(video_words))
        score += min(overlap / 10, 1.0) * 0.4
        
        return round(score, 2)

# Alternative API-based approach (for when scraping becomes difficult)
class TikTokAPIClient:
    """Alternative TikTok client using unofficial APIs or proxies."""
    
    def __init__(self):
        load_dotenv()
        self.api_key = os.getenv('TIKTOK_API_KEY')  # If using a service like RapidAPI
        
    def search_videos(self, query: str, count: int = 10) -> List[Dict[str, Any]]:
        """Search TikTok videos using API (placeholder for future implementation)."""
        # This would be implemented with services like:
        # - RapidAPI TikTok APIs
        # - Apify TikTok scrapers
        # - Custom proxy solutions
        
        logger.info(f"API search not implemented yet for query: {query}")
        return []

if __name__ == "__main__":
    # Test the TikTok scraper
    try:
        scraper = TikTokScraper()
        
        # Test search
        test_query = "back pain relief"
        videos = scraper.search_tiktok(test_query)
        
        print(f"\nFound {len(videos)} videos for '{test_query}':")
        for i, video in enumerate(videos, 1):
            print(f"\n{i}. {video['title']}")
            print(f"   Views: {video['views']:,}")
            print(f"   Author: {video['author']}")
            print(f"   URL: {video['url']}")
            
    except Exception as e:
        logger.error(f"Test failed: {e}")