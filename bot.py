import os
import asyncio
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, WebAppInfo
from telegram.ext import Application, CommandHandler, ContextTypes
from aiohttp import web

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

async def health_check(request):
    return web.Response(text="Bot is running!")

async def main():
    # Create bot application
    if not TOKEN:
        raise ValueError("❌ TOKEN is missing. Set it in Render Environment Variables.")

    application = Application.builder().token(TOKEN).build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CommandHandler("open", open_app))

    # Create aiohttp web app for health checks
    app = web.Application()
    app.router.add_get('/', health_check)
    
    # Set up web server
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', PORT)
    await site.start()
    
    print(f"🤖 Bot is running and web server is listening on port {PORT}...")
    
    # Start polling
    await application.initialize()
    await application.start()
    await application.updater.start_polling()
    
    # Keep the app running
    await asyncio.Event().wait()

if __name__ == "__main__":
    asyncio.run(main())
