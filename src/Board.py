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
            self.branches['starter'].arrange(dominoes)
            if self.branches['starter'].drop_areas[Constants.LEFT].left < 0 or \
                    self.branches['starter'].drop_areas[Constants.RIGHT].right > self.display.WINDOW_WIDTH:
                self.display.rescale_board(self.find_scale('starter'))
                self.branches['starter'].arrange(dominoes)
            pass
        elif self.state == 2:
            # if it's wider than the screen scale it down.
            dominoes[self.spinner].center(self.display.BOARD_CENTER[0], self.display.BOARD_CENTER[1], 3)
            self.branches[Constants.LEFT].arrange(dominoes)  # these initial ones are to make the drop rectangles
            self.branches[Constants.RIGHT].arrange(dominoes)  # for these next checks to work at all.
            # Calculate length of left and right branches + Board_short_dim + 2 * padding + 2 drop areas,
            if self.branches[Constants.LEFT].drop_area.left < 0 or \
                    self.branches[Constants.RIGHT].drop_area.right > self.display.WINDOW_WIDTH:
                self.display.rescale_board(
                    self.find_scale(
                        Constants.LEFT if self.branches[Constants.LEFT].drop_area.left < 0 else Constants.RIGHT
                    )
                )
                dominoes[self.spinner].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
                dominoes[self.spinner].center(self.display.BOARD_CENTER[0], self.display.BOARD_CENTER[1], 3)
                self.branches[Constants.LEFT].arrange(dominoes)
                self.branches[Constants.RIGHT].arrange(dominoes)
        elif self.state == 3:
            for orientation in Constants.ORIENTATIONS:
                self.branches[orientation].arrange(dominoes)
            boundaries = {
                orientation: {
                    Constants.LEFT: self.branches[Constants.LEFT].drop_area.left,
                    Constants.UP: self.branches[Constants.UP].drop_area.top,
                    Constants.RIGHT: self.branches[Constants.RIGHT].drop_area.right,
                    Constants.DOWN: self.branches[Constants.DOWN].drop_area.bottom
                }[orientation] for orientation in Constants.ORIENTATIONS
            }
            overages = {
                orientation: {
                    Constants.LEFT: 0 - boundaries[orientation],
                    Constants.UP: 0 - boundaries[orientation],
                    Constants.RIGHT: boundaries[orientation] - self.display.WINDOW_WIDTH,
                    Constants.DOWN: boundaries[orientation] - self.display.BOARD_HEIGHT
                }[orientation] for orientation in Constants.ORIENTATIONS}
            direction = None
            for orientation in Constants.ORIENTATIONS:
                if overages[orientation] > 0:
                    direction = orientation
                    break
            if direction is not None:
                self.display.rescale_board(self.find_scale(direction))
            for orientation in Constants.ORIENTATIONS:
                for dom_tup, _ in self.branches[orientation].domino_list:
                    dominoes[dom_tup].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
            dominoes[self.spinner].resize(self.display.BOARD_SHORT_DIM, self.display.BOARD_LONG_DIM)
            dominoes[self.spinner].center(self.display.BOARD_CENTER[0], self.display.BOARD_CENTER[1], 3)
            for orientation in Constants.ORIENTATIONS:
                self.branches[orientation].arrange(dominoes)

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
                elif ztwo_branch == Constants.RIGHT:
                    for i in range(len(self.branches['starter'].domino_list) - 1, -1, -1):
                        domino, orientation = self.branches['starter'].domino_list[i]
                        self.branches[Constants.LEFT]\
                            .play(domino, (orientation + 2) % 4 if orientation % 2 == 0 else orientation)
                self.branches['starter'] = None

        elif out_num == 3:
            self.branches[Constants.UP] = Branch(Constants.UP, self.display, self, spinner_val=self.spinner)
            self.branches[Constants.DOWN] = Branch(Constants.DOWN, self.display, self, spinner_val=self.spinner)
        self.state = out_num

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

    def find_scale(self, longest):
        scale_num = float(self.display.WINDOW_WIDTH if longest == Constants.LEFT or longest == Constants.RIGHT else
                          self.display.BOARD_HEIGHT) / \
                            (2 * ((5 if longest == Constants.LEFT or longest == Constants.RIGHT else 10)
                                  + self.branches[longest].rational_length()))
        return scale_num

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
        else:
            if self.branches[Constants.LEFT].is_empty or self.branches[Constants.RIGHT].is_empty:
                return (2 * self.spinner[0]) + sum(branch.get_end() for branch in self.branches)
            else:
                return sum((self.branches[orientation].get_score_value() if not self.branches[orientation].is_empty else 0)
                           if self.branches[orientation] is not None else 0 for orientation in Constants.ORIENTATIONS)
