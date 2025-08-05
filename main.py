import os
import time
import logging
from datetime import datetime
from typing import Set, List, Dict, Any
import gspread
from oauth2client.service_account import ServiceAccountCredentials
import requests
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class GoogleSheetsToTelegram:
    def __init__(self):
        """Initialize the Google Sheets to Telegram bot."""
        # Load environment variables
        load_dotenv()
        
        self.telegram_token = os.getenv('TELEGRAM_TOKEN')
        self.telegram_chat_id = os.getenv('TELEGRAM_CHAT_ID')
        
        if not self.telegram_token or not self.telegram_chat_id:
            raise ValueError("TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set in .env file")
        
        # Set up Google Sheets connection
        self.sheet_name = "Koladata"
        self.worksheet_name = "Sheet1"
        self.service_account_file = "service_account.json"
        
        # Track sent rows to avoid duplicates
        self.sent_rows: Set[int] = set()
        
        # Initialize Google Sheets client
        self.gc = self._setup_google_sheets()
        self.worksheet = None
        
        logger.info("GoogleSheetsToTelegram initialized successfully")
    
    def _setup_google_sheets(self) -> gspread.Client:
        """Set up Google Sheets API connection."""
        try:
            # Define the scope
            scope = [
                'https://spreadsheets.google.com/feeds',
                'https://www.googleapis.com/auth/drive'
            ]
            
            # Add credentials to the account
            credentials = ServiceAccountCredentials.from_json_keyfile_name(
                self.service_account_file, scope
            )
            
            # Authorize the clientsheet
            gc = gspread.authorize(credentials)
            logger.info("Google Sheets API connection established")
            return gc
            
        except Exception as e:
            logger.error(f"Failed to setup Google Sheets connection: {e}")
            raise
    
    def _get_worksheet(self):
        """Get the worksheet, with retry logic."""
        try:
            sheet = self.gc.open(self.sheet_name)
            self.worksheet = sheet.worksheet(self.worksheet_name)
            logger.info(f"Connected to worksheet: {self.worksheet_name}")
        except Exception as e:
            logger.error(f"Failed to open worksheet: {e}")
            raise
    
    def _get_all_rows(self) -> List[List[str]]:
        """Retrieve all rows from the worksheet (excluding header)."""
        try:
            if not self.worksheet:
                self._get_worksheet()
            
            # Get all values from the worksheet
            all_values = self.worksheet.get_all_values()
            
            # Return all rows except the header (first row)
            if len(all_values) > 1:
                return all_values[1:]  # Skip header row
            else:
                return []
                
        except Exception as e:
            logger.error(f"Failed to retrieve rows: {e}")
            return []
    
    def _format_message(self, row_data: List[str], row_index: int) -> str:
        """Format row data into a Markdown message for Telegram."""
        try:
            # Expected fields: title, category, video_url, description, date, views, source
            fields = ['title', 'category', 'video_url', 'description', 'date', 'views', 'source']
            
            # Pad row_data with empty strings if it's shorter than expected
            while len(row_data) < len(fields):
                row_data.append('')
            
            # Create a dictionary mapping field names to values
            data = dict(zip(fields, row_data))
            
            # Format the message in Markdown
            message = f"""📊 **New Data Entry #{row_index + 2}**

🏷️ **Title:** {data['title'] or 'N/A'}
📂 **Category:** {data['category'] or 'N/A'}
🎥 **Video URL:** {data['video_url'] or 'N/A'}
📝 **Description:** {data['description'] or 'N/A'}
📅 **Date:** {data['date'] or 'N/A'}
👀 **Views:** {data['views'] or 'N/A'}
🔗 **Source:** {data['source'] or 'N/A'}

---
*Sent at {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*"""
            
            return message
            
        except Exception as e:
            logger.error(f"Failed to format message for row {row_index}: {e}")
            return f"Error formatting data for row {row_index + 2}"
    
    def _send_telegram_message(self, message: str) -> bool:
        """Send a message to Telegram bot."""
        try:
            url = f"https://api.telegram.org/bot{self.telegram_token}/sendMessage"
            
            payload = {
                'chat_id': self.telegram_chat_id,
                'text': message,
                'parse_mode': 'Markdown',
                'disable_web_page_preview': True
            }
            
            response = requests.post(url, json=payload, timeout=30)
            
            if response.status_code == 200:
                logger.info("Message sent successfully to Telegram")
                return True
            else:
                logger.error(f"Failed to send message to Telegram: {response.status_code} - {response.text}")
                return False
                
        except Exception as e:
            logger.error(f"Error sending message to Telegram: {e}")
            return False
    
    def _process_new_rows(self):
        """Process new rows and send them to Telegram."""
        try:
            rows = self._get_all_rows()
            
            if not rows:
                logger.info("No rows found in the worksheet")
                return
            
            new_rows_count = 0
            
            # Process each row
            for index, row in enumerate(rows):
                # Skip if this row was already sent
                if index in self.sent_rows:
                    continue
                
                # Skip empty rows (all fields empty)
                if not any(cell.strip() for cell in row):
                    continue
                
                # Format and send the message
                message = self._format_message(row, index)
                
                if self._send_telegram_message(message):
                    self.sent_rows.add(index)
                    new_rows_count += 1
                    logger.info(f"Sent row {index + 2} to Telegram")
                    
                    # Small delay between messages to avoid rate limiting
                    time.sleep(1)
                else:
                    logger.error(f"Failed to send row {index + 2}")
            
            if new_rows_count > 0:
                logger.info(f"Processed {new_rows_count} new rows")
            else:
                logger.info("No new rows to process")
                
        except Exception as e:
            logger.error(f"Error processing rows: {e}")
    
    def run(self):
        """Main loop - check for new rows every 5 minutes."""
        logger.info("Starting Google Sheets to Telegram bot...")
        
        while True:
            try:
                logger.info("Checking for new rows...")
                self._process_new_rows()
                
                logger.info("Waiting 5 minutes before next check...")
                time.sleep(300)  # 5 minutes = 300 seconds
                
            except KeyboardInterrupt:
                logger.info("Bot stopped by user")
                break
            except Exception as e:
                logger.error(f"Unexpected error in main loop: {e}")
                logger.info("Waiting 1 minute before retrying...")
                time.sleep(60)  # Wait 1 minute before retrying

def main():
    """Main function to start the bot."""
    try:
        bot = GoogleSheetsToTelegram()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())