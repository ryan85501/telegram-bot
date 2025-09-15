import os
import logging
from telegram import Update, Bot
from flask import Flask, request
import asyncio

# Enable logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

# Get bot token from environment variable
BOT_TOKEN = os.environ.get('BOT_TOKEN')
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

# Create bot instance
bot = Bot(token=BOT_TOKEN)

async def is_member_of_allowed_group(user_id: int) -> bool:
    """Check if the user is a member of the allowed group"""
    try:
        # Get chat member status in the allowed group
        chat_member = await bot.get_chat_member(ALLOWED_GROUP_ID, user_id)
        status = chat_member.status
        
        # Check if user is a member, admin, or creator of the group
        if status in ['member', 'administrator', 'creator']:
            return True
    except Exception as e:
        logger.error(f"Error checking group membership: {e}")
    
    return False

async def process_update(update_data):
    """Process incoming update"""
    try:
        update = Update.de_json(update_data, bot)
        user_id = update.effective_user.id
        
        if not await is_member_of_allowed_group(user_id):
            await bot.send_message(
                chat_id=update.effective_chat.id,
                text="Sorry, this bot is only available to members of the specific group."
            )
            return
        
        if update.message and update.message.text:
            if update.message.text.startswith('/start'):
                await bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Hello! I am your group-exclusive bot. How can I help you?'
                )
            elif update.message.text.startswith('/help'):
                await bot.send_message(
                    chat_id=update.effective_chat.id,
                    text='Help information goes here.'
                )
            else:
                await bot.send_message(
                    chat_id=update.effective_chat.id,
                    text=update.message.text
                )
    except Exception as e:
        logger.error(f"Error processing update: {e}")

@app.route('/')
def index():
    return 'Bot is running!'

@app.route('/webhook', methods=['POST'])
def webhook():
    """Webhook route for Telegram to send updates to"""
    try:
        # Get the update from Telegram
        update_data = request.get_json()
        
        # Process the update asynchronously
        asyncio.run(process_update(update_data))
        
        return 'OK'
    except Exception as e:
        logger.error(f"Error in webhook: {e}")
        return 'Error', 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))
