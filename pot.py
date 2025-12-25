class Pot:
    def __init__(self):
        self.amount = 0
    
    def reset(self):
        self.amount = 0

    def add(self, amount: int):
        self.amount += amount