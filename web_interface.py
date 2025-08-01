#!/usr/bin/env python3
"""
Simple web interface for manually triggering the TikTok Viral Bot
"""

from flask import Flask, render_template, jsonify, request
import subprocess
import threading
import logging
import os
from datetime import datetime

app = Flask(__name__)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Global variable to track if bot is running
bot_running = False
last_run_time = None
last_run_status = None

@app.route('/')
def index():
    """Main page with run button"""
    return render_template('index.html', 
                         last_run_time=last_run_time,
                         last_run_status=last_run_status,
                         bot_running=bot_running)

@app.route('/run_bot', methods=['POST'])
def run_bot():
    """Manually trigger the bot"""
    global bot_running, last_run_time, last_run_status
    
    if bot_running:
        return jsonify({'status': 'error', 'message': 'Bot is already running'})
    
    try:
        bot_running = True
        last_run_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        # Run the bot in a separate thread
        def run_bot_thread():
            global bot_running, last_run_status
            try:
                result = subprocess.run(['python3', 'tiktok_viral_bot.py', '--manual'], 
                                      capture_output=True, text=True, timeout=300)
                if result.returncode == 0:
                    last_run_status = 'Success'
                else:
                    last_run_status = f'Error: {result.stderr}'
            except subprocess.TimeoutExpired:
                last_run_status = 'Timeout (5 minutes)'
            except Exception as e:
                last_run_status = f'Error: {str(e)}'
            finally:
                bot_running = False
        
        thread = threading.Thread(target=run_bot_thread)
        thread.daemon = True
        thread.start()
        
        return jsonify({'status': 'success', 'message': 'Bot started successfully'})
        
    except Exception as e:
        bot_running = False
        return jsonify({'status': 'error', 'message': str(e)})

@app.route('/status')
def status():
    """Get current bot status"""
    return jsonify({
        'running': bot_running,
        'last_run_time': last_run_time,
        'last_run_status': last_run_status
    })

@app.route('/logs')
def logs():
    """View recent logs"""
    try:
        if os.path.exists('bot.log'):
            with open('bot.log', 'r') as f:
                lines = f.readlines()
                # Return last 50 lines
                recent_logs = ''.join(lines[-50:])
                return f'<pre>{recent_logs}</pre>'
        else:
            return '<pre>No logs found</pre>'
    except Exception as e:
        return f'<pre>Error reading logs: {e}</pre>'

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)