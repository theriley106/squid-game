import numpy as np
import random

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