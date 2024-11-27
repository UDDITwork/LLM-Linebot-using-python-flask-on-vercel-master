from flask import Flask, request, abort
from linebot import LineBotApi, WebhookHandler
from linebot.exceptions import InvalidSignatureError
from linebot.models import MessageEvent, TextMessage, TextSendMessage
from api.chatgpt import ChatGPT
import os

# Initialize Line Bot API with access token
line_bot_api = LineBotApi(os.getenv("LINE_CHANNEL_ACCESS_TOKEN"))
line_handler = WebhookHandler(os.getenv("LINE_CHANNEL_SECRET"))
# Set default talking status from environment variable
working_status = os.getenv("DEFALUT_TALKING", default="true").lower() == "true"

app = Flask(__name__)
chatgpt = ChatGPT()

# Root route
@app.route('/')
def home():
    return 'Hello, World!'

# Webhook endpoint for Line Bot
@app.route("/webhook", methods=['POST'])
def callback():
    signature = request.headers['X-Line-Signature']
    body = request.get_data(as_text=True)
    app.logger.info("Request body: " + body)
    
    try:
        line_handler.handle(body, signature)
    except InvalidSignatureError:
        abort(400)
    return 'OK'

@line_handler.add(MessageEvent, message=TextMessage)
def handle_message(event):
    global working_status
    
    if event.message.type != "text":
        return

    # Command to enable talking
    if event.message.text == "speak":  
        working_status = True
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="I can talk now, feel free to interact with me ^_^")  
        )
        return

    # Command to disable talking
    if event.message.text == "quiet": 
        working_status = False
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text="Okay, I'll be quiet now. If you want me to talk again, please say 'speak' > <") 
        )
        return

    # Handle normal conversation when working_status is True
    if working_status:
        chatgpt.add_msg(f"HUMAN:{event.message.text}?\n")
        reply_msg = chatgpt.get_response().replace("AI:", "", 1)
        chatgpt.add_msg(f"AI:{reply_msg}\n")
        line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text=reply_msg)
        )

if __name__ == "__main__":
    app.run()
