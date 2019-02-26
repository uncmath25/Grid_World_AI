import pygame


class Item():

    Food = 'Food'

    def __init__(self, item_type, color, position):
        """
        Initialize item state
        """
        self._TYPE = str(item_type)
        self._pos = tuple(position)
        self._COLOR = tuple(color)

    def get_type(self):
        """
        Returns the block type
        """
        return str(self._TYPE)

    def get_pos(self):
        """
        Return the current position of the block
        """
        return tuple(self._pos)

    def draw(self, screen, block_dim, line_thickness):
        """
        Draw the block
        """
        perc_size = 0.6
        left = block_dim[0] * self._pos[1] + ((line_thickness - 1) / 2) - 0.5 * (1 - perc_size) * block_dim[0]
        top = block_dim[1] * self._pos[0] + ((line_thickness - 1) / 2) - 0.5 * (1 - perc_size) * block_dim[1]
        width = perc_size * (block_dim[0] - (line_thickness - 1))
        height = perc_size * (block_dim[1] - (line_thickness - 1))
        rect = pygame.Surface((width, height), pygame.SRCALPHA)
        rect.fill(self._COLOR)
        screen.blit(rect, (left, top))
