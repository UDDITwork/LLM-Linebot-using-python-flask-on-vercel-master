# LLM-Linebot-using-python-flask-on-vercel-master# ChatGPT Line Bot Implementation
# Author: [Your Name]
# Description: A Line messaging bot powered by ChatGPT API
# Last Updated: 2024

import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

# Initialize Line Bot API with credentials from environment variables
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# Default behavior settings
bot_active = os.getenv("DEFAULT_TALKING", default="true").lower() == "true"

# Initialize Flask application
app = Flask(__name__)
chatgpt = ChatGPT()

# Root endpoint
@app.route('/')
def home():
    return 'Hello, World!'

# Webhook endpoint for Line Bot
@app.route("/webhook", methods=['POST'])
def callback():
    # Get signature from headers for verification
    signature = request.headers['X-Line-Signature']
    
    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    Handles incoming messages and manages bot responses
    Args:
        event: Line message event containing user message
    """
    global bot_active
    
    # Ignore non-text messages
    if event.message.type != "text":
        return

    # Command to enable bot responses
    if event.message.text.lower() == "speak":
        bot_active = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="I'm now active and ready to chat! Feel free to ask me anything.")
        )
        return

    # Command to disable bot responses
    if event.message.text.lower() == "quiet":
        bot_active = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="I'll be quiet now. Say 'speak' when you want to chat again.")
        )
        return

    # Process message with ChatGPT when bot is active
    if bot_active:
        # Format user message for ChatGPT
        chatgpt.add_message(f"Human: {event.message.text}?\n")
        
        # Get response from ChatGPT
        response = chatgpt.get_response().replace("AI:", "", 1)
        
        # Store conversation history
        chatgpt.add_message(f"Assistant: {response}\n")
        
        # Send response back to user
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

if __name__ == "__main__":
    # Start Flask application
    app.run()
# ChatGPT Line Bot Implementation
# Author: [Your Name]
# Description: A Line messaging bot powered by ChatGPT API
# Last Updated: 2024

import os
from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT

# Initialize Line Bot API with credentials from environment variables
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))

# Default behavior settings
bot_active = os.getenv("DEFAULT_TALKING", default="true").lower() == "true"

# Initialize Flask application
app = Flask(__name__)
chatgpt = ChatGPT()

# Root endpoint
@app.route('/')
def home():
    return 'Hello, World!'

# Webhook endpoint for Line Bot
@app.route("/webhook", methods=['POST'])
def callback():
    # Get signature from headers for verification
    signature = request.headers['X-Line-Signature']
    
    # Get request body as text
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    """
    Handles incoming messages and manages bot responses
    Args:
        event: Line message event containing user message
    """
    global bot_active
    
    # Ignore non-text messages
    if event.message.type != "text":
        return

    # Command to enable bot responses
    if event.message.text.lower() == "speak":
        bot_active = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="I'm now active and ready to chat! Feel free to ask me anything.")
        )
        return

    # Command to disable bot responses
    if event.message.text.lower() == "quiet":
        bot_active = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="I'll be quiet now. Say 'speak' when you want to chat again.")
        )
        return

    # Process message with ChatGPT when bot is active
    if bot_active:
        # Format user message for ChatGPT
        chatgpt.add_message(f"Human: {event.message.text}?\n")
        
        # Get response from ChatGPT
        response = chatgpt.get_response().replace("AI:", "", 1)
        
        # Store conversation history
        chatgpt.add_message(f"Assistant: {response}\n")
        
        # Send response back to user
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=response)
        )

if __name__ == "__main__":
    # Start Flask application
    app.run()
