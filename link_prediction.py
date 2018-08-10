#!/usr/bin/env python3
import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages/')

import networkx as nx

from random import seed
from random import randint

from books import *

LNK_STR = '-'

def _str(u, v):
        str(u) + LNK_STR + str(v) 

def map_existing_links(G):
        '''Return a dictionary with the existing edges in the form u-v, e.g
1-2, as keys and a boolean as value.
        '''
        el = {}
        for u,v in G.edges():
                l = _str(u, v)
                el[l] = True
                
        return el

def map_non_existing_links(G, el):
        '''Return a dictionary with the existing edges in the form u-v, e.g
1-2, as keys and a boolean as value.
        '''
        nel = {}
        n = G.number_of_nodes()

        for u in range(n):
                for v in range(n):
                        l = _str(u, v)
                        if l not in el:
                                nel[l] = True

        return nel

def create_missing_links(G, H, p):
        assert p > 0.0
        assert p < 1.0
        N = G.number_of_edges()

        # seed random number generator
        seed(1)
        
        # remove links from graph H to simulate missing links in a to
        # desired percentage p
        while ( float(H.number_of_edges()) / float( N ) < (1 - p) ):

                # the interval to pick a link
                i = randint(0, len(el) - 1)
                
                # the keys are sorted lexicographically only to
                # establish a pattern of sequence to pick a link
                n = 0
                for k,_ in sorted(el.items()):
                     if i == n:
                             ml[k] = True
                             del el[k]
                             break
                     n += 1
                        
if __name__ == '__main__':
        books = Books()
        books.read()

        b = books.get_books()[0]

        G = b.get_graph()
        H = G.clone()

        H = create_missing_links(G, H, p)
        
        el = map_existing_links(G)
        nel = map_non_existing_links(G, el)
        
