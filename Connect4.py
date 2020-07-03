import numpy as np

class Connect4():
    def __init__(self, player1, player2, width = 7, height = 6):
        self.player1 = player1
        self.player2 = player2
        self.board = np.zeros(width*height).reshape(height,width )
        self.width = width  - 1
        self.height = height - 1
        self.counter = [0] * 7
        print (self.counter)
        print (self.board)



    def player1turn(self):
        x = input("Player one, choose your position(a-g)")
        dict = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6}
        self.board[self.height - self.counter[dict[x]]][dict[x]] = 1
        self.counter[dict[x]] += 1
        print (self.counter)
        print (self.board)



    def player2turn(self):
        x = input("Player two, choose your position(a-g)")
        dict = {'a' : 0, 'b' : 1, 'c' : 2, 'd' : 3, 'e' : 4, 'f' : 5, 'g' : 6}
        self.board[self.height - self.counter[dict[x]]][dict[x]] = 2
        self.counter[dict[x]] += 1
        print (self.board)

    def play(self):
        turncount = 0
        while turncount <= 5:
            if turncount % 2 == 0:
                game.player1turn()
            else:
                game.player2turn()
            turncount+=1






game = Connect4('teamEugene', 'James')
game.play()



def pascal(n):
    board = np.zeros(49).reshape(7, 7)
    board[1,5] = 1
    print (board)
    for row in range(7):
        for i in range(7):
            if board[row+1,i+1] == board[row,i+1]:
                print (row, i)
    return x

lst = []
for row in range(7):
    for i in range(4):
        if (board[row,i]) == 1 and (board[row,i] == board[row,i+1]):
            if (board[row,i]) == 1 and (board[row,i] == board[row,i+2]):
                if (board[row,i]) == 1 and (board[row,i] == board[row,i+3]):
                    lst.append([row,i])

for row in range(4):
    for i in range(7):
        if (board[row,i]) == 1 and (board[row,i] == board[row+1,i]):
            if (board[row,i]) == 1 and (board[row,i] == board[row+2,i]):
                if (board[row,i]) == 1 and (board[row,i] == board[row+3,i]):
                    lst.append([row,i])

for row in range(4):
    for i in range(4):
        if (board[row,i]) == 1 and (board[row,i] == board[row+1,i+1]):
            if (board[row,i]) == 1 and (board[row,i] == board[row+2,i+2]):
                if (board[row,i]) == 1 and (board[row,i] == board[row+3,i+3]):
                    lst.append([row,i])

for row in range(4):
    for i in range(3,7):
        if (board[row,i]) == 1 and (board[row,i] == board[row+1,i-1]):
            if (board[row,i]) == 1 and (board[row,i] == board[row+2,i-2]):
                if (board[row,i]) == 1 and (board[row,i] == board[row+3,i-3]):
                    lst.append([row,i])

print (lst)



x[row,i] + x[row,i+1]

def pascal1(n):
    board = np.zeros(49).reshape(6, 7)
    x[:,0] = 1
    for i in range(1,7):
        x[i,1:] = x[i-1,0:n-1] + x[i-1,1:]
    list = x.tolist()
    a = []
    for i in list:
        x = ([a for a in i if a != 0.0])
        a.append(x)
    return a
