import pygame
from Constants import Constants


class Proportions:
    # Holds display variables, and calculates dependent proportions. I don't think this is how you're supposed to do
    # this but it works, it's quick, and I don't have to think too much about it.
    def __init__(self, window_width=1024, window_height=640):
        self.WINDOW_WIDTH = window_width
        self.WINDOW_HEIGHT = window_height
        self.BOARD_HEIGHT = (window_height * 25) // 32
        self.HAND_HEIGHT = ((window_height * 7) // 32) + (window_height % 7)
        self.DOMINO_HEIGHT = (window_height * 10) // 60  # I know this is just divide by 6.
        self.DOMINO_WIDTH = self.DOMINO_HEIGHT // 2
        self.HAND_DOMINO_HEIGHT = self.DOMINO_HEIGHT
        self.BOARD_LONG_DIM = self.DOMINO_HEIGHT
        self.BOARD_SHORT_DIM = self.BOARD_LONG_DIM // 2
        self.BOARD_CENTER = self.WINDOW_WIDTH // 2, self.BOARD_HEIGHT // 2
        self.SPINNER_TL_X = (self.WINDOW_WIDTH - self.BOARD_SHORT_DIM) // 2  # top left x for a domino centered
        self.SPINNER_TL_Y = (self.BOARD_HEIGHT - self.BOARD_LONG_DIM) // 2
        self.SPINNER_RECT = pygame.Rect(self.SPINNER_TL_X, self.SPINNER_TL_Y, self.BOARD_SHORT_DIM, self.BOARD_LONG_DIM)
        self.DOMINO_PADDING = self.BOARD_SHORT_DIM // 5  # find out how to calculate 5 from 30
        self.DROP_AREA_SIDE = 3 * self.BOARD_SHORT_DIM
        self.ROT_DICT = dict()
        self.ROT_DICT[Constants.LEFT] = (self.DOMINO_HEIGHT // 2), (-1) * (self.DOMINO_WIDTH // 2)
        self.ROT_DICT[Constants.UP] = (self.DOMINO_WIDTH // 2), (self.DOMINO_HEIGHT // 2)
        self.ROT_DICT[Constants.RIGHT] = (-1) * (self.DOMINO_HEIGHT // 2), (self.DOMINO_WIDTH // 2)
        self.ROT_DICT[Constants.DOWN] = (-1) * (self.DOMINO_WIDTH // 2), (-1) * (self.DOMINO_HEIGHT // 2)

    def rescale_board(self, scale_num: float):
        """For reference, the starting scale is integral division by 6"""
        self.BOARD_LONG_DIM = int(20 * scale_num)
        self.BOARD_SHORT_DIM = self.BOARD_LONG_DIM // 2
        self.DROP_AREA_SIDE = 3 * self.BOARD_SHORT_DIM
        self.DOMINO_PADDING = self.BOARD_SHORT_DIM // 5  # find out how to calculate 5 from 30
