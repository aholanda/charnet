import matplotlib.pyplot as plt
import matplotlib.pylab as pylab

from scipy.stats import pearsonr

# LOCAL
from books import *
from graphs import *

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

params = {'axes.labelsize': 'small',
          'axes.titlesize':'large',
          'xtick.labelsize':'small',
          'ytick.labelsize':'small'}
pylab.rcParams.update(params)

class Plot:
        markers = ['+', '^', 'v', 'o', 'p', 's', '.', '*', 'd']
        
        @staticmethod
        def get_color(book):
                if (book.get_category() == BookCategory.FICTION):
                        return 'red'
                elif (book.get_category() == BookCategory.BIOGRAPHY):
                        return 'blue'
                elif (book.get_category() == BookCategory.CANONICAL):
                        return 'black'
                else:
                        logger.error('Non categorized book ', book.get_name())
                        exit()

        @staticmethod
        def do_density_versus_clustering_coefficient(books):
                fn = 'Figure-Density_versus_CC.pdf'
                xs = []
                ys = []
        
                f = open(fn, "w")
                
                nms = 0 # counter for markers
                for book in books.get_books():
                        G = book.get_graph()

                        x = nx.density(G)
                        y = nx.average_clustering(G)

                        marker_style = dict(linestyle='', color=Plot.get_color(book), markersize=8)
                        plt.plot(x, y, c=Plot.get_color(book),
                                 marker=Plot.markers[nms % len(Plot.markers)],
                                 label=book.get_raw_book_label(),
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
        def do_centrality(books):
                """Centralities Lobby index centrality is calculated using function
                defined in lobby.py.  Degree, betweenness and closeness centralities
                are calculated using NetworkX. All measures are normalized.
                """
                offset_fig_nr = 1 # figure number starts after 1
                centrs = Graphs.get_centrality_names()
                
                for c in Graphs.get_centrality_names():
                        k = 0
                        fn = 'Figure-' + c + '.pdf'

                        fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8), (ax9, ax10, ax11)) = plt.subplots(nrows=4, ncols=3, sharey=True, sharex=True)
                        axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11]

                        marker_style = dict(linestyle='', markersize=3)
                        for b in books.get_books():
                                (xs, ys) = ([], [])
                                cs = []
                                
                                G = b.get_graph()
                                cs = Graphs.get_centrality_values(G, c)
                                Graphs.get_centrality_values(G, 'Lobby')
                                for u in G.nodes:
                                        xs.append(cs[u])
                                        ys.append(G.nodes[u]['Lobby'])

                                # calculate Pearson correlation
                                (r_row, p_value) = pearsonr(xs, ys)
                                
                                axes[k].set_title(b.get_name() + ' ($r=$'+'${0:.2f}'.format(r_row) +'$)', fontsize=8)
                                axes[k].set_xscale('log')
                                axes[k].set_yscale('log')
                                axes[k].plot(xs, ys,
                                             c = Plot.get_color(b),
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
                                
                                if k % 3 == 0: # if sharey fails
                                        axes[k].set_ylabel('Lobby', fontsize=8)
                                        
                                if k > 8: # if sharex fails
                                        axes[k].set_xlabel(c, fontsize=8)

                                if k==0:
                                        axes[k].legend(loc='upper right', fontsize=4)

                                k = k + 1
                                if k == 12:
                                        break

                        fig.subplots_adjust(hspace=0)
                        plt.tight_layout()
                        plt.savefig(fn)
                        logger.info('Wrote plot %s', fn)

        @staticmethod
        def do_assortativity(books):
                """Assortativity mixing is calculated and plotted versus average degree.
                """
                fn = 'Figure-Assortativity.pdf'
                xticklabels = np.arange(0, 1.1, 0.1)
                yticklabels = xticklabels

                fig, ((ax0, ax1, ax2), (ax3, ax4, ax5), (ax6, ax7, ax8), (ax9, ax10, ax11)) = plt.subplots(nrows=4, ncols=3, sharey=True, sharex=True)
                fig.subplots_adjust(hspace=.1, wspace=.1)
                axes = [ax0, ax1, ax2, ax3, ax4, ax5, ax6, ax7, ax8, ax9, ax10, ax11]

                marker_style = dict(linestyle='', markersize=4)
                k=0
                for b in books.get_books():
                        G = b.get_graph()
                        # xs (vertices), ys (degree of neighbors of xs), xs, ys_avg (avg degree of neighbors of xs)
                        (xs, ys, xxs, yavgs) = Graphs.get_degree_avg_neighbors(G)

                        axes[k].plot(xxs, yavgs, label='avg', color='black')
                        axes[k].plot(xs, ys, '.', color='gray', label=b.get_name(), **marker_style)
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

                        k = k + 1
                        if k==0:
                                axes[k].legend(loc='upper right', fontsize=4)

                        if k == 12:
                                break
                plt.savefig(fn)
                logger.info('Wrote plot %s', fn)

        @staticmethod
        def do(books):
                Plot.do_density_versus_clustering_coefficient(books)
                Plot.do_centrality(books)
                Plot.do_assortativity(books)

