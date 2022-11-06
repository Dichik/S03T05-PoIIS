from algorithm.NegaMax import NegaMax
from algorithm.NegaScout import NegaScout
from algorithm.PVS import PVS


class GameEngine:
    def __init__(self, engineIndex):
        if engineIndex == 1:
            self.predictor = NegaMax()
        elif engineIndex == 2:
            self.predictor = NegaScout()
        elif engineIndex == 3:
            self.predictor = PVS()

    def predictMove(self, board, depth):
        return self.predictor.predict(board, depth)
