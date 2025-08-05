import gspread
from google.oauth2.service_account import Credentials
from typing import List, Dict
import os
from datetime import datetime


def write_products_to_sheet(products: List[Dict]) -> bool:
    """
    Append product data to Google Sheets.
    
    Args:
        products: List of product dictionaries to append
        
    Returns:
        Boolean indicating success
    """
    
    try:
        # Define the scope for Google Sheets and Drive APIs
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        # Load credentials from service account file
        service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service_account.json')
        
        if not os.path.exists(service_account_file):
            print(f"Error: Service account file '{service_account_file}' not found.")
            print("Please ensure you have a valid service_account.json file in the project directory.")
            return False
        
        # Authenticate and create client
        credentials = Credentials.from_service_account_file(service_account_file, scopes=scope)
        client = gspread.authorize(credentials)
        
        # Open the Google Sheet
        sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'Product Discovery Sheet')
        
        try:
            sheet = client.open(sheet_name).sheet1
        except gspread.SpreadsheetNotFound:
            print(f"Error: Spreadsheet '{sheet_name}' not found.")
            print("Please ensure the sheet exists and is shared with your service account email.")
            return False
        
        # Ensure headers exist
        headers = ['title', 'category', 'videoUrl', 'description', 'date', 'views', 'source', 'problem']
        
        # Check if sheet is empty or needs headers
        try:
            existing_headers = sheet.row_values(1)
            if not existing_headers or existing_headers != headers:
                sheet.insert_row(headers, 1)
                print("Headers added to sheet")
        except Exception:
            # Sheet is empty, add headers
            sheet.insert_row(headers, 1)
            print("Headers added to new sheet")
        
        # Prepare rows for insertion
        rows_to_add = []
        
        for product in products:
            # Ensure all required fields are present
            row = [
                product.get('title', ''),
                product.get('category', ''),
                product.get('videoUrl', ''),
                product.get('description', ''),
                product.get('date', datetime.now().strftime("%Y-%m-%d")),
                product.get('views', ''),
                product.get('source', 'TikTok'),
                product.get('problem', '')
            ]
            rows_to_add.append(row)
        
        # Add all rows at once for better performance
        if rows_to_add:
            sheet.append_rows(rows_to_add)
            print(f"Successfully added {len(rows_to_add)} products to the sheet")
            
            # Log the added products
            for i, product in enumerate(products):
                print(f"  {i+1}. {product.get('title', 'Unknown')} - {product.get('category', 'Unknown Category')}")
        
        return True
        
    except Exception as e:
        print(f"Error updating Google Sheet: {e}")
        return False


def setup_sheet_headers(sheet_name: str = None) -> bool:
    """
    Set up the Google Sheet with proper headers if it doesn't exist.
    
    Args:
        sheet_name: Name of the sheet to create/setup
        
    Returns:
        Boolean indicating success
    """
    
    try:
        # Define the scope
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service_account.json')
        
        if not os.path.exists(service_account_file):
            print(f"Error: Service account file '{service_account_file}' not found.")
            return False
        
        credentials = Credentials.from_service_account_file(service_account_file, scopes=scope)
        client = gspread.authorize(credentials)
        
        if not sheet_name:
            sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'Product Discovery Sheet')
        
        try:
            # Try to open existing sheet
            sheet = client.open(sheet_name).sheet1
            print(f"Found existing sheet: {sheet_name}")
        except gspread.SpreadsheetNotFound:
            # Create new sheet
            spreadsheet = client.create(sheet_name)
            sheet = spreadsheet.sheet1
            print(f"Created new sheet: {sheet_name}")
        
        # Set up headers
        headers = ['title', 'category', 'videoUrl', 'description', 'date', 'views', 'source', 'problem']
        
        # Check if headers already exist
        try:
            existing_headers = sheet.row_values(1)
            if existing_headers != headers:
                sheet.insert_row(headers, 1)
                print("Headers updated")
        except Exception:
            sheet.insert_row(headers, 1)
            print("Headers added")
        
        return True
        
    except Exception as e:
        print(f"Error setting up sheet: {e}")
        return False


def get_existing_products(limit: int = 100) -> List[Dict]:
    """
    Retrieve existing products from the sheet to avoid duplicates.
    
    Args:
        limit: Maximum number of rows to retrieve
        
    Returns:
        List of existing product dictionaries
    """
    
    try:
        scope = [
            "https://spreadsheets.google.com/feeds",
            "https://www.googleapis.com/auth/drive"
        ]
        
        service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service_account.json')
        credentials = Credentials.from_service_account_file(service_account_file, scopes=scope)
        client = gspread.authorize(credentials)
        
        sheet_name = os.getenv('GOOGLE_SHEET_NAME', 'Product Discovery Sheet')
        sheet = client.open(sheet_name).sheet1
        
        # Get all records
        records = sheet.get_all_records()
        
        # Return last 'limit' records
        return records[-limit:] if len(records) > limit else records
        
    except Exception as e:
        print(f"Error retrieving existing products: {e}")
        return []


if __name__ == "__main__":
    # Test the sheet updater
    test_products = [
        {
            "title": "Test Smart Arch Support Insoles",
            "category": "Foot Care",
            "videoUrl": "https://www.tiktok.com/@test/video/1234567890",
            "description": "Test product for development",
            "date": datetime.now().strftime("%Y-%m-%d"),
            "views": "1.2M",
            "source": "TikTok",
            "problem": "test foot pain from standing all day"
        }
    ]
    
    print("Testing Google Sheets integration...")
    success = write_products_to_sheet(test_products)
    
    if success:
        print("✅ Sheet update successful!")
    else:
        print("❌ Sheet update failed. Please check your credentials and sheet setup.")