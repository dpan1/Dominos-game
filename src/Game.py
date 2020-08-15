from Board import Board
from Constants import Constants
from Player import Player
from GameState import GameState
import random


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
        pass

    def player(self):
        pass

    def scores(self):
        # TODO return scores that line up with players.
        pass

    def treestrap(self, hand_surf):
        current_player = self.starting_player
        root = dict()

        if current_player == 0:
            plays = hand_surf.playable(self.board)
            for dom_tup, direction, reward in plays:
                root[dom_tup] = GameState(dom_tup, direction, reward, 0, self.hands.copy())
        else:
            plays = self.players[current_player].playable()
            for dom_tup, direction, reward in plays:
                root[dom_tup] = GameState(dom_tup, direction, reward, 0, self.hands.copy())
        current_player = (current_player + 1) % 4
        for dom_tup in root.keys():
            self.trecurse(root[dom_tup])
        pass

    def trecurse(self, parent_state):
        pass

    def take_score(self, player_id: int, board: Board):
        if board.sum_outsides() % 5 == 0:
            self.scores[player_id] += board.sum_outsides()
        pass

    def automate(self, dominoes):
        self.current_player = next(self.player)
        while self.current_player != 0:
            self.players[self.current_player].make_play(dominoes)
            self.current_player = next(self.player)
        # take player action
        pass

    def deal(self):
        random.shuffle(self.domino_list)
        self.hands = [[self.domino_list[j * 4 + i] for j in range(7)] for i in range(4)]
        pass

    def record_play(self, domino_tuple, direction, player):
        self.information_sheet.append((domino_tuple, direction, player))
