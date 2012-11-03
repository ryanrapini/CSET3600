class ships():
	ac = [1,1,1,1,1]
	bs = [2,2,2,2]
	sub = [3,3,3]
	des = [4,4,4]
	pb = [5,5]
	
	def returnaircraftcarrier(self):
				return self.ac
			
	def returnbattleship(self):
				return self.bs
			
	def returnsubmarine(self):
				return self.sub
			
	def returndestroyer(self):
				return self.des
			
	def returnpatrolboat(self):
				return self.ac

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
