
from numpy.linalg import norm
import numpy as np


class Node:
    """
    Node is a base class for storing node info for the tree
    Args:
        state: n-dim state of the tree node
    """
    def __init__(self, state):
        self.state = state


class Edge:
    """
    Edge is a base class for storing edge info for two nodes
    Args:
        node_indices: stores only the indices in a from->to configuration [from, to]
    """
    def __init__(self, node_indices):
        self.node_indices = node_indices


class RapidlyExploringRandomTree:
    """
    Defines and builds a RRT
    Args:
        :param starting_node: inputs the node from which the tree will start
        :param num_nodes: number of total nodes that are going to be present
        :param epsilon_dist: distance to create a new node
        :param threshold: limits of the state space
    """
    def __init__(self, starting_node, epsilon_dist, threshold, num_nodes=None):
        self.nodes = [starting_node]
        self.edges = []
        self.state_dim = starting_node.shape[0]
        self.num_nodes = num_nodes
        self.epsilon_dist = epsilon_dist
        self.threshold = threshold

    def get_current_node_index(self):
        """
        Get index where the current node will be inserted
        :return: len of the node list
        """
        return len(self.nodes)

    def add_node(self, node):
        """
        Add the new node to the current list of nodes
        :param node: new node
        :return: None
        """
        self.nodes.append(node)

    def add_edge(self, edge):
        """
        Add new edge to current list of edges
        :param edge: new edge
        :return: None
        """
        self.edges.append(edge)

    def build_rrt(self):
        """
        Build a complete RRT
        :return: None
        """
        if self.num_nodes is not None:
            for k in range(self.num_nodes):
                node_new, ind_near = self.build_rrt_single_node()
                # get the node index and save to the edge
                ind_new = self.get_current_node_index()
                self.add_node(node_new)
                self.add_edge([ind_near, ind_new])
        else:
            print("Num nodes should not be none")
            exit(-1)

    def build_rrt_single_node(self):
        """
        Args:
        :return: new node and index of the nearest node
        """
        # get nearest node
        # simple collision check:
        # if dist is lesser than epsilon dist, get new random node
        dist_near = 0
        while dist_near <= self.epsilon_dist:
            node_rand = self.rand_free_conf()
            node_near, ind_near, dist_near = self.nearest_vertex(node_rand)
        # create a new node at the specified distance in the direction of the random node
        node_new = self.new_conf(node_near, node_rand, dist_near)
        return node_new, ind_near

    def rand_free_conf(self):
        """
            get a new random node using the uniform distribution between [0,1] and scaling to the threshold
        :return: Created node
        """
        uniform_val = np.random.uniform(0, 1, self.state_dim)
        node = self.threshold[:, 0]*(1-uniform_val) + self.threshold[:, 1]*uniform_val
        return node

    def nearest_vertex(self, node_given):
        """
            find nearest vertex to the given node
        :param node_given: get the nearest node to the given node
        :return: nearest node, index of the nearest node and distance
        """
        dist = float("inf")
        for index, node in enumerate(self.nodes):
            d = norm(node - node_given)
            if d < dist:
                nearest = node
                nearest_index = index
                dist = d
        return nearest, nearest_index, dist

    def new_conf(self, node_near, node_rand, dist_near):
        """
            find a new node which is interpolated between two nodes
        :param node_near: nearest node
        :param node_rand:  random node
        :param dist_near: distance between nodes
        :return: new interpolated node
        """
        vector = node_rand - node_near
        node_new = node_near + (self.epsilon_dist/dist_near)*vector
        return node_new

