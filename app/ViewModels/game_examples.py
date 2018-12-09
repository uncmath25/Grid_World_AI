import random

from AI.random_ai import RandomAI
from AI.enemy.seek_and_destroy_ai import SeekDestroyAI
from Models.agent import Agent
from Models.block import Block
from Models.Utility.color import Color
from Models.Utility.math import compute_dist


DEFAULT_GAME_SPEED = 1


def load_blocks_basic(block_width, block_height, excluded_block_number,
                      random_seed):
    """
    Builds a random mix of empty and excluded blocks
    """
    random.seed(random_seed)
    blocks_map = {}
    possible_pos = []
    for row in range(block_height):
        for col in range(block_width):
            blocks_map[(row, col)] = Block(Block.Empty, Color.SOLID_BLACK,
                                           (row, col))
            possible_pos.append((row, col))
    for _ in range(excluded_block_number):
        random_pos_index = random.randint(0, len(possible_pos))
        random_pos = possible_pos[random_pos_index]
        blocks_map[(random_pos[0], random_pos[1])] \
            = Block(Block.Excluded, Color.SOLID_GREEN,
                    (random_pos[0], random_pos[1]))
        del possible_pos[random_pos_index]
    return(blocks_map, possible_pos)


def load_agents_one_vs_one(block_width, block_height, possible_pos,
                           speed_factor=1, min_agent_distance=4):
    """
    Builds a user-controlled agent and an aggressive enemy
    """
    agent_dist = 0
    while agent_dist < min_agent_distance:
        possible_pos_copy = list(possible_pos)
        random_pos_index = random.randint(0, len(possible_pos_copy))
        random_pos = possible_pos_copy[random_pos_index]
        player_1_name = 'PLayer 1'
        player_1 = Agent(player_1_name, Agent.User_Controlled, None,
                         Color.TRANS_BLUE, random_pos, block_width,
                         block_height)
        del possible_pos[random_pos_index]
        random_pos_index = random.randint(0, len(possible_pos_copy))
        random_pos = possible_pos_copy[random_pos_index]
        player_2_name = 'PLayer 2'
        player_2 = Agent(player_2_name, Agent.Enemy,
                         SeekDestroyAI(random_pos, speed_factor,
                                       DEFAULT_GAME_SPEED, block_width,
                                       block_height, player_2_name),
                         Color.TRANS_RED, random_pos, block_width,
                         block_height)
        agent_dist = compute_dist(player_1.get_pos(), player_2.get_pos(),
                                  block_width, block_height)
    agents = [player_1, player_2]
    agents_name_radii_map = {}
    agents_name_radii_map[player_1.get_name()] = 3
    agents_name_radii_map[player_2.get_name()] = 6
    agents_performance_reports_map = {}
    agents_performance_reports_map[player_2.get_name()] = \
        SeekDestroyAI.PerformanceReport(player_2.get_name(),
                                        player_2.get_pos(), 1)
    return(agents, agents_name_radii_map, agents_performance_reports_map)


def load_agents_snake_mice(block_width, block_height, possible_pos, mice_count,
                           inactive=False, speed_factor=1,
                           min_agent_distance=2):
    """
    Builds a user-controlled agent and an aggressive enemy
    """
    agent_dist = 0
    while agent_dist < min_agent_distance:
        possible_pos_copy = list(possible_pos)
        random_pos_index = random.randint(0, len(possible_pos_copy))
        random_pos = possible_pos_copy[random_pos_index]
        snake_name = 'Snake'
        snake = Agent(snake_name, Agent.Enemy,
                      SeekDestroyAI(random_pos, speed_factor,
                                    DEFAULT_GAME_SPEED, block_width,
                                    block_height, snake_name),
                      Color.TRANS_RED, random_pos, block_width, block_height)
        del possible_pos_copy[random_pos_index]
        mice = []
        for i in range(1, mice_count+1):
            random_pos_index = random.randint(0, len(possible_pos_copy))
            random_pos = possible_pos_copy[random_pos_index]
            mouse_name = 'Mouse {0}'.format(i)
            mouse = Agent(mouse_name, Agent.Friendly,
                          RandomAI(random_pos, speed_factor,
                                   DEFAULT_GAME_SPEED, block_width,
                                   block_height, mouse_name, inactive),
                          Color.TRANS_BLUE, random_pos, block_width,
                          block_height)
            del possible_pos_copy[random_pos_index]
            mice.append(mouse)
        agent_dist = min(compute_dist(snake.get_pos(), mice[i].get_pos(),
                                      block_width, block_height)
                         for i in range(mice_count))
    agents = [snake]
    agents.extend(mice)
    agents_name_radii_map = {}
    agents_name_radii_map[snake.get_name()] = 6
    for mouse in mice:
        agents_name_radii_map[mouse.get_name()] = 6
    agents_performance_reports_map = {}
    agents_performance_reports_map[snake.get_name()] = \
        SeekDestroyAI.PerformanceReport(snake.get_name(), snake.get_pos(),
                                        mice_count)
    return(agents, agents_name_radii_map, agents_performance_reports_map)
