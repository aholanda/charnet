import math
import numpy as np
import logging

import graph_tool as gt
import graph_tool.centrality as gt_central

# LOCAL
from lobby import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Graphs():
        centrality_names =  {'Betweenness', 'Closeness', 'Degree'}
        
        @staticmethod
        def create_graph():
                return gt.Graph(directed=False)

        @staticmethod
        def size(G):
                '''Return the number of vertices in the graph G.'''
                assert G
                return len(list(G.vertices()))

        @staticmethod
        def length(G):
                '''Return the number of edges in the graph G.'''
                assert G
                return len(list(G.edges()))

        @staticmethod
        def density(G):
                '''The density of a network is the ratio of the number of links and
                the possible number of links

                '''
                assert G
                N = Graphs.size(G)
                M = Graphs.length(G)
                return 2*float(M) / (N*(N-1))
        
        @staticmethod
        def get_centrality_names():
                return Graphs.centrality_names

        @staticmethod
        def degree_centrality(G):
                '''Return an array of normalized degree centrality.'''
                N = Graphs.size(G)
                arr = [None] * N
                for v in G.vertices(): # normalize
                        arr[int(v)] = float(v.out_degree()) / N
                return arr

        @staticmethod
        def degree_stat(G):
                '''Calculate the average degree and the standard deviation degree.
                '''
                deg_sum = [] # degree summation
                for v in G.vertices():
                        deg_sum.append(v.out_degree())

                return (np.mean(deg_sum), np.std(deg_sum))

        @staticmethod
        def get_centrality_values(G, which):
                ewprops = G.edge_properties["weight"]
                centr_func = None
                if which == 'Betweenness':
                        centr_func = gt.PropertyMap.get_array(gt_central.betweenness(G, weight=ewprops, norm=True)[0])
                elif which == 'Closeness':
                        centr_func = gt.PropertyMap.get_array(gt.centrality.closeness(G, weight=ewprops))
                elif which == 'Degree':
                        centr_func = Graphs.degree_centrality(G)
                elif which == 'Lobby':
                        centr_func = lobby(G)
                else:
                        logger.error('* Wrong centrality id=%s', which)
                        exit()

                return centr_func

        @staticmethod
        def get_degree_avg_neighbors(G):
                k2knns = {} # map degree to average neighbor degree average
                (xs, ys, xxs, yavgs) = ([], [], [], [])
                (xsp, ysp, xxsp, yavgsp) = ([], [], [], [])

                for u in G.vertices():
                        k = u.out_degree()
                        knn = 0.0 # degree average of neighbors

                        for v in u.out_neighbors():
                                knn += v.out_degree()

                        if u.out_degree() > 0:
                                knn /= u.out_degree()
                        else:
                                continue
                        
                        xs.append(k)
                        ys.append(knn)

                        if k not in k2knns:
                                k2knns[k] = []
                        k2knns[k].append(knn)

                # calculate the avg of knns
                i = 0
                for k, knns in sorted(k2knns.items()):
                        m = np.mean(np.array(knns))
                        xxs.append(k)
                        yavgs.append(m)
                        i += 1

                # NORMALIZE DATA
                xmax = np.amax(np.array(xs))
                ymax = np.amax(np.array(ys))
                for i in range(len(xs)):
                        xsp.append(float(xs[i])/float(xmax))
                        ysp.append(float(ys[i])/float(ymax))

                for i in range(len(xxs)):
                        xxsp.append(float(xxs[i])/float(xmax))
                        yavgsp.append(float(yavgs[i])/float(ymax))

                return (xsp, ysp, xxsp, yavgsp)
        
