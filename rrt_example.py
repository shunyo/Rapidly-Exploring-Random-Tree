# Generates a simple rapidly exploring random tree in a 2D region
# Coded by Arpan Kusari
# adapted from Steve LaValle

import sys, random, math, pygame
from pygame.locals import *
from rrt import RapidlyExploringRandomTree, Node, Edge
from math import sqrt,cos,sin,atan2
import numpy as np

# constants
XDIM = 640
YDIM = 480
WINSIZE = [XDIM, YDIM]
EPSILON = 20.0
NUMNODES = 500


def main():
    # initialize and prepare screen
    pygame.init()
    screen = pygame.display.set_mode(WINSIZE)
    pygame.display.set_caption('RRT      A. Kusari    ')

    # providing colors used in the demo
    white = 255, 240, 200
    red = 255, 20, 20
    black = 20, 20, 40

    # node visualization using circle
    node_radius = 2
    screen.fill(black)

    # starts from the middle of the screen
    starting_node = np.array((XDIM/2.0, YDIM/2.0))

    # draw the starting node
    pygame.draw.circle(screen, red, starting_node.astype(np.int32), int(node_radius))

    # call the RRT class using rrt_obj object
    rrt_obj = RapidlyExploringRandomTree(starting_node, NUMNODES, EPSILON, (XDIM, YDIM))

    # build rrt using algorithm
    rrt_obj.build_rrt()

    # perform visualization 
    for edge in rrt_obj.edges:
        from_node = rrt_obj.nodes[edge[0]]
        to_node = rrt_obj.nodes[edge[1]]
        pygame.draw.line(screen, white, from_node, to_node)
        pygame.draw.circle(screen, red, to_node.astype(np.int32), int(node_radius))
        pygame.display.update()
        pygame.time.wait(100)


# if python says run, then we should run
if __name__ == '__main__':
    main()


