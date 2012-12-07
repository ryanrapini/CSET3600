import sys, pygame, os, random, textrect, socket, pygame.mixer
from pygame.locals import *
from board import *
from AI import *
from server import *
from client import *


color = {
'black' : (0, 0, 0),
'white' : (255, 255, 255),
'gray' : (100, 100, 100),
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

shiparray = [6,5,4,3,2]

def loadSound():
	"""Loads the PyGame Sound Mixer and initializes the frequency, size, number of channels, and buffersize."""
	# Setup mixer
	pygame.mixer.pre_init(22050, -16, 2, 4098)


def seticon():
	"""Sets the icon of the game.

	The icon image is loaded from the resources folder and sets the image.

	"""
	# Call this between pygame init and drawing the first window in order to set the icon
	icon=pygame.Surface((32,32))
	# Using magic pink as transparent
	icon.set_colorkey((255,0,255))
	rawicon=pygame.image.load('resources/icon.bmp')
	for i in range(0,32):
		for j in range(0,32):
			icon.set_at((i,j), rawicon.get_at((i,j)))
	pygame.display.set_icon(icon)


def getIP():
	"""For multiplayer purposes only.

	A socket is created to report local IP addresses of the two players.
	Once connection has been established, multiplayer games can be played.

	"""
	# Create a dummy socket to report local IP address
	s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	s.connect(('google.com', 0))
	return s.getsockname()[0]


def init():
	"""Initializes all parameters of The game.

	Pygame is the first to be initialized due to the extensive use of it's libraries.
	Sound is initialized through the loudSound class.
	The icon for the game is set.
	The clock is declared as a global element and the speed of the clock is set.
	The screen for which our the funcitonal aspects of the game lie is set to sized and the window caption
	is applied.

	"""
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
		global soundon
		soundon = 1
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
	"""Defines a button for the main menu."""
	def __init__(self, position, text, fontsize = 22):
		self.position = position
		self.title = text
		self.offset = 15
		self.bgcolor = color['blue']

		self.font = pygame.font.Font('resources/Vera.ttf', fontsize)
		self.buttonText = self.font.render(text, True, color['white'])
		self.buttonRect = self.buttonText.get_rect()
		self.buttonRect.topleft = position

		self.buttonDimensions = (self.buttonRect.left - self.offset, self.buttonRect.top - self.offset, self.buttonRect.width + self.offset * 1.75, self.buttonRect.height + self.offset * 1.75)

	def draw(self, screen):
		"""Draws buttons and places them on the screen."""
		pygame.draw.rect(screen, self.bgcolor, self.buttonDimensions)
		screen.blit(self.buttonText, self.buttonRect)

	def getBounds(self):
		"""Sets the size of the buttons."""
		return pygame.Rect(self.buttonDimensions)

	def highlighted(self, screen):
		"""If button is moused over, the background color is set to Red."""
		self.bgcolor = color['red']


def title(screen, mousex = -1, mousey = -1, mouseClicked = False):
	"""The screen of the game is displayed with many initialized parameters.

	The title and subtitle are set to display the name of the game and the authors.
	Font is loaded from the resources folder and set to the font variables.
	The background image is loaded from the resources folder and placed as the backdrop of the menu.
	The buttons are placed on the screen with specified locations and captions.
	A series of if statements determine which button is clicked and calls the actions in the main arguments
	for each respective button.

	"""
	
	# Text on the menu displaying game name and creators/masters
	title = 'Battleship'
	subtitle = 'By Allyn Cheney, Ryan Rapini, and Edward Verhovitz'

	# Button positioning variables, tweak to adjust. I'd make them autocenter but I'm lazy
	centeroffset = 200
	leftoffset = 55
	leftoffset2 = 33
	topoffset = 475
	topoffset2 = 550
	buttonspacing = 30

	# Set font
	mainFont = pygame.font.Font('resources/alphbeta.ttf', 100)
	subFont = pygame.font.Font('resources/alphbeta.ttf', 28)

	# Set background
	background = 'resources/battleship.jpg'
	background_surface = pygame.image.load(background)
	screen.blit(background_surface, (0, 0))

	# Draw title background
	titleSurface = pygame.Surface((800, 130))
	# make background transparent and black
	titleSurface.fill(color['black'])
	titleSurface.set_alpha(200)
	screen.blit(titleSurface, (0, 0))

	# Draw title text, centered
	titleText = mainFont.render(title, False, color['white'])
	titleRect = titleText.get_rect()
	titleRect.centerx = 400
	screen.blit(titleText, titleRect)

	# Draw subtitle text
	subtitleText = subFont.render(subtitle, False, color['white'])
	titleRect = subtitleText.get_rect()
	titleRect.centerx = 400
	titleRect.top = 90
	screen.blit(subtitleText, titleRect)

	# Load a singleplayer button, draw to screen
	singleplayereasyButton = Button((leftoffset2, topoffset),"  Play Easy CPU [F1]  ", 20)
	if (singleplayereasyButton.getBounds().collidepoint(mousex, mousey)):
		singleplayereasyButton.highlighted(screen)
	singleplayereasyButton.draw(screen)
	
	# Load a singleplayer button, draw to screen
	singleplayerhardButton = Button((singleplayereasyButton.getBounds().right + buttonspacing, topoffset)," Play Harder CPU [F2] ", 20)
	if (singleplayerhardButton.getBounds().collidepoint(mousex, mousey)):
		singleplayerhardButton.highlighted(screen)
	singleplayerhardButton.draw(screen)
	
	# Load a singleplayer button, draw to screen
	singleplayerhardestButton = Button((singleplayerhardButton.getBounds().right + buttonspacing, topoffset),"Play Hardest CPU [F3]", 20)
	if (singleplayerhardestButton.getBounds().collidepoint(mousex, mousey)):
		singleplayerhardestButton.highlighted(screen)
	singleplayerhardestButton.draw(screen)

	# Load a multiplayer button, draw to screen
	multiplayerButton = Button((leftoffset, topoffset2)," Play Multiplayer [F4] ", 20)
	if (multiplayerButton.getBounds().collidepoint(mousex, mousey)):
		multiplayerButton.highlighted(screen)
	multiplayerButton.draw(screen)
	
	# Load a soundOnOff button, draw to screen
	soundButton = Button((multiplayerButton.getBounds().right + buttonspacing, topoffset2)," Sound On/Off [F6] ", 20)
	if (soundButton.getBounds().collidepoint(mousex, mousey)):
		soundButton.highlighted(screen)
	soundButton.draw(screen)
	
	# Load a quit button, draw to screen
	quitButton = Button((soundButton.getBounds().right + buttonspacing, topoffset2),"  Quit Game [F12]  ", 20)
	if (quitButton.getBounds().collidepoint(mousex, mousey)):
		quitButton.highlighted(screen)
	quitButton.draw(screen)

	
	gamemode = 0
	global gamedifficulty
	global soundon
	
	if (mouseClicked):
		if (singleplayereasyButton.getBounds().collidepoint(mousex, mousey)):
			gamemode = 1
			gamedifficulty = 0
		elif (singleplayerhardButton.getBounds().collidepoint(mousex, mousey)):
			gamemode = 1
			gamedifficulty = 1
		elif (singleplayerhardestButton.getBounds().collidepoint(mousex, mousey)):
			gamemode = 1
			gamedifficulty = 2
		elif (multiplayerButton.getBounds().collidepoint(mousex, mousey)):
			gamemode = 2
		elif (quitButton.getBounds().collidepoint(mousex, mousey)):
			gamemode = 4
		elif (soundButton.getBounds().collidepoint(mousex, mousey)):
			if (soundon == 1):
				pygame.mixer.pause()
				soundon = 0
			elif (soundon == 0):
				pygame.mixer.unpause()
				soundon = 1
				

	return gamemode


def single(screen):
	"""Displays the screen for single player mode.

	The menu is written onto the board with options to start a new game, return to the menu, and quit.
	As with the main menu screen, the font and background image is set from the resources folder.
	Labels for each playing board are drawn on the surface.

	"""
	# Set font
	menu = '[F1] Easy SP Game | [F2] Hard SP Game | [F3] Hardest SP Game | [F4] Network Game | [F5] Main Menu | [F6] Sound On/Off | [F12] Quit'
	mainFont = pygame.font.Font('resources/Vera.ttf', 11)

	# Draw title background
	gameSurface = pygame.Surface((800, 15))
	gameSurface.set_alpha(200)
	screen.fill(color['white'])
	screen.blit(gameSurface, (0, 0))

	# Draw title text, centered
	gameText = mainFont.render(menu, False, color['white'])
	gameRect = gameText.get_rect()
	gameRect.centerx = 400
	screen.blit(gameText, gameRect)
	
	# Draw title text, centered
	#gameText = mainFont.render(menu2, False, color['white'])
	#gameRect = gameText.get_rect()
	#gameRect.centerx = 400
	#gameRect.top = 20
	#screen.blit(gameText, gameRect)
	
	myfont = pygame.font.SysFont('resources/alphbeta.ttf', 25)
	label = myfont.render("Attack Board", 1, (255,0,0))
	screen.blit(label, (XMARGIN+90, 100))
	label2 = myfont.render("Player Board", 1, (255,0,0))
	screen.blit(label2, (XMARGIN2+90, 100))


def singleinstructions(screen, text, text2, yloc, yloc2):
	"""Displays the instuctions for single play mode."""
	single(screen)
	myfont = pygame.font.SysFont('resources/alphbeta.ttf', 25)
	label = myfont.render(text, 1, (255,0,0))
	screen.blit(label, (200, yloc))
	label2 = myfont.render(text2, 1, (255,0,0))
	screen.blit(label2, (20, yloc2))


def printstatus(screen, text):
	"""Displays the current status of play.

	When the player hits or misses on the board, a status message displays
	whether it was a hit or a miss.

	"""
	single(screen)
	myfont = pygame.font.SysFont('resources/alphbeta.ttf', 25)
	label4 = myfont.render(text, 1, (255,0,0))
	screen.blit(label4, (200, 475))


def textbox(screen, position, message):
	"""Prints an onscreen message."""
	mainFont = pygame.font.Font('resources/Vera.ttf', 20)
	textbox = pygame.Rect(position[0]-10, position[1]-5, 200, 36)

	pygame.draw.rect(screen, color['black'], textbox, 0)
	pygame.draw.rect(screen, color['white'], textbox, 2)

	if len(message) != 0:
		screen.blit(mainFont.render(message, True, color['white']),position)


def multi(screen, enteredip, mousex = -1, mousey = -1, mouseClicked = False):
	"""Displays the screen for a multiplayer game.

	The menu is drawn to the screen with options to start a new game, return to the main menu, or quit.
	Instructions for setting up a game server are printed to the screen.
	In multiplayer mode, the game requires the ip addresses of both players.
	More to be had here once Multiplayer is finished.

	"""
	menu = '[F1] Easy SP Game  |  [F2] Hard SP Game  |  [F3] Hardest SP Game  |  [F4] Network Game  |  [F5] Main Menu  | [F6] Sound On/Off |  [F12] Quit'
	# Set font
	mainFont = pygame.font.Font('resources/Vera.ttf', 10)
	screen.fill(color['black'])

	# Draw title text, centered
	gameText = mainFont.render(menu, True, color['white'])
	gameRect = gameText.get_rect()
	gameRect.center = (400, 18)
	mainFont = pygame.font.Font('resources/Vera.ttf', 16)

	screen.blit(gameText, gameRect)

	netstatus = "In progress..."
	ip = "Unknown"
	ip = getIP()

	mainstring = "Welcome to Battleship Multiplayer!\
	\n\n===== Instructions =====\
	\n\nIn order for multiplayer to work, you must have an internet connection (duh!)\
	\n\nIf you are planning to host the server, then give your IP address (shown below!) to your friend and then click the 'Create Server' button.\
	\n\nIf you are connecting to a friend's server, type in your friend's IP address in the box below, and then click the 'Join Server' button.\
	\n\nThere is a 60 second time limit on moves or your turn will be forfeit! If you forfeit three turns in a row, you will lose the game!\
	\n\n===== Information =====\
	\n\nTesting for a network connection: {0}\
	\n\nYour IP is: {1}\
	\n\n".format(netstatus, ip)
	stringrect = pygame.Rect((45, 45, 710, 450))

	offset = 10

	backgroundbox = (stringrect.left - offset, stringrect.top - offset, stringrect.width + offset * 2, stringrect.height + offset * 2)

	rendered_text = textrect.render_textrect(mainstring, mainFont, stringrect, color['white'], color['gray'], 0)

	pygame.draw.rect(screen, color['gray'],backgroundbox)
	
	screen.blit(rendered_text, (45,45))
	
	topoffset = 540
	buttonspacing = 30

	# Load a singleplayer button, draw to screen
	createserverButton = Button((50,topoffset),"Create Server")
	if (createserverButton.getBounds().collidepoint(mousex, mousey)):
		createserverButton.highlighted(screen)
	createserverButton.draw(screen)

	# Load a multiplayer button, draw to screen
	joinserverButton = Button((createserverButton.getBounds().right + buttonspacing, topoffset),"Join Server" + " "*32)
	if (joinserverButton.getBounds().collidepoint(mousex, mousey)):
		joinserverButton.highlighted(screen)
	joinserverButton.draw(screen)
	
	# Load a quit button, draw to screen
	menuButton = Button((joinserverButton.getBounds().right + buttonspacing, topoffset),"Main Menu")
	if (menuButton.getBounds().collidepoint(mousex, mousey)):
		menuButton.highlighted(screen)
	menuButton.draw(screen)
	
	option = 0

	textbox(screen, (joinserverButton.getBounds().centerx-25,topoffset),enteredip)
	
	if (mouseClicked):
		if (createserverButton.getBounds().collidepoint(mousex, mousey)):
			option = 1
		elif (joinserverButton.getBounds().collidepoint(mousex, mousey)):
			option = 2
		elif (menuButton.getBounds().collidepoint(mousex, mousey)):
			option = 3

	return option


def drawboards(attackboard, playerboard, screen, xm1, xm2):
	"""Drawing of the attckboard player board, and screen are defined.

	Colors are given to the spaces of where the ship is placed(green), hit(red), and where misses occur(blue.)
	Once a box on the player or attack board has been clicked, a loop is used to determine
	if the box clicked was a placed shit, hit, or miss.

	"""
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
			elif (attackboard.returnpiece(x,y) == 2) or (attackboard.returnpiece(x,y) == 3) or (attackboard.returnpiece(x,y) == 4) or (attackboard.returnpiece(x,y) == 5) or (attackboard.returnpiece(x,y) == 6):
				pygame.draw.rect(screen, HITCOLOR, (left1, top1, BOXSIZE, BOXSIZE))
			if (playerboard.returnpiece(x,y) == 0):
				pygame.draw.rect(screen, BLANKCOLOR, (left2, top2, BOXSIZE, BOXSIZE))
			elif (playerboard.returnpiece(x,y) == 1):
				pygame.draw.rect(screen, MISSCOLOR, (left2, top2, BOXSIZE, BOXSIZE))
			elif (playerboard.returnpiece(x,y) == 2) or (playerboard.returnpiece(x,y) == 3) or (playerboard.returnpiece(x,y) == 4) or (playerboard.returnpiece(x,y) == 5) or (playerboard.returnpiece(x,y) == 6):
				pygame.draw.rect(screen, SHIPCOLOR, (left2, top2, BOXSIZE, BOXSIZE))
			elif (playerboard.returnpiece(x,y) == 7):
				pygame.draw.rect(screen, MISSCOLOR, (left2, top2, BOXSIZE, BOXSIZE))
			elif (playerboard.returnpiece(x,y) == 8):
				pygame.draw.rect(screen, HITCOLOR, (left2, top2, BOXSIZE, BOXSIZE))


def checkforwin(board):
	"""Checking for a win."""
	winarray = [0,0,0,0,0,0,0,0]
	win = False
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			temp = board.returnpiece(x,y)
			winarray[temp] = winarray[temp] + 1
	temp2 = 2
	while(temp2 < 7):
		if winarray[temp2] == temp2:
			win = True
		else:
			win = False
			break
		temp2 = temp2 + 1
	return win


def checkforshipsunk(board, piece, screen):
	"""Checking for a sunk ship on attack and player boards."""
	sunk = False
	hold = 0
	for x in range(BOARDWIDTH):
		for y in range(BOARDHEIGHT):
			if (board.returnpiece(x,y) == piece):
			   hold = hold + 1
	if (hold == piece):
		if (piece == 6):
			printstatus(screen, 'You sunk my Aircraft Carrier!')
		elif (piece == 5):
			printstatus(screen, 'You sunk my Battleship!')
		elif (piece == 4):
			printstatus(screen, 'You sunk my Submarine!')
		elif (piece == 3):
			printstatus(screen, 'You sunk my Destroyer!')
		elif (piece == 2):
			printstatus(screen, 'You sunk my Patrol Boat!')


def whereisbox(boxx, boxy, xm):
	# Convert board coordinates to pixel coordinates
	left = boxx * (BOXSIZE + GAPSIZE) + xm
	top = boxy * (BOXSIZE + GAPSIZE) + YMARGIN
	return (left, top)


def whatbox(x, y, xm):
	# Determines which box has been selected
	for boxx in range(BOARDWIDTH):
		for boxy in range(BOARDHEIGHT):
			left, top = whereisbox(boxx, boxy, xm)
			boxRect = pygame.Rect(left, top, BOXSIZE, BOXSIZE)
			if boxRect.collidepoint(x, y):
				return (boxx, boxy)
	return (None, None)


def multiplayer_game(ip):
	if ip:
		#We are the client
		if try_connect(ip):
			print ("Connected to server sucessfully")
		else:
			print ("No IP entered or could not connect.")
	else:
		# We are the server
		# Spawn a server process, leave it alone.
		print ("Starting Server...")
		ip = socket.gethostname()
		serv = Server()
		servthread = Thread(target=serv.listen, args=())
		servthread.start()

	s = get_socket(ip)
	preamble = get_preamble(s)

	print (preamble)

	# board = get_board(s)

	# # if send_board(s,gameboard):
	# # 	print ("Move submitted!")

	# pp = pprint.PrettyPrinter(indent=4)
	# pp.pprint (board)

	s.close()


def log_move(message, board):
	f = open('logfile.txt','a', encoding='utf8')
	f.write('{}\n'.format(message))
	for row in board:
		f.write(" ".join(str(item) for item in row))
		f.write('\n')
	f.close()


def main(argv):
	"""The main arguments occur.

	All variables are initialized and set to the respective values, whether an integer or a class definition.
	All mouse motion is tracked once clicked, given statements for the click event
	such as selecting which level of game to play, sound on/off, and exiting the game execute.
	Once a game is selected, the board loads with instructions for placing pieces  on the board.
	The game starts as soon as the last piece(patrol boat) is placed on the player's board.
	Once a ship has been sunk, a message will display saying that respective ship has been destroyed
	and if the final ship is sunk, a winning message will dispaly.
	A new game can be started at any time using the F keys to select which level of play, turn on/off sound, or
	to return to the main menu as well as quit the game.
	All actions on the boards are set to be logged in a seperate text file for documentation and debugging.

	"""
	screen = init()
	print ("Drawing main menu.")
	title(screen)
	gamemode = 0
	global gamedifficulty
	global soundon
	gamestarted = False
	spacetaken = 0
	direction = 0
	turn = 0
	hit = pygame.mixer.Sound('resources\hit.ogg')
	miss = pygame.mixer.Sound('resources\miss.ogg')
	music = pygame.mixer.Sound('resources\TheLibertyBellMarch.ogg')

	# Continuous music
	music.play(loops = -1) 

	#get current hostname
	enteredip = list(socket.gethostbyname(socket.gethostname()))
	socket.gethostbyname(socket.gethostname())
	while 1:
		mouseClicked = False
		for event in pygame.event.get():
			pressed = pygame.key.get_pressed()
			# If the user clicks the x at the top of the window
			if event.type == pygame.QUIT: 
				gamemode = 4

			# If the user presses F1
			elif pressed[pygame.K_F1]:
				gamemode = 1
				gamestarted = False
				gamedifficulty = 0
			# If the user presses F2
			elif pressed[pygame.K_F2]:
				gamemode = 1
				gamestarted = False
				gamedifficulty = 1
			# If the user presses F3
			elif pressed[pygame.K_F3]:
				gamemode = 1
				gamestarted = False
				gamedifficulty = 2
			# If the user presses F4
			elif pressed[pygame.K_F4]:
				gamemode = 2
				gamestarted = False

			# If the user presses F5
			elif pressed[pygame.K_F5]:
				gamemode = 0
				gamestarted = False

			#If the user presses F6
			elif pressed[pygame.K_F6]:
				if (soundon == 1):
					pygame.mixer.pause()
					soundon = 0
				elif (soundon == 0):
					pygame.mixer.unpause()
					soundon = 1
				
			#If the user presses F12
			elif pressed[pygame.K_F12]:
				gamemode = 4

			# If the mouse is moved, record the current coordinates
			elif event.type == MOUSEMOTION:
				mousex, mousey = event.pos

			# If the mouse is clicked, say so and record the current coordinates
			elif event.type == MOUSEBUTTONUP:
				mousex, mousey = event.pos
				mouseClicked = True

			# Blanket catch for any other key press, keep this at the end!
			elif event.type == KEYDOWN:
				if event.key == K_BACKSPACE:
					enteredip = enteredip[0:-1]
				elif event.key == K_RETURN:
					pass
				elif (event.key >= 48 and event.key <= 57) or event.key == 46:
					enteredip.append(chr(event.key))

		# If we're in gamemode 0, show the titlescreen
		if (gamemode == 0):
			gamemode = title(screen, mousex, mousey, mouseClicked)
			if gamemode != 0:
				continue

		# If we're in gamemode 1, show the game screen
		if (gamemode == 1):
			if not gamestarted:
				print ("Starting a new game")
				single(screen)
				place = 0
				spacetaken = 0
				turn = 0
				playerboard = board()
				playerattackboard = board()
				cpuboard = board()
				cpuattackboard = board()
				comp = AI()
				comp.placeships(shiparray, cpuboard)
				gamestarted = True
			else:
				if (place == 0):
					singleinstructions(screen, 'Please place the Aircraft Carrier on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 1):
					singleinstructions(screen, 'Please place the Battleship on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 2):
					singleinstructions(screen, 'Please place the Submarine on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 3):
					singleinstructions(screen, 'Please place the Destroyer on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 4):
					singleinstructions(screen, 'Please place the Patrol Boat on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 5):
					singleinstructions(screen, 'Please select spot on attack board to start game', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				#else:
					#singleinstructions(screen, '', '', 475, 500)
				drawboards(playerattackboard, playerboard, screen, XMARGIN, XMARGIN2)
				boxx2, boxy2 = whatbox(mousex, mousey, XMARGIN2)
				# user places ships on board
				if (boxx2 != None and boxy2 != None) and mouseClicked:
					if (place < 5):
						checkplace = 0
						spacepressed = pressed[pygame.K_SPACE]
						if not (spacepressed):
							hold = boxy2
							if ((shiparray[place]+boxy2) < 11):
								if (checkplace == 0):
									for y in range(shiparray[place]): 
										if ((playerboard.returnpiece(boxx2,hold)) != 0):
											checkplace = 1
										else:
											hold = hold + 1
								for y in range(shiparray[place]): 
									if (checkplace == 1):
										break
									else:
										playerboard.setpiece(shiparray[place],boxx2,boxy2)
										boxy2 = boxy2 + 1
										if (y == (shiparray[place]-1)):
											place = place + 1
						elif (spacepressed):
							hold = boxx2
							if ((shiparray[place]+boxx2) < 11):
								if (checkplace == 0):
									for x in range(shiparray[place]): 
										if ((playerboard.returnpiece(hold,boxy2)) != 0):
											checkplace = 1
										else:
											hold = hold + 1
								for x in range(shiparray[place]): 
									if (checkplace == 1):
										break
									else:
										playerboard.setpiece(shiparray[place],boxx2,boxy2)
										boxx2 = boxx2 + 1
										if (x == (shiparray[place]-1)):
											place = place + 1
				boxx, boxy = whatbox(mousex, mousey, XMARGIN)
				# game ready to play
				if (place >= 5):
					if (turn == 0):
						if (boxx != None and boxy != None) and mouseClicked:
							place = place + 1
							temp = cpuboard.checkforhitormiss(boxx,boxy)
							if (temp == 9):
								blah = 0
							else:
								playerattackboard.setpiece(temp,boxx,boxy)
								log_move('Player Move', playerattackboard.returnboard())
								
								if (temp == 7):
									printstatus(screen, 'Miss')
									miss.play(loops = 0)
								else:
									printstatus(screen, 'Hit')
									hit.play(loops = 0)
								if (checkforwin(playerattackboard)):
									printstatus(screen, 'You win!')
									turn = -1
								else:
									checkforshipsunk(playerattackboard, temp, screen)
									turn = 1
					elif (turn == 1):
						if (gamedifficulty == 0):
							comp.attack(playerboard, cpuattackboard)
							log_move('Easy CPU Move', cpuattackboard.returnboard())

						elif (gamedifficulty == 1):
							comp.attack2(playerboard, cpuattackboard)
							log_move('Harder CPU Move', cpuattackboard.returnboard())

						elif (gamedifficulty == 2):
							comp.attack3(playerboard, cpuattackboard)
							log_move('Hardest CPU Move', cpuattackboard.returnpiece(b,a))

						if (checkforwin(cpuattackboard)):
							printstatus(screen, 'Computer Wins!')
							turn = -1
						else:
							turn = 0  

		# If we're in gamemode 2, show the multiplayer screen
		if (gamemode == 2):

			option = multi(screen, "".join(enteredip), mousex, mousey, mouseClicked)

			if (option == 1):
				multiplayer_game(None)
				gamemode = 3

			elif (option == 2):
				ip = "".join(enteredip)
				multiplayer_game(ip)
				gamemode = 3

			elif (option == 3):
				gamemode = 0

		if (gamemode == 3):
			if not gamestarted:
				print ("Starting a new game")
				single(screen)
				place = 0
				spacetaken = 0
				turn = 0
				playerboard = board()
				playerattackboard = board()
				cpuboard = board()
				cpuattackboard = board()
				comp = AI()
				comp.placeships(shiparray, cpuboard)
				gamestarted = True
			else:
				if (place == 0):
					singleinstructions(screen, 'Please place the Aircraft Carrier on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 1):
					singleinstructions(screen, 'Please place the Battleship on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 2):
					singleinstructions(screen, 'Please place the Submarine on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 3):
					singleinstructions(screen, 'Please place the Destroyer on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 4):
					singleinstructions(screen, 'Please place the Patrol Boat on your board!', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				elif (place == 5):
					singleinstructions(screen, 'Please select spot on attack board to start game', 'Click to place ships down from point, hold space and click to place ships right from point', 475, 500)
				#else:
					#singleinstructions(screen, '', '', 475, 500)
				drawboards(playerattackboard, playerboard, screen, XMARGIN, XMARGIN2)
				boxx2, boxy2 = whatbox(mousex, mousey, XMARGIN2)
				# user places ships on board
				if (boxx2 != None and boxy2 != None) and mouseClicked:
					if (place < 5):
						checkplace = 0
						spacepressed = pressed[pygame.K_SPACE]
						if not (spacepressed):
							hold = boxy2
							if ((shiparray[place]+boxy2) < 11):
								if (checkplace == 0):
									for y in range(shiparray[place]): 
										if ((playerboard.returnpiece(boxx2,hold)) != 0):
											checkplace = 1
										else:
											hold = hold + 1
								for y in range(shiparray[place]): 
									if (checkplace == 1):
										break
									else:
										playerboard.setpiece(shiparray[place],boxx2,boxy2)
										boxy2 = boxy2 + 1
										if (y == (shiparray[place]-1)):
											place = place + 1
						elif (spacepressed):
							hold = boxx2
							if ((shiparray[place]+boxx2) < 11):
								if (checkplace == 0):
									for x in range(shiparray[place]): 
										if ((playerboard.returnpiece(hold,boxy2)) != 0):
											checkplace = 1
										else:
											hold = hold + 1
								for x in range(shiparray[place]): 
									if (checkplace == 1):
										break
									else:
										playerboard.setpiece(shiparray[place],boxx2,boxy2)
										boxx2 = boxx2 + 1
										if (x == (shiparray[place]-1)):
											place = place + 1
				boxx, boxy = whatbox(mousex, mousey, XMARGIN)
				# game ready to play
				if (place >= 5):
					if (turn == 0):
						if (boxx != None and boxy != None) and mouseClicked:
							place = place + 1
							temp = cpuboard.checkforhitormiss(boxx,boxy)
							if (temp == 9):
								blah = 0
							else:
								playerattackboard.setpiece(temp,boxx,boxy)
								log_move('Player Move', playerattackboard.returnboard())

								if (temp == 7):
									printstatus(screen, 'Miss')
									miss.play(loops = 0)
								else:
									printstatus(screen, 'Hit')
									hit.play(loops = 0)
								if (checkforwin(playerattackboard)):
									printstatus(screen, 'You win!')
									turn = -1
								else:
									checkforshipsunk(playerattackboard, temp, screen)
									turn = 1
					elif (turn == 1):
						if (gamedifficulty == 0):
							comp.attack(playerboard, cpuattackboard)
							log_move('Easy CPU Move', cpuattackboard.returnboard())

						elif (gamedifficulty == 1):
							comp.attack2(playerboard, cpuattackboard)
							log_move('Harder CPU Move', cpuattackboard.returnboard())

						elif (gamedifficulty == 2):
							comp.attack3(playerboard, cpuattackboard)
							log_move('Hardest CPU Move', cpuattackboard.returnpiece(b,a))

						if (checkforwin(cpuattackboard)):
							printstatus(screen, 'Computer Wins!')
							turn = -1
						else:
							turn = 0  

		# If we're in gamemode 3, we're quitting
		if (gamemode == 4):
			screen.fill(color['black'])
			font = pygame.font.Font('resources/alphbeta.ttf', 70)
			thanks = font.render("Thanks for playing!", False, color['white'])
			thanksRect = thanks.get_rect()
			thanksRect.center = (400, 300)
			screen.blit(thanks, thanksRect)
			pygame.mixer.quit()



			pygame.display.update()
			print('Quitting :[')

			pygame.time.wait(1500)
			pygame.quit()
			sys.exit(0)
		# redraw screen       
		pygame.display.update()
		fpsClock.tick(60)

if __name__ == "__main__":
	main(sys.argv[1:])

