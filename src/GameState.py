from Constants import Constants


class GameState:
    def __init__(self, hands, state=None, turn=None, dom_tup=None, direction=None, scores=None, score=None):
        self.children = dict()
        if state is not None:
            self.ats = state
        if turn is not None:
            self.ats['TURN'] = turn
            if score is not None:
                self.ats['SCORES'][turn] = self.outsides() + score
        if dom_tup is not None:
            # self.ats['HANDS'][self.ats['TURN']].remove(dom_tup)
            self.ats['HANDS'][self.ats['TURN']] -= 2 ** (hands[self.ats['TURN']].index(dom_tup))

            if self.ats['STATE'] == 0:
                if dom_tup[0] == dom_tup[1]:
                    self.ats['SPINNER'] = dom_tup
                    self.ats['STATE'] = 2
                else:
                    self.ats['S_RIGHT'] = (dom_tup, 0)
                    self.ats['S_LEFT'] = (dom_tup, 0)
                    self.ats['STATE'] = 1

            elif self.ats['STATE'] == 1:
                assert direction is not None
                if direction == Constants.LEFT:
                    if self.ats['S_LEFT'][1] == 0:
                        if self.ats['S_LEFT'][0][0] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.ats['SPINNER'] = dom_tup
                                self.ats['RIGHT'] = (self.ats['S_RIGHT'], 0)
                                self.ats['STATE'] = 2
                            else:
                                self.ats['S_LEFT'] = (dom_tup, 2)
                        elif self.ats['S_LEFT'][0][0] == dom_tup[1]:
                            self.ats['S_LEFT'] = (dom_tup, 0)
                    else:
                        if self.ats['S_LEFT'][0][1] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.ats['SPINNER'] = dom_tup
                                self.ats['RIGHT'] = (self.ats['S_RIGHT'], 0)
                                self.ats['STATE'] = 2
                            else:
                                self.ats['S_LEFT'] = (dom_tup, 0)
                        elif self.ats['S_LEFT'][0][1] == dom_tup[1]:
                            self.ats['S_LEFT'] = (dom_tup, 2)

                elif direction == Constants.RIGHT:
                    if self.ats['S_RIGHT'][1] == 0:
                        if self.ats['S_RIGHT'][0][1] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.ats['SPINNER'] = dom_tup
                                self.ats['LEFT'] = (self.ats['S_LEFT'][0], (self.ats['S_LEFT'][1] + 2) % 4)
                                self.ats['STATE'] = 2
                            else:
                                self.ats['S_RIGHT'] = dom_tup, 0
                        elif self.ats['S_RIGHT'][0][1] == dom_tup[1]:
                            self.ats['S_RIGHT'] = dom_tup, 2
                    else:
                        if self.ats['S_RIGHT'][0][0] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.ats['SPINNER'] = dom_tup
                                self.ats['LEFT'] = (self.ats['S_LEFT'][0], (self.ats['S_LEFT'][1] + 2) % 4)
                                self.ats['STATE'] = 2
                            else:
                                self.ats['S_RIGHT'] = dom_tup, 2
                        elif self.ats['S_RIGHT'][0][0] == dom_tup[1]:
                            self.ats['S_RIGHT'] = dom_tup, 0

            elif self.ats['STATE'] == 2 or self.ats['STATE'] == 3:
                assert direction is not None
                if self.ats[direction] is None:
                    if self.ats['SPINNER'][0] == dom_tup[0]:
                        self.ats[direction] = dom_tup, 0
                    else:
                        self.ats[direction] = dom_tup, 2
                else:
                    if self.ats[direction][1] == 0 or self.ats[direction][1] == 1:
                        if self.ats[direction][0][1] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.ats[direction] = dom_tup, 0
                            else:
                                self.ats[direction] = dom_tup, 0
                        elif self.ats[direction][0][1] == dom_tup[1]:
                            self.ats[direction] = dom_tup, 2
                    else:
                        if self.ats[direction][0][0] == dom_tup[0]:
                            if dom_tup[0] == dom_tup[1]:
                                self.ats[direction] = dom_tup, 1
                            else:
                                self.ats[direction] = dom_tup, 0
                        elif self.ats[direction][0][0] == dom_tup[1]:
                            self.ats[direction] = dom_tup, 2
                if self.ats['STATE'] == 2:
                    if self.ats[Constants.LEFT] is not None and self.ats[Constants.RIGHT] is not None:
                        self.ats['STATE'] = 3
            if turn is None:
                self.ats['TURN'] = ((self.ats['TURN'] + 1) % 4)

        if scores is not None:
            self.ats['SCORES'] = scores
        if self.outsides() % 5 == 0 and self.outsides() >= 10:
            self.ats['SCORES'][self.ats['TURN']] += self.outsides()

    def outsides(self):
        if self.ats['STATE'] == 0:
            return 0
        elif self.ats['STATE'] == 1:
            left_side = self.ats['S_LEFT'][0][0 if self.ats['S_LEFT'][1] == 0 else 1]
            right_side = self.ats['S_RIGHT'][0][1 if self.ats['S_RIGHT'][1] == 0 else 0]
            if (left_side + right_side) % 5 == 0 and (left_side + right_side) >= 10:
                return left_side + right_side
            else:
                return 0
        elif self.ats['STATE'] == 2:
            if self.ats[Constants.LEFT] is None and self.ats[Constants.RIGHT] is None:
                return sum(self.ats['SPINNER'])
            elif self.ats[Constants.RIGHT] is None:
                return sum(self.ats['SPINNER']) + \
                       self.ats[Constants.LEFT][0][0 if self.ats[Constants.LEFT][1] == 2 else 1]
            elif self.ats[Constants.LEFT] is None:
                return sum(self.ats['SPINNER']) + \
                       self.ats[Constants.RIGHT][0][0 if self.ats[Constants.RIGHT][1] == 2 else 1]
            else:
                print('how did we get here?')
        elif self.ats['STATE'] == 3:
            return sum((self.ats[direction][0][0 if self.ats[direction][1] == 2 else 1]
                        if self.ats[direction] is not None else 0) for direction in Constants.ORIENTATIONS)
        pass

    def __hash__(self):
        return hash(frozenset(self.ats.items()))

    def playable(self, player, hands):
        if self.ats['STATE'] == 0:
            return [(hand_item, 0) for hand_item in hands[player]]
        elif self.ats['STATE'] == 1:
            playable = []
            for i in range(7):
                if self.ats['HANDS'][player] & (2 ** i):
                    dom_tup = hands[player][i]
                    s_left = self.ats['S_LEFT'][0][0 if self.ats['S_LEFT'][1] == 0 else 1]
                    s_right = self.ats['S_RIGHT'][0][1 if self.ats['S_RIGHT'][1] == 0 else 0]
                    if s_right == dom_tup[0] or s_right == dom_tup[1]:
                        playable.append((dom_tup, Constants.RIGHT))
                    if s_left == dom_tup[0] or s_left == dom_tup[1]:
                        playable.append((dom_tup, Constants.LEFT))
            return playable
        elif self.ats['STATE'] == 2 or self.ats['STATE'] == 3:
            playable = []
            for direction in [Constants.LEFT, Constants.RIGHT] if self.ats['STATE'] == 2 else Constants.ORIENTATIONS:
                for i in range(7):
                    if self.ats['HANDS'][player] & (2 ** i):
                        dom_tup = hands[player][i]
                        if self.ats[direction] is not None:
                            out_or = self.ats[direction][1]
                            outside_val = self.ats[direction][0 if out_or == 2 else 1]
                            if outside_val == dom_tup[0] or outside_val == dom_tup[1]:
                                playable.append((dom_tup, direction))
                        else:
                            if self.ats['SPINNER'][0] == dom_tup[0] or self.ats['SPINNER'][0] == dom_tup[1]:
                                playable.append((dom_tup, direction))
            return playable
