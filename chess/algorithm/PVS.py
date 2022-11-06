import copy

from algorithm.Evaluation import Evaluation
from constant.constants import DEFAULT_MAX_VALUE
from constant.constants import DEFAUL_MIN_VALUE


class PVS(Evaluation):

    def __init__(self):
        pass

    def pvSearch(self, board, depth, alpha=DEFAUL_MIN_VALUE, beta=DEFAULT_MAX_VALUE):
        if depth == 0 or board.is_checkmate() or board.is_variant_draw():
            return [self.evaluate(board)]
        finalMove = None
        bSearchPv = True
        for move in board.legal_moves:
            newBoard = copy.copy(board)
            newBoard.push(move)
            if bSearchPv:
                score = -1 * self.pvSearch(newBoard, depth - 1, -1 * beta, -1 * alpha)[0]
            else:
                score = -1 * self.pvSearch(newBoard, depth - 1, -1 * alpha - 1, -1 * alpha)[0]
                if score > alpha:
                    score = -1 * self.pvSearch(newBoard, depth - 1, -1 * beta, -1 * alpha)[0]

            if score >= beta:
                return beta, move
            if score > alpha:
                alpha = score
                bSearchPv = False
                finalMove = move
        return alpha, finalMove
