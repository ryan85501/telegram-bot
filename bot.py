
import os
# Replace with your bot token
TOKEN =os.getenv("8361381103:AAHsALmGWe5LPrqUZKpAQzAAOeSgqy3buQE")

# Replace with your group ID (negative number, e.g. -1001234567890)
ALLOWED_GROUP_ID = int(os.getenv("-1002994271767", "0"))  

# Replace with your Mini App URL
MINI_APP_URL = os.getenv("MINI_APP_URL", "https://ryan85501.github.io/Shwe-Pat-Tee/")

async def open_app(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat_id = update.effective_chat.id
    
    # Restrict usage to group only
    if chat_id != ALLOWED_GROUP_ID:
        await update.message.reply_text("❌ This command only works inside the group.")
        return

    # Create a button that opens your Mini App
    keyboard = [
        [InlineKeyboardButton("🚀 Open Mini App", url=MINI_APP_URL)]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)

    await update.message.reply_text(
        "Click below to open the Mini App:",
        reply_markup=reply_markup
    )

def main():
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("open", open_app))

    print("✅ Bot is running...")
    app.run_polling()

if __name__ == "__main__":
    main()


