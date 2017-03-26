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
import copy

class SearchNode:
    """
    This class represents a node in the graph which represents the search problem.
    The class is used as a basic wrapper for search methods - you may use it, however
    you can solve the assignment without it.

    REMINDER: You need to fill in the backtrack function in this class!
    """

    def __init__(self, state, parent=None, transition=None, cost=0, heuristic=0):
        """
        Basic constructor which copies the values. Remember, you can access all the 
        values of a python object simply by referencing them - there is no need for 
        a getter method. 
        """
        self.state = state
        self.parent = parent
        self.cost = cost
        self.heuristic = heuristic
        self.transition = transition

    def isRootNode(self):
        """
        Check if the node has a parent.
        returns True in case it does, False otherwise
        """
        return self.parent == None 

    def unpack(self):
        """
        Return all relevant values for the current node.
        Returns position, parent node, cost, heuristic value
        """
        return self.state, self.parent, self.cost, self.heuristic

    def backtrack(self):
        """
        Reconstruct a path to the initial state from the current node.
        Bear in mind that usually you will reconstruct the path from the 
        final node to the initial.
        """
        moves = []
        # make a deep copy to stop any referencing isues.
        node = copy.deepcopy(self)

        if node.isRootNode(): 
            # The initial state is the final state
            return moves
        
        moves = node.parent.backtrack()
        moves.append(node.transition)
        return moves  

        "**YOUR CODE HERE**"
        util.raiseNotDefined()
    
    def expand(self, succ):
        childrenNodes = []
        for item in succ:
            childrenNodes.append(SearchNode(item[0], self, item[1], self.cost + item[2]))
        return childrenNodes


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

def depthFirstSearch(problem):
    """
    Search the deepest nodes in the search tree first.

    Your search algorithm needs to return a list of actions that reaches the
    goal. Make sure to implement a graph search algorithm.

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())
    """
    open = util.Stack()
    visited = set()
    initialNode = SearchNode (problem.getStartState())
    open.push(initialNode)
    while not open.isEmpty():
        n = open.pop()
        while n.state in visited:
            n = open.pop()
        visited.add(n.state)
        if problem.isGoalState(n.state):
            return n.backtrack()
        lista = n.expand(problem.getSuccessors(n.state))
        for m in lista:
            if m.state not in visited:
                open.push(m)
    return util.raiseSolutionNotFound()

def breadthFirstSearch(problem):
    """Search the shallowest nodes in the search tree first."""
    open = util.Queue()
    visited = set()
    initialNode = SearchNode (problem.getStartState())
    open.push(initialNode)
    while not open.isEmpty():
        n = open.pop()
        while n.state in visited:
            n = open.pop()
        visited.add(n.state)
        if problem.isGoalState(n.state):
            return n.backtrack()
        lista = n.expand(problem.getSuccessors(n.state))
        for m in lista:
            if m.state not in visited:
                open.push(m)
    return util.raiseSolutionNotFound()

def uniformCostSearch(problem):
    """Search the node of least total cost first."""
    open = util.PriorityQueue()
    visited = set()
    initialNode = SearchNode (problem.getStartState())
    open.push(initialNode, initialNode.cost)
    while not open.isEmpty():
        n = open.pop()
        while n.state in visited:
            n = open.pop()
        visited.add(n.state)
        if problem.isGoalState(n.state):
            return n.backtrack()
        lista = n.expand(problem.getSuccessors(n.state))
        for m in lista:
            if m.state not in visited:
                open.push(m, m.cost)
    return util.raiseSolutionNotFound()

def nullHeuristic(state, problem=None):
    """
    A heuristic function estimates the cost from the current state to the nearest
    goal in the provided SearchProblem.  This heuristic is trivial.
    """
    return 0

def aStarSearch(problem, heuristic=nullHeuristic):
    """Search the node that has the lowest combined cost and heuristic first."""
    "*** YOUR CODE HERE ***"
    open = util.PriorityQueue()
    closed = list()
    initialNode = SearchNode (problem.getStartState())
    open.push(initialNode, initialNode.cost)
    while not open.isEmpty():
        repeat = 1
        n = open.pop()
        while repeat:
            repeat = 0
            for m_temp in closed:
                if m_temp.state == n.state:
                    if m_temp.cost <= n.cost:
                        repeat = 1
                        n = open.pop()

        if problem.isGoalState(n.state):
            return n.backtrack()
        closed.append(n)
        lista = n.expand(problem.getSuccessors(n.state))
        for m in lista:
            skip = 0
            for m_temp in closed:
                if m_temp.state == m.state:
                    if m_temp.cost < m.cost:
                        skip = 1
                        break
            if not skip:
                for m_temp in open.heap:
                    if m_temp[2].state == m.state:
                        if m_temp[2].cost < m.cost:
                            skip = 1
                            break
            if not skip:
                parent_f = m.parent.cost + heuristic(m.parent.state, problem)
                f = max(parent_f, m.cost + heuristic(m.state, problem))
                open.push(m, f)
    return util.raiseSolutionNotFound()


# Abbreviations
bfs = breadthFirstSearch
dfs = depthFirstSearch
astar = aStarSearch
ucs = uniformCostSearch
