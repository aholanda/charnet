""""Experimental tests using Huffman code to separate genres
according to Huffman tree properties."""
#!/usr/bin/python3

import sys
import math

from charnet.books import Books

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
    """Calculate the frequency of the string in the sequence."""
    # Frequency (Monobit) test
    s_val = 0
    eps = str_bin_seq
    len_str = len(eps)
    for i in range(len_str):
        n_bits = int(eps[i])
        s_val += (1 + ((1 - n_bits) * -2))
    s_obs = math.fabs(s_val) / math.sqrt(len_str)
    return math.erfc(s_obs/math.sqrt(2))

class NodeTree(object):
    """Class to represent a tree node."""
    def __init__(self, left=None, right=None):
        """Initialize a new node."""
        self.left = left
        self.right = right

    def children(self):
        """Children of a node."""
        return (self.left, self.right)

    def nodes(self):
        """Nodes of the tree."""
        return (self.left, self.right)

    def __str__(self):
        """Convert class information to string."""
        return "%s_%s" % (self.left, self.right)

## Tansverse the NodeTress in every possible way to get codings
def huffman_code_tree(node, left=True, bin_string=""):
    """Produce Huffman code tree."""
    if isinstance(node) is str:
        return {node: bin_string}
    (left, right) = node.children()
    _dict = dict()
    _dict.update(huffman_code_tree(left, True, bin_string + "0"))
    _dict.update(huffman_code_tree(right, False, bin_string + "1"))
    return _dict

def create_tree(nodes):
    """Produce the tree according to the entry."""
    while len(nodes) > 1:
        key1, bit1 = nodes[-1]
        key2, bit2 = nodes[-2]
        nodes = nodes[:-2]
        node = NodeTree(key1, key2)
        nodes.append((node, bit1 + bit2))
        # Re-sort the list
        nodes = sorted(nodes, key=lambda x: x[1], reverse=True)
    return nodes

def write_huffman_code(book_name, which):
    """Produce Huffman code."""
    idx2freq = {}
    file_name = __gen_fn(book_name, which)
    _file = open(file_name, 'r')
    for line in _file:
        line = line.rstrip('\r\n')
        (idx, freq) = line.split(',', 1)
        idx2freq[idx] = int(freq)
    nodes = sorted(idx2freq.items(), key=lambda x: x[1], reverse=True)
    if DEBUG:
        print (' Index | ' + which)
        for idx, freq in nodes:
            print (" %4r | %d" % (idx, freq))
    tree = create_tree(nodes)
    huffman_code = huffman_code_tree(tree[0][0])
    if DEBUG:
        print (' Inde   x | ' + which +  '  | Huffman code ')
        print ('-----------------------------')
        for idx, freq in nodes:
            print ("%-4r | %5d | %12s" % (idx, freq, huffman_code[idx]))
    file_name = __gen_fn(book_name, 'h' + which)
    _file = open(file_name, 'w')
    seq = ''
    for idx, freq in nodes:
        seq += huffman_code[idx]
    _file.write(seq)
    _file.close()
    print ('* Wrote ' + file_name)
    p_value = frequency_test(seq)
    print ('* ' + which + ' Test for ' + book_name + ': p-value=' + p_value)

def write_data():
    """Write Huffman data to output."""
    books = Books.get_books()
    for book in books:
        idx2freq = {} # Map character index to its frequency
        idx2deg = {} # Map character index to vertex degree
        bname = book.get_name()
        file_name = __gen_fn(bname, 'idx')
        _file = open(file_name, 'w')
        graph = book.get_graph()
        idx = 0
        for vert in graph.vertices():
            idx += 1
            idx_str = str(idx)
            charname = graph.vertex_properties["char_name"][vert]
            n_verts = graph.vertex_properties["frequency"][vert]
            deg = graph.vertex(vert).out_degree()
            _file.write(idx_str + ',' + charname + '\n')
            idx2freq[idx_str] = n_verts
            idx2deg[idx_str] = deg
        _file.close()
        print ('* Wrote ' + file_name)
        # TEST FREQUENCY
        file_name = __gen_fn(bname, 'freq')
        _file = open(file_name, 'w')
        for idx, freq in sorted(idx2freq.items(), key=lambda x: x[1]):
            _file.write(str(idx) + ',' + str(freq) + '\n')
        _file.close()
        print ('* Wrote ' + file_name)
        write_huffman_code(bname, 'freq')
        # TEST DEGREE
        file_name = __gen_fn(bname, 'deg')
        _file = open(file_name, 'w')
        for idx, deg in sorted(idx2deg.items(), key=lambda x: x[1]):
            _file.write(str(idx) + ',' + str(deg) + '\n')
        _file.close()
        print ('* Wrote ' + file_name)
        write_huffman_code(bname, 'deg')

def usage(prg):
    """How to use the program."""
    print ('''
    Usage: {} -0
    Where:
    -0   write data to output files in /tmp directory.
    '''.format(prg))

if __name__ == '__main__':
    if len(sys.argv) == 2:
        if sys.argv[1] == '-0':
            exit(1)
            write_data()
    usage(sys.argv[0])
