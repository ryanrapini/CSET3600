import sys, pygame
from pygame.locals import *

class Ship:
	"""
	Generates a single battleship.

	Position is calculated by a given x and y coord, a ship size, and an alignment
	which are then used to calculate the entire array of values for the ship.
	"""
	def __init__(self, size, alignment, x, y):
		self.size = size
		self.health = self.size
		self.alignment = alignment
		self.x = [x]
		self.y = [y]

		if (self.size > 5 or self.size < 2):
			return False 

		# Generate our array of ship positions.
		if (self.alignment == "h"):
			self.x = range(self.x[0], self.x[0] + self.size)

		if (self.alignment == "v"):
			self.y = range(self.y[0], self.y[0] + self.size)

		# Do some checks to make sure our positions are sane and don't leave the board
		# maybe this stuff should be moved elsewhere but for now it's going here
		if (len(self.x) - 1 >= 20):
			return False

		if (len(self.y) - 1 >= 20):
			return False

	def isHit(x,y):
		if x in self.x:
			if y in self.y:
				self.health -= 1
				return True
		return False


	def isSunk():
		if (self.health <= 0):
			return True
		else:
			return False


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
	return screen


def title(screen):
	# moved text up here for easy access.
	title = 'Battleshit'
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
	Defines a button 
	"""
	def __init__(self, position, ):
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
