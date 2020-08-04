import pygame
from Constants import Constants
from Proportions import Proportions
from Hand import Hand
from Game import Game
from Board import Board
from Domino import Domino


def counter(start):
    num = start
    while True:
        num += 1
        yield num


def main():
    pygame.init()
    display = Proportions()  # handles changing domino proportions
    board_click_count = counter(0)
    hand_click_count = counter(0)
    size = display.WINDOW_WIDTH, display.WINDOW_HEIGHT
    screen = pygame.display.set_mode(size)
    screen.fill(Constants.BLACK)
    run = True

    board_rect = pygame.Rect(0, 0, display.WINDOW_WIDTH, display.BOARD_HEIGHT)
    board = Board(board_rect, display)

    dominoes = {(j, i): Domino((j, i), 3, display.DOMINO_WIDTH, display.DOMINO_HEIGHT, display) for i in range(7) for j in range(i+1)}

    hand_rect = pygame.Rect(0, display.BOARD_HEIGHT + 1, display.WINDOW_WIDTH, display.HAND_HEIGHT)
    hand = Hand(hand_rect, display)

    game = Game(board)
    game.deal()  # players in the game are handed dominoes are divided between

    hand.set_hand(game.hands[0])
    hand.set_dom_width(display.DOMINO_WIDTH)
    hand.set_dom_height(display.DOMINO_HEIGHT)

    hand.arrange(dominoes)

    held = None

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_pos = pygame.mouse.get_pos()
                    if board.rect.collidepoint(mouse_pos):
                        print(f'board clicked {next(board_click_count)} time(s) '
                              f'at pos: ({mouse_pos[0]}, {mouse_pos[1]})')
                    if hand.rect.collidepoint(mouse_pos):
                        print(f'hand clicked {next(hand_click_count)} time(s) '
                              f'at pos: ({mouse_pos[0]}, {mouse_pos[1]})')
                    for dom_tup in dominoes.keys():
                        if dominoes[dom_tup].show_me:
                            if dominoes[dom_tup].draggable:
                                if dominoes[dom_tup].get_rect().collidepoint(mouse_pos):
                                    print(
                                        f'dom clicked at pos: ({mouse_pos[0]}, {mouse_pos[1]})')
                                    held = dominoes[dom_tup].pair

            elif event.type == pygame.MOUSEMOTION and held is not None:
                dominoes[held].set_rect(pygame.Rect(event.pos[0] - (display.DOMINO_WIDTH // 2),
                                                    event.pos[1] - (display.DOMINO_HEIGHT // 2),
                                                    display.DOMINO_WIDTH,
                                                    display.DOMINO_HEIGHT)
                                        )

            elif event.type == pygame.MOUSEBUTTONUP and held is not None:
                mouse_pos = pygame.mouse.get_pos()

                if board.state == 0:
                    if board.rect.collidepoint(mouse_pos):
                        hand.remove(held)
                        board.play(held, dominoes)
                    held = None
                    hand.arrange(dominoes)
                    board.arrange(dominoes)

                elif board.state == 1:  # TODO: replace this dummy return domino code with branch collision code.
                    # something along the lines of for collider, if collision and playable, board plays
                    if board.branches['starter'].drop_areas[Constants.LEFT].collidepoint(mouse_pos):

                        if board.branches['starter'].domino_list[0][1] == 0:

                            if board.branches['starter'].domino_list[0][0].pair[0] == held[0]:

                                if held[0] == held[1]:
                                    board.transition(2, dominoes, ztwo_branch=Constants.LEFT, spinner=held)

                                else:
                                    board.branches['starter'].play_left(held, 0)
                                hand.remove(held)

                            elif board.branches['starter'].domino_list[0][0].pair[0] == held[1]:
                                board.branches['starter'].play_left(held, 2)
                                hand.remove(held)

                        elif board.branches['starter'].domino_list[0][1] == 2:
                            if board.branches['starter'].domino_list[0][0].pair[1] == held[0]:
                                if held[0] == held[1]:
                                    board.transition(2, dominoes, ztwo_branch=Constants.LEFT, spinner=held)
                                else:
                                    board.branches['starter'].play_left(held, 0)
                                hand.remove(held)
                            elif board.branches['starter'].domino_list[0][0].pair[1] == held[1]:
                                board.branches['starter'].play_left(held, 2)
                                hand.remove(held)

                    elif board.branches['starter'].drop_areas[Constants.RIGHT].collidepoint(mouse_pos):
                        if board.branches['starter'].domino_list[-1].pair[0] == held[0]:
                            if held[0] == held[1]:
                                board.transition(2, dominoes, ztwo_branch=Constants.RIGHT, spinner=held)
                            else:
                                board.branches['starter'].play(held, 0)
                            hand.remove(held)
                        elif board.branches['starter'].domino_list[-1][0].pair[0] == held[1]:
                            board.branches['starter'].play_left(held, 2)
                            hand.remove(held)

                elif board.state == 2:
                    for branch in board.branches.keys():
                        for key in board.branches[branch].drop_areas.keys():
                            if board.branches[branch].drop_areas[key].collidepoint(mouse_pos):
                                if branch.outside_value() == held[0]:
                                    if held[0] == held[1]:
                                        hand.remove(held)
                                        branch.play(held, 1)
                                    else:
                                        hand.remove(held)
                                        branch.play(held, 0)
                                elif branch.outside_value() == held[0]:
                                    hand.remove(held)
                                    branch.play(held, 2)
                                else:
                                    held = None

                    if not (board.branches[Constants.LEFT].is_empty() or board.branches[Constants.RIGHT].is_empty()):
                        board.transition(3, dominoes)

                    if held is not None:
                        held = None

                elif board.state == 3:
                    held = None

                else:
                    held = None

                board.arrange(dominoes)
                hand.arrange(dominoes)

        screen.blit(board, board.get_rect())

        screen.blit(hand, hand.get_rect())

        for dom_tup in dominoes.keys():
            if dominoes[dom_tup].show_me:
                screen.blit(dominoes[dom_tup], dominoes[dom_tup].get_rect())

        pygame.display.flip()


if __name__ == '__main__':
    main()
