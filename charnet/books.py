import tempfile
import numpy as np

import logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# LOCAL
from graphs import *

class Project:
        # Where to store files generated by the scripts.
        outdir = tempfile.gettempdir()

        def __init__(self):
                pass

        '''Template for specific project configurations.'''
        @staticmethod
        def get_datadir():
                '''Return the directory containing data for the project.'''
                pass

        @staticmethod
        def get_outdir():
                return Project.outdir

        @staticmethod
        def set_outdir(directory):
                Project.outdir = directory

class SGB(Project):
        '''Handle specific configuration for books gathered by Stanford
           GraphBase project.'''

        def __init__(self):
                Project.__init__(self)

        @staticmethod
        def get_datadir():
                return 'sgb-data/'

class Charnet(Project):
        '''Handle specific configuration for books gathered by Charnet project.'''

        def __init__(self):
                Project.__init__(self)
        @staticmethod
        def get_datadir():
                return 'data/'

from enum import Enum
class BookGenre(Enum):
        '''Books are classified in categories.'''
        BIOGRAPHY = 0
        LEGENDARY = 1 # e.g., Bible
        FICTION = 2

class Book():
        def __init__(self):
                self.G = Graphs.create_graph() # Graph to be created from the book
                self.avg = {} # Dictionary to load average values associated with a centrality as key
                self.was_read = False # if the data file was already parsed, dont do it again

                # Dictionaries to store graph information
                # map vertex index and its label
                self.G.vertex_properties["label"] = self.G.new_vertex_property("string")
                # map vertex 'index' object and its frequency
                self.G.vertex_properties["frequency"] = self.G.new_vertex_property("int")
                # map edge index and its weight
                self.G.edge_properties["weight"] = self.G.new_edge_property("int")
                # map vertex index and its character name
                self.G.vertex_properties["char_name"] = self.G.new_vertex_property("string")
                # map vertex label and its vertex 'index' object
                self.vprop_l2v = {}

                # Store a boolean value indicating if vertex PropertyMap containing degree
                # values was already filled
                self.G.graph_properties["was_vprop_degree_set"] = self.G.new_graph_property("boolean")
                self.G.graph_properties["was_vprop_degree_set"] = False
                # Store degree non-normalized degree of vertices
                self.G.vertex_properties["degree"] = self.G.new_vertex_property("int")

        def __str__(self):
                '''Return the name of the book.'''
                pass

        def set_graph_name(self, name):
                self.G.graph_properties["name"] = self.G.new_graph_property("string")
                self.G.graph_properties["name"] = name

        def get_char_label(self, idx):
                return self.G.vertex_properties["label"][idx]

        def set_char_label(self, idx, label):
                self.G.vertex_properties["label"][idx] = label
                self.vprop_l2v[label] = idx

        def set_char_name(self, idx, char_name):
                self.G.vertex_properties["char_name"][idx] = char_name

        def get_char_idx_from_label(self, label):
                return self.vprop_l2v[label]

        def add_char(self, label, char_name):
                '''Add character labelled with character name in the graph. Map label
                and frequency with index; and character name with label.'''
                v = self.G.add_vertex()
                idx = int(v)
                self.set_char_label(idx, label)
                self.set_char_name(idx, char_name)
                self.G.vertex_properties["frequency"][idx] = 0

        def inc_freq(self, label):
                idx = self.get_char_idx_from_label(label)
                self.G.vertex_properties["frequency"][idx] += 1

        def exists(self, label):
                '''Verify the existence of the label in the dictionary associated with
                the graph. The existence means the label was already inserted in the
                graph G.'''
                if label in self.vprop_l2v:
                        return True
                return False

        def degree(self, label):
                idx = self.get_char_idx_from_label(label)
                return self.G.vertex(idx).out_degree()

        def met(self, char_lbl_a, char_lbl_b):
                '''Return True if character label a (char_lbl_a) have met with character
                label b (char_lbl_b), False otherwise.

                '''
                u = self.get_char_idx_from_label(char_lbl_a)
                v = self.get_char_idx_from_label(char_lbl_b)
                if self.G.edge(u, v) == None:
                        return False
                return True

        def add_encounter(self, char_lbl_a, char_lbl_b):
                u = self.get_char_idx_from_label(char_lbl_a)
                v = self.get_char_idx_from_label(char_lbl_b)
                e = self.G.add_edge(u, v)
                self.G.edge_properties["weight"][e] = 1

        def inc_weight(self, char_lbl_a, char_lbl_b):
                u = self.get_char_idx_from_label(char_lbl_a)
                v = self.get_char_idx_from_label(char_lbl_b)
                e = self.G.edge(u, v)
                self.G.edge_properties["weight"][e] += 1

        def get_weight(self, char_lbl_a, char_lbl_b):
                u = self.get_char_idx_from_label(char_lbl_a)
                v = self.get_char_idx_from_label(char_lbl_b)
                e = self.G.edge(u, v)

                return self.G.edge_properties["weight"][e]

        def get_genre(self):
                pass

        def get_comment_token(self):
                '''Asterisk is used as comment to reflect same convention of SGB (Stanford GraphBase).'''
                return '*'

        def get_file_ext(self):
                '''Return the default file extension.'''
                return '.dat'

        def get_file_name(self):
                '''Return the file name to be read.'''
                return self.get_datadir() + self.__str__() + self.get_file_ext()

        def get_graph(self):
                return self.G

        def get_label(self):
                """Format the label of the book to print in table or plot."""
                return '\emph{' + self.get_raw_book_label() + '}'

        def get_name(self):
                return self.__str__()

        def get_number_characters(self):
                assert self.G
                return len(self.G.vs)

        def get_number_hapax_legomenas(self):
                """
                _Hapax_ _Legomena_ are words with occurrence frequency equals to one.
                """
                assert self.G
                nr_hapaxes = 0
                for v in self.G.vertices():
                        freq = self.G.vertex_properties['frequency'][v]
                        if (freq == 1):
                                nr_hapaxes += 1

                return nr_hapaxes

        def get_number_dis_legomenas(self):
                """
                _Dis_ _Legomena_ are words with occurrence frequency equals to two.
                """
                assert self.G
                nr_dis = 0
                for v in self.G.vertices():
                        freq = self.G.vertex_properties['frequency'][v]
                        if (freq == 2):
                                nr_dis += 1

                return nr_dis

        def get_raw_book_label(self):
                return self.__str__().title()

        def get_vertex_color(self):
                '''Return the color set to vertices in the plot of graph. Default: white.'''
                return 'white'

        def read(self):
                """
                Read the file containing characters encounters of a book
                and return a graph.

                Returns
                -------
                a graph
                """
                are_edges = False
                book_name = self.get_name().title()

                # assert data file is not read several times
                if (self.was_read == False):
                        self.was_read = True
                else:
                        return self.G

                # set graph name
                self.set_graph_name(self.get_name())

                fn = self.get_file_name()
                f = open(fn, "r")
                u = 'AA' # store old vertex label and it is used to check it the order is right
                for ln in f:
                        # ignore comments
                        if (ln.startswith(self.get_comment_token())):
                                continue

                        # edges start after an empty line
                        if (ln.startswith('\n') or ln.startswith('\r')):
                                are_edges = True
                                continue

                        # remove new line
                        ln = ln.rstrip('\r\n')

                        # boolean are_edges indicates if it is inside vertices region
                        if (are_edges==False):
                                (v, character_name) = ln.split(' ', 1)

                                # check the order
                                if u > v:
                                        logger.error('* Labels {} and {} is out of order in {}'.format(u, v, book_name))
                                        exit()

                                #DEBUG
                                logger.debug("* G.add_vertice({}, name={})".format(v, character_name))
                                #GUBED
                                if not self.exists(v):
                                        self.add_char(v, character_name)
                                        u = v
                                else:
                                        logger.error('* Label {} is repeated in book {}.'.format(v, book_name))
                                        exit()
                                continue

                        # edges region from here
                        # eg., split "1.2:ST,MR;ST,PH,MA;MA,DO" => ["1.2" , "ST,MR;ST,PH,MA;MA,DO"]
                        (chapter, edges_list) = ln.split(':', 1)

                        # eg., split "ST,MR;ST,PH,MA;MA,DO" => ["ST,MR", "ST,PH,MA", "MA,DO"]
                        edges = edges_list.split(';')

                        if(edges[0] == ''): # eliminate chapters with no edges
                                continue

                        for e in edges:
                                # eg., split "ST,PH,MA" => ["ST", "PH", "MA"]
                                vs = e.split(',')  # vertices

                                # add vertices to graph G if it does not exit
                                # otherwise, increment frequency
                                for v in vs:
                                        if not self.exists(v):
                                                logger.error('* Label \"{}\" was not added as node in the graph for book {}.'.format(v, book_name))
                                                exit()
                                        else:
                                                self.inc_freq(v)

                                # add characters encounters (edges) to graph G
                                for i in range(len(vs)):
                                        u = vs[i]
                                        for j in range(i+1, len(vs)):
                                                v = vs[j]

                                                # link u--v
                                                eid = -1 # edge id
                                                if not self.met(u, v):
                                                        self.add_encounter(u, v)
                                                else: # u--v already in G, increase weight
                                                        self.inc_weight(u, v)
                                                #DEBUG
                                                action = 'add'
                                                w = self.get_weight(u, v)
                                                if w > 1: action = 'mod'
                                                logger.debug('* G.{}_edge({}, {}, weight={})'.format(action, u, v, w))
                                                #GUBED
                f.close()
                logger.info("* Read G from book \"{}\"".format(book_name))
                return self.G

class Acts(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'acts'

        def get_genre(self):
                return BookGenre.LEGENDARY

        def get_vertex_color(self):
                return 'khaki'

class Apollonius(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'apollonius'

        def get_genre(self):
                return BookGenre.LEGENDARY

        def get_vertex_color(self):
                return 'red'

class Arthur(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'arthur'

        def get_genre(self):
                return BookGenre.FICTION

        def get_vertex_color(self):
                return 'cyan'

class David(Book, SGB):
        def __init__(self):
                Book.__init__(self)
                SGB.__init__(self)

        def __str__(self):
                return 'david'

        def get_genre(self):
                return BookGenre.FICTION

        def get_vertex_color(self):
                return 'orange'

class Dick(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'dick'

        def get_genre(self):
                return BookGenre.BIOGRAPHY

        def get_vertex_color(self):
                return 'orchid'

class Hawking(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'hawking'

        def get_genre(self):
                return BookGenre.BIOGRAPHY

        def get_vertex_color(self):
                return 'silver'

class Hobbit(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'hobbit'

        def get_genre(self):
                return BookGenre.FICTION

        def get_vertex_color(self):
                return 'gold'

class Huck(Book, SGB):
        def __init__(self):
                Book.__init__(self)
                SGB.__init__(self)

        def __str__(self):
                return 'huck'

        def get_genre(self):
                return BookGenre.FICTION

        def get_vertex_color(self):
                return 'salmon'

class Luke(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'luke'

        def get_genre(self):
                return BookGenre.LEGENDARY

        def get_vertex_color(self):
                return 'wheat'

class Newton(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'newton'

        def get_genre(self):
                return BookGenre.BIOGRAPHY

        def get_vertex_color(self):
                return 'tan'

class Pythagoras(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'pythagoras'

        def get_genre(self):
                return BookGenre.LEGENDARY

        def get_vertex_color(self):
                return 'tomato'

class Tolkien(Book, Charnet):
        def __init__(self):
                Book.__init__(self)
                Charnet.__init__(self)

        def __str__(self):
                return 'tolkien'

        def get_genre(self):
                return BookGenre.BIOGRAPHY

        def get_vertex_color(self):
                return 'yellowgreen'

class Books(Book):
        was_already_read = False
        books = [             # row, col
                Dick(),       #  0,  0
                Apollonius(), #  1,  1
                Hobbit(),     #  2,  2
                Tolkien(),    #  3,  0
                Acts(),       #  0,  1
                David(),      #  1,  2
                Newton(),     #  2,  0
                Pythagoras(), #  3,  1
                Arthur(),     #  0,  2
                Hawking(),    #  1,  0
                Luke(),       #  2,  1
                Huck(),       #  3,  2
        ]

        genre_names = ['Biography', 'Legendary', 'Fiction']

        @staticmethod
        def get_genre_label(book):
                gen = book.get_genre()
                if (gen == BookGenre.BIOGRAPHY):
                        return 'B'
                elif (gen == BookGenre.LEGENDARY):
                        return 'L'
                elif (gen == BookGenre.FICTION):
                        return 'F'
                else:
                        logger.error('* Unknown book: \"{}\"'.format(book.get_name()))
                        exit()

        @staticmethod
        def get_genre_name(idx):
                return Books.genre_names[idx]

        @staticmethod
        def get_genre_enums():
                return np.arange(0,len(Books.genre_names))

        @staticmethod
        def get_books():
                if Books.was_already_read == False:
                        Books.was_already_read = True
                        logger.info("\n\t#### PRE-PROCESSING ####")
                        for book in Books.books:
                                book.read()
                return Books.books
