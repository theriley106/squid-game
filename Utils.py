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
                return self.state.get_neighbors(self.state.find(self.opposing_player()), True)

        def getNumNeighborsMoves(self):
                return self.getOpposingMoves()

        def getNumMoves(self):
                return self.state.get_neighbors(self.state.find(self.player()), True)

        # This is the 'score' heuristic
        # probably can be improved
        def get_score(self, player, opponent):
                if self.score == None:
                        possible_moves = 0

                        for val in self.state.get_neighbors(self.state.find(player), True):
                                possible_moves += len(self.state.get_neighbors(val, True))

                        for val in self.state.get_neighbors(self.state.find(opponent), True):
                                possible_moves -= len(self.state.get_neighbors(val, True))

                        self.score = possible_moves
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


