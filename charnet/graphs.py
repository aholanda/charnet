"""Main operations on graphs."""

import logging
from enum import Enum

import numpy as np

import graph_tool as gt
import graph_tool.centrality as gt_central

from .lobby import lobby

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class Measure(Enum):
    """IDs of measures."""
    AVG_DEGREE_OF_NEIGHBORS = 0
    BETWEENNESS = 1
    CDF = 2
    CLOSENESS = 3
    CLUSTERING_COEFFICIENT = 4
    DEGREE = 5
    DEGREE_CENTRALITY = 6
    DENSITY = 7
    LOBBY = 8
    @staticmethod
    def get_label(measure_num):
        """Return the label of the measure ID."""
        label = {
            Measure.AVG_DEGREE_OF_NEIGHBORS: 'knn',
            Measure.BETWEENNESS: 'betweenness',
            Measure.CDF: 'Pk',
            Measure.CLOSENESS: 'closeness',
            Measure.CLUSTERING_COEFFICIENT: 'clustering coefficient',
            Measure.DEGREE: 'k',
            Measure.DEGREE_CENTRALITY: 'D',
            Measure.DENSITY: 'density',
            Measure.LOBBY: 'Lobby'
        }
        lab = label[measure_num]
        assert lab
        return lab

class Graphs(object):
    """Handle all graphs in one place."""
    centrality_nums = [
        Measure.BETWEENNESS,
        Measure.CLOSENESS,
        Measure.DEGREE_CENTRALITY
    ]

    def __init__(self):
        pass

    @staticmethod
    def create_graph():
        """Return the graph."""
        return gt.Graph(directed=False)
    @staticmethod
    def size(graph):
        '''Return the number of vertices in the graph G.'''
        assert graph
        return len(list(graph.vertices()))

    @staticmethod
    def length(graph):
        '''Return the number of edges in the graph G.'''
        assert graph
        return len(list(graph.edges()))

    @staticmethod
    def density(graph):
        '''The density of a network is the ratio of the number of links and
        the possible number of links
        '''
        assert graph
        n_verts = Graphs.size(graph)
        n_edges = Graphs.length(graph)
        return 2*float(n_edges) / (n_verts*(n_verts-1))

    @staticmethod
    def get_centrality_nums():
        """Return the ID of centralities."""
        return Graphs.centrality_nums

    @staticmethod
    def get_vprop_degrees(graph):
        """Return the properties of vertices and edges of the graph."""
        if graph.graph_properties["was_vprop_degree_set"] is False:
            graph.graph_properties["was_vprop_degree_set"] = True
            for vert in graph.vertices():
                graph.vertex_properties["degree"][vert] = vert.out_degree()
        return graph.vertex_properties["degree"]

    @staticmethod
    def degree_centrality(graph):
        '''Return an array of normalized degree centrality.'''
        vprop = Graphs.get_vprop_degrees(graph)
        n_verts = Graphs.size(graph)
        arr = [None] * n_verts
        for vert in graph.vertices(): # normalize
            arr[int(vert)] = float(vprop[vert]) / n_verts
        return arr

    @staticmethod
    def degree_stat(graph):
        '''Calculate the average degree and the standard deviation degree.
        '''
        deg_sum = [] # degree summation
        for vert in graph.vertices():
            deg_sum.append(vert.out_degree())
        return (np.mean(deg_sum), np.std(deg_sum))

    @staticmethod
    def get_centrality_values(graph, which):
        """Return the centrality values for the graph."""
        ewprops = graph.edge_properties["weight"]
        centr_func = None
        if which == Measure.BETWEENNESS:
            centr_func = \
                gt.PropertyMap.get_array(gt_central.betweenness(graph,
                                                                weight=ewprops,
                                                                norm=True)[0])
        elif which == Measure.CLOSENESS:
            centr_func = gt.PropertyMap.get_array(gt.centrality.closeness(graph, weight=ewprops))
        elif which == Measure.DEGREE_CENTRALITY:
            centr_func = Graphs.degree_centrality(graph)
        elif which == Measure.LOBBY:
            centr_func = lobby(graph)
        else:
            LOGGER.error('* Wrong centrality id=%s', which)
            exit()
        return centr_func

    @staticmethod
    def get_degree_avg_neighbors(graph):
        """Return the average degrees of vertices of the graph."""
        k2knns = {} # map degree to average neighbor degree average
        (x_vals, y_vals, xxs, yavgs) = ([], [], [], [])
        (xsp, ysp, xxsp, yavgsp) = ([], [], [], [])
        for vert in graph.vertices():
            k = vert.out_degree()
            knn = 0.0 # degree average of neighbors
            for neighbor in vert.out_neighbors():
                knn += neighbor.out_degree()
            if vert.out_degree() > 0:
                knn /= vert.out_degree()
            else:
                continue
            x_vals.append(k)
            y_vals.append(knn)
            if k not in k2knns:
                k2knns[k] = []
                k2knns[k].append(knn)
        # calculate the avg of knns
        i = 0
        for k, knns in sorted(k2knns.items()):
            mean = np.mean(np.array(knns))
            xxs.append(k)
            yavgs.append(mean)
            i += 1
        # NORMALIZE DATA
        xmax = np.amax(np.array(x_vals))
        ymax = np.amax(np.array(y_vals))
        for i in range(len(x_vals)):
            xsp.append(float(x_vals[i])/float(xmax))
            ysp.append(float(y_vals[i])/float(ymax))
        for i in range(len(xxs)):
            xxsp.append(float(xxs[i])/float(xmax))
            yavgsp.append(float(yavgs[i])/float(ymax))
        return (xsp, ysp, xxsp, yavgsp)
