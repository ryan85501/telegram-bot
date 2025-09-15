# --- Telegram Bot Server with Flask ---
import os
import sys
import logging
from flask import Flask, request

# Fix for imghdr removal in Python 3.13
import imghdr_pure as imghdr
sys.modules['imghdr'] = imghdr

from telegram import Update
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext

# --- Config ---
TOKEN = os.getenv("TELEGRAM_TOKEN")  # Set in Render Dashboard
PORT = int(os.environ.get("PORT", 8443))  # Render assigns a PORT env var

# --- Flask app (for Render web service) ---
app = Flask(__name__)

# --- Logging ---
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# --- Telegram Bot Handlers ---
def start(update: Update, context: CallbackContext):
    update.message.reply_text("Hello! 🎉 I’m alive on Render 🚀")

def echo(update: Update, context: CallbackContext):
    update.message.reply_text(update.message.text)

# --- Initialize Updater/Dispatcher ---
updater = Updater(TOKEN, use_context=True)
dispatcher = updater.dispatcher

dispatcher.add_handler(CommandHandler("start", start))
dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, echo))

# --- Flask route for webhook ---
@app.route("/" + TOKEN, methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), updater.bot)
    dispatcher.process_update(update)
    return "ok"

@app.route("/")
def index():
    return "Bot is running ✅"

# --- Run app ---
if __name__ == "__main__":
    # Set webhook to Render URL
    WEBHOOK_URL = f"https://{os.getenv('RENDER_EXTERNAL_HOSTNAME')}/{TOKEN}"
    updater.bot.set_webhook(WEBHOOK_URL)
    print(f"📡 Webhook set to {WEBHOOK_URL}")

    # Run Flask app
    app.run(host="0.0.0.0", port=PORT)
