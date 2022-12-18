import copy

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
        best_state = mcts.best_action(total_simulation_time=1)
        if best_state is None:
            continue
        print("--------------")
        print(best_state.state)

    print("Game is over!")