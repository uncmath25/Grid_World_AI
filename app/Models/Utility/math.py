import numpy as np


def compute_dist(pos_1, pos_2, block_width, block_height):
    """ Compute the distance between two grid positions """
    return(min((pos_1[0] - pos_2[0])% block_height, (pos_2[0] - pos_1[0])% block_height) + min((pos_1[1] - pos_2[1])% block_width, (pos_2[1] - pos_1[1])% block_width))

def build_grid_zone(center_pos, distance, block_width, block_height):
    """ Builds a set of positions within a given distance of the center position, according to the taxicab metric """
    center_pos = tuple(center_pos)
    zone = {}
    zone[center_pos] = 0
    zone_boundary = {}
    zone_boundary[center_pos] = 0
    current_boundary_dist = 1
    while current_boundary_dist <= distance:
        new_zone_boundary = {}
        for pos in zone_boundary:
            left_pos = ((pos[0] - 1) % block_height, pos[1])
            right_pos = ((pos[0] + 1) % block_height, pos[1])
            top_pos = (pos[0], (pos[1] - 1) % block_width)
            bottom_pos = (pos[0], (pos[1] + 1) % block_width)
            if left_pos not in zone:
                zone[left_pos] = 0
                new_zone_boundary[left_pos] = 0
            if right_pos not in zone:
                zone[right_pos] = 0
                new_zone_boundary[right_pos] = 0
            if top_pos not in zone:
                zone[top_pos] = 0
                new_zone_boundary[top_pos] = 0
            if bottom_pos not in zone:
                zone[bottom_pos] = 0
                new_zone_boundary[bottom_pos] = 0
        zone_boundary = dict(new_zone_boundary)
        current_boundary_dist += 1
    return(list(zone))
