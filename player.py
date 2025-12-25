class Player:
    def __init__(self, name: str, stack: int):
        self.name = name
        self.stack = stack
        self.hand = []
        self.current_bet = 0
        self.folded = False
        self.all_in = False
    
    def reset_for_hand(self):
        self.hand.clear()
        self.current_bet = 0
        self.folded = False
        self.all_in = False
    
    def bet(self, amount: int):
        amount = min(amount, self.stack)
        self.stack -= amount
        self.current_bet += amount
        if self.stack == 0:
            self.all_in = True
        return amount
    
    def fold(self):
        self.folded = True
    
    def _str__(self):
        return f"{self.name} (${self.stack})"