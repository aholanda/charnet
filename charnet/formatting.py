"""This module contains instructions to produce output in LaTeX."""

import os.path
import operator

import graph_tool.clustering as gt_cluster

# LOCAL
from charnet.graphs import Graphs
from charnet.books import Project
from charnet.books import Books

class Formatting(object):
    """Main class to format output."""
    suppl_f = None # file to write supplementary material

    def __init__(self):
        pass

    @staticmethod
    def write_hapax_legomena_table():
        """"Hapax Legomena: write_hapax_legomena_table() function write the
            _Hapax_ frequency to be included in the paper using LaTeX
            syntax for tables.
         """
        n2h = {} # map book name to hapax
        n2b = {} # map book name to book object
        tbl = "" # store table content string
        # Sort books by hapax
        books = Books.get_books()
        for book in books:
            name = book.get_name()
            graph = book.get_graph()
            n2h[name] = float(book.get_number_hapax_legomenas()) / Graphs.size(graph)
            n2b[name] = book

        file_name = os.path.join(Project.get_outdir(), 'legomenas.tex')
        _file = open(file_name, "w")

        for name in Books.get_genre_enums():
            tbl += '\t\\begin{minipage}{.3\\textwidth}\\centering\n'
            tbl += '\t\t\\caption*{' + Books.get_genre_name(name) +'}\\\\ \\smallskip\n'
            tbl += '\t\t\\begin{tabular}{@{}p{1.65cm}p{1cm}@{}}\\toprule\n'
            tbl += '\t\t\\bf book  & $\\mathbf{HL}$\\\\ \\colrule\n'
            n2h_lst = sorted(n2h.items(), key=operator.itemgetter(1), reverse=True)
            for bname, _ in n2h_lst:
                book = n2b[bname]
                enum = book.get_genre()
                if enum.value == name:
                    nr_hap = book.get_number_hapax_legomenas()
                    nr_chars = Graphs.size(book.get_graph())
                    tbl += '\t\t\t' + book.get_label() + ' & '
                    tbl += '{0:.2f}'.format(float(nr_hap)/nr_chars)
                    tbl += ' \\\\ \n'
            tbl += '\t\t\\botrule \\end{tabular}\n'
            tbl += '\t\\end{minipage}\n'

        _file.write(tbl)
        _file.close()
        print ('* Wrote ' + file_name)

    @staticmethod
    def write_global_measures():
        """Global measures for each character network are written as a table and
            included in a LaTeX file named `global.tex` to be included in the
            manuscript.
        """
        file_name = os.path.join(Project.get_outdir(), 'global.tex')

        _file = open(file_name, "w")

        _file.write('''
        {\\small \\begin{tabular}{@{}cccccccc@{}}\\toprule
        \\hfil \\bf genre \\hfil
        & \\bf \\hfil book \\hfil
        & \\hfil\\hphantom{00} $\\mathbf n$ \\hphantom{00}\\hfil
        & \\hfil $\\mathbf m$\\hfil
        & \\hfil\\hphantom{0} $\\mathbf\\langle k\\rangle$\\hphantom{0} \\hfil
        & \\hfil\\hphantom{0} $\\mathbf \\rho$ \\hphantom{0}\\hfil
        & \\hfil\\hphantom{0} $\\mathbf c$\\hphantom{0}\\hfil \\\\ \n''')

        for _id in Books.get_genre_enums():
            line = '\t\t\\colrule\\multirow{4}{*}{'+ Books.get_genre_name(_id)  + '}' + '\n'
            books = Books.get_books()
            for book in books:
                enum = book.get_genre()
                if enum.value == _id:
                    graph = book.get_graph()
                    clustering_coeff, _ = gt_cluster.global_clustering(graph)
                    density = Graphs.density(graph)
                    (deg_avg, deg_stdev) = Graphs.degree_stat(graph)
                    # OUTPUT
                    line += '\t\t\t&\\emph{' + book.get_label() + '} & '
                    line += str(len(list(graph.vertices()))) + ' & '
                    line += str(len(list(graph.edges()))) + ' & '
                    line += '{0:.2f}'.format(deg_avg) + '$\\pm$'
                    line += '{0:.2f}'.format(deg_stdev) + ' & '
                    line += '{0:.3f}'.format(density) + ' & '
                    line += '{0:.3f}'.format(clustering_coeff) + ' & '
                    line += "\\\\ \n"
            _file.write(line)
        _file.write("\t\t\\botrule\\end{tabular}}\n")

        _file.close()
        print ('* Wrote ' + file_name)

    @staticmethod
    def write_vertices_degree():
        """Write the degree of the vertices of a graph to output."""
        suf = '-vertex-degree.csv'
        sep = ','

        books = Books.get_books()
        for book in books:
            degs = {}
            char_names = {}
            graph = book.get_graph()
            for vert in graph.vertices():
                lab = graph.vertex_properties["label"][vert]
                degs[lab] = vert.out_degree()
                char_names[lab] = graph.vertex_properties["char_name"][vert]
            file_name = book.get_name() + suf
            file_name = os.path.join(Project.get_outdir(), file_name)
            _file = open(file_name, 'w')
            # Sort by degree in reverse order
            labs = sorted(degs.items(), key=lambda x: x[1], reverse=True)
            for lab, deg in labs:
                _file.write(lab + sep + '\"'
                            + char_names[lab] + '\"'
                            + sep + str(deg) + '\n')
            _file.close()
            print ('* Wrote ' + file_name)

    @staticmethod
    def write_vertices_frequency():
        """Write the frequency of vertices to output."""
        suf = '-vertex-frequency.csv'
        sep = ','
        books = Books.get_books()
        for book in books:
            freqs = {}
            char_names = {}
            graph = book.get_graph()
            file_name = book.get_name() + suf
            file_name = os.path.join(Project.get_outdir(), file_name)
            _file = open(file_name, 'w')
            for vert in graph.vertices():
                lab = graph.vertex_properties["label"][vert]
                freqs[lab] = graph.vertex_properties["frequency"][vert]
                char_names[lab] = graph.vertex_properties["char_name"][vert]
            labs = sorted(freqs.items(), key=lambda x: x[1], reverse=True)
            for lab, freq in labs:
                _file.write(lab + sep + '\"' + char_names[lab] + '\"'+ sep + str(freq) + '\n')
            _file.close()
            print ('* Wrote ' + file_name)

    @staticmethod
    def write_edges_weight():
        """Write the weight of edges to output."""
        suf = '-edge-weight.csv'
        sep = ','
        lnk = '--'
        books = Books.get_books()
        for book in books:
            weights = {}
            char_names = {}
            graph = book.get_graph()
            file_name = book.get_name() + suf
            file_name = os.path.join(Project.get_outdir(), file_name)
            _file = open(file_name, 'w')
            for edge in graph.edges():
                src = edge.source()
                dest = edge.target()
                lab = graph.vertex_properties["label"][src]
                lab += lnk + graph.vertex_properties["label"][dest]
                weights[lab] = graph.edge_properties["weight"][edge]
                char_names[lab] = '\"' + graph.vertex_properties["char_name"][src] + '\"' + lnk \
                                  + '\"' + graph.vertex_properties["char_name"][dest] + '\"'
            labs = sorted(weights.items(), key=lambda x: x[1], reverse=True)
            for lab, weight in labs:
                _file.write(lab + sep + char_names[lab] + sep + str(weight) + '\n')
            _file.close()
            print ('* Wrote ' + file_name)

    @staticmethod
    def couro_write_suppl(filename):
        """Write supplementary material like p-values to output.
        Here we use couroutines to receive values from parser."""
        xlbl = '' # x label
        ylbl = '' # y label
        file_name = os.path.join('preprint/', filename + '.tex')
        _file = open(file_name, 'w')
        _file.write('\\pagebreak\\section*{Supplementary Material}\n')
        while True:
            (key, content) = yield # receive the message as a tuple
            if key == 'begin_table':
                _file.write('\\begin{table}[ht]\n')
                _file.write('\t\\begin{center} \n')
                _file.write('\t\\tbl{' + content + ' $p$-values.}\n')
                _file.write('{') # OPEN BRACKET
            elif key == 'begin_subtable':
                _file.write('\\begin{minipage}{' + content + '\\textwidth}\n')
            elif key == 'xlabel':
                xlbl = content
            elif key == 'ylabel':
                ylbl = content
                _file.write('\\hspace{.7cm}\\hbox{' + xlbl + '$\\times$' + ylbl +
                            '} \\par \\smallskip\n')
            elif key == 'begin_data':
                _file.write('\t\\begin{tabular}{@{}p{1.6cm}p{1.3cm}@{}} \\toprule \n')
                _file.write('\t\t\\bf book & $\\mathbf p$ \\\\ \\colrule \n')
            elif key == 'book_name':
                _file.write('\t\t' + content + ' & ')
            elif key == 'pvalue':
                _file.write(content + ' \\\\ \n')
            elif key == 'end_subtable':
                _file.write('\\end{minipage}\n')
            elif key == 'end_data':
                _file.write('\t\\botrule\\end{tabular}')
            elif key == 'end_table':
                _file.write('\n}\n') # CLOSE BRACKET
                _file.write('\t\\end{center}\n')
                _file.write('\\end{table}\n')
            elif key == 'CLOSE_FILE':
                _file.close()
                print ('* Wrote ' + file_name)
            else:
                print ('\n******** ERROR: wrong key: '+ key +' ********')
                exit()
