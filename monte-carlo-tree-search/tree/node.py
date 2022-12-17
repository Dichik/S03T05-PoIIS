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

    @property
    def q(self):
        wins = self._results[self.parent.state]
        loses = self._results[-1 * self.parent.state]
        return wins - loses

    def best_child(self, c_param=1.4):
        choices_weights = [
            (c.q / c._number_of_visits) + c_param * np.sqrt((2 * np.log(self._number_of_visits) / c._number_of_visits))
            for c in self.children
        ]
        return self.children[np.argmax(choices_weights)]

    def rollout_policy(self, possible_moves):
        return possible_moves[np.randint(len(possible_moves))]

    def expand(self):
        action = self._untried_actions.pop()
        next_state = self.state.push(action)
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
        while not self.is_terminal_node(current_rollout_state):
            possible_moves = current_rollout_state.legal_moves
            action = self.rollout_policy(possible_moves)
            current_rollout_state = current_rollout_state.push(action)
        return current_rollout_state

    def backpropagate(self, result):
        self._number_of_visits += 1
        self._results[result] += 1
        if result.parent:
            self.parent.backpropagate(result)
