# Changelog

## [v1.2] - 2018-07-05
## Added
- [`data/apollonius.dat`](data/apollonius.dat) - the data from book "Apollonius fo Tyana" was added.

### Changed
- [`books.py`](books.py) - add method `get_vertex_color()` to return the color to print the vertex in the graph drawing.
- [`draw.py`](draw.py) - use the method `Book.get_vertex_color()` from `books.py`.
- Fix syntax error of single isolated vertex in [`data/tolkien.dat`](data/tolkien.dat).

## [v1.11] - 2018-05-07
### Changed
- Improve the sequence of commands in [`crypto.mk`](crypto.mk) to exit when an error occur.

## [v1.1] - 2018-05-07
### Added
- `Project`, `Project.Charnet` and `Project.SGB` classes to handle project configuration
  or properties. This decision allows to set values of general configuration in a single
  point.

### Changed
- The code `books.py` was changed to accomodate the new design.

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
