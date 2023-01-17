import numpy as np
import random

'''This is Ultimate Tic-Tac-Toe:
In this game, there is a 9 x 9 board, which consists of 9 3 x 3 sub-boards.
Once a player moves, the next player must move in the sub-board corresponding
to the relative position the first player moved at. To learn how to play, 
visit: https://bejofo.net/ttt. To learn more about the rules, visit 
https://en.wikipedia.org/wiki/Ultimate_tic-tac-toe.'''
class XO9:
    #The Board--has a "1" or "2" indicating which player has a spot
    r = np.zeros((9, 9))
    #Indicates which sub-boards are won, and by whom("1" or "2")
    w = np.zeros((3, 3))
    #Indicates which sub-boards are full("0" or "1")
    f = np.zeros((3, 3))
    #The last move taken--initialized at [0,0]
    x = [0,0]
    #The next player to move--initialized at 1
    to_move = 1
    #The next place to move--initialized at [-1, -1], which allows 1 to move anywhere
    direct = [-1, -1]

    '''Pass in a list of length two to edit a spot on the board--
    the spot is automatically taken by the person who's turn it is--
    if a valid move was input, returns a list [self.r, self.done()]--
    otherwise, returns False'''
    def edit(self, x):
        
        panel_row = x[0]//3
        panel_column = x[1]//3

        if self.direct[0] != -1 :
            if panel_row != self.direct[0] or panel_column != self.direct[1]:
                return False
        if self.f[panel_row, panel_column] == 9:
            return False

        self.r[x[0]][x[1]] = self.to_move

        if (self.won(self.to_move, panel_row, panel_column)):
            self.w[panel_row][panel_column] = self.to_move
        if (self.to_move == 1):
            self.to_move = 2
        else:
            self.to_move = 1
        self.f[panel_row][panel_column] += 1

        self.direct = [x[0]%3, x[1]%3]
        if (self.f[self.direct[0]][self.direct[1]] == 9):
            self.direct = [-1, -1]

        return self.r, self.done()

    '''Checks if a 3 x 3 tic-tac-toe board is won'''
    def won(self, player, panel_row, panel_column):
        count = 0
        list = []
        for i in range(panel_row*3, panel_row*3+3):
            for j in range(panel_column*3, panel_column*3+3):
                if (self.r[i][j] == player):
                    count += 1
                    list.append(np.array([i, j]))
        if count >= 6:
            return 1
        elif count <= 2:
            return 0
        for i in range(2, count):
            for j in range(i):
                for k in range(j):
                    if (np.equal((list[i] - list[j]),(list[j] - list[k])).all()):
                        return 1
        return 0

    '''Counts the amount of sub-boards won by a player--
    pass in a number corresponding to a player'''
    def count(self, player):
        count = 0
        for i in range(3):
            for j in range(3):
                if (self.w == player):
                    count += 1
        return count

    '''This method checks if there is a 3 x 3 match in the
    large board.'''
    def score(self):
        for player in [1, 2]:
            count = 0
            list = []
            for i in range(3):
                for j in range(3):
                    if (self.w[i][j] == player):
                        count += 1
                        list.append(np.array([i, j]))
            if count >= 6:
                return player
            elif count <= 2:
                return 0
            for i in range(2, count):
                for j in range(i):
                    for k in range(j):
                        if (np.equal((list[i] - list[j]),(list[j] - list[k])).all()):
                            return player
            return 0

    '''For debugging--shows the current status of the board'''
    def show(self):
        print(self.r)
        print(self.w)
        print(self.f)

    '''Returns a viable random position to play--
    continues infinitely if the board is full--
    useful for training an algorithm against random moves'''
    def sample(self):
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        if (self.r[i][j] == 0 and self.f[i//3][j//3] != 9):
            if (self.direct[0] == -1 and self.direct[1] == -1):
                return (i, j)
            if (i//3 == self.direct[0] and j//3 == self.direct[1]):
                return (i, j)
        self.sample()

    '''Resets the board'''
    def reset(self):
        self.r = np.zeros((9, 9))
        self.w = np.zeros((3, 3))
        self.f = np.zeros((3, 3))
        self.x = [0,0]
        self.to_move = 1
        self.direct = [-1, -1]
        self.reset = 0

    '''Checks if the game has concluded''' 
    def done(self):
        if self.score():
            return True
        for i in range(9):
            for j in range(9):
                if (self.w[i][j] == 0):
                    return False
        return True