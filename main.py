import sys, pygame
from pygame.locals import *

class Ship:
	"""Generates a single battleship."""
	def __init__(self):
		self.size = 0

	def set(self, values):


def init():
	pygame.init()
	global fpsClock 
	fpsClock = pygame.time.Clock()

	size = width, height = 800, 600
	speed = [2, 2]

	colors = {
	'black' : (0, 0, 0),
	'white' : (255, 255, 255),
	'blue' : (0, 0, 255),
	'red' : (0, 255, 0)
	}

	screen = pygame.display.set_mode(size)
	pygame.display.set_caption('Battleship')
	return screen

def menu():
	mainFont = pygame.font.Font('resources/alphbeta.ttf', 100)

	background = 'resources/battleship.jpg'
	background_surface = pygame.image.load(background)
	screen.blit(background_surface, (0,0))
	pygame.display.flip() 

	text = mainFont.render('Battleship', False, colors['white'], colors['black'])

	# Create a rectangle
	textRect = text.get_rect()


	# Blit the text
	screen.blit(text, textRect)

def main(argv):
	screen = init()
	gamemode = 0
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

		pygame.display.update()
		fpsClock.tick(30)

if __name__ == "__main__":
	main(sys.argv[1:])
