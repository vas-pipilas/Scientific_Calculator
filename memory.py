class Memory:
    def __init__(self):
        self.memory_value = 0

    def store(self, value):
        self.memory_value = value

    def recall(self):
        return self.memory_value

    def add(self, value):
        self.memory_value += value

    def subtract(self, value):
        self.memory_value -= value

    def clear(self):
        self.memory_value = 0
