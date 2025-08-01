# 🔥 TikTok Viral Product Scanner

Automatically scans TikTok for viral product videos using popular hashtags and sends notifications to your Telegram channel.

**TikTok'ta ürünle ilgili popüler etiketleri saatlik olarak tarar, yeni viral olmaya başlayan videoları tespit eder ve Telegram'a gönderir.**

## ✨ Features

- 🎯 **Smart Hashtag Monitoring**: Tracks multiple product-related hashtags
- 🚀 **Viral Detection**: Identifies videos with high engagement and recent posting times
- 📱 **Telegram Integration**: Sends formatted notifications with video links
- ⏰ **Automated Scheduling**: Runs scans at configurable intervals
- 📊 **Comprehensive Logging**: Tracks all activities and errors
- 🔧 **Easy Configuration**: JSON-based settings management
- 🛡️ **Error Handling**: Robust error handling and recovery mechanisms

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Up Telegram Bot

1. Create a new bot by messaging [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the instructions
3. Save your bot token (looks like `123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ`)
4. Add your bot to a channel or group and make it an admin
5. Get your chat ID:
   - For channels: Use the channel username (e.g., `@mychannel`) or numeric ID
   - For groups: Use a bot like [@userinfobot](https://t.me/userinfobot)

### 3. Configure the Scanner

Edit `config.json` with your settings:

```json
{
  "telegram_bot_token": "YOUR_BOT_TOKEN_HERE",
  "telegram_chat_id": "@your_channel_or_chat_id",
  "hashtags": [
    "tiktokmademebuyit",
    "amazonfinds",
    "viralproducts",
    "musthaveproducts"
  ],
  "min_views": 10000,
  "max_age_hours": 1,
  "scan_interval_minutes": 60
}
```

### 4. Run the Scanner

**Test run (single scan):**
```bash
python run_once.py
```

**Continuous monitoring:**
```bash
python scheduler.py
```

## 📁 Project Structure

```
tiktok-viral-scanner/
├── tiktok_scanner.py      # Main scanner logic
├── scheduler.py           # Automated scheduling
├── run_once.py           # Single run for testing
├── config.json           # Configuration settings
├── requirements.txt      # Python dependencies
├── README.md            # This file
├── tiktok_scanner.log   # Scanner logs (created automatically)
└── scheduler.log        # Scheduler logs (created automatically)
```

## ⚙️ Configuration Options

| Setting | Description | Default |
|---------|-------------|---------|
| `telegram_bot_token` | Your Telegram bot token | Required |
| `telegram_chat_id` | Target chat/channel ID | Required |
| `hashtags` | List of hashtags to monitor | See config.json |
| `min_views` | Minimum views for viral detection | 10000 |
| `max_age_hours` | Maximum video age in hours | 1 |
| `scan_interval_minutes` | Minutes between scans | 60 |
| `max_videos_per_hashtag` | Videos to check per hashtag | 20 |
| `rate_limit_seconds` | Delay between requests | 2 |

## 🏷️ Popular Product Hashtags

The scanner comes pre-configured with these viral product hashtags:

- `tiktokmademebuyit` - Products that went viral on TikTok
- `amazonfinds` - Amazon product discoveries
- `viralproducts` - Generally viral products
- `musthaveproducts` - Essential/trending products
- `gadgettok` - Tech gadgets and tools
- `buyitnow` - Impulse purchase products
- `problemSolved` - Problem-solving products
- `usefulgadgets` - Practical gadgets
- `aliexpressfinds` - AliExpress discoveries
- `shopwithme` - Shopping experience videos
- `founditonamazon` - Amazon product finds
- `productreview` - Product review videos

## 🔧 Environment Variables

Instead of `config.json`, you can use environment variables:

```bash
export TELEGRAM_BOT_TOKEN="your_bot_token"
export TELEGRAM_CHAT_ID="your_chat_id"
```

## 📱 Telegram Message Format

The bot sends beautifully formatted messages like this:

```
🔥 New Viral Product Video!

📱 Description: This gadget will change your life!
👤 Creator: @productguru
👁️ Views: 50,000
🏷️ Hashtag: #tiktokmademebuyit
🕒 Posted: 2024-01-15 14:30

🔗 Watch Video

#ViralProducts #TikTokFinds
```

## 🚨 Troubleshooting

### Common Issues

**"Configuration error: Telegram bot token and chat ID must be configured"**
- Make sure your `config.json` has valid `telegram_bot_token` and `telegram_chat_id`
- Or set the environment variables `TELEGRAM_BOT_TOKEN` and `TELEGRAM_CHAT_ID`

**"All API endpoints failed for hashtag"**
- TikTok may be blocking requests or have changed their API
- Try running with fewer hashtags or increase delays
- Check your internet connection

**"Failed to send Telegram message"**
- Verify your bot token is correct
- Make sure the bot is added to your channel/group as an admin
- Check if your chat ID is correct (should start with @ for channels or be numeric)

**No videos found**
- Lower the `min_views` threshold in config
- Increase `max_age_hours` to catch older videos
- Try different hashtags

### Logs

Check the log files for detailed information:
- `tiktok_scanner.log` - Scanner activities and errors
- `scheduler.log` - Scheduling activities

### Rate Limiting

If you're getting rate limited:
1. Increase `rate_limit_seconds` in config
2. Reduce the number of hashtags
3. Increase `scan_interval_minutes`

## 🔄 Running as a Service

### Linux (systemd)

Create `/etc/systemd/system/tiktok-scanner.service`:

```ini
[Unit]
Description=TikTok Viral Product Scanner
After=network.target

[Service]
Type=simple
User=your_username
WorkingDirectory=/path/to/tiktok-viral-scanner
ExecStart=/usr/bin/python3 scheduler.py
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

Enable and start:
```bash
sudo systemctl enable tiktok-scanner
sudo systemctl start tiktok-scanner
```

### Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.9-slim

WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["python", "scheduler.py"]
```

Build and run:
```bash
docker build -t tiktok-scanner .
docker run -d --name tiktok-scanner tiktok-scanner
```

## 📊 Monitoring

The scanner provides detailed logging:

- **INFO**: Normal operations, successful scans
- **WARNING**: Non-critical issues, API fallbacks
- **ERROR**: Failed requests, parsing errors

Monitor logs in real-time:
```bash
tail -f tiktok_scanner.log
```

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## ⚠️ Disclaimer

This tool is for educational and personal use only. Please respect TikTok's Terms of Service and rate limits. The authors are not responsible for any misuse of this tool.

## 🆘 Support

If you encounter any issues or have questions:

1. Check the [Troubleshooting](#-troubleshooting) section
2. Review the log files for error details
3. Open an issue on GitHub with:
   - Your configuration (remove sensitive tokens)
   - Relevant log entries
   - Steps to reproduce the problem

---

**Happy hunting for viral products! 🛍️✨**