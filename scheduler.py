#!/usr/bin/env python3
"""
TikTok Scanner Scheduler
Runs the TikTok viral product scanner at regular intervals.
"""

import schedule
import time
import logging
from datetime import datetime
from tiktok_scanner import TikTokScanner
import json

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('scheduler.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class TikTokScheduler:
    def __init__(self, config_file: str = "config.json"):
        """Initialize the scheduler"""
        self.config_file = config_file
        self.load_config()
        
    def load_config(self):
        """Load configuration from JSON file"""
        try:
            with open(self.config_file, 'r', encoding='utf-8') as f:
                config = json.load(f)
                self.scan_interval = config.get("scan_interval_minutes", 60)
        except FileNotFoundError:
            logger.warning(f"Config file {self.config_file} not found, using default interval")
            self.scan_interval = 60
    
    def run_scanner(self):
        """Run the TikTok scanner"""
        try:
            logger.info("Starting scheduled TikTok scan")
            scanner = TikTokScanner(self.config_file)
            scanner.run_scan()
            logger.info("Scheduled scan completed successfully")
        except Exception as e:
            logger.error(f"Error during scheduled scan: {e}")
    
    def start_scheduler(self):
        """Start the scheduler"""
        logger.info(f"Starting TikTok scanner scheduler - running every {self.scan_interval} minutes")
        
        # Schedule the scanner to run at regular intervals
        schedule.every(self.scan_interval).minutes.do(self.run_scanner)
        
        # Run once immediately
        logger.info("Running initial scan...")
        self.run_scanner()
        
        # Keep the scheduler running
        while True:
            try:
                schedule.run_pending()
                time.sleep(60)  # Check every minute
            except KeyboardInterrupt:
                logger.info("Scheduler stopped by user")
                break
            except Exception as e:
                logger.error(f"Scheduler error: {e}")
                time.sleep(300)  # Wait 5 minutes before retrying

def main():
    """Main function"""
    try:
        scheduler = TikTokScheduler()
        scheduler.start_scheduler()
    except Exception as e:
        logger.error(f"Fatal scheduler error: {e}")
        raise

if __name__ == "__main__":
    main()