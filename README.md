# charnet - character networks

This project performed studies using complex networks in some books. We considered
 characters as nodes and characters encounters as edges. The project
 has a [GitHub page](https://ajholanda.github.io/charnet/), a
 [manuscript](https://arxiv.org/abs/1704.08197) and a 
 [presentation](https://pt.overleaf.com/read/vszbrbjcbtpq).

## Directories content

* [`_assets`](_assets/) - files used to document or manage the project;
* [`charnet`](charnet/) - Python code for the project;
* [`data`](data/) - data gathered for the project;
* [`sgb-data`](sgb-data/) - some data from [Stanford GraphBase](http://www-cs-faculty.stanford.edu/~uno/sgb.html).

## Prerequisites

* [Gnuplot](http://www.gnuplot.info/): mixed with jinja2 template engine
    to produce graphics with excellent quality;
* Python and the packages:
  * [jinja2](http://jinja.pocoo.org/docs/2.10/) - template engine used to handle intervene code;
  * [graph-tool](https://graph-tool.skewed.de/) - used to calculate the network measures and draw the graphs;
  * `numpy` and `scipy`.

## Structure

The structure of the project in [`charnet/`](charnet/) follows,
mainly, the Composite design pattern where `Book` is the `Component`,
`Books` class is the `Composite`, and the books like "acts of the
apostles" (`Acts`) and the biography of J. R. R. Tolkien (`Tolkien`)
are `Leaf`s.
 
![UML class diagram](dia.png)

- [`Book`](charnet/__main__.py): methods declared here are inherited by `Leaf`
  books, and the main method is `read()` that returns a `Graph`
  containing characters' encounters as edges.

- [`Acts`](charnet/__main__.py): is an example of concrete `Leaf` classes, like
  `Acts` that represents the book "acts of apostles", were coded
  inside inside the file [`books.py`](books.py).

- [`Books`](charnet/__main__.py): is the `Composite` class, `read()` method has a
  different behavior iterating over all `Leaf`s to execute their
  `read()` method.

- [`Formatting`](charnet/__main__.py): is responsible to write
  LaTeX-formatted output to append in the paper.

- [`Graphs`](charnet/__main__.py): process graphs to obtain measures used in the
  analisys like average degree, betweenness, closeness and lobby.

- `Graph`: is a `Graph` instance from graph-tool library.

- [`Plot`](charnet/__main__.py): plot the curves from data generated from
  graphs.

- [`Draw`](charnet/__main__.py): draw graphs using graphviz python library.

- [`lobby()`](charnet/__main__.py): function to calculate the lobby index.

- [`Charnet`](charnet/__main__.py): helper to handle configuration specific to
  books gathered in this project.

- [`SGB`](charnet/__main__.py): helper to handle configuration specific to books
  gathered in Stanford GraphBase project.

- [`Project`](charnet/__main__.py): template (interface) for project properties.

- [`main`](__main__.py): client to execute the operations.

## Running

Install `graph-tool` according to your setup by following the
[installation instructions](https://git.skewed.de/count0/graph-tool/wikis/installation-instructions).


Download the charnet using `git` and enter in the `charnet` directory:

````
$ git clone https://github.com/ajholanda/charnet.git && cd charnet
````

To install the dependencies, the easy way is to run

````
$ python3 setup.py install --user
````

Install [graph-tools](https://git.skewed.de/count0/graph-tool/wikis/installation-instructions) and run all the project tasks:

````
$ python3 charnet -a
````

To print the possible tasks to be performed apart:

````
$ python3 charnet -h
````

To clean the generated files:

````
$ python setup.py clean --all
````

## Feedback

Please, open an [issue](https://github.com/ajholanda/charnet/issues) for any feeback.
