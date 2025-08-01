#!/bin/bash

echo "🤖 Setting up TikTok Viral Bot..."

# Check if Python 3 is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is required but not installed."
    exit 1
fi

# Create virtual environment if it doesn't exist
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔄 Activating virtual environment..."
source venv/bin/activate

# Install Python dependencies
echo "📚 Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Install Playwright browsers
echo "🌐 Installing Playwright browsers..."
playwright install chromium

# Create templates directory if it doesn't exist
mkdir -p templates

# Make scripts executable
chmod +x setup.sh
chmod +x run_bot.sh
chmod +x run_web.sh

echo "✅ Setup complete!"
echo ""
echo "📖 Usage:"
echo "  • Run persistent bot (every 15 min): ./run_bot.sh"
echo "  • Run web interface with manual button: ./run_web.sh"
echo "  • Manual single run: python3 tiktok_viral_bot.py --manual"
echo ""
echo "🌐 Web interface will be available at: http://localhost:5000"