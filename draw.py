import matplotlib.pyplot as plt
import pygraphviz as pgv

# LOCAL
from books import *
from plot import *

class Draw:
        @staticmethod
        def do_graphs(books):
                """Graphs for the characters' encounters are drawn for visualization
                only using matplotlib and NetworkX."""

                print('Drawing graphs...')
                for book in books.get_books():
                        G = book.get_graph()
                        fn = "g-" + book.get_name() + ".png"

                        labels = {}
                        for i in range(G.number_of_nodes()):
                                labels[i] = G.node[i]['name'].rstrip("\r")
                
                        fig = plt.figure(figsize=(12,12))
                        ax = plt.subplot(111)
                        ax.set_title('Graph - ' + book.get_name().title(), fontsize=16)
                        pos = nx.spring_layout(G)
                        nx.draw(G, pos, node_size=1500, node_color=Plot.get_color(book), font_size=14, font_weight='bold')
                        nx.draw_networkx_labels(G, pos, labels, font_size=12)
                        plt.tight_layout()
                        plt.savefig(fn, format="PNG")
                        print('Wrote %s' % fn )
