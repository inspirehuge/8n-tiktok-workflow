# TikTok Product Finder Workflow

This n8n workflow automatically monitors TikTok for product-related content and sends notifications to Telegram when potential product videos are found.

## Workflow Overview

The workflow consists of 5 main nodes:

1. **Set Hashtag Input** - Defines the hashtag to monitor (`#tiktokmademebuyit`)
2. **Fetch TikTok Data** - Uses Apify to scrape TikTok data based on the hashtag
3. **Filter Products** - Filters content using product-related keywords
4. **Split In Batches** - Processes results one by one
5. **Send Telegram Message** - Sends formatted notifications to Telegram

## Setup Instructions

### Prerequisites
- n8n instance (self-hosted or cloud)
- Apify account with API key
- Telegram bot token and chat ID

### Configuration Steps

1. **Import the Workflow**
   - Import the `tiktok-product-finder-workflow.json` file into your n8n instance

2. **Configure Apify Integration**
   - Create an Apify account and get your API key
   - Set up the "Apify API Key" credential in n8n
   - Update the `workflowId` parameter in the "Fetch TikTok Data" node to match your TikTok scraping workflow

3. **Configure Telegram Bot**
   - Create a Telegram bot using [@BotFather](https://t.me/botfather)
   - Get your bot token
   - Get your chat ID (you can use [@userinfobot](https://t.me/userinfobot))
   - Replace `<YOUR_BOT_TOKEN>` and `<YOUR_CHAT_ID>` in the "Send Telegram Message" node

4. **Customize Keywords (Optional)**
   - Edit the `keywords` array in the "Filter Products" node to add/remove product-related terms
   - Current keywords include: product, buy, musthave, amazon, review, unboxing, etc.

## Product Detection Keywords

The workflow filters TikTok content using these categories of keywords:

- **General Product Terms**: product, buy, musthave, wishlist, finds, review, unboxing, haul
- **Platform Specific**: amazon, amazonfinds, aliexpress, bestbuy, shopee
- **Category Specific**: homefinds, kitchenfinds, skincarefinds, beautyfinds, gymfinds
- **Viral Terms**: tiktokmademebuyit, viralproduct, testedontiktok, beforeandafter

## Message Format

When a product video is detected, the Telegram message includes:
- 🔥 Notification header
- 💬 Video text/caption
- 🎥 Direct link to the TikTok video
- 🏷️ Associated hashtags

## Customization Options

### Change Monitored Hashtag
Edit the `functionCode` in the "Set Hashtag Input" node:
```javascript
return [
  { json: { hashtag: 'your-hashtag-here', type: 'hashtag' } }
];
```

### Add Multiple Hashtags
Modify the input to include multiple hashtags:
```javascript
return [
  { json: { hashtag: 'tiktokmademebuyit', type: 'hashtag' } },
  { json: { hashtag: 'amazonfinds', type: 'hashtag' } },
  { json: { hashtag: 'musthaves', type: 'hashtag' } }
];
```

### Adjust Filtering Sensitivity
Modify the filtering logic in the "Filter Products" node to be more or less strict with keyword matching.

## Scheduling

To run this workflow automatically:
1. Add a "Cron" trigger node at the beginning
2. Set your desired schedule (e.g., every hour, every 30 minutes)
3. Connect it to the "Set Hashtag Input" node

## Troubleshooting

### Common Issues
1. **Apify API Errors**: Ensure your API key is correct and you have sufficient credits
2. **Telegram Not Working**: Verify bot token and chat ID are correct
3. **No Results**: Check if the hashtag exists and has recent content
4. **Rate Limiting**: Add delays between requests if needed

### Debug Tips
- Test each node individually using the "Execute Node" feature
- Check the execution logs for error messages
- Verify data structure between nodes using the data inspector

## Legal Considerations

- Respect TikTok's terms of service
- Be mindful of rate limits and API usage
- Consider privacy implications when processing user content
- Ensure compliance with applicable data protection regulations