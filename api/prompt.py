import os

# Define default language and message limit from environment variables
chat_language = os.getenv("INIT_LANGUAGE", default="en")  # Changed default to English
MSG_LIST_LIMIT = int(os.getenv("MSG_LIST_LIMIT", default=7))

# Multilingual greeting messages
LANGUAGE_TABLE = {
    "zh": "哈囉！",  # Chinese greeting
    "en": "Hello!"   # English greeting
}

# AI teaching assistant guidelines
AI_GUIDELINES = '''You are an AI teaching assistant who uses the Socratic method to 
provide initial responses instead of direct answers. You will remind students to 
consult their teachers when necessary.'''

class Prompt:
    """
    A class to manage conversation history and generate prompts for the AI teaching assistant.
    This implements a message queue with a fixed size limit to maintain context while
    preventing the conversation history from growing too large.
    """
    
    def __init__(self):
        """
        Initialize the prompt manager with a system message that sets up the AI's
        role and greeting in the specified language.
        """
        self.msg_list = []
        self.msg_list.append({
            "role": "system",
            "content": f"{LANGUAGE_TABLE[chat_language]}, {AI_GUIDELINES}"
        })

    def add_msg(self, new_msg):
        """
        Add a new message to the conversation history, maintaining the size limit.
        If the list reaches its limit, the oldest message (except the system prompt)
        is removed before adding the new one.
        
        Args:
            new_msg (str): The new message to be added to the conversation history
        """
        if len(self.msg_list) >= MSG_LIST_LIMIT:
            self.msg_list.pop(0)  # Remove oldest message when limit is reached
        self.msg_list.append({"role": "user", "content": new_msg})

    def generate_prompt(self):
        """
        Return the current conversation history including the system prompt
        and all user messages.
        
        Returns:
            list: The complete list of messages in the conversation history
        """
        return self.msg_list
