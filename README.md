# 🔧 Reddit → TikTok Product Discovery → Google Sheets → Telegram Bot

A Python-based system that automatically:
1. 🔍 Scrapes Reddit for user pain/problem posts
2. 🎯 Extracts keywords from those problems  
3. 🎥 Searches TikTok for matching product videos (simulated)
4. 📊 Appends matched product data to Google Sheets
5. 💬 Triggers Telegram notifications via your existing bot

## 📁 Project Structure

```
├── reddit_scraper.py      # Scrapes Reddit for problems
├── tiktok_matcher.py      # Matches problems to TikTok products
├── update_sheet.py        # Updates Google Sheets
├── main.py               # Main controller script
├── requirements.txt      # Python dependencies
├── README.md            # This file
└── service_account.json # Google Sheets credentials (you need to create this)
```

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Reddit API

1. Go to [Reddit Apps](https://www.reddit.com/prefs/apps)
2. Click "Create App" or "Create Another App"
3. Choose "script" type
4. Note your `client_id` and `client_secret`

### 3. Set Up Google Sheets API

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing one
3. Enable Google Sheets API and Google Drive API
4. Create a Service Account
5. Download the JSON key file and rename it to `service_account.json`
6. Share your Google Sheet with the service account email

### 4. Configure Environment Variables

Create a `.env` file or set environment variables:

```bash
# Reddit API
export REDDIT_CLIENT_ID="your_reddit_client_id"
export REDDIT_CLIENT_SECRET="your_reddit_client_secret"
export REDDIT_USER_AGENT="ProductDiscovery/1.0"

# Google Sheets
export GOOGLE_SHEET_NAME="Product Discovery Sheet"
export GOOGLE_SERVICE_ACCOUNT_FILE="service_account.json"
```

### 5. Run the System

```bash
# Full discovery process
python main.py

# Test with mock data
python main.py test

# Setup Google Sheet headers only
python main.py setup
```

## 📊 Google Sheet Format

The system creates/uses a sheet with these columns:

| title | category | videoUrl | description | date | views | source | problem |
|-------|----------|----------|-------------|------|-------|--------|---------|
| Smart Arch Support Insoles | Foot Care | https://tiktok.com/... | Great for retail workers | 2024-01-15 | 1.2M | TikTok | foot pain from standing |

## 🎯 Target Subreddits

The system monitors these subreddits for pain/problem posts:

- `r/BuyItForLife` - Durable product recommendations
- `r/Frugal` - Budget-friendly solutions
- `r/ChronicPain` - Chronic pain discussions
- `r/backpain` - Back pain specific
- `r/plantarfasciitis` - Foot pain specific
- `r/Productivity` - Work efficiency issues
- `r/Arthritis` - Joint pain discussions
- `r/ShoulderPain` - Shoulder issues
- `r/Sciatica` - Sciatica pain

## 🔧 Configuration Options

### Environment Variables

| Variable | Default | Description |
|----------|---------|-------------|
| `REDDIT_CLIENT_ID` | `your_client_id` | Reddit API client ID |
| `REDDIT_CLIENT_SECRET` | `your_client_secret` | Reddit API client secret |
| `REDDIT_USER_AGENT` | `ProductDiscovery/1.0` | Reddit API user agent |
| `GOOGLE_SHEET_NAME` | `Product Discovery Sheet` | Google Sheet name |
| `GOOGLE_SERVICE_ACCOUNT_FILE` | `service_account.json` | Path to service account file |

### Customizing Target Keywords

Edit `reddit_scraper.py` to modify the pain/problem keywords:

```python
pain_keywords = [
    'pain', 'hurt', 'ache', 'sore', 'chronic', 'help', 'recommend', 
    'suggestion', 'advice', 'problem', 'issue', 'struggle', 'difficulty',
    'fatigue', 'tired', 'exhausted', 'relief', 'solution', 'fix'
]
```

### Adding Product Categories

Edit `tiktok_matcher.py` to add new product categories:

```python
product_database = {
    'your_category': [
        {
            "title": "Your Product",
            "category": "Your Category",
            "videoUrl": "https://www.tiktok.com/@user/video/123",
            "description": "Product description",
            "views": "1.0M",
            "source": "TikTok"
        }
    ]
}
```

## 🧪 Testing

### Test Individual Components

```bash
# Test Reddit scraper
python reddit_scraper.py

# Test TikTok matcher
python tiktok_matcher.py

# Test Google Sheets updater
python update_sheet.py
```

### Run System Test

```bash
python main.py test
```

This runs the system with mock data to verify everything works.

## 🔍 How It Works

### 1. Reddit Scraping (`reddit_scraper.py`)

- Connects to Reddit API using PRAW
- Searches specified subreddits for recent posts (last 7 days)
- Filters posts containing pain/problem keywords
- Extracts problem descriptions and relevant keywords
- Returns structured problem data

### 2. Product Matching (`tiktok_matcher.py`)

- Takes extracted keywords and problem descriptions
- Matches against simulated TikTok product database
- Returns relevant products with TikTok-style metadata
- Limits results to prevent spam (max 3 products per problem)

### 3. Sheet Updates (`update_sheet.py`)

- Connects to Google Sheets using service account
- Ensures proper headers exist
- Appends new product data as rows
- Handles errors gracefully

### 4. Main Controller (`main.py`)

- Orchestrates the entire workflow
- Provides command-line options for testing and setup
- Includes comprehensive error handling and logging

## 🚨 Troubleshooting

### Reddit API Issues

**Error: `prawcore.exceptions.ResponseException: received 401 HTTP response`**
- Check your Reddit API credentials
- Ensure your app is set to "script" type
- Verify your user agent string

**Error: `prawcore.exceptions.TooManyRequests`**
- Reddit API rate limiting - wait and try again
- Consider reducing the number of subreddits or posts processed

### Google Sheets Issues

**Error: `gspread.exceptions.SpreadsheetNotFound`**
- Ensure the sheet exists and is shared with your service account email
- Check the sheet name in your environment variables

**Error: `google.auth.exceptions.DefaultCredentialsError`**
- Ensure `service_account.json` exists and is valid
- Check file permissions

### General Issues

**No problems found from Reddit**
- Reddit API might be rate-limited
- Try running with test data: `python main.py test`
- Check if subreddits are accessible

**Products not appearing in Telegram**
- Ensure your existing Telegram bot is monitoring the Google Sheet
- Check that products were actually added to the sheet
- Verify sheet permissions and format

## 📈 Scaling and Production

### For Production Use

1. **Add Real TikTok API Integration**
   - Replace simulated products with actual TikTok API calls
   - Consider TikTok's rate limits and terms of service

2. **Implement Duplicate Detection**
   - Track processed Reddit posts to avoid duplicates
   - Use database instead of in-memory tracking

3. **Add Scheduling**
   - Use cron jobs or task schedulers
   - Consider running every few hours instead of continuously

4. **Enhanced Error Handling**
   - Add retry logic for API failures
   - Implement proper logging to files
   - Add monitoring and alerting

5. **Database Integration**
   - Store processed data in a database
   - Enable better analytics and reporting

### Performance Optimization

- Use batch processing for Google Sheets updates
- Implement caching for frequently accessed data
- Add connection pooling for API calls

## 📄 License

This project is provided as-is for educational and personal use.

## 🤝 Contributing

Feel free to submit issues, feature requests, or pull requests to improve the system.

---

**Note**: This system currently simulates TikTok product searches. For production use, you'll need to integrate with actual TikTok APIs or alternative product discovery services.