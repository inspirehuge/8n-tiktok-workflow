#!/usr/bin/env python3
"""
Reddit → TikTok Product Discovery → Google Sheets → Telegram Bot
Main controller script that orchestrates the entire workflow.
"""

import os
import time
from datetime import datetime
from typing import List, Dict

# Import our custom modules
from reddit_scraper import get_problems
from tiktok_matcher import find_matching_products
from update_sheet import write_products_to_sheet, setup_sheet_headers


def run_discovery_and_update() -> None:
    """
    Main function that runs the complete discovery and update process.
    """
    
    print("🚀 Starting Reddit → TikTok Product Discovery Process")
    print("=" * 60)
    
    # Step 1: Setup Google Sheet headers if needed
    print("\n📊 Setting up Google Sheet...")
    if not setup_sheet_headers():
        print("❌ Failed to setup Google Sheet. Please check your credentials.")
        return
    
    # Step 2: Scrape Reddit for problems
    print("\n🔍 Scraping Reddit for user problems...")
    try:
        problems = get_problems()
        print(f"✅ Found {len(problems)} problems from Reddit")
        
        if not problems:
            print("⚠️  No problems found. This might be due to Reddit API limits or configuration.")
            return
            
    except Exception as e:
        print(f"❌ Error scraping Reddit: {e}")
        return
    
    # Step 3: Process each problem
    total_products_added = 0
    
    for i, problem in enumerate(problems, 1):
        print(f"\n📝 Processing problem {i}/{len(problems)}")
        print(f"   Problem: {problem['problem'][:80]}...")
        print(f"   Keywords: {problem['keywords']}")
        
        try:
            # Find matching products on TikTok
            products = find_matching_products(problem["keywords"], problem["problem"])
            
            if products:
                print(f"   🎯 Found {len(products)} matching products")
                
                # Write products to Google Sheet
                if write_products_to_sheet(products):
                    total_products_added += len(products)
                    print(f"   ✅ Added {len(products)} products to sheet")
                else:
                    print(f"   ❌ Failed to add products to sheet")
            else:
                print(f"   ⚠️  No matching products found")
                
        except Exception as e:
            print(f"   ❌ Error processing problem: {e}")
            continue
        
        # Small delay to be respectful to APIs
        time.sleep(1)
    
    # Summary
    print("\n" + "=" * 60)
    print("🎉 Discovery Process Complete!")
    print(f"📊 Total problems processed: {len(problems)}")
    print(f"🛍️  Total products added: {total_products_added}")
    print(f"📅 Completed at: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    if total_products_added > 0:
        print("\n💬 Your Telegram bot should now send notifications for these new products!")
    
    print("=" * 60)


def run_single_test() -> None:
    """
    Run a single test with mock data to verify the system works.
    """
    
    print("🧪 Running single test with mock data...")
    
    # Mock problem data
    test_problem = {
        "problem": "chronic back pain from sitting at desk all day",
        "context": "I work in an office and my lower back kills me every day by 3 PM.",
        "keywords": ["back", "pain", "sitting", "office", "desk"]
    }
    
    print(f"Test problem: {test_problem['problem']}")
    print(f"Keywords: {test_problem['keywords']}")
    
    # Find products
    products = find_matching_products(test_problem["keywords"], test_problem["problem"])
    
    if products:
        print(f"\nFound {len(products)} products:")
        for product in products:
            print(f"  - {product['title']} ({product['category']})")
        
        # Try to write to sheet
        if write_products_to_sheet(products):
            print("\n✅ Test successful! Products added to Google Sheet.")
        else:
            print("\n❌ Test failed: Could not write to Google Sheet.")
    else:
        print("\n❌ Test failed: No products found.")


def main():
    """
    Main entry point with command line options.
    """
    
    import sys
    
    # Check for command line arguments
    if len(sys.argv) > 1:
        if sys.argv[1] == "test":
            run_single_test()
            return
        elif sys.argv[1] == "setup":
            print("🔧 Setting up Google Sheet headers...")
            if setup_sheet_headers():
                print("✅ Setup complete!")
            else:
                print("❌ Setup failed!")
            return
    
    # Check environment variables
    required_env_vars = [
        'REDDIT_CLIENT_ID',
        'REDDIT_CLIENT_SECRET', 
        'REDDIT_USER_AGENT'
    ]
    
    missing_vars = [var for var in required_env_vars if not os.getenv(var)]
    
    if missing_vars:
        print("⚠️  Warning: Missing environment variables:")
        for var in missing_vars:
            print(f"   - {var}")
        print("\nThe system will use default values, but Reddit scraping may not work properly.")
        print("Please set these environment variables for full functionality.")
        print()
    
    # Check for service account file
    service_account_file = os.getenv('GOOGLE_SERVICE_ACCOUNT_FILE', 'service_account.json')
    if not os.path.exists(service_account_file):
        print(f"⚠️  Warning: Google service account file '{service_account_file}' not found.")
        print("Please ensure you have a valid service_account.json file for Google Sheets access.")
        print()
    
    # Run the main process
    try:
        run_discovery_and_update()
    except KeyboardInterrupt:
        print("\n\n⏹️  Process interrupted by user.")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")


if __name__ == "__main__":
    main()