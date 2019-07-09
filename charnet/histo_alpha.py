#!/usr/bin/env python3

"""Test with histogram on alpha values."""

import matplotlib.pyplot as plt
import numpy as np

from .books import Books

(xs, ys, zs) = ([], [], [])

GENRES = ['Biography', 'Legendary', 'Fiction']

def fill_data(which, data):
    if genre == GENRES[0]:
        xs.append(data)
    elif genre == GENRES[1]:
        ys.append(data)
    elif genre == GENRES[2]:
        zs.append(data)
    else:
        print('ERROR: Wrong book genre: {}'.format(which))
        exit(-1)

def plot_data():
    hist = plt.figure()
    bins = np.linspace(0, 50, 10)
    plt.hist([xs, ys, zs], bins, color=['black', 'darkgray', 'lightgray'])
    plt.xlabel("Character Appearance")
    plt.ylabel("Frequency")
    plt.legend(GENRES)
    hist.savefig('/tmp/histogram.png')

def write_data(g2f_arr, g2f2n):
    for i in range(len(GENRES)):
        file_name = '/tmp/'+ GENRES[i] + '-freq-appear-dist.txt'
        _file = open(file_name, 'w')
        for freq in g2f_arr[GENRES[i]]:
            _file.write(str(freq) + '\n')
        _file.close()
        print('* Wrote %s', file_name)
        file_name = '/tmp/' + GENRES[i] + '-freq-x-N.txt'
        _file = open(file_name, 'w')
        for freq, times in g2f2n[GENRES[i]].items():
            _file.write(str(freq) + ',' + str(times) + '\n')
        _file.close()
        print('* Wrote {}'.format(file_name))

if __name__ == '__main__':
    genre2freq_arr = {}
    genre2freq2n = {}

    BOOKS = Books.get_books()
    for book in BOOKS:
        genre = Books.get_genre_name(book.get_genre().value)
        if genre not in genre2freq_arr:
            genre2freq_arr[genre] = []
        if genre not in genre2freq2n:
            genre2freq2n[genre] = {}

        fn = '/tmp/' + book.get_name() + '-freq-only.txt'
        fd = open(fn, 'w')
        G = book.get_graph()
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
