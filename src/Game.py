from Board import Board
from Constants import Constants
from GameState import GameState
from Player import Player
import copy
import random
# Magic Numbers in use:
# 4: number of players
# 5: basic unit of dominos
# 7: number of dominos to deal to a player/size of list for a player's hands. also 28/4
# 10: minimum scoring point value for dominos


def player_no(starting_no):
    number = starting_no
    while True:
        yield number
        number = (number + 1) % 4


class Game(object):
    def __init__(self, board, starting_player=0):
        self.player = player_no(starting_player)
        self.current_player = next(self.player)
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
        self.node_ht = dict()  #emphasis on using the hash
        pass

    def player(self):
        pass

    def scores(self):
        # TODO return scores that line up with players.
        pass

    def treestrap(self, hand_surf):
        current_player = self.starting_player
        root = dict()

    def trecurse(self, hand, parent_state, depth):
        pass

    def take_score(self, player_id: int, board: Board):
        if board.sum_outsides() % 5 == 0 and board.sum_outsides() >= 10:
            self.scores[player_id] += board.sum_outsides()

    def automate(self, dominoes):
        self.current_player = next(self.player)
        while self.current_player != 0:
            self.root = self.dump()

            for play in self.players[self.current_player].playable():
                self.root.children[play[0]] = GameState()

        # take player action

    def deal(self):
        random.shuffle(self.domino_list)
        self.hands = [[self.domino_list[j * 4 + i] for j in range(7)] for i in range(4)]

    def record_play(self, domino_tuple, direction, player):
        self.information_sheet.append((domino_tuple, direction, player))

    def dump(self):
        ats = {
            'STATE': self.board.state,
            'SPINNER': self.board.spinner,
            'STARTER': copy.deepcopy(self.board.branches['starter'].domino_list),
            'UP': copy.deepcopy(self.board.branches[Constants.UP].domino_list),
            'RIGHT': copy.deepcopy(self.board.branches[Constants.RIGHT].domino_list),
            'LEFT': copy.deepcopy(self.board.branches[Constants.LEFT].domino_list),
            'DOWN': copy.deepcopy(self.board.branches[Constants.DOWN].domino_list),
            'HANDS': copy.deepcopy(self.hands),
            'TURN': self.current_player
        }
        return GameState(state=ats)
