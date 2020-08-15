import pygame
from src.Constants import Constants


class Hand(pygame.Surface):
    def __init__(self, rect, display):
        super().__init__((rect.width, rect.height))
        self.display = display
        self.rect = rect
        self.hand = None
        self.fill(Constants.WHITE)
        self.dom_width = display.DOMINO_WIDTH
        self.dom_height = display.DOMINO_HEIGHT

    def set_dom_width(self, width):
        self.dom_width = width

    def set_dom_height(self, height):
        self.dom_height = height

    def set_hand(self, hand):
        self.hand = hand.copy()

    def arrange(self, dominoes):
        for left, dom_tup in zip(spacing(self.rect.width, len(self.hand), self.dom_width, 20), self.hand):
            dominoes[dom_tup].set_rect(
                pygame.Rect(left, 520, self.display.DOMINO_WIDTH, self.display.DOMINO_HEIGHT))

    def remove(self, dom: tuple):
        self.hand.remove(dom)

    def playable(self, board):
        if board.state == 0:
            return [(hand_item, 0, (hand_item[0] + hand_item[1])
                     if (hand_item[0] + hand_item[1]) % 5 and (hand_item[0] + hand_item[1]) > 5 else 0)
                    for hand_item in self.hand]
        elif board.state == 1:
            playable = []
            for dom_tup in self.hand:
                if board.branches['starter'].domino_list[-1][0][1] == dom_tup[0] or \
                        board.branches['starter'].domino_list[-1][0][1]:
                    playable.append((dom_tup, Constants.RIGHT,
                                     board.sum_outsides() if board.sum_outsides() % 5 == 0 else 0))
            return playable
        elif board.state == 2:
            playable = []
            for direction in [Constants.LEFT, Constants.RIGHT]:
                for dom_tup in self.hand:
                    if board.branches[direction].outside_val == dom_tup[0] or \
                            board.branches[direction].outside_val == dom_tup[1]:
                        playable.append((dom_tup, direction,
                                         board.sum_outsides() if board.sum_outsides() % 5 == 0 else 0))
            return playable
        elif board.state == 3:
            playable = []
            for direction in Constants.ORIENTATIONS:
                for dom_tup in self.hand:
                    if board.branches[direction].outside_val == dom_tup[0] or \
                            board.branches[direction].outside_val == dom_tup[1]:
                        playable.append((dom_tup, direction,
                                         board.sum_outsides() if board.sum_outsides() % 5 == 0 else 0))
            return playable


def spacing(dimension, num_objs, obj_dim, obj_gap):
    return [i for i in range(((dimension - ((num_objs * obj_dim) + ((num_objs - 1) * obj_gap)))//2), dimension -
            ((dimension - ((num_objs * obj_dim) + ((num_objs - 1) * obj_gap)))//2) + 1, (obj_dim + obj_gap))]
