import random

class AI():
    
    def __init__(self):
        self.attackmode = 0
        self.targettype = 1
        self.originalx = 0
        self.originaly = 0
        self.direction = 0
        self.turntaken = 0
        self.targettype = 0
        self.temp2 = 0
        self.boom = 1
    
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
        #this AI is harder but doesn't cheat
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
                self.originalx = col
                self.originaly = row
                self.boom = 1
                self.direction = 0
                self.targettype = temp
                
        elif self.attackmode == 1:
            #check up
            if (self.turntaken == 0) and (self.direction == 0) and (self.originalx - self.boom >= 0) and (cpuattackboard.returnpiece(self.originaly, self.originalx - self.boom) == 0):
                    self.temp2 = playerboard.checkforhitormiss(self.originaly, self.originalx - self.boom)
                    cpuattackboard.setpiece(self.temp2,self.originaly,self.originalx - self.boom)
                    self.boom = self.boom + 1
                    self.turntaken = 1
                    if (self.temp2 == 7): #or (cpuattackboard.returnpiece(self.originaly, self.originalx - self.boom) != 0):
                        self.direction = 1
                        self.boom = 1
            elif (self.turntaken == 0) and (self.direction == 0) and (self.originalx - self.boom >= 0) and ((cpuattackboard.returnpiece(self.originaly, self.originalx - self.boom) != 7)) and ((cpuattackboard.returnpiece(self.originaly, self.originalx - self.boom) != 0)):
                    thissucks = self.originalx - self.boom
                    self.temp2 = playerboard.checkforhitormiss(self.originaly, thissucks)  
                    while (self.temp2 == 9) or (thissucks < 0):
                        thissucks = thissucks - 1
                        if (thissucks < 0):
                            break
                        self.temp2 = playerboard.checkforhitormiss(self.originaly, thissucks)      
                    if (thissucks >= 0) and (self.temp2 != 9):
                        cpuattackboard.setpiece(self.temp2, self.originaly, thissucks)       
                        self.boom = thissucks + self.originalx
                        self.turntaken = 1
                    else:
                        self.direction = 1
                        self.boom = 1                                                                                                      
            elif (self.turntaken == 0) and (self.direction == 0) and ((self.originalx - self.boom < 0) or (cpuattackboard.returnpiece(self.originaly, self.originalx - self.boom) == 7)):
                        self.direction = 1
                        self.boom = 1
            
            #check down   
            if (self.turntaken == 0) and (self.direction == 1) and (self.originalx + self.boom < 10) and (cpuattackboard.returnpiece(self.originaly, self.originalx + self.boom) == 0):
                    self.temp2 = playerboard.checkforhitormiss(self.originaly, self.originalx + self.boom)
                    cpuattackboard.setpiece(self.temp2,self.originaly,self.originalx + self.boom)
                    self.boom = self.boom + 1
                    self.turntaken = 1
                    if (self.temp2 == 7):# or (cpuattackboard.returnpiece(self.originaly, self.originalx + self.boom) != 0):
                        self.direction = 2
                        self.boom = 1
            elif (self.turntaken == 0) and (self.direction == 1) and (self.originalx + self.boom < 10) and ((cpuattackboard.returnpiece(self.originaly, self.originalx + self.boom) != 7)) and ((cpuattackboard.returnpiece(self.originaly, self.originalx + self.boom) != 0)):
                    thissucks = self.originalx + self.boom
                    self.temp2 = playerboard.checkforhitormiss(self.originaly, thissucks)  
                    while (self.temp2 == 9) or (thissucks > 9):
                        thissucks = thissucks + 1
                        if (thissucks > 9):
                            break
                        self.temp2 = playerboard.checkforhitormiss(self.originaly, thissucks)      
                    if (thissucks <= 9) and (self.temp2 != 9):
                        cpuattackboard.setpiece(self.temp2, self.originaly, thissucks)       
                        self.boom = thissucks - self.originalx
                        self.turntaken = 1
                    else:
                        self.direction = 2
                        self.boom = 1 
            elif (self.turntaken == 0) and (self.direction == 1) and ((self.originalx + self.boom > 9) or (cpuattackboard.returnpiece(self.originaly, self.originalx + self.boom) == 7)):
                        self.direction = 2
                        self.boom = 1
                        
            #check left
            if (self.turntaken == 0) and (self.direction == 2) and (self.originaly - self.boom >= 0) and (cpuattackboard.returnpiece(self.originaly - self.boom, self.originalx) == 0):
                    self.temp2 = playerboard.checkforhitormiss(self.originaly - self.boom, self.originalx)
                    cpuattackboard.setpiece(self.temp2,self.originaly - self.boom,self.originalx)
                    self.boom = self.boom + 1
                    self.turntaken = 1
                    if (self.temp2 == 7):# or (cpuattackboard.returnpiece(self.originaly - self.boom, self.originalx) != 0):
                        self.direction = 3
                        self.boom = 1
            elif (self.turntaken == 0) and (self.direction == 2) and (self.originaly - self.boom >= 0) and ((cpuattackboard.returnpiece(self.originaly - self.boom, self.originalx) != 7)) and ((cpuattackboard.returnpiece(self.originaly - self.boom, self.originalx) != 0)):
                    thissucks = self.originaly - self.boom
                    self.temp2 = playerboard.checkforhitormiss(thissucks,self.originalx)  
                    while (self.temp2 == 9) or (thissucks < 0):
                        thissucks = thissucks - 1
                        if (thissucks < 0):
                            break
                        self.temp2 = playerboard.checkforhitormiss(thissucks,self.originalx)      
                    if (thissucks >= 0) and (self.temp2 != 9):
                        cpuattackboard.setpiece(self.temp2, thissucks, self.originalx)     
                        self.boom = thissucks + self.originaly
                        self.turntaken = 1
                    else:
                        self.direction = 3
                        self.boom = 1 
            elif (self.turntaken == 0) and (self.direction == 2) and ((self.originaly - self.boom < 0) or (cpuattackboard.returnpiece(self.originaly - self.boom, self.originalx) == 7)):
                        self.direction = 3
                        self.boom = 1
                        
            #check right
            if (self.turntaken == 0) and (self.direction == 3) and (self.originaly + self.boom < 10) and (cpuattackboard.returnpiece(self.originaly + self.boom, self.originalx) == 0):
                    self.temp2 = playerboard.checkforhitormiss(self.originaly + self.boom, self.originalx)
                    cpuattackboard.setpiece(self.temp2,self.originaly + self.boom,self.originalx)
                    self.boom = self.boom + 1
                    self.turntaken = 1
                    if (self.temp2 == 7):# or (cpuattackboard.returnpiece(self.originaly + self.boom, self.originalx) != 0):
                        self.direction = 0
                        self.boom = 1
            elif (self.turntaken == 0) and (self.direction == 3) and (self.originaly + self.boom < 10) and ((cpuattackboard.returnpiece(self.originaly + self.boom, self.originalx) != 7)) and ((cpuattackboard.returnpiece(self.originaly + self.boom, self.originalx) != 0)):
                    thissucks = self.originaly + self.boom
                    self.temp2 = playerboard.checkforhitormiss(thissucks, self.originalx)  
                    while (self.temp2 == 9) or (thissucks > 9):
                        thissucks = thissucks + 1
                        if (thissucks > 9):
                            break
                        self.temp2 = playerboard.checkforhitormiss(thissucks, self.originalx)      
                    if (thissucks <= 9) and (self.temp2 != 9):
                        cpuattackboard.setpiece(self.temp2, thissucks, self.originalx)       
                        self.boom = thissucks - self.originaly
                        self.turntaken = 1
                    else:
                        self.direction = 0
                        self.boom = 1 
            elif (self.turntaken == 0) and (self.direction == 3) and ((self.originaly + self.boom > 9) or (cpuattackboard.returnpiece(self.originaly + self.boom, self.originalx) == 7)):
                        self.direction = 0
                        self.boom = 1
                        
                        
            checkship = self.checkforshipsunk2(cpuattackboard, self.targettype)
            
            if (checkship == self.targettype):
                        self.boom = 1
                        self.direction = 0
                        self.attackmode = 0
                        self.targettype = 0
                           
            self.turntaken = 0
                     
    def attack3(self, playerboard, cpuattackboard):
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
            
    def checkforshipsunk2(self, board, piece):
        hold = 0
        for x in range(10):
            for y in range(10):
                if (board.returnpiece(x,y) == piece):
                    hold = hold + 1
        return hold
    
