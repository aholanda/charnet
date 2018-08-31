#!/usr/bin/python3

import sys
sys.path.append('/usr/local/lib/python2.7/dist-packages/')

# LOCAL
from books import *
from draw import *
from formatting import *

def run_all_tasks(books):
        i = 1
        while True:
                print(hdrs[i])
                tasks[i](books)

                i += 1
                if i == len(tasks)-1: # BUG: without this, in this way, dont stop
                        exit()

# header to tasks dictionary
tasks = [ None, # sys.argv[0] name of the program, no flag associated
          Plot.do_centralities, # -c
          Draw.do_graphs, # -g
          Formatting.write_global_measures, # -b
          Formatting.write_hapax_legomena_table, # -l
          Formatting.write_stat_centralities, # -s
          run_all_tasks] # -a
        
# headers
hdrs = ["__main__", 
        "\n\t#### TASK 1 - Plot centralities ####",
        "\n\t#### TASK 2 - Draw graph ####", 
        "\n\t#### TASK 3 - Write global measures ####", 
        "\n\t#### TASK 4 - Write the frequency of _hapax_ _legomena_ ####", 
        "\n\t#### TASK 5 - Write statistics of centralities ####", 
        "\n\t#### RUNNING ALL TASKS ####"] 

class Main:
        def __init__(self):
                print("\n\t#### PRE-PROCESSING ####")
                self.books = Books()
                self.books.read()
                
        @staticmethod
        def usage():
                print('usage: ' + sys.argv[0] + ''' [options]
                OPTIONS
                -c, --centralities 
                \tPlot the lobby and other centralities comparisons, generating PDF files.
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
        opts = [False] * len(tasks)

        # numer og arguments
        n = len(sys.argv)

        # retrieve the flags set by the user
        if n > 1:
                for i in range(1, n):
                        opt = sys.argv[i]
                        if opt == "-c" or opt == "--centralities":
                                opts[1] = True
                        elif opt == "-g" or opt == "--draw-graph":
                                opts[2] = True
                        elif opt == "-b" or opt == "--global":
                                opts[3] = True
                        elif opt == "-l" or opt == "--legomena":
                                opts[4] = True
                        elif opt == "-s" or opt == "--stat-centralities":
                                opts[5] = True
                        elif opt == "-a" or opt == "--all-tasks":
                                opts[6] = True
                                for i in range(1, n-1): # to not repeat tasks
                                        opts[i] = False
                        elif opt == "-h" or opt == "--help": # help make exit
                                Main.usage()
                        else:
                                print('Unknown OPTION:', opt)
                                Main.usage()
                                
        else:
                Main.usage()

        m = Main()
        for i in range(1, len(opts)):
                if opts[i] == True:
                        print(hdrs[i])
                        tasks[i](m.books)

