import math
import numpy as np
import logging

from igraph import *

# LOCAL
from lobby import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Graphs():
        centrality_names =  {'Betweenness', 'Closeness', 'Degree'}
        
        @staticmethod
        def create_graph():
                return Graph()

        @staticmethod
        def get_centrality_names():
                return Graphs.centrality_names

        @staticmethod
        def degree_centrality(G):
                '''Return an array of normalized degree centrality.'''
                N = G.vcount()
                arr = [None] * N
                for v in G.vs: # normalize
                        arr[v.index] = float(v.degree()) / N
                return arr

        @staticmethod
        def degree_stat(G):
                '''Calculate the average degree and the standard deviation degree.
                '''
                deg_sum = [] # degree summation
                for v in G.vs:
                        deg_sum.append(v.degree())

                return (np.mean(deg_sum), np.std(deg_sum))

        @staticmethod
        def get_centrality_values(G, which):
                if which == 'Betweenness':
                        arr = Graph.betweenness(G, directed=False, weights='weight')
                        N = G.vcount()
                        for v in G.vs: # normalize
                                arr[v.index] /= ((N-1)*(N-2))
                        return arr
                elif which == 'Closeness':
                        centr_func = Graph.closeness(G, weights='weight')
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

                for u in G.vs:
                        k = u.degree()
                        knn = 0.0 # degree average of neighbors

                        for v in G.neighbors(u):
                                knn += G.vs[v].degree()

                        if len(list(G.neighbors(u))) > 0:
                                knn /= len(list(G.neighbors(u)))
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
        
