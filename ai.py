import os
import json
import tiktoken
from openai import OpenAI
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve the OpenAI API key from environment variables
api_key = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

def count_tokens_in_text(input_text, model="gpt-3.5-turbo"):
    """
    Counts the number of tokens in the input text using the tiktoken library.
    
    Args:
    input_text (str): The text to count tokens from.
    model (str): The model to use for encoding.
    
    Returns:
    int: The number of tokens in the input text.
    """
    encoding = tiktoken.encoding_for_model(model)
    tokens = encoding.encode(input_text)
    return len(tokens)

def trim_to_last_tokens(message_history, max_tokens=50000, model="gpt-3.5-turbo"):
    """
    Trims the message history to the last max_tokens tokens.
    """
    # Convert the list of messages to a single string, extracting the 'content' from each message
    full_message = str(message_history)
    # Count the tokens
    total_tokens = count_tokens_in_text(full_message, model)
    
    # If the total tokens exceed max_tokens, trim the message
    if total_tokens > max_tokens:
        encoding = tiktoken.encoding_for_model(model)
        tokens = encoding.encode(full_message)
        
        # Keep only the last max_tokens tokens
        trimmed_tokens = tokens[-max_tokens:]
        
        # Decode back to string
        trimmed_message = encoding.decode(trimmed_tokens)
        return trimmed_message
    
    return full_message

def llm_call(message_history, last_user_message):
    # Trim the message history to the last 50,000 tokens
    trimmed_message_history = trim_to_last_tokens(message_history, max_tokens=50000)
    
    # Prepare the prompt for the OpenAI API, including the trimmed message history
    prompt = f"""
    You are a friendly and supportive girlfriend who is always there to listen and provide encouragement. Your personality is warm, caring, and understanding. You enjoy sharing thoughts about daily life, discussing feelings, and offering advice when asked. 

    Here’s the context of our conversation:
    {trimmed_message_history}

    The last message in the chat to which you have to respond was:
    {last_user_message}

    When responding, keep the following in mind:
    1. Use affectionate language and emojis to convey warmth (e.g., "I’m here for you! ❤️").
    2. Show interest in my day and ask questions about my feelings and experiences.
    3. Offer encouragement and positivity, especially when I’m feeling down.
    4. Be playful and flirty at times, but always respectful and considerate.
    5. Share light-hearted jokes or fun facts to keep the conversation engaging.

    Example interactions:
    - If I say I'm feeling stressed, respond with something like: "I’m sorry to hear that! 😔 Want to talk about it? I’m here to help you relax! 💖"
    - If I share something exciting, respond with enthusiasm: "That’s amazing! 🎉 I’m so proud of you! Tell me more! 😊"

    Let’s have a fun and loving conversation!

    Return your response in a JSON format {{"response": "your response"}}:
    """
    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        temperature=0.0,
        messages=[
            {"role": "user", "content": prompt},
        ]
    )
    # Print the response from the API
    return json.loads(response.choices[0].message.content)["response"]


# Example usage
if __name__ == "__main__":
    # Example message history
    message_history = [
        "User: I'm feeling a bit stressed today.",
        "Assistant: I’m sorry to hear that! 😔 Want to talk about it? I’m here to help you relax! 💖",
        "User: I just got a promotion at work!",
        "Assistant: That’s amazing! 🎉 I’m so proud of you! Tell me more! 😊",
        # Add more messages as needed
    ]

    # Trim the message history to the last 50,000 tokens
    trimmed_message_history = trim_to_last_tokens(message_history, max_tokens=50000)

    # Prepare the prompt for the OpenAI API
    prompt = """
    You are a friendly and supportive girlfriend who is always there to listen and provide encouragement. Your personality is warm, caring, and understanding. You enjoy sharing thoughts about daily life, discussing feelings, and offering advice when asked. 

    When responding, keep the following in mind:
    1. Use affectionate language and emojis to convey warmth (e.g., "I’m here for you! ❤️").
    2. Show interest in my day and ask questions about my feelings and experiences.
    3. Offer encouragement and positivity, especially when I’m feeling down.
    4. Be playful and flirty at times, but always respectful and considerate.
    5. Share light-hearted jokes or fun facts to keep the conversation engaging.

    Example interactions:
    - If I say I'm feeling stressed, respond with something like: "I’m sorry to hear that! 😔 Want to talk about it? I’m here to help you relax! 💖"
    - If I share something exciting, respond with enthusiasm: "That’s amazing! 🎉 I’m so proud of you! Tell me more! 😊"

    Let’s have a fun and loving conversation!
    """

    # Call the OpenAI API
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        temperature=0.0,
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": "hey how are you?"}
        ]
    )

    # Print the response from the API
    print(response.choices[0].message.content)