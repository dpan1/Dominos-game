import pygame
from Constants import Constants
from Branch import Branch


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
        pass

    def played(self):
        return self.played_dominoes

    def reset(self):
        self.played_dominoes = {}

    def get_rect(self):
        return self.rect

    def colliders(self):
        return self.colliders

    def arrange(self, dominoes):
        if self.state == 0:
            pass
        elif self.state == 1:
            self.branches['starter'].arrange(dominoes)
        elif self.state == 2:
            dominoes[self.spinner].set_rect(self.display.SPINNER_RECT)
            self.branches[Constants.LEFT].arrange(dominoes)
            self.branches[Constants.RIGHT].arrange(dominoes)
        elif self.state == 3:
            dominoes[self.spinner].set_rect(self.display.SPINNER_RECT)
            for orientation in Constants.ORIENTATIONS:
                self.branches[orientation].arrange(dominoes)
            pass

    def transition(self, out_num, dominoes, starter=None, ztwo_branch=None, spinner=None):
        if out_num == 0:
            for key in self.branches.keys():
                self.branches[key] = None

        elif out_num == 1:
            self.branches["starter"] = Branch(Constants.RIGHT, self.display, self)
            for orientation in Constants.ORIENTATIONS:
                self.branches[orientation] = None

        elif out_num == 2:
            if self.state == 0:
                self.branches[Constants.LEFT] = Branch(Constants.LEFT, self.display, self)
                self.branches[Constants.RIGHT] = Branch(Constants.RIGHT, self.display, self)
                # dominoes[spinner].set_rect(self.display.spinner_rect)
            elif self.state == 1:
                self.branches[Constants.LEFT] = Branch(Constants.LEFT, self.display, self)
                self.branches[Constants.RIGHT] = Branch(Constants.RIGHT, self.display, self)
                passed_dominoes = self.starter_branch.domino_list
                passed_orientations = self.starter_branch.orientations
                if ztwo_branch == Constants.LEFT:
                    for i in range(len(self.branches['starter'].domino_list)):
                        domino, orientation = self.branches[i]
                        self.branches[Constants.RIGHT].play(domino, orientation)
                    self.branches[Constants.RIGHT].rescale()
                elif ztwo_branch == Constants.RIGHT:
                    for i in range(len(self.branches['starter'].domino_list), -1, -1):
                        domino, orientation = self.branches[i]
                        self.branches[Constants.RIGHT].play(domino, orientation)
                    self.branches[Constants.LEFT].domino_list = reversed(self.branches['starter'].domino_list.copy())
                    self.branches[Constants.LEFT].orientations = list(map(lambda z: z if z == 2 else (z+2) % 4,
                                                                          self.branches['starter'].orientations))
                    self.branches[Constants.LEFT].rescale()
                pass
            pass
        elif out_num == 3:
            pass
        self.state = out_num
        pass

    def play(self, domino: tuple, dominoes, orient=None):
        self.spinner = domino
        if self.state == 0:
            if domino[0] == domino[1]:
                self.transition(2, dominoes, spinner=domino)
                # dominoes[domino].set_rect(self.display.spinner_rect)
            else:
                self.transition(1, dominoes)
                self.branches['starter'].play(domino, 0)
        dominoes[domino].draggable = False

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
            pass  # TODO this is some weird math that I will need to take a second with when I'm actually writing scoring
        else:
            if self.branches[Constants.LEFT].is_empty or self.branches[Constants.RIGHT].is_empty:
                return (2 * self.spinner[0]) + sum(branch.outside_value() for branch in self.branches)
            else:
                return sum(self.branches[orientation].outside_value() if self.branches[orientation] is not None else 0
                           for orientation in Constants.ORIENTATIONS)
        pass

