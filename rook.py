import random

SUITS = ['black', 'red', 'green', 'yellow']
ROOKS = ['rook', 'redone']

class RookCard(object):
    def __init__(self, s, r):
        self.suit = s
        self.rank = r
        self.is_face_up = False
        
    def __str__(self):
        if self.is_face_up:
            return self.suit+('' if self.rank>14 else str(self.rank))
        else:
            return "CardBack"
        
    def __gt__(self, other):
        if self.suit == other.suit:
            return self.rank > other.rank
        else:
            return (SUITS+ROOKS).index(self.suit) > (SUITS+ROOKS).index(other.suit)
    
    def __lt__(self, other):
        if self.suit == other.suit:
            return self.rank < other.rank
        else:
            return (SUITS+ROOKS).index(self.suit) < (SUITS+ROOKS).index(other.suit)
        
    def rook_value(self):
        if self.suit == ROOKS[0]:
            return 20
        elif self.suit == ROOKS[1]:
            return 30
        elif self.rank == 14 or self.rank == 10:
            return 10
        elif self.rank == 5:
            return 5
        else:
            return 0
        
    def golden10_value(self):
        if self.suit == 'red':
            if self.rank == 10:
                return 10
            elif self.rank == 5:
                return 5
            else:
                return 1
        elif self.suit == 'yellow' and self.rank == 10:
            return -10
        else:
            return 0
        
    def turn_over(self):
        self.is_face_up = not self.is_face_up
        
    def turn_up(self):
        self.is_face_up = True
        
    def turn_down(self):
        self.is_face_up = False

class RookDeck(object):
    def __init__(self, low=5, high=14, rook=True, redone=False):
        self.cards = []
        for suit in SUITS:
            for rank in range(low,high+1):
                self.cards.append(RookCard(suit, rank))
        if rook: self.cards.append(RookCard(ROOKS[0],20))
        if redone: self.cards.append(RookCard(ROOKS[1],30))
    
    def __len__(self):
        return len(self.cards)
    
    def shuffle(self):
        random.shuffle(self.cards)
        
    def is_empty(self):
        return len(self.cards) == 0
    
    def get_next_card(self):
        return self.cards.pop()
        
    def deal_next_card(self):
        c = self.cards.pop()
        c.turn_over()
        return c