import sys, pygame, os, pygame.mixer, random

from pygame.locals import *
from board import *
from ships import *
from AI import *

pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer
BOXSIZE = 25 
GAPSIZE = 5 
BOARDWIDTH = 10 
BOARDHEIGHT = 10 
WINDOWWIDTH = 800 
WINDOWHEIGHT = 600 
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 6)
XMARGIN2 = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 1.15)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
HIGHLIGHTCOLOR = (  0,   0, 255)

def init():
    pygame.init()
    global fpsClock
    fpsClock = pygame.time.Clock()

    size = width, height = 800, 600
    speed = [2, 2]

    global color
    color = {
    'black' : (0, 0, 0),
    'white' : (255, 255, 255),
    'blue' : (0, 0, 255),
    'red' : (255, 0, 0)
    }

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Battleship')
    
    return screen

def title(screen):
    # moved text up here for easy access.
    title = 'Battleship'
    subtitle = 'By Allyn Cheney, Ryan Rapini, and Edward Verhovitz'
    press = 'Press:'
    menu1 = 'F1 for single player game'
    menu2 = 'F2 for network game'
    menu3 = 'F3 to quit'

    # set font
    mainFont = pygame.font.Font('resources/alphbeta.ttf', 100)
    subFont = pygame.font.Font('resources/alphbeta.ttf', 30)
    menuFont = pygame.font.Font('resources/Vera.ttf', 26)

    # set background
    background = 'resources/battleship.jpg'
    background_surface = pygame.image.load(background)
    screen.blit(background_surface, (0, 0))

    # draw title background
    titleSurface = pygame.Surface((800, 130))
    # make background transparent and black
    titleSurface.fill(color['black'])
    titleSurface.set_alpha(200)
    screen.blit(titleSurface, (0, 0))

    # draw title text, centered
    titleText = mainFont.render(title, False, color['white'])
    titleRect = titleText.get_rect()
    titleRect.centerx = 400
    screen.blit(titleText, titleRect)

    # draw subtitle text
    subtitleText = subFont.render(subtitle, False, color['white'])
    titleRect = subtitleText.get_rect()
    titleRect.centerx = 400
    titleRect.top = 90
    screen.blit(subtitleText, titleRect)
    
    # draw menu surface
    # draw title background
    menuSurface = pygame.Surface((400, 275))
    # make background transparent and black
    menuSurface.fill(color['black'])
    menuSurface.set_alpha(200)
    screen.blit(menuSurface, (200, 225))
    
    # draw press text
    menu0color = pygame.Color(255,0,0,0)
    menu0titleText = menuFont.render(press, False, menu0color)
    menuRect = menu0titleText.get_rect()
    menuRect.centerx = 400
    menuRect.top = 240
    screen.blit(menu0titleText, menuRect)
    
     # draw menu1 text
    menu1color = pygame.Color(255,0,0,0)
    menutitleText = menuFont.render(menu1, False, menu1color)
    menuRect = menutitleText.get_rect()
    menuRect.centerx = 400
    menuRect.top = 300
    screen.blit(menutitleText, menuRect)
    
    # draw menu2 text
    menu2color = pygame.Color(255,0,0,0)
    menu2titleText = menuFont.render(menu2, False, menu2color)
    menuRect = menu2titleText.get_rect()
    menuRect.centerx = 400
    menuRect.top = 375
    screen.blit(menu2titleText, menuRect)
    
     # draw menu3 text
    menu3color = pygame.Color(255,0,0,0)
    menu3titleText = menuFont.render(menu3, False, menu3color)
    menuRect = menu3titleText.get_rect()
    menuRect.centerx = 400
    menuRect.top = 450
    screen.blit(menu3titleText, menuRect)
    
def single(screen):
    menu = 'Press F1 for new single Game, F2 for network game, F3 to quit game, F4 to return to menu'
    # set font
    mainFont = pygame.font.Font('resources/Vera.ttf', 16)

    # draw title background
    gameSurface = pygame.Surface((800, 20))
    gameSurface.set_alpha(200)
    screen.fill(color['white'])
    screen.blit(gameSurface, (0, 0))

    # draw title text, centered
    gameText = mainFont.render(menu, False, color['white'])
    gameRect = gameText.get_rect()
    gameRect.centerx = 400
    screen.blit(gameText, gameRect)
    
    myfont = pygame.font.SysFont('resources/alphbeta.ttf', 25)
    label = myfont.render("Attack Board", 1, (255,0,0))
    screen.blit(label, (XMARGIN+90, 100))
    label2 = myfont.render("Player Board", 1, (255,0,0))
    screen.blit(label2, (XMARGIN2+90, 100))
    
    
    
def multi(screen):
    menu = 'Press F1 for new single Game, F2 for network game, F3 to quit game, F4 to return to menu'
    # set font
    mainFont = pygame.font.Font('resources/Vera.ttf', 16)

    # draw title background
    gameSurface = pygame.Surface((800, 20))
    gameSurface.set_alpha(200)
    screen.fill(color['white'])
    screen.blit(gameSurface, (0, 0))

    # draw title text, centered
    gameText = mainFont.render(menu, False, color['white'])
    gameRect = gameText.get_rect()
    gameRect.centerx = 400
    screen.blit(gameText, gameRect)

def drawBoard(board, screen, xm):
    BLANKCOLOR = color['black']
    HITCOLOR = color['red']
    MISSCOLOR = color['blue']
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            left, top = whereisbox(x, y, xm)
            if (board.returnpiece(x,y) == 0):
            	pygame.draw.rect(screen, BLANKCOLOR, (left, top, BOXSIZE, BOXSIZE))
            elif (board.returnpiece(x,y) == 7):
                pygame.draw.rect(screen, MISSCOLOR, (left, top, BOXSIZE, BOXSIZE))
            elif (board.returnpiece(x,y) == 8):
            	pygame.draw.rect(screen, HITCOLOR, (left, top, BOXSIZE, BOXSIZE))
            
def whereisbox(boxx, boxy, xm):
    # Convert board coordinates to pixel coordinates
    left = boxx * (BOXSIZE + GAPSIZE) + xm
    top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
    return (left, top)
    
def whatbox(x, y, xm):
    for boxx in range(BOARDWIDTH):
        for boxy in range(BOARDHEIGHT):
            left, top = whereisbox(boxx, boxy, xm)
            boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
            if boxRect.collidepoint(x, y):
                return (boxx, boxy)
    return (None, None)
   
def main(argv):
    screen = init()
    title(screen)
    gametype = 0
    
    while 1:
        mouseClicked = False
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            if event.type == pygame.QUIT: 
                pygame.quit()
                sys.exit()
            elif pressed[pygame.K_F1]:
                single(screen)
                gametype = 1
                gamestarted = 0
            elif pressed[pygame.K_F2]:
                multi(screen)
                gametype = 2
                gamestarted = 0
            elif pressed[pygame.K_F3]:
                pygame.quit()
                sys.exit()
            elif pressed[pygame.K_F4]:
                title(screen)
                gametype = 0
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True
        if (gametype == 1):
            if (gamestarted == 0):
                playerboard = board()
                playerattackboard = board()
                playerships = ships()
                cpuboard = board()
                cpuattackboard = board()
                cpuships = ships()
                gamestarted = 1
            else:
                drawBoard(playerattackboard, screen, XMARGIN)
                drawBoard(playerboard, screen, XMARGIN2)
                boxx, boxy = whatbox(mousex, mousey, XMARGIN)
                boxx2, boxy2 = whatbox(mousex, mousey, XMARGIN2)
                if (boxx != None and boxy != None):
                    if mouseClicked:
                        print(boxx, boxy)
                        test = playerattackboard.returnpiece(boxx,boxy)
                        print(test)
                elif (boxx2 != None and boxy2 != None) and mouseClicked:
                    if mouseClicked:
                        print(boxx2, boxy2)
        # redraw screen       
        pygame.display.update()
        fpsClock.tick(60)

if __name__ == "__main__":
	main(sys.argv[1:])

