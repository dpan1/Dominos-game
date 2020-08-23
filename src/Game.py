from Board import Board
from Constants import Constants
from GameState import GameState
from Player import Player
import copy
import random
# Magic Numbers in use:
# 4: number of players
# 5: basic unit of dominos, also, nickel for knocking
# 7: number of dominos to deal to a player/size of list for a player's hands. also 28/4
# 10: minimum scoring point value for dominos


class Game(object):
    def __init__(self, board, settings, starting_player=0):
        self.settings = settings
        self.domino_list = list(Constants.FULL_SET)
        self.information_sheet = list()
        self.hands = [[] for _ in range(4)]
        self.scores = [0 for _ in range(4)]
        self.starting_player = starting_player
        self.board = board
        self.players = [Player(i, board, Constants.RANDOM_PLAYABLE, self) if i > 0 else None for i in range(4)]
        self.state = 0
        self.iter = 0
        self.root = None
        self.node_ht = dict()  # emphasis on using the hash
        pass

    def set_hand(self, handsurf):  # as mentioned in the code that calls this
        self.players[0] = handsurf

    def scores(self):
        # TODO return scores that line up with players.
        pass

    def recur(self, parent_state, player, depth):
        if depth < 1:
            return
        if len(parent_state.playable(player)) == 0:  # we can add 5 points to the game state by adding score=5 here
            parent_state.children['knock'] = GameState(
                copy.deepcopy(parent_state.ats), turn=(parent_state.ats['TURN'] + 1) % 4,
                score=5 if self.settings.nickel_for_knocking else 0
            )
            self.recur(parent_state.children['knock'], (player + 1) % 4, depth - 1)
        else:
            for play in parent_state.playable(player):
                parent_state.children[play] = GameState(copy.deepcopy(parent_state.ats),
                                                        dom_tup=play[0], direction=play[1])
                self.recur(parent_state.children[play], (player + 1) % 4, depth - 1)
        pass

    def automate(self, dominoes):
        self.root = self.dump()
        self.recur(self.root, 1, 7)
        pass

    def deal(self):
        random.shuffle(self.domino_list)
        self.hands = [[self.domino_list[j * 4 + i] for j in range(7)] for i in range(4)]

    def record_play(self, domino_tuple, direction, player):
        self.information_sheet.append((domino_tuple, direction, player))

    def dump(self):
        # ats is just short for attributes
        ats = {
            'STATE': self.board.state,
            'SPINNER': self.board.spinner,
            'S_LEFT': self.board.branches['starter'].domino_list[0] if
            'starter' in self.board.branches.keys() else None,
            'S_RIGHT': self.board.branches['starter'].domino_list[-1] if
            'starter' in self.board.branches.keys() else None,
            Constants.UP: self._dump_branch(Constants.UP),
            Constants.RIGHT: self._dump_branch(Constants.RIGHT),
            Constants.LEFT: self._dump_branch(Constants.LEFT),
            Constants.DOWN: self._dump_branch(Constants.DOWN),
            'HANDS': [copy.deepcopy(player.hand) for player in self.players],
            'TURN': 0,
            'SCORES': [0 for _ in range(4)]
        }
        return GameState(state=ats)

    def _dump_branch(self, branch_name):
        if self.board.branches[branch_name] is not None:
            if len(self.board.branches[branch_name].domino_list) > 0:
                return self.board.branches[branch_name].domino_list[-1]
            else:
                return None
        else:
            return None
