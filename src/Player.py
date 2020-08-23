import random
import time
from Constants import Constants


class Player(object):
    def __init__(self, player_id, board, profile, game):
        random.seed(time.time())
        self.hand = None
        self.player_id = player_id
        self.board = board
        self.game = game
        self.play_fun = {
            Constants.RANDOM_PLAYABLE: Player.random_picker,
            Constants.AMIGM_THEN_RANDOM: Player.all_money_is_good_money_picker,
        }[profile]
        pass

    def make_play(self, dominoes):
        plays = self.playable()
        choice = self.play_fun(plays)
        self.play_domino(choice[0], choice[1], dominoes)

    def detective(self, playable):
        info = self.game.information_sheet

    def set_hand(self, hand):
        self.hand = hand

    def play_domino(self, held, direction, dominoes):
        if self.board.state == 0:
            self.board.play(held)
            self.hand.remove(held)
        if self.board.state == 1:
            if self.board.branches['starter'].is_valid_play(held, direction):
                self.board.branches['starter'].play_plain(held, direction=direction)
                self.hand.remove(held)
        else:   # we're in some other state
            if self.board.branches[direction].get_end_value == held[0] or \
                    self.board.branches[direction].get_end_value == held[1]:
                self.board.branches[direction].play_plain(held)
                dominoes[held].draggable = False
                self.hand.remove(held)

    @staticmethod
    def random_picker(playable):
        return random.choice(playable)

    @staticmethod
    def all_money_is_good_money_picker(playable):
        local_max = max(map(lambda y: y[2], playable))
        # max_list = list(filter(lambda x: x[2] == local_max, playable))
        if local_max == 0:
            return random.choice(playable)
        elif local_max > 0:
            return random.choice(list(filter(lambda x: x[2] == local_max, playable)))
        else:
            return None

    def right_check(self, dom_tup):
        return self.board.branches['starter'].domino_list[-1][0][
                   0 if self.board.branches['starter'].domino_list[-1][0] == 0 else 1] == dom_tup[0] or \
               self.board.branches['starter'].domino_list[-1][0][
                   0 if self.board.branches['starter'].domino_list[-1][0] == 0 else 1] == dom_tup[1]

    def left_check(self, dom_tup):
        return self.board.branches['starter'].domino_list[0][0][
                   1 if self.board.branches['starter'].domino_list[0][1] == 1 else 0] == dom_tup[0] or \
               self.board.branches['starter'].domino_list[0][0][
                   1 if self.board.branches['starter'].domino_list[0][1] == 0 else 0] == dom_tup[1]

    def playable(self):  # TODO needs to calculate rewards for potential plays
        if self.board.state == 0:
            return [(hand_item, 0) for hand_item in self.hand]
        elif self.board.state == 1:
            playable = []
            for dom_tup in self.hand:
                if self.right_check(dom_tup):
                    playable.append((dom_tup, Constants.RIGHT))
                if self.left_check(dom_tup):
                    playable.append((dom_tup, Constants.LEFT))
            return playable
        elif self.board.state == 2:
            playable = []
            for direction in [Constants.LEFT, Constants.RIGHT]:
                for dom_tup in self.hand:
                    if self.board.branches[direction].outside_val == dom_tup[0] or \
                            self.board.branches[direction].outside_val == dom_tup[1]:
                        playable.append((dom_tup, direction))
            return playable
        elif self.board.state == 3:
            playable = []
            for direction in Constants.ORIENTATIONS:
                for dom_tup in self.hand:
                    if self.board.branches[direction].outside_val == dom_tup[0] or \
                            self.board.branches[direction].outside_val == dom_tup[1]:
                        playable.append((dom_tup, direction))
            return playable
