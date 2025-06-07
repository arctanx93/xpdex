# xpdex

xpdex is a Python script that extracts individual PCM files from a PDX file — the PCM data file format used by the MXDRV sound driver, known on the X680x0 computer series.  
Originally, this tool was intended to enable music data development in environments outside of the X680x0, without relying on emulators. However, if Emscripten and similar tools allow original MDX/PDX development environments to run in web browsers, that purpose may already be fulfilled.

## Specifications

The script is designed based on the following specifications, although actual behavior may differ. Use with caution.

- Supports the EX-PDX format (detection may not always be accurate).
- Attempts to extract from PDX files even when headers are non-standard, such as:
  - Header size is not a multiple of 768 bytes (e.g., 208 or 1024 bytes).
  - PCM data with higher note numbers placed before those with lower note numbers.
  - Extra empty header banks are appended.
- Error checking is partial or sometimes nonexistent depending on the area.
  - Please back up your important files before running the script to avoid potential data loss.
  - Avoid specifying non-PDX files, as format checking is not strict and may lead to problems.
- Behavior or results may differ from other `pdex`-like software due to bugs or implementation differences.
- Additional behaviors may be inferred from reading the source code—but note that the messy source is part of the spec.
- This script was created as part of the author's learning process with Python; please excuse the code quality.
- Many parts of the code and documentation may not follow standard coding practices.
- **This program is provided as-is, with no warranty.**

## Requirements

- Python 3 environment (Python 2 is not supported/tested).
- Should work with only standard libraries, although results may vary by Python version.
- Verified to run on Python 3.9.16 in Cygwin64 on Windows 11 by the author.
- You may optionally add a shebang line suitable for your environment.

## Usage

```plain
$ python xpdex.py --help
usage: xpdex.py [-h] [-f] [-p [PREFIX]] [-v] [-V] PDX_filename [pcm_num ...]

Extract PCM file(s) from a PDX file.

positional arguments:
  PDX_filename          specify PDX filename
  pcm_num               specify PCM number to extract (0-8255)

optional arguments:
  -h, --help            show this help message and exit
  -f, --force           force to overwrite pcm file(s)
  -p [PREFIX], --prefix [PREFIX]
                        specify prefix of PCM files
  -v, --verbose         increase verbose level
  -V, --version         show program's version number and exit

Copyright (c) 2023-2025 ArctanX
```

The following behaviors are expected, but may not always perform as intended:

- Extracts component PCM files from the specified PDX file.
  - For non-EX-PDX files, the number part of the PCM filename will be 2 digits (e.g., `00.pcm`).
  - For EX-PDX files, it will be 5 digits (e.g., `00000.pcm`).
- One or more PCM numbers (0–8255) can be specified, separated by spaces (e.g., `1 5 7 123 4096`).
  - If no numbers are given, it will attempt to extract all PCM files in the PDX.
  - Order doesn’t matter; extraction will occur in ascending PCM number order.
  - PCM numbers not found in the file are ignored without error.
  - Musical note notation (`o4c`, etc.) and bank numbers are not supported.
- If the specified PDX file is not found, `.pdx` or `.PDX` will be appended and retried automatically.

### Options

- `-h`: Display help and exit.
- `-f`: Force overwrite of output files without confirmation.
  - If not specified, confirmation is required before overwriting (default).
- `-p`: Adds a prefix to the output PCM filenames.
  - `-p foo` results in filenames like `foo00.pcm`, `foo01.pcm`, etc.
  - If only `-p` is provided, the PDX filename is used as the prefix.  
    For example, `bar.pdx` results in `bar_00.pcm`, `bar_01.pcm`, etc.
    - For EX-PDX, the number part becomes 5 digits.
  - This option must be specified before other options or at the very end of the command to avoid misbehavior.
- `-v`: Increase verbosity level.
  - Usually `-v` or `-vv` is enough; `-vvv` or higher is for the curious.
- `-V`: Show program version and exit.

## Acknowledgments

The documentation for `tpdex` and `bpdex` was a valuable reference during feature planning and development.  
Many thanks to the original authors.

## Author

[ArctanX](https://github.com/arctanx93)

## License

MIT License  
© 2023–2025 ArctanX
