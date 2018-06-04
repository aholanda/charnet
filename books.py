import numpy as np

# LOCAL
from graphs import *

from enum import Enum
class BookCategory(Enum):
        FICTION = 1
        BIOGRAPHY = 2
        CANONICAL = 3
        
class Book:
        def __init__(self):
                self.G = Graphs.create_graph() # Graph to be created from the book
                self.avg = {} # Dictionary to load average values associated with a centrality as key
                
        def get_basedir(self):
                '''Return the default base directory containing data for the project.'''
                return 'data/'

        def get_category(self):
                pass
        
        def get_comment_token(self):
                '''Asterisk is used as comment to reflect same convention of SGB (Stanford GraphBase).'''
                return '*'
        
        def get_file_ext(self):
                '''Return the default file extension.'''
                return '.dat'

        def get_file_freq_ext(self):
                '''Return the character frequency file extension.'''
                return '.freq'

        def get_file_name(self):
                '''Return the file name to be read.'''
                return self.get_basedir() + self.__str__() + self.get_file_ext()

        def get_file_name_freq(self):
                '''Return the file name with character frequency to be read.'''
                return self.get_basedir() + self.__str__() + self.get_file_freq_ext()
        
        def has_frequency_file(self):
                '''Return if the book has a file containg character frequency.'''
                pass
        
        def get_graph(self):
                return self.G

        def get_label(self):
                """Format the label of the book to print in table or plot."""
                return '\emph{' + self.get_raw_book_label() + '}'

        def get_name(self):
                return self.__str__()
        
        def get_number_characters(self):
                return self.nr_chars

        def get_number_hapax_legomenas(self):
                """
                _Hapax_ _Legomena_ are words with occurrence frequency equals to one.
                """
                nr_hapaxes = 0
                for name, freq in self.name_freqs.items():
                        if (freq == 1):
                                nr_hapaxes += 1

                return nr_hapaxes

        def get_number_dis_legomenas(self):
                """
                _Dis_ _Legomena_ are words with occurrence frequency equals to two.
                """
                nr_dis = 0
                for name, freq in self.name_freqs.items():
                        if (freq == 2):
                                nr_dis += 1

                return nr_dis
        
        def get_raw_book_label(self):
                return self.__str__().title()
        
        def read(self):
                """
                Read the file containing characters encounters of a book 
                and return a graph.
                
                Returns
                -------
                networkx graph
                """
                self.code_names = {}
                self.name_idxs = {}
                self.name_freqs = {}
                next_idx = 0
                arcs = {}
                are_edges = False

                fn = self.get_file_name()
                f = open(fn, "r")
                print(' o', fn)
                for ln in f:
                        if (ln.startswith(self.get_comment_token())): # ignore comments
                                continue

                        if (ln.startswith('\n') or ln.startswith('\r')): # edges start after empty line
                                are_edges = True
                                continue
                                
                        if (are_edges==False):
                                (code, charname) = ln.split(' ', 1)
                                self.code_names[code] = charname
                                continue

                        # edges region from here
                        # eg., split "1.2:ST,MR;ST,PH,MA;MA,DO" => ["1.2" , "ST,MR;ST,PH,MA;MA,DO"]
                        (chapter, edges_list) = ln.split(':', 1)

                        # eg., split "ST,MR;ST,PH,MA;MA,DO" => ["ST,MR", "ST,PH,MA", "MA,DO"]
                        edges = edges_list.rstrip("\n").split(';')

                        for e in edges:
                                # eg., split "ST,PH,MA" => ["ST", "PH", "MA"]
                                vs = e.split(',')  # vertices

                                # assign an index to label, if does not exist
                                # otherwise, increment frequency
                                for v in vs:
                                        if (v in self.name_idxs.keys()):
                                                self.name_freqs[v] += 1
                                        else:
                                                self.name_idxs[v] = next_idx
                                                next_idx += 1
                                                self.name_freqs[v] = 1

                                                
                                # add characters encounters linked (adjacency list) in a dictionary
                                for i in range(len(vs)):
                                        u = vs[i]
                                        if (u not in arcs.keys()):
                                                arcs[u] = []
                                    
                                        for j in range(i+1, len(vs)):
                                                v = vs[j]
                                                arcs[u].append(v)
                f.close()
                
                self.nr_chars = next_idx

                # Some files in `data/` directory with ".freq" extension contains characters'
                # frequency already counted during data compilation. For the books that
                # don't have this file in `data/`, this file are generated and written
                # in a file with the same extension. The file has the following format:
                
                # ````
                # Sir Isaac Newton;4
                # ````
                
                # where "`;`" is the separator, the first column is the character name and
                # the second the frequency.
                if (self.has_frequency_file()==True):
                        name_freqs = {}
                        fn = self.get_file_name_freq()

                        f = open(fn, "r")
                        for ln in f:
                                (vname, freq) = ln.rstrip("\n").split(';')
                                name_freqs[vname] = int(freq)
                        f.close()                        

                # name the Graph
                self.get_graph().graph['name'] = self.get_name()
                
		# name the vertices
                for name, idx in self.name_idxs.items():
                        self.G.add_node(idx, name=name)
			
		# add the edges
                for u_name, vs in arcs.items():
                        u = self.name_idxs[u_name]
                        for v_name in vs:
                                v = self.name_idxs[v_name]

                                if (self.G.has_edge(u, v)==True): # increase weight
                                        self.G[u][v]['weight'] += 1
                                else: # add edge with weight = 1
                                        self.G.add_edge(u, v, weight=1)
                                
                return self.G

        def __str__(self):
                '''Return the name of the book.'''
                pass

        
class Acts(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return False

        def get_category(self):
                return BookCategory.CANONICAL
        
        def __str__(self):
                return 'acts'

class Arthur(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return False

        def get_category(self):
                return BookCategory.BIOGRAPHY
        
        def __str__(self):
                return 'arthur'

class David(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return False

        def get_basedir(self):
                '''Return the base directory containing SGB data for the project.'''
                return 'sgb/'

        def get_category(self):
                return BookCategory.FICTION
        
        def __str__(self):
                return 'david'

class Dick(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return False

        def get_category(self):
                return BookCategory.BIOGRAPHY
        
        def __str__(self):
                return 'dick'

class Hawking(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return True

        def get_category(self):
                return BookCategory.BIOGRAPHY
        
        def __str__(self):
                return 'hawking'

class Hobbit(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return False

        def get_category(self):
                return BookCategory.FICTION
        
        def __str__(self):
                return 'hobbit'

class Huck(Book):
        def __init__(self):
                Book.__init__(self)
                
        def get_basedir(self):
                '''Return the base directory containing SGB data for the project.'''
                return 'sgb/'

        def get_category(self):
                return BookCategory.FICTION
        
        def has_frequency_file(self):
                return False

        def __str__(self):
                return 'huck'

class Luke(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return False

        def get_category(self):
                return BookCategory.CANONICAL
        
        def __str__(self):
                return 'luke'

class Newton(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return True

        def get_category(self):
                return BookCategory.BIOGRAPHY
        
        def __str__(self):
                return 'newton'

class Pythagoras(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return True

        def get_category(self):
                return BookCategory.BIOGRAPHY
        
        def __str__(self):
                return 'pythagoras'

class Tolkien(Book):
        def __init__(self):
                Book.__init__(self)
                
        def has_frequency_file(self):
                return False

        def get_category(self):
                return BookCategory.BIOGRAPHY
        
        def __str__(self):
                return 'tolkien'
                
class Books(Book):
        def __init__(self):
                self.books = [Acts(), Arthur(), David(), Dick(), Hawking(), Hobbit(),
                              Huck(), Luke(), Newton(), Pythagoras(), Tolkien()]

        def get_books(self):
                return self.books

        def read(self):
                for book in self.books:
                        book.read()
