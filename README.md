# charnet - character networks

This project performed studies using complex networks in some books. We considered
 characters as nodes and characters encounters as edges. The project
 has a [GitHub page](https://ajholanda.github.io/charnet/) and a
 [manuscript](https://arxiv.org/abs/1704.08197).

## Directories content

* `data` - data gathered for the project;
* `sgb` - some data from [Stanford GraphBase](http://www-cs-faculty.stanford.edu/~uno/sgb.html).

## Prerequisites

* Python and the packages:
  * [matplotlib](https://matplotlib.org/);
  * [NetworkX](https://networkx.github.io/);
  * [PyGraphviz](https://pygraphviz.github.io/).

## Structure

The structure of the project follows, mainly, the Composite design
pattern where `Book` is the `Component`, `Books` class is the
`Composite`, and the books like "acts of the apostles" (`Acts`) and
the biography of J. R. R. Tolkien (`Tolkien`) are `Leaf`s.
 
![UML class diagram](dia.png)

- [`Book`](books.py): methods declared here are inherited by `Leaf`
  books, and the main method is `read()` that returns a `Graph`
  containing characters' encounters as edges.

- [`Acts`](books.py): is an example of concrete `Leaf` classes, like
  `Acts` that represents the book "acts of apostles", were coded
  inside inside the file [`books.py`](books.py).

- [`Books`](books.py): is the `Composite` class, `read()` method has a
  different behavior iterating over all `Leaf`s to execute their
  `read()` method.

- [`Formatting`](formatting.py): is responsible to write
  LaTeX-formatted output to append in the paper.

- [`Graphs`](graphs.py): process graphs to obtain measures used in the
  analisys like average degree, betweenness, closeness and lobby.

- [`Graph`](https://networkx.github.io/documentation/stable/reference/classes/graph.html):
  is an instance from `Graph` from NetworkX library.

- [`Plot`](plot.py): plot the curves from data generated from
  graphs.

- [`Draw`](draw.py): draw graphs using graphviz python library.

- [`Lobby`](lobby.py): function to calculate the lobby index.

- [`Main`](__main__.py): client to execute the operations.

## Running

To generate all results and plots, just run:

````
$ make
````

To select a specific target, see the help:

````
$ make help
````

To clean the output generated:

````
$ make clean
````

## Feedback

Please, open an [issue](https://github.com/ajholanda/charnet/issues) for any feeback.

