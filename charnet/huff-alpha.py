#!/usr/bin/python3

# Experimental script to test some ideas

import sys
import math

from books import Books

DEBUG = True

DIR = '/tmp/'
SUFFIX = {'deg':'-deg.txt',
          'freq':'-freq.txt',
          'idx':'-idx.txt',
          'hfreq':'-huffman-freq.txt',
          'hdeg':'-huffman-deg.txt'}

def __gen_fn(prefix, suffix):
        '''Generate a file name path.'''
        return DIR + prefix + SUFFIX[suffix]

def frequency_test(str_bin_seq):
        '''Frequency (Monobit) test'''
        s = 0
        eps = str_bin_seq
        n = len(eps)

        for i in range(n):
                b = int(eps[i])
                s += (1 + ((1 - b) * -2))

        s_obs = math.fabs(s) / math.sqrt(n)

        return math.erfc(s_obs/math.sqrt(2))


class NodeTree(object):
    def __init__(self, left=None, right=None):
            self.left = left
            self.right = right

    def children(self):
        return (self.left, self.right)

    def nodes(self):
        return (self.left, self.right)

    def __str__(self):
        return "%s_%s" % (self.left, self.right)

## Tansverse the NodeTress in every possible way to get codings
def huffman_code_tree(node, left=True, binString=""):
        if type(node) is str:
                return {node: binString}
        (l, r) = node.children()
        d = dict()
        d.update(huffman_code_tree(l, True, binString + "0"))
        d.update(huffman_code_tree(r, False, binString + "1"))
        return d

def create_tree(nodes):
        while len(nodes) > 1:
                key1, c1 = nodes[-1]
                key2, c2 = nodes[-2]
                nodes = nodes[:-2]
                node = NodeTree(key1, key2)
                nodes.append((node, c1 + c2))
                # Re-sort the list
                nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
                
        return nodes
                
def write_huffman_code(book_name, which):
        idx2freq = {}
        fn = __gen_fn(book_name, which)
        f = open(fn, 'r')
        for ln in f:
                 ln = ln.rstrip('\r\n')
                 (idx, freq) = ln.split(',', 1)
                 idx2freq[idx] = int(freq)

        nodes = sorted(idx2freq.items(), key=lambda x: x[1], reverse=True)
        if DEBUG:
                print (' Index | {} '.format(which))
                for idx, freq in nodes:
                        print( " %4r | %d" % (idx, freq))
                 
        tree = create_tree(nodes)
        huffman_code = huffman_code_tree(tree[0][0])

        if DEBUG:
                print(' Index | {}  | Huffman code '.format(which))
                print("-----------------------------")
                for idx, freq in nodes:
                        print("%-4r | %5d | %12s" % (idx, freq, huffman_code[idx]))

        fn = __gen_fn(book_name, 'h' + which)
        f = open(fn, 'w')
        seq = ''
        for idx, freq in nodes:
                seq += huffman_code[idx]
        f.write(seq)
        f.close()
        print('* Wrote {}'.format(fn))

        p_value = frequency_test(seq)
        print('* {} Test for {}: p-value={}'.format(which, book_name, p_value))

def write_data():
        books = Books.get_books()
        for b in books:
                idx2freq = {} # Map character index to its frequency
                idx2deg = {} # Map character index to vertex degree
                bname = b.get_name()
                
                fn = __gen_fn(bname, 'idx')
                f = open(fn, 'w')
                
                G = b.get_graph()
                idx = 0
                for v in G.vertices():
                        idx += 1
                        idx_str = str(idx)
                        charname = G.vertex_properties["char_name"][v]
                        n = G.vertex_properties["frequency"][v]
                        deg = G.vertex(v).out_degree()
                        
                        f.write(idx_str + ',' + charname + '\n')
                        
                        idx2freq[idx_str] = n
                        idx2deg[idx_str] = deg

                f.close()
                print('* Wrote {}'.format(fn))

                # TEST FREQUENCY
                fn = __gen_fn(bname,'freq')
                f = open(fn, 'w')
                for idx, freq in sorted(idx2freq.items(), key=lambda x: x[1]):
                        f.write(str(idx) + ',' + str(freq) + '\n');
                f.close()
                print('* Wrote {}'.format(fn))

                write_huffman_code(bname, 'freq')
                
                # TEST DEGREE
                fn = __gen_fn(bname,'deg')
                f = open(fn, 'w')
                for idx, deg in sorted(idx2deg.items(), key=lambda x: x[1]):
                        f.write(str(idx) + ',' + str(deg) + '\n');
                f.close()
                print('* Wrote {}'.format(fn))

                write_huffman_code(bname, 'deg')

                
def usage(prg):
        print('''
        Usage: {} -0
        Where:
        -0   write data to output files in /tmp directory.
        '''.format(prg))
                
if __name__ == '__main__':
        if len(sys.argv) == 2:
                if sys.argv[1] == '-0':
                        write_data()
                        exit(1)

        usage(sys.argv[0])
        
