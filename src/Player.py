import random
import time


class Player(object):
    def __init__(self, player_id, board):
        random.seed(time.time())
        self.hand = None
        self.player_id = player_id
        self.board = board
        pass

    def set_hand(self, hand):
        self.hand = hand

    def play_domino(self, index):
        assert index < len(self.hand)

    def random_picker(self):
        return random.choice(self.playable)

    def all_money_is_good_money_picker(self):
        local_max = max(map(lambda y: y[2], self.playable))
        max_list = list(filter(lambda x: x[2] == local_max, self.playable))
        if local_max == 0:
            return random.choice(self.playable)
        elif local_max > 0:
            return random.choice(list(filter(lambda x: x[2] == local_max, self.playable)))
        else:
            return None
