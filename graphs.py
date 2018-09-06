import math
import networkx as nx
import numpy as np

# LOCAL
from lobby import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Graphs():
        centrality_names =  {'Betweenness':'blue', 'Closeness':'red', 'Degree':'green'}
        
        @staticmethod
        def create_graph():
                return nx.Graph()

        @staticmethod
        def get_centrality_names():
                return Graphs.centrality_names

        @staticmethod
        def get_centr_func(which):
                if which == 'Betweenness':
                        centr_func = nx.betweenness_centrality
                elif which == 'Closeness':
                        centr_func = nx.closeness_centrality
                elif which == 'Degree':
                        centr_func = nx.degree_centrality
                elif which == 'Lobby':
                        centr_func = lobby
                elif which == 'Eigenvector':
                        centr_func = nx.eigenvector_centrality
                elif which == 'Pagerank':
                        centr_func = nx.pagerank
                else:
                        logger.error('wrong centrality id=%s', which)
                        exit()

                return centr_func

        @staticmethod
        def get_centrality_values(G, which):
                func = Graphs.get_centr_func(which)
                return func(G)
        
        @staticmethod
        def calc_normalized_centralities(G):
		# DEGREE
                degs = nx.degree_centrality(G)                
                for i in range(G.number_of_nodes()):
                        G.node[i]['Degree'] = degs[i]
                        
		# BETWEENNESS
                bets = nx.betweenness_centrality(G)
                for i in range(G.number_of_nodes()):
                        G.node[i]['Betweenness'] = bets[i]

		# CLOSENESS - already normalized
                closes = nx.closeness_centrality(G)
                for i in range(G.number_of_nodes()):
                        G.node[i]['Closeness']   = closes[i]

                return(degs, bets, closes, lobby(G, None))
                        
        @staticmethod
        def calc_graph_vertex_lobby(G, log_file=None):
                lobby(G, log_file)

        @staticmethod
        def degree_stat(G):
                """Calculate the average degree and the standard deviation degree.
                Source: http://holanda.xyz/files/mean.c
                """
                avg_prev = float(G.degree(0))
                var_prev = 0
                for i in range(1, G.number_of_nodes()):
                        deg = float(G.degree(i))
                        avg_curr = avg_prev + (deg - avg_prev)/(i + 1)
                        var_curr = var_prev + (deg - avg_prev) * (deg - avg_curr)
                        
                        avg_prev = avg_curr
                        var_prev = var_curr
                        
                stdev = math.sqrt(var_curr/(G.number_of_nodes() - 1))

                return (avg_curr, stdev)

        @staticmethod
        def pre_process_centralities(books):
                """
                Calculate centralities and store in associative array.
                """
                # PRE-processing
                f = open('lobby.log', 'w') # log file, used to debug the results
                for book in books.get_books():
                        G = book.get_graph()
                        Graphs.calc_normalized_centralities(G)
                        ## Already do the assignment of lobby value to each vertex                
                        Graphs.calc_graph_vertex_lobby(G, f)
                f.close()

        def get_degree_avg_neighbors(G):
                k2knns = {} # map degree to average neighbor degree average
                (xs, ys, xxs, yavgs) = ([], [], [], [])
                (xsp, ysp, xxsp, yavgsp) = ([], [], [], [])

                for u in G.nodes():
                        k = G.degree(u)
                        knn = 0.0 # degree average of neighbors

                        for v in list(G.neighbors(u)):
                                knn += G.degree(v)

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
