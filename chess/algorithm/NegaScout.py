import copy

from algorithm.Evaluation import Evaluation
from constant.constants import DEFAULT_MAX_VALUE
from constant.constants import DEFAUL_MIN_VALUE


class NegaScout(Evaluation):

    def __init__(self):
        pass

    def negaScout(self, board, depth, alpha=DEFAUL_MIN_VALUE, beta=DEFAULT_MAX_VALUE):
        if depth == 0 or board.is_checkmate() or board.is_variant_draw():
            return [self.evaluate(board)]
        finalMove = None
        a = alpha
        b = beta
        for move in board.legal_moves:
            newBoard = copy.copy(board)
            newBoard.push(move)
            score = -1 * self.negaScout(newBoard, depth - 1, -1 * b, -1 * alpha)[0]
            if alpha < score < beta and depth >= 2:
                a = -1 * self.negaScout(newBoard, depth - 1, -1 * beta, -1 * score)[0]
            if score > a:
                a = score
                finalMove = move
            if a >= beta:
                return a, move
            b = a + 1
        return a, finalMove
