# TikTok to Telegram Automation - n8n Workflow

This is a fully working n8n workflow that automatically fetches trending TikTok product videos daily and sends them to a Telegram channel with rich formatting and preview capabilities.

## Features

✅ **Daily Automation**: Runs automatically every day at 9 AM  
✅ **TikTok Scraping**: Uses Apify's reliable TikTok scraper API  
✅ **Smart Filtering**: Focuses on trending product videos  
✅ **Duplicate Prevention**: Avoids reposting the same videos  
✅ **Rich Telegram Messages**: Includes thumbnails, descriptions, stats, and links  
✅ **Batch Processing**: Handles multiple videos efficiently  
✅ **Rate Limiting**: Prevents API rate limit issues  
✅ **Web Preview**: Enables link previews in Telegram  

## Prerequisites

### 1. Apify Account
- Sign up at [Apify.com](https://apify.com)
- Get your API token from the Apify Console
- The workflow uses the free TikTok scraper: `clockworks~free-tiktok-scraper`

### 2. Telegram Bot
- Create a bot via [@BotFather](https://t.me/botfather) on Telegram
- Get your bot token (format: `123456789:ABCdefGHIjklMNOpqrSTUvwxYZ`)
- Get your chat ID (can be a channel, group, or private chat)

### 3. n8n Instance
- Self-hosted n8n or n8n Cloud account
- Access to create workflows and credentials

## Setup Instructions

### Step 1: Import the Workflow

1. Copy the contents of `tiktok-telegram-automation.json`
2. In n8n, go to **Workflows** → **Import from File** or **Import from URL**
3. Paste the JSON content and import

### Step 2: Configure Credentials

#### Apify API Credentials
1. Go to **Credentials** in n8n
2. Create new **HTTP Header Auth** credential
3. Set:
   - **Name**: `Apify API`
   - **Header Name**: `Authorization`
   - **Header Value**: `Bearer YOUR_APIFY_TOKEN`

#### Telegram Variables
1. Go to **Settings** → **Variables** in n8n
2. Add these variables:
   - `telegram_bot_token`: Your Telegram bot token
   - `telegram_chat_id`: Your chat/channel ID

### Step 3: Test the Workflow

1. Open the imported workflow
2. Click on the **Daily Trigger** node
3. Click **Execute Workflow** to test manually
4. Check each node's output to ensure everything works
5. Verify messages appear in your Telegram chat

### Step 4: Activate Automation

1. Toggle the workflow to **Active**
2. The workflow will now run daily at 9 AM automatically

## Workflow Structure

```
Daily Trigger (9 AM)
    ↓
Fetch TikTok Data (HTTP Request to Apify)
    ↓
Load Cache (Get previously processed videos)
    ↓
Split Into Batches (Process 5 videos at a time)
    ↓
Filter Duplicates (Skip already processed videos)
    ↓
Format Video Data (Extract relevant fields)
    ↓
Format Telegram Message (Create rich message)
    ↓
Send to Telegram (Main message with preview)
    ↓
Check Thumbnail (If thumbnail exists)
    ↓
Send Thumbnail (Optional thumbnail image)
    ↓
Update Cache (Mark video as processed)
    ↓
Rate Limit Delay (2 second delay between messages)
```

## Configuration Options

### Search Queries
The workflow searches for these trending product keywords:
- "trending products"
- "viral products"
- "amazon finds"
- "tiktok made me buy it"

To modify search terms, edit the `Fetch TikTok Data` node's `searchQueries` parameter.

### Batch Size
Currently processes 5 videos at a time. Change the `batchSize` in the `Split Into Batches` node.

### Schedule
Runs daily at 9 AM. Modify the cron expression in the `Daily Trigger` node:
- `0 9 * * *` = 9 AM daily
- `0 */6 * * *` = Every 6 hours
- `0 12 * * 1` = Mondays at noon

### Message Format
The Telegram message includes:
- 🔥 Trending indicator
- 👤 Username
- 📝 Description (truncated to 200 chars)
- 📊 Stats (views, likes, shares)
- 🔗 Direct TikTok link
- 🎬 Inline button to watch video

## Troubleshooting

### Common Issues

1. **No videos fetched**
   - Check Apify API credentials
   - Verify the TikTok scraper is working
   - Try different search queries

2. **Messages not sending to Telegram**
   - Verify bot token and chat ID
   - Check if bot has permission to post in the channel
   - Ensure variables are set correctly

3. **Duplicate videos appearing**
   - Check the cache mechanism
   - Verify the `Filter Duplicates` node logic
   - Clear workflow static data if needed

4. **Rate limiting errors**
   - Increase delay in `Rate Limit Delay` node
   - Reduce batch size
   - Check API rate limits

### Debug Steps

1. **Test individual nodes**: Execute each node separately to identify issues
2. **Check node outputs**: Use the data inspector to verify data flow
3. **Review execution logs**: Check workflow execution history for errors
4. **Test with smaller batches**: Reduce `resultsPerQuery` for testing

## API Data Structure

The workflow handles various TikTok data field variations:

```json
{
  "id": "video_id",
  "authorMeta": { "name": "username" },
  "author": { "uniqueId": "username" },
  "text": "description",
  "desc": "description",
  "webVideoUrl": "video_url",
  "videoUrl": "video_url",
  "covers": ["thumbnail_url"],
  "videoMeta": { "coverUrl": "thumbnail_url" },
  "playCount": 12345,
  "stats": { "playCount": 12345, "diggCount": 123, "shareCount": 45 }
}
```

## Security Notes

- Store API tokens securely using n8n credentials
- Use environment variables for sensitive data
- Regularly rotate API keys
- Monitor API usage to avoid unexpected charges

## Support

For issues with:
- **n8n workflow**: Check n8n community forums
- **Apify scraping**: Contact Apify support
- **Telegram Bot API**: Reference Telegram Bot API documentation

## License

This workflow is provided as-is for educational and automation purposes. Ensure compliance with TikTok's terms of service and API usage policies.