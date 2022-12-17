import time

class MonteCarloTreeSearch:
    
    def __init__(self):
        pass


    def best_child(self, root):
        # pick child with highest number of visits
        pass


    def update_stats(self, node, result):
        pass


    # Node being not-fully expanded means at least one of its children is unvisited, not explored
    def fully_expanded(self, node):
        pass


    def best_uct(self, node):
        pass


    def pick_unvisited(self, children):
        pass


    def traverse(self, node):
        while self.fully_expanded(node):
            node = self.best_uct(node)
        return self.pick_unvisited(node.children) or node # in case no children are present / node is terminal 


    def pick_random(self, children):
        pass


    def rollout_policy(self, node):
        return self.pick_random(node.children)


    def non_terminal(self, node):
        pass


    def rollout(self, leaf):
        while self.non_terminal(node):
            node = self.rollout_policy(node)
        return self.result(node)


    def is_root(self, node):
        pass


    def backpropagate(self, node, result):
        if self.is_root(node):
            return
        node.stats = self.update_stats(node, result) 
        self.backpropagate(node.parent)


    def resources_left(self, end_time):
        return end_time > time.time()


    def best_action(self, root, total_simulation_time=5000):
        end_time = time.time() + total_simulation_time

        while self.resources_left(end_time):
            leaf = self.traverse(root)
            simulation_result = self.rollout(leaf)
            self.backpropagate(leaf, simulation_result)
        
        return self.best_child(root)
