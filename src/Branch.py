import pygame
from Constants import Constants
from collections import deque
# For domino orientation, 0 is standard, 1 is double oriented, 2 is reverse oriented
# orientation in constructor should be from the Constants class.


class Branch(object):  # not a Surface itself, but more of a Surface Traffic Controller wrapping domino_list
    def __init__(self, orientation: tuple, display, parent, spinner_val=None):
        self.display = display
        self.parent = parent
        self.domino_list = deque()
        self.orientations = []
        self.orientation = orientation
        self.drop_areas = dict()
        self.drop_area = None
        self.center = None
        self.outside_val = None
        self.is_starter = False
        self.center_dim = self.display.BOARD_HEIGHT // 2, self.display.WINDOW_WIDTH // 2
        # self.spinner_val = spinner_val
        if spinner_val is None:
            self.is_starter = True
        else:
            self.outside_val = spinner_val[0]

    def arrange(self, dominoes):
        for dom_tup, _ in self.domino_list:
            dominoes[dom_tup].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
        if self.is_starter:
            x_series = list(range((self.display.WINDOW_WIDTH // 2) - (self.length() // 2)
                                  + (self.display.BOARD_LONG_DIM // 2),
                                  (self.display.WINDOW_WIDTH // 2) + (self.length() // 2)
                                  - (self.display.BOARD_LONG_DIM // 2) + self.display.DOMINO_PADDING + 1,
                                  (self.display.BOARD_LONG_DIM + self.display.DOMINO_PADDING)))
            for (domino, orientation), x in zip(self.domino_list, x_series):
                dominoes[domino].center(x,
                                        (self.display.BOARD_HEIGHT // 2),
                                        (Constants.ORIENTATIONS.index(self.orientation) + orientation) % 4)

            self.drop_areas[Constants.LEFT] = \
                pygame.Rect(self.display.BOARD_CENTER[0] - (self.length()//2) - self.display.DOMINO_PADDING
                            - self.display.DROP_AREA_SIDE,
                            self.display.BOARD_CENTER[1] - (self.display.DROP_AREA_SIDE // 2),
                            self.display.DROP_AREA_SIDE,
                            self.display.DROP_AREA_SIDE)
            self.drop_areas[Constants.RIGHT] = \
                pygame.Rect(self.display.BOARD_CENTER[0] + (self.length() // 2)
                            + self.display.DOMINO_PADDING,
                            self.display.BOARD_CENTER[1] - (self.display.DROP_AREA_SIDE // 2),
                            self.display.DROP_AREA_SIDE,
                            self.display.DROP_AREA_SIDE)
        else:
            self.drop_area = pygame.Rect(0, 0, self.display.DROP_AREA_SIDE, self.display.DROP_AREA_SIDE)
            self.drop_area.center = \
                self.display.BOARD_CENTER[0] \
                + (self.orientation[0]
                   * (self.length()
                      + (self.display.DROP_AREA_SIDE // 2)
                      + (self.display.BOARD_SHORT_DIM // 2)
                      + ((2 if len(self.domino_list) > 0 else 1) * self.display.DOMINO_PADDING))),\
                self.display.BOARD_CENTER[1]\
                + (self.orientation[1]
                   * (self.length()
                      + (self.display.DROP_AREA_SIDE // 2)
                      + (self.display.BOARD_LONG_DIM // 2)
                      + ((2 if len(self.domino_list) > 0 else 1) * self.display.DOMINO_PADDING)))
            first_position = \
                ((self.display.BOARD_CENTER[0] +
                 (self.orientation[0] *
                  (((self.display.BOARD_SHORT_DIM + self.display.BOARD_LONG_DIM)//2) +
                  self.display.DOMINO_PADDING))),
                 (self.display.BOARD_CENTER[1] +
                  (self.orientation[1] * (self.display.BOARD_LONG_DIM + self.display.DOMINO_PADDING))))
            pairs = [(self.domino_list[i][1], self.domino_list[i+1][1]) for i in range(len(self.domino_list) - 1)]
            if len(self.domino_list) > 0:
                dominoes[self.domino_list[0][0]].\
                    center(first_position[0], first_position[1],
                           (Constants.ORIENTATIONS.index(self.orientation) + self.domino_list[0][1]) % 4)
            if len(self.domino_list) > 1:
                additions = [(((self.display.BOARD_LONG_DIM + self.display.BOARD_SHORT_DIM)//2) +
                              self.display.DOMINO_PADDING) if
                             (pair[0] == 1 or pair[1] == 1) else
                             (self.display.BOARD_LONG_DIM + self.display.DOMINO_PADDING) for pair in pairs]
                positions = [((first_position[0] + (self.orientation[0] * sum(additions[:i+1]))),
                              (first_position[1] + (self.orientation[1] * (sum(additions[:i+1])))))
                             for i in range(len(additions))]
                for i in range(len(self.domino_list) - 1):
                    dominoes[self.domino_list[i+1][0]].center(positions[i][0],
                                                              positions[i][1],
                                                              (Constants.ORIENTATIONS.index(self.orientation)
                                                               + self.domino_list[i + 1][1]) % 4)

    def get_end_value(self):
        if len(self.domino_list) > 0:
            domino, orientation = self.domino_list[-1][1]
            if orientation == 0:
                return domino[1]
            else:
                return domino[0]
        else:
            return 0

    def get_left_end_value(self):
        if len(self.domino_list) > 0:
            domino, orientation = self.domino_list[-1][1]
            if orientation == 0:
                return domino[0]
            else:
                return domino[1]
        else:
            return 0

    def get_score_value(self):
        if len(self.domino_list) > 0:
            domino, orientation = self.domino_list[-1][1]
            if orientation == 0:
                return domino[1]
            elif orientation == 1:
                return sum(domino)
            elif orientation == 2:
                return domino[0]
        else:
            return 0

    def length(self):
        length = (self.display.DOMINO_PADDING * ((len(self.domino_list) - 1) if len(self.domino_list) > 0 else 0)) \
                 + sum(list(map(
                    lambda x: self.display.BOARD_LONG_DIM if x[1] % 2 == 0
                    else self.display.BOARD_SHORT_DIM, self.domino_list)))
        return length

    def is_valid_play(self, domino, direction=None):
        if self.parent.state == 1:
            if direction == Constants.LEFT:
                if self.domino_list[0][1] == 0:
                    if self.domino_list[0][0][0] == domino[0]:
                        return True
                    elif self.domino_list[0][0][0] == domino[1]:
                        return True
                elif self.domino_list[0][1] == 2:
                    if self.domino_list[0][0][1] == domino[0]:
                        return True
                    elif self.domino_list[0][0][1] == domino[1]:
                        return True
            elif direction == Constants.RIGHT:
                if self.domino_list[-1][1] == 0:
                    if self.domino_list[-1][0][0] == domino[0]:
                        return True
                    elif self.domino_list[-1][0][0] == domino[1]:
                        return True
                elif self.domino_list[-1][1] == 2:
                    if self.domino_list[-1][0][1] == domino[0]:
                        return True
                    elif self.domino_list[-1][0][1] == domino[1]:
                        return True
            return False
        else:
            if self.get_end_value() == domino[0] or self.get_end_value() == domino[1]:
                return True
            else:
                return False

    def play_plain(self, domino, direction=None):
        if self.parent.state == 1:
            if direction == Constants.LEFT:
                if self.domino_list[0][1] == 0:
                    if self.domino_list[0][0][0] == domino[0]:
                        if domino[0] == domino[1]:
                            self.parent.transition(2, ztwo_branch=direction, spinner=domino)
                        else:
                            self.play_left(domino, 2)
                    elif self.domino_list[0][0][0] == domino[1]:
                        self.play_left(domino, 0)
                elif self.domino_list[0][1] == 2:
                    if self.domino_list[0][0][1] == domino[0]:
                        if domino[0] == domino[1]:
                            self.parent.transition(2, ztwo_branch=direction, spinner=domino)
                        else:
                            self.play_left(domino, 2)
                    elif self.domino_list[0][0][1] == domino[1]:
                        self.play_left(domino, 0)
            elif direction == Constants.RIGHT:
                if self.domino_list[-1][1] == 0:
                    if self.domino_list[-1][0][1] == domino[0]:
                        if domino[0] == domino[1]:
                            self.parent.transition(2, ztwo_branch=direction, spinner=domino)
                        else:
                            self.play(domino, 2)
                    elif self.domino_list[0][0][0] == domino[1]:
                        self.play(domino, 0)
                elif self.domino_list[0][1] == 2:
                    if self.domino_list[-1][0][1] == domino[0]:
                        if domino[0] == domino[1]:
                            self.parent.transition(2, ztwo_branch=direction, spinner=domino)
                        else:
                            self.play_left(domino, 2)
                    elif self.domino_list[0][0][1] == domino[1]:
                        self.play_left(domino, 0)
        else:
            if domino[0] == domino[1]:
                self.domino_list.append((domino, 1))
            else:
                if self.get_end_value() == domino[0]:
                    self.domino_list.append((domino, 0))
                elif self.get_end_value() == domino[1]:
                    self.domino_list.append((domino, 2))

    def play(self, domino, orientation):
        self.domino_list.append((domino, orientation))

    def play_left(self, domino, orientation):
        self.domino_list.appendleft((domino, orientation))

    def rational_length(self):
        my_sum = 0
        for _, orientation in self.domino_list:
            if orientation % 2 == 0:
                my_sum += 20
            else:
                my_sum += 10
        return 30 + (2 * (len(self.domino_list) + 1)) + my_sum  # my rationale is that padding is 2
