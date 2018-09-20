import logging
from networkx import *

# change INFO to DEBUG to output in "lobby.log" file
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

if logger.getEffectiveLevel() == logging.DEBUG:
    handler = logging.FileHandler('./lobby.log')
    formatter = logging.Formatter('%(message)s')
    handler.setFormatter(formatter)
    logger.addHandler(handler)


def lobby(G):
    """Lobby or h index
    ================
    
    All graph vertices are traversed and Lobby index is calculated and stored in the lobby macro-field.
    
    If a node has the following list of neighbors sorted by degree:

    ==========  ========
    neighbor     degree
    ==========  ========
    1          21 
    2          18 
    3           4 
    4           3 
    ==========  ========
    
    the Lobby index is 3 because degree $\leq$ neighbor_position. 
    
    """
    lobbies = {}

    logger.debug('* {}'.format(G.graph['name']))
    
    for u in G.nodes():

        logger.debug('{}\tdegree={}'.format(G.node[u]['name'], str(G.degree(u))))

        G.node[u]['Lobby'] = lobby = 1 # initialize lobby
        degs = [] # neighbors' degree

        for v in G.neighbors(u):
            degs.append(G.degree(v))
                            
        degs.sort()
        degs.reverse()
        old_idx = idx = 0
        for deg in degs:
            lobby = idx = idx + 1

            logger.debug("\t{}\t{}".format(str(idx), str(deg)))

            if (deg < idx):
                lobby = old_idx
                break
            old_idx = idx

            logger.debug("** Lobby={}".format(str(lobby)))

        G.node[u]['Lobby'] = float(lobby) / G.number_of_nodes() # normalize by N vertices
        
        lobbies[u] = G.node[u]['Lobby']

    return lobbies
            
