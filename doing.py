#!/usr/bin/env python3

import matplotlib.pyplot as plt
import math
import networkx as nx
from scipy.stats import *

# LOCAL
from books import *

def plot(basename, xs, ys):
        fn = '/tmp/' + basename + '-cc-plt.png'
        f = open(fn, "w")
        
        marker_style = dict(linestyle=':', color='black', markersize=8)
        plt.plot(xs, ys,
                 label=basename,
                 alpha=0.3, 
                 **marker_style)
        
        plt.xlabel('links')
        plt.ylabel('% giant component')
        plt.grid()
        plt.title('')
        plt.legend(fontsize=7, loc='center right')
        plt.savefig(fn)
        print('Wrote', fn)

if __name__=='__main__':
        bs = Books()
        bs.read()

        for b in bs.get_books():
                (xs, ys) = ([], [])
                G = b.get_graph()
                H = nx.Graph()
                fn = '/tmp/' + str(G) + '-cc.csv'

                f = open(fn, 'w')
                
                #print(G)
                N = len(G.edges())
                maxgiant = max(nx.connected_component_subgraphs(G), key=len)
                # sort edges by weight in reverse order
                edges=sorted(G.edges(data=True), reverse=True, key=lambda t: t[2].get('weight', 1))
                for u, v, data in edges:
                        #print ('<- deg',  data['weight'])

                        H.add_edge(u, v, weight=data['weight'])
                        G.remove_edge(u, v)
                        
                        giant  = max(nx.connected_component_subgraphs(H), key=len)
                        per_links = len(H.edges()) / float(N)
                        per_gc = len(giant) / float(len(maxgiant))
                        f.write(str(per_gc) + ',' + str(per_links) + '\n')
                        xs.append(per_links)
                        ys.append(per_gc)                        
                f.close()
                plot(str(G), xs, ys)
                print('Wrote ' + fn)
                #break



                       
