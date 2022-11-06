import copy

from algorithm.Evaluation import Evaluation


class NegaMax(Evaluation):

    def __init__(self):
        pass

    def negaMax(self, board, depth):
        if depth == 0 or board.is_checkmate() or board.is_variant_draw():
            return [self.evaluate(board)]
        max = -10000000
        finalMove = None
        for move in board.legal_moves:
            newBoard = copy.copy(board)
            newBoard.push(move)
            score = -1 * self.negaMax(newBoard, depth - 1)[0]
            if score > max:
                max = score
                finalMove = move
        return max, finalMove