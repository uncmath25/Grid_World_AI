from AI.base_ai import BaseAI
from Models.agent import Agent
from Models.block import Block
from Models.item import Item
from Models.Utility.math import build_grid_zone


class Info():

    def __init__(self, block_width, block_height):
        """
        Initialize game state
        """
        self._BLOCK_WIDTH = int(block_width)
        self._BLOCK_HEIGHT = int(block_height)

        self._agents_name_type_map = {}
        self._agents_name_pos_map = {}
        self._blocks_pos_type_map = {}
        self._items_pos_type_map = {}

    def localize(self, center_pos, radius):
        """
        Copy the info into a readonly local version that the agent can see
        """
        agents = []
        blocks = []
        items = []
        zone = build_grid_zone(center_pos, radius, self._BLOCK_WIDTH, self._BLOCK_HEIGHT)
        for pos in zone:
            for name in self._agents_name_pos_map:
                if pos == self._agents_name_pos_map[name]:
                    agents.append(Agent(name, self._agents_name_type_map[name], BaseAI((0, 0), 0, 0, 0, 0, ''), (0, 0, 0), pos, self._BLOCK_WIDTH, self._BLOCK_HEIGHT))
            if pos in self._blocks_pos_type_map:
                blocks.append(Block(self._blocks_pos_type_map[pos], (0, 0, 0), pos))
            if pos in self._items_pos_type_map:
                items.append(Item(self._items_pos_type_map[pos], (0, 0, 0), pos))
        info_copy = Info(self._BLOCK_WIDTH, self._BLOCK_HEIGHT)
        info_copy.set_agents(agents)
        info_copy.set_blocks(blocks)
        info_copy.set_items(items)
        return info_copy

    def get_agents_name_type_map(self):
        """
        Returns the agents name to type map
        """
        return dict(self._agents_name_type_map)

    def get_agents_name_pos_map(self):
        """
        Returns the agents name to position map
        """
        return dict(self._agents_name_pos_map)

    def get_blocks_pos_type_map(self):
        """
        Returns the blocks position to type map
        """
        return dict(self._blocks_pos_type_map)

    def get_items_pos_type_map(self):
        """
        Returns the items position to type map
        """
        return dict(self._items_pos_type_map)

    def is_pos_occupied(self, pos):
        """
        Returns a flag indicating whether the given position is occupied by an agent
        """
        name_pos_map = self.get_agents_name_pos_map()
        for name in name_pos_map:
            if name_pos_map[name] == pos:
                return True
        return False

    def set_agents(self, agents):
        """
        Specifies the agents which exist in the grid
        """
        self._agents_name_type_map.clear()
        self._agents_name_pos_map.clear()
        for agent in agents:
            self._agents_name_type_map[agent.get_name()] = agent.get_type()
            self._agents_name_pos_map[agent.get_name()] = agent.get_pos()

    def set_agent_pos_by_name(self, name, pos):
        """
        Sets the agents info map at the given position with the given type
        """
        self._agents_name_pos_map[str(name)] = tuple(pos)

    def set_blocks(self, blocks):
        """
        Specifies the blocks which exist in the grid
        """
        self._blocks_pos_type_map.clear()
        for block in blocks:
            self._blocks_pos_type_map[block.get_pos()] = block.get_type()

    def set_items(self, items):
        """
        Specifies the items which exist in the grid
        """
        self._items_pos_type_map.clear()
        for item in items:
            pos = item.get_pos()
            self._items_pos_type_map[pos] = item.get_type()
