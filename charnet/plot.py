"""Define functions to plot graphics used in the paper."""

import math
import os

import numpy as np

from jinja2 import Environment, FileSystemLoader

from scipy.stats import pearsonr
from scipy.optimize import curve_fit

import graph_tool.clustering as gt_cluster

# LOCAL
from charnet.books import Books, Project
from charnet.graphs import Graphs, Measure
from charnet.formatting import Formatting

SEP = '_'

def dump_book_data(xmeasure_num, ymeasure_num, book_name,
                   extension, x_coords, y_coords, xxs=None, yys=None,
                   book_genre=None):
    '''Dump data to output file.'''
    assert len(x_coords) == len(y_coords)
    xlabel = Measure.get_label(xmeasure_num)
    ylabel = Measure.get_label(ymeasure_num)
    (_xs, _ys) = ([], [])
    label = ''
    file_name = os.path.join(Project.get_outdir(), xlabel + SEP + ylabel \
                             + SEP + book_name + extension)
    _file = open(file_name, 'w')
    for i in range(len(x_coords)):
        if math.isnan(x_coords[i]) or math.isnan(y_coords[i]):
            continue
        line = '\n'
        if xxs is not None and yys is not None:
            if i < len(xxs):
                line = '\t' + str(xxs[i]) + '\t' + str(yys[i]) + '\n'
        # sorry, but \lblfmt is defined in templates/settings.gp
        if xmeasure_num == Measure.DENSITY and ymeasure_num == Measure.CLUSTERING_COEFFICIENT:
            label = '"\\\\tiny ' + book_name + ' (' + book_genre + ')"\t'
        line = label + str(x_coords[i]) + '\t' + str(y_coords[i]) + line
        _file.write(line)
        _xs.append(x_coords[i])
        _ys.append(y_coords[i])
    _file.close()
    print('* mode_str + fn')
    return _xs, _ys, file_name

class Coordinates(object):
    '''Wrap coordinates x, y, z (optional).'''
    def __init__(self, x, y, z=0.0):
        self.x_coord = x
        self.y_coord = y
        self.z_coord = z
    def get(self, axis):
        """Return the value of selected axis."""
        val = 0.0
        if axis == 'x':
            val = self.x_coord
        elif axis == 'y':
            val = self.y_coord
        elif axis == 'z':
            val = self.z_coord
        else:
            print('Unknown axis {}'.format(axis))
        return val
    def set(self, axis, val):
        """Set values for coordinates."""
        if axis == 'x':
            self.x_coord = val
        elif axis == 'y':
            self.y_coord = val
        elif axis == 'z':
            self.z_coord = val
        else:
            print('Unknown axis {}'.format(axis))
            exit()

class DataInfo(object):
    """Class to wrap main data."""
    def __init__(self, title, filename, rvalue=0.0,
                 pvalue=0.0, slope=0.0, intercept=0.0,
                 coords_xmin=None, yoffset=.1, xoffset=0.0,
                 alpha=0.0):
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

class PlotInfo(object):
    """Class to wrap information for plotting."""
    def __init__(self, title, xlabel, ylabel, datainfos=None):
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        if datainfos == None:
            self.datainfos = []

def linear_func(x_coord, slope, offset):
    """Function that represents a linear one."""
    return x_coord*slope + offset

def test_ceil(x_coords, y_coords, xmax, ymax):
    """Check superior bounds."""
    if np.max(x_coords) > xmax or np.max(y_coords) > ymax:
        print(np.max(x_coords), np.max(y_coords))
        exit(-1)

def run_command(cmd, filename):
    """Execute a command in the OS."""
    cmd = cmd + filename
    print('\n$ {}'.format(cmd))
    os.system(cmd)

# These values were obtained running Matlab scripts from
# http://tuvalu.santafe.edu/~aaronc/powerlaws/{plfit,plpva}.m
class Fits(object):
    """Class with functions to perform a curve fitting."""
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
        """Verify if the label exists."""
        if label not in Fits.parms:
            print ('Wrong book name {}'.format(label))
            exit()
    @staticmethod
    def kmin(name):
        """Return the point where the fitting begins."""
        Fits.check_label(name)
        return Fits.parms[name][0]
    @staticmethod
    def alpha(name):
        """Return alpha from fitting."""
        Fits.check_label(name)
        return Fits.parms[name][1]
    @staticmethod
    def pvalue(name):
        """Returns p-value from fitting."""
        Fits.check_label(name)
        return Fits.parms[name][2]
class Plot(object):
    """Class with static functions to plot graphics used in the paper."""
    # significance level for statistical tests
    P = 0.05
    # plot command prefix
    GP_CMD = 'gnuplot '
    CMDs = ['cd preprint && ' + GP_CMD, 'cd presentation && ' + GP_CMD]
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

    def __init__(self):
        pass

    @staticmethod
    def init():
        """Initialize environment for plotting. Remove old files. """
        tmpdir = Project.get_outdir()
        # Initialize graphs.
        Plot.BOOKS = Books.get_books()
        for book in Plot.BOOKS:
            graph = book.get_graph()
            Plot.GS.append(graph)
        cmd = 'rm -f {}/*{} {}/*{} {}/*{}'.format(tmpdir, Plot.EXT,
                                                  tmpdir, Plot.PLT_EXT,
                                                  tmpdir, Plot.DATA_EXT)
        print('* Cleaning {}\n$ {}'.format(tmpdir, cmd))
        os.system(cmd)
    @staticmethod
    def init_multiplot_template():
        '''Initialize multiplot template.'''
        templates_dir = os.path.join('templates')
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template('multiplot.gp.j2')
        return template
    @staticmethod
    def do_density_x_clustering_coeff():
        '''Generate plotting of Density and clustering coefficient comparison.'''
        templates_dir = os.path.join('templates')
        env = Environment(loader=FileSystemLoader(templates_dir))
        template = env.get_template('plot.gp.j2')
        (x_coords, y_coords) = ([], [])
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
        plot_info = PlotInfo(Measure.get_label(xmeasure_num) \
                             + SEP + 'cluster-coeff', xlabel, ylabel)
        for i in range(len(Plot.BOOKS)):
            book = Plot.BOOKS[i]
            book_name = book.get_name()
            graph = Plot.GS[i]
            x_coord = Graphs.density(graph)
            y_coord = gt_cluster.global_clustering(graph)[0]
            x_coords.append(x_coord)
            y_coords.append(y_coord)
            _x_coords, _y_coords, file_name = \
                    dump_book_data(xmeasure_num, ymeasure_num,
                                   book_name, Plot.DATA_EXT, [x_coord], [y_coord],
                                   book_genre=Books.get_genre_label(book))
            plot_info.datainfos.append(DataInfo(book.get_name(), file_name,
                                                xoffset=offs[book_name][0],
                                                yoffset=offs[book_name][1]))
        (r_val, p_val) = pearsonr(x_coords, y_coords)
        popt, _ = curve_fit(linear_func, x_coords, y_coords)
        test_ceil(x_coords, y_coords, xmax, ymax)
        filename = os.path.join(Project.get_outdir(), plot_info.title + Plot.PLT_EXT)
        with open(filename, 'w') as file_handle:
            file_handle.write(template.render(
                plot_measure='DxCC',
                filename=file_name,
                extension=Plot.EXT,
                PlotInfo=plot_info,
                xmax=xmax,
                ymax=ymax,
                outdir=Project.get_outdir(),
                rvalue=r_val,
                pvalue=p_val,
                slope=popt[0],
                intercept=popt[1],
            ))
        for cmd in Plot.CMDs:
            run_command(cmd, filename)
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
            plot_info = PlotInfo(label + SEP + lobby_str, label, lobby_str)
            supp.send(('begin_subtable', '0.3'))
            supp.send(('xlabel', label))
            supp.send(('ylabel', lobby_str))
            supp.send(('begin_data', ''))
            for i in range(len(Plot.BOOKS)):
                book = Plot.BOOKS[i]
                book_name = book.get_name()
                graph = Plot.GS[i]
                x_coords = np.array(Graphs.get_centrality_values(graph, num))
                y_coords = np.array(Graphs.get_centrality_values(graph, Measure.LOBBY))
                x_coords, y_coords, file_name = dump_book_data(num, Measure.LOBBY,
                                                               book.get_name(), Plot.DATA_EXT,
                                                               x_coords, y_coords)
                (r_val, p_val) = pearsonr(x_coords, y_coords)
                # send to write to suplementary material in formatting.py
                supp.send(('book_name', book_name))
                if p_val < 0.0099:
                    supp.send(('pvalue', '{:.2e}'.format(float(p_val))))
                else:
                    supp.send(('pvalue', '{:.2f}'.format(float(p_val))))
                popt, _ = curve_fit(linear_func, x_coords, y_coords)
                plot_info.datainfos.append(DataInfo(book_name, file_name,
                                                    r_val, p_val, popt[0],
                                                    popt[1]))
                test_ceil(x_coords, y_coords, xmax, ymax)
            supp.send(('end_data', ''))
            supp.send(('end_subtable', ''))
            filename = os.path.join(Project.get_outdir(), plot_info.title + Plot.PLT_EXT)
            with open(filename, 'w') as file_handle:
                file_handle.write(template.render(
                    plot_measure='centralities',
                    measure_type=label.lower(),
                    significance_level=Plot.P,
                    extension=Plot.EXT,
                    PlotInfo=plot_info,
                    xmax=xmax,
                    ymax=ymax,
                    outdir=Project.get_outdir(),
                    nrows=4,
                    ncols=3,
                ))
            for cmd in Plot.CMDs:
                run_command(cmd, filename)
        supp.send(('end_table', ''))
    @staticmethod
    def do_assortativity():
        '''Generate assortativity multiplot on books.'''
        template = Plot.init_multiplot_template()
        xmax = 1.0
        ymax = 1.0
        plot_info = PlotInfo('assortativity', 'k', 'k_{nn}')
        for i in range(len(Plot.BOOKS)):
            book = Plot.BOOKS[i]
            graph = Plot.GS[i]
            (x_coords, y_coords, xx_coords, y_avgs) = Graphs.get_degree_avg_neighbors(graph)
            x_coords, y_coords, file_name = dump_book_data(Measure.DEGREE,
                                                           Measure.AVG_DEGREE_OF_NEIGHBORS,
                                                           book.get_name(),
                                                           Plot.DATA_EXT,
                                                           x_coords, y_coords,
                                                           xx_coords, y_avgs)
            plot_info.datainfos.append(DataInfo(book.get_name(), file_name))
            test_ceil(x_coords, y_coords, xmax, ymax)
        filename = os.path.join(Project.get_outdir(), plot_info.title + Plot.PLT_EXT)
        with open(filename, 'w') as file_handle:
            file_handle.write(template.render(
                plot_measure='assortativity',
                extension=Plot.EXT,
                PlotInfo=plot_info,
                xmax=xmax,
                ymax=ymax,
                outdir=Project.get_outdir(),
                nrows=4,
                ncols=3,
            ))
        for cmd in Plot.CMDs:
            run_command(cmd, filename)
    @staticmethod
    def do_cdf_w_fit(supp):
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
        plot_info = PlotInfo('cdf', xlabel, ylabel)
        for i in range(len(Plot.BOOKS)):
            datax = []
            book = Plot.BOOKS[i]
            book_name = book.get_name()
            # alpha
            alpha = Fits.alpha(book_name)
            # kmin
            xmin = Fits.kmin(book_name)
            # p-value
            pval = Fits.pvalue(book_name)
            graph = Plot.GS[i]
            # store degrees to run fitting algorithm
            file_name = os.path.join(Project.get_outdir(), book_name + '-degrees' + Plot.DATA_EXT)
            _file = open(file_name, 'w')
            for vert in graph.vertices():
                k = vert.out_degree()
                if k <= 0:
                    continue
                _file.write(str(k) + '\n')
                datax.append(k)
                if k > xmax:
                    xmax = k
            print('* Wrote ' + file_name + ';\t')
            _file.close()
            # Empirical data
            len_data = len(datax)
            x_coords = np.unique(datax)
            vals, _ = np.histogram(datax, x_coords)
            vals = vals/len_data # nomalize frequncy in hist.
            # inverse CDF
            y_coords = 1 - np.insert(np.cumsum(vals), 0, 0.0) # add 0.0 at front
            # Theoretical line
            cfy = np.power(np.arange(xmin, x_coords[len(x_coords)-1]+1), -alpha)/(sz.zeta(alpha) - \
                                           np.sum(np.power(np.arange(1, xmin), -alpha)))
            # do and invert cumulative distribution
            cfy = 1 - np.insert(np.cumsum(cfy), 0, 0.0)
            # normalize
            cfy = cfy * y_coords[np.where(x_coords == xmin)[0][0]]
            # get the corresponding values for y in the x axis
            cfx = np.arange(xmin, x_coords[len(x_coords)-1] + 2)
            x_coords, y_coords, file_name = dump_book_data(Measure.DEGREE, Measure.CDF, book_name,
                                                           Plot.DATA_EXT, x_coords, y_coords,
                                                           xxs=cfx, yys=cfy)
            plot_info.datainfos.append(DataInfo(book_name,
                                                file_name,
                                                alpha=alpha,
                                                coords_xmin=Coordinates(cfx[0], cfy[0]),
                                                pvalue=pval))
            # send to write to suplementary material in formatting.py
            supp.send(('book_name', book_name))
            supp.send(('pvalue', str(pval)))
        supp.send(('end_data', ''))
        supp.send(('end_subtable', ''))
        supp.send(('end_table', ''))
        filename = os.path.join(Project.get_outdir(), plot_info.title + Plot.PLT_EXT)
        with open(filename, 'w') as file_handle:
            file_handle.write(template.render(
                plot_measure='cdf',
                significance_level=Plot.P,
                extension=Plot.EXT,
                PlotInfo=plot_info,
                xmax=xmax,
                ymax=ymax,
                outdir=Project.get_outdir(),
                nrows=4,
                ncols=3,
            ))
        for cmd in Plot.CMDs:
            run_command(cmd, filename)
    @staticmethod
    def do_plot():
        """All plot functions are called at this function.
            Use a couroutine from Formatting to send parsed
            values to output."""
        # Prepare to write supplemental material sending info to couroutine
        supp = Formatting.couro_write_suppl('suppl')
        next(supp)
        Plot.init()
        Plot.do_centralities(supp)
        Plot.do_assortativity()
        Plot.do_density_x_clustering_coeff()
        Plot.do_cdf_w_fit(supp)
        # send key to close supplementary file
        supp.send(('CLOSE_FILE', ''))
