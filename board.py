class board(object):
	
	def __init__(self):
			self.gameboard = [[0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0],
				 [0,0,0,0,0,0,0,0,0,0]]
	
	def setpiece(self, piece, row, col):
			self.gameboard[col][row] = piece
			
	def returnpiece(self, row, col):
			return self.gameboard[col][row]
		
	def checkforhitormiss(self, row, col):
		hold = self.returnpiece(row, col)
		if hold != 7 and hold != 8:
			if hold == 0:
				self.setpiece(7, row, col)
				return 7
			else:
				self.setpiece(8, row, col)
				return hold
		else:
			return 9
		
	def returnboard(self):
		return self.gameboard
				