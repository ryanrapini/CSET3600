import sys, pygame, os, pygame.mixer, random
from pygame.locals import *
from board import *
from AI import *

color = {
'black' : (0, 0, 0),
'white' : (255, 255, 255),
'blue' : (0, 0, 255),
'red' : (255, 0, 0),
'green' : (0, 255, 0)
}

BOXSIZE = 25 
GAPSIZE = 5 
BOARDWIDTH = 10 
BOARDHEIGHT = 10 
WINDOWWIDTH = 800 
WINDOWHEIGHT = 600 
XMARGIN = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 6)
XMARGIN2 = int((WINDOWWIDTH - (BOARDWIDTH * (BOXSIZE + GAPSIZE))) / 1.15)
YMARGIN = int((WINDOWHEIGHT - (BOARDHEIGHT * (BOXSIZE + GAPSIZE))) / 2)
HIGHLIGHTCOLOR = color['blue']
shiparray = [6,5,4,3,2]
piecevalue = 1

def loadSound():
    pygame.mixer.pre_init(44100, -16, 2, 2048)  # setup mixer


def seticon():
    # Call this between pygame init and drawing the first window in order to set the icon
    icon=pygame.Surface((32,32))
    # using magic pink as transparent
    icon.set_colorkey((255,0,255))
    rawicon=pygame.image.load('resources/icon.bmp')
    for i in range(0,32):
        for j in range(0,32):
            icon.set_at((i,j), rawicon.get_at((i,j)))
    pygame.display.set_icon(icon)


def init():
    # Initilize Pygame. THIS MUST HAPPEN BEFORE ANYTHING ELSE CAN TOUCH THE PYGAME UTILS.
    try:
        pygame.init()
    except Exception as ex:
        print("Failed to load pygame. Exception is:\n{0}".format(ex))
        # If pygame doesn't load, we might as well just give up.
        sys.exit(1)
    else:
        print("Pygame initilized sucessfully.")

    # Load sound
    try:
        loadSound()
    except Exception as ex:
        print("Failed to load sound. Exception is:\n{0}".format(ex))
    else:
        print("Sound loaded sucessfully.")

    seticon()
    global fpsClock
    fpsClock = pygame.time.Clock()

    size = width, height = 800, 600
    speed = [2, 2]

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Battleship')
    
    return screen


class Button:
    """
    Defines a button for the main outermenu.
    """
    def __init__(self, position, text, action, fontsize = 22):
        self.position = position
        self.title = text
        self.action = action
        self.offset = 15
        self.bgcolor = color['blue']

        self.font = pygame.font.Font('resources/Vera.ttf', fontsize)
        self.buttonText = self.font.render(text, True, color['white'])
        self.buttonRect = self.buttonText.get_rect()
        self.buttonRect.topleft = position

        self.buttonDimensions = (self.buttonRect.left - self.offset, self.buttonRect.top - self.offset, self.buttonRect.width + self.offset * 2, self.buttonRect.height + self.offset * 2)

    def draw(self, screen):
        pygame.draw.rect(screen, self.bgcolor, self.buttonDimensions)
        screen.blit(self.buttonText, self.buttonRect)

    def getBounds(self):
        return pygame.Rect(self.buttonDimensions)

    def highlighted(self, screen):
        self.bgcolor = color['red']


def title(screen, mousex = 0, mousey = 0, mouseClicked = False):
    # moved text up here for easy access.
    title = 'Battleship'
    subtitle = 'By Allyn Cheney, Ryan Rapini, and Edward Verhovitz'

    # Button positioning variables, tweak to adjust. I'd make them autocenter but I'm lazy
    leftoffset = 35
    topoffset = 520
    buttonspacing = 30

    # set font
    mainFont = pygame.font.Font('resources/alphbeta.ttf', 100)
    subFont = pygame.font.Font('resources/alphbeta.ttf', 30)

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

    # load a singleplayer button, draw to screen
    singleplayerButton = Button((leftoffset, topoffset),"Play Singleplayer [F1]",1)
    if (singleplayerButton.getBounds().collidepoint(mousex, mousey)):
        singleplayerButton.highlighted(screen)
    singleplayerButton.draw(screen)

    # load a multiplayer button, draw to screen
    multiplayerButton = Button((singleplayerButton.getBounds().right + buttonspacing, topoffset),"Play Multiplayer [F2]",2)
    if (multiplayerButton.getBounds().collidepoint(mousex, mousey)):
        multiplayerButton.highlighted(screen)
    multiplayerButton.draw(screen)
    
    # load a quit button, draw to screen
    quitButton = Button((multiplayerButton.getBounds().right + buttonspacing, topoffset),"Quit Game [F3]",3)
    if (quitButton.getBounds().collidepoint(mousex, mousey)):
        quitButton.highlighted(screen)
    quitButton.draw(screen)
    
    gamemode = 0
    
    if (mouseClicked):
        if (singleplayerButton.getBounds().collidepoint(mousex, mousey)):
            gamemode = 1
        elif (multiplayerButton.getBounds().collidepoint(mousex, mousey)):
            gamemode = 2
        elif (quitButton.getBounds().collidepoint(mousex, mousey)):
            gamemode = 3

    return gamemode

    
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


def drawboards(attackboard, playerboard, screen, xm1, xm2):
    BLANKCOLOR = color['black']
    HITCOLOR = color['red']
    MISSCOLOR = color['blue']
    SHIPCOLOR = color['green']
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            left1, top1 = whereisbox(x, y, xm1)
            left2, top2 = whereisbox(x, y, xm2)
            if (attackboard.returnpiece(x,y) == 0):
            	pygame.draw.rect(screen, BLANKCOLOR, (left1, top1, BOXSIZE, BOXSIZE))
            elif (attackboard.returnpiece(x,y) == 1):
                pygame.draw.rect(screen, MISSCOLOR, (left1, top1, BOXSIZE, BOXSIZE))
            elif (attackboard.returnpiece(x,y) == 7):
                pygame.draw.rect(screen, MISSCOLOR, (left1, top1, BOXSIZE, BOXSIZE))
            elif (attackboard.returnpiece(x,y) == 8):
            	pygame.draw.rect(screen, HITCOLOR, (left1, top1, BOXSIZE, BOXSIZE))
            if (playerboard.returnpiece(x,y) == 0):
                pygame.draw.rect(screen, BLANKCOLOR, (left2, top2, BOXSIZE, BOXSIZE))
            elif (playerboard.returnpiece(x,y) == 1):
                pygame.draw.rect(screen, MISSCOLOR, (left2, top2, BOXSIZE, BOXSIZE))
            elif (playerboard.returnpiece(x,y) == 7):
                pygame.draw.rect(screen, MISSCOLOR, (left2, top2, BOXSIZE, BOXSIZE))
            elif (playerboard.returnpiece(x,y) == 8):
                pygame.draw.rect(screen, HITCOLOR, (left2, top2, BOXSIZE, BOXSIZE))
            
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
    print ("Drawing main menu.")
    title(screen)
    gamemode = 0
    gamestarted = 0
    
    while 1:
        mouseClicked = False
        for event in pygame.event.get():
            pressed = pygame.key.get_pressed()
            # If the user clicks the x at the top of the window
            if event.type == pygame.QUIT: 
                gamemode = 3

            # If the user presses F1
            elif pressed[pygame.K_F1]:
                gamemode = 1

            # If the user presses F2
            elif pressed[pygame.K_F2]:
                gamemode = 2

            # If the user presses F3
            elif pressed[pygame.K_F3]:
                gamemode = 3

            # If the user presses F4
            elif pressed[pygame.K_F4]:
                gamemode = 0

            # If the mouse is moved, record the current coordinates
            elif event.type == MOUSEMOTION:
                mousex, mousey = event.pos

            # If the mouse is clicked, say so and record the current coordinates
            elif event.type == MOUSEBUTTONUP:
                mousex, mousey = event.pos
                mouseClicked = True

        # If we're in gamemode 0, show the titlescreen
        if (gamemode == 0):
            gamemode = title(screen, mousex, mousey, mouseClicked)

        # If we're in gamemode 1, show the game screen
        if (gamemode == 1):
            if (gamestarted == 0):
                print ("Starting a new game")
                single(screen)
                playerboard = board()
                playerattackboard = board()
                cpuboard = board()
                cpuattackboard = board()
                comp = AI()
                comp.placeships(shiparray, piecevalue, playerboard)
                gamestarted = 1
            else:
                drawboards(playerattackboard, playerboard, screen, XMARGIN, XMARGIN2)
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
                        test = playerboard.returnpiece(boxx2,boxy2)
                        print(test)

        # If we're in gamemode 2, show the multiplayer screen
        if (gamemode == 2):
            multi(screen)
            pass

        # If we're in gamemode 3, we're quitting
        if (gamemode == 3):
            screen.fill(color['black'])
            font = pygame.font.Font('resources/alphbeta.ttf', 70)
            thanks = font.render("Thanks for playing!", False, color['white'])
            thanksRect = thanks.get_rect()
            thanksRect.center = (400, 300)
            screen.blit(thanks, thanksRect)

            pygame.display.update()
            print('Quitting :[')

            pygame.time.wait(500)
            pygame.quit()
            sys.exit(0)
        # redraw screen       
        pygame.display.update()
        fpsClock.tick(60)

if __name__ == "__main__":
	main(sys.argv[1:])

