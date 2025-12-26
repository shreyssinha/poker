class HandEvaluator:
    def best_hand(self, hole_cards, board_cards):
        """
        """
        all_cards = hole_cards + board_cards
        return max(card.rank.value for card in all_cards)