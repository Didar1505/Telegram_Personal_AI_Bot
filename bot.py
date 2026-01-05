from pyrogram import Client, filters, enums
from pyrogram.types import Message
from free_chatbot import OpenRouterChatbot
from dotenv import load_dotenv
from db import db
import os
import logging

load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)

# Telegram Auth API ID
API_ID = os.getenv("API_ID")
# Telegram Auth API HASH
API_HASH = os.getenv("API_HASH")
# Telegram Bot API TOKEN generated from @botfather
BOT_TOKEN = os.getenv("BOT_TOKEN")
# Open router api key 
OPEN_ROUTER_API_KEY = os.getenv("OPEN_ROUTER")

# Initialize the client
app = Client("Artemis", api_id=API_ID, api_hash=API_HASH, bot_token=BOT_TOKEN)

bot_ai = OpenRouterChatbot(api_key=OPEN_ROUTER_API_KEY)

@app.on_bot_business_message(filters.incoming & filters.text)
async def start(client: Client, message: Message):
    logger.info(f"Received message from {message.from_user.id}")
    try:
        await message.reply_chat_action(enums.ChatAction.TYPING)

        user_id = message.from_user.id

        chat_history = db.get_chat_history(user_id)
        
        prompt = message.text

        db.add_chat_history(user_id, {"role": "user", "content": prompt})

        response = bot_ai.generate_response(prompt, chat_history)
        
        db.add_chat_history(user_id, {"role": "assistant", "content": response})
        
        await message.reply_text(f"{response}")
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)

if __name__ == "__main__":
    logger.info("Bot is starting...")
    app.run()
