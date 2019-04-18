import os.path
import numpy as np
import operator

import graph_tool as gt
import graph_tool.clustering as gt_cluster

# LOCAL
from plot import *
from graphs import *

class Formatting:
        @staticmethod
        def write_hapax_legomena_table(abs=False, dis=False):
                """"Hapax Legomena The write_hapax_legomena_table() function write the
                    _Hapax_ frequency to be included in the paper using LaTeX
                    syntax for tables.
                Arguments:
                  abs (Boolean): if true, print out absolute values over the number of characters;
                  dis (Boolean): if true, print out Hapax DisLegomena that are the number of
                     characters that appear twice.
                """
                n2h = {} # map book name to hapax
                n2b = {} # map book name to book object
                tbl = "" # store table content string
                # Sort books by hapax
                books = Books.get_books()
                for book in books:
                        n = book.get_name()
                        G = book.get_graph()
                        n2h[n] = float(book.get_number_hapax_legomenas()) / Graphs.size(G)
                        n2b[n] = book

                fn = os.path.join(Project.get_outdir(), 'legomenas.tex')
                f = open(fn, "w")

                for n in Books.get_genre_enums():
                        tbl += '\t\\begin{minipage}{.3\\textwidth}\\centering\n'
                        tbl += '\t\t\\caption*{' + Books.get_genre_name(n) +'}\\\\ \\smallskip\n'
                        tbl += '\t\t\\begin{tabular}{@{}p{1.65cm}p{1cm}@{}}\\toprule\n'
                        tbl += '\t\t\\bf book  & $\\mathbf{HL}$\\\\ \\colrule\n'

                        n2h_lst = sorted(n2h.items(), key=operator.itemgetter(1), reverse=True)
                        for bname, hap in n2h_lst:
                                book = n2b[bname]
                                enum = book.get_genre()
                                if enum.value == n:
                                        nr_hap = book.get_number_hapax_legomenas()
                                        nr_chars = Graphs.size(book.get_graph())
                                        tbl += '\t\t\t' + book.get_label() + ' & '
                                        tbl += '{0:.2f}'.format(float(nr_hap)/nr_chars)
                                        tbl += ' \\\\ \n'
                        tbl += '\t\t\\botrule \\end{tabular}\n'
                        tbl += '\t\end{minipage}\n'

                f.write(tbl)
                f.close()
                print('* Wrote {}'.format(fn))

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

                f.write('''
                {\small \\begin{tabular}{@{}cccccccc@{}}\\toprule
                \hfil \\bf genre \hfil
                & \\bf \hfil book \hfil
                & \hfil\hphantom{00} $\mathbf n$ \hphantom{00}\hfil
                & \hfil $\mathbf m$\hfil
                & \hfil\hphantom{0} $\mathbf\\langle k\\rangle$\hphantom{0} \hfil
                & \hfil\hphantom{0} $\mathbf \rho$ \hphantom{0}\hfil
                & \hfil\hphantom{0} $\mathbf c$\hphantom{0}\hfil \\\\ \n''')

                for n in Books.get_genre_enums():
                        ln = '\t\t\\colrule\\multirow{4}{*}{'+ Books.get_genre_name(n)  + '}' + '\n'

                        books = Books.get_books()
                        for book in books:
                                enum = book.get_genre()
                                if enum.value == n:
                                        G = book.get_graph()
                                        CC,_ = gt_cluster.global_clustering(G)
                                        D = Graphs.density(G)
                                        (deg_avg, deg_stdev) = Graphs.degree_stat(G)

                                        # OUTPUT
                                        ln += '\t\t\t&\emph{' + book.get_label() + '} & '
                                        ln += str(len(list(G.vertices()))) + ' & '
                                        ln += str(len(list(G.edges()))) + ' & '
                                        ln += '{0:.2f}'.format(deg_avg) + '$\\pm$' + '{0:.2f}'.format(deg_stdev) + ' & '
                                        ln += '{0:.3f}'.format(D) + ' & '
                                        ln += '{0:.3f}'.format(CC) + ' & '
                                        ln += "\\\\ \n"
                        f.write(ln)

                f.write("\t\t\\botrule\\end{tabular}}\n")

                f.close()
                logger.info('* Wrote {}'.format(fn))

        @staticmethod
        def write_vertices_degree():
                suf = '-vertex-degree.csv'
                sep = ','

                books = Books.get_books()
                for book in books:
                        degs = {}
                        char_names = {}
                        G = book.get_graph()
                        for v in G.vertices():
                                lab = G.vertex_properties["label"][v]
                                degs[lab] = v.out_degree()
                                char_names[lab] = G.vertex_properties["char_name"][v]

                        fn = book.get_name() + suf
                        fn = os.path.join(Project.get_outdir(), fn)
                        f = open(fn, 'w')

                        # Sort by degree in reverse order
                        labs=sorted(degs.items(), key=lambda x: x[1], reverse=True)
                        for lab, deg in labs:
                                f.write(lab + sep + '\"'
                                        + char_names[lab] + '\"'
                                        + sep + str(deg) + '\n')

                        f.close()
                        logger.info('* Wrote {}'.format(fn))

        @staticmethod
        def write_vertices_frequency():
                suf = '-vertex-frequency.csv'
                sep = ','

                books = Books.get_books()
                for book in books:
                        freqs = {}
                        char_names = {}
                        G = book.get_graph()

                        fn = book.get_name() + suf
                        fn = os.path.join(Project.get_outdir(), fn)
                        f = open(fn, 'w')

                        for v in G.vertices():
                                lab = G.vertex_properties["label"][v]
                                freqs[lab] = G.vertex_properties["frequency"][v]
                                char_names[lab] = G.vertex_properties["char_name"][v]

                        labs=sorted(freqs.items(), key=lambda x: x[1], reverse=True)
                        for lab, freq in labs:
                                f.write(lab + sep + '\"' + char_names[lab] + '\"'+ sep + str(freq) + '\n')

                        f.close()
                        logger.info('* Wrote {}'.format(fn))

        @staticmethod
        def write_edges_weight():
                suf = '-edge-weight.csv'
                sep = ','
                lnk = '--'

                books = Books.get_books()
                for book in books:
                        ws = {}
                        char_names = {}
                        G = book.get_graph()

                        fn = book.get_name() + suf
                        fn = os.path.join(Project.get_outdir(), fn)
                        f = open(fn, 'w')

                        for e in G.edges():
                                u = e.source()
                                v = e.target()
                                lab = G.vertex_properties["label"][u] + lnk + G.vertex_properties["label"][v]
                                ws[lab] = G.edge_properties["weight"][e]
                                char_names[lab] = '\"' + G.vertex_properties["char_name"][u] + '\"' + lnk \
                                                  + '\"' + G.vertex_properties["char_name"][v] + '\"'

                        labs=sorted(ws.items(), key=lambda x: x[1], reverse=True)
                        for lab,w in labs:
                                f.write(lab + sep + char_names[lab] + sep + str(w) + '\n')
                        f.close()
                        logger.info('* Wrote {}'.format(fn))
