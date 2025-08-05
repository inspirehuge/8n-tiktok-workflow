import os
import time
import logging
from datetime import datetime
from typing import List, Dict, Any, Optional
import gspread
from oauth2client.service_account import ServiceAccountCredentials
from dotenv import load_dotenv

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ProductFinderSheets:
    def __init__(self):
        """Initialize ProductFinder Google Sheets integration."""
        load_dotenv()
        
        # Google Sheets configuration
        self.sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'ProductFinderBot')
        self.worksheet_name = os.getenv('GOOGLE_WORKSHEET_NAME', 'Product_Matches')
        self.service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service_account.json')
        
        # Set up Google Sheets connection
        self.gc = self._setup_google_sheets()
        self.worksheet = None
        
        # Define column headers for ProductFinderBot
        self.headers = [
            'Reddit Title',
            'TikTok Title', 
            'Category',
            'TikTok URL',
            'Description',
            'Views',
            'Source',
            'Reddit URL',
            'Reddit Subreddit',
            'Reddit Score',
            'TikTok Author',
            'Match Score',
            'Date Added',
            'Search Query',
            'Status'
        ]
        
        logger.info("ProductFinderSheets initialized successfully")
    
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
            
            # Authorize the client
            gc = gspread.authorize(credentials)
            logger.info("Google Sheets API connection established")
            return gc
            
        except Exception as e:
            logger.error(f"Failed to setup Google Sheets connection: {e}")
            raise
    
    def _get_or_create_worksheet(self):
        """Get the worksheet, creating it if it doesn't exist."""
        try:
            # Try to open existing sheet
            try:
                sheet = self.gc.open(self.sheet_name)
                logger.info(f"Opened existing sheet: {self.sheet_name}")
            except gspread.SpreadsheetNotFound:
                # Create new sheet if it doesn't exist
                sheet = self.gc.create(self.sheet_name)
                logger.info(f"Created new sheet: {self.sheet_name}")
            
            # Try to get existing worksheet
            try:
                self.worksheet = sheet.worksheet(self.worksheet_name)
                logger.info(f"Found existing worksheet: {self.worksheet_name}")
            except gspread.WorksheetNotFound:
                # Create new worksheet
                self.worksheet = sheet.add_worksheet(
                    title=self.worksheet_name,
                    rows=1000,
                    cols=len(self.headers)
                )
                logger.info(f"Created new worksheet: {self.worksheet_name}")
                
                # Add headers
                self.worksheet.append_row(self.headers)
                logger.info("Added headers to worksheet")
                
                # Format headers
                self._format_headers()
            
            # Ensure headers are correct
            self._validate_headers()
            
        except Exception as e:
            logger.error(f"Failed to setup worksheet: {e}")
            raise
    
    def _format_headers(self):
        """Format the header row."""
        try:
            # Make headers bold
            self.worksheet.format('1:1', {
                'textFormat': {'bold': True},
                'backgroundColor': {'red': 0.9, 'green': 0.9, 'blue': 0.9}
            })
            
            # Auto-resize columns
            self.worksheet.columns_auto_resize(0, len(self.headers))
            
        except Exception as e:
            logger.warning(f"Failed to format headers: {e}")
    
    def _validate_headers(self):
        """Validate that headers match expected format."""
        try:
            current_headers = self.worksheet.row_values(1)
            
            if not current_headers:
                # No headers, add them
                self.worksheet.append_row(self.headers)
                self._format_headers()
            elif current_headers != self.headers:
                logger.warning("Headers don't match expected format, updating...")
                self.worksheet.update('1:1', [self.headers])
                self._format_headers()
                
        except Exception as e:
            logger.error(f"Failed to validate headers: {e}")
    
    def add_product_matches(self, matches: List[Dict[str, Any]]) -> int:
        """Add product matches to the sheet."""
        if not matches:
            logger.info("No matches to add")
            return 0
        
        try:
            if not self.worksheet:
                self._get_or_create_worksheet()
            
            # Prepare rows for batch insert
            rows_to_add = []
            
            for match in matches:
                row = [
                    match.get('reddit_title', '')[:500],  # Limit length
                    match.get('tiktok_title', '')[:500],
                    match.get('category', ''),
                    match.get('tiktok_url', ''),
                    match.get('description', '')[:500],
                    str(match.get('tiktok_views', 0)),
                    match.get('source', 'Reddit + TikTok'),
                    match.get('reddit_url', ''),
                    match.get('reddit_subreddit', ''),
                    str(match.get('reddit_score', 0)),
                    match.get('tiktok_author', ''),
                    str(match.get('match_score', 0.0)),
                    match.get('date', datetime.now().strftime('%Y-%m-%d %H:%M:%S')),
                    match.get('search_query', ''),
                    'New'
                ]
                rows_to_add.append(row)
            
            # Batch insert all rows
            if rows_to_add:
                self.worksheet.append_rows(rows_to_add)
                logger.info(f"Added {len(rows_to_add)} product matches to sheet")
                
                # Auto-resize columns after adding data
                try:
                    self.worksheet.columns_auto_resize(0, len(self.headers))
                except:
                    pass  # Ignore formatting errors
                
                return len(rows_to_add)
            
        except Exception as e:
            logger.error(f"Failed to add product matches: {e}")
            return 0
        
        return 0
    
    def get_existing_matches(self) -> List[Dict[str, Any]]:
        """Get existing matches from the sheet to avoid duplicates."""
        try:
            if not self.worksheet:
                self._get_or_create_worksheet()
            
            # Get all rows except header
            all_values = self.worksheet.get_all_values()
            
            if len(all_values) <= 1:
                return []
            
            matches = []
            headers = all_values[0]
            
            for row in all_values[1:]:
                # Pad row with empty strings if needed
                while len(row) < len(headers):
                    row.append('')
                
                match = dict(zip(headers, row))
                matches.append(match)
            
            logger.info(f"Retrieved {len(matches)} existing matches")
            return matches
            
        except Exception as e:
            logger.error(f"Failed to get existing matches: {e}")
            return []
    
    def is_duplicate_match(self, new_match: Dict[str, Any], existing_matches: List[Dict[str, Any]]) -> bool:
        """Check if a match already exists in the sheet."""
        new_reddit_title = new_match.get('reddit_title', '').lower()
        new_tiktok_url = new_match.get('tiktok_url', '')
        
        for existing in existing_matches:
            existing_reddit_title = existing.get('Reddit Title', '').lower()
            existing_tiktok_url = existing.get('TikTok URL', '')
            
            # Consider it a duplicate if both Reddit title and TikTok URL match
            if (new_reddit_title == existing_reddit_title and 
                new_tiktok_url == existing_tiktok_url):
                return True
        
        return False
    
    def add_unique_matches(self, matches: List[Dict[str, Any]]) -> int:
        """Add only unique matches to avoid duplicates."""
        if not matches:
            return 0
        
        # Get existing matches
        existing_matches = self.get_existing_matches()
        
        # Filter out duplicates
        unique_matches = []
        for match in matches:
            if not self.is_duplicate_match(match, existing_matches):
                unique_matches.append(match)
            else:
                logger.info(f"Skipping duplicate match: {match.get('reddit_title', '')[:50]}...")
        
        if unique_matches:
            logger.info(f"Adding {len(unique_matches)} unique matches (filtered {len(matches) - len(unique_matches)} duplicates)")
            return self.add_product_matches(unique_matches)
        else:
            logger.info("No unique matches to add")
            return 0
    
    def update_match_status(self, row_number: int, status: str):
        """Update the status of a specific match."""
        try:
            if not self.worksheet:
                self._get_or_create_worksheet()
            
            # Find status column (last column)
            status_col = len(self.headers)
            
            # Update status
            self.worksheet.update_cell(row_number, status_col, status)
            logger.info(f"Updated row {row_number} status to: {status}")
            
        except Exception as e:
            logger.error(f"Failed to update match status: {e}")
    
    def get_sheet_stats(self) -> Dict[str, Any]:
        """Get statistics about the sheet."""
        try:
            if not self.worksheet:
                self._get_or_create_worksheet()
            
            all_values = self.worksheet.get_all_values()
            total_rows = len(all_values) - 1  # Exclude header
            
            # Count by category
            categories = {}
            statuses = {}
            
            if len(all_values) > 1:
                headers = all_values[0]
                category_idx = headers.index('Category') if 'Category' in headers else -1
                status_idx = headers.index('Status') if 'Status' in headers else -1
                
                for row in all_values[1:]:
                    if category_idx >= 0 and category_idx < len(row):
                        category = row[category_idx] or 'Unknown'
                        categories[category] = categories.get(category, 0) + 1
                    
                    if status_idx >= 0 and status_idx < len(row):
                        status = row[status_idx] or 'Unknown'
                        statuses[status] = statuses.get(status, 0) + 1
            
            return {
                'total_matches': total_rows,
                'categories': categories,
                'statuses': statuses,
                'sheet_name': self.sheet_name,
                'worksheet_name': self.worksheet_name
            }
            
        except Exception as e:
            logger.error(f"Failed to get sheet stats: {e}")
            return {}
    
    def cleanup_old_matches(self, days_old: int = 30):
        """Remove matches older than specified days."""
        try:
            if not self.worksheet:
                self._get_or_create_worksheet()
            
            # This would require parsing dates and removing old rows
            # Implementation depends on specific requirements
            logger.info(f"Cleanup function not implemented yet")
            
        except Exception as e:
            logger.error(f"Failed to cleanup old matches: {e}")

if __name__ == "__main__":
    # Test the ProductFinderSheets
    try:
        sheets = ProductFinderSheets()
        
        # Test with sample data
        sample_matches = [
            {
                'reddit_title': 'Test Reddit Post About Back Pain',
                'tiktok_title': 'Amazing Back Pain Relief Device!',
                'category': 'Back Pain',
                'tiktok_url': 'https://tiktok.com/test123',
                'description': 'This device helps with back pain',
                'tiktok_views': 50000,
                'source': 'Reddit + TikTok',
                'reddit_url': 'https://reddit.com/r/backpain/test',
                'reddit_subreddit': 'backpain',
                'reddit_score': 25,
                'tiktok_author': '@healthguru',
                'match_score': 0.85,
                'search_query': 'back pain relief'
            }
        ]
        
        # Add test matches
        added = sheets.add_unique_matches(sample_matches)
        print(f"Added {added} test matches")
        
        # Get stats
        stats = sheets.get_sheet_stats()
        print(f"Sheet stats: {stats}")
        
    except Exception as e:
        logger.error(f"Test failed: {e}")