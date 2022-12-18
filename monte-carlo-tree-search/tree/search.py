import time


class MonteCarloTreeSearch:

    def __init__(self, root):
        self.root = root

    def best_action(self, total_simulation_time=5000):
        end_time = time.time() + total_simulation_time

        while self.resources_left(end_time):
            leaf = self.traverse()
            simulation_result = leaf.rollout()
            leaf.backpropagate(simulation_result)

        return self.root.best_child(c_param=0.)

    @staticmethod
    def resources_left(end_time):
        return end_time - time.time() > 0

    def traverse(self):
        current_node = self.root
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node.expand()
            else:
                current_node = current_node.best_child()
        return current_node
