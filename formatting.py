import networkx as nx
import numpy as np

# LOCAL
from plot import *
from graphs import *

class Formatting:
        @staticmethod
        def write_hapax_legomena_table(books):
                """"Hapax Legomena The write_hapax_legomena_table() function write the
                _Hapax_ frequency to be included in the paper using LaTeX
                syntax for tables.
                """
                fn = 'legomenas.tex'

                f = open(fn, "w")
                f.write("\\begin{tabular}{@{}ccc@{}}\\toprule \n")
                f.write("\\bf Book &  $\\mathbf HL^N=H/N$ & $\\mathbf DL^N=DL/N$ \\\\ \\colrule \n")
	
	        # count the lapaxes for each book
                for book in books.get_books():
                        nr_hapaxes = book.get_number_hapax_legomenas()
                        nr_dis = book.get_number_dis_legomenas()                
                        nr_chars = book.get_number_characters()
                        
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
                print('Wrote',fn)

        @staticmethod
        def write_global_measures(books):
                """Global measures for each character network are written as a table and
                included in a LaTeX file named `global.tex` to be included in the
                manuscript.
                Clustering coefficient is calculated using _NetworkX_ library
                [average clustering]https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.algorithms.cluster.average_clustering.html#networkx.algorithms.cluster.average_clustering
                routine.  We also calculate
                [density](https://networkx.github.io/documentation/networkx-1.9/reference/generated/networkx.classes.function.density.html).
                """
                print('Writing global measures...')
        
                fn = 'global.tex'
                
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
                for book in books.get_books():
                        G = book.G
                        G.graph['clustering'] = nx.average_clustering(book.G)
                        G.graph['density'] = nx.density(book.G)

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

                print('Wrote %s'% fn)

                Plot.do_density_versus_clustering_coefficient(books)

        @staticmethod
        def write_stat_centralities(books):
                """
                Calculate the mean and deviation for centralities for each book.
                """
                fn = 'centr.tex'
                f = open(fn, "w")

                centrs = ['Degree', 'Betweenness', 'Closeness', 'Assortativity', 'Lobby']

                Graphs.pre_process_centralities(books)

                f.write("{\small\\begin{tabular}{@{}cccccc@{}}\\toprule\n")
                f.write("\\bf Book &\\bf Degree &\\bf Betweenness &\\bf Closeness &\\bf Assortativity &\\bf Lobby \\\ \\colrule \n");
                for book in books.get_books():
                        f.write(book.get_label() + ' & ')
                        G = book.G
                        for centr in centrs:
                                vals = []

                                if centr == 'Assortativity':
                                        f.write('${0:.3f}'.format(nx.degree_assortativity_coefficient(G)) +'$ & ')
                                        continue
                                
                                for i in range(G.number_of_nodes()):
                                        vals.append(G.node[i][centr])

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
                print('Wrote', fn)
                f.close()
