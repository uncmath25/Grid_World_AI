import random

from AI.base_ai import BaseAI
from Models.agent import Agent
from Models.block import Block
from Models.Utility.actions import Actions
from Models.Utility.math import compute_dist


class SeekDestroyAI(BaseAI):

    def __init__(self, position, speed_factor, game_speed, block_width, block_height, agent_name):
        """
        Initializes the ai state
        """
        super().__init__(position, speed_factor, game_speed, block_width, block_height, agent_name)
        self._exluded_actions = []
        self._current_target_name = None
        self._log = None

    def print_log(self):
        """
        Prints the log of the most recent decisions
        """
        for line in self._log:
            print(' - '.join([str(s) for s in line]))

    def _find_closest_friendly_agent_pos(self):
        """
        Finds the closest friendly agent, if any, that this agent can see
        """
        closest_friendly_agent_pos = None
        closest_friendly_agent_dist = 10000000000
        closest_friendly_agent_name = None
        agents_name_type_map = self._info.get_agents_name_type_map()
        agents_name_pos_map = self._info.get_agents_name_pos_map()
        for name in agents_name_type_map:
            if (agents_name_type_map[name] == Agent.Friendly) or (agents_name_type_map[name] == Agent.User_Controlled):
                pos = agents_name_pos_map[name]
                dist = compute_dist(self._pos, pos, self._BLOCK_WIDTH, self._BLOCK_HEIGHT)
                if dist < closest_friendly_agent_dist:
                    closest_friendly_agent_pos = tuple(pos)
                    closest_friendly_agent_dist = int(dist)
                    closest_friendly_agent_name = str(name)
        self._current_target_name = closest_friendly_agent_name
        return closest_friendly_agent_pos

    def _is_path_clear(self, self_pos, target_pos, action):
        """
        Determines if the path to the target is clear of exclusion blocks
        """
        blocks_pos_type_map = self._info.get_blocks_pos_type_map()
        if action == Actions.MOVE_LEFT:
            for y in range(target_pos[1] + 1 if target_pos[1] < self_pos[1] else target_pos[1] + 1 - self._BLOCK_WIDTH, self_pos[1]):
                if blocks_pos_type_map[(self_pos[0], y % self._BLOCK_WIDTH)] == Block.Excluded:
                    return False
        elif action == Actions.MOVE_RIGHT:
            for y in range(self_pos[1] + 1, target_pos[1] if self_pos[1] < target_pos[1] else target_pos[1] + self._BLOCK_WIDTH):
                if blocks_pos_type_map[(self_pos[0], y % self._BLOCK_WIDTH)] == Block.Excluded:
                    return False
        elif action == Actions.MOVE_UP:
            for x in range(target_pos[0] + 1 if target_pos[0] < self_pos[0] else target_pos[0] + 1 - self._BLOCK_HEIGHT, self_pos[0]):
                if blocks_pos_type_map[(x % self._BLOCK_HEIGHT, self_pos[1])] == Block.Excluded:
                    return False
        elif action == Actions.MOVE_DOWN:
            for x in range(self_pos[0] + 1, target_pos[0] if self_pos[1] < target_pos[1] else target_pos[1] + self._BLOCK_HEIGHT):
                if blocks_pos_type_map[(x % self._BLOCK_HEIGHT, self_pos[1])] == Block.Excluded:
                    return False
        return True

    def update(self, is_forced):
        """
        Inform the ai to update its state given its current info
        """
        if not is_forced and not self._check_can_update():
            return
        possible_moves = self._get_possible_moves()

        self._log = [['### Update Log for {0} ###'.format(self._AGENT_NAME)]]
        possible_moves_line = ['Possible Moves']
        possible_moves_line.extend(possible_moves)
        self._log.append(possible_moves_line)
        excluded_actions_line = ['Excluded Actions']
        excluded_actions_line.extend(self._exluded_actions)
        self._log.append(excluded_actions_line)

        target_agent_pos = None
        agents_name_pos_map = self._info.get_agents_name_pos_map()
        if not self._current_target_name or self._current_target_name not in agents_name_pos_map:
            target_agent_pos = self._find_closest_friendly_agent_pos()
        else:
            target_agent_pos = agents_name_pos_map[self._current_target_name]
        if not target_agent_pos:
            return random.choice(possible_moves)

        best_action = None
        best_action_coord_diff = 10000000000
        left_diff = (self._pos[1] - target_agent_pos[1]) % self._BLOCK_WIDTH
        self._log.append(['Move Left Score', left_diff, 'PATH OPEN' if self._is_path_clear(self._pos, target_agent_pos, Actions.MOVE_LEFT) else 'PATH BLOCKED'])
        if left_diff > 0 and left_diff < best_action_coord_diff:
            if Actions.MOVE_LEFT in possible_moves and Actions.MOVE_LEFT not in self._exluded_actions and self._is_path_clear(self._pos, target_agent_pos, Actions.MOVE_LEFT):
                best_action = Actions.MOVE_LEFT
                best_action_coord_diff = left_diff
        right_diff = (target_agent_pos[1] - self._pos[1]) % self._BLOCK_WIDTH
        self._log.append(['Move Right Score', right_diff, 'PATH OPEN' if self._is_path_clear(self._pos, target_agent_pos, Actions.MOVE_RIGHT) else 'PATH BLOCKED'])
        if right_diff > 0 and right_diff < best_action_coord_diff:
            if Actions.MOVE_RIGHT in possible_moves and Actions.MOVE_RIGHT not in self._exluded_actions and self._is_path_clear(self._pos, target_agent_pos, Actions.MOVE_RIGHT):
                best_action = Actions.MOVE_RIGHT
                best_action_coord_diff = right_diff
        top_diff = (self._pos[0] - target_agent_pos[0]) % self._BLOCK_HEIGHT
        self._log.append(['Move Up Score', top_diff, 'PATH OPEN' if self._is_path_clear(self._pos, target_agent_pos, Actions.MOVE_UP) else 'PATH BLOCKED'])
        if top_diff > 0 and top_diff < best_action_coord_diff:
            if Actions.MOVE_UP in possible_moves and Actions.MOVE_UP not in self._exluded_actions and self._is_path_clear(self._pos, target_agent_pos, Actions.MOVE_UP):
                best_action = Actions.MOVE_UP
                best_action_coord_diff = top_diff
        bottom_diff = (target_agent_pos[0] - self._pos[0]) % self._BLOCK_HEIGHT
        self._log.append(['Move Down Score', bottom_diff, 'PATH OPEN' if self._is_path_clear(self._pos, target_agent_pos, Actions.MOVE_DOWN) else 'PATH BLOCKED'])
        if bottom_diff > 0 and bottom_diff < best_action_coord_diff:
            if Actions.MOVE_DOWN in possible_moves and Actions.MOVE_DOWN not in self._exluded_actions and self._is_path_clear(self._pos, target_agent_pos, Actions.MOVE_DOWN):
                best_action = Actions.MOVE_DOWN
                best_action_coord_diff = bottom_diff

        self._log.append(['Best Action', best_action])
        self._log.append(['#########################'])

        if best_action is not None:
            self._exluded_actions.clear()
            return best_action
        else:
            self._log = [['### Update Log for {0} ###'.format(self._AGENT_NAME)]]

            random_move = random.choice([move for move in possible_moves if move not in self._exluded_actions])
            if random_move == Actions.MOVE_LEFT:
                self._exluded_actions.append(Actions.MOVE_RIGHT)
            elif random_move == Actions.MOVE_RIGHT:
                self._exluded_actions.append(Actions.MOVE_LEFT)
            elif random_move == Actions.MOVE_UP:
                self._exluded_actions.append(Actions.MOVE_DOWN)
            elif random_move == Actions.MOVE_DOWN:
                self._exluded_actions.append(Actions.MOVE_UP)

            self._log.append(['Random choice made: {0}'.format(random_move)])
            self._log.append(['#########################'])

            return random_move

    class PerformanceReport():

        def __init__(self, name, position, total_target_agents):
            """
            Initializes the report state
            """
            self._NAME = str(name)
            self._positions = [tuple(position)]
            self._agents_destroyed_timestamps_map = {}
            self._TOTAL_TARGET_AGENTS = int(total_target_agents)

        def update(self, position, new_agents_destroyed):
            """
            Updates the report log based upon the diff between the newly passed info and the old info
            """
            self._positions.append(tuple(position))
            for pair in new_agents_destroyed:
                self._agents_destroyed_timestamps_map[len(self._positions) - 1] = tuple(pair)

        def _evaluate_performance(self):
            """
            Evaluate the performance of the given ai
            """
            agents_destroyed_timestamps = list(self._agents_destroyed_timestamps_map)
            if len(agents_destroyed_timestamps) == 0:
                return 0
            score = (100 / float(self._TOTAL_TARGET_AGENTS)) * 1 / max(1, agents_destroyed_timestamps[0])
            for i in range(1, len(agents_destroyed_timestamps)):
                score += (100 / float(self._TOTAL_TARGET_AGENTS)) * 1 / max(1, agents_destroyed_timestamps[i] - agents_destroyed_timestamps[i - 1])
            return int(score)

        def print_to_console(self):
            """
            Prints the performance report to the console
            """
            print('Agent {0} destroyed {1} targets agents in {2} update cycles with a score of {3}'.format(self._NAME, self._TOTAL_TARGET_AGENTS, len(self._positions) - 1, self._evaluate_performance()))

        def export_to_csv(self):
            """
            Exports the performance report as a csv file
            """
            pass
