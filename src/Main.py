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
    # conflicted about whether Board is structured correctly, or if I should just make it an object and a rectangle
    board_rect = pygame.Rect(0, 0, display.WINDOW_WIDTH, display.BOARD_HEIGHT)
    board = Board(board_rect, display)
    # Domino objects are pygame Surfaces, and contain information about rotation
    dominoes = {(j, i): Domino((j, i), 3, display.DOMINO_WIDTH, display.DOMINO_HEIGHT, display)
                for i in range(7) for j in range(i+1)}

    hand_rect = pygame.Rect(0, display.BOARD_HEIGHT + 1, display.WINDOW_WIDTH, display.HAND_HEIGHT)
    hand = Hand(hand_rect, display)

    game = Game(board)
    game.deal()  # players in the game are handed dominoes are divided between

    # default hand setting statement, comment for debugging
    # hand.set_hand(game.hands[0])

    # debugging hand setting statements
    hand.set_hand([(1, 3), (3, 4), (3, 5), (2, 5), (2, 3), (0, 6), (3, 3)])  # set a test hand
    # hand.set_hand([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 3)])  # set a test hand
    hand.set_dom_width(display.DOMINO_WIDTH)
    hand.set_dom_height(display.DOMINO_HEIGHT)

    hand.arrange(dominoes)

    held = None

    # drop_surfaces = dict()  # This helps immensely with debugging, but starts to get in the way because it's not
    # transparent

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
                    if board.state == 1:
                        for drop in board.branches['starter'].drop_areas.keys():
                            if board.branches['starter'].drop_areas[drop].collidepoint(mouse_pos):
                                print(f"drop area {drop} clicked")
                    elif board.state == 2:
                        for direction in [Constants.LEFT, Constants.RIGHT]:
                            if board.branches[direction].drop_area.collidepoint(mouse_pos):
                                print(f"drop area {direction} clicked")
                    elif board.state == 3:
                        for direction in Constants.ORIENTATIONS:
                            if board.branches[direction].drop_area.collidepoint(mouse_pos):
                                print(f"drop area {direction} clicked")

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
                        dominoes[held].draggable = False
                        board.play(held)
                    held = None
                    hand.arrange(dominoes)
                    board.arrange(dominoes)

                elif board.state == 1:
                    for side in [Constants.LEFT, Constants.RIGHT]:
                        if board.branches['starter'].drop_areas[side].collidepoint(mouse_pos):
                            if side == Constants.RIGHT:
                                if board.branches['starter'].domino_list[-1][1] == 0:
                                    if board.branches['starter'].domino_list[-1][0][1] == held[0]:
                                        if held[0] == held[1]:
                                            board.transition(2, ztwo_branch=side, spinner=held)
                                            dominoes[held].draggable = False
                                            hand.remove(held)
                                            break  # otherwise, the second part of the loop won't work.
                                        else:
                                            board.branches['starter'].play(held, 0)
                                            dominoes[held].draggable = False
                                            hand.remove(held)
                                            break
                                    elif board.branches['starter'].domino_list[-1][0][1] == held[1]:
                                        board.branches['starter'].play(held, 2)
                                        dominoes[held].draggable = False
                                        hand.remove(held)
                                        break
                                elif board.branches['starter'].domino_list[-1][1] == 2:  # board.branches['starter'].domino_list[-1][1] == 1: is implied
                                    if board.branches['starter'].domino_list[-1][0][0] == held[0]:
                                        if held[0] == held[1]:
                                            board.transition(2, ztwo_branch=side, spinner=held)
                                            dominoes[held].draggable = False
                                            hand.remove(held)
                                            break
                                        else:
                                            board.branches['starter'].play(held, 0)
                                            dominoes[held].draggable = False
                                            hand.remove(held)
                                            break
                                    elif board.branches['starter'].domino_list[-1][0][0] == held[1]:
                                        board.branches['starter'].play(held, 2)
                                        dominoes[held].draggable = False
                                        hand.remove(held)
                                        break
                            else:  # side == Constants.LEFT
                                if board.branches['starter'].domino_list[0][1] == 0:
                                    if board.branches['starter'].domino_list[0][0][0] == held[0]:
                                        if held[0] == held[1]:
                                            board.transition(2, ztwo_branch=side, spinner=held)
                                            dominoes[held].draggable = False
                                        else:
                                            board.branches['starter'].play_left(held, 2)
                                            dominoes[held].draggable = False
                                        hand.remove(held)
                                        break
                                    elif board.branches['starter'].domino_list[0][0][0] == held[1]:
                                        board.branches['starter'].play_left(held, 0)
                                        dominoes[held].draggable = False
                                        hand.remove(held)
                                        break
                                else:  # board.branches['starter'].domino_list[-1][1] == 1: is implied
                                    if board.branches['starter'].domino_list[0][0][0] == held[0]:
                                        if held[0] == held[1]:
                                            board.transition(2, ztwo_branch=side, spinner=held)
                                            dominoes[held].draggable = False
                                            hand.remove(held)
                                            break
                                        else:
                                            board.branches['starter'].play_left(held, 2)
                                            dominoes[held].draggable = False
                                            hand.remove(held)
                                            break
                    held = None

                elif board.state == 2:
                    for branch in [Constants.LEFT, Constants.RIGHT]:
                        if board.branches[branch].drop_area.collidepoint(mouse_pos):
                            if board.branches[branch].outside_val == held[0]:
                                if held[0] == held[1]:
                                    board.branches[branch].play(held, 1)
                                else:
                                    board.branches[branch].play(held, 0)
                                dominoes[held].draggable = False
                                hand.remove(held)
                            elif board.branches[branch].outside_val == held[1]:
                                board.branches[branch].play(held, 2)
                                dominoes[held].draggable = False
                                hand.remove(held)

                    if (len(board.branches[Constants.LEFT].domino_list) != 0 and
                            len(board.branches[Constants.RIGHT].domino_list) != 0):
                        board.transition(3)

                    if held is not None:
                        held = None

                elif board.state == 3:
                    for branch in Constants.ORIENTATIONS:
                        if board.branches[branch].drop_area.collidepoint(mouse_pos):
                            if board.branches[branch].outside_val == held[0]:
                                if held[0] == held[1]:
                                    board.branches[branch].play(held, 1)
                                else:
                                    board.branches[branch].play(held, 0)
                                    dominoes[held].draggable = False
                                    hand.remove(held)
                                    break
                            elif board.branches[branch].outside_val == held[1]:
                                board.branches[branch].play(held, 2)
                                dominoes[held].draggable = False
                                hand.remove(held)
                                break
                    if held is not None:
                        held = None

                else:  # the above statements should exhaust the list of board states.
                    held = None

                board.arrange(dominoes)
                hand.arrange(dominoes)

        screen.blit(board, board_rect)

        screen.blit(hand, hand_rect)

        for dom_tup in dominoes.keys():
            if dominoes[dom_tup].show_me:
                screen.blit(dominoes[dom_tup], dominoes[dom_tup].get_rect())

        # if board.state == 1:
        #     for drop_area in board.branches['starter'].drop_areas.keys():
        #         drop_surfaces[drop_area] = pygame.Surface((board.branches['starter'].drop_areas[
        #                                                        drop_area].width,
        #                                                    board.branches['starter'].drop_areas[
        #                                                        drop_area].height
        #                                                    ))
        #         drop_surfaces[drop_area].fill(Constants.AQUA)
        #         screen.blit(drop_surfaces[drop_area], board.branches['starter'].drop_areas[drop_area])
        # else:
        #     for branch in Constants.ORIENTATIONS:
        #         if board.branches[branch] is not None:
        #             drop_surfaces[branch] = pygame.Surface((board.branches[branch].drop_area.width,
        #                                                     board.branches[branch].drop_area.height))
        #             drop_surfaces[branch].fill(Constants.AQUA)
        #             screen.blit(drop_surfaces[branch], board.branches[branch].drop_area)
        pygame.display.flip()


if __name__ == '__main__':
    main()
