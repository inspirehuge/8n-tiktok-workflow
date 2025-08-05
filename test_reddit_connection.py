#!/usr/bin/env python3
"""
Test script to diagnose Reddit API connection issues
"""

import os
import sys
from dotenv import load_dotenv
import praw

def test_reddit_connection():
    """Test Reddit API connection and diagnose issues."""
    print("🔍 Testing Reddit API Connection")
    print("=" * 40)
    
    # Load environment variables
    load_dotenv()
    
    # Check if credentials are set
    client_id = os.getenv('REDDIT_CLIENT_ID')
    client_secret = os.getenv('REDDIT_CLIENT_SECRET')
    user_agent = os.getenv('REDDIT_USER_AGENT', 'ProductFinderBot/1.0')
    
    print(f"Client ID: {'✓ Set' if client_id else '❌ Missing'}")
    print(f"Client Secret: {'✓ Set' if client_secret else '❌ Missing'}")
    print(f"User Agent: {user_agent}")
    
    if not client_id or not client_secret:
        print("\n❌ Reddit API credentials are missing!")
        print("\nTo fix this:")
        print("1. Go to https://www.reddit.com/prefs/apps")
        print("2. Click 'Create App' or 'Create Another App'")
        print("3. Choose 'script' as the app type")
        print("4. Copy the client ID (under the app name)")
        print("5. Copy the client secret")
        print("6. Add them to your .env file:")
        print("   REDDIT_CLIENT_ID=your_client_id_here")
        print("   REDDIT_CLIENT_SECRET=your_client_secret_here")
        return False
    
    # Test connection
    try:
        print("\n🔄 Testing Reddit API connection...")
        
        reddit = praw.Reddit(
            client_id=client_id,
            client_secret=client_secret,
            user_agent=user_agent
        )
        
        # Test with a simple request
        subreddit = reddit.subreddit('test')
        
        # Try to get a few posts
        posts = list(subreddit.hot(limit=5))
        
        print(f"✅ Connection successful!")
        print(f"   Retrieved {len(posts)} posts from r/test")
        print(f"   Reddit instance: {reddit}")
        
        # Test with a target subreddit
        print("\n🎯 Testing target subreddit access...")
        target_subreddit = reddit.subreddit('ChronicPain')
        target_posts = list(target_subreddit.hot(limit=3))
        
        print(f"✅ Successfully accessed r/ChronicPain")
        print(f"   Retrieved {len(target_posts)} posts")
        
        if target_posts:
            print(f"   Sample post: {target_posts[0].title[:50]}...")
        
        return True
        
    except praw.exceptions.ResponseException as e:
        print(f"❌ Reddit API Error: {e}")
        
        if "401" in str(e):
            print("\n🔧 401 Unauthorized Error - Possible fixes:")
            print("1. Check your client ID and secret are correct")
            print("2. Make sure there are no extra spaces in .env file")
            print("3. Verify your app is set to 'script' type on Reddit")
            print("4. Try creating a new Reddit app")
            
        elif "403" in str(e):
            print("\n🔧 403 Forbidden Error - Possible fixes:")
            print("1. Your app might be rate limited")
            print("2. Check if the subreddit exists and is accessible")
            print("3. Try again in a few minutes")
            
        return False
        
    except Exception as e:
        print(f"❌ Unexpected error: {e}")
        print(f"   Error type: {type(e).__name__}")
        return False

def main():
    """Main function."""
    success = test_reddit_connection()
    
    if success:
        print("\n🎉 Reddit API is working correctly!")
        print("You can now run the ProductFinderBot.")
    else:
        print("\n❌ Reddit API connection failed.")
        print("Please fix the issues above before running ProductFinderBot.")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())