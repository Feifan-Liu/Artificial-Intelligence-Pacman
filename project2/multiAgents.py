# multiAgents.py
# --------------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

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
    newFood = successorGameState.getFood().asList()
    newGhostStates = successorGameState.getGhostStates()
    newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
    if successorGameState.isLose(): 
      return -float("inf")
    elif successorGameState.isWin():
      return float("inf")
    disToClosestFood = 0
    disToClosestGhostNotScared = 0
    disToClosestGhostScared = 0
    disToPowerUp = float("inf")
    numberOfFood = len(newFood)
    disList = []
    for food in newFood:
      disList.append(util.manhattanDistance(newPos,food))
    if len(disList) > 0:
      disToClosestFood = min(disList)
    ghostNotScared = []
    ghostScared = []
    for ghost in newGhostStates:
      if ghost.scaredTimer:
        ghostScared.append(ghost)
      else: ghostNotScared.append(ghost)

    disList = []
    for ghost in ghostNotScared:
      disList.append(util.manhattanDistance(newPos,ghost.getPosition()))
    if len(disList) > 0:
      disToClosestGhostNotScared = min(disList)
    disToClosestGhostNotScared = max(disToClosestGhostNotScared,1)

    disList = []
    for ghost in ghostScared:
      disList.append(util.manhattanDistance(newPos,ghost.getPosition()))
    if len(disList) > 0:
      disToClosestGhostScared = min(disList)

    # disList = []
    # for powerUp in successorGameState.getCapsules():
    #   disList.append(util.manhattanDistance(newPos,powerUp))
    # if len(disList) > 0:
    #   disToPowerUp = min(disList)
    #   disToPowerUp = min(disToPowerUp,5)
    disToPowerUp = len(successorGameState.getCapsules())
    return successorGameState.getScore() - disToClosestFood - 4 * numberOfFood - 20 * disToPowerUp - 2 * 1.0/disToClosestGhostNotScared - 2 * disToClosestGhostScared

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

  def getAction(self, gameState):
    """
      Returns the minimax action from the current gameState using self.depth
      and self.evaluationFunction.

      Here are some method calls that might be useful when implementing minimax.

      gameState.getLegalActions(agentIndex):
        Returns a list of legal actions for an agent
        agentIndex=0 means Pacman, ghosts are >= 1

      Directions.STOP:
        The stop direction, which is always legal

      gameState.generateSuccessor(agentIndex, action):
        Returns the successor game state after an agent takes an action

      gameState.getNumAgents():
        Returns the total number of agents in the game
    """
    "*** YOUR CODE HERE ***"
    return self.getMiniMaxValue(0,gameState,0)

  def getMiniMaxValue(self, agentIndex, gameState, depth):
    if gameState.isLose() or gameState.isWin():
      return self.evaluationFunction(gameState)
    legalActions = gameState.getLegalActions(agentIndex)
    resAction = Directions.STOP
    value = 0
    if agentIndex == 0:
      value = float("-inf")
      for action in legalActions:
        if action == Directions.STOP: continue
        minimax = self.getMiniMaxValue((agentIndex+1)%gameState.getNumAgents(), gameState.generateSuccessor(agentIndex,action), depth)
        if minimax > value:
          value = minimax
          resAction = action
      if depth == 0: 
        return resAction
      else: return value
    else:
      value = float("inf")
      if agentIndex == gameState.getNumAgents() - 1: 
        depth = depth + 1
        if depth == self.depth:
          for action in legalActions:
            value = min(value, self.evaluationFunction(gameState.generateSuccessor(agentIndex,action)))
          return value
      for action in legalActions:
        value = min(value, self.getMiniMaxValue((agentIndex+1)%gameState.getNumAgents(), gameState.generateSuccessor(agentIndex,action), depth))
      return value

class AlphaBetaAgent(MultiAgentSearchAgent):
  """
    Your minimax agent with alpha-beta pruning (question 3)
  """

  def getAction(self, gameState):
    """
      Returns the minimax action using self.depth and self.evaluationFunction
    """
    "*** YOUR CODE HERE ***"
    return self.getMiniMaxValue(0,gameState,0,float("-inf"),float("inf"))
  
  def getMiniMaxValue(self, agentIndex, gameState, depth, alpha, beta):
    if gameState.isLose() or gameState.isWin():
      return self.evaluationFunction(gameState)
    legalActions = gameState.getLegalActions(agentIndex)
    resAction = Directions.STOP
    value = 0
    if agentIndex == 0:
      value = float("-inf")
      for action in legalActions:
        if action == Directions.STOP: continue
        minimax = self.getMiniMaxValue((agentIndex+1)%gameState.getNumAgents(), gameState.generateSuccessor(agentIndex,action), depth, alpha, beta)
        if minimax > value:
          value = minimax
          resAction = action
        alpha = max(alpha,value)
        if alpha >= beta:
          if depth == 0: 
            return resAction
          else: return value
      if depth == 0: 
        return resAction
      else: return value
    else:
      value = float("inf")
      if agentIndex == gameState.getNumAgents() - 1: 
        depth = depth + 1
        if depth == self.depth:
          for action in legalActions:
            value = min(value, self.evaluationFunction(gameState.generateSuccessor(agentIndex,action)))
            beta = min(beta,value)
            if alpha >= beta: return value
          return value
      for action in legalActions:
        value = min(value, self.getMiniMaxValue((agentIndex+1)%gameState.getNumAgents(), gameState.generateSuccessor(agentIndex,action), depth, alpha, beta))
        beta = min(beta,value)
        if alpha >= beta: return value
      return value

class ExpectimaxAgent(MultiAgentSearchAgent):
  """
    Your expectimax agent (question 4)
  """

  def getAction(self, gameState):
    """
      Returns the expectimax action using self.depth and self.evaluationFunction

      All ghosts should be modeled as choosing uniformly at random from their
      legal moves.
    """
    "*** YOUR CODE HERE ***"
    return self.getMiniMaxValue(0,gameState,0)
  
  def getMiniMaxValue(self, agentIndex, gameState, depth):
    if gameState.isLose() or gameState.isWin():
      return self.evaluationFunction(gameState)
    legalActions = gameState.getLegalActions(agentIndex)
    numberOfActions = len(legalActions)
    resAction = Directions.STOP
    value = 0
    if agentIndex == 0:
      value = float("-inf")
      for action in legalActions:
        if action == Directions.STOP: continue
        minimax = self.getMiniMaxValue((agentIndex+1)%gameState.getNumAgents(), gameState.generateSuccessor(agentIndex,action), depth)
        if minimax > value:
          value = minimax
          resAction = action
      if depth == 0: 
        return resAction
      else: return value
    else:
      value = 0
      if agentIndex == gameState.getNumAgents() - 1: 
        depth = depth + 1
        if depth == self.depth:
          for action in legalActions:
            value += self.evaluationFunction(gameState.generateSuccessor(agentIndex,action))
          value = value / numberOfActions
          return value
      for action in legalActions:
        value += self.getMiniMaxValue((agentIndex+1)%gameState.getNumAgents(), gameState.generateSuccessor(agentIndex,action), depth)
      value = value / numberOfActions
      return value

def betterEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood().asList()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  if currentGameState.isLose(): 
    return -float("inf")
  elif currentGameState.isWin():
    return float("inf")
  disToClosestFood = 0
  disToClosestGhostNotScared = float("inf")
  disToClosestGhostScared = 0
  numberOfPowerUp = 0
  numberOfFood = len(newFood) # the number of food, which we wish to be smaller
  disList = []
  for food in newFood:
    disList.append(util.manhattanDistance(newPos,food))
  if len(disList) > 0:
    disToClosestFood = min(disList) # the shortest distance to the closet food, which we wish to be smaller
  ghostNotScared = []
  ghostScared = []
  for ghost in newGhostStates:
    if ghost.scaredTimer:
      ghostScared.append(ghost)
    else: ghostNotScared.append(ghost)

  disList = []
  for ghost in ghostNotScared:
    disList.append(util.manhattanDistance(newPos,ghost.getPosition()))
  if len(disList) > 0:
    disToClosestGhostNotScared = min(disList) # the shortest distance to the closet ghost that's not scared, which we wish to be greater
  disToClosestGhostNotScared = max(disToClosestGhostNotScared,1) # in case the distance is 0

  disList = []
  for ghost in ghostScared:
    disList.append(util.manhattanDistance(newPos,ghost.getPosition()))
  if len(disList) > 0:
    disToClosestGhostScared = min(disList) # the shortest distance to the closet ghost that's scared, which we wish to be smaller
  numberOfPowerUp = len(currentGameState.getCapsules()) # the number of powerups, which we wish to be smaller
  return currentGameState.getScore() - disToClosestFood - 4 * numberOfFood - 50 * numberOfPowerUp - 2 * 1.0/disToClosestGhostNotScared - 2 * disToClosestGhostScared

# Abbreviation
better = betterEvaluationFunction

class ContestAgent(MultiAgentSearchAgent):
  """
    Your agent for the mini-contest
  """
  def __init__(self, evalFn = 'contestEvaluationFunction', depth = '3'):
    self.index = 0 # Pacman is always agent index 0
    self.evaluationFunction = util.lookup(evalFn, globals())
    self.depth = int(depth)

  def getAction(self, gameState):
    """
      Returns an action.  You can use any method you want and search to any depth you want.
      Just remember that the mini-contest is timed, so you have to trade off speed and computation.

      Ghosts don't behave randomly anymore, but they aren't perfect either -- they'll usually
      just make a beeline straight towards Pacman (or away from him if they're scared!)
    """
    "*** YOUR CODE HERE ***"
    return self.getMiniMaxValue(0,gameState,0,float("-inf"),float("inf"))
  
  def getMiniMaxValue(self, agentIndex, gameState, depth, alpha, beta):
    if gameState.isLose() or gameState.isWin():
      return self.evaluationFunction(gameState)
    legalActions = gameState.getLegalActions(agentIndex)
    resAction = Directions.STOP
    value = 0
    if agentIndex == 0:
      value = float("-inf")
      for action in legalActions:
        if action == Directions.STOP: continue
        state = gameState.generateSuccessor(agentIndex,action)
        # if state.isWin():
        #   if depth == 0:
        #     return action
        #   else: return float("inf")
        # elif state.isLose():
        #   if depth == 0:
        #     if value == float("-inf"):
        #       resAction = action
        #       continue
        #   else: return float("-inf")
        minimax = self.getMiniMaxValue((agentIndex+1)%gameState.getNumAgents(), state, depth, alpha, beta)
        if minimax > value:
          value = minimax
          resAction = action
        alpha = max(alpha,value)
        if alpha >= beta:
          if depth == 0: 
            return resAction
          else: return value
      if depth == 0: 
        return resAction
      else: return value
    else:
      value = float("inf")
      if agentIndex == gameState.getNumAgents() - 1: 
        depth = depth + 1
        if depth == self.depth:
          for action in legalActions:
            value = min(value, self.evaluationFunction(gameState.generateSuccessor(agentIndex,action)))
            beta = min(beta,value)
            if alpha >= beta: return value
          return value
      for action in legalActions:
        value = min(value, self.getMiniMaxValue((agentIndex+1)%gameState.getNumAgents(), gameState.generateSuccessor(agentIndex,action), depth, alpha, beta))
        beta = min(beta,value)
        if alpha >= beta: return value
      return value

def contestEvaluationFunction(currentGameState):
  """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
  """
  "*** YOUR CODE HERE ***"
  newPos = currentGameState.getPacmanPosition()
  newFood = currentGameState.getFood().asList()
  newGhostStates = currentGameState.getGhostStates()
  newScaredTimes = [ghostState.scaredTimer for ghostState in newGhostStates]
  if currentGameState.isLose(): 
    return -float("inf")
  elif currentGameState.isWin():
    return float("inf")
  disToClosestFood = 0
  disToClosestGhostNotScared = float("inf")
  disToClosestGhostScared = 0
  disToClosestPowerUp = 0
  numberOfPowerUp = 0
  numberOfFood = len(newFood) # the number of food, which we wish to be smaller
  disList = []
  for food in newFood:
    disList.append(util.manhattanDistance(newPos,food))
  if len(disList) > 0:
    disToClosestFood = min(disList) # the shortest distance to the closet food, which we wish to be smaller
  ghostNotScared = []
  ghostScared = []
  for ghost in newGhostStates:
    if ghost.scaredTimer:
      ghostScared.append(ghost)
    else: ghostNotScared.append(ghost)

  disList = []
  for ghost in ghostNotScared:
    disList.append(util.manhattanDistance(newPos,ghost.getPosition()))
  if len(disList) > 0:
    disToClosestGhostNotScared = min(disList) # the shortest distance to the closet ghost that's not scared, which we wish to be greater
  disToClosestGhostNotScared = max(disToClosestGhostNotScared,1) # in case the distance is 0
  if disToClosestGhostNotScared > 8:
    disToClosestGhostNotScared = float("inf")

  disList = []
  for ghost in ghostScared:
    disList.append(util.manhattanDistance(newPos,ghost.getPosition()))
  if len(disList) > 0:
    disToClosestGhostScared = min(disList) # the shortest distance to the closet ghost that's scared, which we wish to be smaller
  if disToClosestGhostScared > 8:
    disToClosestGhostScared = 0
  powerUps = currentGameState.getCapsules()
  numberOfPowerUp = len(powerUps) # the number of powerups, which we wish to be smaller

  disList = []
  for power in powerUps:
    disList.append(util.manhattanDistance(newPos,power))
  if len(disList) > 0:
    disToClosestPowerUp = min(disList) 
  if len(ghostScared) > 2:
    dontEatPowerUp = True
    for ghost in ghostScared:
      if ghost.scaredTimer < 5:
        dontEatPowerUp = False
        break
    if dontEatPowerUp:
      numberOfPowerUp = -numberOfPowerUp
      disToClosestPowerUp = 0
  if disToClosestPowerUp > 4:
    disToClosestPowerUp = 0
  
  return currentGameState.getScore() - 3.5 * disToClosestFood - 10 * numberOfFood - 20 * numberOfPowerUp - disToClosestPowerUp - 2 * 1.0/disToClosestGhostNotScared - 1.5*disToClosestGhostScared

# def breadthFirstSearch(currentState):
#     """
#     Search the shallowest nodes in the search tree first.
#     [2nd Edition: p 73, 3rd Edition: p 82]
#     """
#     "*** YOUR CODE HERE ***"
#     import operator
#     explored = []
#     solution = []
#     w=Directions.WEST
#     e=Directions.EAST
#     s=Directions.SOUTH
#     n=Directions.NORTH
#     stop = Directions.STOP
#     foodList = currentState.getFood().asList()
#     q = util.Queue()
#     previous = []
#     previous.append((-1,stop))
#     q.push((currentState,0))
#     while ~q.isEmpty():
#         # print q.list
#         currentState,index = q.pop()
#         explored.append(currentState)
#         # print "current list:" 
#         # print currentState[1]
#         if(currentState.getPacmanPosition() in foodList): 
#             while(index > 0):
#                 pre,direction = previous[index]
#                 solution.insert(0,direction)
#                 index = pre
#             break
#         successors = []
#         for action in currentState.getLegalActions():
#           successors.append((currentState.generateSuccessor(0,action),action,1))
#         if(successors!=None):
#             for state,dir,cost in successors:
#                 if state not in explored:
#                     stateExist = False
#                     for stateInQueue in q.list:
#                         if state == stateInQueue[0]:
#                             stateExist = True
#                             break
#                     if stateExist == False:
#                         previous.append((index,dir))
#                         q.push((state,len(previous)-1))
#                     # explored.append(state)
#     return len(solution)