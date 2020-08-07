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


def spacing(dimension, num_objs, obj_dim, obj_gap):
    return [i for i in range(((dimension - ((num_objs * obj_dim) + ((num_objs - 1) * obj_gap)))//2), dimension -
            ((dimension - ((num_objs * obj_dim) + ((num_objs - 1) * obj_gap)))//2) + 1, (obj_dim + obj_gap))]
