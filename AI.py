import random

class AI():
    
    def placeships(self, shiparray, piece, board):
        totalships = len(shiparray)
        for x in range(totalships):
            row = random.randint(0,9)
            col = random.randint(0,9)
            direction = random.randint(0,1)
            size = shiparray[x]
            spacetaken = True
            if (direction == 0):
                while (spacetaken):
                    while ((size+col) > 9):
                        row = random.randint(0,9)
                        col = random.randint(0,9)
                    for temp in range(size):
                        if (board.returnpiece(row,col+temp) != 0):
                             spacetaken = True
                             row = random.randint(0,9)
                             col = random.randint(0,9)
                             break
                        else:
                            spacetaken = False 
                for y in range(size): 
                    board.setpiece(piece,row,col)
                    col = col + 1
            if (direction == 1):
                while (spacetaken):
                    while ((size+row) > 9):
                        row = random.randint(0,9)
                        col = random.randint(0,9)
                    for temp in range(size):
                        if (board.returnpiece(row+temp,col) != 0):
                             spacetaken = True
                             row = random.randint(0,9)
                             col = random.randint(0,9)
                             break
                        else:
                            spacetaken = False 
                for y in range(size): 
                    board.setpiece(piece,row,col)
                    row = row + 1    
                            
                            
                    
                