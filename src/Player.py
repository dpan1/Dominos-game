import random
import time
from Constants import Constants


class Player(object):
    def __init__(self, player_id, board, profile):
        random.seed(time.time())
        self.hand = None
        self.player_id = player_id
        self.board = board
        self.play_fun = {
            Constants.RANDOM_PLAYABLE: Player.random_picker,
            Constants.AMIGM_THEN_RANDOM: Player.all_money_is_good_money_picker,
        }[profile]
        pass

    def set_hand(self, hand):
        self.hand = hand

    def play_domino(self, held, direction, dominoes):
        if self.board.state == 0:
            self.board.play()
        if self.board.state == 1:
            if direction == Constants.RIGHT:
                if self.board.branches['starter'].domino_list[-1][1] == 0:
                    if self.board.branches['starter'].domino_list[-1][0][1] == held[0]:
                        if held[0] == held[1]:
                            self.board.transition(2, ztwo_branch=Constants.RIGHT, spinner=held)
                            dominoes[held].draggable = False
                            self.hand.remove(held)
                        else:
                            self.board.branches['starter'].play(held, 0)
                            dominoes[held].draggable = False
                            self.hand.remove(held)
                    elif self.board.branches['starter'].domino_list[-1][0][1] == held[1]:
                        self.board.branches['starter'].play(held, 2)
                        dominoes[held].draggable = False
                        self.hand.remove(held)
                elif self.board.branches['starter'].domino_list[-1][1] == 2:
                    if self.board.branches['starter'].domino_list[-1][0][0] == held[0]:
                        if held[0] == held[1]:
                            self.board.transition(2, ztwo_branch=Constants.RIGHT, spinner=held)
                            dominoes[held].draggable = False
                            self.hand.remove(held)
                        else:
                            self.board.branches['starter'].play(held, 0)
                            dominoes[held].draggable = False
                            self.hand.remove(held)
                    elif self.board.branches['starter'].domino_list[-1][0][0] == held[1]:
                        self.board.branches['starter'].play(held, 2)
                        dominoes[held].draggable = False
                        self.hand.remove(held)
            elif direction == Constants.LEFT:
                if self.board.branches['starter'].domino_list[0][1] == 0:
                    if self.board.branches['starter'].domino_list[0][0][0] == held[0]:
                        if held[0] == held[1]:
                            self.board.transition(2, ztwo_branch=Constants.LEFT, spinner=held)
                            dominoes[held].draggable = False
                        else:
                            self.board.branches['starter'].play_left(held, 2)
                            dominoes[held].draggable = False
                        self.hand.remove(held)
                    elif self.board.branches['starter'].domino_list[0][0][0] == held[1]:
                        self.board.branches['starter'].play_left(held, 0)
                        dominoes[held].draggable = False
                        self.hand.remove(held)
                else:  # board.branches['starter'].domino_list[-1][1] == 1: is implied
                    if self.board.branches['starter'].domino_list[0][0][0] == held[0]:
                        if held[0] == held[1]:
                            self.board.transition(2, ztwo_branch=Constants.LEFT, spinner=held)
                            dominoes[held].draggable = False
                            self.hand.remove(held)
                        else:
                            self.board.branches['starter'].play_left(held, 2)
                            dominoes[held].draggable = False
                            self.hand.remove(held)
        else:   # we're in some other state
            if self.board.branches[direction].outside_val == held[0]:
                if held[0] == held[1]:
                    self.board.branches[direction].play(held, 1)
                else:
                    self.board.branches[direction].play(held, 0)
                    dominoes[held].draggable = False
                    self.hand.remove(held)
            elif self.board.branches[direction].outside_val == held[1]:
                self.board.branches[direction].play(held, 2)
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

    def playable(self):
        if self.board.state == 0:
            return [(hand_item, 0) for hand_item in self.hand]
        elif self.board.state == 1:
            playable = []
            for dom_tup in self.hand:
                if self.board.branches['starter'].domino_list[-1][0][1] == dom_tup[0] or \
                        self.board.branches['starter'].domino_list[-1][0][1]:
                    playable.append((dom_tup, Constants.RIGHT))
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
