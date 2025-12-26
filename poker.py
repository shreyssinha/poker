from deck import Deck
from player import Player
from pot import Pot
from board import Board
from hand_evaluator import HandEvaluator

class Poker:
    def __init__(self, players, small_blind=5, big_blind=10):
        self.players = players
        self.deck = Deck()
        self.board = Board()
        self.pot = Pot()
        self.evaluator = HandEvaluator()
        self.small_blind = small_blind
        self.big_blind = big_blind
        self.button = 0

    def rotate_button(self):
        self.button = (self.button + 1) % len(self.players)

    # Define small blind and big blind player and bet accordingly
    def post_blinds(self):
        sb = self.players[(self.button + 1) % len(self.players)]
        bb = self.players[(self.button + 2) % len(self.players)]
        self.pot.add(sb.bet(self.small_blind))
        self.pot.add(bb.bet(self.big_blind))

    # Player Cards
    def deal_hole_cards(self):
        for i in range(2):
            for player in self.players:
                player.hand.append(self.deck.draw())
    
    def deal_flop(self):
        self.deck.draw() # Burn
        for i in range(3):
            self.board.add(self.deck.draw())
    
    def deal_turn(self):
        self.deck.draw()
        self.board.add(self.deck.draw())
    
    def deal_river(self):
        self.deck.draw()
        self.board.add(self.deck.draw())

    def showdown(self):
        scores = {}
        for player in self.players:
            if not player.folded:
                scores[player] = self.evaluator.best_hand(
                    player.hand, self.board.cards
                )
        best = max(scores.values())
        winners = [p for p, s in scores.items() if s == best]
        return winners
    
    def play_hand(self):
        self.deck.reset()
        self.board.reset()
        self.pot.reset()

        for p in self.players:
            p.reset_for_hand()
        
        self.post_blinds()
        self.deal_hole_cards()
        self.deal_flop()
        self.deal_turn()
        self.deal_river()

        winners = self.showdown()
        split = self.pot.amount // len(winners)
        for w in winners:
            w.stack += split
        
        print("Board:", self.board)
        for p in self.players:
            print(p.name, p.hand)
        print("Winners:", ", ".join(w.name for w in winners))