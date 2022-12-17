import chess

from tree.search import MonteCarloTreeSearch
from tree.node import MonteCarloTreeSearchNode


def is_game_over(state):
    return state.is_checkmate() or state.is_variant_draw()


if __name__ == "__main__":

    board = chess.Board()
    while not is_game_over(board):
        root = MonteCarloTreeSearchNode(state=board)
        mcts = MonteCarloTreeSearch(root)
        best_move = mcts.best_action(root, total_simulation_time=1)
        if best_move is not None:
            board.push(best_move)
        print(board)
