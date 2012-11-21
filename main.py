import sys, pygame, os, pygame.mixer
import easygui

from pygame.locals import *


pygame.mixer.pre_init(44100, -16, 2, 2048) # setup mixer

#hit = pygame.mixer.Sound(os.path.join('resoureces/hit.wav'))  #load sound
#miss = pygame.mixer.Sound(os.path.join('resoureces/miss.wav'))  #load sound
#lasthit = pygame.mixer.Sound(os.path.join('resources/lasthit.wav'))  #load sound


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
    'red' : (0, 255, 0)
    }

    screen = pygame.display.set_mode(size)
    pygame.display.set_caption('Battleship')

    hit = pygame.mixer.Sound(os.path.join('resources/hit.wav')) #load hit sound
    miss = pygame.mixer.Sound(os.path.join('resources/miss.wav')) #load miss sound
    lasthit = pygame.mixer.Sound(os.path.join('resources/lasthit.wav')) #load lasthit sound
    return screen

def title(screen):
    # moved text up here for easy access.
    title = 'Battleship'
    subtitle = 'By Allyn Cheney, Ryan Rapini, and Edward Verhovitz'

    # set font
    mainFont = pygame.font.Font('resources/alphbeta.ttf', 100)
    subFont = pygame.font.Font('resources/alphbeta.ttf', 30)

    # set background
    background = 'resources/battleship.jpg'
    background_surface = pygame.image.load(background)
    screen.blit(background_surface, (0,0))

    # draw title background
    titleSurface = pygame.Surface((800,130))
    # make background transparent and black
    titleSurface.fill(color['black'])
    titleSurface.set_alpha(200)
    screen.blit(titleSurface, (0,0))

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

class Button:
    """
    Defines a button for the main outermenu.
    """
    def __init__(self, position, text, action, screen):
        self.position = position
        self.title = text
        self.action = action
        self.offset = 15
        
        font = pygame.font.Font('resources/alphbeta.ttf', 30)
        buttonText = font.render(text, False, color['white'])
        buttonRect = buttonText.get_rect()
        buttonRect.center = position

        buttonDimensions = (buttonRect.left - self.offset, buttonRect.top - self.offset, buttonRect.width + self.offset * 2, buttonRect.height + self.offset * 2)
        pygame.draw.rect(screen, color['red'], buttonDimensions)

        screen.blit(buttonText, buttonRect)

    def highlighted(self):
        self.color = color['red']


def outermenu():
    resolution = [640,480]
    msg = "This is BattleShip!"
    buttons = ["Single Player Game", "Network Game", "Quit"]
    picture = None # gif file
    while True: #endless loop
        title = "Welcome To BattleShip! Developed by Team Lazer Explosion!"
        selection = easygui.buttonbox(msg, title, buttons, picture)
        if selection == "Quit":
            easygui.msgbox("Quitter!")
            sys.exit(0)
        elif selection == "Single Player Game":
            msg = "Single Player Game Selected." #load board and AI
            break
        elif selection == "Network Game":
            msg = "Multiplayer Game Selected."
            break
            ##load board and netcoding 
    return 


def menu(screen):
    title(screen)
    singleplayer = Button((100,20),"Play",1,screen)
    # singleplayer.

def main(argv):
	screen = init()
	gamemode = 0

	while 1:
		if gamemode == 0:
			menu(screen)
		elif gamemode == 1:
			game(screen)

		for event in pygame.event.get():
			if event.type == pygame.QUIT: 
				pygame.quit()
				sys.exit()
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONDOWN:
				mousex, mousey = event.pos
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos

		pygame.display.update()
		fpsClock.tick(30)

if __name__ == "__main__":
	main(sys.argv[1:])