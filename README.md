# 🤖 TikTok Viral Bot

An automated Python agent that scrapes Reddit for product keywords, searches TikTok for viral videos, and sends filtered results to Telegram.

## 🚀 Features

- **Reddit Scraping**: Automatically scrapes latest posts from r/shutupandtakemymoney and r/BuyItForLife
- **Keyword Extraction**: Uses NLP to extract product-related keywords from Reddit post titles
- **TikTok Search**: Searches TikTok using Playwright for viral videos matching extracted keywords
- **Smart Filtering**: Only includes videos with 10K+ views from the last 48 hours
- **Telegram Integration**: Sends formatted messages to your Telegram channel/group
- **Duplicate Prevention**: Tracks sent videos to avoid duplicates
- **Persistent Scheduling**: Runs automatically every 15 minutes
- **Manual Trigger**: Web interface with "Run" button for manual execution
- **Comprehensive Logging**: Detailed logs for monitoring and debugging

## 📋 Requirements

- Python 3.8+
- Linux/macOS/Windows
- Internet connection
- Telegram Bot Token and Chat ID

## 🔧 Installation

1. **Clone or download this repository**
2. **Run the setup script**:
   ```bash
   chmod +x setup.sh
   ./setup.sh
   ```

The setup script will:
- Create a Python virtual environment
- Install all dependencies
- Install Playwright browsers
- Set up the directory structure

## ⚙️ Configuration

The bot is pre-configured with the provided Telegram credentials in `config.py`:

- **TELEGRAM_BOT_TOKEN**: `8358172003:AAGSxIY9ejRF8o_nG-mhIY6ZXany7hq9XqM`
- **TELEGRAM_CHAT_ID**: `-1002197208879`

You can modify other settings in `config.py`:
- Reddit subreddits to monitor
- Minimum view count threshold
- Video age limit
- Run interval

## 🎯 Usage

### Option 1: Persistent Bot (Recommended)
Run the bot continuously with 15-minute intervals:
```bash
./run_bot.sh
```

### Option 2: Web Interface with Manual Button
Start the web interface for manual control:
```bash
./run_web.sh
```
Then open http://localhost:5000 in your browser.

### Option 3: Single Manual Run
Execute the bot once:
```bash
source venv/bin/activate
python3 tiktok_viral_bot.py --manual
```

## 🔄 How It Works

1. **Reddit Scraping**: Fetches latest 10 posts from each configured subreddit
2. **Keyword Extraction**: Extracts meaningful product keywords from post titles
3. **TikTok Search**: Searches TikTok for each keyword using headless browser
4. **Video Analysis**: Extracts video metadata (title, views, author, URL)
5. **Filtering**: Applies criteria (10K+ views, recent, not previously sent)
6. **Telegram Notification**: Sends formatted message with video details
7. **Tracking**: Records sent videos to prevent future duplicates

## 📱 Telegram Message Format

```
🔥 *New Viral Product Video*
🎬 {video title}
👁️ {views} views
👤 @{author}
🔗 [Watch on TikTok]({video URL})
```

## 📁 File Structure

```
tiktok-viral-bot/
├── tiktok_viral_bot.py    # Main bot script
├── web_interface.py       # Web interface for manual runs
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── setup.sh             # Setup script
├── run_bot.sh           # Run persistent bot
├── run_web.sh           # Run web interface
├── templates/
│   └── index.html       # Web interface template
├── sent_videos.txt      # Tracks sent videos (auto-created)
├── bot.log             # Application logs (auto-created)
└── README.md           # This file
```

## 🔍 Monitoring

- **Logs**: Check `bot.log` for detailed execution logs
- **Web Interface**: View real-time status at http://localhost:5000
- **Sent Videos**: Track history in `sent_videos.txt`

## 🛠️ Troubleshooting

### Common Issues

1. **Playwright Browser Not Found**:
   ```bash
   source venv/bin/activate
   playwright install chromium
   ```

2. **Permission Denied on Scripts**:
   ```bash
   chmod +x setup.sh run_bot.sh run_web.sh
   ```

3. **TikTok Search Issues**:
   - TikTok may block automated requests
   - The bot includes delays and user agent rotation
   - Check logs for specific error messages

4. **No Videos Found**:
   - Verify Reddit subreddits are accessible
   - Check if keywords are being extracted properly
   - Lower the view count threshold in config.py

### Debug Mode

Run with detailed logging:
```bash
source venv/bin/activate
python3 tiktok_viral_bot.py --manual
```

## 📊 Performance

- **Reddit API**: ~2-3 requests per cycle
- **TikTok Search**: 1 request per keyword (rate-limited)
- **Telegram API**: 1 request per video sent
- **Memory Usage**: ~50-100MB during execution
- **Execution Time**: 2-5 minutes per cycle (depending on keywords)

## 🔒 Security & Privacy

- Uses headless browsing for TikTok searches
- Rotates user agents to avoid detection
- No personal data collection
- Logs contain only operational information
- Telegram credentials are configurable

## 🚨 Rate Limiting

The bot includes built-in rate limiting:
- 2-second delays between TikTok searches
- 1-second delays between Telegram messages
- Respects robots.txt and platform guidelines

## 📝 Customization

### Adding New Subreddits
Edit `config.py`:
```python
REDDIT_SUBREDDITS = [
    "shutupandtakemymoney",
    "BuyItForLife",
    "ProductPorn",  # Add new subreddit
]
```

### Adjusting Filters
Modify filtering criteria in `config.py`:
```python
MIN_VIEWS = 5000        # Lower threshold
MAX_VIDEO_AGE_HOURS = 72  # Extend time window
```

### Changing Schedule
Update run interval in `config.py`:
```python
RUN_INTERVAL_MINUTES = 10  # Run every 10 minutes
```

## 📞 Support

For issues or questions:
1. Check the logs in `bot.log`
2. Review this README
3. Verify your configuration in `config.py`
4. Test with manual runs first

## ⚠️ Disclaimer

This bot is for educational and personal use. Please respect:
- Platform terms of service
- Rate limiting guidelines
- Copyright and intellectual property rights
- Privacy considerations

Use responsibly and in accordance with all applicable laws and platform policies.