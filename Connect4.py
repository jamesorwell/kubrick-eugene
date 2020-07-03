import numpy as np

class Connect4():
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.boardsize = None

    def board(self, width, height):
        size = np.zeros(width*height).reshape(width,height)
        print (size)


game = Connect4('teamEugene', 'James')
game.board(5,7)
