import os.path
import matplotlib.pyplot as plt
import pygraphviz as pgv
import logging

# LOCAL
from books import *
from plot import *


logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Draw:
        @staticmethod
        def do_graphs():
                '''Graphs for the characters' encounters are drawn for visualization
                only using matplotlib and NetworkX.'''
                edge_dict = {}
                
                logger.info('* Drawing graphs...')
                books = Books.get_books()
                for book in books:
                        factor = 10 # increase factor
                        G = book.get_graph()
                        color = book.get_vertex_color()

                        fn = 'g-' + book.get_name() + '.png'
                        fn = os.path.join(Project.get_outdir(), fn)

                        visual_style = {}
                        #visual_style['vertex_color']
                        visual_style['vertex_label'] = G.vs['name']
                        visual_style['vertex_color'] = book.get_vertex_color()
                        visual_style['vertex_size'] = [25 + math.ceil(v.degree()/5) for v in G.vs]
                        visual_style['edge_width'] = [math.ceil(int(e['weight'])/2.0) for e in G.es]
                        visual_style['layout'] = G.layout('kk')
                        visual_style['bbox'] = (600, 600)
                        visual_style["margin"] = 30
                        plot(G, fn, **visual_style)
                        logger.info('* Wrote {}'.format(fn))
