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

basicFont = pygame.font.Font('../resources/alphbeta.ttf', 48)

def printCoords(x,y):
	text = basicFont.render('X:{0} Y:{1}'.format(x,y), False, colors['white'], colors['blue'])
	screen.blit(text, (x,y))
	return True

def main(argv):

	text = basicFont.render('Hello world!', False, colors['white'], colors['blue'])
	textRect = text.get_rect()
	textRect.centerx = screen.get_rect().centerx
	textRect.centery = screen.get_rect().centery
	
	screen.fill(colors['black'])

	pygame.draw.rect(screen, colors['red'], (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))
	screen.blit(text, (100,100))

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

		pygame.draw.rect(screen, colors['red'], (textRect.left - 20, textRect.top - 20, textRect.width + 40, textRect.height + 40))
		screen.blit(text, textRect)

		printCoords(mousex,mousey)



		pygame.display.update()
		fpsClock.tick(30)

if __name__ == "__main__":
    main(sys.argv[1:])