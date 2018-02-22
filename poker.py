import re
import argparse
from collections import defaultdict

SUIT = {'S': 'Spades♠', 'H': 'Hearts♡', 'D': 'Diamonds♢', 'C': 'Clovers♣'}
RANK = ("2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A")
CARDS_PER_HAND = 5
# Initialize argyment parser object
parser = argparse.ArgumentParser(description="Evaluate a poker hand")
# Add optional argument
parser.add_argument('-i',
                    '--input', help="Input is a poker hand (ex: python poker.py -i D4C4C8D8S4)")


class Card:
    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __repr__(self):
        return self.suit + "-" + self.rank


class PokerHand:
    def __init__(self, cards):
        self.hand = self.getHand(cards)

    def validate(self, hands):
        errCode = 0
        errCards = []

        if len(hands) != CARDS_PER_HAND:
            errCode = 1
            return errCode, errCards

        for card in hands:
            if card.rank not in RANK or card.suit not in list(SUIT.keys()):
                errCode = 2
                errCards.append(card)

        return errCode, errCards

    def getHand(self, cards):
        cards_list = re.findall(r'.{1,2}', cards)
        hand = []
        # serialize cards to hand
        for card in cards_list:
            s, r = card[:-1], card[-1]
            hand.append(Card(s, r))
        # check validation of hand
        errCode, errCards = self.validate(hand)

        if errCode != 0:
            errorCode_list = {
                1: 'A hand must be 5 cards',
                2: 'Card is not valid',
            }

            mss_err = errorCode_list[errCode] + ' ' + \
                (str(errCards), '')[not errCards]

            raise ValueError(mss_err)

        return hand

    def evaluate(self):
        TYPE_OF_PKH = {
            1: '4C',
            2: 'FH',
            3: '3C',
            4: '2P',
            5: '1P',
            6: '--'
        }
        # default is no hand
        rank_hand = 6
        rank_dict = defaultdict(int)
        for card in self.hand:
            rank_dict[card.rank] += 1

        ranks_per_card = len(rank_dict)

        if ranks_per_card == 4:
            rank_hand = 5  # One Pair

        if ranks_per_card == 3:
            if 3 in rank_dict.values():
                rank_hand = 3  # Three Cards
            else:
                rank_hand = 4  # Two Pairs

        if ranks_per_card == 2:
            if 2 in rank_dict.values():
                rank_hand = 2  # Full House
            else:
                rank_hand = 1  # Four Cards

        return TYPE_OF_PKH[rank_hand]

    def __repr__(self):
        return self.evaluate()


if __name__ == '__main__':
    args = parser.parse_args()

    hand = args.input or 'S8D3HQS3CQ'
    print(hand)
    print('-----output-----')
    print(PokerHand(hand))

    
