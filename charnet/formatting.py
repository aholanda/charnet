import os.path
import numpy as np
import logging

# LOCAL
from plot import *
from graphs import *

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Formatting:
        @staticmethod
        def write_hapax_legomena_table():
                """"Hapax Legomena The write_hapax_legomena_table() function write the
                _Hapax_ frequency to be included in the paper using LaTeX
                syntax for tables.
                """
                fn = os.path.join(Project.get_outdir(), 'legomenas.tex')

                f = open(fn, "w")
                f.write("\\begin{tabular}{@{}ccc@{}}\\toprule \n")
                f.write("\\bf Book &  $\\mathbf HL^N=H/N$ & $\\mathbf DL^N=DL/N$ \\\\ \\colrule \n")
	
	        # count the lapaxes for each book
                books = Books.get_books()
                for book in books:
                        G = book.get_graph()
                        nr_hapaxes = book.get_number_hapax_legomenas()
                        nr_dis = book.get_number_dis_legomenas()                
                        nr_chars = G.vcount()
                        
                        ln = book.get_label() + " & "
                        ln += '{0:02d}'.format(nr_hapaxes) + "/"
                        ln += '{0:02d}'.format(nr_chars) + " = "
                        ln += '{0:.3f}'.format(float(nr_hapaxes)/nr_chars) 
                        ln += ' & '
                        ln += '{0:02d}'.format(nr_dis) + "/"
                        ln += '{0:02d}'.format(nr_chars) + " = "
                        ln += '{0:.3f}'.format(float(nr_dis)/nr_chars) 
                        ln +=" \\\\\n"
                        
                        f.write(ln)

                f.write("\\botrule \\end{tabular}\n")
                f.close()
                logger.info('* Wrote {}'.format(fn))

        @staticmethod
        def write_global_measures():
                """Global measures for each character network are written as a table and
                included in a LaTeX file named `global.tex` to be included in the
                manuscript.
                Clustering coefficient is calculated using _NetworkX_ library
                [average clustering]https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.algorithms.cluster.average_clustering.html#networkx.algorithms.cluster.average_clustering
                routine.  We also calculate
                [density](https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.classes.function.density.html).
                """
                logger.info('* Writing global measures...')
        
                fn = os.path.join(Project.get_outdir(), 'global.tex')
                
                f = open(fn, "w")

                f.write('{\small\\begin{tabular}{@{}ccccccc@{}}\\toprule\n')
                f.write('\\bf\\hfil Book\\hfil '
                        + ' & \\hfil \\hphantom{00} $\\mathbf N$ \\hphantom{00} \\hfil '
                        + ' & \\hfil \\mathbf M\hfil '
                        + ' & \\hfil \\hphantom{0} $\\mathbf\langle K\rangle$ \\hphantom{0} \\hfil '
                        + ' & \\hfil \\hphantom{0} $\\mathbf D$ \\hphantom{0} \\hfil ' # Density
                        + ' & \\hfil \\hphantom{0} $\\mathbf C_c$ \\hphantom{0} \\hfil ' # Cluster. Coef.
                        + ' \\\\ \\colrule\n'
                )
                books = Books.get_books()
                for book in books:
                        G = book.get_graph()
                        G['clustering'] = Graph.transitivity_undirected(G)
                        G['density'] = Graph.density(G)
                        (deg_avg, deg_stdev) = Graphs.degree_stat(G)
                
                        # OUTPUT
                        ln = book.get_label() + ' & '
                        ln += str(G.vcount()) + ' & '
                        ln += str(G.ecount()) + ' & '
                        ln += '{0:.2f}'.format(deg_avg) + '$\\pm$' + '{0:.2f}'.format(deg_stdev) + ' & '
                        ln += '{0:.3f}'.format(book.G['density']) + ' & '
                        ln += '{0:.3f}'.format(book.G['clustering']) + ' & '
                        ln += "\\\\ \n"
                
                        f.write(ln)
                
                f.write("\\botrule\\end{tabular}}\n")        
                f.close()

                logger.info('* Wrote {}'.format(fn))

        @staticmethod
        def write_vertices_degree():
                suf = '-vertex-degree.csv'
                sep = ','

                books = Books.get_books()
                for book in books:
                        G = book.get_graph()
                        for v in G.vs:
                                G.vs[v.index]['degree'] = v.degree()

                        fn = book.get_name() + suf
                        fn = os.path.join(Project.get_outdir(), fn)
                        f = open(fn, 'w')

                        # Sort by degree in reverse order
                        vs=sorted(G.vs, key=lambda z:z['degree'], reverse=True)
                        for v in vs:
                                f.write(v['name'] + sep + '\"' + v['char_name'] + '\"'+ sep + str(v['degree']) + '\n')

                        f.close()
                        logger.info('* Wrote {}'.format(fn))                

        @staticmethod
        def write_vertices_frequency():
                suf = '-vertex-frequency.csv'
                sep = ','

                books = Books.get_books()
                for book in books:
                        G = book.get_graph()

                        fn = book.get_name() + suf
                        fn = os.path.join(Project.get_outdir(), fn) 
                        f = open(fn, 'w')
                        vs=sorted(G.vs, key=lambda z:z['frequency'], reverse=True)
                        for v in vs:
                                f.write(v['name'] + sep + '\"' + v['char_name'] + '\"'+ sep + str(v['frequency']) + '\n')

                        f.close()
                        logger.info('* Wrote {}'.format(fn))                

        @staticmethod
        def write_edges_weight():
                suf = '-edge-weight.csv'
                sep = ','
                lnk = '--'

                books = Books.get_books()
                for book in books:
                        G = book.get_graph()

                        fn = book.get_name() + suf
                        fn = os.path.join(Project.get_outdir(), fn) 
                        f = open(fn, 'w')
                        es=sorted(G.es, key=lambda z:z['weight'], reverse=True)
                        for e in es:
                                (nu, nv) = (G.vs[e.source]['char_name'], G.vs[e.target]['char_name'])
                                w = e['weight']

                                f.write(G.vs[e.source]['name'] + lnk + G.vs[e.target]['name'] + sep + '\"' + nu + '\"' + lnk + '\"' + nv + '\"' + sep + str(w) + '\n')
                        f.close()
                        logger.info('* Wrote {}'.format(fn))                

