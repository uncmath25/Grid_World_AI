import pygame

from Models.block import Block
from Models.Utility.actions import Actions


class Agent():

    User_Controlled = 'User Controlled'
    Friendly = 'Friendly'
    Enemy = 'Enemy'

    def __init__(self, name, agent_type, ai, color, position, block_width, block_height):
        """
        Initialize agent state
        """
        self._NAME = str(name)
        self._TYPE = str(agent_type)
        self._AI = ai
        self._IS_AGGRESSIVE = self._TYPE == Agent.Enemy
        self._COLOR = tuple(color)
        self._pos = tuple(position)
        self._BLOCK_WIDTH = int(block_width)
        self._BLOCK_HEIGHT = int(block_height)

        self._INFO = None
        self._excluded_blocks_seen = None

    def get_name(self):
        """
        Return the name of the agent
        """
        return str(self._NAME)

    def get_type(self):
        """
        Returns the agent type
        """
        return str(self._TYPE)

    def is_aggressive(self):
        """
        Returns a flag indicating whether the agent can occupy other agent's blocks
        """
        return bool(self._IS_AGGRESSIVE)

    def get_pos(self):
        """
        Return the current position of the agent
        """
        return tuple(self._pos)

    def set_pos(self, pos):
        """
        Return the current position of the agent
        """
        self._pos = tuple(pos)

    def set_info(self, info):
        """
        Set the object specifying the local grid info
        """
        self._INFO = info
        if self._AI:
            self._AI.set_pos_info(self._pos, info)

    def set_game_speed(self, game_speed):
        """
        Informs the agent's ai of the updated game speed
        """
        if self._AI:
            self._AI.set_game_speed(game_speed)

    def notify_game_resumed(self):
        """
        Informs the agent's ai that the game is resumed and the update cycle should be reset
        """
        if self._AI:
            self._AI.notify_game_resumed()

    def print_log(self):
        """
        Prints the log of the ai's most recent decisions
        """
        if self._AI:
            self._AI.print_log()

    def draw(self, screen, block_dim, line_thickness):
        """
        Draw the agent's current position
        """
        left = block_dim[0] * self._pos[1] + ((line_thickness - 1) / 2)
        top = block_dim[1] * self._pos[0] + ((line_thickness - 1) / 2)
        width = block_dim[0] - (line_thickness - 1)
        height = block_dim[1] - (line_thickness - 1)
        rect = pygame.Surface((width, height), pygame.SRCALPHA)
        rect.fill(self._COLOR)
        screen.blit(rect, (left, top))

    def _move(self, action, step_size=1):
        """
        Move the agent
        """
        new_pos = list(self._pos)
        if action == Actions.MOVE_LEFT:
            new_pos[1] = (new_pos[1] - step_size) % self._BLOCK_WIDTH
        elif action == Actions.MOVE_RIGHT:
            new_pos[1] = (new_pos[1] + step_size) % self._BLOCK_WIDTH
        elif action == Actions.MOVE_UP:
            new_pos[0] = (new_pos[0] - step_size) % self._BLOCK_HEIGHT
        elif action == Actions.MOVE_DOWN:
            new_pos[0] = (new_pos[0] + step_size) % self._BLOCK_HEIGHT
        new_pos = tuple(new_pos)
        if self._INFO.get_blocks_pos_type_map()[new_pos] == Block.Empty:
            self.set_pos(new_pos)

    def _process_user_input(self, action):
        """
        Change the agent accoring to the specified action
        """
        if action in [Actions.MOVE_LEFT, Actions.MOVE_RIGHT, Actions.MOVE_UP, Actions.MOVE_DOWN]:
            self._move(action)
            return action

    def update(self, action, is_forced):
        """
        Update the agent's current state
        """
        if self._AI:
            action = self._AI.update(is_forced)
            self._move(action)
            return action is not None
        else:
            return self._process_user_input(action) is not None
