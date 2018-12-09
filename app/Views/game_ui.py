import pygame
import sys
import time

from ViewModels.game import Game


class GameUI():

    def __init__(self, block_dim, block_width, block_height, background,
                 line_color, line_thickness, title, fps,
                 max_updates_per_second):
        """
        Initialize the game ui state
        """
        self._BLOCK_DIM = tuple(block_dim)
        self._BLOCK_WIDTH = int(block_width)
        self._BLOCK_HEIGHT = int(block_height)
        self._BACKGROUND = tuple(background)
        self._LINE_COLOR = tuple(line_color)
        self._LINE_THICKNESS = int(line_thickness)
        self._TITLE = str(title)
        self._FPS = int(fps)
        self._MAX_UPDATES_PER_SECOND = int(max_updates_per_second)

        self._screen = None
        self._clock = None
        self._game = None
        self._can_send_event = None
        self._last_event_notification_time = None
        self._is_paused = True
        self._kill_flag_dict = {}
        self._kill_flag_dict['kill_flag'] = False

    def init(self):
        """
        Initialize the game ui
        """
        pygame.init()
        pygame.display.set_caption(self._TITLE)
        pygame.font.init()

        self._screen = \
            pygame.display.set_mode([self._BLOCK_DIM[0]*self._BLOCK_WIDTH,
                                     self._BLOCK_DIM[1]*self._BLOCK_HEIGHT])
        self._clock = pygame.time.Clock()
        self._game = Game(self._BLOCK_DIM, self._BLOCK_WIDTH,
                          self._BLOCK_HEIGHT, self._BACKGROUND,
                          self._LINE_COLOR, self._LINE_THICKNESS, self._screen)
        self._can_send_event = False
        self._last_event_notification_time = time.time()
        pygame.display.update()

    def run(self):
        """
        Run the main game loop
        """
        game_speed_key_map = {}
        game_speed_key_map[pygame.K_1] = 0.1
        game_speed_key_map[pygame.K_2] = 0.25
        game_speed_key_map[pygame.K_3] = 0.5
        game_speed_key_map[pygame.K_4] = 0.75
        game_speed_key_map[pygame.K_5] = 1
        game_speed_key_map[pygame.K_6] = 1.5
        game_speed_key_map[pygame.K_7] = 2
        game_speed_key_map[pygame.K_8] = 2.5
        game_speed_key_map[pygame.K_9] = 3

        while not self._kill_flag_dict['kill_flag']:
            for event in pygame.event.get():
                if event.type == pygame.QUIT \
                        or (event.type == pygame.KEYDOWN
                            and event.key == pygame.K_ESCAPE):
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_SPACE:
                    self._is_paused = not self._is_paused
                    if not self._is_paused:
                        self._game.notify_game_resumed()
                    print('GAME PAUSED') \
                        if self._is_paused else print('GAME RUNNING')
                if event.type == pygame.KEYDOWN \
                        and event.key in game_speed_key_map:
                    self._game.set_game_speed(game_speed_key_map[event.key])
                    print('Game Speed: {0} Hz'.
                          format(round(1/game_speed_key_map[event.key], 1)))
                if self._is_paused and event.type == pygame.KEYDOWN \
                        and event.key == pygame.K_RETURN:
                    self._game.update(self._kill_flag_dict, True)
                    self._game.draw(self._screen)
                    pygame.display.update()
                    self._game.print_log()
                if event.type == pygame.KEYUP:
                    self._can_send_event = True

            if self._is_paused:
                continue

            keys_pressed = pygame.key.get_pressed()
            for key_index_pair in list(enumerate(keys_pressed)):
                if key_index_pair[1]:
                    if (time.time()-self._last_event_notification_time) > \
                            (1 / self._MAX_UPDATES_PER_SECOND) \
                            or self._can_send_event:
                        self._game.notify_user_input_event(key_index_pair[0])
                        self._can_send_event = False
                        self._last_event_notification_time = time.time()

            self._game.update(self._kill_flag_dict, False)
            self._game.draw(self._screen)

            pygame.display.update()
            self._clock.tick(self._FPS)
