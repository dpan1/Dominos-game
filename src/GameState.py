from Constants import Constants
from collections import deque
import copy


class GameState(object):
    ats = {
        'STATE': 0,
        'SPINNER': None,
        'STARTER': [],
        'UP': [],
        'RIGHT': [],
        'LEFT': [],
        'DOWN': [],
        'HANDS': [],
        'TURN': 0
    }
    children = dict()

    def __init__(self, state=None, turn=None):
        if state is not None:
            self.ats = state
        if turn is not None:
            self.ats['TURN'] = turn

    def transition(self, out_state, spinner=None, direction=None):
        if out_state == 1:
            pass
        elif out_state == 2:
            self.ats['SPINNER'] = spinner
            if direction == Constants.LEFT:
                self.ats['RIGHT'] = self.ats['STARTER']
                self.ats['STARTER'] = None
            else:
                self.ats['LEFT'] = deque(reversed(self.ats['STARTER']))
        elif out_state == 3:
            pass
        self.ats['STATE'] = out_state
        pass

    def score(self):
        pass

    def valid_play(self, dom_tup, orientation):
        pass

    def __hash__(self):
        return hash(frozenset(self.ats.items()))

    def play(self, dom_tup, orientation, playbook):
        new_state = copy.deepcopy(self.ats)
        if self.ats['state'] == 0:
            if dom_tup[0] == dom_tup[1]:
                self.transition(2, )
            else:
                self.transition(1)
                self.ats['STARTER'] = dom_tup
        elif self.ats['state'] == 1:
            pass
        elif self.ats['state'] == 2:
            pass
        elif self.ats['state'] == 3:
            pass
        return GameState()
