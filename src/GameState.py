from Constants import Constants
from collections import deque
import copy


class GameState(object):
    ats = {
        'STATE': 0,
        'SPINNER': None,
        'STARTER': None,
        Constants.UP: [],
        Constants.RIGHT: [],
        Constants.LEFT: [],
        Constants.DOWN: [],
        'HANDS': [],
        'TURN': 0
    }
    children = dict()

    def __init__(self, state=None, turn=None, dom_tup=None, direction=None):
        if state is not None:
            self.ats = state
        if turn is not None:
            self.ats['TURN'] = turn
        if dom_tup is not None:

            if self.ats['STATE'] == 0:
                if dom_tup[0] == dom_tup[1]:
                    self.spinner_transfer(2, spinner=dom_tup)
                else:
                    self.ats['STARTER'].append((dom_tup, 0))

            if self.ats['STATE'] == 1:
                assert direction is not None
                if direction == Constants.LEFT:
                    if self.ats['STARTER'][0][1] == 0:
                        if self.ats['STARTER'][0][0][0] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.spinner_transfer(2, spinner=dom_tup, direction=Constants.LEFT)
                            else:
                                self.ats['STARTER'].append_left((dom_tup, 2))
                        elif self.ats['STARTER'][0][0][0] == dom_tup[1]:
                            self.ats['STARTER'].append_left((dom_tup, 0))
                    else:
                        if self.ats['STARTER'][0][0][1] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.spinner_transfer(2, spinner=dom_tup, direction=Constants.LEFT)
                            else:
                                self.ats['STARTER'].append_left((dom_tup, 0))
                        elif self.ats['STARTER'][0][0][1] == dom_tup[1]:
                            self.ats['STARTER'].append_left((dom_tup, 2))

                elif direction == Constants.RIGHT:
                    if self.ats['STARTER'][-1][1] == 0:
                        if self.ats['STARTER'][-1][0][1] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.spinner_transfer(2, spinner=dom_tup, direction=Constants.LEFT)
                            else:
                                self.ats['STARTER'].append((dom_tup, 0))
                        elif self.ats['STARTER'][-1][0][1] == dom_tup[1]:
                            self.ats['STARTER'].append((dom_tup, 2))
                    else:
                        if self.ats['STARTER'][-1][0][0] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.spinner_transfer(2, spinner=dom_tup, direction=Constants.LEFT)
                            else:
                                self.ats['STARTER'].append((dom_tup, 2))
                        elif self.ats['STARTER'][-1][0][0] == dom_tup[1]:
                            self.ats['STARTER'].append((dom_tup, 0))

            elif self.ats['STATE'] == 2 or self.ats['STATE'] == 3:
                assert direction is not None
                if self.ats[direction][-1][1] == 0 or self.ats[direction][-1][1] == 1:
                    if self.ats[direction][-1][0][1] == dom_tup[0]:
                        if dom_tup[0] == dom_tup[1]:
                            self.ats[direction].append((dom_tup, 1))
                        else:
                            self.ats[direction].append((dom_tup, 0))
                    elif self.ats[direction][-1][0][1] == dom_tup[1]:
                        self.ats[direction].append((dom_tup, 2))
                else:
                    if self.ats[direction][-1][0][0] == dom_tup[0]:
                        if dom_tup[0] == dom_tup[1]:
                            self.ats[direction].append((dom_tup, 1))
                        else:
                            self.ats[direction].append((dom_tup, 0))
                    elif self.ats[direction][-1][0][0] == dom_tup[1]:
                        self.ats[direction].append((dom_tup, 2))
                if self.ats['STATE'] == 2:
                    if len(self.ats[Constants.LEFT]) > 0 and len(self.ats[Constants.RIGHT]) > 0:
                        self.ats['STATE'] = 3

    def spinner_transfer(self, out_state, spinner=None, direction=None):
        self.ats['SPINNER'] = spinner
        if self.ats['STATE'] == 1:
            self.ats['STARTER'] = deque()
        elif self.ats['STATE'] == 2:
            if direction is not None:
                if direction == Constants.LEFT:
                    self.ats[Constants.RIGHT] = self.ats['STARTER']
                    self.ats['STARTER'] = None
                else:
                    self.ats['LEFT'] = list(reversed(self.ats['STARTER']))
        self.ats['STATE'] = out_state
        pass

    def score(self):
        if self.ats['STATE'] == 0:
            return 0
        elif self.ats['STATE'] == 1:
            left_side = self.ats['STARTER'][0][0 if self.ats['STARTER'][1] == 0 else 1]
            right_side = self.ats['STARTER'][-1][1 if self.ats['STARTER'][1] == 0 else 0]
            if (left_side + right_side) % 5 == 0 and (left_side + right_side) >= 10:
                return left_side + right_side
        elif self.ats['STATE'] == 2:
            if len(self.ats['LEFT']) == 0 or len(self.ats['RIGHT']) == 0:
                pass
            else:
                pass
            pass
        elif self.ats['STATE'] == 3:
            pass
        pass

    def is_valid_play(self, dom_tup, orientation):
        if self.ats['state'] == 0:
            return True
        elif self.ats['state'] == 1:
            pass
        pass

    def __hash__(self):
        return hash(frozenset(self.ats.items()))

    def play(self, dom_tup, orientation, playbook):
        new_state = copy.copy(self.ats)
        if self.ats['state'] == 0:
            if dom_tup[0] == dom_tup[1]:
                self.spinner_transfer(2, spinner=dom_tup)
            else:
                self.spinner_transfer(1)
                self.ats['STARTER'].append((dom_tup, 0))
        elif self.ats['state'] == 1:
            pass
        elif self.ats['state'] == 2:
            pass
        elif self.ats['state'] == 3:
            pass
        return GameState()
