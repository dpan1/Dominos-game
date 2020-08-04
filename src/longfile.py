import pygame
import random


class Constants:
    BLACK = 0, 0, 0
    WHITE = 255, 255, 255
    SCREEN_WIDTH = 1024
    SCREEN_HEIGHT = 640
    HAND_X_MAX = 1023
    HAND_Y_MAX = 120
    TABLE_X_MAX = 1023
    TABLE_Y_MAX = 648
    TABLE_X_CENTER = TABLE_X_MAX // 2
    TABLE_Y_CENTER = TABLE_Y_MAX // 2
    DOMINO_SHORT_DIM = 30
    DOMINO_LONG_DIM = 60
    X_MAX = 1023
    Y_MAX = 767
    WINDOW_SIZE = X_MAX, Y_MAX
    NUM_BRANCHES = 4
    STARTER = (1, 1)
    RIGHT = (1, 0)
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    ORIENTATIONS = [DOWN, LEFT, UP, RIGHT]  # sets an ordering
    ROT_DICT = dict()
    DOMINO_SPACING = 2

    RANDOM_PLAYABLE = 0
    AMIGM_THEN_RANDOM = 1
    FULL_SET = {(j, i) for i in range(7) for j in range(i+1)}

    Aqua = 0, 255, 255
    Black = 0, 0, 0
    Blue = 0, 0, 255
    Fuchsia = 255, 0, 255
    Gray = 128, 128, 128
    Green = 0, 128, 0
    Lime = 0, 255, 0
    Maroon = 128, 0, 0
    NavyBlue = 0, 0, 128
    Olive = 128, 128, 0
    Purple = 128, 0, 128
    Red = 255, 0, 0
    Silver = 192, 192, 192
    Teal = 0, 128, 128
    White = 255, 255, 255
    Yellow = 255, 255, 0


class Domino(pygame.Surface):
    def __init__(self, a: tuple, rect: pygame.Rect):
        super().__init__((rect.width, rect.height))
        self.rect = rect
        self.pair = a
        self.rotation = 1
        self.original = pygame.image.load(f'./tiles/{a[0]}{a[1]}.png')
        pre_scaled_image = pygame.transform.rotate(self.original, 90 * self.rotation)
        self.image = pygame.transform.scale(pre_scaled_image, (rect.width, rect.height))
        self.blit(self.image, self.rect)
        pass

    def get_rect(self):
        return self.rect

    def set_rect(self, rect):
        self.rect = rect

    def set_rotate(self, rotation):
        self.rotation = rotation
        pre_scaled_image = pygame.transform.rotate(self.original, 90 * self.rotation)
        self.image = pygame.transform.scale(pre_scaled_image, (Constants.DOMINO_SHORT_DIM, Constants.DOMINO_LONG_DIM))


class Board(pygame.Surface):
    def __init__(self, rect: pygame.Rect):
        super().__init__((rect.width, rect.height))
        self.rect = rect
        self.fill(Constants.WHITE)
        self.played_dominoes = []
        self.state = 0
        self.starter_branch = None
        self.branches = {orientation: None for orientation in Constants.ORIENTATIONS}
        pass

    def reset(self):
        self.played_dominoes = {}

    def get_rect(self):
        return self.rect

    def draw(self):
        self.fill(Constants.WHITE)
        # self.blits([(dom, dom.get_rect()) for dom in self.played_dominoes])
        if len(self.played_dominoes) > 0:
            self.blit(self.played_dominoes[0], self.played_dominoes[0].get_rect())


class Hand(pygame.Surface):
    def __init__(self, rect):
        super().__init__((rect.width, rect.height))
        self.rect = rect
        self.hand = None
        self.domino_container = []
        self.domino_rects = []
        self.fill(Constants.WHITE)

    def set_hand(self, hand):
        self.hand = hand.copy()
        self.domino_container = [Domino((dom_tup), pygame.Rect(left, 520, 30, 60))for left, dom_tup in
                                 zip(spacing(self.rect.width, len(self.hand), 30, 20), self.hand)]
        pass

    def update(self):
        self.domino_container = [Domino((dom_tup), pygame.Rect(left, 520, 30, 60))for left, dom_tup in
                                 zip(spacing(self.rect.width, len(self.hand), 30, 20), self.hand)]

    def remove(self, ind: int):
        self.hand.remove(self.domino_container[ind].pair)
        del self.domino_container[ind]

    def surfaces(self):
        return self.domino_container

    def get_rect(self):
        return self.rect


def spacing(dimension, num_objs, obj_dim, obj_gap):
    return [i for i in range(((dimension - ((num_objs * obj_dim) + ((num_objs - 1) * obj_gap)))//2), dimension -
            ((dimension - ((num_objs * obj_dim) + ((num_objs - 1) * obj_gap)))//2) + 1, (obj_dim + obj_gap))]


def player_no(starting_no):
    number = starting_no
    while True:
        yield number
        number = (number + 1) % 4


class Player(object):
    def __init__(self, player_id, board):
        self.hand = None
        self.player_id = player_id
        self.board = board
        pass

    def set_hand(self, hand):
        self.hand = hand

    def play_domino(self, index):
        assert index < len(self.hand)


class Game(object):
    def __init__(self, board, starting_player=0):
        self.current_player = starting_player
        self.domino_list = [(j, i) for i in range(7) for j in range(i+1)]
        self.hands = [[] for _ in range(4)]
        self.deal()
        self.scores = [0 for _ in range(4)]
        self.players = [None]
        self.players.extend([Player(i, board) for i in range(1, 4)])
        self.state = 0
        pass

    def scores(self):
        # TODO return scores that line up with players.
        pass

    def take_score(self, player: Player, board: Board):
        pass

    def automate(self, player: Player):
        # take player action
        pass

    def deal(self):
        random.shuffle(self.domino_list)
        self.hands = [[self.domino_list[j * 4 + i] for j in range(7)] for i in range(4)]
        pass


def main():
    pygame.init()
    size = Constants.SCREEN_WIDTH, Constants.SCREEN_HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill(Constants.BLACK)
    run = True
    board_rect = pygame.Rect(0, 0, 1024, 500)
    board = Board(board_rect)
    game = Game(board)
    hand_rect = pygame.Rect(0, 501, 1024, 139)
    hand = Hand(hand_rect)
    hand.set_hand(game.hands[0])
    held = None
    played_dominos = []
    while run:
        # pygame.time.delay(100)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    for index, dom in enumerate(hand.domino_container):
                        if dom.rect.collidepoint(mouse_pos):
                            held = index
                            rect_x = hand.domino_container[held].get_rect().x
                            rect_y = hand.domino_container[held].get_rect().y
            elif event.type == pygame.MOUSEMOTION and held is not None:
                hand.domino_container[held].set_rect(pygame.Rect(event.pos[0]-15, event.pos[1] - 30, 30, 60))
                pass
            elif event.type == pygame.MOUSEBUTTONUP and held is not None:
                mouse_pos = pygame.mouse.get_pos()
                if board.state == 0:
                    if board.rect.collidepoint(mouse_pos):
                        board.played_dominoes.append(hand.domino_container[held])
                        hand.remove(held)
                        hand.update()
                    held = None
                elif board.state == 1:
                    hand.domino_container[held].set_rect(pygame.Rect(rect_x, rect_y, 30, 60))
                    held = None
                elif board.state == 2:
                    hand.domino_container[held].set_rect(pygame.Rect(rect_x, rect_y, 30, 60))
                    held = None
                elif board.state == 3:
                    hand.domino_container[held].set_rect(pygame.Rect(rect_x, rect_y, 30, 60))
                    held = None
                else:
                    hand.domino_container[held].set_rect(pygame.Rect(rect_x, rect_y, 30, 60))
                    held = None
        board.draw()
        screen.blit(board, board.get_rect())
        screen.blit(hand, hand.get_rect())
        dom_rects = [domino.get_rect() for domino in hand.domino_container]
        screen.blits([(dom.image, rect) for dom, rect in zip(hand.domino_container, dom_rects)])
        pygame.display.update()
        # pygame.display.flip()


if __name__ == '__main__':
    main()
