import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from flask import Flask
from threading import Thread

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
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    if chat_id != ALLOWED_GROUP_ID:
        await update.message.reply_text("❌ This bot only works inside the group.")
        return
    await update.message.reply_text("✅ Bot is active in this group!")

# /open command → launches Mini App
async def open_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    app.run(host='0.0.0.0', port=PORT)

def run_bot():
    if not TOKEN:
        raise ValueError("❌ TOKEN is missing. Set it in Render Environment Variables.")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("open", open_app))

    print("🤖 Bot is running...")
    application.run_polling()

if __name__ == "__main__":
    # Start Flask in a separate thread for health checks
    flask_thread = Thread(target=run_flask)
    flask_thread.daemon = True
    flask_thread.start()
    
    # Run the bot in the main thread
    run_bot()
