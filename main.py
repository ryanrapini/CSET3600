import sys, pygame
from pygame.locals import *

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
	'purple' : (168, 28, 265)
	}

	screen = pygame.display.set_mode(size)
	pygame.display.set_caption('Battleship')
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
	Defines a button for the main menu.
	"""
	def __init__(self, position, title, action):
		self.position = position
		self.title = title
		self.action = action

	def highlighted(self):
		pass



def menu(screen, hover):
	quit = ""

def main(argv):
	screen = init()

	gamemode = 0

	while 1:
		if gamemode == 0:
			title(screen)
			# menu(screen)
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
