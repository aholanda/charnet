#!/usr/bin/python

import sys

# LOCAL
from books import *
from draw import *
from formatting import *

def run_all_tasks(books):
        for t in tasks:
                t(books)
        
tasks = [None, # sys.argv[0] name of the program, no flag associated
         Plot.do_centralities, # -c
         Draw.do_graphs, # -g
         Formatting.write_global_measures, # -b
         Formatting.write_hapax_legomena_table, # -l
         Formatting.write_stat_centralities, # -s
         run_all_tasks] # -a

def usage():
        print('usage: ' + sys.argv[0] + ''' [options]
        OPTIONS
        -c, --centralities 
        \tPlot the lobby and other centralities comparisons, generating PNG files.
        -g, --draw-graph
        \tDraw the graph of characters encounters for visualization generating PNG files.
        -b, --global
        \tWrite global measures in a table in a LaTeX file.
        -l, --legomena
        \tWrite the frequency of hapax legomena, characters that appear only once in a table in a LaTeX file.
        -s, --stat-centralities
        \tGenerate statistics from centralities.
        -a, --all
        \tExecute all options.
        -h, --help
        \t Print this help message.
        '''
        )
        exit()

if __name__ == "__main__":
        """The main subroutine declares some attributes associated with the
        books. Those attributes are used to label the books and to
        standardize the pictorial elements properties like color and point
        marker in the plot."""

        # Boolean array to store state of the flags 
        opts = [None] * len(tasks)

        # numer og arguments
        n = len(sys.argv)

        # retrieve the flags set by the user
        if n > 1:
                for i in range(1, n):
                        opt = sys.argv[i]
                        if opt == "-c" or opt == "--centralities":
                                opts[i] = True
                        elif opt == "-g" or opt == "--draw-graph":
                                opts[i] = True
                        elif opt == "-b" or opt == "--global":
                                opts[i] = True
                        elif opt == "-l" or opt == "--legomena":
                                opts[i] = True
                        elif opt == "-s" or opt == "--stat-centralities":
                                opts[i] = True
                        elif opt == "-a" or opt == "--all-tasks":
                                opts[i] = True
                                for i in range(1, n-2): # to not repeat tasks
                                        opts[i] = False
                        elif opt == "-h" or opt == "--help": # help make exit
                                usage()
                        else:
                                print('Unknown OPTION:', opt)
                                usage()
                                
        else:
                usage()


        books = Books()
        books.read()
        for i in range(1, n):
                if opts[i] == True:
                        tasks[i](books)

