import time

from Models.block import Block
from Models.Utility.actions import Actions


class BaseAI():

    def __init__(self, position, speed_factor, game_speed, block_width, block_height, agent_name):
        """
        Initialize the ai state
        """
        self._pos = tuple(position)
        self._SPEED_FACTOR = float(speed_factor)
        self._game_speed = float(game_speed)
        self._BLOCK_WIDTH = int(block_width)
        self._BLOCK_HEIGHT = int(block_height)
        self._AGENT_NAME = str(agent_name)

        self._info = None
        self._last_update_time = 0

    def set_pos_info(self, pos, info):
        """
        Set the object specifying the local grid info
        """
        self._pos = tuple(pos)
        self._info = info

    def set_game_speed(self, game_speed):
        """
        Informs the ai of the updated game speed
        """
        self._game_speed = float(game_speed)

    def notify_game_resumed(self):
        """
        Informs the ai that the game is resumed and the update cycle should be reset
        """
        self._is_resumed = True

    def update(self, is_forced):
        """
        Inform the ai to update its state given its current info
        """
        raise NotImplementedError

    def _get_possible_moves(self):
        """
        Returns the list of possible moves, based upon the given blocks info
        """
        possible_actions = [Actions.MOVE_NONE]
        blocks_pos_type_map = self._info.get_blocks_pos_type_map()
        if blocks_pos_type_map[(self._pos[0], (self._pos[1] - 1) % self._BLOCK_WIDTH)] == Block.Empty:
            possible_actions.append(Actions.MOVE_LEFT)
        if blocks_pos_type_map[(self._pos[0], (self._pos[1] + 1) % self._BLOCK_WIDTH)] == Block.Empty:
            possible_actions.append(Actions.MOVE_RIGHT)
        if blocks_pos_type_map[((self._pos[0] - 1) % self._BLOCK_HEIGHT, self._pos[1])] == Block.Empty:
            possible_actions.append(Actions.MOVE_UP)
        if blocks_pos_type_map[((self._pos[0] + 1) % self._BLOCK_HEIGHT, self._pos[1])] == Block.Empty:
            possible_actions.append(Actions.MOVE_DOWN)
        return possible_actions

    def _check_can_update(self):
        """
        Inform the ai to update its state given its current info
        """
        if self._is_resumed:
            self._last_update_time = time.time()
            self._is_resumed = False
        if time.time() - self._last_update_time < self._SPEED_FACTOR * self._game_speed:
            return False
        else:
            self._last_update_time = time.time()
            return True
