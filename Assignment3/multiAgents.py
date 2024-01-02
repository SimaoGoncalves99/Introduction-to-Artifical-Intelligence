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

        "*** YOUR CODE HERE ***"
        return successorGameState.getScore()

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
    
    def max_value(self,gameState,depth):
        
        agent_index = 0; #Agent 0 is pacman so in order for him to start his turn, this variable is initialized to 0
        
        #Check if pacman has any remaining actions given the game state, if he hasn´t we call the evaluation function and the game ends
        # returning the current score
        if not gameState.getLegalActions(agent_index):
               return (self.evaluationFunction(gameState)), None
            
        #Check if the game is in a winning or losing situation, from the pacman point of view, also, check if we reached
        #the end of the search tree. If any of the conditions is verified, we return the score and the game is over
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState)), None
            
        v = float("-inf") #initialize the value of v to -infinity
        
        #We iterate through pacman´s legal actions and we choose the one that 
        #maximizes the score, in the end we return the maximum score found and the move pacman makes
        for i in gameState.getLegalActions(agent_index):
            
            #For each possible action for pacman we call the min_value function
            #which is responsible for the ghosts' actions in the game
               v2,a2 = self.min_value(gameState.generateSuccessor(agent_index,i),depth,1)
                
               if v2 > v:
                   v = v2
                   move = i
                   
        return v,move     
            
            
            
    def min_value(self,gameState,depth,agent_index):    
            

           #We do the same two if conditions we did for pacman,
           #but now for the ghosts
           
           if not gameState.getLegalActions(agent_index):
               return self.evaluationFunction(gameState), None
           
             
           if gameState.isWin() or gameState.isLose() or depth == self.depth:
               return (self.evaluationFunction(gameState)), None
            
           v = float("inf") #initialize value v to +infinity
             
           #Go through the legal actions of the given ghost and pick the action which minimizes the game score
           #In the end we return the best value that minimizes the score and the performed move 
           for i in gameState.getLegalActions(agent_index):
               
               #These two if conditions allow us to decide who is playing the next turn.
               #If in this game state the last ghost is playing, then pacman is playing up
               #next and we call the max function, increasing the depth. Otherwise, we call the min_value again 
               #and it´s the next ghost turn, meaning that the depth must not increase yet
               
               if agent_index == gameState.getNumAgents() - 1:
                   v2,a2 = self.max_value(gameState.generateSuccessor(agent_index,i),depth + 1)
               else: 
                   v2,a2 = self.min_value(gameState.generateSuccessor(agent_index,i),depth,agent_index + 1)
        
               if v2 < v:
                   v = v2
                   move = i
                    
           return v,move        

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
            
        depth = 0 #Initializes the depth with the value 0 
            
        v,move = self.max_value(gameState,depth) #Calls the max_value function, so that pacman can play first 
            
        return move 
    
            
        "*** YOUR CODE HERE ***"
        #util.raiseNotDefined()

class AlphaBetaAgent(MultiAgentSearchAgent):
    """
    Your minimax agent with alpha-beta pruning (question 3)
    """
    
    def min_value(self,gameState,depth,agent_index, alpha, beta):    
            
            
           #Check wether the given agent has any legal actions
           #if not gameState.getLegalActions(agent_index):
             #  return self.evaluationFunction(gameState), None
            
           if gameState.isWin() or gameState.isLose() or depth == self.depth:
               return (self.evaluationFunction(gameState)), None
            
           v = float("inf") #initialize value v to +infinity
           move = float("inf")
             
           #Go through the actions of the agent and pick the one with the least value
           for i in gameState.getLegalActions(agent_index):
               if agent_index == gameState.getNumAgents() - 1:
                   v2,a2 = self.max_value(gameState.generateSuccessor(agent_index,i),depth + 1, alpha, beta)
               else: 
                   v2,a2 = self.min_value(gameState.generateSuccessor(agent_index,i),depth,agent_index + 1, alpha, beta)
        
               if v2 < v:
                   v = v2
                   move = i
                   beta = min(v,beta)
               if v < alpha:
                   return v, move
           return v,move    
    
    def max_value(self,gameState,depth, alpha, beta):
        
        agent_index = 0;
            
       # if not gameState.getLegalActions(agent_index):
              # return (self.evaluationFunction(gameState)), None
            
        #Check if the game is finished
        if gameState.isWin() or gameState.isLose() or depth == self.depth:
            return (self.evaluationFunction(gameState)), None
            
        v = float("-inf") #initialize value v
        move = float("-inf")
        for i in gameState.getLegalActions(agent_index):
               v2,a2 = self.min_value(gameState.generateSuccessor(agent_index,i),depth, 1, alpha, beta)
                
               if v2 > v:
                   v = v2
                   move = i
                   alpha = max(v,alpha)
               if v > beta:
                   return v, move
                   
        return v,move
    def getAction(self, gameState):
        """
        Returns the minimax action using self.depth and self.evaluationFunction
        """
        "*** YOUR CODE HERE ***"
        depth = 0
        alpha = float("-inf")  
        beta = float("inf")
        v,move = self.max_value(gameState ,depth, alpha, beta)
            
        return move

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
        util.raiseNotDefined()

def betterEvaluationFunction(currentGameState):
    """
    Your extreme ghost-hunting, pellet-nabbing, food-gobbling, unstoppable
    evaluation function (question 5).

    DESCRIPTION: <write something here so we know what you did>
    """
    "*** YOUR CODE HERE ***"
    util.raiseNotDefined()

# Abbreviation
better = betterEvaluationFunction
