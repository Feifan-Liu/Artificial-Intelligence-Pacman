# search.py
# ---------
# Licensing Information: Please do not distribute or publish solutions to this
# project. You are free to use and extend these projects for educational
# purposes. The Pacman AI projects were developed at UC Berkeley, primarily by
# John DeNero (denero@cs.berkeley.edu) and Dan Klein (klein@cs.berkeley.edu).
# For more info, see http://inst.eecs.berkeley.edu/~cs188/sp09/pacman.html

"""
In search.py, you will implement generic search algorithms which are called
by Pacman agents (in searchAgents.py).
"""

import util
import game

class SearchProblem:
    """
    This class outlines the structure of a search problem, but doesn't implement
    any of the methods (in object-oriented terminology: an abstract class).

    You do not need to change anything in this class, ever.
    """

    def getStartState(self):
        """
        Returns the start state for the search problem
        """
        util.raiseNotDefined()

    def isGoalState(self, state):
        """
          state: Search state

        Returns True if and only if the state is a valid goal state
        """
        util.raiseNotDefined()

    def getSuccessors(self, state):
        """
          state: Search state

        For a given state, this should return a list of triples,
        (successor, action, stepCost), where 'successor' is a
        successor to the current state, 'action' is the action
        required to get there, and 'stepCost' is the incremental
        cost of expanding to that successor
        """
        util.raiseNotDefined()

    def getCostOfActions(self, actions):
        """
         actions: A list of actions to take

        This method returns the total cost of a particular sequence of actions.  The sequence must
        be composed of legal moves
        """
        util.raiseNotDefined()


def tinyMazeSearch(problem):
    """
    Returns a sequence of moves that solves tinyMaze.  For any other
    maze, the sequence of moves will be incorrect, so only use this for tinyMaze
    """
    from game import Directions
    s = Directions.SOUTH
    w = Directions.WEST
    return  [s,s,w,s,w,w,s,w]

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first
    [2nd Edition: p 75, 3rd Edition: p 87]

    Your search algorithm needs to return a list of actions that reaches
    the goal.  Make sure to implement a graph search algorithm
    [2nd Edition: Fig. 3.18, 3rd Edition: Fig 3.7].

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    "*** YOUR CODE HERE ***"
    explored = []
    solution = []
    w=game.Directions.WEST
    e=game.Directions.EAST
    s=game.Directions.SOUTH
    n=game.Directions.NORTH
    stop = game.Directions.STOP
    stack = []
    currentState = (problem.getStartState(),stop)
    stack.append(currentState)
    while len(stack) <> 0:
        currentState = stack[-1]
        if currentState[0] in explored:
            stack.pop()
            solution.pop()
            continue
        explored.append(currentState[0])
        # if(currentState[1]!=stop):
        solution.append(currentState[1])
        if(problem.isGoalState(currentState[0])): 
            solution.pop(0)
            break
        successors = problem.getSuccessors(currentState[0])
        if(successors!=None):
            for triple in successors:
                if triple[0] not in explored:
                    stateExist = False
                    for stateInQueue in stack:
                        if triple[0] == stateInQueue[0]:
                            stateExist = True
                            break
                    if stateExist == False:
                        stack.append((triple[0],triple[1]))
    return solution
    # util.raiseNotDefined()

def breadthFirstSearch(problem):
    """
    Search the shallowest nodes in the search tree first.
    [2nd Edition: p 73, 3rd Edition: p 82]
    """
    "*** YOUR CODE HERE ***"
    import operator
    explored = []
    solution = []
    w=game.Directions.WEST
    e=game.Directions.EAST
    s=game.Directions.SOUTH
    n=game.Directions.NORTH
    stop = game.Directions.STOP
    q = util.Queue()
    previous = []
    currentState = problem.getStartState()
    previous.append((-1,stop))
    q.push((currentState,0))
    while ~q.isEmpty():
        # print q.list
        currentState,index = q.pop()
        explored.append(currentState)
        # print "current list:" 
        # print currentState[1]
        if(problem.isGoalState(currentState)): 
            while(index > 0):
                pre,direction = previous[index]
                solution.insert(0,direction)
                index = pre
            break
        successors = problem.getSuccessors(currentState)
        if(successors!=None):
            for state,dir,cost in successors:
                if state not in explored:
                    stateExist = False
                    for stateInQueue in q.list:
                        if state == stateInQueue[0]:
                            stateExist = True
                            break
                    if stateExist == False:
                        previous.append((index,dir))
                        q.push((state,len(previous)-1))
                    # explored.append(state)
    return solution
    # util.raiseNotDefined()

def uniformCostSearch(problem):
    "Search the node of least total cost first. "
    "*** YOUR CODE HERE ***"
    import operator
    print problem.getSuccessors(problem.getStartState())
    explored = []
    solution = []
    w=game.Directions.WEST
    e=game.Directions.EAST
    s=game.Directions.SOUTH
    n=game.Directions.NORTH
    stop = game.Directions.STOP
    q = []
    previous = []
    currentState = problem.getStartState()
    previous.append((-1,stop))
    q.append((currentState,0,0))
    while len(q)<>0:
        currentState,index,currentCost = min(q,key=operator.itemgetter(2))
        q.remove((currentState,index,currentCost))
        if currentState in explored: continue
        explored.append(currentState)
        if(problem.isGoalState(currentState)): 
            while(True):
                pre,direction = previous[index]
                solution.insert(0,direction)
                index = pre
                if index == 0: break
            break
        successors = problem.getSuccessors(currentState)
        if(successors!=None):
            for state,dir,cost in successors:
                if state not in explored:
                    previous.append((index,dir))
                    q.append((state,len(previous)-1,currentCost+cost))
    return solution
    # util.raiseNotDefined()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    "Search the node that has the lowest combined cost and heuristic first."
    "*** YOUR CODE HERE ***"
    import operator
    explored = []
    solution = []
    w=game.Directions.WEST
    e=game.Directions.EAST
    s=game.Directions.SOUTH
    n=game.Directions.NORTH
    stop = game.Directions.STOP
    q = []
    previous = []
    currentState = problem.getStartState()
    previous.append((-1,stop))
    q.append((currentState,0,0,heuristic(currentState,problem)))
    while len(q)<>0:
        currentState,index,currentCost,fn = min(q,key=operator.itemgetter(3))
        q.remove((currentState,index,currentCost,fn))
        if currentState in explored: continue
        explored.append(currentState)
        if(problem.isGoalState(currentState)): 
            while(True):
                pre,direction = previous[index]
                solution.insert(0,direction)
                index = pre
                if index == 0: break
            break
        successors = problem.getSuccessors(currentState)
        if(successors!=None):
            for state,dir,cost in successors:
                if state not in explored:
                    previous.append((index,dir))
                    q.append((state,len(previous)-1,currentCost+cost,currentCost+cost+heuristic(state,problem)))
    return solution
    # util.raiseNotDefined()



# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
