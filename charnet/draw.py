"""This module contains class to draw graphs."""

import os.path
import logging

import graph_tool.draw as gt_draw

# LOCAL
from charnet.books import Books, Graphs, Project

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

class Draw(object):
    """Draw graphs."""
    def __init__(self):
        return

    def __str__(self):
        return self.__class__.__name__

    @staticmethod
    def do_graphs():
        '''Graphs for the characters' encounters are drawn for visualization
        only using matplotlib and NetworkX.'''
        LOGGER.info('* Drawing graphs...')
        books = Books.get_books()
        for book in books:
            graph = book.get_graph()
            color = book.get_vertex_color()
            vprop_degrees = Graphs.get_vprop_degrees(graph)
            file_name = 'g-' + book.get_name() + '.png'
            file_name = os.path.join(Project.get_outdir(), file_name)
            pos = gt_draw.arf_layout(graph, max_iter=0)
            gt_draw.graph_draw(graph, pos=pos, output=file_name,
                               vertex_text_color="black",
                               vertex_font_size=12,
                               vertex_fill_color=color,
                               vertex_text=graph.vertex_properties["label"],
                               vertex_size=vprop_degrees,
                               edge_pen_width=graph.edge_properties["weight"])
            LOGGER.info('* Wrote %s', file_name)
