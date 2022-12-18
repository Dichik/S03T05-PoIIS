import copy
from collections import defaultdict

import chess
import numpy as np


# Q: what do we store in results?
class MonteCarloTreeSearchNode:

    def __init__(self, state, parent=None):
        self.state = state
        self.parent = parent
        self.children = []

        self._number_of_visits = 0
        self._results = defaultdict(int)
        self._untried_actions = None

    def is_fully_expanded(self):
        return len(self.untried_actions) == 0

    @property
    def untried_actions(self):
        if self._untried_actions is None:
            self._untried_actions = list(self.state.legal_moves)
        return self._untried_actions

    def evaluate(self, board):
        white = board.occupied_co[chess.WHITE]
        black = board.occupied_co[chess.BLACK]
        return self.material_balance(board, white, black) * (chess.popcount(white) - chess.popcount(black))

    def material_balance(self, board, white, black):
        return (
                chess.popcount(white & board.pawns) - chess.popcount(black & board.pawns) +
                3 * (chess.popcount(white & board.knights) - chess.popcount(black & board.knights)) +
                3 * (chess.popcount(white & board.bishops) - chess.popcount(black & board.bishops)) +
                5 * (chess.popcount(white & board.rooks) - chess.popcount(black & board.rooks)) +
                9 * (chess.popcount(white & board.queens) - chess.popcount(black & board.queens))
        )

    @property
    def q(self):
        return self.evaluate(self.state)

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c._number_of_visits) + c_param * np.sqrt((2 * np.log(self._number_of_visits) / c._number_of_visits))
            for c in self.children
        ]
        if choices_weights is []:
            return None
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        if len(possible_moves) == 0:
            return None
        return possible_moves[np.random.randint(len(possible_moves))]

    def expand(self):
        action = self._untried_actions.pop()
        next_state = copy.copy(self.state)
        next_state.push(action)
        child_node = MonteCarloTreeSearchNode(state=next_state, parent=self)
        self.children.append(child_node)
        return child_node

    def is_terminal_node(self, state=None):
        if state is None:
            return self.state.is_checkmate() or self.state.is_variant_draw()
        else:
            return state.is_checkmate() or state.is_variant_draw()

    def rollout(self):
        current_rollout_state = self.state
        number_of_rollouts = 100
        while not self.is_terminal_node(current_rollout_state) and number_of_rollouts > 0:
            possible_moves = list(current_rollout_state.legal_moves)
            action = self.rollout_policy(possible_moves)
            if action is not None:
                current_rollout_state.push(action)
            number_of_rollouts -= 1
        return current_rollout_state

    def backpropagate(self, result):
        self._number_of_visits += 1.
        self._results[str(result)] = self.evaluate(result)
        if self.parent:
            self.parent.backpropagate(result)
