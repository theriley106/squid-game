from Utils import possible_states
import numpy as np
import random
import time
import sys
import os 
from BaseAI import BaseAI
from Grid import Grid
from Utils import *

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
            currentChild = StateInfo(state, None, player=player, score=float("-inf"))
            if alpha == None and beta == None:
                alpha = float("-inf")
                beta = float("inf")

        else:
            currentChild = StateInfo(state, None, player=player, score=float("inf"))
            if alpha == None and beta == None:
                alpha = float("inf")
                beta = float("-inf")

        for new_state in possible_states(state, player):
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
    
    def getPosition(self):
        return self.pos

    def setPosition(self, new_position):
        self.pos = new_position 

    def getPlayerNum(self):
        return self.player_num

    def setPlayerNum(self, num):
        self.player_num = num

    def getMove(self, grid: Grid) -> tuple:
        return self.minimax(grid).move

    def trapMiniMax(self, state, depth=0, maximizing_player=True, alpha=None, beta=None, player=None):
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

        possible_traps = state.getOpposingMoves()


        # This means the depth is too deep
        # In place of using the algo in the doc
        if depth == self.max_depth - 1 or len(possible_traps) == 0:
            # Return early
            return state, 0

        # Maximum
        if maximizing_player == True:
            next_move, max_cost = None, float("-inf")
            for trap in possible_traps:
                child_state = state.state.clone()
                child_state.trap(trap)
                _, cost = self.trapMiniMax(child_state, depth+1, not maximizing_player, alpha, beta)

                if cost > max_cost:
                    next_move = trap
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
                _, cost = self.trapMiniMax(child_state, depth+1, not maximizing_player, alpha, beta)
                if cost < min_cost:
                    next_move = child_state
                    min_cost = cost
                if min_cost <= alpha:
                    break
                if min_cost < beta:
                    beta = min_cost
        return next_move, min_cost

    def getTrap(self, grid : Grid) -> tuple:
        return self.trapMiniMax(grid)[0]
        

    