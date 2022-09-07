# Changelog
All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased] - 2022-09-07

### Added
  
### Changed

### Deprecated

### Removed

### Fixed

### CI/CD


## [2.3.0] - 2022-09-07

### Added
* User-configurable ordering of the bibliometrics.
* User-configurable exclusions (e.g., if user wishes to exclude one or more of the bibliometrics).

### Fixed
* Changed the default order of the bibliometrics, moving e-index to the last bibliometric, to
  improve the appearance since it is the only one of the bibliometrics that is a real-value, 
  where the others are all integers.


## [2.2.0] - 2022-08-26

### Added
* Calculation of e-index.


## [2.1.1] - 2022-08-01

### Fixed
* Reordered the bibliometrics, moving g-index immediately after h-index, which looks better
  for cases when several of i10, i100, i1000, and i10000 are non-zero.


## [2.1.0] - 2022-07-16

### Added
* Calculation of i100-index, i1000-index, and i10000-index, with inclusion in SVG for any of
  these that are greater than 0.


## [2.0.0] - 2022-06-30

**BREAKING CHANGES** Entry point has changed--now runs as a module rather than a script.

### Added
* First release available via PyPI.
  
### Changed
* Restructured code into a Python module enabling installing and running with `-m` flag.
* Minor refactoring for miscellaneous improvements.

### CI/CD
* Enabled publishing to PyPI on all GitHub releases.
* Enabled CodeQL analysis on all push and pull-request events.


## [1.1.0] - 2022-06-10

### Added
* Inserted Scholar logo to two upper corners.


## [1.0.0] - 2022-06-08

Initial release.
