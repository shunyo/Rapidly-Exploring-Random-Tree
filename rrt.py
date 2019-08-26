
from numpy.linalg import norm
import numpy as np
import random


class Node:
    def __init__(self, state):
        self.state = state


class Edge:
    def __init__(self, node_indices):
        self.node_indices = node_indices


class RapidlyExploringRandomTree:
    def __init__(self, starting_node, num_nodes, epsilon_dist, threshold):
        self.nodes = [starting_node]
        self.edges = []
        self.state_dim = starting_node.shape[0]
        self.num_nodes = num_nodes
        self.epsilon_dist = epsilon_dist
        self.threshold = threshold

    # build rrt from start
    def build_rrt(self):
        for k in range(self.num_nodes):
            # get nearest node
            # if dist is lesser than epsilon dist, get new random node
            dist_near = 0
            while dist_near <= self.epsilon_dist:
                node_rand = self.rand_free_conf()
                node_near, ind_near, dist_near = self.nearest_vertex(node_rand)
            node_new = self.new_conf(node_near, node_rand, dist_near)
            ind_new = len(self.nodes)
            self.nodes.append(node_new)
            self.edges.append([ind_near, ind_new])

    # get new random configuration and check if collision free
    def rand_free_conf(self):
        node = np.multiply(np.random.uniform(0, 1, self.state_dim), self.threshold)
        return node

    # find nearest vertex to the given node
    def nearest_vertex(self, node_given):
        dist = float("inf")
        for index, node in enumerate(self.nodes):
            d = norm(node - node_given)
            if d < dist:
                nearest = node
                nearest_index = index
                dist = d
        return nearest, nearest_index, dist

    # find a new node which is interpolated between two nodes
    def new_conf(self, node_near, node_rand, dist_near):
        vector = node_rand - node_near
        node_new = node_near + (self.epsilon_dist/dist_near)*vector
        return node_new

