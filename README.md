# 🧠 ProductFinderBot – Automated Product Discovery from Reddit to TikTok

**🎯 Purpose:**  
ProductFinderBot is an intelligent discovery bot that analyzes real user pain points from Reddit, matches them with viral TikTok product videos, and reports the results via Google Sheets and Telegram.

---

## 🔧 Workflow Overview

1. **Reddit Scanning**  
   - Scrapes specific subreddits (e.g. `r/ChronicPain`, `r/BuyItForLife`, `r/backpain`)  
   - Extracts post titles and content from the past 7 days  
   - Detects pain-related problems using keywords like "pain", "relief", "can't sleep", "sore", etc.

2. **TikTok Product Matching**  
   - Automatically matches identified problems with relevant TikTok product videos  
   - Filters for viral content (e.g. videos with >10K views)  
   - Example: "plantar fasciitis pain" → TikTok video of arch support insoles

3. **Google Sheets Logging**  
   Each matched product is logged with:
   - ✅ Reddit problem title  
   - ✅ TikTok product title  
   - ✅ Category (e.g. Foot Care)  
   - ✅ TikTok video link  
   - ✅ Description  
   - ✅ View count  
   - ✅ Source (Reddit + TikTok)

4. **Telegram Notification**  
   - When a match is found, a Telegram bot sends a notification  
   - Includes product title, description, and video link

---

## 🧱 Technical Stack

| Component           | Description                              |
|---------------------|------------------------------------------|
| Reddit API (PRAW)   | Analyzes user-generated problem posts    |
| TikTok Scraper      | Matches problems with product videos     |
| Google Sheets API   | Logs matched products                    |
| Telegram Bot API    | Sends automated notifications            |
| Selenium            | Web scraping for TikTok                  |
| BeautifulSoup       | HTML parsing                             |

---

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up API Credentials

1. **Reddit API:**
   - Go to https://www.reddit.com/prefs/apps
   - Create a new app (script type)
   - Note your client ID and secret

2. **Telegram Bot:**
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Create a new bot with `/newbot`
   - Get your bot token and chat ID

3. **Google Sheets:**
   - Go to [Google Cloud Console](https://console.cloud.google.com/)
   - Enable Google Sheets API and Google Drive API
   - Create a service account and download JSON key
   - Rename the key file to `service_account.json`

### 3. Configure Environment

```bash
cp .env.example .env
# Edit .env with your actual credentials
```

### 4. Run the Bot

```bash
# Test components
python product_finder_bot.py test

# Run single scan
python product_finder_bot.py once

# Run on schedule (every 6 hours by default)
python product_finder_bot.py

# View statistics
python product_finder_bot.py stats
```

---

## 📋 Configuration

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `REDDIT_CLIENT_ID` | Reddit API client ID | Required |
| `REDDIT_CLIENT_SECRET` | Reddit API client secret | Required |
| `TELEGRAM_TOKEN` | Telegram bot token | Required |
| `TELEGRAM_CHAT_ID` | Telegram chat ID for notifications | Required |
| `GOOGLE_SHEET_NAME` | Name of Google Sheet | ProductFinderBot |
| `SCAN_INTERVAL_HOURS` | Hours between scans | 6 |
| `MIN_TIKTOK_VIEWS` | Minimum views for viral content | 10000 |
| `MAX_PROBLEMS_PER_SCAN` | Max problems to process per scan | 20 |

### Target Subreddits

The bot monitors these subreddits for pain-related posts:
- `ChronicPain`, `BuyItForLife`, `backpain`
- `migraine`, `Fibromyalgia`, `PlantarFasciitis`
- `kneepain`, `shoulderpain`, `neckpain`
- `sciatica`, `arthritis`, `insomnia`, `sleep`
- `PainManagement`, `ehlersdanlos`, `disability`

---

## 🎯 How It Works

### Pain Detection Algorithm

The bot uses multiple methods to identify pain-related posts:

1. **Keyword Matching**: Searches for terms like "pain", "relief", "chronic", "suffering"
2. **Pattern Recognition**: Detects phrases like "can't sleep", "need help", "what works"
3. **Category Classification**: Automatically categorizes problems (Back Pain, Sleep Issues, etc.)

### TikTok Matching

1. **Search Query Generation**: Converts Reddit problems into TikTok search terms
2. **Video Filtering**: Only considers videos with sufficient views and product-related content
3. **Relevance Scoring**: Calculates match quality based on keyword overlap and popularity

### Data Flow

```
Reddit Posts → Pain Detection → Category Classification → TikTok Search → 
Product Filtering → Match Scoring → Google Sheets → Telegram Notification
```

---

## 📊 Google Sheets Structure

The bot creates a sheet with these columns:

| Column | Description |
|--------|-------------|
| Reddit Title | Original Reddit post title |
| TikTok Title | Matching TikTok video title |
| Category | Problem category (Back Pain, etc.) |
| TikTok URL | Link to TikTok video |
| Description | Video description |
| Views | TikTok video view count |
| Source | Always "Reddit + TikTok" |
| Reddit URL | Link to original Reddit post |
| Match Score | Relevance score (0-1) |
| Date Added | When match was found |
| Status | Processing status |

---

## 🤖 Command Line Usage

```bash
# Run different modes
python product_finder_bot.py once    # Single scan
python product_finder_bot.py stats   # Show statistics  
python product_finder_bot.py test    # Test all components
python product_finder_bot.py         # Scheduled runs

# View logs
tail -f product_finder_bot.log
```

---

## 🛠 Troubleshooting

### Common Issues

1. **Reddit 401 Unauthorized**
   - Check your Reddit API credentials
   - Ensure client ID and secret are correct
   - Verify user agent string

2. **TikTok Scraping Fails**
   - TikTok may block automated requests
   - Consider using proxy services or APIs
   - Check Chrome driver installation

3. **Google Sheets Access Denied**
   - Ensure service account JSON is valid
   - Share your sheet with the service account email
   - Check API permissions

4. **Telegram Not Working**
   - Verify bot token and chat ID
   - Start a conversation with your bot first
   - Check network connectivity

### Debug Mode

Enable debug logging by setting `DEBUG_MODE=true` in your `.env` file.

---

## 🔮 Future Enhancements

- [ ] Replace TikTok scraper with proxy-friendly tools like Apify  
- [ ] Add sentiment analysis from product reviews (e.g. Amazon)  
- [ ] Calculate and rank product trend scores
- [ ] Add support for more social platforms (Instagram, YouTube Shorts)
- [ ] Implement machine learning for better problem-product matching
- [ ] Add web dashboard for monitoring and management

---

## 📄 License

MIT License - feel free to modify and use as needed.

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

---

## 📞 Support

If you encounter issues or have questions:

1. Check the troubleshooting section above
2. Review the logs in `product_finder_bot.log`
3. Open an issue on GitHub with detailed error information

---

**Happy product hunting! 🎯**