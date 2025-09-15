import os
import logging
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from flask import Flask, request

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
TOKEN = os.environ.get('TOKEN')
# Get allowed group ID from environment variable
ALLOWED_GROUP_ID = os.environ.get('ALLOWED_GROUP_ID')

if not BOT_TOKEN or not ALLOWED_GROUP_ID:
    logger.error("Please set BOT_TOKEN and ALLOWED_GROUP_ID environment variables")
    exit(1)

# Convert to integer
try:
    ALLOWED_GROUP_ID = int(ALLOWED_GROUP_ID)
except ValueError:
    logger.error("ALLOWED_GROUP_ID must be an integer")
    exit(1)

# Create Flask app
app = Flask(__name__)

# Create Application
application = Application.builder().token(TOKEN).build()

async def is_member_of_allowed_group(update: Update) -> bool:
    """Check if the user is a member of the allowed group"""
    user_id = update.effective_user.id
    
    try:
        # Get chat member status in the allowed group
        chat_member = await application.bot.get_chat_member(ALLOWED_GROUP_ID, user_id)
        status = chat_member.status
        
        # Check if user is a member, admin, or creator of the group
        if status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        logger.error(f"Error checking group membership: {e}")
    
    return False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /start is issued."""
    if not await is_member_of_allowed_group(update):
        await update.message.reply_text("Sorry, this bot is only available to members of the specific group.")
        return
        
    await update.message.reply_text('Hello! I am your group-exclusive bot. How can I help you?')

async def help_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Send a message when the command /help is issued."""
    if not await is_member_of_allowed_group(update):
        await update.message.reply_text("Sorry, this bot is only available to members of the specific group.")
        return
        
    await update.message.reply_text('Help!')

async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Echo the user message."""
    if not await is_member_of_allowed_group(update):
        await update.message.reply_text("Sorry, this bot is only available to members of the specific group.")
        return
        
    await update.message.reply_text(update.message.text)

# Add handlers to application
application.add_handler(CommandHandler("start", start))
application.add_handler(CommandHandler("help", help_command))
application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

@app.route('/')
def index():
    return 'Bot is running!'

@app.route('/webhook', methods=['POST'])
async def webhook():
    """Webhook route for Telegram to send updates to"""
    try:
        # Process the update
        update = Update.de_json(request.get_json(), application.bot)
        await application.update_queue.put(update)
        return 'OK'
    except Exception as e:
        logger.error(f"Error processing update: {e}")
        return 'Error', 500

if __name__ == '__main__':
    # For development
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
