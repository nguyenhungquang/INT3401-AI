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
        some Directions.X for some X in the set {North, South, West, East, Stop}
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
        newFood = successorGameState.getFood()
        newGhostStates = successorGameState.getGhostStates()
        newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
        isStop=0
        if action=="Stop":
            isStop=2
        "*** YOUR CODE HERE ***"
        minDistance=999999
        m=0
        n=0
        for i in newFood:
            for j in i:
                if newFood[m][n]:
                    minDistance=min(minDistance,manhattanDistance(newPos,(m,n)))
                    #print m,n,newPos,minDistance
                n+=1
            n=0
            m+=1
        ghostDistance=min([manhattanDistance(newPos,ghost.getPosition()) for ghost in newGhostStates])
        if ghostDistance<=1:
            return 0
        if currentGameState.getFood()[newPos[0]][newPos[1]]:
            return float("inf")
        #if newScaredTimes>1:
        #    ghostDistance=1
        evaluation = successorGameState.getScore()+ghostDistance/(minDistance+isStop)
        #print evaluation,ghostDistance,minDistance
        return evaluation

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

    def __init__(self, evalFn = 'scoreEvaluationFunction', depth = '2'):
        self.index = 0 # Pacman is always agent index 0
        self.evaluationFunction = util.lookup(evalFn, globals())
        self.depth = int(depth)

class MinimaxAgent(MultiAgentSearchAgent):
    """
      Your minimax agent (question 2)
    """

    def max_value(self,gameState,depth,index):
        v=-99999
        move=""
        #if gameState.isWin or gameState.isLose or index>=self.depth*gameState.getNumAgents():
        #    return self.evaluationFunction(gameState)
        #else:
        actions=gameState.getLegalActions(index)
        #if not actions:
        #    return [self.evaluationFunction(gameState),""]
        for action in actions:
            temp=self.mmvalue(gameState.generateSuccessor(index,action),depth,index+1)
            if v<temp[0]:
                v=temp[0]
                move=action
        return [v,move]
    def min_value(self,gameState,depth,index):
        v=99999
        move =""
        #if gameState.isWin or gameState.isLose or index>=self.depth*gameState.getNumAgents():
        #    return self.evaluationFunction(gameState)
        #else:
        actions=gameState.getLegalActions(index)
        #if not actions:
        #    return [self.evaluationFunction(gameState),""]
        for action in actions:
            temp=self.mmvalue(gameState.generateSuccessor(index,action),depth,index+1)
            if v>temp[0]:
                v=temp[0]
                move=action
        return [v,move]
    def mmvalue(self,gameState,depth,agentNumber):
        if agentNumber>=gameState.getNumAgents():
            depth+=1
        agentNumber=agentNumber%gameState.getNumAgents()
        if gameState.isLose() or gameState.isWin() or depth==self.depth:
            return [self.evaluationFunction(gameState),""]
        elif agentNumber==0:
            return self.max_value(gameState,depth,agentNumber)
        else:
            return self.min_value(gameState,depth,agentNumber)

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
        """
        "*** YOUR CODE HERE ***"
        #print self.min_value(gameState,0) 
        #util.raiseNotDefined()
        return self.mmvalue(gameState,0,0)[1]
class AlphaBetaAgent(MultiAgentSearchAgent):
    def max_value(self,gameState,depth,index,a,b):
        v=-99999
        move=""
        #if gameState.isWin or gameState.isLose or index>=self.depth*gameState.getNumAgents():
        #    return self.evaluationFunction(gameState)
        #else:
        actions=gameState.getLegalActions(index)
        #if not actions:
        #    return [self.evaluationFunction(gameState),""]
        for action in actions:
            temp=self.mmvalue(gameState.generateSuccessor(index,action),depth,index+1,a,b)
            if v<temp[0]:
                v=temp[0]
                move=action
            if v>b:
                return [v,action]
            a=max(a,v)
        return [v,move]
    def min_value(self,gameState,depth,index,a,b):
        v=99999
        move =""
        #if gameState.isWin or gameState.isLose or index>=self.depth*gameState.getNumAgents():
        #    return self.evaluationFunction(gameState)
        #else:
        actions=gameState.getLegalActions(index)
        #if not actions:
        #    print [self.evaluationFunction(gameState),""]
        for action in actions:
            temp=self.mmvalue(gameState.generateSuccessor(index,action),depth,index+1,a,b)
            if v>temp[0]:
                v=temp[0]
                move=action
            if v<a:
                return [v,action]
            b=min(b,v)
        return [v,move]
    def mmvalue(self,gameState,depth,agentNumber,a,b):
        if agentNumber>=gameState.getNumAgents():
            depth+=1
        agentNumber=agentNumber%gameState.getNumAgents()
        if gameState.isLose() or gameState.isWin() or depth==self.depth:
            return [self.evaluationFunction(gameState),""]
        elif agentNumber==0:
            return self.max_value(gameState,depth,agentNumber,a,b)
        else:
            return self.min_value(gameState,depth,agentNumber,a,b)

    """
      Your minimax agent with alpha-beta pruning (question 3)
    """

    def getAction(self, gameState):
        """
          Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        return self.mmvalue(gameState,0,0,-float("inf"),float("inf"))[1]

class ExpectimaxAgent(MultiAgentSearchAgent):
    """
      Your expectimax agent (question 4)
    """
    def max_value(self,gameState,depth,index):
        v=-99999
        move=""
        #if gameState.isWin or gameState.isLose or index>=self.depth*gameState.getNumAgents():
        #    return self.evaluationFunction(gameState)
        #else:
        actions=gameState.getLegalActions(index)
        #if not actions:
        #    print [self.evaluationFunction(gameState),""]
        for action in actions:
            temp=self.mmvalue(gameState.generateSuccessor(index,action),depth,index+1)
            if v<temp[0]:
                v=temp[0]
                move=action
        return [v,move]
    def exp_value(self,gameState,depth,index):
        v=99999
        move =""
        #if gameState.isWin or gameState.isLose or index>=self.depth*gameState.getNumAgents():
        #    return self.evaluationFunction(gameState)
        #else:
        actions=gameState.getLegalActions(index)
        p=1/len(actions)
        #if not actions:
        #    print [self.evaluationFunction(gameState),""]
        #for action in actions:
        v=sum([self.mmvalue(gameState.generateSuccessor(index,action),depth,index+1)[0] for action in actions])
        return [v,""]
    def mmvalue(self,gameState,depth,agentNumber):
        if agentNumber>=gameState.getNumAgents():
            depth+=1
        agentNumber=agentNumber%gameState.getNumAgents()
        if gameState.isLose() or gameState.isWin() or depth==self.depth:
            return [self.evaluationFunction(gameState),""]
        elif agentNumber==0:
            return self.max_value(gameState,depth,agentNumber)
        else:
            return self.exp_value(gameState,depth,agentNumber)

    def getAction(self, gameState):
        """
          Returns the expectimax action using self.depth and self.evaluationFunction

          All ghosts should be modeled as choosing uniformly at random from their
          legal moves.
        """
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()
        return self.mmvalue(gameState,0,0)[1]

def betterEvaluationFunction(currentGameState):
    """
      Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
      evaluation function (question 5).

      DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    newPos = currentGameState.getPacmanPosition()
    newFood = currentGameState.getFood()
    newGhostStates = currentGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    foodSet=[]
    heuristicVal=0
    #isStop=0
    #if action=="Stop":
    #    isStop=2
    "*** YOUR CODE HERE ***"
    minDistance=999999
    m=0
    n=0
    for i in newFood:
        for j in i:
            if newFood[m][n]:
                foodSet.append((m,n))
                minDistance=min(minDistance,manhattanDistance(newPos,(m,n)))
                #print m,n,newPos,minDistance
            n+=1
        n=0
        m+=1
    if len(foodSet)>0:
        firstFood=foodSet[0]
        diameter,lastFood=max((manhattanDistance(firstFood,otherFood),otherFood) for otherFood in foodSet)
        heuristicVal=min(manhattanDistance(newPos,x) for x in (firstFood,lastFood))+diameter
    #else:
    #    heuristicVal=-float("inf")
    ghostDistance=min([manhattanDistance(newPos,ghost.getPosition()) for ghost in newGhostStates])
    if ghostDistance<=1:
        return -float("inf")
    if newScaredTimes>1:
        ghostDistance=-0.5*ghostDistance
    evaluation = currentGameState.getScore()+ghostDistance-heuristicVal-20*len(foodSet)
    return evaluation
    #util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction

