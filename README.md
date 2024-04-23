# PyShared

PyShared is a Python utility library providing a collection of functions and constants I've found useful across multiple projects.

It also has several common aliases I use for typehints and common imports.

## Installation

To incorporate PyShared into your project, use pip for installation:

```bash
pip install pyshared
# To include development dependencies:
pip install pyshared[dev]
```

## Feature Overview

### `args.py`

-

### `consts.py`

- `ALPHANUMERIC_CHARS`: A string of alphanumeric characters.
- `ALPHANUMERIC_EXT_CHARS`: Alphanumeric characters, including underscores and hyphens.

### `crypto.py`

- `is_jwt`: Simply verifies if a string looks like a JSON Web Token (JWT)

### `env.py`

- `typed_evar`: Retrieves and type-casts environment variables.

Examples: (input, default, type, expected_output)

```
'evname, ev, default, vartype, expected',
    # with default arg
    ('evname', '0', 0, None, 0),
    # this shouldnt ever happen but if it does, it should raise error
    (None, None, '20.1', int, ValueError),
    (None, None, None, float, ValueError),
    # assumed typing
    ('evname', '0.0', None, None, 0.0),
    ('evname', '0.', None, None, '0.'),
    ('evname', '.0', None, None, 0.0),
    ('evname', 'True', None, None, True),
    ('evname', 'tRuE', None, None, True),
    ('evname', 'false', None, None, False),
    ('evname', 'fAlSe', None, None, False),
    ('evname', '0', None, None, 0),
    ('evname', '0', True, None, False),
    ('evname', '0', False, None, False),
    ('evname', '0', None, bool, True),
    ('evname', '0', None, int, 0),
    ('evname', '0', 1.0, float, 0.0),
    ('evname', '0', None, float, 0.0),
    ('evname', 'true', None, str, 'true'),
    ('evname', 'test', True, None, ValueError),
    ('evname', 'test', None, int, ValueError),
    ('evname', 'test', 1, None, ValueError),
```

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

### `tests.py`

- `RanData`: A class for generating random data for testing purposes.

## Test Coverage

not quite 100% lol

```
---------- coverage: platform darwin, python 3.9.18-final-0 ----------
Name                     Stmts   Miss  Cover   Missing
------------------------------------------------------
pyshared/__init__.py        17      0   100%
pyshared/consts.py           3      0   100%
pyshared/crypto.py          21      0   100%
pyshared/env.py             34      3    91%   30, 42, 54
pyshared/exceptions.py       8      0   100%
pyshared/pytest.py          12      0   100%
pyshared/python.py          69      3    96%   40, 63, 139
pyshared/shell.py            9      0   100%
pyshared/terminal.py        34      0   100%
pyshared/test.py            54      0   100%
pyshared/version.py          1      0   100%
------------------------------------------------------
TOTAL                      262      6    98%
```

## License

MIT

## Contact

ccarterdev@gmail.com
