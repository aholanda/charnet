#!/usr/bin/env python3

# THIS IS A DRAFT OF WHAT I AM CURRENTLY DOING CHANGING AND PREPARED
# TO MUTATE OR DIE

import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages/')

import numpy as np

import matplotlib.pyplot as plt
import math
import networkx as nx
from networkx.algorithms.community import girvan_newman

from scipy.stats import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LOCAL
from books import *

def get_name(G, v):
        return G.node[v]['name']

def add_degree(degs, key, val):
        if key not in degs:
                degs[key] = val
        
def how_many_nodes_intersect(G, u, v):
        vs = G.neighbors(u)
        ws = G.neighbors(v)

        inter = 0
        for v in vs:
                vstr = get_name(G, v)
                for w in ws:
                        wstr = get_name(G, w)

                        if (vstr == wstr):
                                inter += 1

        return inter
                        
if __name__=='__main__':
        books = Books()
        books.read()

        for b in books.get_books():
                accs = [0.0, 0.0]
                n = 0
                m = 0
                degs = {}
                G = b.get_graph()
                name = b.get_name()
                print(name)

                for u in G.nodes():
                        n += 1
                        add_degree(degs, u, G.degree(u)) 
                        vs = G.neighbors(u)

                        for v in vs:
                                m += 1
                                add_degree(degs, v, G.degree(v))
                                union = degs[u] + degs[v]
                                inter = how_many_nodes_intersect(G, u, v)

                                j = float(inter) / float(union)
                                accs[0] += j

                                if (inter > 0):
                                        accs[1] += 1 / float(inter)
                                
                                #print("o J(%s[%d],%s[%d)]=%f"% (get_name(G,u), u , get_name(G, v), v, j))
                print("%s=(%f,%f)" % (name,accs[0]/(m+n), accs[1]/(m+n)))

# def plot(ys, book_name, ylabel):
#         fn = '/tmp/' + book_name + '-' + ylabel + '-plot.png'
#         plt.figure()
#         plt.xscale('log')
#         if ylabel != 'Eigenvector' and ylabel != 'Closeness':
#                 plt.yscale('log')
#         #plt.ylim(0.0, 1.0)
#         plt.plot(ys, 'bv')
#         plt.xlabel('index')
#         plt.ylabel(ylabel)
#         plt.title(book_name.title())
#         plt.savefig(fn)
#         logger.info('Wrote %s', fn)

# # plot every centrality value        
# if __name__=='__main__':
#         books = Books().get_books()
#         centrs = Graphs.get_centrality_names()

#         for c in centrs:
#                 for b in books:
#                         vals = []
#                         fn = '/tmp/' + b.get_name() + '-' + c + '.csv'
#                         f = open(fn)
#                         for ln in f:
#                                 (key, val) = ln.rstrip("\n").split(',')
#                                 if float(val) > 0.0:
#                                         vals.append(float(val))

#                         vals = sorted(vals, reverse=True)

#                         plot(vals, b.get_name(), c)

        
# # pop vertex with higher centrality value at each iteration
# if __name__=='__main__':
#         books = Books()
#         books.read()

#         for b in books.get_books():
#                 G = b.get_graph()
#                 name = b.get_name()
#                 ys = []

#                 cs = nx.degree_centrality(G)
#                 cs = sorted(cs.items(), key=lambda x: x[1])
#                 while (len(cs) != 0 ):
#                         c = cs.pop()[1]
#                         if c > 0.0:
#                                 ys.append(c)

#                 plot(name, ys)


## get the communities using Girvan-Newman algorithm                
# if __name__=='__main__':
#         books = Books()
#         books.read()

#         for b in books.get_books():
#                 G = b.get_graph()
#                 name = b.get_name()

#                 comp = girvan_newman(G)

#                 print(name)
#                 print(tuple(sorted(c) for c in next(comp)))


                
        
# if __name__=='__main__':
#         books = Books()
        
#         for b in books.get_books():
#                 name = b.get_name()
#                 (xs, ys) = ([], [])
#                 fn = '/tmp/' + name + '-VE-growth.csv'
#                 f = open(fn)

#                 for ln in f:
#                         (v, e) = ln.rstrip("\n").split(',')
#                         xs.append(int(v))
#                         ys.append(int(e))
#                 plot(name, xs, ys)
                        
# if __name__=='__main__':
#         books = Books()
#         books.read()
        
#         for b in books.get_books():
#                 G = b.get_graph()
#                 name = b.get_name()
#                 d2n = {}
#                 (xs, ys) = ([], [])
#                 acc = 0.0

#                 for v in G.nodes():
#                         d = G.degree(v)

#                         if d in d2n:
#                                 d2n[d] += 1
#                         else:
#                                 d2n[d] = 1

#                 d2n = dict(sorted(d2n.items(), reverse=True))
#                 for d,n in d2n.items():
#                         acc = acc + n/G.number_of_nodes()
#                         print(d, acc)
#                         xs.append(d)
#                         ys.append(acc)

#                 plot(xs, ys, name)
        

# doing = 'assortative'
# def plot(basename, xs, ys, k2knns):
#         (xxs, yys) = ([], [])
#         # calculate the avg of knns
#         for k, knns in sorted(k2knns.items()):
#                 m = np.mean(np.array(knns))
#                 xxs.append(k)
#                 yys.append(m)
#                 print(' - ', k, m)
                
#         fn = '/tmp/' + basename + '-' + doing +'-plt.png'
#         f = open(fn, "w")
        
#         plt.figure()
#         plt.plot(xxs, yys, label='avg')
#         plt.plot(xs, ys, 'ro', label=basename)
#         plt.xlabel('k')
#         plt.ylabel('$k_{nn}$')
#         plt.grid()
#         plt.title('')
#         plt.legend(fontsize=7, loc='center right')
#         plt.savefig(fn)
#         print('Wrote', fn)

# if __name__=='__main__':
#         bs = Books()
#         bs.read()

#         for b in bs.get_books():
#                 k2knns = {} # map degree to average neighbor degree average
#                 (xs, ys) = ([], [])
#                 G = b.get_graph()
#                 H = nx.Graph()
#                 fn = '/tmp/' + str(G) +'-'+ doing + '-.csv'

#                 f = open(fn, 'w')
                
#                 for u in G.nodes():
#                         k = G.degree(u)
#                         knn = 0.0 # degree average of neighbors
#                         vs = G.neighbors(u)
#                         for v in vs:
#                                 knn += G.degree(v)

#                         if len(vs) != 0:
#                                 knn /= len(vs)
#                         else:
#                                 continue
                        
#                         xs.append(k)
#                         ys.append(knn)

#                         if k not in k2knns:
#                                 k2knns[k] = []
#                         k2knns[k].append(knn)

#                         print(' + ', k, knn)
                        
#                 f.close()
#                 plot(str(G), xs, ys, k2knns)
#                 print('Wrote ' + fn)
#                 #break
        
# def connected_components():
        
# def plot(basename, xs, ys):
#         fn = '/tmp/' + basename + '-cc-plt.png'
#         f = open(fn, "w")
        
#         marker_style = dict(linestyle=':', color='black', markersize=8)
#         plt.figure()
#         plt.plot(xs, ys,
#                  label=basename,
#                  alpha=0.3, 
#                  **marker_style)
        
#         plt.xlabel('links')
#         plt.ylabel('% giant component')
#         plt.grid()
#         plt.title('')
#         plt.legend(fontsize=7, loc='center right')
#         plt.savefig(fn)
#         print('Wrote', fn)

# if __name__=='__main__':
#         bs = Books()
#         bs.read()

#         for b in bs.get_books():
#                 (xs, ys) = ([], [])
#                 G = b.get_graph()
#                 H = nx.Graph()
#                 fn = '/tmp/' + str(G) + '-cc.csv'

#                 f = open(fn, 'w')
                
#                 #print(G)
#                 N = len(G.edges())
#                 maxgiant = max(nx.connected_component_subgraphs(G), key=len)
#                 # sort edges by weight in reverse order
#                 edges=sorted(G.edges(data=True), reverse=True, key=lambda t: t[2].get('weight', 1))
#                 for u, v, data in edges:
#                         #print ('<- deg',  data['weight'])

#                         H.add_edge(u, v, weight=data['weight'])
#                         G.remove_edge(u, v)
                        
#                         giant  = max(nx.connected_component_subgraphs(H), key=len)
#                         per_links = len(H.edges()) / float(N)
#                         per_gc = len(giant) / float(N) # float(len(maxgiant))
#                         f.write(str(per_gc) + ',' + str(per_links) + '\n')
#                         xs.append(per_links)
#                         ys.append(per_gc)                        
#                 f.close()
#                 plot(str(G), xs, ys)
#                 print('Wrote ' + fn)
#                 #break
