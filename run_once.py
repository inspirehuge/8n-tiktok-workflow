#!/usr/bin/env python3
"""
TikTok Scanner - Single Run
Runs the TikTok viral product scanner once for testing.
"""

import sys
from tiktok_scanner import TikTokScanner

def main():
    """Run scanner once"""
    try:
        print("🚀 Starting TikTok viral product scanner...")
        scanner = TikTokScanner()
        scanner.run_scan()
        print("✅ Scan completed!")
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("Please check your config.json file or environment variables.")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()