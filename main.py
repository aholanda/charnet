#!/usr/bin/env python3

"""Point entry of execution."""

import os.path
import sys
import logging

from charnet.draw import Draw
from charnet.formatting import Formatting
from charnet.plot import Plot
from charnet.books import Project

sys.path.append('/usr/local/lib/python2.7/dist-packages/')

logging.basicConfig(level=logging.INFO)
LOGGER = logging.getLogger(__name__)

def run_all_tasks():
    """Run all tasks available."""
    i = 1
    while True:
        print(HEADERS[i])
        TASKS[i]()
        i += 1
        if i == len(TASKS)-1: # BUG: without this, in this way, dont stop
            exit()

# header to tasks dictionary
TASKS = [None, # sys.argv[0] name of the program, no flag associated
         Plot.do_plot, # -c
         Draw.do_graphs, # -g
         Formatting.write_global_measures, # -m
         Formatting.write_hapax_legomena_table, # -l
         Formatting.write_vertices_degree, # -d
         Formatting.write_vertices_frequency, # -f
         Formatting.write_edges_weight, # -e
         run_all_tasks] # -a

# headers
HEADERS = ["__main__",
           "\n\t#### TASK 1 - Plot graphics ####",
           "\n\t#### TASK 2 - Draw graph ####",
           "\n\t#### TASK 3 - Write global measures ####",
           "\n\t#### TASK 4 - Write the frequency of _hapax_ _legomena_ ####",
           "\n\t#### TASK 5 - Write the vertices' degree ####",
           "\n\t#### TASK 6 - Write the characters' frequency ####",
           "\n\t#### TASK 7 - Write the edges' weight ####",
           "\n\t#### RUNNING ALL TASKS ####"]

def usage():
    """Write how to use the program."""
    print('* Usage: python3 ' + sys.argv[0] + ''' [options]
    OPTIONS
    -p, --plot
    \tPlot the lobby and other centralities comparisons, assortativity mixing and degree distribution with fitting.
    -g, --draw-graph
    \tDraw the graph of characters encounters for visualization generating PNG files.
    -m, --global-measures
    \tWrite global measures in a table in a LaTeX file.
    -l, --legomena
    \tWrite the frequency of hapax legomena, characters that appear only once in a table in a LaTeX file.
    -d, --degree
    \tWrite the vertices' degree in a file named \"{dir}/<book_name>-vertex-degree.csv\".
    -f, --frequency
    \tWrite the frequency of characters' appearance in a file named \"{dir}/<book_name>-vertex-frequency.csv\".
    -e, --weight
    \tWrite the weight of edges in a file named \"{dir}/<book_name>-edge-weight.csv\".
    -a, --all
    \tExecute all options.
    -o <directory>, --output-dir <directory>
    \tSet the <directory> to write the generated files. Default directory: \"{dir}\"
    -h, --help
    \t Print this help message.
    One of the flags listed above must be selected, with exception of the \"-o\" or
    \"--output-dir\" that changes the program behavior and it is optional.
    '''.format(dir=Project.get_outdir()))
    exit()
def print_out_banner(directory):
    """Print a header and write the directory where output will be send."""
    spc = '\n\n'
    line = '\t\t################################################'
    print(spc)
    print(line)
    print('\t\t  Writing output to \"{}\"  '.format(directory))
    print(line)
    print(spc)

# The main subroutine declares some attributes associated with the
# books. Those attributes are used to label the books and to
# standardize the pictorial elements properties like color and point
# marker in the plot.
if __name__ == "__main__":
    # Boolean array to store state of the flags
    OPTS = [False] * len(TASKS)
    # numer og arguments
    LEN_ARGS = len(sys.argv)
    # retrieve the flags set by the user
    if LEN_ARGS > 1:
        ARG_NO = 1
        while ARG_NO < LEN_ARGS:
            OPT = sys.argv[ARG_NO]
            # OPTIONAL
            if OPT == "-o" or OPT == "--output-dir":
                ARG_NO += 1
                if ARG_NO == LEN_ARGS:
                    usage()
                DIR = sys.argv[ARG_NO]
                DIR = DIR.rstrip('\n')
                if os.path.exists(DIR):
                    Project.set_outdir(DIR)
                else:
                    LOGGER.error(' Directory \"%s\" does not exists!', DIR)
                    exit()
            elif OPT == "-p" or OPT == "--plot":
                OPTS[1] = True
            elif OPT == "-g" or OPT == "--draw-graph":
                OPTS[2] = True
            elif OPT == "-m" or OPT == "--global-measures":
                OPTS[3] = True
            elif OPT == "-l" or OPT == "--legomena":
                OPTS[4] = True
            elif OPT == "-d" or OPT == "--degree":
                OPTS[5] = True
            elif OPT == "-f" or OPT == "--frequency":
                OPTS[6] = True
            elif OPT == "-e" or OPT == "--weight":
                OPTS[7] = True
            elif OPT == "-a" or OPT == "--all-tasks":
                OPTS[8] = True
                for ARG_NO in range(1, LEN_ARGS-1): # to not repeat tasks
                    OPTS[ARG_NO] = False
            elif OPT == "-h" or OPT == "--help": # help make exit
                usage()
            else:
                LOGGER.error('* Unknown OPTION: %s', OPT)
                usage()
            ARG_NO += 1
else:
    usage()
print_out_banner(Project.get_outdir())
for ARG_NO in range(1, len(OPTS)):
    if OPTS[ARG_NO] is True:
        LOGGER.info(HEADERS[ARG_NO])
        TASKS[ARG_NO]()
