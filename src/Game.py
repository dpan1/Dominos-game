from Constants import Constants
from GameState import GameState
from Player import Player
import copy
import random
# Magic Numbers in use:
# 4: number of players
# 5: basic unit of dominoes, also, nickel for knocking
# 7: number of dominoes to deal to a player/size of list for a player's hands. also 28/4
# 10: minimum scoring point value for dominoes


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

    def set_hand(self, hand_surf):  # as mentioned in the code that calls this
        self.players[0] = hand_surf

    def scores(self):
        # TODO return scores that line up with players.
        pass

    def recur(self, parent_state, player, depth):
        if depth < 1:
            return
        if len(parent_state.playable(player, self.hands)) == 0:  # we can add 5 points to the game state by adding score=5 here
            parent_state.children['knock'] = GameState(self.hands,
                state=copy.copy(parent_state.ats),
                turn=(parent_state.ats['TURN'] + 1) % 4,
                score=5 if self.settings.nickel_for_knocking else 0
            )
            self.recur(parent_state.children['knock'], (player + 1) % 4, depth - 1)
        else:
            for play in parent_state.playable(player, self.hands):
                parent_state.children[play] = GameState(self.hands, state=copy.copy(parent_state.ats),
                                                        dom_tup=play[0], direction=play[1])
                self.recur(parent_state.children[play], (player + 1) % 4, depth - 1)
        pass

    def automate(self):
        self.root = self.dump()
        for play in self.root.playable(0, self.hands):
            self.root.children[play[0]] = GameState(self.hands, state=copy.deepcopy(self.root.ats), dom_tup=play[0], direction=play[1])
        for key in self.root.children.keys():
            self.recur(self.root.children[key], 1, 27)
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
            'HANDS': [255 for j in range(4)],  # I think it's slow because of this.
            'TURN': 0,
            'SCORES': [0 for _ in range(4)]
        }
        return GameState(self.hands, state=ats)

    def _dump_branch(self, branch_name):
        if self.board.branches[branch_name] is not None:
            if len(self.board.branches[branch_name].domino_list) > 0:
                return self.board.branches[branch_name].domino_list[-1]
            else:
                return None
        else:
            return None
