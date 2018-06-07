# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](http://keepachangelog.com/en/1.0.0/)
and this project adheres to [Semantic Versioning](http://semver.org/spec/v2.0.0.html).

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
