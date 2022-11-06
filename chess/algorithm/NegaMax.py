import copy

from algorithm.Evaluation import Evaluation
from algorithm.Predictor import Predictor
from constant.constants import DEFAUL_MIN_VALUE, DEFAULT_MAX_VALUE


class NegaMax(Evaluation, Predictor):

    def __init__(self):
        pass

    def predict(self, board, depth, alpha=DEFAUL_MIN_VALUE, beta=DEFAULT_MAX_VALUE):
        if depth == 0 or board.is_checkmate() or board.is_variant_draw():
            return [self.evaluate(board)]
        max = -10000000
        finalMove = None
        for move in board.legal_moves:
            newBoard = copy.copy(board)
            newBoard.push(move)
            score = -1 * self.predict(newBoard, depth - 1)[0]
            if score > max:
                max = score
                finalMove = move
        return max, finalMove