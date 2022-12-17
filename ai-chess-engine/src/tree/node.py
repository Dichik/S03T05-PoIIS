from constant.constants import DEFAULT_C_PARAM

class MonteCarloTreeSearchNode:
    
    def __init__(self, state, parent=None):
        self.state=state
        self.parent=parent
        self.children=[]

    def is_fully_expanded(self):
        pass

    def best_child(self, c_param=DEFAULT_C_PARAM):
        pass

    def rollout_policy(self, possible_moves):        
        pass

class TwoPlayersGameMonteCarloTreeSearchNode(MonteCarloTreeSearchNode):

    def __init__(self, state, parent=None):
        super().__init__(state, parent)
        self._number_of_visits = 0.
        self._results = defaultdict(int)
        self._untried_actions = None

    def untried_actions(self):
        pass

    def expand(self):
        pass

    def is_terminal_node(self):
        pass

    def rollout(self):
        pass

    def backpropagate(self, result):
        pass
