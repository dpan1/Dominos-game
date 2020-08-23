import pygame
from Constants import Constants
from Proportions import Proportions
from Hand import Hand
from Game import Game
from Board import Board
from Domino import Domino
from GameSettings import GameSettings


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
    domino_surface_dict = {(j, i): Domino((j, i), 3, display.DOMINO_WIDTH, display.DOMINO_HEIGHT, display)
                           for i in range(7) for j in range(i+1)}

    hand_rect = pygame.Rect(0, display.BOARD_HEIGHT + 1, display.WINDOW_WIDTH, display.HAND_HEIGHT)
    hand = Hand(board, hand_rect, display)

    settings = GameSettings()

    game = Game(board, settings)
    game.deal()  # players in the game are handed dominoes are divided between

    # default hand setting statement, comment for debugging
    hand.set_hand(game.hands[0])
    game.set_hand(hand)  # this is a hack because I didn't set the compositions correctly in the beginning.
    # set hand before making tree
    # debugging hand setting statements
    # hand.set_hand([(6, 6), (5, 5), (3, 5), (2, 5), (2, 3), (0, 6), (3, 3)])  # set a test hand
    # hand.set_hand([(1, 3), (3, 4), (3, 5), (2, 5), (2, 3), (0, 6), (3, 3)])  # set a test hand
    # hand.set_hand([(0, 1), (1, 2), (2, 3), (3, 4), (4, 5), (5, 6), (3, 3)])  # set a test hand

    for i in range(3):
        game.players[i + 1].set_hand(game.hands[i + 1])

    # game.treestrap(hand)
    hand.set_dom_width(display.DOMINO_WIDTH)
    hand.set_dom_height(display.DOMINO_HEIGHT)

    hand.arrange(domino_surface_dict)

    held = None
    play_made = False

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
                    for dom_tup in domino_surface_dict.keys():
                        if domino_surface_dict[dom_tup].show_me:
                            if domino_surface_dict[dom_tup].draggable:
                                if domino_surface_dict[dom_tup].get_rect().collidepoint(mouse_pos):
                                    print(
                                        f'dom clicked at pos: ({mouse_pos[0]}, {mouse_pos[1]})')
                                    held = domino_surface_dict[dom_tup].pair
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
                domino_surface_dict[held].set_rect(pygame.Rect(event.pos[0] - (display.DOMINO_WIDTH // 2),
                                                               event.pos[1] - (display.DOMINO_HEIGHT // 2),
                                                               display.DOMINO_WIDTH,
                                                               display.DOMINO_HEIGHT)
                                                   )

            elif event.type == pygame.MOUSEBUTTONUP and held is not None:
                mouse_pos = pygame.mouse.get_pos()

                if board.state == 0:
                    if board.rect.collidepoint(mouse_pos):
                        hand.remove(held)
                        domino_surface_dict[held].draggable = False
                        board.play(held)
                        play_made = True
                    held = None

                elif board.state == 1:
                    if board.branches['starter'].drop_areas[Constants.LEFT].collidepoint(mouse_pos):
                        if board.branches['starter'].is_valid_play(held, Constants.LEFT):
                            board.branches['starter'].play_plain(held, direction=Constants.LEFT)
                            domino_surface_dict[held].draggable = False
                            hand.remove(held)
                    elif board.branches['starter'].drop_areas[Constants.RIGHT].collidepoint(mouse_pos):
                        if board.branches['starter'].is_valid_play(held, Constants.RIGHT):
                            board.branches['starter'].play_plain(held, direction=Constants.RIGHT)
                            domino_surface_dict[held].draggable = False
                            hand.remove(held)
                            play_made = True
                    held = None

                elif board.state == 2:
                    for branch in [Constants.LEFT, Constants.RIGHT]:
                        if board.branches[branch].drop_area.collidepoint(mouse_pos):
                            if board.branches[branch].get_value_end() == held[0] or \
                                    board.branches[branch].get_value_end() == held[1]:
                                board.branches[branch].play_plain(held)
                                play_made = True
                                domino_surface_dict[held].draggable = False
                                hand.remove(held)

                    if (len(board.branches[Constants.LEFT].domino_list) != 0 and
                            len(board.branches[Constants.RIGHT].domino_list) != 0):
                        board.transition(3)

                    if held is not None:
                        held = None

                elif board.state == 3:
                    for branch in Constants.ORIENTATIONS:
                        if board.branches[branch].drop_area.collidepoint(mouse_pos):
                            if board.branches[branch].outside_val == held[0] or \
                                    board.branches[branch].outside_val == held[1]:
                                board.branches[branch].play_plain(held)
                                play_made = True
                                domino_surface_dict[held].draggable = False
                                hand.remove(held)
                                break
                    if held is not None:
                        held = None

                else:  # the above statements should exhaust the list of board states.
                    held = None
                # These lines are contained in the mouse up
                board.arrange(domino_surface_dict)
                hand.arrange(domino_surface_dict)  # arrange the hand for a removed domino

        if play_made:
            tally = board.sum_outsides() % 5
            if tally == 0 and tally >= 10:
                game.scores[0] += board.sum_outsides()
            if len(hand.hand) == 0:
                print('domino!')
            game.automate(domino_surface_dict)
            play_made = False
            board.arrange(domino_surface_dict)

        screen.blit(board, board_rect)
        screen.blit(hand, hand_rect)
        # gotta show the dominos.
        for dom_tup in domino_surface_dict.keys():
            if domino_surface_dict[dom_tup].show_me:
                screen.blit(domino_surface_dict[dom_tup], domino_surface_dict[dom_tup].get_rect())

        pygame.display.flip()


if __name__ == '__main__':
    main()
