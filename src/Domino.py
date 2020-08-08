import pygame


class Domino(pygame.Surface):
    def __init__(self, pair: tuple, rotation, width, height, display):
        super().__init__((width, height), pygame.SRCALPHA)
        self.display = display
        self.width = width
        self.height = height
        self.rect = None
        self.pair = pair
        self.rotation = rotation
        self.show_me = False
        self.draggable = True
        self.original = pygame.image.load(f'../tiles/{pair[0]}{pair[1]}.png')
        self.pre_scaled_image = pygame.transform.rotate(self.original, 90 * self.rotation)
        self.image = pygame.transform.scale(self.pre_scaled_image, (self.width, self.height))
        self.blit(self.image, (0, 0))
        pass

    def get_rect(self):
        return self.rect

    def resize(self, width, height):
        self.width, self.height = width, height

    def set_rect(self, rect: pygame.Rect):
        self.show_me = True
        self.rect = rect

    def set_rotate(self, rotation):
        center = self.image.get_rect().center
        self.rotation = rotation
        self.width = self.display.BOARD_LONG_DIM if \
            self.rotation % 2 == 0 else self.display.BOARD_SHORT_DIM
        self.height = self.display.BOARD_SHORT_DIM if self.rotation % 2 == 0 else self.display.BOARD_LONG_DIM
        super().__init__((self.width, self.height))
        self.pre_scaled_image = pygame.transform.rotate(self.original, 90 * self.rotation)
        self.image = pygame.transform.scale(self.pre_scaled_image, (self.width, self.height))
        self.rect = self.image.get_rect(center=center)
        self.blit(self.image, (0, 0))

    def center(self, ctr_x, ctr_y, rotation):
        self.set_rotate(rotation)
        self.get_rect().center = ctr_x, ctr_y
        self.blit(self.image, (0, 0))
        pass
