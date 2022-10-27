# multiAgents.py
# --------------
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


from util import manhattanDistance
from game import Directions
import random, util

from game import Agent
from pacman import GameState


def calculateCost(objPos, newPos):
    x1 = objPos[0]
    y1 = objPos[1]
    x2 = newPos[0]
    y2 = newPos[1]
    return abs(x1 - x2) + abs(y1 - y2)


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState: GameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(len(scores)) if scores[index] == bestScore]
        chosenIndex = random.choice(bestIndices)  # Pick randomly among the best

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState: GameState, action):
        """
        Design a better evaluation function here.

        The evaluation function takes in the current and proposed successor
        GameStates (pacman.py) and returns a number, where higher numbers are better.

        The code below extracts some useful information from the state, like the
        remaining food (newFood) and Pacman position after moving (newPos).
        newScaredTimes holds the number of moves that each ghost will remain
        scared because of Pacman having eaten a power pellet.

        Print out these variables to see what you're getting, then combine them
        to create a masterful evaluation function.
        """
        # Useful information you can extract from a GameState (pacman.py)
        successorGameState = currentGameState.generatePacmanSuccessor(action)

        if successorGameState.isWin():
            return 100000

        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        currentCapsules = currentGameState.getCapsules()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]  # not active ghost
        totalScaredTime = sum(newScaredTimes)

        "*** YOUR CODE HERE ***"
        # print("New pos: ", newPos)
        # print("New food: ", newFood.asList())
        # print("New Scared Times: ", newScaredTimes)
        # print(newGhostStates)

        # Key points and need to take into account:
        # 1. [+] food positions and number (as it was and is)
        # 2. [+] ghost is scared or not
        # 3. [+] difference in score between states
        # 4. [+] capsules and their number (as it was and is)
        # 5. [+] ghost locations and min diff to them (try to be as far as possible from them is bad practice)

        minCost = 5
        avarageCost = 100
        maxCost = 200

        score = successorGameState.getScore() - currentGameState.getScore()

        score -= minCost if action == Directions.STOP else 0

        score += avarageCost * len(currentCapsules) if newPos in currentCapsules else 0

        score += maxCost if newPos in newFood.asList() else 0

        score -= minCost * len(newFood.asList())

        costsToCurrentGhosts = [calculateCost(ghostPos.getPosition(), newPos) for ghostPos in
                                currentGameState.getGhostStates()]
        costToMinCurrentGhost = min(costsToCurrentGhosts)

        costsToGhost = [calculateCost(ghostPos.getPosition(), newPos) for ghostPos in newGhostStates]
        costToGhost = min(costsToGhost)

        if totalScaredTime > 0:
            score += maxCost if costToMinCurrentGhost < costToGhost else -avarageCost  # we want to go toward ghost
        else:
            score += -maxCost if costToMinCurrentGhost < costToGhost else avarageCost  # we don't want to meet ghost

        return score


def scoreEvaluationFunction(currentGameState: GameState):
    """
    This default evaluation function just returns the score of the state.
    The score is the same one displayed in the Pacman GUI.

    This evaluation function is meant for use with adversarial search agents
    (not reflex agents).
    """
    return currentGameState.getScore()


class MultiAgentSearchAgent(Agent):
    """
    This class provides some common elements to all of your
    multi-agent searchers.  Any methods defined here will be available
    to the MinimaxPacmanAgent, AlphaBetaPacmanAgent & ExpectimaxPacmanAgent.

    You *do not* need to make any changes here, but you can if you want to
    add functionality to all your adversarial search agents.  Please do not
    remove anything, however.

    Note: this is an abstract class: one that should not be instantiated.  It's
    only partially specified, and designed to be extended.  Agent (game.py)
    is another abstract class.
    """

    def __init__(self, evalFn='scoreEvaluationFunction', depth='2'):
        self.index = 0  # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)


class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action from the current gameState using self.depth
        and self.evaluationFunction.

        Here are some method calls that might be useful when implementing minimax.

        gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

        gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

        gameState.getNumAgents():
        Returns the total number of agents in the game

        gameState.isWin():
        Returns whether or not the game state is a winning state

        gameState.isLose():
        Returns whether or not the game state is a losing state
        """
        legalActions = gameState.getLegalActions(0)
        calculatedMinimaxes = [self.minimax(0, 0, gameState.generateSuccessor(0, action)) for action in legalActions]
        maxAnswer = max(calculatedMinimaxes)
        bestIndex = [index for index in range(len(legalActions)) if calculatedMinimaxes[index] == maxAnswer ]
        return legalActions[bestIndex[0]]

    def minimax(self, agent, depth, gameState):
        if gameState.isWin() or gameState.isLose() or self.depth == depth:
            return self.evaluationFunction(gameState)

        if agent == 0:
            return max(self.minimax(1, depth, gameState.generateSuccessor(agent, action)) for action in
                       gameState.getLegalActions(agent))
        else:
            nextAgent = agent + 1
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
            if nextAgent == 0:
                depth += 1
            return min(self.minimax(nextAgent, depth, gameState.generateSuccessor(agent, action)) for action in
                       gameState.getLegalActions(agent))


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        score, bestAction = self.alpha_beta_pruning(self.index, 0, gameState)
        return bestAction

    def alpha_beta_pruning(self, agent, depth, gameState, alpha = -100000, beta = 100000):
        legalActions = gameState.getLegalActions(agent)
        totalAgens = gameState.getNumAgents() - 1
        bestAction = None

        if gameState.isWin() or gameState.isLose() or self.depth == depth:
            return [self.evaluationFunction(gameState)]

        nextAgent = self.index if agent == totalAgens else agent + 1
        depth += 1 if agent == totalAgens else 0

        if agent == self.index:
            for action in legalActions:
                if beta <= alpha:
                    break
                nextGameState = gameState.generateSuccessor(agent, action)
                updatedAlpha = self.alpha_beta_pruning(nextAgent, depth, nextGameState, alpha, beta)[0]
                if updatedAlpha > alpha:
                    alpha = updatedAlpha
                    bestAction = action
            return alpha, bestAction
        else:
            for action in legalActions:
                if beta <= alpha:
                    break
                nextGameState = gameState.generateSuccessor(agent, action)
                updatedBeta = self.alpha_beta_pruning(nextAgent, depth, nextGameState, alpha, beta)[0]
                if updatedBeta < beta:
                    beta = updatedBeta
                    bestAction = action
            return beta, bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """

    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        legalActions = gameState.getLegalActions(0)
        calculatedMinimaxes = [self.minimax(0, 0, gameState.generateSuccessor(0, action)) for action in legalActions]
        maxAnswer = max(calculatedMinimaxes)
        bestIndex = [index for index in range(len(legalActions)) if calculatedMinimaxes[index] == maxAnswer ]
        return legalActions[bestIndex[0]]

    def expectedValue(self, agent, depth, gameState):
        legalActions = gameState.getLegalActions(agent)
        result = list()
        for action in legalActions:
            successorState = gameState.generateSuccessor(agent, action)
            result.append(self.minimax((agent + 1) % gameState.getNumAgents(), depth + 1, successorState))
        return sum(result) / len(result)

    def minimax(self, agent, depth, gameState):
        if gameState.isWin() or gameState.isLose() or self.depth == depth:
            return self.evaluationFunction(gameState)

        if agent == 0:
            return max(self.minimax(1, depth, gameState.generateSuccessor(agent, action)) for action in
                       gameState.getLegalActions(agent))
        else:
            nextAgent = agent + 1
            if gameState.getNumAgents() == nextAgent:
                nextAgent = 0
            if nextAgent == 0:
                depth += 1
            return self.expectedValue(nextAgent, depth, gameState)


def betterEvaluationFunction(currentGameState: GameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()


# Abbreviation
better = betterEvaluationFunction
