    class board():
        gameboard = [[0,0,0,0,0,0,0,0,0,0],
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
                self.gameboard[row][col] = piece
                
        def returnpiece(self, row, col):
                return self.gameboard[row][col]
            
        def checkforhitormiss(self, row, col):
            hold = self.returnpiece(row, col)
            if hold != 7 or hold != 8:
                if hold == 0:
                    self.setpiece(7, row, col)
                    return 'miss'
                else:
                    self.setpiece(8, row, col)
                    return 'hit'
            else:
                return 'Pick another Space'
                