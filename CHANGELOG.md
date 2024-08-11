# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

None

## [1.2.2] - 2024-08-11
- Add py.typed marker (PEP-561) (#9)
- Remove setuptools, wheel from build-system (#7)

## [1.2.1] - 2023-02-20

### Changed
- Update dependencies to support Python 3.11 to match Home Assistant CI

## [1.2.0] - 2023-02-20

### Changed
- Update supported Python to 3.8-3.10
- Update project to use `poetry-core` (from @fabaff)
- Update to force HTTPS since AirNow requires HTTPS as of Feb 3rd 2023 (from @stephenjamieson)

## [1.1.0] - 2020-09-13

### Added
- Added conversion helpers between AQI and Pollutant Concentration

## [1.0.1] - 2020-09-13

### Changed
- Fixed GitHub Publish workflow

[unreleased]: https://github.com/asymworks/pyairnow/compare/v1.2.1...HEAD
[1.2.1]: https://github.com/asymworks/pyairnow/compare/v1.2.0...v1.2.1
[1.2.0]: https://github.com/asymworks/pyairnow/compare/v1.1.0...v1.2.0
[1.1.0]: https://github.com/asymworks/pyairnow/compare/v1.0.1...v1.1.0
[1.0.1]: https://github.com/asymworks/pyairnow/releases/tag/v1.0.1
