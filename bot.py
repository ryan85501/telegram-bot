import os
import logging
import asyncio
import telegram
print(f"Telegram bot version: {telegram.__version__}")
from queue import Queue
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Updater, CommandHandler, CallbackContext, Application
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
async def start(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id != ALLOWED_GROUP_ID:
        await update.message.reply_text("❌ This bot only works inside the group.")
        return
    await update.message.reply_text("✅ Bot is active in this group!")

# /open command → launches Mini App
async def open_app(update: Update, context: CallbackContext):
    chat_id = update.effective_chat.id
    if chat_id != ALLOWED_GROUP_ID:
        await update.message.reply_text("❌ This bot only works inside the group.")
        return

    keyboard = [
        [InlineKeyboardButton("🚀 Open App", web_app=WebAppInfo(url=MINI_APP_URL))]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text("Click below to open the app:", reply_markup=reply_markup)

def run_flask():
    app.run(host='0.0.0.0', port=PORT, debug=False, use_reloader=False)

def run_bot():
    if not TOKEN:
        raise ValueError("❌ TOKEN is missing. Set it in Render Environment Variables.")

    # Create an update queue
    update_queue = Queue()
    
    # Create updater with the queue
    updater = Updater(TOKEN, update_queue=update_queue)
    
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

