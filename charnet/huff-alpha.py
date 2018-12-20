#!/usr/bin/python3

# Experimental script to test some ideas

import sys
import queue

from books import Books

class HuffmanNode(object):
        def __init__(self, left=None, right=None, root=None):
                self.left = left
                self.right = right
                self.root = root     # Why?  Not needed for anything.
                
        def children(self):
                return((self.left, self.right))

def create_tree(frequencies):
        p = queue.PriorityQueue()

        for val in frequencies:    # 1. Create a leaf node for each symbol
                print(val)
                p.put(val)             #    and add it to the priority queue
        while p.qsize() > 1:         # 2. While there is more than one node
                l, r = p.get(), p.get()  # 2a. remove two highest nodes
                node = HuffmanNode(l, r) # 2b. create internal node with children
                p.put((l[0]+r[0], node)) # 2c. add new node to queue      
        return p.get()               # 3. tree is complete - return root node

def walk_tree(node, prefix="", code={}):
        if isinstance(node[1].left[1], HuffmanNode):
                walk_tree(node[1].left,prefix+"0", code)
        else:
                code[node[1].left[1]]=prefix+"0"
        if isinstance(node[1].right[1],HuffmanNode):
                walk_tree(node[1].right,prefix+"1", code)
        else:
                code[node[1].right[1]]=prefix+"1"
        return(code)

def write_huffman_code(fn):
        freqidxs = []
        f = open(fn, 'r')
        for ln in f:
                 ln = ln.rstrip('\r\n')
                 (idx, freq) = ln.split(',', 1)
                 freqidxs.append((int(freq), int(idx)))

        tree = create_tree(freqidxs)
        code = walk_tree(tree)
                 
        for i in sorted(freq, reverse=True):
                print(i[1], '{}'.format(i[0]), code[i[1]])

def write_data():
        books = Books.get_books()
        for b in books:
                idx2freq = {}
                bname = b.get_name()
                
                fn = '/tmp/' + bname +  '-index.txt'
                f = open(fn, 'w')
                
                G = b.get_graph()
                idx = 0
                for v in G.vertices():
                        idx += 1
                        idx_str = str(idx)
                        n = G.vertex_properties["frequency"][v]
                        charname = G.vertex_properties["char_name"][v]
                        
                        f.write(idx_str + ',' + charname + '\n')
                        
                        idx2freq[idx] = n

                f.close()
                print('* Wrote {}'.format(fn))
                
                fn = '/tmp/' + bname +  '-freq.txt'
                f = open(fn, 'w')
                for idx, freq in sorted(idx2freq.items(), key=lambda x: x[1]):
                        f.write(str(idx) + ',' + str(freq) + '\n');
                f.close()
                print('* Wrote {}'.format(fn))

def usage(prg):
        print('''
        Usage: {} -0|-1 </tmp/book_name-freq.txt>
        Where:
        -0   write data to output files in /tmp directory.
        -1   analize the data
        '''.format(prg))
                
if __name__ == '__main__':
        if len(sys.argv) == 2:
                if sys.argv[1] == '-0':
                        write_data()
                        exit(1)

        if len(sys.argv) == 3:
                if sys.argv[1] == '-1':
                        fn = sys.argv[2]
                        write_huffman_code(fn)
                        
        usage(sys.argv[0])
        
