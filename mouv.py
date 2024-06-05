class Tyr():
    '''class that is used to build the player and make it mouv in a given board'''
    def __init__(self):
       self.up = 3
       self.side = 1
       self.board = None
       self.x = 0
       self.y = 0
       self.nextX = [0, True]
       self.nextY = [0, 0]
       self.goThrought = ['sky', 'void', 'start', 'door']
       self.gameCondition = None
       self.lastCase = ('start', ())
       self.map = 0
       self.unlockedMap = 0
       self.money = 0
       self.moneyCount = True
       # [name, max, resolution, level, + by upgrade, nbr or plus par level,curent value]
       self.aiVar = [
                    ['alpha', 0.2, 0.01, 0, 0.2, 200, 0],
                    ['gamma', 0.2, 0.01, 0, 0.2, 200, 0],
                    ['tiks', 1, 1, 0, 1, 500, 0],
                    ['epsilon', 0.01, 0.01, 0, 0.01, 400, 0],
                    ['reward', 1, 0.1, 0, 1, 300, 0]
                    ]
       
    
    def start(self):
        '''place Tyr at the start of the board'''
        self.gameCondition = None
        self.money += 0.5 * (1.5 * (self.map + 1))
        for i in range(len(self.board)):
            for j in range(len(self.board[0])):
                if self.board[i][j] == 'start':
                    self.y = i
                    self.x = j
                    self.lastCase = ('start', (self.y, self.x))
                    
    def checkStat(self):
        if self.board[self.y][self.x] == 'door':
            self.gameCondition = True
        elif self.board[self.y][self.x] == 'void':
            self.gameCondition = False
        elif self.y == len(self.board)-1:
            self.gameCondition = False
        

    def goRight(self):
        '''set the next coord of tyr to the right case if he can'''
        try:
            if self.x + self.side <= len(self.board[0]) and self.board[self.y][self.x + self.side] in self.goThrought:
                self.nextX[0] += self.side
                self.nextX[1] = True
                self.Fall()
        except:
            pass

    def goLeft(self):
        '''set the next coord of tyr to the left case if he can'''
        try:    
            if self.x - self.side >= 0 and self.board[self.y][self.x - self.side] in self.goThrought: 
                self.nextX[0] += self.side
                self.nextX[1] = False
                self.Fall()
        except: 
            pass

    def Jump(self, direction):
        '''go up for self.up y and then if direction != None go to left or right and fall'''
        for i in range(self.up, 0, -1):
            if self.y - i >= 0 and self.board[self.y - i][self.x] in self.goThrought: 
                self.nextY[0] = self.nextY[0] + i
                if direction == 'l': 
                    if self.x - self.side >= 0 and self.board[self.y - i][self.x - self.side] in self.goThrought: 
                        self.nextX[0] += self.side
                        self.nextX[1] = False
                elif direction == 'r':
                    if self.x + self.side <= len(self.board[0])-1 and self.board[self.y - i][self.x + self.side] in self.goThrought: 
                        self.nextX[0] += self.side
                        self.nextX[1] = True
                self.Fall()
                return 0

    def goDown(self):
        '''when on a floor go throught it and then fall'''
        try:
            if self.board[self.y+1][self.x] == 'floor' and self.board[self.y+2][self.x] in self.goThrought:
                self.nextY[1] += 2
                self.Fall()
        except:
            pass

    def Fall(self):
        '''-1 y untill there is a floor or a wall below tyr'''
        if not(self.board[self.y+1+self.nextY[1]-self.nextY[0]][self.x+self.nextX[0] if self.nextX[1] else self.x - self.nextX[0]] in self.goThrought):
            pass

        else:
            self.nextY[1] += 1
            return self.Fall() 
        return


