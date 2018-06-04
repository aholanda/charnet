#import matplotlib.pyplot as plt
import networkx as nx
#from lobby import lobby

from enum import Enum
class BookCategory(Enum):
        FICTION = 1
        BIOGRAPHY = 2
        SACRED = 3
        
class Book:
        def get_basedir(self):
                '''Return the default base directory containing data for the project.'''
                return 'data/'

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
                return self.get_basedir() + self.__str__() + self.get_file_freq_ext()

        def get_file_name_freq(self):
                '''Return the file name with character frequency to be read.'''
                return self.get_basedir() + self.__str__() + self.get_file_ext()

        def has_frequency_file(self):
                '''Return if the book has a file containg character frequency.'''
                pass
        
        #@abstractmethod
        def read(self):
                """
                Read the file containning characters encounters of a book 
                and return a graph.
                
                Returns
                -------
                networkx graph
                """
                code_names = {}
                name_idxs = {}
                next_idx = 0
                arcs = {}
                are_edges = False
                
                fn = self.get_file_name()
                f = open(fn, "r")
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
                                        if (name_idxs.has_key(v)==False):
                                                name_idxs[v] = next_idx
                                                next_idx += 1
                                                self.name_freqs[v] = 1
                                        else:
                                                self.name_freqs[v] += 1
                                                
                                # add characters encounters linked (adjacency list) in a dictionary
                                for i in range(len(vs)):
                                        u = vs[i]
                                        if (arcs.has_key(u)==False):
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

                G = nx.Graph()
                G.graph['name'] = self.name
                
		# name the vertices
                for name, idx in name_idxs.items():
                        G.add_node(idx, name=name)
			
		# add the edges
                for u_name, vs in arcs.items():
                        u = name_idxs[u_name]
                        for v_name in vs:
                                v = name_idxs[v_name]

                                if (G.has_edge(u, v)==True): # increase weight
                                        G[u][v]['weight'] += 1
                                else: # add edge with weight = 1
                                        G.add_edge(u, v, weight=1)
                                
                return G

        #@abstractmethod
        def __str__(self):
                '''Return the name of the book.'''
                pass

        
class Acts(Book):
        def has_frequency_file(self):
                return False
        
        def __str__(self):
                return 'acts'

        def read(self):
                super(Acts, self).read()

class Books(Book):
        def read(self):
                a = Acts()
                a.read()
