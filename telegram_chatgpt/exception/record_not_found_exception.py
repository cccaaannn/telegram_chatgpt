class RecordNotFoundException(Exception):
    def __init__(self, message="Record not found"):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
