import math
import networkx as nx

# LOCAL
from lobby import *

class Graphs():
        def create_graph():
                return nx.Graph()
                
        def get_avg_lobby(G, log_file=None):
                '''Return the average Lobby index of the book characters'''
                lobby(G, log_file)
                acc = 0.0
                N = G.number_of_nodes()
                for i in range(N):
                        acc = acc + G.node[i]['Lobby']

                return float(acc) / N

        def get_avg_degree(G):
                '''Return the average degree of the book characters'''
                acc = 0.0
                N = G.number_of_nodes()
                degs = nx.degree_centrality(G)
                for i in range(N):
                        acc = acc + degs[i]

                return float(acc) / N

        def get_avg_betweenness(G):
                '''Return the average betweenness of the book characters'''
                acc = 0.0
                N = G.number_of_nodes()
                bets = nx.betweenness_centrality(G)
                for i in range(N):
                        acc =  acc + bets[i]

                return acc / N

        def get_avg_closeness(G):
                '''Return the average closeness of the book characters'''
                acc = 0.0
                N = G.number_of_nodes()
                closes = nx.closeness_centrality(G)
                for i in range(N):
                        acc = acc + closes[i]

                return acc / N
        
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


        def calc_graph_vertex_lobby(G, log_file=None):
                lobby(G, log_file)
        
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
