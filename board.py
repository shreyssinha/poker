class Board:
    def __init__(self):
        self.cards = []
    
    def reset(self):
        self.cards.clear()
    
    def add(self, card):
        self.cards.append(card)

    def __str__(self):
        return " ".join(str(c) for c in self.cards)