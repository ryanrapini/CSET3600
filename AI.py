import random

class AI():
    
    def __init__(self):
        self.attackmode = 0
        self.targettype = 1
    
    def placeships(self, shiparray, board):
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
                    board.setpiece(size,row,col)
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
                    board.setpiece(size,row,col)
                    row = row + 1    
                            
                            
    def attack(self, playerboard, cpuattackboard):
        #this AI just randomly guesses
        row = random.randint(0,9)
        col = random.randint(0,9)
        temp = playerboard.checkforhitormiss(row, col)
        while temp == 9:
            row = random.randint(0,9)
            col = random.randint(0,9)
            temp = playerboard.checkforhitormiss(row, col)
        cpuattackboard.setpiece(temp,row,col)
        
        
    def attack2(self, playerboard, cpuattackboard):
        #this AI cheats
        if self.attackmode == 0:
            row = random.randint(0,9)
            col = random.randint(0,9)
            temp = playerboard.checkforhitormiss(row, col)
            while temp == 9:
                row = random.randint(0,9)
                col = random.randint(0,9)
                temp = playerboard.checkforhitormiss(row, col)
            cpuattackboard.setpiece(temp,row,col)
            if (temp == 2) or (temp == 3) or (temp == 3) or (temp == 4) or (temp == 5) or (temp == 6):
                self.attackmode = 1
                self.targettype = temp
        elif self.attackmode == 1:
            for x in range(10):
                for y in range(10):
                    findnextpiece = playerboard.returnpiece(x,y)
                    print(findnextpiece)
                    if (findnextpiece == self.targettype):
                        break
                if (findnextpiece == self.targettype):
                    playerboard.checkforhitormiss(x,y)
                    cpuattackboard.setpiece(findnextpiece,x,y)
                    self.checkforshipsunk(cpuattackboard)
                    break
                        
            
    def checkforshipsunk(self, board):
        hold = 0
        for x in range(10):
            for y in range(10):
                if (board.returnpiece(x,y) == self.targettype):
                    hold = hold + 1
        if (hold == self.targettype):
            self.attackmode = 0
            self.targettype = 1
    
