#!/usr/bin/python
from optparse import OptionParser
import matplotlib.pyplot as plt
import networkx as nx

# to calculate Pearson correlation
from scipy.stats.stats import pearsonr

# LOCAL
from books import *
from draw import *
from formatting import *

if __name__ == "__main__":
        """The main subroutine declares some attributes associated with the
        books. Those attributes are used to label the books and to
        standardize the pictorial elements properties like color and point
        marker in the plot."""
        books = []
        flags = 0
        
        # process command line arguments
        usage = "usage: %prog [options] arg"
        parser = OptionParser(usage)
        parser.add_option("-a", "--all",
                          help="execute all tasks",
                          action="store_true", dest="all_tasks")
        parser.add_option("-c", "--centralities",
                          help="plot the lobby and other centralities comparisons, generating PNG files",
                          action="store_true", dest="centralities")
        parser.add_option("-d", "--draw-graph",
                          help="draw the graph of characters encounters for visualization generating PNG files",
                          action="store_true", dest="draw_graph")
        parser.add_option("-g", "--global",
                          help="write global measures in a table in a LaTeX file",
                          action="store_true", dest="global_measures")
        parser.add_option("-l", "--legomena",
                          help="Write the frequency of hapax legomena, characters that "
                          +"appear only once in a table in a LaTeX file",
                          action="store_true", dest="hapax_legomena")
        parser.add_option("-s", "--stat-centralities",
                          help="generate statistics from centralities",
                          action="store_true", dest="stat")
        
        (options, args) = parser.parse_args()
        
        books = Books()
        books.read()

        tasks = {options.centralities: Plot.do_centralities,
                 options.draw_graph: Draw.do_graphs,
                 options.global_measures: Formatting.write_global_measures,
                 options.hapax_legomena: Formatting.write_hapax_legomena_table,
                 options.stat: Formatting.write_stat_centralities,}
        
        if options.all_tasks:
                funcs = array(tasks.values())
                funcs[0]
                for f in range(funcs):
                        print(f)
                        f(books)
        else:
                for opt,func in tasks.items():
                        if opt:
                                func(books)
