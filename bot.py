# at the very top of bot.py
import imghdr_pure as imghdr
import sys
sys.modules['imghdr'] = imghdr

import os
import logging
import threading
from flask import Flask
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

# === Telegram Bot Token ===
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")  # set in Render env vars

# === Logging ===
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# === Flask server for Render health check ===
app = Flask(__name__)

@app.route("/")
def home():
    return "Bot is running!"

# === Telegram Bot Handlers ===
def start(update, context):
    update.message.reply_text("Hello 👋 I am alive on Render!")

def echo(update, context):
    update.message.reply_text(update.message.text)

def run_telegram_bot():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)

    dp = updater.dispatcher
    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

    # Start polling
    updater.start_polling()
    updater.idle()

# === Main entry ===
if __name__ == "__main__":
    # Start Telegram bot in separate thread
    threading.Thread(target=run_telegram_bot, daemon=True).start()

    # Start Flask server (Render requires this)
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

