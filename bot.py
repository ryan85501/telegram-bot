import os
from flask import Flask, request
from telegram import Update
from telegram.ext import Application, CommandHandler, ContextTypes

TOKEN = os.getenv("TOKEN")
ALLOWED_GROUP_ID = os.getenv("ALLOWED_GROUP_ID")
MINI_APP_URL = os.getenv("MINI_APP_URL")

app = Flask(__name__)

# Create the Application
application = Application.builder().token(TOKEN).build()

# --- Handlers ---
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hello! ✅ Bot is running on Render.")

async def open_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(f"Mini App: {MINI_APP_URL}")

application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("app", open_app))

# --- Flask webhook route ---
@app.route(f"/{TOKEN}", methods=["POST"])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return "ok", 200

@app.route("/", methods=["GET"])
def home():
    return "Bot is running!", 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)
