
"""
In search.py, you will implement generic search algorithms which are called by
Pacman agents (in searchAgents.py).
"""

import util
from logic import * 

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


def miniWumpusSearch(problem): 
    """
    A sample pass through the miniWumpus layout. Your solution will not contain 
    just three steps! Optimality is not the concern here.
    """
    from game import Directions
    e = Directions.EAST 
    n = Directions.NORTH
    return  [e, n, n]

def logicBasedSearch(problem):
    """

    To get started, you might want to try some of these simple commands to
    understand the search problem that is being passed in:

    print "Start:", problem.getStartState()
    print "Is the start a goal?", problem.isGoalState(problem.getStartState())
    print "Start's successors:", problem.getSuccessors(problem.getStartState())

    print "Does the Wumpus's stench reach my spot?", 
               \ problem.isWumpusClose(problem.getStartState())

    print "Can I sense the chemicals from the pills?", 
               \ problem.isPoisonCapsuleClose(problem.getStartState())

    print "Can I see the glow from the teleporter?", 
               \ problem.isTeleporterClose(problem.getStartState())
    
    (the slash '\\' is used to combine commands spanning through multiple lines - 
    you should remove it if you convert the commands to a single line)
    
    Feel free to create and use as many helper functions as you want.

    A couple of hints: 
        * Use the getSuccessors method, not only when you are looking for states 
        you can transition into. In case you want to resolve if a poisoned pill is 
        at a certain state, it might be easy to check if you can sense the chemicals 
        on all cells surrounding the state. 
        * Memorize information, often and thoroughly. Dictionaries are your friends and 
        states (tuples) can be used as keys.
        * Keep track of the states you visit in order. You do NOT need to remember the
        tranisitions - simply pass the visited states to the 'reconstructPath' method 
        in the search problem. Check logicAgents.py and search.py for implementation.
    """
    # array in order to keep the ordering
    visitedStates = []
    gameMap = dict()
    safeStates = util.PriorityQueueWithFunction(stateWeight)
    unknownStates = util.PriorityQueueWithFunction(stateWeight)
    propDict = {"safe":0, "poison":0, "wumpus":0, "teleporter":0}

    startState = problem.getStartState()
    currentState = startState
    visitedStates.append(currentState)
    gameMap[currentState] = propDict.copy()
    gameMap[currentState]["safe"] = 1
    
    while not problem.isTeleporter(currentState):
        premise_s = Clause(Literal('s', currentState, not problem.isWumpusClose(currentState)))
        premise_b = Clause(Literal('b', currentState, not problem.isPoisonCapsuleClose(currentState)))
        premise_g = Clause(Literal('g', currentState, not problem.isTeleporterClose(currentState)))

        for state_total in problem.getSuccessors(currentState):
            state = state_total[0]
            if state not in visitedStates:
                if state not in gameMap.keys():
                    gameMap[state] = propDict.copy()

                goal_t = Clause(Literal('t', state, True))
                _teleporter = resolution(set([premise_g, premise_t(currentState, state)]), goal_t)
                if _teleporter:
                    gameMap[state]["teleporter"] = -1
                goal_w = Clause(Literal('w', state, True))
                _wumpus = resolution(set([premise_s, premise_w(currentState, state)]), goal_w)
                if _wumpus:
                    gameMap[state]["wumpus"] = -1
                goal_p = Clause(Literal('p', state, True))
                _poison = resolution(set([premise_b, premise_p(currentState, state)]), goal_p)
                if _poison:
                    gameMap[state]["poison"] = -1

                poison = poisonFinder(problem, premise_b, currentState, state, gameMap)
                if poison:
                    gameMap[state]["poison"] = 1
                wumpus = wumpusFinder(problem, premise_s, currentState, state, gameMap)
                if wumpus:
                    gameMap[state]["wumpus"] = 1
                    wumpusFound = True
                teleport = teleportFinder(problem, premise_g, currentState, state, gameMap)
                if teleport:
                    gameMap[state]["teleport"] = 1
                    teleportFound = True
                    visitedStates.append(state)
                    return problem.reconstructPath(visitedStates)

                if _wumpus and _poison:
                    gameMap[state]["safe"] = 1
                    safeStates.push(state)
                elif gameMap[state]["wumpus"] == -1 and gameMap[state]["poison"] == -1:
                    gameMap[state]["safe"] = 1
                    safeStates.push(state)
                elif gameMap[state]["poison"] != 1 and gameMap[state]["wumpus"] != 1:
                    unknownStates.push( (state, currentState) )

        repeat = False
        while currentState in visitedStates:
            if len(safeStates.heap) > 0:
                currentState = safeStates.pop()
            else:
                while currentState in visitedStates or repeat:
                    if len(unknownStates.heap) > 0:
                        fullState = unknownStates.pop()
                        currentState = fullState[0]
                        lastState = fullState[1]
                        premise_s = Clause(Literal('s', lastState, not problem.isWumpusClose(lastState)))
                        premise_b = Clause(Literal('b', lastState, not problem.isPoisonCapsuleClose(lastState)))
                        poison = poisonFinder(problem, premise_b, lastState, currentState, gameMap)
                        wumpus = wumpusFinder(problem, premise_s, lastState, currentState, gameMap)
                        if poison or wumpus:
                            repeat = True
                    else:
                        return problem.reconstructPath(visitedStates)

        visitedStates.append(currentState)
    
    return problem.reconstructPath(visitedStates)


def positionIndex (state):
    return 20*state[0] + state[1]

    #s - stench      w - wumpus
    #b - breeze      p - poison pill
    #g - glow        t - teleporter
def premise_w (centerState, otherState): # Pacard doesn't smell stench -> no Wumpus around
    return Clause(set([Literal('s', centerState), Literal('w', otherState, True)]))

def premise_p (centerState, otherState): # Pacard doesn't smell chemicals -> no pills around
    return Clause(set([Literal('b', centerState), Literal('p', otherState, True)]))

def premise_t (centerState, otherState): # Pacard doesn't see glow -> no telepoter around
    return Clause(set([Literal('g', centerState), Literal('t', otherState, True)]))

def poisonFinder(problem, premise, centerState, otherState, gameMap):
    goal = Clause(Literal('p', otherState))
    ruleLiterals = set([Literal('b', centerState, True), Literal('p', otherState)])
    premises = set([premise])

    for state_total in problem.getSuccessors(centerState):
        state = state_total[0]
        if state != otherState:
            ruleLiterals.add(Literal('o', state, True))
            subGameMap = gameMap.get(state, {"safe":0, "poison":0, "wumpus":0, "teleporter":0})
            isSafe = (subGameMap["safe"] == 1)
            premise = Clause(Literal('o', state, not isSafe))
            premises.add(premise)
    rule = Clause(ruleLiterals)
    premises.add(rule)
    return resolution(premises, goal)

def wumpusFinder(problem, premise, centerState, otherState, gameMap):
    goal = Clause(Literal('w', otherState))
    ruleLiterals = set([Literal('s', centerState, True), Literal('w', otherState)])
    premises = set([premise])

    for state_total in problem.getSuccessors(centerState):
        state = state_total[0]
        if state != otherState:
            ruleLiterals.add(Literal('o', state, True))
            subGameMap = gameMap.get(state, {"safe":0, "poison":0, "wumpus":0, "teleporter":0})
            isSafe = (subGameMap["safe"] == 1)
            premise = Clause(Literal('o', state, not isSafe))
            premises.add(premise)
    rule = Clause(ruleLiterals)
    premises.add(rule)
    return resolution(premises, goal)

def teleportFinder(problem, premise, centerState, otherState, gameMap):
    goal = Clause(Literal('t', otherState))
    ruleLiterals = set([Literal('g', centerState, True), Literal('t', otherState)])
    premises = set([premise])

    for state_total in problem.getSuccessors(centerState):
        state = state_total[0]
        if state != otherState:
            ruleLiterals.add(Literal('o', state, True))
            subGameMap = gameMap.get(state, {"safe":0, "poison":0, "wumpus":0, "teleporter":0})
            isSafe = (subGameMap["safe"] == 1)
            premise = Clause(Literal('o', state, not isSafe))
            premises.add(premise)
    rule = Clause(ruleLiterals)
    premises.add(rule)
    return resolution(premises, goal)
    


# Abbreviations
lbs = logicBasedSearch
