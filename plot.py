import asyncio
import functools

import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

from numpy import argmax

from scipy.stats import pearsonr
import sys

# LOCAL
sys.path.append('./plfit/')
import plfit

from books import *
from graphs import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

params = {'axes.labelsize': 'small',
          'axes.titlesize':'large',
          'xtick.labelsize':'x-small',
          'ytick.labelsize':'x-small',
          'legend.fontsize':'x-small'}
pylab.rcParams.update(params)

marker_style = dict(linestyle='', markersize=3)

def plot_fill(axes, k, subtitle, xs, ys, xlabel, ylabel, color='black', loglog=True):
        axes[k].set_title(subtitle, fontsize=8)
        if loglog:
                axes[k].set_xscale('log')
                axes[k].set_yscale('log')
        axes[k].plot(xs, ys,
                          c = color,
			  marker = '.',
                          alpha=.6,
                          **marker_style)
        axes[k].grid(True)
        axes[k].text(0.5, 1.1, '' ,
                          style='italic',
                          horizontalalignment='center',
                          verticalalignment='center',
                          color='gray',
                          transform=axes[k].transAxes)
        
        multiplot_print_axis(axes, k, xlabel, 'x')
        multiplot_print_axis(axes, k, 'Lobby', 'y')

        
        if k==0:
                axes[k].legend(loc='upper right', fontsize=4)

def plot_begin():
        fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8), (ax9, ax10, ax11)) = plt.subplots(nrows=4, ncols=3, sharey=True, sharex=True)
        fig.subplots_adjust(hspace=.1, wspace=.1)
        axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11]
        
        return (fig, axes)

def multiplot_print_axis(axes, k, label, which):
        fontsz = 6
        if which is 'x':
                if k > 8:
                        axes[k].set_xlabel(label, fontsize=fontsz)
        elif which is 'y':
                if k % 3 == 0:
                        axes[k].set_ylabel(label, fontsize=fontsz)
        else:
             logger.error('Axes {} is not defined' % which)
             exit()

def plot_end(fig, fn):
        fig.subplots_adjust(hspace=0)
        plt.tight_layout()
        plt.savefig(fn)
        logger.info('Wrote plot %s', fn)

def get_empty_xy_arrays():
        return ([], [])

def plot_CDF(axes, xs, book, k, pl, **kwargs):
        a = pl._alpha
        a_str = '{0:.2f}'.format(round(a,2))
        xmin = pl._xmin

        xs = np.sort(xs)
        n=len(xs)
        xcdf = np.arange(n,0,-1,dtype='float')/float(n)

        q = xs[xs>=xmin]
        fcdf = (q/xmin)**(1-a)
        nc = xcdf[argmax(xs>=xmin)]
        fcdf_norm = nc*fcdf

        axes[k].plot(xs, xcdf, '.', label=book.get_name(), color=Plot.get_color(book), **marker_style, **kwargs)
        axes[k].plot(q, fcdf_norm, 'black', label=r'$x^{1-\alpha}, \alpha=' + a_str + '$')
        axes[k].set_xscale('log')
        axes[k].set_yscale('log')
        axes[k].legend(fontsize=4, loc='upper right')

        multiplot_print_axis(axes, k, 'k', 'x')
        multiplot_print_axis(axes, k, 'CDF', 'y')
        
class Plot:
        markers = ['+', '^', 'v', 'o', 'p', 's', '.', '*', 'd']
        
        @staticmethod
        def get_color(book):
                if (book.get_category() == BookCategory.FICTION):
                        return 'red'
                elif (book.get_category() == BookCategory.BIOGRAPHY):
                        return 'blue'
                elif (book.get_category() == BookCategory.LEGENDARY):
                        return 'green'
                else:
                        logger.error('Non categorized book ', book.get_name())
                        exit()

        @staticmethod
        def do_degree_distrib(verbose=False):
                '''Plot degree distribution for books with curve fitting made by
                plfit.
                '''
                fn = 'Figure-Degree_Distrib.pdf'

                (fig, axes) = plot_begin()

                books = Books.get_books()
                for k in range(len(books)):
                        G = books[k].get_graph()
                        degs = []
                        
                        # get the degrees
                        for n in G.nodes():
                                deg = G.degree(n)
                                if deg > 0: degs.append(deg)

                        pl = plfit.plfit(np.array(degs), usefortran=False, verbose=verbose, quiet=False)

                        plot_CDF(axes, degs, books[k], k, pl)

                plot_end(fig, fn)
                        
        @staticmethod
        def do_density_versus_clustering_coefficient():
                fn = 'Figure-Density_versus_CC.pdf'
                (xs, ys) = get_empty_xy_arrays()

                (fig, axes) = plot_begin()
                
                nms = 0 # counter for markers
                books = Books.get_books()
                for k in range(len(books)):
                        G = books[k].get_graph()

                        x = nx.density(G)
                        y = nx.average_clustering(G)

                        marker_style = dict(linestyle='', color=Plot.get_color(books[k]), markersize=6)
                        plt.plot(x, y, c=Plot.get_color(book),
                                 marker=Plot.markers[nms % len(Plot.markers)],
                                 label=books[k].get_raw_book_label(),
                                 **marker_style)

                        nms += 1 # increment no. of markers counter

                plt.ylim(-0.1,0.8)
                plt.xlabel('Density')
                plt.ylabel('Clustering coefficient')
                plt.grid()
                plt.title('')
                plt.legend(fontsize=7, loc='center right')
                plt.savefig(fn)

                logger.info('Wrote %s', fn)

        @staticmethod
        def do_centralities():
                """
                Centralities Lobby index centrality is calculated using function
                defined in lobby.py.  Degree, betweenness and closeness centralities
                are calculated using NetworkX. All measures are normalized.
                """
                offset_fig_nr = 1 # figure number starts after 1
                
                for centr_name in Graphs.get_centrality_names():
                        fn = 'Figure-' + centr_name + '.pdf'
                        
                        (fig, axes) = plot_begin()

                        books = Books.get_books()
                        for k in range(len(books)):
                                (xs, ys) = get_empty_xy_arrays()
                                centrs = []
                                
                                G = books[k].get_graph()
                                centrs = Graphs.get_centrality_values(G, centr_name)
                                Graphs.get_centrality_values(G, 'Lobby')
                                for u in G.nodes():
                                        xs.append(centrs[u])
                                        ys.append(G.node[u]['Lobby'])

                                # Calculate Pearson correlation and concatenate to graphic title
                                (r_row, p_value) = pearsonr(xs, ys)
                                title = books[k].get_name() + ' ($r=$'+'${0:.2f}'.format(r_row) +'$)'

                                plot_fill(axes, k, title, xs, ys, centr_name, 'Lobby', Plot.get_color(books[k]))

                        plot_end(fig, fn)
                                
        @staticmethod
        def do_assortativity():
                """Assortativity mixing is calculated and plotted versus average degree.
                """
                fn = 'Figure-Assortativity.pdf'
                xticklabels = np.arange(0, 1.1, 0.1)
                yticklabels = xticklabels

                (fig, axes) = plot_begin()

                books = Books.get_books()
                for k in range(len(books)):
                        G = books[k].get_graph()
                        # xs (vertices), ys (degree of neighbors of xs), xs, ys_avg (avg degree of neighbors of xs)
                        (xs, ys, xxs, yavgs) = Graphs.get_degree_avg_neighbors(G)

                        axes[k].plot(xxs, yavgs, label='avg', color='red')
                        axes[k].plot(xs, ys, '.', color='blue', label=books[k].get_name(), **marker_style)
                        axes[k].set_xlim(xticklabels[0], xticklabels[len(xticklabels)-1])
                        axes[k].set_ylim(yticklabels[0], yticklabels[len(yticklabels)-1])
                        axes[k].xaxis.set_tick_params(labelsize=6)
                        axes[k].yaxis.set_tick_params(labelsize=6)
                        axes[k].legend(fontsize='x-small')
                        axes[k].grid(True)
                        
                        if k > 8: # if sharex fails
                                axes[k].set_xlabel('$k/k_{max}$')
                                
                        if k % 3 == 0: # if sharey fails
                                axes[k].set_ylabel('$knn/knn_{max}$')
                                
                        if k==0:
                                axes[k].legend(loc='upper right', fontsize=4)

                plt.savefig(fn)
                logger.info('Wrote plot %s', fn)

        @staticmethod
        def do():
                Plot.do_degree_distrib()
                # Plot.do_density_versus_clustering_coefficient()
                # Plot.do_centralities()
                # Plot.do_assortativity()

