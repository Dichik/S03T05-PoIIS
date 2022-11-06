from algorithm.NegaMax import NegaMax
from algorithm.NegaScout import NegaScout
from algorithm.PVS import PVS


class GameEngine:
    def __init__(self, engineIndex):
        if engineIndex == 1:
            self.predict = NegaMax.negaMax
        elif engineIndex == 2:
            self.predict = NegaScout.negaScout
        elif engineIndex == 3:
            self.predict = PVS.pvSearch

    def predictMove(self, board, depth):
        return self.predict(board, depth)
