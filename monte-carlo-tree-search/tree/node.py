import numpy as np

from collections import defaultdict


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

    def best_child(self, c_param=1.4):
        # here we calculating UCT (Upper Confidence Bound applied to trees)
        # and after that choose the best child among all available
        scores = [0 for c in self.children]
        return self.children[0]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.randint(len(possible_moves))]

    def expand(self):
        pass
        # take from untried_actions the first one
        action = self._untried_actions.pop()

    def is_terminal_node(self):
        return self.state.is_checkmate() == True \
               or self.state.is_variant_draw() == True

    def rollout(self):
        current_state = self.state
        while not current_state.is_terminal_state():
            action = self.rollout_policy(current_state.legal_moves)
            current_rollout_state = self.state.push(action)
        return current_rollout_state

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if result.parent:
            self.parent.backpropagate(result)
