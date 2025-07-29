# TikTok Product Tracker - n8n Workflow

This n8n workflow automatically monitors TikTok for product-related content and sends notifications to Telegram with video details and thumbnails.

## 🚀 Features

- **Automated TikTok Scraping**: Uses Apify's TikTok scraper to fetch videos from popular product hashtags
- **Smart Filtering**: Filters videos based on product-related keywords in text and hashtags
- **Telegram Notifications**: Sends formatted messages with video details and thumbnails
- **Batch Processing**: Processes videos one at a time to avoid rate limits
- **Scheduled Execution**: Runs every hour automatically

## 📋 Prerequisites

1. **n8n Instance**: Running n8n (cloud or self-hosted)
2. **Apify Account**: For TikTok scraping
3. **Telegram Bot**: For sending notifications

## 🔧 Setup Instructions

### 1. Import the Workflow

1. Download the `tiktok-product-tracker.json` file
2. In n8n, go to **Workflows** → **Import from File**
3. Select the downloaded JSON file
4. Click **Import**

### 2. Configure Credentials

#### Apify API Credentials
1. Go to [Apify Console](https://console.apify.com/)
2. Navigate to **Settings** → **Integrations** → **API tokens**
3. Create a new token or copy existing one
4. In n8n, go to **Credentials** → **Add Credential** → **Apify API**
5. Enter your API token
6. Name it `apify_credentials`

#### Telegram Bot Credentials
1. Create a bot via [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Copy the bot token
4. Get your chat ID by messaging [@userinfobot](https://t.me/userinfobot)
5. In n8n, go to **Credentials** → **Add Credential** → **Telegram API**
6. Enter your bot token
7. Name it `telegram_credentials`

### 3. Set Environment Variables

In your n8n instance, set the following environment variable:
- `TELEGRAM_CHAT_ID`: Your Telegram chat ID (where notifications will be sent)

### 4. Customize Hashtags (Optional)

In the **Apify TikTok Scraper** node, you can modify the hashtags being monitored:

```json
"hashtags": ["tiktokmademebuyit", "amazonfinds", "aliexpressfinds", "viralproduct", "musthave"]
```

### 5. Adjust Filtering Keywords (Optional)

In the **Filter Product Videos** node, you can modify the product-related keywords:

```
product|buy|musthave|wishlist|finds|review|unboxing|haul|amazon|aliexpress|organizerfinds|gymfinds|beautyfinds|viralproduct|testedontiktok|recommendation|worthit
```

## 🔄 Workflow Components

1. **Schedule Trigger**: Runs every hour
2. **Apify TikTok Scraper**: Fetches videos from specified hashtags
3. **Filter Product Videos**: Filters videos based on product keywords
4. **Split In Batches**: Processes videos one at a time
5. **Send Telegram Message**: Sends formatted product notification
6. **Check If Image Available**: Verifies thumbnail availability
7. **Send Telegram Photo**: Sends video thumbnail
8. **Merge Results**: Combines message and photo results
9. **Check Batch Complete**: Manages batch processing loop
10. **Send Completion Message**: Notifies when scan is complete

## 📱 Telegram Message Format

Each product notification includes:
- 🔥 Attention-grabbing header
- 💬 Video text content
- 🏷️ Relevant hashtags
- 🎥 Direct link to TikTok video
- 📊 Engagement stats (likes, comments, shares, views)
- 📸 Video thumbnail (if available)

## ⚙️ Configuration Options

### Adjust Scan Frequency
Modify the **Schedule Trigger** node to change how often the workflow runs:
- Every 30 minutes: `{"field": "minutes", "value": 30}`
- Every 2 hours: `{"field": "hours", "value": 2}`
- Daily: `{"field": "days", "value": 1}`

### Change Results Per Page
In the **Apify TikTok Scraper** node, modify `resultsPerPage` (default: 50)

### Batch Size
In the **Split In Batches** node, modify `batchSize` (default: 1)

## 🛠️ Troubleshooting

### Common Issues

1. **No videos found**: Check if hashtags are popular and contain product content
2. **Apify rate limits**: Reduce `resultsPerPage` or increase scan interval
3. **Telegram not working**: Verify bot token and chat ID
4. **Filtering too strict**: Adjust keyword regex patterns

### Debug Mode

Enable debug mode in n8n to see detailed execution logs and troubleshoot issues.

## 📊 Expected Results

- **Videos per scan**: 10-50 (depending on hashtag popularity)
- **Filtered results**: 20-80% of scraped videos (varies by hashtag)
- **Notifications**: 1 message + 1 photo per qualifying video
- **Execution time**: 2-5 minutes per scan

## 🔒 Security Notes

- Keep your Apify API token secure
- Use environment variables for sensitive data
- Consider using Telegram bot with restricted permissions
- Monitor API usage to avoid unexpected charges

## 📈 Optimization Tips

1. **Focus hashtags**: Use more specific product-related hashtags for better results
2. **Keyword tuning**: Regularly update filtering keywords based on trends
3. **Rate limiting**: Adjust batch size and delays to respect API limits
4. **Storage**: Clean up old execution data regularly

## 🆘 Support

If you encounter issues:
1. Check n8n execution logs
2. Verify all credentials are correctly configured
3. Test individual nodes to isolate problems
4. Check Apify and Telegram API status pages

## 📄 License

This workflow is provided as-is for educational and personal use. Please respect TikTok's terms of service and rate limits when using this automation.