#!/usr/bin/env python3

import numpy as np

import matplotlib.pyplot as plt
import math
import networkx as nx
from scipy.stats import *

# LOCAL
from books import *

doing = 'assortative'
def plot(basename, xs, ys, k2knns):
        (xxs, yys) = ([], [])
        # calculate the avg of knns
        for k, knns in sorted(k2knns.items()):
                m = np.mean(np.array(knns))
                xxs.append(k)
                yys.append(m)
                print(' - ', k, m)
                
        fn = '/tmp/' + basename + '-' + doing +'-plt.png'
        f = open(fn, "w")
        
        plt.figure()
        plt.plot(xxs, yys, label='avg')
        plt.plot(xs, ys, 'ro', label=basename)
        plt.xlabel('k')
        plt.ylabel('$k_{nn}$')
        plt.grid()
        plt.title('')
        plt.legend(fontsize=7, loc='center right')
        plt.savefig(fn)
        print('Wrote', fn)

if __name__=='__main__':
        bs = Books()
        bs.read()

        for b in bs.get_books():
                k2knns = {} # map degree to average neighbor degree average
                (xs, ys) = ([], [])
                G = b.get_graph()
                H = nx.Graph()
                fn = '/tmp/' + str(G) +'-'+ doing + '-.csv'

                f = open(fn, 'w')
                
                for u in G.nodes():
                        k = G.degree(u)
                        knn = 0.0 # degree average of neighbors
                        vs = G.neighbors(u)
                        for v in vs:
                                knn += G.degree(v)

                        if len(vs) != 0:
                                knn /= len(vs)
                        else:
                                continue
                        
                        xs.append(k)
                        ys.append(knn)

                        if k not in k2knns:
                                k2knns[k] = []
                        k2knns[k].append(knn)

                        print(' + ', k, knn)
                        
                f.close()
                plot(str(G), xs, ys, k2knns)
                print('Wrote ' + fn)
                #break
        
