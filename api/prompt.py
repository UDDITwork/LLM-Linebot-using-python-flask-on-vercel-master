import os

# Default settings from environment variables
initial_language = os.getenv("INIT_LANGUAGE", default="en")
message_history_limit = int(os.getenv("MSG_LIST_LIMIT", default=7))

# Available greetings in different languages
available_greetings = {
    "en": "Hello!",
    "fr": "Bonjour!",
    "es": "¡Hola!",
    "de": "Hallo!"
}

# Teaching assistant behavior guidelines
teaching_guidelines = '''
You are an AI teaching assistant implementing the Socratic method of instruction.
Your role is to guide students through questioning rather than providing direct answers.
When necessary, remind students to verify important concepts with their teachers.
Encourage critical thinking and self-discovery in the learning process.
'''

class ConversationManager:
    """
    Manages the conversation flow between users and the AI teaching assistant.
    Maintains a limited message history and structures the conversation format.
    """
    
    def __init__(self):
        """
        Initializes the conversation manager with a system-level greeting
        and teaching guidelines in the specified language.
        """
        self.message_history = []
        self.message_history.append({
            "role": "system",
            "content": f"{available_greetings[initial_language]}, {teaching_guidelines}"
        })

    def add_message(self, incoming_message):
        """
        Adds a new message to the conversation history while maintaining
        the specified message limit.

        Args:
            incoming_message (str): The new message to be added to the conversation
        """
        if len(self.message_history) >= message_history_limit:
            # Remove oldest message when limit is reached, preserving system message
            self.message_history.pop(0)
        
        self.message_history.append({
            "role": "user",
            "content": incoming_message
        })

    def get_conversation_history(self):
        """
        Retrieves the current conversation history including system prompt
        and user messages.

        Returns:
            list: Complete conversation history in chronological order
        """
        return self.message_history
