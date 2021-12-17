from Utils import possible_states, possible_traps_to_throw
import numpy as np
import random
import time
import sys
import os 
from BaseAI import BaseAI
from Grid import Grid
from Utils import *

class StateInfo:
    def __init__(self, state, move, score=None, player=None):
            self.state = state
            self.move = move
            self.score = score
            self.player = player

    def setDepth(self, depth):
            self.depth = depth

    def compare(self, comparing_to, maximize):
            return

    def opposing_player(self):
            return 3 - self.player

    def getOpposingMoves(self):
            x = self.state.get_neighbors(self.state.find(self.opposing_player()), True)
            return [r for r in x if r != self.state.find(self.player) and r != self.state.find(self.opposing_player())]

    def getNumNeighborsMoves(self):
            return len(self.getOpposingMoves())

    def getNumMoves(self):
            return self.state.get_neighbors(self.state.find(self.player()), True)

    # This is the 'score' heuristic
    # probably can be improved
    def get_score(self, player, opponent):
            if self.score == None:
                    possible_moves = 0
                    opp_moves = 0

                    for val in self.state.get_neighbors(self.state.find(player), True):
                            possible_moves += len(self.state.get_neighbors(val, True))

                    for val in self.state.get_neighbors(self.state.find(opponent), True):
                            opp_moves += len(self.state.get_neighbors(val, True))
                    # opp_moves *
                    c = manhattan_distance(self.state.find(player), self.state.find(3-player))
                    
                    # input(str(self.state.find(2), str(self.state)))
                    # input(self.state.find(1))
                    self.score = opp_moves - possible_moves - c
            return self.score

def heuristics(state, player, opponent):
        return random.randint(1, 100)

def manhattan_distance(position, target):
        return np.abs(target[0] - position[0]) + np.abs(target[1] - position[1])

# Gets all states that a current player could change the board to
def possible_states(state, player):
        # player is either player 1 or 2
        # state is the grid
        state = state.state
        allStates = []
        #input(player)
        my_x, my_y = state.find(player)
        # all neighbords
        #input(my_x)
        #input(my_y)
        for x, y in state.get_neighbors((my_x, my_y), True):
                cloned_state = state.clone()
                # set to 0
                cloned_state.setCellValue((my_x, my_y), 0)
                # set to the id of the player
                cloned_state.setCellValue((x, y), player)
                allStates.append(StateInfo(cloned_state, move=(x, y), player=player))
        return allStates



def possible_traps_to_throw(state, player):
        # player is either player 1 or 2
        # state is the grid
        state = state.state
        allStates = []
        #input(player)
        opponent = 3-player
        # my_x, my_y = state.find(player)
        op_x, op_y = state.find(opponent)
        # all neighbords
        #input(my_x)
        #input(my_y)
        for x, y in state.get_neighbors((op_x, op_y), True):
                cloned_state = state.clone()
                # set to 0
                # cloned_state.setCellValue((op_x, op_y), 0)
                # set to the id of the player
                cloned_state.setCellValue((x, y), player)
                allStates.append(StateInfo(cloned_state, move=(x, y), player=player))
        return allStates

class PlayerAI(BaseAI):
    # Notes from OH:
    # Can either be player 1 or player 2
    # The space you're at should not be assigned somewhere
    # Position wise and number wise
    # EasyAi
    # 3 - you_number is the opponents number
    # Test player as both player 1 and player 2
    # Accuracy deterirates with distance
    # 

    # Make a move -- how would the opponent respond? probably trap
    # Look around opponent, how would they respond? 
    # Minimax, Alpha beta pruning, depth limit
    # 

    # State -> the current 2 players positions on the board
    # The current location of the unavailable spots on the board
    # 
    # When do you stop? When is a terminal state reached?
    #   This is stopped when the opposing player has no moves
    #   
    # Calculate the state for each player
    # a state may be good for one player and 
    # Sort your branches in some order before pruning
    # Sort the array in descending order
    # Maximum depth of the game is 46 bc Average is 5 ^ 46
    # 2 utility functions for move & trap
    # You can throw a trap on another trap
    # How far are you in the game?
    # 
    # You should be more aggresive if the
    # Number of moves you have is lower
    # and the inverse also being true

    def heuristic(self, state):
        if type(state) != StateInfo:
            state = StateInfo(state, None, player=self.player_num)
        # input(state.state)
        x = state.get_score(self.player_num, 3-self.player_num)
        # print(state.get_score(self.player_num, 3-self.player_num))
        self.states.append([x, state])
        return x

    def trap_heuristic(self, state, player):
        a = len(state.get_neighbors(state.find(player), True))
        b = len(state.get_neighbors(state.find(3 - player), True))
        return -1 * (a-b)

    def maximize_trap(self, state, depth, initial_position, alpha, beta):
        if depth == self.max_depth - 1:
            #input(depth)
            # print("END EARLY")
            return None, self.trap_heuristic(state, 3-self.player_num)

        if type(state) != StateInfo:
            state = StateInfo(state, None, player=self.player_num)

        maximum_child_node = None
        # Start at infinity
        max_cost = float("-inf")

        neighbors = state.getOpposingMoves()

        for position in neighbors:
            state_if_traped = state.state.clone()
            state_if_traped.trap(position)
            new_state, cost = self.minimize_trap(state_if_traped, depth+1, position, alpha, beta)
            if cost > max_cost:
                # print(new_state)
                # input("UPDATE MAX COST")
                maximum_child_node = position
                max_cost = cost
            if cost >= beta:
                # print("END EARLY")
                break
            if cost > alpha:
                alpha = max_cost
        return maximum_child_node, max_cost

    def minimize_trap(self, state, depth, initial_position, alpha, beta):
        # print("MIN")

        if type(state) != StateInfo:
            state = StateInfo(state, None, player=self.player_num)

        minimum_child_node = None
        # Start at infinity
        minimum_cost = float("inf")

        neighbors = state.state.get_neighbors(initial_position, True)

        for position in neighbors:
            state_if_moved = state.state.clone()
            state_if_moved.move(position, 3-self.player_num)
            new_state, cost = self.maximize_trap(state_if_moved, depth+1, position, alpha, beta)
            if cost < minimum_cost:
                minimum_child_node = position
                minimum_cost = cost
            if cost <= alpha:
                break
            if cost < beta:
                beta = minimum_cost
        return minimum_child_node, minimum_cost    
        
    def maximize_move(self, state, depth, initial_position, alpha, beta):
        # print("MAX")
        if depth == self.max_depth - 1:
            #input(depth)
            # print("END EARLY")
            return None, self.heuristic(state)

        if type(state) != StateInfo:
            state = StateInfo(state, None, player=self.player_num)

        maximum_child_node = None
        # Start at infinity
        max_cost = float("-inf")

        neighbors = state.state.get_neighbors(initial_position, True)
        if len(neighbors) == 0:
            # print("TRAPPED")
            return None, self.heuristic(state.state)

        for position in neighbors:
            state_if_moved = state.state.clone()
            state_if_moved.move(position, self.player_num)
            new_state, cost = self.minimize_move(state_if_moved, depth+1, position, alpha, beta)
            if cost > max_cost:
                # print(new_state)
                # input("UPDATE MAX COST")
                maximum_child_node = position
                max_cost = cost
            if cost >= beta:
                # print("END EARLY")
                break
            if cost > alpha:
                alpha = max_cost
            #input(cost)
            #input(maximum_child_node)
        return maximum_child_node, max_cost

    def minimize_move(self, state, depth, initial_position, alpha, beta):
        # print("MIN")
        if depth == self.max_depth - 1:
            return None, 1

        if type(state) != StateInfo:
            state = StateInfo(state, None, player=self.player_num)

        minimum_child_node = None
        # Start at infinity
        minimum_cost = float("inf")

        neighbors = state.state.getAvailableCells()
        neighbors = state.getOpposingMoves()

        for position in neighbors:
            state_if_moved = state.state.clone()
            state_if_moved.move(position, self.player_num)
            new_state, cost = self.maximize_move(state_if_moved, depth+1, position, alpha, beta)
            if cost < minimum_cost:
                minimum_child_node = position
                minimum_cost = cost
            if cost <= alpha:
                break
            if cost < beta:
                beta = minimum_cost
        return minimum_child_node, minimum_cost

    # We want to maximize the number of moves and minimize the number of traps
    def minimax(self, state, depth=0, maximizing_player=True, alpha=None, beta=None, player=None):
        if player == None:
            player = self.player_num
        # This means the depth is too deep
        # In place of using the algo in the doc
        if depth == self.max_depth - 1:
            # Return early
            return state

        # This means it's not a StateInfo class
        if type(state) != StateInfo:
            state = StateInfo(state, None, player=player)


        # This is maximizing
        if maximizing_player == True:
            possible_state_values = possible_states(state, player)
            currentChild = StateInfo(state, None, player=player, score=float("-inf"))
            if alpha == None and beta == None:
                alpha = float("-inf")
                beta = float("inf")

        else:
            possible_state_values = possible_traps_to_throw(state, player)
            currentChild = StateInfo(state, None, player=player, score=float("inf"))
            if alpha == None and beta == None:
                alpha = float("inf")
                beta = float("-inf")

        for new_state in possible_state_values:
            temp_child = self.minimax(state, depth+1, not maximizing_player, alpha, beta, 3 - player)

            if maximizing_player == True:
                if temp_child.get_score(player, 3-player) > currentChild.get_score(player, 3-player):
                    currentChild = new_state
                if temp_child.get_score(player, 3-player) >= beta:
                    break
                if currentChild.get_score(player, 3-player) > alpha:
                    alpha = currentChild.get_score(player, 3-player)
            else:
                if temp_child.get_score(player, 3-player) < currentChild.get_score(player, 3-player):
                    currentChild = new_state
                if temp_child.get_score(player, 3-player) <= alpha:
                    break
                if currentChild.get_score(player, 3-player) < beta:
                    beta = currentChild.get_score(player, 3-player)
        
        return currentChild



    def __init__(self) -> None:
        # You may choose to add attributes to your player - up to you!
        super().__init__()
        self.pos = None
        self.player_num = None
        self.max_depth = 5
        self.best_trap = None
        self.best_trap_size = float("inf")
        self.states = []
        self.lowest_state_num = float("inf")

        self.recent_move = None
    
    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position 

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        self.states = []
        self.lowest_state_num = float("inf")
        if self.pos == None:
            self.pos = grid.find(1)
        else:
            print(self.pos)
        # print(self.pos)
        r = self.maximize_move(grid, 0, self.pos, float("-inf"), float("inf"))[0]
        return r
        self.states.sort(key=lambda k: k[0])
        minVal = self.states[0][0]
        e = random.choice([r for r in self.states if r[0] == minVal])[1]
        print(e)

        input(self.states)
        input(e)
        # input("{} -> {}".format(str(self.pos), str(r)))
        return r

    def trapMiniMax(self, state, depth=0, maximizing_player=False, alpha=None, beta=None, player=None, move=None):
        if player == None:
            player = self.player_num
        
        # This is maximizing
        if maximizing_player == True:
            if alpha == None and beta == None:
                alpha = float("-inf")
                beta = float("inf")
        else:
            if alpha == None and beta == None:
                alpha = float("inf")
                beta = float("-inf")

        # This means it's not a StateInfo class
        if type(state) != StateInfo:
            state = StateInfo(state, None, player=player)

        possible_traps = [x for x in state.getOpposingMoves() if x != self.recent_move and x != None]
        #input(self.recent_move)
        #input(possible_traps)
        
        if not maximizing_player:
            #print("MOVING TO {}".format(move))
            if len([x for x in possible_traps]) < self.best_trap_size:
                self.best_trap = move
                self.best_trap_size = len([x for x in possible_traps])
            #print([x for x in possible_traps])
            #input("")

        #input(len(possible_traps))
        # This means the depth is too deep
        # In place of using the algo in the doc
        if depth == self.max_depth - 1 or len(possible_traps) == 0:
            # Return early
            return state

        # Maximum
        if maximizing_player == True:
            next_move, max_cost = None, float("-inf")
            for trap in possible_traps:
                child_state = state.state.clone()
                child_state.trap(trap)
                new_state = self.trapMiniMax(child_state, depth+1, not maximizing_player, alpha, beta, move=trap)
                cost = new_state.getNumNeighborsMoves()
                if cost > max_cost:
                    next_move = new_state
                    max_cost = cost
                if max_cost >= beta:
                    break
                if max_cost > alpha:
                    alpha = max_cost
            min_cost = max_cost
        # Minimizing
        else:
            next_move, min_cost = None, float('inf')
            for trap in possible_traps:
                child_state = state.state.clone()
                child_state.move(trap, 3-self.player_num)
                new_state = self.trapMiniMax(child_state, depth+1, not maximizing_player, alpha, beta, move=trap)
                cost = new_state.getNumNeighborsMoves()
                if cost < min_cost:
                    next_move = new_state
                    min_cost = cost
                if min_cost <= alpha:
                    break
                if min_cost < beta:
                    beta = min_cost
        return next_move

    def getTrap(self, grid : Grid) -> tuple:
        return self.maximize_trap(grid, 0, grid.find(3-self.player_num), float("-inf"), float("inf"))[0]
        

    