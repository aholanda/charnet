from jinja2 import Environment, FileSystemLoader
import os
import numpy as np
from scipy.stats import pearsonr
from scipy.optimize import curve_fit

import graph_tool as gt
import graph_tool.clustering as gt_cluster

from books import *

SEP = '_'

def dump_book_data(xlabel, ylabel, book_name, extension, xs, ys, xxs=None, yys=None, append=False):
        ''''Dump data to output file. 
            When append is not False means unique plot with labels as markers.'''
        assert(len(xs) == len(ys))
        (_xs, _ys) = ([], [])
        label = ''
        mode = 'w'
        mode_str = 'Wrote'
        _book_name = SEP + book_name
        
        
        if append == True:
                mode = 'a'
                mode_str = 'Append'
                _book_name = ''

        fn = os.path.join(Project.get_outdir(), xlabel + SEP + ylabel + _book_name + extension)
        f = open(fn, mode)
        for i in range(len(xs)):
                if math.isnan(xs[i]) or math.isnan(ys[i]):
                        continue

                ln = '\n'
                if xxs and yys:
                        if i < len(xxs):
                                ln = '\t' + str(xxs[i]) + '\t' + str(yys[i]) + '\n'

                # sorry, but \lblfmt is defined in templates/settings.gp
                if append == True:
                        label = '"\\\\tiny ' + book_name + '"\t'
                                
                ln = label + str(xs[i]) + '\t' + str(ys[i]) + ln
                f.write(ln)
                _xs.append(xs[i])
                _ys.append(ys[i])
        f.close()
        print('* {} {}; '.format(mode_str, fn), end='', flush=True)
        return _xs, _ys, fn

class datainfo:
        def __init__(self, title, filename, rvalue=0.0, ptest=0.0, slope=0.0, intercept=0.0, xrange_=None):
                self.title = title
                self.filename = filename
                self.rvalue = rvalue
                self.ptest = ptest
                self.slope = slope
                self.intercept = intercept

class plotinfo:
        def __init__(self, title, xlabel, ylabel, datainfos=None):
                self.title = title
                self.xlabel = xlabel
                self.ylabel = ylabel
                if datainfos == None:
                        self.datainfos = []
def linear_func(x, a, b):
        return x*a + b

def test_ceil(xs, ys, xmax, ymax):
        if np.max(xs) > xmax or np.max(ys) > ymax:
                print(np.max(xs), np.max(ys))
                print('ERROR max value {%1.2f}/{%1.2f},{%1.2f}/{%1.2f} ignored'.format(np.max(xy), xmax, np.max(ys), ymax))
                exit(-1)

class Plot:
        # plot command prefix
        CMD = 'cd preprint && gnuplot '        
        # plot figure extension
        EXT = '.tex'
        # gnuplot extension
        PLT_EXT = '.gp'
        # data file extension
        DATA_EXT = '.dat'
        # gnuplot common settings
        GP_SET_PATH = os.path.join(Project.get_outdir(), 'settings.gp')
        # Graphs
        GS = []
        #
        BOOKS = []
        
        @staticmethod
        def init():
                tmpdir = Project.get_outdir()
                '''Initialize graphs.'''
                Plot.BOOKS = Books.get_books()
                for book in Plot.BOOKS:
                        G = book.get_graph()
                        Plot.GS.append(G)

                cmd = 'rm -f {}/*{} {}/*{} {}/*{}'.format(tmpdir, Plot.EXT, tmpdir, Plot.PLT_EXT, tmpdir, Plot.DATA_EXT)
                print('* Cleaning {}\n$ {}'.format(tmpdir, cmd))
                os.system(cmd)

        @staticmethod
        def init_multiplot_template():
                '''Initialize multiplot template.'''
                templates_dir = os.path.join('templates')
                env = Environment( loader = FileSystemLoader(templates_dir) )
                template = env.get_template('multiplot.gp.j2')

                return template

        @staticmethod
        def do_density_x_clustering_coeff():
                '''Generate plotting of Density and clustering coefficient comparison.'''
                templates_dir = os.path.join('templates')
                env = Environment( loader = FileSystemLoader(templates_dir) )
                template = env.get_template('plot.gp.j2')
                (xs, ys) = ([], [])
                xmax = 0.225
                ymax = 1.0
                xlabel = 'Density'
                
                pi = plotinfo(xlabel.lower() + SEP + 'cluster-coeff', xlabel, 'Clustering coefficient')
                # file name is unique because there is only one point for each book
                fn = os.path.join(Project.get_outdir(), xlabel + SEP + 'cluster-coeff' + Plot.DATA_EXT)
                for i in range(len(Plot.BOOKS)):
                        book = Plot.BOOKS[i]
                        G = Plot.GS[i]

                        x = Graphs.density(G)
                        y = gt_cluster.global_clustering(G)[0]
                        xs.append(x)
                        ys.append(y)

                        dump_book_data(xlabel, 'cluster-coeff', book.get_name(), Plot.DATA_EXT, [x], [y], append=True)
                        pi.datainfos.append(datainfo(book.get_name(), fn))
                        
                (r, p) = pearsonr(xs, ys)
                popt, pcov = curve_fit(linear_func, xs, ys)
                test_ceil(xs, ys, xmax, ymax)                
                filename = os.path.join(Project.get_outdir(), pi.title + Plot.PLT_EXT)
                with open(filename, 'w') as fh:
                        fh.write(template.render(
                                filename = fn,
                                extension = Plot.EXT,
                                plotinfo = pi,
                                xmax = xmax,
                                ymax = ymax,
                                outdir = Project.get_outdir(),
                                rvalue = r,
                                ptest = p,
                                slope=popt[0],
                                intercept = popt[1],
                        ))
                cmd = Plot.CMD + filename
                print('\n$ {}'.format(cmd))
                os.system(cmd)
                        
        @staticmethod
        def do_centralities():
                '''Generate plotting of centralities comparisons.'''
                template = Plot.init_multiplot_template()
                xmax = 1.0
                ymax = 0.5
                
                for plt in Graphs.get_centrality_names():
                        pi = plotinfo(plt.lower() + SEP + 'lobby' , plt, 'Lobby')
                                        
                        for i in range(len(Plot.BOOKS)):
                                book = Plot.BOOKS[i]
                                G = Plot.GS[i]
                                xs = np.array(Graphs.get_centrality_values(G, plt))
                                ys = np.array(Graphs.get_centrality_values(G, 'Lobby'))
                                xs, ys, fn = dump_book_data(plt.lower(), 'lobby', book.get_name(), Plot.DATA_EXT, xs, ys)
                                (r, p) = pearsonr(xs, ys)
                                popt, pcov = curve_fit(linear_func, xs, ys)
                                pi.datainfos.append(datainfo(book.get_name(), fn, r, p, popt[0], popt[1]))
                                test_ceil(xs, ys, xmax, ymax)

                        filename = os.path.join(Project.get_outdir(), pi.title + Plot.PLT_EXT)
                        with open(filename, 'w') as fh:
                                fh.write(template.render(
                                        plot_measure = 'centralities',
                                        extension = Plot.EXT,
                                        plotinfo = pi,
                                        xmax = xmax,
                                        ymax = ymax,
                                        outdir = Project.get_outdir(),
                                        nrows = 4,
                                        ncols = 3,
                                ))
                        cmd = Plot.CMD + filename
                        print('\n$ {}'.format(cmd))
                        os.system(cmd)

        @staticmethod
        def do_assortativity():
                '''Generate assortativity multiplot on books.'''
                template = Plot.init_multiplot_template()
                xmax = 1.0
                ymax = 1.0
                
                pi = plotinfo('assortativity' , 'k', 'k_{nn}')
                                        
                for i in range(len(Plot.BOOKS)):
                        book = Plot.BOOKS[i]
                        G = Plot.GS[i]
                        (xs, ys, xxs, yavgs) = Graphs.get_degree_avg_neighbors(G)
                        xs, ys, fn = dump_book_data('k', 'knn', book.get_name(), Plot.DATA_EXT, xs, ys, xxs, yavgs)
                        pi.datainfos.append(datainfo(book.get_name(), fn))

                        test_ceil(xs, ys, xmax, ymax)
                        
                filename = os.path.join(Project.get_outdir(), pi.title + Plot.PLT_EXT)
                with open(filename, 'w') as fh:
                        fh.write(template.render(
                                plot_measure = 'assortativity',
                                extension = Plot.EXT,
                                plotinfo = pi,
                                xmax = xmax,
                                ymax = ymax,
                                outdir = Project.get_outdir(),
                                nrows = 4,
                                ncols = 3,
                        ))
                cmd = Plot.CMD + filename
                print('\n$ {}'.format(cmd))
                os.system(cmd)

        def do():
                Plot.init()
                Plot.do_centralities()
                Plot.do_assortativity()
                Plot.do_density_x_clustering_coeff()
