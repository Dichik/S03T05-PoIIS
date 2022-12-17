import time


class MonteCarloTreeSearch:

    def __init__(self, root):
        self.root = root

    def best_child(self, root):
        # pick child with highest number of visits
        pass

    def traverse(self, node):
        pass
        # while self.fully_expanded(node):
        #     node = self.best_uct(node)
        # return self.pick_unvisited(node.children) or node  # in case no children are present / node is terminal

    def resources_left(self, end_time):
        return end_time > time.time()

    def best_action(self, root, total_simulation_time=5000):
        # end_time = time.time() + total_simulation_time
        #
        # while self.resources_left(end_time):
            # leaf = self.traverse(root)
            # simulation_result = self.rollout(leaf)
            # self.backpropagate(leaf, simulation_result)
        #
        # return self.best_child(root)
        return None
