# Google Sheets to Telegram Bot

This Python script connects to a Google Sheet named "Koladata" and automatically sends new rows as formatted Markdown messages to a Telegram bot. It runs continuously, checking for new data every 5 minutes.

## Features

- Connects to Google Sheets using service account credentials
- Sends formatted Markdown messages to Telegram
- Tracks sent rows to avoid duplicates
- Runs in an infinite loop with 5-minute intervals
- Comprehensive logging
- Error handling and retry logic

## Requirements

- Python 3.7+
- Google Sheets API access
- Telegram Bot Token
- Service account JSON file

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Google Sheets API Setup

1. Go to the [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select an existing one
3. Enable the Google Sheets API and Google Drive API
4. Create a service account:
   - Go to "IAM & Admin" > "Service Accounts"
   - Click "Create Service Account"
   - Fill in the details and create
   - Generate a JSON key file
5. Download the JSON key file and rename it to `service_account.json`
6. Place the file in the same directory as `main.py`
7. Share your Google Sheet with the service account email (found in the JSON file)

### 3. Telegram Bot Setup

1. Create a new bot:
   - Message [@BotFather](https://t.me/botfather) on Telegram
   - Send `/newbot` command
   - Follow the instructions to create your bot
   - Save the bot token
2. Get your chat ID:
   - Start a conversation with your bot
   - Send a message to your bot
   - Visit `https://api.telegram.org/bot<YOUR_BOT_TOKEN>/getUpdates`
   - Find your chat ID in the response

### 4. Environment Configuration

1. Copy the example environment file:
   ```bash
   cp .env.example .env
   ```
2. Edit `.env` and add your credentials:
   ```
   TELEGRAM_TOKEN=your_actual_bot_token
   TELEGRAM_CHAT_ID=your_actual_chat_id
   ```

### 5. Google Sheet Setup

Make sure your Google Sheet:
- Is named "Koladata"
- Has a worksheet named "Sheet1"
- Has the following columns in order:
  1. title
  2. category
  3. video_url
  4. description
  5. date
  6. views
  7. source

## Usage

Run the script:

```bash
python main.py
```

The script will:
1. Connect to your Google Sheet
2. Check for new rows every 5 minutes
3. Send each new row as a formatted message to your Telegram bot
4. Keep track of sent rows to avoid duplicates
5. Continue running until manually stopped (Ctrl+C)

## Message Format

Each row is sent as a Markdown-formatted message with:
- Entry number
- All field values with emojis
- Timestamp of when the message was sent

Example:
```
📊 **New Data Entry #2**

🏷️ **Title:** Sample Video Title
📂 **Category:** Education
🎥 **Video URL:** https://example.com/video
📝 **Description:** This is a sample description
📅 **Date:** 2024-01-15
👀 **Views:** 1000
🔗 **Source:** YouTube

---
*Sent at 2024-01-15 14:30:25*
```

## Logging

The script provides comprehensive logging with timestamps for:
- Connection status
- New rows processed
- Messages sent
- Errors and retries

## Error Handling

The script includes robust error handling for:
- Google Sheets API connection issues
- Telegram API failures
- Network connectivity problems
- Invalid data formats

## File Structure

```
.
├── main.py              # Main script
├── requirements.txt     # Python dependencies
├── .env                 # Environment variables (create from .env.example)
├── .env.example         # Environment template
├── service_account.json # Google service account credentials (you need to add this)
└── README.md           # This file
```

## Troubleshooting

### Common Issues

1. **"No module named 'gspread'"**
   - Run `pip install -r requirements.txt`

2. **"Failed to setup Google Sheets connection"**
   - Check that `service_account.json` exists and is valid
   - Ensure the Google Sheets API is enabled
   - Verify the sheet is shared with the service account email

3. **"TELEGRAM_TOKEN and TELEGRAM_CHAT_ID must be set"**
   - Check that `.env` file exists and contains valid values
   - Ensure there are no extra spaces in the environment variables

4. **"Failed to open worksheet"**
   - Verify the sheet name is exactly "Koladata"
   - Check that the worksheet name is exactly "Sheet1"
   - Ensure the service account has access to the sheet

## License

MIT License - feel free to modify and use as needed.