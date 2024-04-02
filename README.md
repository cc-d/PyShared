# PyShared

PyShared is a Python utility library providing a collection of functions and constants I've found useful across multiple projects.

## Installation

To incorporate PyShared into your project, use pip for installation:

```bash
pip install pyshared
# To include development dependencies:
pip install pyshared[dev]
```

## Feature Overview

### `consts.py`

- `ALPHANUMERIC_CHARS`: A string of alphanumeric characters.
- `ALPHANUMERIC_EXT_CHARS`: Alphanumeric characters, including underscores and hyphens.

### `crypto.py`

- `is_jwt`: Simply verifies if a string looks like a JSON Web Token (JWT)

### `env.py`

- `typed_evar`: Retrieves and type-casts environment variables.

### `exceptions.py`

- `NotPrintableError`: Both str and repr methods raised exceptions.

### `python.py`

- `ranstr`: Creates random strings of specified length and character set.
- `safe_repr`: Safely returns the object's repr/str or an error string without throwing exceptions if the object is not printable.
- `default_repr`: Generates a default representation for custom objects.
- `truncstr`: Truncates a string, preserving a portion from the start and/or end.

### `pytest.py`

- `multiscope_fixture`: Creates multiple scoped pytest fixture and ensures the fixtures are available in the module.

### `shell.py`

Shell command execution within Python.

- `runcmd`: Executes a command in the system shell.

### `terminal.py`

Terminal utilities for improved user interaction.

- `get_terminal_width`: Safely retrieves the terminal width, defaulting to 80 columns on failure.
- `print_middle`: Centers text within left/right padding based on terminal width.
- `print_columns`: Arranges a list of strings into guestimated $x length strings based on what is approximately optimal for the contents/terminal width.

## Test Coverage

100% lol

```
---------- coverage: platform darwin, python 3.9.18-final-0 ----------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
pyshared/__init__.py         9      0   100%
pyshared/consts.py           3      0   100%
pyshared/crypto.py          21      0   100%
pyshared/env.py             26      0   100%
pyshared/exceptions.py       8      0   100%
pyshared/pytest.py          11      0   100%
pyshared/python.py          45      0   100%
pyshared/shell.py            9      0   100%
pyshared/terminal.py        34      0   100%
pyshared/version.py          1      0   100%
------------------------------------------------------
TOTAL                      167      0   100%
```

## License

MIT

## Contact

ccarterdev@gmail.com
