#!/usr/bin/env python3
"""
ProductFinderBot - Automated Product Discovery from Reddit to TikTok

This bot analyzes real user pain points from Reddit, matches them with viral 
TikTok product videos, and reports the results via Google Sheets and Telegram.
"""

import os
import sys
import time
import logging
import schedule
from datetime import datetime, timedelta
from typing import List, Dict, Any
from dotenv import load_dotenv
import json

# Import our custom modules
from reddit_scanner import RedditScanner
from tiktok_scraper import TikTokScraper
from product_finder_sheets import ProductFinderSheets
from main import GoogleSheetsToTelegram  # Import existing Telegram functionality

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('product_finder_bot.log'),
        logging.StreamHandler(sys.stdout)
    ]
)
logger = logging.getLogger(__name__)

class ProductFinderBot:
    def __init__(self):
        """Initialize the ProductFinderBot."""
        load_dotenv()
        
        # Configuration
        self.scan_interval_hours = int(os.getenv('SCAN_INTERVAL_HOURS', '6'))
        self.max_problems_per_scan = int(os.getenv('MAX_PROBLEMS_PER_SCAN', '20'))
        self.max_matches_per_problem = int(os.getenv('MAX_MATCHES_PER_PROBLEM', '3'))
        self.min_reddit_score = int(os.getenv('MIN_REDDIT_SCORE', '5'))
        self.enable_telegram = os.getenv('ENABLE_TELEGRAM', 'true').lower() == 'true'
        
        # Initialize components
        try:
            self.reddit_scanner = RedditScanner()
            logger.info("Reddit scanner initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Reddit scanner: {e}")
            self.reddit_scanner = None
        
        try:
            self.tiktok_scraper = TikTokScraper()
            logger.info("TikTok scraper initialized")
        except Exception as e:
            logger.error(f"Failed to initialize TikTok scraper: {e}")
            self.tiktok_scraper = None
        
        try:
            self.sheets_client = ProductFinderSheets()
            logger.info("Google Sheets client initialized")
        except Exception as e:
            logger.error(f"Failed to initialize Google Sheets client: {e}")
            self.sheets_client = None
        
        if self.enable_telegram:
            try:
                self.telegram_client = GoogleSheetsToTelegram()
                logger.info("Telegram client initialized")
            except Exception as e:
                logger.error(f"Failed to initialize Telegram client: {e}")
                self.telegram_client = None
        else:
            self.telegram_client = None
        
        # Statistics
        self.stats = {
            'total_scans': 0,
            'total_problems_found': 0,
            'total_matches_found': 0,
            'total_matches_added': 0,
            'last_scan_time': None,
            'errors': []
        }
        
        logger.info("ProductFinderBot initialized successfully")
    
    def scan_and_match(self) -> Dict[str, Any]:
        """Main workflow: scan Reddit, find TikTok matches, and log results."""
        scan_results = {
            'problems_found': 0,
            'matches_found': 0,
            'matches_added': 0,
            'errors': [],
            'scan_time': datetime.now().isoformat()
        }
        
        try:
            logger.info("🚀 Starting ProductFinderBot scan...")
            
            # Step 1: Scan Reddit for pain-related problems
            if not self.reddit_scanner:
                raise Exception("Reddit scanner not available")
            
            logger.info("📡 Scanning Reddit for pain-related problems...")
            problems = self.reddit_scanner.get_top_problems(limit=self.max_problems_per_scan)
            
            # Filter problems by minimum score
            problems = [p for p in problems if p.get('score', 0) >= self.min_reddit_score]
            
            scan_results['problems_found'] = len(problems)
            logger.info(f"Found {len(problems)} qualifying problems on Reddit")
            
            if not problems:
                logger.info("No problems found, ending scan")
                return scan_results
            
            # Step 2: Find TikTok product matches
            if not self.tiktok_scraper:
                raise Exception("TikTok scraper not available")
            
            logger.info("🎵 Searching TikTok for product matches...")
            all_matches = []
            
            for i, problem in enumerate(problems, 1):
                try:
                    logger.info(f"Processing problem {i}/{len(problems)}: {problem['reddit_title'][:50]}...")
                    
                    # Search for TikTok videos
                    videos = self.tiktok_scraper.search_tiktok(problem['search_query'])
                    
                    # Limit matches per problem
                    videos = videos[:self.max_matches_per_problem]
                    
                    # Create match records
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
                            'source': 'Reddit + TikTok',
                            'match_score': self.tiktok_scraper._calculate_match_score(problem, video),
                            'date': datetime.now().strftime('%Y-%m-%d'),
                            'search_query': problem['search_query']
                        }
                        all_matches.append(match)
                    
                    # Small delay between searches
                    time.sleep(2)
                    
                except Exception as e:
                    error_msg = f"Error processing problem {i}: {e}"
                    logger.error(error_msg)
                    scan_results['errors'].append(error_msg)
                    continue
            
            scan_results['matches_found'] = len(all_matches)
            logger.info(f"Found {len(all_matches)} total product matches")
            
            # Step 3: Save to Google Sheets
            if all_matches and self.sheets_client:
                logger.info("📊 Saving matches to Google Sheets...")
                
                # Add only unique matches
                added_count = self.sheets_client.add_unique_matches(all_matches)
                scan_results['matches_added'] = added_count
                
                logger.info(f"Added {added_count} unique matches to Google Sheets")
                
                # Step 4: Send Telegram notifications for new matches
                if added_count > 0 and self.telegram_client:
                    logger.info("📱 Sending Telegram notifications...")
                    try:
                        # Get recent matches for notification
                        recent_matches = all_matches[:5]  # Limit notifications
                        
                        for match in recent_matches:
                            message = self._format_telegram_message(match)
                            self.telegram_client._send_telegram_message(message)
                            time.sleep(1)  # Avoid rate limiting
                        
                        logger.info(f"Sent {len(recent_matches)} Telegram notifications")
                        
                    except Exception as e:
                        error_msg = f"Error sending Telegram notifications: {e}"
                        logger.error(error_msg)
                        scan_results['errors'].append(error_msg)
            
            elif not self.sheets_client:
                logger.warning("Google Sheets client not available, skipping save")
            
            # Update statistics
            self.stats['total_scans'] += 1
            self.stats['total_problems_found'] += scan_results['problems_found']
            self.stats['total_matches_found'] += scan_results['matches_found']
            self.stats['total_matches_added'] += scan_results['matches_added']
            self.stats['last_scan_time'] = scan_results['scan_time']
            
            logger.info(f"✅ Scan completed successfully!")
            logger.info(f"   Problems: {scan_results['problems_found']}")
            logger.info(f"   Matches: {scan_results['matches_found']}")
            logger.info(f"   Added: {scan_results['matches_added']}")
            
        except Exception as e:
            error_msg = f"Critical error in scan_and_match: {e}"
            logger.error(error_msg)
            scan_results['errors'].append(error_msg)
            self.stats['errors'].append({
                'time': datetime.now().isoformat(),
                'error': error_msg
            })
        
        return scan_results
    
    def _format_telegram_message(self, match: Dict[str, Any]) -> str:
        """Format a product match for Telegram notification."""
        message = f"""🎯 **New Product Match Found!**

📝 **Reddit Problem:** {match['reddit_title'][:100]}{'...' if len(match['reddit_title']) > 100 else ''}

🎵 **TikTok Solution:** {match['tiktok_title'][:100]}{'...' if len(match['tiktok_title']) > 100 else ''}

📂 **Category:** {match['category']}
👀 **Views:** {match['tiktok_views']:,}
⭐ **Match Score:** {match['match_score']}/1.0
📱 **Author:** {match['tiktok_author']}

🔗 **TikTok Video:** {match['tiktok_url']}
🔗 **Reddit Post:** {match['reddit_url']}

---
*Found by ProductFinderBot at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""
        
        return message
    
    def get_stats(self) -> Dict[str, Any]:
        """Get bot statistics."""
        if self.sheets_client:
            try:
                sheet_stats = self.sheets_client.get_sheet_stats()
                self.stats.update(sheet_stats)
            except Exception as e:
                logger.error(f"Failed to get sheet stats: {e}")
        
        return self.stats
    
    def run_once(self) -> Dict[str, Any]:
        """Run a single scan cycle."""
        logger.info("Running single ProductFinderBot scan...")
        return self.scan_and_match()
    
    def run_scheduled(self):
        """Run the bot on a schedule."""
        logger.info(f"Starting ProductFinderBot with {self.scan_interval_hours}h intervals...")
        
        # Schedule the scan
        schedule.every(self.scan_interval_hours).hours.do(self.scan_and_match)
        
        # Run initial scan
        logger.info("Running initial scan...")
        self.scan_and_match()
        
        # Keep running scheduled scans
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
                
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Error in scheduled run: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying
    
    def test_components(self) -> Dict[str, bool]:
        """Test all components to ensure they're working."""
        results = {}
        
        # Test Reddit scanner
        try:
            if self.reddit_scanner:
                test_problems = self.reddit_scanner.get_top_problems(limit=1)
                results['reddit'] = len(test_problems) >= 0
            else:
                results['reddit'] = False
        except Exception as e:
            logger.error(f"Reddit test failed: {e}")
            results['reddit'] = False
        
        # Test TikTok scraper
        try:
            if self.tiktok_scraper:
                test_videos = self.tiktok_scraper.search_tiktok("test")
                results['tiktok'] = len(test_videos) >= 0
            else:
                results['tiktok'] = False
        except Exception as e:
            logger.error(f"TikTok test failed: {e}")
            results['tiktok'] = False
        
        # Test Google Sheets
        try:
            if self.sheets_client:
                stats = self.sheets_client.get_sheet_stats()
                results['sheets'] = 'total_matches' in stats
            else:
                results['sheets'] = False
        except Exception as e:
            logger.error(f"Sheets test failed: {e}")
            results['sheets'] = False
        
        # Test Telegram
        try:
            if self.telegram_client:
                # Just check if client exists (don't send test message)
                results['telegram'] = True
            else:
                results['telegram'] = False
        except Exception as e:
            logger.error(f"Telegram test failed: {e}")
            results['telegram'] = False
        
        return results

def main():
    """Main function to run ProductFinderBot."""
    print("🧠 ProductFinderBot - Automated Product Discovery")
    print("=" * 50)
    
    try:
        bot = ProductFinderBot()
        
        # Test components first
        print("\n🔧 Testing components...")
        test_results = bot.test_components()
        
        for component, status in test_results.items():
            status_icon = "✅" if status else "❌"
            print(f"   {component.capitalize()}: {status_icon}")
        
        if not any(test_results.values()):
            print("\n❌ No components are working. Please check your configuration.")
            return 1
        
        # Get command line arguments
        if len(sys.argv) > 1:
            command = sys.argv[1].lower()
            
            if command == 'once':
                print("\n🚀 Running single scan...")
                results = bot.run_once()
                print(f"\nScan Results:")
                print(f"  Problems found: {results['problems_found']}")
                print(f"  Matches found: {results['matches_found']}")
                print(f"  Matches added: {results['matches_added']}")
                if results['errors']:
                    print(f"  Errors: {len(results['errors'])}")
                
            elif command == 'stats':
                print("\n📊 Bot Statistics:")
                stats = bot.get_stats()
                for key, value in stats.items():
                    if key != 'errors':
                        print(f"  {key}: {value}")
                
            elif command == 'test':
                print("\n✅ Component tests completed (see above)")
                
            else:
                print(f"\nUnknown command: {command}")
                print("Available commands: once, stats, test, or no command for scheduled run")
                return 1
        else:
            # Run scheduled
            print(f"\n⏰ Starting scheduled runs (every {bot.scan_interval_hours} hours)")
            print("Press Ctrl+C to stop...")
            bot.run_scheduled()
        
        return 0
        
    except Exception as e:
        logger.error(f"Failed to start ProductFinderBot: {e}")
        print(f"\n❌ Error: {e}")
        return 1

if __name__ == "__main__":
    exit(main())