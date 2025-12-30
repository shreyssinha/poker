from itertools import combinations
from collections import Counter

class HandEvaluator:

    HAND_RANKINGS = {
        'High Card': 1,
        'One Pair': 2,
        'Two Pair': 3,
        'Three of a Kind': 4,
        'Straight': 5,
        'Flush': 6,
        'Full House': 7,
        'Four of a Kind': 8,
        'Straight Flush': 9,
        'Royal Flush': 10
    }

    def best_hand(self, hole_cards, board_cards):
        all_cards = hole_cards + board_cards
        
        best_hand = None
        best_rank = 0

        for five in combinations(all_cards, 5):
            hand_rank, hand_name, tiebreakers = self._score_five(list(five))

            if hand_rank > best_rank or (hand_rank == best_rank and tiebreakers > best_hand[3]):
                best_rank = hand_rank
                best_hand = (hand_rank, hand_name, list(five), tiebreakers)

        return best_hand


    def _score_five(self, cards):
        ranks = [c.rank.value for c in cards]
        suits = [c.suit for c in cards]
        rank_counts = Counter(ranks)
        
        is_flush = len(set(suits)) == 1
        is_straight, straight_high = self._check_straight(ranks)
        
        # Count rank frequencies
        counts = sorted(rank_counts.values(), reverse=True)
        unique_ranks = sorted(rank_counts.keys(), reverse=True)
        
        # Royal Flush
        if is_flush and is_straight and max(ranks) == 14:
            return (HandEvaluator.HAND_RANKINGS['Royal Flush'], 'Royal Flush', [14])
        
        # Straight Flush
        if is_flush and is_straight:
            return (HandEvaluator.HAND_RANKINGS['Straight Flush'], 'Straight Flush', [straight_high])
        
        # Four of a Kind
        if counts == [4, 1]:
            quad = [r for r, c in rank_counts.items() if c == 4][0]
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return (HandEvaluator.HAND_RANKINGS['Four of a Kind'], 'Four of a Kind', [quad, kicker])
        
        # Full House
        if counts == [3, 2]:
            trips = [r for r, c in rank_counts.items() if c == 3][0]
            pair = [r for r, c in rank_counts.items() if c == 2][0]
            return (HandEvaluator.HAND_RANKINGS['Full House'], 'Full House', [trips, pair])
        
        # Flush
        if is_flush:
            return (HandEvaluator.HAND_RANKINGS['Flush'], 'Flush', sorted(ranks, reverse=True))
        
        # Straight
        if is_straight:
            return (HandEvaluator.HAND_RANKINGS['Straight'], 'Straight', [straight_high])
        
        # Three of a Kind
        if counts == [3, 1, 1]:
            trips = [r for r, c in rank_counts.items() if c == 3][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return (HandEvaluator.HAND_RANKINGS['Three of a Kind'], 'Three of a Kind', [trips] + kickers)
        
        # Two Pair
        if counts == [2, 2, 1]:
            pairs = sorted([r for r, c in rank_counts.items() if c == 2], reverse=True)
            kicker = [r for r, c in rank_counts.items() if c == 1][0]
            return (HandEvaluator.HAND_RANKINGS['Two Pair'], 'Two Pair', pairs + [kicker])
        
        # One Pair
        if counts == [2, 1, 1, 1]:
            pair = [r for r, c in rank_counts.items() if c == 2][0]
            kickers = sorted([r for r, c in rank_counts.items() if c == 1], reverse=True)
            return (HandEvaluator.HAND_RANKINGS['One Pair'], 'One Pair', [pair] + kickers)
        
        # High Card
        return (HandEvaluator.HAND_RANKINGS['High Card'], 'High Card', sorted(ranks, reverse=True))
    
    def _check_straight(self, ranks):
        sorted_ranks = sorted(set(ranks), reverse=True)
        
        # Check for A-2-3-4-5 (wheel)
        if sorted_ranks == [14, 5, 4, 3, 2]:
            return (True, 5)
        
        # Check for regular straight
        if len(sorted_ranks) == 5:
            if sorted_ranks[0] - sorted_ranks[4] == 4:
                return (True, sorted_ranks[0])
        
        return (False, 0)

    def find_winner(self, players_hands):
        evaluated_hands = []
        
        for player_id, hole_cards, board_cards in players_hands:
            hand_result = self.best_hand(hole_cards, board_cards)
            evaluated_hands.append((player_id, hand_result))
        
        evaluated_hands.sort(key=lambda x: (x[1][0], x[1][3]), reverse=True)
        
        best_rank = evaluated_hands[0][1][0]
        best_tiebreakers = evaluated_hands[0][1][3]
        
        winners = []
        for player_id, hand_result in evaluated_hands:
            if hand_result[0] == best_rank and hand_result[3] == best_tiebreakers:
                winners.append({
                    'player_id': player_id,
                    'hand_name': hand_result[1],
                    'best_cards': hand_result[2],
                    'hand_rank': hand_result[0],
                    'tiebreakers': hand_result[3]
                })
            else:
                break
        
        return winners