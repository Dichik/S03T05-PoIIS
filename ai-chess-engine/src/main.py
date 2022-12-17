import chess

from src.tree.node import TwoPlayersGameMonteCarloTreeSearchNode
from tree.search import MonteCarloTreeSearch

def is_game_over(board):
    return board.is_checkmate() == True \
            or board.is_variant_draw() == True

if __name__ == "__main__":

    board = chess.Board()
    while is_game_over(board) == False:
        root = TwoPlayersGameMonteCarloTreeSearchNode(state = board)
        mcts = MonteCarloTreeSearch(root)
        best_move = mcts.best_action(total_simulation_time=1)

        board.move(best_move)
        print(board)