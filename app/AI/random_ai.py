import random

from AI.base_ai import BaseAI
from Models.Utility.actions import Actions


class RandomAI(BaseAI):

    def __init__(self, position, speed_factor, game_speed, block_width, block_height, agent_name, inactive=False):
        """ Initializes the ai state """
        super().__init__(position, speed_factor, game_speed, block_width, block_height, agent_name)
        self._INACTIVE = bool(inactive)


    def print_log(self):
        """ Prints the log of the most recent decisions """
        pass


    def update(self, is_forced):
        """ Inform the ai to update its state given its current info """
        if not is_forced and not self._check_can_update():
            return(None)
        if self._INACTIVE:
            return(Actions.MOVE_NONE)
        else:
            return(random.choice(self._get_possible_moves()))
