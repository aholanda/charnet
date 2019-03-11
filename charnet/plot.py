from jinja2 import Environment, FileSystemLoader
import os
import numpy
from scipy.stats import pearsonr
from sklearn.linear_model import LinearRegression

from books import *

def dump_data(filename, xs, ys):
        assert(len(xs) == len(ys))

        f = open(filename, 'w')
        for i in range(len(xs)):
                f.write(str(xs[i]) + '\t' + str(ys[1]) + '\n')
        f.close()
        print('* Wrote {}'.format(filename))

class datainfo:
        def __init__(self, title, filename, rvalue, ptest, slope, intercept):
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
def X(xs, ys):
        X = numpy.array([])
        for i in range(len(xs)):
                numpy.append(X, [xs[i], ys[i]])

        return X

class Plot:
        # plot figure extension
        EXT = '.eps'
        # gnuplot extension
        PLT_EXT = '.gp'
        # data file extension
        DATA_EXT = '.dat'

        @staticmethod
        def do():
                templates_dir = os.path.join('templates')
                env = Environment( loader = FileSystemLoader(templates_dir) )
                template = env.get_template('multiplot.gp.j2')

                for plt in Graphs.get_centrality_names():
                        pi = plotinfo(plt + ' x ' + 'Lobby' , plt, 'Lobby')
                
                        books = Books.get_books()
                        for book in books:
                                G = book.get_graph()
                                xs = numpy.array(Graphs.get_centrality_values(G, plt))
                                ys = numpy.array(Graphs.get_centrality_values(G, 'Lobby'))
                                filename = plt + '-' + book.get_name() + Plot.DATA_EXT
                                filename = os.path.join('/tmp', filename)
                                dump_data(filename, xs, ys)
                                (r, p) = pearsonr(xs, ys)
                                fit = LinearRegression().fit(X(xs, ys), X(xs, ys))
                                print(r, p)
                                pi.datainfos.append(datainfo(book.get_name(), filename, r, p, fit.coef_, fit.intercept_))

                        filename = plt + Plot.PLT_EXT
                        filename = os.path.join('/tmp', filename)
                        with open(filename, 'w') as fh:
                                fh.write(template.render(
                                        extension = Plot.EXT,
                                        plotinfo = pi
                                ))
                        print('Run: gnuplot {}'.format(filename))
