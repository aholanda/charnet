import os.path
import matplotlib.pyplot as plt
import logging

import graph_tool.draw as gt_draw

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
                        vprop_degrees = Graphs.get_vprop_degrees(G)

                        fn = 'g-' + book.get_name() + '.png'
                        fn = os.path.join(Project.get_outdir(), fn)

                        pos = gt_draw.arf_layout(G, max_iter=0)
                        gt_draw.graph_draw(G, pos=pos, output=fn,
                                           vertex_text_color="black",
                                           vertex_font_size=12,
                                           vertex_fill_color=color,
                                           vertex_text=G.vertex_properties["label"],
                                           vertex_size=vprop_degrees,
                                           edge_pen_width=G.edge_properties["weight"])

                        logger.info('* Wrote {}'.format(fn))
