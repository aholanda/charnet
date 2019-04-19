from jinja2 import Environment, FileSystemLoader
import os
import numpy as np
from scipy.stats import pearsonr
from scipy.optimize import curve_fit

import graph_tool as gt
import graph_tool.clustering as gt_cluster

# LOCAL
from books import *
from graphs import Measure
from formatting import Formatting

SEP = '_'

def dump_book_data(xmeasure_num, ymeasure_num, book_name, extension, xs, ys, xxs=None, yys=None, book_genre=None):
        '''Dump data to output file.'''
        assert(len(xs) == len(ys))
        xlabel = Measure.get_label(xmeasure_num)
        ylabel = Measure.get_label(ymeasure_num)
        (_xs, _ys) = ([], [])
        label = ''
        mode_str = 'Wrote'

        fn = os.path.join(Project.get_outdir(), xlabel + SEP + ylabel + SEP + book_name + extension)
        f = open(fn, 'w')
        for i in range(len(xs)):
                if math.isnan(xs[i]) or math.isnan(ys[i]):
                        continue

                ln = '\n'
                if xxs is not None and yys is not None:
                        if i < len(xxs):
                                ln = '\t' + str(xxs[i]) + '\t' + str(yys[i]) + '\n'

                # sorry, but \lblfmt is defined in templates/settings.gp
                if xmeasure_num == Measure.DENSITY and ymeasure_num == Measure.CLUSTERING_COEFFICIENT:
                        label = '"\\\\tiny ' + book_name + ' (' + book_genre + ')"\t'

                ln = label + str(xs[i]) + '\t' + str(ys[i]) + ln
                f.write(ln)
                _xs.append(xs[i])
                _ys.append(ys[i])
        f.close()
        print('* {} {}; '.format(mode_str, fn), end='', flush=True)
        return _xs, _ys, fn

class coordinates:
        '''Wrap coordinates x, y, z (optional).'''
        def __init__(self, x, y, z=0.0):
                self.x = x
                self.y = y
                self.z = z

        def get(self, axis):
                if axis == 'x':
                        return self.x
                elif axis == 'y':
                        return self.y
                elif axis == 'z':
                        return self.z
                else:
                        print('Unknown axis {}'.format(axis))

        def set(self, axis, v):
                if axis == 'x':
                        self.x = v
                elif axis == 'y':
                        self.y = v
                elif axis == 'z':
                        self.z = v
                else:
                        print('Unknown axis {}'.format(axis))
                        exit()

class datainfo:
        def __init__(self, title, filename, rvalue=0.0, pvalue=0.0, slope=0.0, intercept=0.0, coords_xmin=None, yoffset=.1, xoffset=0.0, alpha=0.0):
                self.title = title
                self.filename = filename
                self.rvalue = rvalue
                self.pvalue = pvalue
                self.slope = slope
                self.intercept = intercept
                self.coords_xmin = coords_xmin
                self.labelpt_xoffset = xoffset
                self.labelpt_yoffset = yoffset
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
                xmeasure_num = Measure.DENSITY
                ymeasure_num = Measure.CLUSTERING_COEFFICIENT
                xlabel = Measure.get_label(xmeasure_num)
                ylabel = Measure.get_label(ymeasure_num)
                # y offset for point labels
                doff = 0.4 # default offset
                # offsets for point labels
                offs = {
                        # bio
                        'dick': [0, doff],
                        'tolkien': [0, doff],
                        'newton': [0, doff],
                        'hawking': [-doff/2, doff],
                        # legendary
                        'apollonius': [9*doff, 0],
                        'acts': [0, doff],
                        'pythagoras': [9*doff, 0],
                        'luke': [2*doff, doff],
                        # fiction
                        'hobbit': [0, doff],
                        'david': [0, doff],
                        'arthur': [4*doff, -doff],
                        'huck': [0, doff]
                }

                pi = plotinfo(Measure.get_label(xmeasure_num) + SEP + 'cluster-coeff', xlabel, ylabel)
                for i in range(len(Plot.BOOKS)):
                        book = Plot.BOOKS[i]
                        book_name = book.get_name()
                        G = Plot.GS[i]
                        x = Graphs.density(G)
                        y = gt_cluster.global_clustering(G)[0]
                        xs.append(x)
                        ys.append(y)

                        _xs, _ys, fn = dump_book_data(xmeasure_num, ymeasure_num, book_name, Plot.DATA_EXT, [x], [y], book_genre=Books.get_genre_label(book))
                        pi.datainfos.append(datainfo(book.get_name(), fn, xoffset=offs[book_name][0], yoffset=offs[book_name][1]))

                (r, p) = pearsonr(xs, ys)
                popt, pcov = curve_fit(linear_func, xs, ys)
                test_ceil(xs, ys, xmax, ymax)
                filename = os.path.join(Project.get_outdir(), pi.title + Plot.PLT_EXT)
                with open(filename, 'w') as fh:
                        fh.write(template.render(
                                plot_measure = 'DxCC',
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
        def do_centralities(supp):
                '''Generate plotting of centralities comparisons.'''
                template = Plot.init_multiplot_template()
                xmax = 1.0
                ymax = 0.5

                supp.send(('begin_table', 'Centralities $p$-values.'))
                        
                for num in Graphs.get_centrality_nums():
                        label = Measure.get_label(num)
                        lobby_str = Measure.get_label(Measure.LOBBY)
                        pi = plotinfo(label + SEP + lobby_str , label, lobby_str)

                        supp.send(('begin_subtable', '0.3'))

                        supp.send(('xlabel', label))
                        supp.send(('ylabel', lobby_str))
                        
                        supp.send(('begin_data', ''))
                        for i in range(len(Plot.BOOKS)):
                                book = Plot.BOOKS[i]
                                book_name = book.get_name()
                                G = Plot.GS[i]
                                xs = np.array(Graphs.get_centrality_values(G, num))
                                ys = np.array(Graphs.get_centrality_values(G, Measure.LOBBY))
                                xs, ys, fn = dump_book_data(num, Measure.LOBBY, book.get_name(), Plot.DATA_EXT, xs, ys)
                                (r, p) = pearsonr(xs, ys)

                                # send to write to suplementary material in formatting.py
                                supp.send(('book_name', book_name))
                                if p < 0.0099:
                                        supp.send(('pvalue', '{:.2e}'.format(float(p))))
                                else:
                                        supp.send(('pvalue', '{:.2f}'.format(float(p))))
                                           
                                popt, pcov = curve_fit(linear_func, xs, ys)
                                pi.datainfos.append(datainfo(book_name, fn, r, p, popt[0], popt[1]))
                                test_ceil(xs, ys, xmax, ymax)

                        supp.send(('end_data', ''))
                        supp.send(('end_subtable', ''))

                        filename = os.path.join(Project.get_outdir(), pi.title + Plot.PLT_EXT)
                        with open(filename, 'w') as fh:
                                fh.write(template.render(
                                        plot_measure = 'centralities',
                                        measure_type = label.lower(),
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

                supp.send(('end_table', ''))

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
                        xs, ys, fn = dump_book_data(Measure.DEGREE, Measure.AVG_DEGREE_OF_NEIGHBORS, book.get_name(), Plot.DATA_EXT, xs, ys, xxs, yavgs)
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

        def do_CDF_w_fit(supp):
                '''Do cumulative distribution probability with fitting multiplot on books.'''
                import scipy.special as sz
                template = Plot.init_multiplot_template()
                xmax = 1.0
                ymax = 1.0
                xlabel = 'x'
                ylabel = 'Pr(X\\\\geq x)'

                supp.send(('begin_table', 'Degree cumulative distribution'))

                supp.send(('begin_subtable', '0.4'))
                supp.send(('xlabel', '$' + xlabel + '$'))
                supp.send(('ylabel', '$' + ylabel.replace("\\\\", "\\") + '$'))
                supp.send(('begin_data', ''))

                
                pi = plotinfo('cdf' , xlabel, ylabel)

                for i in range(len(Plot.BOOKS)):
                        datax = []
                        book = Plot.BOOKS[i]
                        book_name = book.get_name()
                        # alpha
                        a = Fits.alpha(book_name)
                        # kmin
                        xmin = Fits.kmin(book_name)
                        # p-value
                        pval = Fits.pvalue(book_name)

                        G = Plot.GS[i]

                        # store degrees to run fitting algorithm
                        fn = os.path.join(Project.get_outdir(), book_name + '-degrees' + Plot.DATA_EXT)
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

                        xs, ys, fn = dump_book_data(Measure.DEGREE, Measure.CDF, book_name, Plot.DATA_EXT, xs, ys, xxs=cfx, yys=cfy)
                        pi.datainfos.append(datainfo(book_name, fn, alpha=a, coords_xmin=coordinates(cfx[0], cfy[0]), pvalue=pval))

                        # send to write to suplementary material in formatting.py
                        supp.send(('book_name', book_name))
                        supp.send(('pvalue', str(pval)))

                supp.send(('end_data', ''))
                supp.send(('end_subtable', ''))
                supp.send(('end_table', ''))

                filename = os.path.join(Project.get_outdir(), pi.title + Plot.PLT_EXT)
                with open(filename, 'w') as fh:
                        fh.write(template.render(
                                plot_measure = 'cdf',
                                significance_level = Plot.P + 0.05, # P + Epsilon
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
                # Prepare to write supplemental material sending info to couroutine
                supp = Formatting.couroutine_write_supplementary_material('suppl')
                next(supp)
                Plot.init()
                Plot.do_centralities(supp)
                Plot.do_assortativity()
                Plot.do_density_x_clustering_coeff()
                Plot.do_CDF_w_fit(supp)
                # send key to close supplementary file
                supp.send(('CLOSE_FILE', ''))
