#!/bin/bash

echo "🌐 Starting TikTok Viral Bot Web Interface..."
echo "Web interface will be available at: http://localhost:5000"
echo "Press Ctrl+C to stop."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run the web interface
python3 web_interface.py