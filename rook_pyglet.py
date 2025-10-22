import pyglet
from pyglet.window import key, mouse
import random
import rook

win_width, win_height = 1300, 950

PLAYERS = 4
SUITS = ['black', 'red', 'green', 'yellow']
ROOKS = ['rook', 'redone']

HAND_POSITIONS = [[(50*i+250, 0, 0) for i in range(15)],
                [(0, -50*i+win_height-50, 0) for i in range(15)],
                [(-50*i+win_width-250, win_height, 0) for i in range(15)],
                [(win_width, 50*i+win_height-850, 0) for i in range(15)]]
# NEST = []

DISCARDS = [(600,250,0), (400,400,0), (600,500,0), (800,400,0)]

window = pyglet.window.Window(win_width,win_height,"Rook!")
batch = pyglet.graphics.Batch()
background = pyglet.sprite.Sprite(pyglet.image.load('background.jpg'), batch=batch)
background.scale_x = win_width/background.width
background.scale_y = win_height/background.height
cardback = pyglet.image.load('CardBack.png')

trump_picker = pyglet.sprite.Sprite(pyglet.image.load('trump_picker.png'), x=500, y=300, batch=batch)
trump_picker.scale = 2

class RookCardSprite(rook.RookCard):
    def __init__(self, s, r):
        super().__init__(s,r)
        self.is_face_up = True
        self.image = pyglet.image.load(f'{self.suit}{'' if self.rank>14 else self.rank}.png')
        self.sprite = pyglet.sprite.Sprite(self.image, batch=batch)
        
    def __str__(self):
        if self.is_face_up:
            return self.suit+('*' if self.rank>14 else str(self.rank))
        else:
            return "CardBack"
        
    def turn_up(self):
        self.is_face_up = True
        self.sprite.image = self.image
        
    def turn_down(self):
        self.is_face_up = False
        self.sprite.image = cardback

class RookDeckSprite(rook.RookDeck):
    def __init__(self):
        self.cards = []
        for suit in SUITS:
            for rank in range(1,15):
                self.cards.append(RookCardSprite(suit, rank))
        self.cards.append(RookCardSprite(ROOKS[0],20))
        self.cards.append(RookCardSprite(ROOKS[1],30))
    
class RookGame(object):
    def __init__(self):
        self.players = [[],[],[],[]]
        self.current = 0
        self.dealer = 0
        self.game_on = False
        self.trump = ''
        self.led_suit = ''
        self.trick = [None,None,None,None]
        self.won_tricks = [[],[],[],[]]
        self.score = [0,0,0,0]
        
    def new_game(self):
        self.new_round()
        
    def new_round(self):
        self.current = (self.dealer + 1) % PLAYERS
        self.players = [[],[],[],[]]
        self.won_tricks = [[],[],[],[]]
        
        d = RookDeckSprite()
        d.shuffle()
        
        while d:
            self.players[self.current].append(d.get_next_card())
            self.current = (self.current + 1) % PLAYERS
        
        for i in range(PLAYERS):
            self.players[i].sort()
            for j in range(len(self.players[i])):
                card = self.players[i][j]
                # if i!=0: card.turn_down()
                card.sprite.rotation = i*90
        
        self.resprite()
        self.current = self.dealer
        self.trump = ''
        trump_picker.visible = True

    def resprite(self):
        for i in range(PLAYERS):
            self.players[i].sort()
            for j in range(len(self.players[i])):
                card = self.players[i][j]
                card.sprite.position = HAND_POSITIONS[i][j]
                card.sprite.rotation = i*90
            if pd := self.trick[i]:
                pd.sprite.position = DISCARDS[i]
                pd.sprite.rotation = 0

    def count_cards(self):
        for i in range(PLAYERS):
            round_score = 0
            for j in range(len(self.won_tricks[i])):
                t_card = self.won_tricks[i][j]
                if t_card.rook_value() > 0:
                    # t_card.sprite.visible = True
                    self.players[i].append(t_card)
                print(f"    {t_card} - {t_card.rook_value()} points")
                round_score += t_card.rook_value()
            print(f"player {i} - {round_score} points\n")
            self.score[i] += round_score
        
    def trick_winner(self):
        self.resprite()
        follow_suit = []
        played_trumps = []
        for t in self.trick:
            # print(t, end=' ')
            if t.suit == self.led_suit:
                follow_suit.append(t)
            if t.suit in [self.trump]+ROOKS:
                played_trumps.append(t)
        winner = self.trick.index(max(played_trumps)) if played_trumps else self.trick.index(max(follow_suit))
        print(f"Player {winner} takes the trick\n")
        self.current = winner
        self.won_tricks[winner].extend(self.trick)
        for t in self.trick:
            t.sprite.position = (win_width,win_height,0)
        self.trick = [None,None,None,None]
        self.led_suit = ''
        if not all(self.players):
            print("End of round\n")
            for p in self.players:
                if p:
                    last_card = p.pop()
                    last_card.sprite.position = (win_width,win_height,0)
                    last_card.sprite.rotation = 0
                    self.won_tricks[winner].append(last_card)
            self.game_on = False
        

g = RookGame()
g.new_game()

def next_player():
    if all(g.trick):
        g.trick_winner()
    else:
        g.current = (g.current + 1) % PLAYERS
    while g.game_on and g.current != 0:
        r = play_trick(g.current)
        g.players[g.current][r].turn_up()
        g.trick[g.current] = g.players[g.current][r]
        print(f"Player {g.current} discards card {r}: {g.players[g.current][r]}")
        g.players[g.current].pop(r)
        if all(g.trick):
            g.trick_winner()
        else:
            g.current = (g.current + 1) % PLAYERS
    g.resprite()
    if not g.game_on:
        g.count_cards()
        g.resprite()
        print("Current scores:", g.score)

def play_trick(player):
    if not g.led_suit:
        i = random.randrange(len(g.players[player]))
        if g.players[player][i].suit in ROOKS:
            g.led_suit = g.trump
        else:
            g.led_suit = g.players[player][i].suit
    else:
        follow_suit = []
        for c in g.players[player]:
            if c.suit in [g.led_suit]+ROOKS:
                follow_suit.append(c)
        if follow_suit:
            cc = random.choice(follow_suit)
            i = g.players[player].index(cc)
        else:
            i = random.randrange(len(g.players[player]))
    return i

@window.event
def on_draw():
    window.clear()
    batch.draw()

def selected_card(x,y):
    for i in range(len(g.players[0])):
        c = g.players[0][i]
        cx = c.sprite.x
        if x>cx and x<cx+(135 if i == len(g.players[0])-1 else 50) and y>0 and y<210:
            if (g.led_suit == '') or (not can_follow_suit()) or (can_follow_suit() and c.suit in [g.led_suit]+ROOKS):
                return c, i

def can_follow_suit():
    if g.led_suit == g.trump:
        for c in g.players[0]:
            if c.suit == g.led_suit or c.suit in ROOKS:
                return True
        return False
    else:
        for c in g.players[0]:
            if c.suit == g.led_suit:
                return True
        return False

def select_trump(x,y):
    if x>535 and x<655 and y>480 and y<600:
        g.trump = 'red'
    elif x>675 and x<795 and y>480 and y<600:
        g.trump = 'black'
    elif x>535 and x<655 and y>340 and y<460:
        g.trump = 'yellow'
    elif x>675 and x<795 and y>340 and y<460:
        g.trump = 'green'
    if g.trump:
        trump_picker.visible = False
        window.set_caption(f"Trump is {g.trump}; Current Scores: {g.score}")
        g.game_on = True
        next_player()

@window.event
def on_mouse_press(x, y, button, modifiers):
    if button == mouse.LEFT:
        # print(x,y)
        if g.trump and g.game_on:
            if ci := selected_card(x,y):
                c,i = ci
                print(f"Player 0 discards card {i}: {c}")
                g.trick[0] = c
                if not g.led_suit:
                    if c.suit in ROOKS:
                        g.led_suit = g.trump
                    else:
                        g.led_suit = c.suit
                g.players[0].pop(i)
                g.resprite()
                next_player()
            else:
                if g.led_suit: print(f"Must follow suit: {g.led_suit}")
        elif g.trump:
            g.dealer = (g.dealer + 1) % PLAYERS
            g.new_round()
        else:
            select_trump(x,y)
        

pyglet.app.run()