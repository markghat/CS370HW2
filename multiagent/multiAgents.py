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
import random
import util

from game import Agent


class ReflexAgent(Agent):
    """
    A reflex agent chooses an action at each choice point by examining
    its alternatives via a state evaluation function.

    The code below is provided as a guide.  You are welcome to change
    it in any way you see fit, so long as you don't touch our method
    headers.
    """

    def getAction(self, gameState):
        """
        You do not need to change this method, but you're welcome to.

        getAction chooses among the best options according to the evaluation function.

        Just like in the previous project, getAction takes a GameState and returns
        some Directions.X for some X in the set {NORTH, SOUTH, WEST, EAST, STOP}
        """
        # Collect legal moves and successor states
        legalMoves = gameState.getLegalActions()

        # Choose one of the best actions
        scores = [self.evaluationFunction(
            gameState, action) for action in legalMoves]
        bestScore = max(scores)
        bestIndices = [index for index in range(
            len(scores)) if scores[index] == bestScore]
        # Pick randomly among the best
        chosenIndex = random.choice(bestIndices)

        "Add more of your code here if you want to"

        return legalMoves[chosenIndex]

    def evaluationFunction(self, currentGameState, action):
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
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()  # make into a list
        newGhostStates = successorGameState.getGhostStates()
        # print("New Position: " + str(newPos))
        # print("New Food: " + str(newFood))
        # print("New Ghost States: " + str(newGhostStates))
        # print("New Scared Times: " + str(newScaredTimes))
        "*** YOUR CODE HERE ***"
        score = 0  # update score according to conditions of environment
        for gstate in newGhostStates:
            distFromGhost = manhattanDistance(
                newPos, gstate.getPosition())  # distance from ghost

            if distFromGhost < 3:
                score -= 30
            if newFood:
                minDist = min([manhattanDistance(newPos, food)
                              for food in newFood])
            else:
                minDist = 0
            score -= (minDist + 20*len(newFood))

        return score


def scoreEvaluationFunction(currentGameState):
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

    def getAction(self, gameState):
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
        def max_val(state, depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = float('-inf')
            # Posibble Pac Actions
            for action in state.getLegalActions(0):
                v = max(v, min_val(state.generateSuccessor(0, action), depth, 1))
            return v

        def min_val(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = float('inf')
            num_agents = state.getNumAgents()
            for action in state.getLegalActions(agentIndex):
                # Last Ghost
                if agentIndex == num_agents - 1:
                    v = min(v, max_val(state.generateSuccessor(
                        agentIndex, action), depth - 1))
                # Any Other Ghosts
                else:
                    v = min(v, min_val(state.generateSuccessor(
                        agentIndex, action), depth, agentIndex + 1))
            return v

        maximum = float('-inf')
        for action in gameState.getLegalActions(0):
            # Pac's Move
            v = min_val(gameState.generateSuccessor(0, action),
                        self.depth, 1)
            if v > maximum:
                maximum = v
                best_action = action
        return best_action if best_action else None


class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        def ABmax_val(state, depth, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = float('-inf')
            for action in state.getLegalActions(0):
                v = max(v, ABmin_val(state.generateSuccessor(
                    0, action), depth, 1, alpha, beta))
                if v > beta:  # best guaranteed option available to min
                    return v  # no longer exploring branch
                alpha = max(alpha, v)
            return v

        def ABmin_val(state, depth, agentIndex, alpha, beta):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = float('inf')
            num_agents = state.getNumAgents()
            for action in state.getLegalActions(agentIndex):
                if agentIndex == num_agents - 1:
                    v = min(v, ABmax_val(state.generateSuccessor(
                        agentIndex, action), depth - 1, alpha, beta))
                else:
                    v = min(v, ABmin_val(state.generateSuccessor(
                        agentIndex, action), depth, agentIndex + 1, alpha, beta))
                if v < alpha:  # best guaranteed option available to max
                    return v  # no longer exploring branch
                beta = min(beta, v)
            return v

        alpha = maximum = float('-inf')
        beta = float('inf')
        best_action = None
        for action in gameState.getLegalActions(0):
            v = ABmin_val(gameState.generateSuccessor(
                0, action), self.depth, 1, alpha, beta)
            if v > maximum:
                maximum = v
                best_action = action
            alpha = max(alpha, v)
        return best_action if best_action else None


class ExpectimaxAgent(MultiAgentSearchAgent):
    """
    Your expectimax agent (question 4)
    """

    def getAction(self, gameState):
        def max_val(state, depth):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            v = float('-inf')
            # Possible Pac Actions
            for action in state.getLegalActions(0):
                v = max(v, exp_val(state.generateSuccessor(0, action), depth, 1))
            return v

        def exp_val(state, depth, agentIndex):
            if state.isWin() or state.isLose() or depth == 0:
                return self.evaluationFunction(state)
            total_value = 0
            num_actions = len(state.getLegalActions(agentIndex))
            # Randomize
            prob = 1.0 / num_actions
            for action in state.getLegalActions(agentIndex):
                if agentIndex == state.getNumAgents() - 1:  # Last ghost's turn
                    # Pac's turn
                    total_value += max_val(state.generateSuccessor(
                        agentIndex, action), depth - 1) * prob
                else:
                    total_value += exp_val(state.generateSuccessor(
                        agentIndex, action), depth, agentIndex + 1) * prob  # next ghost's turn
            return total_value

        maximum = float('-inf')
        best_action = None
        for action in gameState.getLegalActions(0):
            # Pac's Move
            v = exp_val(gameState.generateSuccessor(0, action), self.depth, 1)
            if v > maximum:
                maximum = v
                best_action = action
        return best_action if best_action else None


def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: This funtion evaluates the desirability of a gien game state for PacMan based on a score that takes into account the distance to ghosts, food, and PacMan's position. The first few lines create variables, similarly to how it is done in the Q1 evaluationFunction(). Then it calculates distances to food and ghosts mased on a Manhattan heursitic. This information is then used to calculate the min distances to food and ghosts, as well as teh total distance to food. This is used to update the score to be evaluated. In order to try and get a higher score, it also takes into account the remaining time that scared ghosts are scared for.
    """
    "*** YOUR CODE HERE ***"
    """x, y = position = currentGameState.getPacmanPosition()
    ghostStates = currentGameState.getGhostStates()
    scaredTimes = [ghostState.scaredTimer for ghostState in ghostStates]
    currentFood = currentGameState.getFood().asList()

    score = 0

    for gstate in ghostStates:
        distFromGhost = manhattanDistance(
            position, gstate.getPosition())  # distance from ghost

        if distFromGhost < 3:
            score -= 20
        if currentFood:
            minDist = min([manhattanDistance(position, food)
                          for food in currentFood])
        else:
            minDist = 0
        score -= (minDist+1 + 5000*len(currentFood))
    return score"""
    """if currentGameState.isWin():
        return float("inf")
    elif currentGameState.isLose():
        return -float("inf")"""

    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

    foodDistances = [manhattanDistance(newPos, food) for food in newFood.asList()]
    minFoodDistance = min(foodDistances) if foodDistances else 0

    ghostDistances = [manhattanDistance(newPos, ghost.getPosition()) for ghost in newGhostStates]
    #scaredGhosts, activeGhosts = [], []
    #for i, ghost in enumerate(newGhostStates):
    # if newScaredTimes[i] > 0:
    #     scaredGhosts.append(ghostDistances[i])
    # else:
    #     activeGhosts.append(ghostDistances[i])

    #ghostScore = sum([(-2 / (ghostDist + 1)) for ghostDist in activeGhosts])
    #scaredGhostScore = sum([(2 / (ghostDist + 1)) for ghostDist in scaredGhosts])

    minGhostDistance = min(ghostDistances)

    totalFoodDistance = sum(foodDistances)
    remainingFoodScore = -len(newFood.asList())
    remainingScaredTime = sum(newScaredTimes)

    score = currentGameState.getScore()
    ##score += -1.5 * minFoodDistance
    if (totalFoodDistance):
        score += minGhostDistance/totalFoodDistance
    else:
        score += 0
    ##score += ghostScore
    ##score += scaredGhostScore
    score += remainingFoodScore
    score += remainingScaredTime

    return score


# Abbreviation
better = betterEvaluationFunction
