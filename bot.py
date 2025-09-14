import os
 
from telegram.ext import Application, CommandHandler, ContextTypes

# Get environment variables (from Render dashboard)
TOKEN = os.getenv("TOKEN")
ALLOWED_GROUP_ID = int(os.getenv("ALLOWED_GROUP_ID", "0"))
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://ryan85501.github.io/Shwe-Pat-Tee/")

# /start command
async def start(update, context):
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

def main():
    if not TOKEN:
        raise ValueError("❌ TOKEN is missing. Set it in Render Environment Variables.")

    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("open", open_app))

    print("🤖 Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()





