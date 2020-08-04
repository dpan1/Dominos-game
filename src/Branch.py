import pygame
from Constants import Constants
from collections import deque
# For domino orientation, 0 is standard, 1 is double oriented, 2 is reverse oriented
# orientation in constructor should be from the Constants class.


class Branch(object):
    def __init__(self, orientation: tuple, display, parent, spinner_val=None):
        # super(Branch, self).__init__()
        # self.is_starter = is_starter
        self.is_empty = True
        self.display = display
        self.parent = parent
        self.domino_list = deque()
        self.orientations = []
        self.orientation = orientation
        self.drop_areas = dict()
        self.drop_area = None
        self.outside_val = spinner_val
        self.center = None
        self.is_starter = False
        self.center_dim = self.display.BOARD_HEIGHT // 2, self.display.WINDOW_WIDTH // 2
        if spinner_val is None:
            left_rect = pygame.Rect((self.display.WINDOW_WIDTH // 2) - self.length()//2 - self.display.DROP_AREA_SIDE,
                                    (self.display.BOARD_HEIGHT // 2) - (self.display.DROP_AREA_SIDE // 2),
                                    self.display.DROP_AREA_SIDE, self.display.DROP_AREA_SIDE)
            right_rect = pygame.Rect((self.display.WINDOW_WIDTH // 2) + self.length() // 2,
                                     (self.display.BOARD_HEIGHT // 2) - (self.display.DROP_AREA_SIDE // 2),
                                     self.display.DROP_AREA_SIDE, self.display.DROP_AREA_SIDE)
            self.drop_areas[Constants.LEFT] = left_rect
            self.drop_areas[Constants.RIGHT] = right_rect
            self.is_starter = True
        else:
            self.drop_area = pygame.Rect(self.center_dim[0] + (self.length() * self.orientation[0]),
                                         self.center_dim[1] + (self.length() * self.orientation[1]),
                                         self.display.DROP_AREA_SIDE,
                                         self.display.DROP_AREA_SIDE
                                         )

    def add_domino(self, domino, orientation: int):
        self.domino_list.append((domino, orientation))
        # self.orientations.append(orientation)
        pass

    def play(self, domino, orientation):
        self.domino_list.append((domino, orientation))
        pass

    def play_left(self, domino, orientation):
        self.domino_list.appendleft((domino, orientation))

    def rescale(self, scale_num, scale_den, dominoes):
        for domino in self.parent.domino_list:
            pass
        pass

    def arrange(self, dominoes):
        if self.is_starter:
            tl_x_series = list(range((self.display.WINDOW_WIDTH // 2) - (self.length() // 2)
                                - self.display.BOARD_DOMINO_HEIGHT // 2,
                                (self.display.WINDOW_WIDTH // 2) + (self.length() // 2),
                                (self.display.DOMINO_HEIGHT + self.display.DOMINO_PADDING)
                                ))
            for (domino, orientation), x in zip(self.domino_list, tl_x_series):
                dominoes[domino] = pygame.transform.rotate(dominoes[domino], 1 * 90)
                # dominoes[domino].set_rotate(Constants.ORIENTATIONS.index(self.orientation) + orientation - 1)
                dominoes[domino].set_rect(pygame.Rect(x + (self.display.BOARD_DOMINO_HEIGHT // 2), (self.display.BOARD_HEIGHT // 2) - (self.display.BOARD_DOMINO_WIDTH // 2)))
        else:
            pass

    def center_value(self, center_dim, index, orientation):
        return (self.display.domino_padding * index) \
               + sum(list(map(lambda x:
                              self.display.DOMINO_HEIGHT if x % 2 == 0 else self.display.DOMINO_WIDTH,
                              self.orientations[:index])))

    def drop_area_tl(self):  # TODO figure out this calculation
        return

    def length(self):
        length = (self.display.DOMINO_PADDING * (len(self.domino_list) + 1 if self.is_starter is None else 0)) \
                 + sum(list(map(lambda x: self.display.DOMINO_HEIGHT if x[1] % 2 == 0 else self.display.DOMINO_WIDTH,
                                self.domino_list)))
        return length

    def outside_value(self):  # TODO does not account for starting branch
        if self.orientations[-1]:
            return self.domino_list[-1][0] * 2
        else:
            # TODO needs checking, might be the reverse orientation
            return self.domino_list[-1][0] if self.orientations[-1] == 0 else self.domino_list[-1][1]
        pass
