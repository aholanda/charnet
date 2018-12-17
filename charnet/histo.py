#!/usr/bin/python3

import matplotlib.pyplot as plt
import numpy as np
from matplotlib import colors
from matplotlib.ticker import PercentFormatter

from books import Books

(xs, ys, zs) = ([], [], [])

genres = ['Biography', 'Legendary', 'Fiction']

def fill_data(which, d):
        if genre == genres[0]:
                xs.append(d)
        elif genre == genres[1]:
                ys.append(d)
        elif genre == genres[2]:
                zs.append(d)
        else:
                print('ERROR: Wrong book genre: {}'.format(which))
                exit(-1)
        
def plot_data():
        hist = plt.figure()

        bins = np.linspace(0, 50, 10)

        plt.hist([xs, ys, zs], bins, color=['green', 'blue', 'red'])
        #plt.hist(ys, bins, alpha=0.5)
        #plt.hist(zs, bins, alpha=0.5)
        plt.xlabel("Character Appearance")
        plt.ylabel("Frequency")
        plt.legend(genres)
        # We can set the number of bins with the `bins` kwarg
        # axs[0].hist(xs, bins=nbins)
        # axs[1].hist(ys, bins=nbins)
        # axs[2].hist(zs, bins=nbins)
        hist.savefig('/tmp/histogram.png')
        
if __name__ == '__main__':
        genre2freq2n = {}

        books = Books.get_books()
        for b in books:
                genre = Books.get_genre_name(b.get_genre().value)
                if genre not in genre2freq2n: genre2freq2n[genre] = {}
                
                G = b.get_graph()

                for v in G.vertices():
                        f = G.vertex_properties["frequency"][v]
                        fill_data(genre, f)

        plot_data()
        
