#!/bin/bash

# ProductFinderBot Installation Script
echo "🧠 ProductFinderBot Installation Script"
echo "======================================="

# Check Python version
python_version=$(python3 --version 2>&1 | awk '{print $2}')
echo "✓ Python version: $python_version"

# Check if pip is available
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3 first."
    exit 1
fi

# Install dependencies
echo "📦 Installing Python dependencies..."
pip3 install -r requirements.txt

if [ $? -eq 0 ]; then
    echo "✓ Dependencies installed successfully"
else
    echo "❌ Failed to install dependencies"
    exit 1
fi

# Check if Chrome is installed (for TikTok scraping)
if command -v google-chrome &> /dev/null || command -v chromium-browser &> /dev/null; then
    echo "✓ Chrome/Chromium browser found"
else
    echo "⚠️  Chrome/Chromium not found. TikTok scraping may not work properly."
    echo "   Install Chrome: https://www.google.com/chrome/"
fi

# Create .env file if it doesn't exist
if [ ! -f .env ]; then
    echo "📝 Creating environment configuration file..."
    cp .env.example .env
    echo "✓ Created .env file from template"
    echo "⚠️  Please edit .env file with your actual API credentials"
else
    echo "✓ .env file already exists"
fi

# Check for service account file
if [ ! -f service_account.json ]; then
    echo "⚠️  service_account.json not found"
    echo "   Please download your Google service account JSON file"
    echo "   and save it as 'service_account.json' in this directory"
fi

echo ""
echo "🎯 Installation Complete!"
echo ""
echo "Next steps:"
echo "1. Edit .env file with your API credentials"
echo "2. Add your service_account.json file"
echo "3. Test the bot: python3 product_finder_bot.py test"
echo "4. Run a single scan: python3 product_finder_bot.py once"
echo ""
echo "For help, see README.md or run: python3 product_finder_bot.py --help"