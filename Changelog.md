# Changelog

## [v3.0] - 2019-07-12
- Use pylint3 to reduce warnings and conform to python way of coding.
- Put all scripts in one file charnet/__main__.py.
- Fixes related with python code standard with the help of pylint3 tool.
- Add description of most of classes, methods and functions.
- Substitute plotting library from python matplotlib to gnuplot.
- Add coroutines to generate supplementary material that contains 
  significance levels for the tests applied in the dataset.
- Fix syntax errors in LaTeX generated ouput.

## [v2.0]
- This version was improved compared with version sent to International Journal of Modern Physics C.
  Assortativity mixing formula was fixed and in the Discussion the style of book names was standardized.
- Improve style of plots taking better care of space between labels and axis and the font size of labels.
- Write the plots to [`presentation`](presentation/) directory too.
- Add [`presentation`](presentation/) that is a sub-module pointing to an Overleaf git repository where
  the presentation in LaTeX were written.
- Add [`preprint`](preprint/) that is a sub-module pointing to an Overleaf git repository where
  the preprint in LaTeX was written.

## [v1.2] - 2018-07-05
### Added
- [`data/apollonius.dat`](data/apollonius.dat) - the data from book "Apollonius of Tyana" was added.

### Changed
- [`books.py`](books.py) - add method `get_vertex_color()` to return the color to print the vertex in the graph drawing.
- [`draw.py`](draw.py) - use the method `Book.get_vertex_color()` from `books.py`.
- Fix syntax error of single isolated vertex in [`data/tolkien.dat`](data/tolkien.dat).

## [v1.11] - 2018-05-07
### Changed
- Improve the sequence of commands in [`crypto.mk`](crypto.mk) to exit when an error occurs.

## [v1.1] - 2018-05-07
### Added
- `Project`, `Project.Charnet` and `Project.SGB` classes to handle project configuration
  or properties. This decision allows to set values of general configuration in a single
  point.

### Changed
- The code `books.py` was changed to accommodate the new design.

## [v1.0] - 2018-05-05
### Changed
- Change `README.md`, adding UML class diagram for the project and an explanation
  about the classes.
- Transferred chunk of code responsible to to draw graphs using graphviz
  from `charnet.py` to `draw.py`.
- Transferred chunk of code responsible to output text in TeX format
  from `charnet.py` to `formatting.py`.
- Transferred the chunk of code responsible to process graphs and calculate
  the main measures from `charnet.py` to `graphs.py`.
- Transferred the chunk of code responsible to plot graphics using
  matplotlib from `charnet.py` to `plot.py`.
- The file `charnet.py` was renamed `__main__.py`.
- The code was changed using [Composite](https://github.com/ajholanda/design-patterns)
  pattern.

## [v0.9] 2018-05-04
- Version with code used to generate data evaluated in
  the paper submitted to Physica A.
