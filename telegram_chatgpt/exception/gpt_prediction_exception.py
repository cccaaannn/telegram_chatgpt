class GPTPredictionException(Exception):
    def __init__(self, message="Could not predict"):
        self.message = message

    def __str__(self):
        return self.message

    def __repr__(self):
        return self.message
