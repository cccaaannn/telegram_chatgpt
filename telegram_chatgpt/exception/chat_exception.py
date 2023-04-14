class ChatException(Exception):
    def __init__(self, message="Chat error"):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
