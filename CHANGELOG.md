# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

---

## [Unreleased]

---

## [0.9.0] - 2025-06-08

### Added

- Initial commit for GitHub.

### Changed

- Showed PDX header information for only specified PCM numbers with `-vv` option.
- Changed the name of the program from pdxex to xpdex.

---

## [0.8.0] - 2024-06-01

### Added

- Completed `.pdx` / `.PDX` suffix when needed.

### Changed

- Changed some functions to class methods.

---

## [0.7.0] - 2023-11-15

### Changed

- Allowed to specify PCM numbers without the `-n` option.

### Removed

- Removed `-n` option.

---

## [0.6.0] - 2023-10-01

### Changed

- Improved error checking and error/exception handling.

---

## [0.5.0] - 2023-10-01

### Added

- Added the `-f` option to force overwrite PCM files.

### Changed

- Refactored code.

---

## [0.4.0] - 2023-07-30

### Added

- Added the `-p` option to specify the prefix of PCM files.

---

## [0.3.0] - 2023-07-24

### Changed

- Improved handling of PDX files with incomplete headers (< 768 bytes), trailing empty banks, etc.

---

## [0.2.0] - 2023-07-23

### Added

- Partially supported PDX files without sufficient header size.

---

## [0.1.0] - 2023-07-23

### Added

- First working version that extracts PCM files from `bos.pdx`.
