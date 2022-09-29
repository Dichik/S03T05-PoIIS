# search.py
# ---------
# Licensing Information:  You are free to use or extend these projects for
# educational purposes provided that (1) you do not distribute or publish
# solutions, (2) you retain this notice, and (3) you provide clear
# attribution to UC Berkeley, including a link to http://ai.berkeley.edu.
# 
# Attribution Information: The Pacman AI projects were developed at UC Berkeley.
# The core projects and autograders were primarily created by John DeNero
# (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# Student side autograding was added by Brad Miller, Nick Hay, and
# Pieter Abbeel (pabbeel@cs.berkeley.edu).


"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from util import Stack
from util import Queue

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem.
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state.
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples, (successor,
        action, stepCost), where 'successor' is a successor to the current
        state, 'action' is the action required to get there, and 'stepCost' is
        the incremental cost of expanding to that successor.
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.
        The sequence must be composed of legal moves.
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other maze, the
    sequence of moves will be incorrect, so only use this for tinyMaze.
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s, s, w, s, w, w, s, w]

def depthFirstSearch(problem: SearchProblem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    """
    "*** YOUR CODE HERE ***"
    print("Start:", problem.getStartState())
    print("Is the start a goal?", problem.isGoalState(problem.getStartState()))
    print("Start's successors:", problem.getSuccessors(problem.getStartState()))

    visited = set()
    path = dict()
    stack = Stack()
    stack.push(problem.getStartState())
    target = None
    path[problem.getStartState()] = -1

    while not stack.isEmpty():
        current = stack.pop()
        visited.add(current)
        successors = problem.getSuccessors(current)

        if problem.isGoalState(current):
            target = current
        if successors is None:
            continue

        for i in range(0, len(successors)):
            coord = successors[i][0]
            if coord not in visited:
                stack.push(coord)
                path[coord] = current

    result = []
    curr = target
    while curr != -1:
        result.append(curr)
        curr = path.get(curr)
    result.reverse()

    return translated(result)


def translated(result):
    answer = []
    from game import Directions
    for i in range(0, len(result) - 1):
        _from = result[i]
        _to = result[i + 1]
        if _from[0] != _to[0]:
            if _from[0] > _to[0]:
                answer.append(Directions.WEST)
            else:
                answer.append(Directions.EAST)
        else:
            if _from[1] > _to[1]:
                answer.append(Directions.SOUTH)
            else:
                answer.append(Directions.NORTH)

    return answer


def breadthFirstSearch(problem: SearchProblem):
    """Search the shallowest nodes in the search tree first."""
    "*** YOUR CODE HERE ***"
    queue = Queue()
    used = set()
    path = dict()

    path[problem.getStartState()] = -1
    used.add(problem.getStartState())
    queue.push(problem.getStartState())
    target = None
    while not queue.isEmpty():
        current = queue.pop()
        successors = problem.getSuccessors(current)
        if problem.isGoalState(current):
            target = current
        for i in range(0, len(successors)):
            _to = successors[i][0]
            if _to not in used:
                queue.push(_to)
                path[_to] = current
                used.add(_to)

    result = []
    while target != -1:
        result.append(target)
        target = path.get(target)

    result.reverse()
    return translated(result)


def uniformCostSearch(problem: SearchProblem):
    """Search the node of least total cost first."""
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem: SearchProblem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    frontier = util.PriorityQueue()
    start = problem.getStartState()
    frontier.push(start, 0)
    came_from = dict()
    cost_so_far = dict()
    came_from[start] = None
    cost_so_far[start] = 0
    target = None

    while not frontier.isEmpty():
        current = frontier.pop()
        successors = problem.getSuccessors(current)
        if problem.isGoalState(current):
            target = current
            break

        for i in range(0, len(successors)):
            _next = successors[i][0]
            new_cost = heuristic(_next, problem)
            if _next not in cost_so_far or new_cost < cost_so_far[_next]:
                cost_so_far[_next] = new_cost
                priority_cost = new_cost + heuristic(_next, problem)
                frontier.push(_next, priority_cost)
                came_from[_next] = current

    result = []
    while target is not None:
        result.append(target)
        target = came_from.get(target)

    result.reverse()
    return translated(result)


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
