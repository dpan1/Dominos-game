from src.Board import Board
from src.Constants import Constants
from src.Player import Player
import random


def player_no(starting_no):
    number = starting_no
    while True:
        yield number
        number = (number + 1) % 4


class Game(object):
    def __init__(self, board, starting_player=0):
        self.current_player = starting_player
        self.domino_list = list(Constants.FULL_SET)
        self.hands = [[] for _ in range(4)]
        self.scores = [0 for _ in range(4)]
        self.players = [Player(i, board) if i > 0 else None for i in range(4)]
        self.state = 0
        pass

    def scores(self):
        # TODO return scores that line up with players.
        pass

    def take_score(self, player: Player, board: Board):
        # Read board state, if sum
        pass

    def automate(self, player: Player):
        # take player action
        pass

    def deal(self):
        random.shuffle(self.domino_list)
        self.hands = [[self.domino_list[j * 4 + i] for j in range(7)] for i in range(4)]
        pass
