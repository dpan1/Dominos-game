import pygame


class Domino(pygame.Surface):
    def __init__(self, a: tuple, rotation, width, height, display):
        super().__init__((width, height, pygame.SRCALPHA))
        self.display = display
        self.width = width
        self.height = height
        self.rect = None
        self.pair = a
        self.rotation = rotation
        self.show_me = False
        self.draggable = True
        self.original = pygame.image.load(f'../tiles/{a[0]}{a[1]}.png')
        pre_scaled_image = pygame.transform.rotate(self.original, 90 * self.rotation)
        self.image = pygame.transform.scale(pre_scaled_image, (self.width, self.height))
        self.blit(self.image, (0, 0))
        pass

    def get_rect(self):
        return self.rect

    def resize(self, width, height):
        self.width, self.height = width, height

    def set_rect(self, rect):
        self.show_me = True
        self.rect = rect

    def set_rotate(self, rotation):
        center = self.image.get_rect().center
        self.rotation = rotation
        self.width = self.display.BOARD_DOMINO_HEIGHT if \
            self.rotation % 2 == 0 else self.display.BOARD_DOMINO_WIDTH
        self.height = self.display.BOARD_DOMINO_WIDTH if self.rotation % 2 == 0 else self.display.BOARD_DOMINO_HEIGHT
        pre_scaled_image = pygame.transform.rotate(self.original, 90 * self.rotation)
        self.image = pygame.transform.scale(pre_scaled_image, (self.width, self.height))
        self.rect = self.image.get_rect(center=center)
        self.blit(self.image, (0, 0))

    def place(self, tl_x, tl_y):
        self.set_rect(pygame.Rect(tl_x, tl_y,
                                  self.height if self.rotation % 2 == 0 else self.width,
                                  self.width if self.rotation % 2 == 0 else self.height))
        # super().rect = pygame.Rect(tl_x, tl_y,
        #                           self.height if self.rotation % 2 == 0 else self.width,
        #                           self.width if self.rotation % 2 == 0 else self.height)
        self.blit(self.image, (0, 0))

    # def center(self, ctr_x, ctr_y, rotation):
    #     self.rotation = rotation
    #     pre_scaled_image = pygame.transform.rotate(self.original, 90 * (self.rotation))
    #     self.image = pygame.transform.scale(pre_scaled_image, (self.height,
    #                                                            self.width))
    #     self.rect = pygame.Rect(ctr_x + self.display.ROT_DICT[Constants.ORIENTATIONS[self.rotation + 1]][0],
    #                             ctr_y + self.display.ROT_DICT[Constants.ORIENTATIONS[self.rotation + 1]][1],
    #                             self.height if self.rotation % 2 == 0 else self.width,
    #                             self.width if self.rotation % 2 == 0 else self.height ,
    #                             )
    #     self.blit(self.image, (0, 0))
    #     pass
