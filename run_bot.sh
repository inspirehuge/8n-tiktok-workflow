#!/bin/bash

echo "🤖 Starting TikTok Viral Bot (Persistent Mode)..."
echo "Bot will run every 15 minutes automatically."
echo "Press Ctrl+C to stop."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run the bot in persistent mode
python3 tiktok_viral_bot.py