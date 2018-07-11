import math
import networkx as nx

# LOCAL
from lobby import *

class Graphs():
        maxi = 0.0
        
        @staticmethod
        def create_graph():
                return nx.Graph()

        @staticmethod
        def get_avg_lobby(G, log_file=None):
                '''Return the average Lobby index of the book characters'''
                lobby(G, log_file)
                acc = 0.0
                maxi = 0
                N = G.number_of_nodes()
                for i in range(N):
                        acc = acc + G.node[i]['Lobby']

                if G.node[i]['Lobby'] > G.node[maxi]['Lobby']:
                                maxi = i
                        
                #print('Lobby', G.node[maxi], G.node[maxi]['Lobby'])

                return float(acc) / N

        @staticmethod
        def get_avg_degree(G):
                '''Return the average degree of the book characters'''
                acc = 0.0
                maxi = 0
                N = G.number_of_nodes()
                centrs = nx.degree_centrality(G)
                for i in range(N):
                        acc = acc + centrs[i]

                if centrs[i] > centrs[maxi]:
                                maxi = i
                        
                #print('Degree', G.node[maxi], centrs[maxi])

                        
                return float(acc) / N

        @staticmethod
        def get_avg_betweenness(G):
                '''Return the average betweenness of the book characters'''
                acc = 0.0
                maxi = 0
                maxii = 0
                N = G.number_of_nodes()
                centrs = nx.betweenness_centrality(G)
                for i in range(N):
                        acc =  acc + centrs[i]

                        if centrs[i] > centrs[maxi]:
                                maxi = i

                for i in range(N):
                        if i == maxi:
                                continue
                        
                        if centrs[i] > centrs[maxii]:
                                        maxii = i
                        
                print('Bet', G.node[maxi], centrs[maxi], G.node[maxii], centrs[maxii], centrs[maxi]/centrs[maxii])
                        
                return acc / N

        @staticmethod
        def get_avg_closeness(G):
                '''Return the average closeness of the book characters'''
                acc = 0.0
                maxi = 0
                N = G.number_of_nodes()
                centrs = nx.closeness_centrality(G)
                for i in range(N):
                        acc = acc + centrs[i]

                if centrs[i] > centrs[maxi]:
                        maxi = i
                        
                #print('Close', G.node[maxi], centrs[maxi])

                return acc / N
        
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
        def calc_graph_vertex_lobby(G, log_file=None):
                lobby(G, log_file)

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
