import os
import sys

# Add a shim for imghdr if it's not available (for Python 3.13+)
try:
    import imghdr
except ModuleNotFoundError:
    # Create a simple imghdr shim
    class ImghdrShim:
        @staticmethod
        def what(file, h=None):
            # Simple implementation that checks common image formats
            if h is None:
                with open(file, 'rb') as f:
                    h = f.read(32)
            
            if h.startswith(b'\xff\xd8\xff'):
                return 'jpeg'
            elif h.startswith(b'\x89PNG\r\n\x1a\n'):
                return 'png'
            elif h.startswith(b'GIF87a') or h.startswith(b'GIF89a'):
                return 'gif'
            elif h.startswith(b'BM'):
                return 'bmp'
            elif h.startswith(b'RIFF') and h[8:12] == b'WEBP':
                return 'webp'
            return None
    
    # Add to sys.modules so telegram can import it
    sys.modules['imghdr'] = ImghdrShim()

import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackContext
from flask import Flask
from threading import Thread

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Initialize Flask app for health checks
app = Flask(__name__)

@app.route('/')
def home():
    return "Telegram bot is running!"

# Get environment variables
TOKEN = os.getenv("TOKEN")
ALLOWED_GROUP_ID = int(os.getenv("ALLOWED_GROUP_ID", "0"))
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://ryan85501.github.io/Shwe-Pat-Tee/")
PORT = int(os.environ.get('PORT', 5000))

# /start command
def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id != ALLOWED_GROUP_ID:
        update.message.reply_text("❌ This bot only works inside the group.")
        return
    update.message.reply_text("✅ Bot is active in this group!")

# /open command → launches Mini App
def open_app(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id != ALLOWED_GROUP_ID:
        update.message.reply_text("❌ This bot only works inside the group.")
        return

    keyboard = [
        [InlineKeyboardButton("🚀 Open App", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    update.message.reply_text("Click below to open the app:", reply_markup=reply_markup)

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def run_bot():
    if not TOKEN:
        raise ValueError("❌ TOKEN is missing. Set it in Render Environment Variables.")

    # Use the older Updater pattern instead of Application
    updater = Updater(TOKEN, use_context=True)
    
    # Get the dispatcher to register handlers
    dispatcher = updater.dispatcher

    # Register command handlers
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(CommandHandler("open", open_app))

    # Start the Bot with polling
    updater.start_polling()
    
    # Run the bot until you press Ctrl-C
    updater.idle()

if __name__ == "__main__":
    # Start Flask in a separate thread for health checks
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run the bot
    run_bot()
