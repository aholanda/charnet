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
                if xxs is not None and yys is not None:
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
        def __init__(self, title, filename, rvalue=0.0, pvalue=0.0, slope=0.0, intercept=0.0, xmin=0, xrange_=None, alpha=0.0):
                self.title = title
                self.filename = filename
                self.rvalue = rvalue
                self.pvalue = pvalue
                self.slope = slope
                self.intercept = intercept
                self.xmin = xmin
                self.alpha = alpha

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
#                print('ERROR max value {%1.2f}/{%1.2f},{%1.2f}/{%1.2f} ignored'.format(np.max(xs), xmax, np.max(ys), ymax))
                exit(-1)

# These values were obtained running Matlab scripts from
# http://tuvalu.santafe.edu/~aaronc/powerlaws/{plfit,plpva}.m
class Fits:
        # label: [kmin, alpha, p-value]
        parms = {
                # bio
                'dick': [3, 2.71, .84],
                'tolkien': [6, 2.66, .79],
                'newton': [2, 2.95, .82],
                'hawking': [2, 2.54, .05],
                # legendary
                'apollonius': [2, 2.43, .28],
                'acts': [6, 3.41, .79],
                'pythagoras': [1, 2.93, .73],
                'luke': [3, 2.26, .00],
                # fiction
                'hobbit': [1, 1.5, .00],
                'david': [14, 3.49, .39],
                'arthur': [3, 2.3, .66],
                'huck': [8, 3.5, .01]
        }

        @staticmethod
        def check_label(label):
                if label not in Fits.parms:
                        print ('Wrong book name {}'.format(label))
                        exit()

        @staticmethod
        def kmin(name):
                Fits.check_label(name)
                return Fits.parms[name][0]

        @staticmethod
        def alpha(name):
                Fits.check_label(name)
                return Fits.parms[name][1]

        @staticmethod
        def pvalue(name):
                Fits.check_label(name)
                return Fits.parms[name][2]

        
class Plot:
        # significance level for statistical tests
        P = 0.05        
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
                                pvalue = p,
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
                
                for centr in Graphs.get_centrality_names():
                        pi = plotinfo(centr.lower() + SEP + 'lobby' , centr, 'Lobby')
                                        
                        for i in range(len(Plot.BOOKS)):
                                book = Plot.BOOKS[i]
                                G = Plot.GS[i]
                                xs = np.array(Graphs.get_centrality_values(G, centr))
                                ys = np.array(Graphs.get_centrality_values(G, 'Lobby'))
                                xs, ys, fn = dump_book_data(centr.lower(), 'lobby', book.get_name(), Plot.DATA_EXT, xs, ys)
                                (r, p) = pearsonr(xs, ys)
                                popt, pcov = curve_fit(linear_func, xs, ys)
                                pi.datainfos.append(datainfo(book.get_name(), fn, r, p, popt[0], popt[1]))
                                test_ceil(xs, ys, xmax, ymax)

                        filename = os.path.join(Project.get_outdir(), pi.title + Plot.PLT_EXT)
                        with open(filename, 'w') as fh:
                                fh.write(template.render(
                                        plot_measure = 'centralities',
                                        measure_type = centr.lower(),
                                        significance_level = Plot.P,
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

        def do_CDF_w_fit():
                '''Do cumulative distribution probability with fitting multiplot on books.'''
                import scipy.special as sz
                template = Plot.init_multiplot_template()
                xmax = 1.0
                ymax = 1.0
                
                pi = plotinfo('cdf' , '$x$', '$P(X\\\\geq x)$')

                for i in range(len(Plot.BOOKS)):
                        datax = []
                        book = Plot.BOOKS[i]
                        name = book.get_name()
                        # alpha
                        a = Fits.alpha(name)
                        # kmin
                        xmin = Fits.kmin(name)
                        # p-value
                        pval = Fits.pvalue(name)

                        G = Plot.GS[i]

                        # store degrees to run fitting algorithm
                        fn = os.path.join(Project.get_outdir(), book.get_name() + '-degrees' + Plot.DATA_EXT)
                        f = open(fn, 'w')
                        for v in G.vertices():
                                k = v.out_degree()
                                if k <= 0:
                                        continue
                                
                                f.write(str(k) + '\n')
                                datax.append(k)
                                if k > xmax:
                                        xmax = k
                        print('* Wrote {};\t'.format(fn), end='')
                        f.close()
                                        
                        # Empirical data
                        n = len(datax)
                        xs = np.unique(datax)
                        vals, base = np.histogram(datax, xs)
                        vals = vals/n # nomalize frequncy in hist.

                        # inverse CDF
                        ys = 1 - np.insert(np.cumsum(vals), 0, 0.0) # add 0.0 at front

                        # Theoretical line
                        cfy = np.power(np.arange(xmin, xs[len(xs)-1]+1), -a)/(sz.zeta(a) - np.sum(np.power(np.arange(1,xmin), -a)))
                        # do and invert cumulative distribution
                        cfy = 1 - np.insert(np.cumsum(cfy), 0, 0.0)
                        # normalize
                        cfy = cfy * ys[np.where(xs == xmin)[0][0]]
                        
                        # get the corresponding values for y in the x axis
                        cfx = np.arange(xmin, xs[len(xs)-1] + 2)
                                                                            

                        xs, ys, fn = dump_book_data('k', 'Pk', book.get_name(), Plot.DATA_EXT, xs, ys, xxs=cfx, yys=cfy)
                        pi.datainfos.append(datainfo(book.get_name(), fn, alpha=a, xmin=xmin, pvalue=pval))
                        
                        #test_ceil(xs, ys, xmax, ymax)
                        
                filename = os.path.join(Project.get_outdir(), pi.title + Plot.PLT_EXT)
                with open(filename, 'w') as fh:
                        fh.write(template.render(
                                plot_measure = 'cdf',
                                significance_level = Plot.P,
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
                # Plot.do_assortativity()
                # Plot.do_density_x_clustering_coeff()
                Plot.do_CDF_w_fit()
