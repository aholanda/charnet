import os.path
import numpy as np
import logging
import networkx as nx

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
                        nr_chars = G.number_of_nodes()
                        
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
                        G.graph['clustering'] = nx.average_clustering(G)
                        G.graph['density'] = nx.density(G)
                        (deg_avg, deg_stdev) = Graphs.degree_stat(G)
                
                        # OUTPUT
                        ln = book.get_label() + ' & '
                        ln += str(G.number_of_nodes()) + ' & '
                        ln += str(G.number_of_edges()) + ' & '
                        ln += '{0:.2f}'.format(deg_avg) + '$\\pm$' + '{0:.2f}'.format(deg_stdev) + ' & '
                        ln += '{0:.3f}'.format(book.G.graph['density']) + ' & '
                        ln += '{0:.3f}'.format(book.G.graph['clustering']) + ' & '
                        ln += "\\\\ \n"
                
                        f.write(ln)
                
                f.write("\\botrule\\end{tabular}}\n")        
                f.close()

                logger.info('* Wrote {}'.format(fn))

                Plot.do_density_versus_clustering_coefficient()

        @staticmethod
        def write_stat_centralities():
                """
                Calculate the mean and deviation for centralities for each book.
                """
                fn = os.path.join(Project.get_outdir(), 'centr.tex')
                f = open(fn, "w")

                centrs = ['Degree', 'Betweenness', 'Closeness', 'Assortativity', 'Lobby']

                Books.pre_process_centralities()

                f.write("{\small\\begin{tabular}{@{}cccccc@{}}\\toprule\n")
                f.write("\\bf Book &\\bf Degree &\\bf Betweenness &\\bf Closeness &\\bf Assortativity &\\bf Lobby \\\ \\colrule \n");
                books = Books.get_books()
                for book in books:
                        f.write(book.get_label() + ' & ')
                        G = book.get_graph()
                        for centr in centrs:
                                vals = []

                                if centr == 'Assortativity':
                                        f.write('${0:.3f}'.format(nx.degree_assortativity_coefficient(G)) +'$ & ')
                                        continue
                                
                                for v in G.nodes():
                                        vals.append(G.node[v][centr])

                                m = np.mean(np.array(vals))
                                std = np.std(np.array(vals))
                                f.write('${0:.3f}'.format(m) + ' \pm ' '{0:.3f}'.format(std) + '$ ')
                                if centr != 'Lobby':
                                        f.write(' & ')
                                else:
                                        f.write(' \\\ ')
                                        if book.get_name() == 'tolkien' and centr == 'Lobby':
                                                f.write(' \\botrule')
                        f.write('\n')
                f.write('\\end{tabular}}\n')
                logger.info('* Wrote {}'.format(fn))
                f.close()

        @staticmethod
        def write_vertices_degree():
                suf = '-vertex-degree.csv'
                sep = ','

                books = Books.get_books()
                for book in books:
                        G = book.get_graph()

                        for v in G.nodes():
                                G.node[v]['degree'] = G.degree(v)

                        fn = book.get_name() + suf
                        fn = os.path.join(Project.get_outdir(), fn)
                        f = open(fn, 'w')
                        for v, data in sorted(G.nodes(data=True), reverse=True, key=lambda x: x[1]['degree']):
                                f.write(v + sep + '\"' + data['name'] + '\"'+ sep + str(data['degree']) + '\n')

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
                        for v, data in sorted(G.nodes(data=True), reverse=True, key=lambda x: x[1]['frequency']):
                                f.write(v + sep + '\"' + data['name'] + '\"'+ sep + str(data['frequency']) + '\n')

                        f.close()
                        logger.info('* Wrote {}'.format(fn))                
