import pygame

from Models.agent import Agent
from Models.info import Info
from Models.Utility.actions import Actions
from ViewModels.game_examples import load_blocks_basic, load_agents_snake_mice


class Game():

    def __init__(self, block_dim, block_width, block_height, background,
                 line_color, line_thickness, screen):
        """
        Initialize game state
        """
        self._BLOCK_DIM = tuple(block_dim)
        self._BLOCK_WIDTH = int(block_width)
        self._BLOCK_HEIGHT = int(block_height)
        self._BACKGROUND = tuple([int(color) for color in background])
        self._LINE_COLOR = tuple([int(color) for color in line_color])
        self._LINE_THICKNESS = int(line_thickness)

        self._agents = None
        self._agents_name_radii_map = None
        self._agents_performance_reports = None
        self._user_actions = []
        self._blocks_map = None
        self._block_pos_to_redraw = None
        self._info = None

        self._init_world()
        self._init_screen(screen)

    def notify_user_input_event(self, key_code):
        """
        Notify the game about a user-input event
        """
        if key_code in Actions.Map:
            self._user_actions.append(Actions.Map[key_code])

    def set_game_speed(self, game_speed):
        """
        Notifies all the agents of the change in the game's speed
        """
        for agent in self._agents:
            agent.set_game_speed(game_speed)

    def notify_game_resumed(self):
        """
        Notifies all the agents that the game is resumed
        """
        for agent in self._agents:
            agent.notify_game_resumed()

    def _init_world(self):
        """
        Initializes the initial game blocks and agents
        """
        self._blocks_map, possible_pos \
            = load_blocks_basic(self._BLOCK_WIDTH, self._BLOCK_HEIGHT, 10, 123)
        # self._agents, self._agents_name_radii_map, \
        #     self._agents_performance_reports_map \
        #     = load_agents_one_vs_one(self._BLOCK_WIDTH, self._BLOCK_HEIGHT,
        #                              possible_pos)
        self._agents, self._agents_name_radii_map, \
            self._agents_performance_reports_map \
            = load_agents_snake_mice(self._BLOCK_WIDTH, self._BLOCK_HEIGHT,
                                     possible_pos, 3, False)

        self._info = Info(self._BLOCK_WIDTH, self._BLOCK_HEIGHT)
        self._info.set_blocks(list(self._blocks_map.values()))
        self._info.set_agents(self._agents)

    def _init_screen(self, screen):
        """
        Draw the initial state of the board
        """
        screen.fill(self._BACKGROUND)
        for width in range(self._BLOCK_WIDTH):
            pygame.draw.lines(screen, self._LINE_COLOR, False,
                              ((self._BLOCK_DIM[0]*width, 0),
                               (self._BLOCK_DIM[0]*width,
                                self._BLOCK_DIM[1]*self._BLOCK_HEIGHT)),
                              self._LINE_THICKNESS)
        for height in range(self._BLOCK_HEIGHT):
            pygame.draw.lines(screen, self._LINE_COLOR, False,
                              ((0, self._BLOCK_DIM[1]*height),
                               (self._BLOCK_DIM[0]*self._BLOCK_WIDTH,
                                self._BLOCK_DIM[1]*height)),
                              self._LINE_THICKNESS)
        for row in range(self._BLOCK_HEIGHT):
            for col in range(self._BLOCK_WIDTH):
                self._blocks_map[(row, col)].\
                    draw(screen, self._BLOCK_DIM, self._LINE_THICKNESS)
        self._block_pos_to_redraw = []
        for agent in self._agents:
            agent.draw(screen, self._BLOCK_DIM, self._LINE_THICKNESS)
            self._block_pos_to_redraw.append(agent.get_pos())

    def print_log(self):
        """
        Prints the log of the agent's ai's most recent decisions
        """
        for agent in self._agents:
            agent.print_log()

    def _check_who_died(self, kill_flag_dict):
        """
        Determines which, if any, agents died during the last update cycle
        """
        friendly_agents = []
        enemy_agents = []
        destroyed_agent_pairs = []
        for agent in self._agents:
            if (agent.get_type() == Agent.User_Controlled) \
                    or (agent.get_type() == Agent.Friendly):
                friendly_agents.append(agent)
            elif (agent.get_type() == Agent.Enemy):
                enemy_agents.append(agent)
        remaining_friendly_agents = len(friendly_agents)
        for friendly_agent in friendly_agents:
            for enemy_agent in enemy_agents:
                if friendly_agent.get_pos() == enemy_agent.get_pos():
                    self._agents.remove(friendly_agent)
                    remaining_friendly_agents -= 1
                    destroyed_agent_pairs.append((friendly_agent.get_type(),
                                                  friendly_agent.get_name()))
                    print('{0} was destroyed'.
                          format(friendly_agent.get_name()))
                    break
        if remaining_friendly_agents <= 0:
            kill_flag_dict['kill_flag'] = True
        if len(destroyed_agent_pairs) > 0:
            self._info.set_agents(self._agents)
        return(destroyed_agent_pairs)

    def _end_world(self):
        """
        Cleans up any necessary game resources and prints or logs appropriate \
            performance reports
        """
        for agent in self._agents:
            if agent.get_type() == Agent.Enemy:
                self._agents_performance_reports_map[agent.get_name()].\
                    print_to_console()

    def update(self, kill_flag_dict, is_forced):
        """
        Update the game state
        """
        for agent in self._agents:
            agent.set_info(self._info.
                           localize(agent.get_pos(),
                                    self._agents_name_radii_map
                                    [agent.get_name()]))
            # TODO: Decide how many actions to pass
            action = self._user_actions[0] \
                if len(self._user_actions) > 0 else None

            if agent.update(action, is_forced) \
                    and agent.get_name() \
                    in self._agents_performance_reports_map:
                self._agents_performance_reports_map[agent.get_name()].\
                    update(agent.get_pos(),
                           self._check_who_died(kill_flag_dict))

            self._info.set_agent_pos_by_name(agent.get_name(), agent.get_pos())

        self._user_actions.clear()

        if kill_flag_dict['kill_flag']:
            self._end_world()

    def draw(self, screen):
        """
        Draw the current game state
        """
        for pos in self._block_pos_to_redraw:
            self._blocks_map[pos].draw(screen, self._BLOCK_DIM,
                                       self._LINE_THICKNESS)
        self._block_pos_to_redraw.clear()
        for agent in self._agents:
            agent.draw(screen, self._BLOCK_DIM, self._LINE_THICKNESS)
            self._block_pos_to_redraw.append(agent.get_pos())
