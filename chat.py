import logging
import json
from telegram import Update
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
)
from dotenv import load_dotenv
import os
from supabase import create_client, Client
import tiktoken
from ai import count_tokens_in_text, trim_to_last_tokens, llm_call

# Load environment variables from .env file
load_dotenv()

# Retrieve the Telegram token and Supabase URL and Key from the environment variables
TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
SUPABASE_URL = os.getenv("SUPABASE_URL")
SUPABASE_KEY = os.getenv("SUPABASE_KEY")
USER_EMAIL = "maxhager28@gmail.com"

# Initialize Supabase client
supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

# Enable logging
logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)
logger = logging.getLogger(__name__)

# Define a function to handle messages
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    #this is called every time, i need to 
    chat_id = update.message.chat.id  # Get the chat_id
    message_text = update.message.text  # Get the message text
    user_id = update.message.from_user.id  # Get the user ID

    # Log the received message
    logger.info(f"Received message from chat_id: {chat_id}")  # Log the chat_id
    logger.info(f"Message text: {message_text}")  # Log the message text

    # Query Supabase to find the user by email
    response = supabase.table('chat').select('chat').eq('user', USER_EMAIL).execute()

    if response.data and len(response.data) > 0:
        # User found, retrieve chat history
        chat_data = response.data[0]['chat']
        if chat_data is not None:
            chat_history = chat_data if isinstance(chat_data, list) else json.loads(chat_data)
        else:
            chat_history = []  # Initialize as empty list if chat_data is None
    else:
        # User not found or no chat history, initialize an empty list
        chat_history = []
    
    chat_history.append({"role": "user", "content": message_text})

    # Prepare the assistant's response (for demonstration, we just echo back)
    assistant_response = llm_call(chat_history, message_text)
    chat_history.append({"role": "assistant", "content": assistant_response})

    # Update the chat history in Supabase
    update_response = supabase.table('chat').update({
        'chat': chat_history  # Store the list directly
    }).eq('user', USER_EMAIL).execute()

    # Check if the update was successful
    if update_response.data:
        logger.info("Chat history updated in Supabase successfully.")
    else:
        logger.error(f"Error updating chat history in Supabase: {update_response.error}")

    # Respond with the assistant's response
    await update.message.reply_text(assistant_response)  # Respond with "Okay"

def main() -> None:
    # Create the Application and pass it your bot's token
    application = ApplicationBuilder().token(TELEGRAM_TOKEN).build()

    # Register the message handler
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))

    # Start the Bot
    application.run_polling()

if __name__ == "__main__":
    main()