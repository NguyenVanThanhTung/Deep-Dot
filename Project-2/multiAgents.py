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
        chosenIndex = random.choice(bestIndices) # Pick randomly among the best

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
        # successorGameState = currentGameState.generatePacmanSuccessor(action)
        # newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood()
        # newGhostStates = successorGameState.getGhostStates()
        # newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]

        "*** YOUR CODE HERE ***"
        successorGameState = currentGameState.generatePacmanSuccessor(action)
        score = successorGameState.getScore()
        newPos = successorGameState.getPacmanPosition()
        newFood = successorGameState.getFood().asList()
        newGhostStates = successorGameState.getGhostStates()

        if len(newFood) > 0:
            foodDistances = [manhattanDistance(newPos, food) for food in newFood]
            minFoodDist = min(foodDistances)
            score += 10 / (minFoodDist + 1)
            score -= 2 * len(newFood)

        for ghost in newGhostStates:
            ghostPos = ghost.getPosition()
            dist = manhattanDistance(newPos, ghostPos)

            if ghost.scaredTimer > 0:
                # can eat ghost
                score += 5 / (dist + 1)
            else:
                # dangerous ghost
                if dist < 2:
                    score -= 500
                else:
                    score -= 2 / (dist + 1)

        return score

        # # version phức tạp hơn
        # successorGameState = currentGameState.generatePacmanSuccessor(action)
        # if successorGameState.isWin():
        #     return float("inf")
        # if successorGameState.isLose():
        #     return -float("inf")

        # from game import Directions

        # score = successorGameState.getScore()

        # newPos = successorGameState.getPacmanPosition()
        # newFood = successorGameState.getFood().asList()
        # newGhosts = successorGameState.getGhostStates()
        # newCapsules = successorGameState.getCapsules()

        # # =========================
        # # GHOST ANALYSIS
        # # =========================
        # danger = False
        # nearestGhostDist = float("inf")

        # for ghost in newGhosts:
        #     dist = manhattanDistance(newPos, ghost.getPosition())
        #     nearestGhostDist = min(nearestGhostDist, dist)

        #     if ghost.scaredTimer == 0 and dist <= 3:
        #         danger = True

        # # =========================
        # # CAPSULE LOGIC
        # # =========================
        # if newCapsules:
        #     capsuleDists = [manhattanDistance(newPos, c) for c in newCapsules]
        #     minCapsuleDist = min(capsuleDists)

        #     if danger:
        #         score += 80 / (minCapsuleDist + 1)

        # # =========================
        # # GHOST SCORING (FIXED ZONES)
        # # =========================
        # for ghost in newGhosts:
        #     dist = manhattanDistance(newPos, ghost.getPosition())

        #     if ghost.scaredTimer > 0:
        #         score += 200 / (dist + 1)
        #     else:
        #         if dist <= 1:
        #             score -= 500
        #         elif dist == 2:
        #             score -= 200
        #         elif dist == 3:
        #             score -= 80
        #         else:
        #             score -= 5 / (dist + 1)

        # # =========================
        # # FOOD LOGIC (FIXED SCOPE)
        # # =========================
        # foodDists = []

        # if newFood:
        #     foodDists = [manhattanDistance(newPos, f) for f in newFood]
        #     minFoodDist = min(foodDists)

        #     if not danger:
        #         score += 15 / (minFoodDist + 1)
        #     else:
        #         score += 5 / (minFoodDist + 1)

        #     score -= 2 * len(newFood)

        # # =========================
        # # ENDGAME PRIORITY (SAFE CAPSULE vs FOOD)
        # # =========================
        # if len(newFood) == 1 and newCapsules:
        #     if nearestGhostDist <= 3 and foodDists:
        #         score -= 30 / (min(foodDists) + 1)

        # # =========================
        # # STOP PENALTY (FIXED DUPLICATE)
        # # =========================
        # if action == Directions.STOP:
        #     score -= 10

        # # =========================
        # # DEAD END PENALTY
        # # =========================
        # legal = currentGameState.getLegalActions()
        # if len(legal) <= 2:
        #     score -= 20

        # return score

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
    Your minimax agent (question 2)
    """
    def minimax(self, gameState: GameState, agentIndex, depth):
        numAgents = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if depth == self.depth:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            bestValue = -float('inf')
            nextAgent = agentIndex + 1
            nextDepth = depth

            legalMoves = gameState.getLegalActions(agentIndex)
            if not legalMoves:
                return self.evaluationFunction(gameState)
            
            for legalMove in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, legalMove)
                value = self.minimax(successor, nextAgent,  nextDepth)
                bestValue = max(bestValue, value)
            return bestValue
        else:
            bestValue = float('inf')
            nextAgent = agentIndex + 1

            if agentIndex == numAgents - 1:
                nextAgent = 0
                nextDepth = depth + 1
            else:
                nextDepth = depth

            legalMoves = gameState.getLegalActions(agentIndex)
            if not legalMoves:
                return self.evaluationFunction(gameState)
            
            for legalMove in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, legalMove)
                value = self.minimax(successor, nextAgent, nextDepth)
                bestValue = min(bestValue, value)
            return bestValue

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
        "*** YOUR CODE HERE ***"
        bestValue = -float('inf')
        bestAction = None

        legalMoves = gameState.getLegalActions(0)
        if not legalMoves:
            return self.evaluationFunction(gameState)
            
        for legalMove in legalMoves:
            successor = gameState.generateSuccessor(0, legalMove)
            value = self.minimax(successor, 1, 0)
            if value > bestValue:
                bestValue = value
                bestAction = legalMove
        
        return bestAction

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    def alphabeta(self, gameState: GameState, agentIndex, depth, alpha, beta):
        numAgents = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if depth == self.depth:
            return self.evaluationFunction(gameState)

        legalMoves = gameState.getLegalActions(agentIndex)
        if not legalMoves:
            return self.evaluationFunction(gameState)
        
        if agentIndex == 0:
            bestValue = -float('inf')
            nextAgent = agentIndex + 1
            nextDepth = depth
            
            for legalMove in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, legalMove)
                value = self.alphabeta(successor, nextAgent, nextDepth, alpha, beta)
                bestValue = max(bestValue, value)
                if bestValue > beta:
                    return bestValue
                alpha = max(alpha, bestValue)
            return bestValue
        else:
            bestValue = float('inf')
            nextAgent = agentIndex + 1

            if agentIndex == numAgents - 1:
                nextAgent = 0
                nextDepth = depth + 1
            else:
                nextDepth = depth
            
            for legalMove in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, legalMove)
                value = self.alphabeta(successor, nextAgent, nextDepth, alpha, beta)
                bestValue = min(bestValue, value)
                if bestValue < alpha:
                    return bestValue
                beta = min(beta, bestValue)
            return bestValue

    def getAction(self, gameState: GameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        alpha = -float('inf')
        beta = float('inf')
        bestValue = -float('inf')
        bestAction = None

        legalMoves = gameState.getLegalActions(0)
        if not legalMoves:
            return self.evaluationFunction(gameState)
            
        for legalMove in legalMoves:
            successor = gameState.generateSuccessor(0, legalMove)
            value = self.alphabeta(successor, 1, 0, alpha, beta)
            if value > bestValue:
                bestValue = value
                bestAction = legalMove
            alpha = max(alpha, bestValue)

        return bestAction

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def expectimax(self, gameState: GameState, agentIndex, depth):
        numAgents = gameState.getNumAgents()
        if gameState.isWin() or gameState.isLose():
            return self.evaluationFunction(gameState)
        if depth == self.depth:
            return self.evaluationFunction(gameState)
        
        
        legalMoves = gameState.getLegalActions(agentIndex)
        if not legalMoves:
            return self.evaluationFunction(gameState)

        if agentIndex == 0:
            bestValue = -float('inf')
            nextAgent = agentIndex + 1
            nextDepth = depth

            for legalMove in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, legalMove)
                value = self.expectimax(successor, nextAgent,  nextDepth)
                bestValue = max(bestValue, value)
            return bestValue
        else:
            totalValue = 0
            nextAgent = agentIndex + 1

            if agentIndex == numAgents - 1:
                nextAgent = 0
                nextDepth = depth + 1
            else:
                nextDepth = depth

            for legalMove in legalMoves:
                successor = gameState.generateSuccessor(agentIndex, legalMove)
                value = self.expectimax(successor, nextAgent, nextDepth)
                totalValue = totalValue + value
            return totalValue/len(legalMoves)


    def getAction(self, gameState: GameState):
        """
        Returns the expectimax action using self.depth and self.evaluationFunction

        All ghosts should be modeled as choosing uniformly at random from their
        legal moves.
        """
        "*** YOUR CODE HERE ***"
        bestValue = -float('inf')
        bestAction = None

        legalMoves = gameState.getLegalActions(0)
        if not legalMoves:
            return self.evaluationFunction(gameState)
            
        for legalMove in legalMoves:
            successor = gameState.generateSuccessor(0, legalMove)
            value = self.expectimax(successor, 1, 0)
            if value > bestValue:
                bestValue = value
                bestAction = legalMove
        
        return bestAction

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
