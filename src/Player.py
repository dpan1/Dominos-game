

class Player(object):
    def __init__(self, player_id, board):
        self.hand = None
        self.player_id = player_id
        self.board = board
        pass

    def set_hand(self, hand):
        self.hand = hand

    def play_domino(self, index):
        assert index < len(self.hand)

