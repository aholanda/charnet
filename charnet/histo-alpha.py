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

        plt.hist([xs, ys, zs], bins, color=['black', 'darkgray', 'lightgray'])
        plt.xlabel("Character Appearance")
        plt.ylabel("Frequency")
        plt.legend(genres)
        hist.savefig('/tmp/histogram.png')

def write_data(g2f_arr, g2f2n):
        for i in range(len(genres)):
                fn = '/tmp/' + genres[i] + '-freq-appear-dist.txt'
                f = open(fn, 'w')

                for fr in g2f_arr[genres[i]]:
                        f.write(str(fr) + '\n')
                f.close()
                print('* Wrote {}'.format(fn))

                fn = '/tmp/' + genres[i] + '-freq-x-N.txt'
                f = open(fn, 'w')

                for fr,n in g2f2n[genres[i]].items():
                        f.write(str(fr) + ',' + str(n) + '\n')
                f.close()
                print('* Wrote {}'.format(fn))

if __name__ == '__main__':
        genre2freq_arr = {}
        genre2freq2n = {}
        
        books = Books.get_books()
        for b in books:
                genre = Books.get_genre_name(b.get_genre().value)
                if genre not in genre2freq_arr: genre2freq_arr[genre] = []
                if genre not in genre2freq2n: genre2freq2n[genre] = {}
                
                fn = '/tmp/' + b.get_name() + '-freq-only.txt'
                fd = open(fn, 'w')

                G = b.get_graph()
                for v in G.vertices():
                        f = G.vertex_properties["frequency"][v]
                        fill_data(genre, f)

                        fd.write(str(f) + '\n')
                        
                        genre2freq_arr[genre].append(f)

                        if f not in genre2freq2n[genre]:
                                genre2freq2n[genre][f] = 1
                        else:
                               genre2freq2n[genre][f] += 1 

                fd.close()
                print(' ** Wrote {}'.format(fn))
        plot_data()
        write_data(genre2freq_arr, genre2freq2n)
