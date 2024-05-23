class Memory:
    def __init__(self):
        self.memory_value = 0  # Αρχικοποίηση της μεταβλητής μνήμης σε 0

    def store(self, value):
        self.memory_value = value  # Αποθήκευση της τιμής στη μνήμη

    def recall(self):
        return self.memory_value  # Επαναφορά της αποθηκευμένης τιμής

    def add(self, value):
        self.memory_value += value  # Προσθήκη της τιμής στη μνήμη

    def subtract(self, value):
        self.memory_value -= value  # Αφαίρεση της τιμής από τη μνήμη

    def clear(self):
        self.memory_value = 0  # Εκκαθάριση της μνήμης (επαναφορά στο 0)