"""This module has the function to calculate Lobby centrality."""

import os.path

import logging

from charnet.books import Project

# change INFO to DEBUG to write to "lobby.log" file
LOGGER = logging.getLogger(__name__)
LOGGER.setLevel(logging.INFO)

HANDLER = None
if LOGGER.getEffectiveLevel() == logging.DEBUG:
    HANDLER = logging.FileHandler(os.path.join(Project.get_outdir(), 'lobby.log'))
    FORMATTER = logging.Formatter('%(message)s')
    HANDLER.setFormatter(FORMATTER)
    LOGGER.addHandler(HANDLER)

def lobby(graph):
    """ Lobby or h index
        ================

        All graph vertices are traversed and Lobby index is calculated
        and stored in the lobby macro-field.

        If a node has the following list of neighbors sorted by degree:

         ==========  ========
         neighbor     degree
         ==========  ========
         1          21
         2          18
         3           4
         4           3
         ==========  ========

         the Lobby index is 3 because degree $\\leq$ neighbor_position.

    """
    n_verts = len(list(graph.vertices()))
    lobbies = [0] * n_verts

    LOGGER.debug('* %s', graph.graph_properties["name"])

    for vert in graph.vertices():

        LOGGER.debug('%s\tdegree=%s',
                     graph.vertex_properties['label'][vert],
                     str(vert.out_degree()))

        degs = [] # neighbors' degree

        for neighbor in vert.out_neighbors():
            degs.append(neighbor.out_degree())

        degs.sort()
        degs.reverse()
        old_idx = idx = 0
        for deg in degs:
            lob = idx = idx + 1

            LOGGER.debug("\t%s\t%s", str(idx), str(deg))

            if (deg < idx):
                lob = old_idx
                break
            old_idx = idx

            LOGGER.debug("** Lobby=%s", str(lob))

        lobbies[int(vert)] = float(lob) / n_verts # normalize by N vertices

        if HANDLER:
            LOGGER.debug('* Wrote %s', HANDLER.stream.name)

    return lobbies
