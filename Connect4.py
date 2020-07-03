import numpy as np

class Connect4():
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.boardsize = None



    def boards(self, width, height):
        size = np.zeros(width*height).reshape(height,width )
        self.boardsize = size
        self.columncounter = [0] * width
        print (self.columncounter)
        print (self.boardsize)


    def player1turn(self):
        x = input("Player one, choose your position(a-g)")
        dict = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, 'f' : 6, 'g' : 7}
        self.boardsize[]

    def player2turn(self):
        x = input("Player one, choose your position(a-g)")
        dict = {'a' : 1, 'b' : 2, 'c' : 3, 'd' : 4, 'e' : 5, 'f' : 6, 'g' : 7}






game = Connect4('teamEugene', 'James')
game.boards(7,6)
game.player1turn()
