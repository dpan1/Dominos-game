

class GameState(object):
    def __init__(self, dom_tup, direction, reward, player_index, hand_info, state_dict=None):
        self.score_ends = dict()
        self.play_ends = dict()
        self.score_changes = [0 for i in range(4)]
        self.children = []
        self.hands = hand_info
        self.hands.remove(dom_tup)
        if state_dict is not None:
            for key in state_dict.keys():
                self.play_ends, self.score_ends[key] = state_dict[key]
        pass

    def create_children(self, dom_tup, direction, state_dict):
        pass

    def score(self):
        pass
