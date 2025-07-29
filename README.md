# TikTok Product Scraper to Telegram Workflow

This n8n workflow automatically scrapes TikTok videos using Apify, filters for product-related content, and sends formatted notifications to Telegram with video thumbnails and engagement stats.

## Features

- ⏰ **Automated Scraping**: Runs every hour using cron trigger
- 🔍 **Smart Filtering**: Filters videos by product-related keywords
- 📱 **Rich Telegram Messages**: Sends both text and photo messages
- 📊 **Engagement Stats**: Includes likes, views, shares, and comments
- 🖼️ **Video Thumbnails**: Sends cover images as photo previews
- 🚨 **Error Handling**: Notifications for workflow failures

## Prerequisites

1. **n8n Instance**: Self-hosted or cloud n8n installation
2. **Apify Account**: Free tier available at [apify.com](https://apify.com)
3. **Telegram Bot**: Created via [@BotFather](https://t.me/botfather)
4. **Telegram Chat ID**: Your personal or group chat ID

## Setup Instructions

### 1. Create Apify Credentials

1. Go to your Apify account settings
2. Generate an API token
3. In n8n, create new credentials:
   - **Type**: HTTP Header Auth
   - **Name**: `Apify API Token`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer YOUR_APIFY_TOKEN`

### 2. Create Telegram Bot Credentials

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Create a new bot with `/newbot`
3. Get your bot token
4. In n8n, create new credentials:
   - **Type**: Telegram API
   - **Name**: `Telegram Bot Token`
   - **Access Token**: `YOUR_BOT_TOKEN`

### 3. Get Telegram Chat ID

**Method 1: Using Bot**
1. Start a chat with your bot
2. Send any message
3. Visit: `https://api.telegram.org/botYOUR_BOT_TOKEN/getUpdates`
4. Find your chat ID in the response

**Method 2: Using @userinfobot**
1. Message [@userinfobot](https://t.me/userinfobot)
2. It will reply with your user ID

### 4. Set Environment Variables

In your n8n instance, set the following environment variable:
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID (e.g., `123456789`)

### 5. Import Workflow

1. Copy the contents of `tiktok-telegram-workflow.json`
2. In n8n, go to **Workflows** → **Import from JSON**
3. Paste the JSON content
4. Save the workflow

### 6. Configure Credentials

1. Open the imported workflow
2. For each node with credentials, select the appropriate credential:
   - **Apify nodes**: Select "Apify API Token"
   - **Telegram nodes**: Select "Telegram Bot Token"

## Workflow Components

### Nodes Overview

1. **Cron Trigger**: Runs every hour
2. **Apify TikTok Scraper**: Initiates scraping job
3. **Wait for Completion**: Monitors scraping progress
4. **Get Scraping Results**: Retrieves scraped data
5. **Filter Product Videos**: Filters by keywords
6. **Split Into Batches**: Processes videos individually
7. **Set Message Text**: Formats Telegram messages
8. **Send Telegram Message**: Sends text notification
9. **Send Telegram Photo**: Sends thumbnail image
10. **Merge Results**: Combines outputs
11. **Error Handler**: Manages failures

### Hashtags Monitored

- `#tiktokmademebuyit`
- `#productreview`
- `#amazonfinds`
- `#musthave`

### Product Keywords Filter

The workflow filters videos containing these keywords:
- buy, purchase, product, review, recommend
- amazon, link in bio, must have, obsessed
- game changer, worth it, money, price
- deal, sale, discount, shopping, haul
- find, favorite, love this, need this
- get this, order, checkout, cart

## Message Format

### Text Message
```
🎵 *TikTok Product Alert!*

📝 *Caption:*
[Video caption text]

🏷️ *Hashtags:*
[Video hashtags]

🔗 *Watch Video:*
[TikTok video link]

📊 *Engagement Stats:*
👍 Likes: [formatted number]
👁️ Views: [formatted number]
🔄 Shares: [formatted number]
💬 Comments: [formatted number]

👤 *Creator:* @[username]

#TikTokFinds #ProductReview #MustHave
```

### Photo Message
- Video thumbnail image
- Simplified caption with video details

## Customization

### Modify Hashtags
Edit the `hashtags` parameter in the "Apify TikTok Scraper" node:
```json
{
  "name": "hashtags",
  "value": "[\"#yourcustomhashtag\", \"#another\"]"
}
```

### Adjust Keywords
Modify the `productKeywords` array in the "Filter Product Videos" node.

### Change Schedule
Update the cron trigger interval:
- Every 30 minutes: `hoursInterval: 0.5`
- Every 2 hours: `hoursInterval: 2`
- Daily at 9 AM: Use cron expression `0 9 * * *`

### Modify Message Format
Edit the message templates in the "Set Message Text" node.

## Troubleshooting

### Common Issues

1. **No videos found**: Check if hashtags are popular and recent
2. **Apify timeout**: Increase `maxWaitTime` in wait node
3. **Telegram errors**: Verify bot token and chat ID
4. **Rate limiting**: Reduce scraping frequency

### Debug Mode

1. Enable workflow execution logs
2. Test individual nodes using "Execute Node"
3. Check Apify dashboard for scraping job status

### Error Notifications

The workflow includes error handling that sends Telegram notifications when:
- Apify scraping fails
- Timeout occurs
- Invalid credentials
- Network issues

## Limitations

- **Apify Free Tier**: Limited monthly usage
- **TikTok Rate Limits**: May affect scraping frequency
- **Telegram Limits**: 30 messages per second per bot
- **Image Loading**: Some thumbnails may fail to load

## Contributing

Feel free to enhance this workflow by:
- Adding more social platforms
- Improving keyword filtering
- Adding sentiment analysis
- Creating analytics dashboards

## License

This workflow is provided as-is for educational and personal use. Ensure compliance with TikTok's terms of service and applicable laws when scraping content.

## Support

For issues and questions:
1. Check n8n community forum
2. Review Apify documentation
3. Verify Telegram Bot API limits
4. Test individual workflow components