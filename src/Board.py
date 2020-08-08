import pygame
from Constants import Constants
from Branch import Branch
# TODO rewrite this coherently as a State Machine. For better code organization if anything (keeps different state
# TODO handling code together, by state, rather than by function)


class Board(pygame.Surface):
    def __init__(self, rect: pygame.Rect, display):
        super().__init__((rect.width, rect.height))
        self.display = display
        self.rect = rect
        self.fill(Constants.WHITE)
        self.state = 0
        self.starter_branch = None
        self.played_dominoes = {}
        # self.colliders = {orientation: None for orientation in Constants.ORIENTATIONS}
        self.branches = {orientation: None for orientation in Constants.ORIENTATIONS}
        self.spinner = None

    def played(self):
        return self.played_dominoes

    def reset(self):
        self.played_dominoes = {}

    def arrange(self, dominoes):
        if self.state == 0:
            pass
        elif self.state == 1:
            # Calculate length of starter branch + 2 * padding + 2 drop areas,
            # if it's wider than the screen, scale it down
            self.branches['starter'].arrange(dominoes)
            l = self.branches['starter'].drop_areas[Constants.LEFT].left
            r = self.branches['starter'].drop_areas[Constants.RIGHT].right
            if l < 0 or r > self.display.WINDOW_WIDTH:
                self.display.rescale_board(self.find_scale())
            pass
        elif self.state == 2:  # TODO look into some sort of fall through cases. if self.state > 1 and so on
            # if it's wider than the screen scale it down.
            dominoes[self.spinner].center(self.display.BOARD_CENTER[0], self.display.BOARD_CENTER[1], 3)
            # dominoes[self.spinner].center = self.display.BOARD_CENTER
            self.branches[Constants.LEFT].arrange(dominoes)
            self.branches[Constants.RIGHT].arrange(dominoes)
            # Calculate length of left and right branches + Board_short_dim + 2 * padding + 2 drop areas,
            l = self.branches[Constants.LEFT].drop_area.left
            r = self.branches[Constants.RIGHT].drop_area.right
            if l < 0 or r > self.display.WINDOW_WIDTH:
                self.display.rescale_board(self.find_scale())
                dominoes[self.spinner].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
                dominoes[self.spinner].center(self.display.BOARD_CENTER[0], self.display.BOARD_CENTER[1], 3)
                self.branches[Constants.LEFT].arrange(dominoes)
                self.branches[Constants.RIGHT].arrange(dominoes)
        elif self.state == 3:
            l = self.branches[Constants.LEFT].drop_area.left
            r = self.branches[Constants.RIGHT].drop_area.right
            # u = self.branches[Constants.UP].drop_area.
            if l < 0 or r > self.display.WINDOW_WIDTH:
                self.find_scale()
            # same as above, but with up and down.
            dominoes[self.spinner].center(self.display.BOARD_CENTER[0], self.display.BOARD_CENTER[1], 3)
            # dominoes[self.spinner].center = self.display.BOARD_CENTER
            for orientation in Constants.ORIENTATIONS:
                self.branches[orientation].arrange(dominoes)
            pass

    def transition(self, out_num, ztwo_branch=None, spinner=None):
        if out_num == 0:
            for key in self.branches.keys():
                self.branches[key] = None

        elif out_num == 1:
            self.branches["starter"] = Branch(Constants.RIGHT, self.display, self)
            for orientation in Constants.ORIENTATIONS:
                self.branches[orientation] = None

        elif out_num == 2:
            self.spinner = spinner
            if self.state == 0:
                self.branches[Constants.LEFT] = Branch(Constants.LEFT, self.display, self, spinner_val=spinner)
                self.branches[Constants.RIGHT] = Branch(Constants.RIGHT, self.display, self, spinner_val=spinner)
            elif self.state == 1:
                self.branches[Constants.LEFT] = Branch(Constants.LEFT, self.display, self, spinner_val=spinner)
                self.branches[Constants.RIGHT] = Branch(Constants.RIGHT, self.display, self, spinner_val=spinner)
                if ztwo_branch == Constants.LEFT:
                    for i in range(len(self.branches['starter'].domino_list)):
                        domino, orientation = self.branches['starter'].domino_list[i]
                        self.branches[Constants.RIGHT].\
                            play(domino, orientation)
                    self.branches[Constants.LEFT].outside_val = spinner[0]
                elif ztwo_branch == Constants.RIGHT:
                    for i in range(len(self.branches['starter'].domino_list) - 1 , -1, -1):
                        domino, orientation = self.branches['starter'].domino_list[i]
                        self.branches[Constants.LEFT]\
                            .play(domino, (orientation + 2) % 4 if orientation % 2 == 0 else orientation)
                    self.branches[Constants.RIGHT].outside_val = spinner[0]
                self.branches['starter'] = None

        elif out_num == 3:
            self.branches[Constants.UP] = Branch(Constants.UP, self.display, self, spinner_val=self.spinner)
            self.branches[Constants.DOWN] = Branch(Constants.DOWN, self.display, self, spinner_val=self.spinner)
        self.state = out_num
        pass

    def play(self, domino: tuple):
        if self.state == 0:
            if domino[0] == domino[1]:
                self.spinner = domino
                self.transition(2, spinner=domino)
                # dominoes[domino].set_rect(self.display.spinner_rect)
            else:
                self.transition(1)
                self.branches['starter'].play(domino, 0)
        # dominoes[domino].draggable = False

    def find_scale(self, u=None, d=None):
        # determine what the scale of the branch is.

        if len(self.branches[Constants.RIGHT].domino_list) > len(self.branches[Constants.LEFT].domino_list):  # right is bigger
            if u is None:
                scale_num = float(self.display.WINDOW_WIDTH) / (2 * (5 + self.branches[Constants.RIGHT].rational_length()))
                pass
            else:
                pass
        else:
            if u is None:
                scale_num = float(self.display.WINDOW_WIDTH) / (2 * (5 + self.branches[Constants.LEFT].rational_length()))
            else:
                pass
        return scale_num
        # self.display.rescale_board(scale_num)
        # if self.state == 0:
        #     pass
        # elif self.state == 1:
        #     for dom_tup, _ in self.branches['starter'].domino_list:
        #         dominoes[dom_tup].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
        # elif self.state == 2:
        #     dominoes[self.spinner].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
        #     for orientation in [Constants.LEFT, Constants.RIGHT]:
        #         for dom_tup, _ in self.branches[orientation].domino_list:
        #             dominoes[dom_tup].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
        # elif self.state == 3:
        #     dominoes[self.spinner].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
        #     for orientation in Constants.ORIENTATIONS:
        #         for dom_tup, _ in self.branches[orientation].domino_list:
        #             dominoes[dom_tup].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
        #     pass

    def sum_outsides(self):
        if self.state == 0:
            return 0
        elif self.state == 1:
            side_a = self.branches['starter'].domino_list[0][0][0] if \
                self.branches['starter'].domino_list[0][1] == 0 else \
                self.branches['starter'].domino_list[0][1]
            side_b = self.branches['starter'].domino_list[-1][0][0] if \
                self.branches['starter'].domino_list[-1][1] == 0 else \
                self.branches['starter'].domino_list[-1][1]
            return side_a + side_b
            pass  # TODO this is some weird math
        else:
            if self.branches[Constants.LEFT].is_empty or self.branches[Constants.RIGHT].is_empty:
                return (2 * self.spinner[0]) + sum(branch.outside_value() for branch in self.branches)
            else:
                return sum(self.branches[orientation].outside_value() if self.branches[orientation] is not None else 0
                           for orientation in Constants.ORIENTATIONS)
        pass
