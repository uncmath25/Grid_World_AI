import argparse

from Models.Utility.color import Color
from Views.game_ui import GameUI


def main(block_dim, block_width, block_height, background, line_color, line_thickness, title, fps, max_updates_per_second):
    """ Runs the app """
    game_ui = GameUI(block_dim, block_width, block_height, background, line_color, line_thickness, title, fps, max_updates_per_second)
    game_ui.init()
    game_ui.run()


def run():
    """ Run the program using the cli inputs """
    BLOCK_DIM = (100, 100)
    BLOCK_WIDTH = 12
    BLOCK_HEIGHT = 8
    BACKGROUND = Color.SOLID_BLACK
    LINE_COLOR = Color.SOLID_GREEN
    LINE_THICKNESS = 3
    TITLE = 'Grid-World'
    FPS = 20
    MAX_UPDATES_PER_SECOND = 5

    main(BLOCK_DIM, BLOCK_WIDTH, BLOCK_HEIGHT, BACKGROUND, LINE_COLOR, LINE_THICKNESS, TITLE, FPS, MAX_UPDATES_PER_SECOND)
    # import cProfile
    # cProfile.run('main(BLOCK_DIM, BLOCK_WIDTH, BLOCK_HEIGHT, BACKGROUND, LINE_COLOR, LINE_THICKNESS, TITLE, FPS, MAX_UPDATES_PER_SECOND)')


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Grid World Simulation')
    args = parser.parse_args()

    try:
        run()
    except Exception as e:
        print(e)
