# PyShared: A Python Utility Library

PyShared is a personal Python utility library that I use in my projects containing a collection of consts/functions/classes/etc that I have found useful across multiple codebases.

## Installation

```bash
pip install pyshared
```

for the lib, for the dev dependencies:

```bash
pip install pyshared[dev]
```

## `consts.py`

- `ALPHANUMERIC_CHARS`: Import this constant for a string of all alphanumeric characters.
- `ALPHANUMERIC_EXT_CHARS`: Import this for an extended set of alphanumeric characters including underscores and hyphens.

```python
from pyshared.consts import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS
```

## `crypto.py`

- `is_jwt`: Import this function to check if a given string is a valid JSON Web Token (JWT).

```python
from pyshared.crypto import is_jwt
```

## `env.py`

- `typed_evar`: Import this function to fetch environment variables with automatic type casting based on a provided default value.

```python
from pyshared.env import typed_evar
```

## `exceptions.py`

- `NotPrintableError`: Import this custom exception class for use in scenarios where object representations fail.

```python
from pyshared.exceptions import NotPrintableError
```

## `python.py`

- `ranstr`: Import this function to generate random strings.
- `safe_repr`: Import this for a safe string representation of objects.
- `default_repr`: Import this for a default string representation of custom Python objects.

```python
from pyshared.python import ranstr, safe_repr, default_repr
```

## `shell.py`

- `runcmd`: Import this function to execute shell commands from within Python.

```python
from pyshared.shell import runcmd
```

## `terminal.py`

- `get_terminal_width`: Import this to get the current width of the terminal.
- `print_middle`: Import this for printing text centered in the terminal.
- `print_columns`: Import this to neatly print items in columns according to the terminal width.

```python
from pyshared.terminal import get_terminal_width, print_middle, print_columns
```

These specific imports are designed to provide direct access to the functionalities within the PyShared package, aligning with my approach to efficient and reusable coding.

## Test Coverage

**LITERALLY 100% LOL**

Test Results:

```
tests.py::test_consts PASSED
tests.py::test_is_jwt_valid_valid PASSED
tests.py::test_is_jwt_valid_invalid PASSED
...
tests.py::test_default_repr_for_custom_slot_object PASSED

Coverage report:
------------------------------------------------------
pyshared/__init__.py         100%
pyshared/consts.py           100%
pyshared/crypto.py           100%
pyshared/env.py              100%
pyshared/exceptions.py       100%
pyshared/python.py           100%
pyshared/shell.py            100%
pyshared/terminal.py         100%
------------------------------------------------------
TOTAL                        100%
```

This comprehensive testing ensures that the library is reliable for production use.

## License

MIT
