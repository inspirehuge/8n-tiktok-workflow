# TikTok Positive Sentiment Monitor - Setup Guide

## Overview
This n8n workflow monitors TikTok videos from an Apify dataset, analyzes comments for positive sentiment, and sends Telegram notifications when positive mentions are found.

## Features
- ✅ Automated TikTok data fetching from Apify datasets
- ✅ Advanced positive sentiment analysis with 25+ keywords
- ✅ Rich Telegram notifications with video stats and creator info
- ✅ Scheduled execution (every 2 hours by default)
- ✅ Error handling and monitoring
- ✅ Comprehensive logging

## Prerequisites
1. **n8n instance** (self-hosted or cloud)
2. **Apify account** with TikTok dataset access
3. **Telegram Bot** for notifications
4. **TikTok data source** configured in Apify

## Setup Instructions

### 1. Import the Workflow
1. Copy the entire content from `tiktok-positive-sentiment-workflow.json`
2. In n8n, go to **Workflows** → **Import from File/URL**
3. Paste the JSON content and click **Import**

### 2. Configure Apify Integration

#### Create Apify Credentials
1. In n8n, go to **Credentials** → **Add Credential**
2. Search for "Apify" and select **Apify API**
3. Enter your Apify API token from [Apify Console](https://console.apify.com/account/integrations)
4. Name it "Apify API" and save

#### Configure Dataset
1. Open the **"Fetch TikTok Data"** node
2. Replace `YOUR_APIFY_DATASET_ID` with your actual Apify dataset ID
3. Adjust the `limit` parameter (default: 50 videos per run)

### 3. Configure Telegram Bot

#### Create Telegram Bot
1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow instructions
3. Save the **Bot Token** provided

#### Get Chat ID
1. Add your bot to a chat or group
2. Send a message to the bot
3. Visit: `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
4. Find your `chat_id` in the response

#### Create Telegram Credentials
1. In n8n, go to **Credentials** → **Add Credential**
2. Search for "Telegram" and select **Telegram API**
3. Enter your Bot Token
4. Name it "Telegram Bot API" and save

#### Configure Telegram Nodes
1. Open **"Send Telegram Notification"** node
2. Replace `YOUR_TELEGRAM_CHAT_ID` with your actual chat ID
3. Open **"Send Error Notification"** node
4. Replace `YOUR_TELEGRAM_ADMIN_CHAT_ID` with admin chat ID (can be same as above)

### 4. Configure Schedule
1. Open the **"Schedule Trigger"** node
2. Adjust the interval (default: every 2 hours)
3. Options: minutes, hours, days, weeks, months

### 5. Customize Positive Keywords
The workflow includes 25+ positive keywords by default:
- love, great, helped, amazing, awesome, fantastic
- perfect, excellent, wonderful, incredible, brilliant
- outstanding, superb, magnificent, marvelous, phenomenal
- inspiring, motivating, helpful, useful, valuable
- appreciate, grateful, thank you, thanks, blessing

To modify keywords:
1. Open **"Analyze Comments for Positive Sentiment"** node
2. Edit the `positiveKeywords` array in the JavaScript code
3. Add or remove keywords as needed

## Workflow Nodes Explained

### 1. Schedule Trigger
- **Purpose**: Automatically runs the workflow at specified intervals
- **Default**: Every 2 hours
- **Customizable**: Change frequency as needed

### 2. Fetch TikTok Data
- **Purpose**: Retrieves TikTok video data from Apify dataset
- **Configuration**: Requires Apify dataset ID and credentials
- **Output**: Raw TikTok video data with comments and metadata

### 3. Analyze Comments for Positive Sentiment
- **Purpose**: Processes video data and identifies positive comments
- **Logic**: 
  - Scans all comments for positive keywords
  - Extracts first matching positive comment
  - Compiles video and creator statistics
- **Output**: Filtered data with positive matches only

### 4. Filter Positive Results
- **Purpose**: Only processes videos with positive comments found
- **Logic**: Checks if `positiveComment` field is not empty
- **Branches**: Positive matches continue, others are logged only

### 5. Format Telegram Message
- **Purpose**: Creates rich, formatted notification message
- **Features**:
  - Emoji-rich formatting
  - Number formatting with commas
  - Verification badges for creators
  - Truncated descriptions and comments
  - Hashtags for organization

### 6. Send Telegram Notification
- **Purpose**: Sends formatted message to Telegram chat
- **Features**:
  - Markdown formatting
  - Web preview enabled
  - Non-silent notifications

### 7. Log Processing Results
- **Purpose**: Tracks workflow performance and results
- **Metrics**:
  - Total videos processed
  - Positive matches found
  - Messages sent
  - Execution timestamp

### 8. Error Handling
- **Purpose**: Catches and reports workflow errors
- **Features**:
  - Automatic error detection
  - Admin notifications
  - Detailed error information

## Sample Telegram Notification

```
🎯 Positive TikTok Mention Found!

📱 Video Details:
• URL: https://www.tiktok.com/@user/video/1234567890
• Views: 1,234,567
• Likes: 45,678
• Comments: 2,345

👤 Creator Stats: ✅
• Username: @influencer_name
• Followers: 2,345,678
• Total Likes: 12,345,678
• Total Videos: 1,234

💬 Positive Comment:
"This video helped me so much! Amazing content, thank you for sharing this valuable information!"

📝 Video Description:
Learn the top 5 productivity tips that will change your life! These simple strategies have helped thousands of people...

⏰ Detected: 1/15/2024, 3:45:23 PM

#TikTok #PositiveFeedback #SocialListening
```

## Monitoring and Maintenance

### Performance Monitoring
- Check execution logs regularly
- Monitor Apify dataset usage
- Review Telegram message delivery

### Troubleshooting Common Issues

#### No Data Retrieved
- Verify Apify dataset ID is correct
- Check Apify API credentials
- Ensure dataset has recent data

#### No Positive Matches
- Review positive keywords list
- Check comment data structure
- Verify sentiment analysis logic

#### Telegram Not Working
- Verify bot token is correct
- Check chat ID is accurate
- Ensure bot has send message permissions

#### High API Usage
- Reduce execution frequency
- Lower dataset limit per execution
- Implement data caching if needed

### Customization Options

#### Adjust Sensitivity
- Modify positive keywords list
- Change minimum comment length
- Add negative keyword filtering

#### Enhance Notifications
- Add more video metadata
- Include trending analysis
- Add custom message templates

#### Scale for Multiple Accounts
- Duplicate workflow for different datasets
- Use different Telegram channels
- Implement account-specific keywords

## Security Considerations

1. **API Keys**: Store all credentials securely in n8n credential manager
2. **Chat IDs**: Use private chats or controlled groups
3. **Data Privacy**: Respect TikTok's terms of service and user privacy
4. **Rate Limits**: Monitor API usage to avoid rate limiting

## Support and Updates

For issues or enhancements:
1. Check n8n community forums
2. Review Apify documentation
3. Test workflow with manual execution
4. Monitor execution logs for errors

## License and Compliance

Ensure compliance with:
- TikTok Terms of Service
- Apify Usage Policies  
- Telegram Bot API Guidelines
- Local data protection regulations