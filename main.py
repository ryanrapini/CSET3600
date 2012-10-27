import sys, pygame
from pygame.locals import *

pygame.init()
fpsClock = pygame.time.Clock()

size = width, height = 1024, 768
speed = [2, 2]

colors = {
	'black' : (0, 0, 0),
	'white' : (255, 255, 255),
	'blue' : (0, 0, 255),
	'red' : (0, 255, 0)
}

screen = pygame.display.set_mode(size)
pygame.display.set_caption('Hello world!')

basicFont = pygame.font.Font('resources/alphbeta.ttf', 48)

def main(argv):
	screen.fill(colors['black'])
	while 1:
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

		screen.fill(colors['black'])

		pygame.display.update()
		fpsClock.tick(30)

if __name__ == "__main__":
    main(sys.argv[1:])