import matplotlib.pyplot as plt
import pygraphviz as pgv

# LOCAL
from books import *
from plot import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Draw:
        @staticmethod
        def do_graphs():
                """Graphs for the characters' encounters are drawn for visualization
                only using matplotlib and NetworkX."""

                logger.info('Drawing graphs...')
                books = Books.get_books()
                for book in books:
                        factor = 10 # increase factor
                        G = book.get_graph()
                        color = book.get_vertex_color()
                        fn = "g-" + book.get_name() + ".png"

                        # edge proportional to weight
                        edgewidths=[]
                        for (u,v,data) in G.edges(data=True):
                                edgewidths.append(data['weight'])

                        # vertices proportional to degree
                        nodesizes = []
                        labels = {}
                        for v in G.nodes():
                                deg = G.degree(v)
                                nodesizes.append(deg*factor)
                                if deg > 1:
                                        labels[v] = G.node[v]['name'].rstrip("\r")
                                else:
                                        labels[v] = ''
                                
                        try:
                                pos = nx.graphviz_layout(G)
                        except:
                                pos=nx.spring_layout(G,iterations=20)
                                
                        fig = plt.figure(figsize=(12,12))
                        nx.draw_networkx_edges(G, pos, alpha=0.3, width=edgewidths, edge_color=color)
                        ax = plt.subplot(111)
                        ax.set_title('Graph - ' + book.get_name().title(), fontsize=16)
                        nx.draw(G,pos, with_labels=False, node_size=factor, node_color='black')
                        nx.draw_networkx_nodes(G, pos, node_size=nodesizes, node_color=color, alpha=0.4)
                        nx.draw_networkx_edges(G, pos,alpha=0.4, node_size=0, width=1, edge_color='k')
                        nx.draw_networkx_labels(G, pos, labels, font_size=11)
                        plt.tight_layout()
                        plt.savefig(fn, format="PNG")
                        print('Wrote %s' % fn )
