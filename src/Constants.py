

class Constants:
    NUM_BRANCHES = 4
    STARTER = (1, 1)
    RIGHT = (1, 0)
    UP = (0, -1)
    LEFT = (-1, 0)
    DOWN = (0, 1)
    # ORIENTATIONS = [DOWN, LEFT, UP, RIGHT]  # sets an ordering
    ORIENTATIONS = [RIGHT, UP, LEFT, DOWN]  # This ordering worked better for rotations in pygame, I was fighting it.
    # game modes
    FFA = 0
    TEAM = 1
    # player profiles
    RANDOM_PLAYABLE = 0
    AMIGM_THEN_RANDOM = 1
    DETECTIVE = 2
    PERFECT_KNOWLEDGE = 3
    # useful for some domino AI math and generation
    FULL_SET = {(j, i) for i in range(7) for j in range(i+1)}
    # Colors. Maybe I'll make a color setting panel where you can set the fills of different surfaces, and you can
    # define your own palette that gets saved to a pickled configuration object.
    AQUA = 0, 255, 255
    BLACK = 0, 0, 0
    BLUE = 0, 0, 255
    FUCHSIA = 255, 0, 255
    GRAY = 128, 128, 128
    GREEN = 0, 128, 0
    LIME = 0, 255, 0
    MAROON = 128, 0, 0
    NAVYBLUE = 0, 0, 128
    OLIVE = 128, 128, 0
    PURPLE = 128, 0, 128
    RED = 255, 0, 0
    SILVER = 192, 192, 192
    TEAL = 0, 128, 128
    WHITE = 255, 255, 255
    YELLOW = 255, 255, 0
