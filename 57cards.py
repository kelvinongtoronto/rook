import pygame, sys
from pygame.locals import *
import random
import rook

pygame.init()
winwidth, winheight = 1400, 780
screen = pygame.display.set_mode((winwidth, winheight))
pygame.display.set_caption('Hello World!')
BACKGROUND = (0,128,0)
TEXTCOLOR = (255,255,0)
TEXT_WIDTH, TEXT_HEIGHT = 120, 30
TEXT_X, TEXT_Y = winwidth-TEXT_WIDTH, winheight-TEXT_HEIGHT
screen.fill(BACKGROUND)
fontObj = pygame.font.Font('freesansbold.ttf', 26)
# fontObj = pygame.font.SysFont('bookmanoldstyle',25)
# fontObj.bikd = True

origin1 = (0,0)
row=0
col=0

width = 100
height = 156

#create the deck
d = rook.RookDeck(1,14,True,True)
d.shuffle()

tableau={}

def get_moused_card(mx, my):
    for card,position in tableau.items():
        if position[0][0]<mx<position[1][0] and position[0][1]<my<position[1][1]:
            return card
    return None
    
def flip_card(mx,my):
    try:
        moused_card = get_moused_card(mx,my)
        origin = tableau[moused_card]
        moused_card.turn_over()
        
        img = pygame.transform.scale(pygame.image.load(str(moused_card)+".PNG"), (width,height))
        screen.blit(img, origin)
    except:
        pass
    
def swap_cards(card1x,card1y,card2x,card2y):
    try:
        card1 = get_moused_card(card1x,card1y)
        card2 = get_moused_card(card2x,card2y)
        
        tableau[card1], tableau[card2] = tableau[card2], tableau[card1]
        
        origin1 = tableau[card1]
        origin2 = tableau[card2]
        
        img1 = pygame.transform.scale(pygame.image.load(str(card1)+".PNG"), (width,height))
        img2 = pygame.transform.scale(pygame.image.load(str(card2)+".PNG"), (width,height))
        
        screen.blit(img1, origin1)
        screen.blit(img2, origin2)
    except:
        pass
        
while True: # main game loop
    mouseClicked = False
    if not d.is_empty():
        # draw a card
        c = d.deal_next_card() if random.random()>0.5 else d.get_next_card()
        # Blit the card
        img = pygame.transform.scale(pygame.image.load(str(c)+".PNG"), (width,height))
            
        screen.blit(img, origin1)
        tableau[c] = (origin1, (origin1[0]+width, origin1[1]+height))
        
        if col==(13):
            origin1 = (0, origin1[1] + height)
            row+=1
            col=0
        else:
            origin1 = (origin1[0] + width, origin1[1])
            col+=1
            
        pygame.draw.rect(screen, BACKGROUND, (TEXT_X, TEXT_Y, TEXT_WIDTH, TEXT_HEIGHT))
        textSurfaceObj = fontObj.render(str(c) if c.is_face_up else '', True, TEXTCOLOR)
        screen.blit(textSurfaceObj, (TEXT_X, TEXT_Y))
        
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == MOUSEMOTION:
            mousex, mousey = event.pos
            if d.is_empty():
                pygame.draw.rect(screen, BACKGROUND, (TEXT_X, TEXT_Y, TEXT_WIDTH, TEXT_HEIGHT))
                moused_card = get_moused_card(mousex, mousey)
                textSurfaceObj = fontObj.render(str(moused_card) if moused_card and moused_card.is_face_up else '', True, TEXTCOLOR)
                screen.blit(textSurfaceObj, (TEXT_X, TEXT_Y))
        elif event.type == MOUSEBUTTONDOWN:
            downx, downy = event.pos
        elif event.type == MOUSEBUTTONUP:
            mouseClicked = True
            upx, upy = event.pos
            if upx==downx and upy==downy:
                if d.is_empty(): flip_card(upx,upy)
            else:
                if d.is_empty(): swap_cards(downx,downy,upx,upy)
    pygame.display.update()
    if not d.is_empty(): pygame.time.wait(50)
