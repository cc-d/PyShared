import typing as TYPE
from functools import wraps
from random import choice, randint
from shlex import split as shx_split
from subprocess import CompletedProcess
from subprocess import run as sp_run

from .consts import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS
from .exceptions import NotPrintableError


def ranstr(
    min_len: int = 16,
    max_len: TYPE.Optional[int] = None,
    chars: TYPE.Iterable = ALPHANUMERIC_CHARS,
    as_generator: bool = False,
) -> TYPE.Union[TYPE.Generator, str]:
    """Generates str with random chars between min and max length
    Args:
        min_length (int) = 16: The length of the string.
        max_length (Optional[int]): The maximum length of the string.
            If None, min_length is used with no variance on ranstr len
        chars (Iterable = ALPHANUMERIC_CHARS): Characters used for random str
        as_generator (bool) = False: Return a generator instead of a string
    Returns:
        Generator | str: The random str or generator for random str
    """
    str_len = min_len if max_len is None else randint(min_len, max_len)

    if as_generator:
        return (choice(chars) for _ in range(str_len))
    return ''.join(choice(chars) for _ in range(str_len))


def runcmd(
    cmd: TYPE.Union[str, TYPE.List], output: bool = True, *args, **kwargs
) -> TYPE.Optional[CompletedProcess]:
    """Runs a single command in the shell with subprocess.run
    Args:
        cmd (Union[str, List]): The command to run in the shell.
        output (bool): Whether or not to return the output of the command.
            Defaults to True.
    """
    if isinstance(cmd, str):
        cmd = shx_split(cmd)

    if output:
        return sp_run(
            cmd, check=True, text=True, capture_output=True, *args, **kwargs
        )
    else:
        sp_run(
            cmd, check=False, text=False, capture_output=False, *args, **kwargs
        )


def safe_repr(obj):
    """Try and returns an objects repr, then str if err, then NotPrintableError
    error message if both fail
    """
    try:
        return repr(obj)
    except Exception as e_repr:
        try:
            return str(obj)
        except Exception as e_str:
            err = NotPrintableError(obj, e_repr, e_str)
            return err.message


def default_repr(
    obj: TYPE.Any,
    join_attrs_on: str = ', ',
    attrs_format: str = "{attr_name}={safe_attr_repr}",
    repr_format: str = "{obj_name}({attributes})",
) -> str:
    """Return a string representation of a custom Python object.
    This representation is constructed such that the object can be
    reconstructed from the returned string, ideally. Complex objects
    may not be able to be reconstructed.
    Args:
        obj (Any): The input Python object.
        attrs_join (str) = ', ': The string to join the attributes with.
        attrs_format (str) = "{attr_name}={safe_attr_repr}": The format string
            to use for each attribute.
    Returns:
        str: The string representation of the object.
    """
    # If the object has a __dict__ attribute, use that
    if hasattr(obj, '__dict__'):
        attributes = join_attrs_on.join(
            attrs_format.format(attr_name=key, safe_attr_repr=safe_repr(value))
            for key, value in obj.__dict__.items()
            if not hasattr(value, '__call__') and not str(key).startswith("_")
        )
    # Otherwise, use dir() to gather potential attributes
    else:
        if isinstance(obj, int):
            return 'int(%s)' % obj
        elif isinstance(obj, float):
            return 'float(%s)' % obj
        elif isinstance(obj, str):
            return 'str(%s)' % obj
        elif isinstance(obj, set):
            return 'set(%s)' % obj
        elif isinstance(obj, (list, tuple, dict)):
            return str(obj)

        attributes = join_attrs_on.join(
            attrs_format.format(
                attr_name=attr, safe_attr_repr=safe_repr(getattr(obj, attr))
            )
            for attr in dir(obj)
            if not hasattr(obj, '__call__') and not str(attr).startswith('_')
        )

    return repr_format.format(
        obj_name=obj.__class__.__name__, attributes=attributes
    )
