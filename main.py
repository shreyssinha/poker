from poker import Poker
from player import Player

players = [
    Player("Alice", 1000),
    Player("Bob", 1000),
    Player("Charlie", 1000),
]

game = Poker(players)
game.play_hand()