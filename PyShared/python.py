from typing import (
    Optional as Opt,
    Union,
    Any,
    Generator as Gen,
    Iterable,
    Union as U,
)
from random import choice, randint
from pathlib import Path
from importlib import reload, import_module
from .exceptions import NotPrintableError
from .consts import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS


def ranstr(
    min_len: int = 16,
    max_len: Opt[int] = None,
    chars: Iterable = ALPHANUMERIC_CHARS,
    as_generator: bool = False,
) -> Union[Gen, str]:
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


_EVAL_FORMAT = '{obj_name}({attributes})'
_REPR_FORMAT = '<{obj_name} {attributes}>'
_ATTRS_FORMAT = '{attr_name}={attr_repr}'


def default_repr(
    obj: Any,
    use_eval_format: bool = False,
    join_attrs_on: str = ', ',
    attrs_format: str = _ATTRS_FORMAT,
    repr_format: str = _REPR_FORMAT,
    exclude_attrs: Opt[Iterable[str]] = None,
) -> str:
    """Return a string representation of a custom Python object.
    This representation is constructed such that the object can be
    reconstructed from the returned string, ideally. Complex objects
    may not be able to be reconstructed.
    Args:
        use_eval_format (bool): If True, the repr will always be formatted as
            as "Name(attr=value)" instead of "<Name attr=value>" or the
            user-defined repr_format.
        obj (Any): The input Python object.
        attrs_join (str): The string to join the attributes with.
            Default: ", "
        attrs_format (str): The format string to use for each attribute.
            Default: "{attr_name}={attr_repr}"
        repr_format (str): The format string to use for the object repr.
            Default: "<{obj_name} {attributes}>"
        exclude_attrs (Optional[Iterable[str]]): A list names of attributes
            to exclude from the repr.
    Returns:
        str: The string representation of the object.
    """
    exclude_attrs = exclude_attrs or []
    if use_eval_format:
        repr_format = _EVAL_FORMAT

    if obj is None:
        return 'None'
    elif isinstance(obj, (float, str, set, list, tuple, dict, int, bool)):
        return repr(obj)

    # If the object has a __dict__ attribute, use that
    if hasattr(obj, '__dict__'):
        attributes = {key: value for key, value in obj.__dict__.items()}
    else:
        attributes = {attr: getattr(obj, attr) for attr in dir(obj)}
    attributes = join_attrs_on.join(
        attrs_format.format(attr_name=attr, attr_repr=safe_repr(value))
        for attr, value in attributes.items()
        if not hasattr(value, '__call__')
        and not str(attr).startswith('_')
        and attr not in exclude_attrs
    )
    obj_name = ''
    if hasattr(obj, '__class__'):
        if hasattr(obj.__class__, '__name__'):
            obj_name = obj.__class__.__name__
    if hasattr(obj, '__name__'):
        obj_name += ' ' + obj.__name__
    return repr_format.format(obj_name=obj_name, attributes=attributes)


def truncstr(
    text: str,
    start_chars: int = 3,
    ellipsis: str = '...',
    end_chars: Opt[int] = None,
) -> str:
    """Truncates a string using a provided ellipsis string.
    Args:
        text (str): The str to truncate.
        ellipsis (str): The ellipsis string to use.
            Default: '...'
        start_chars (int): The number of visible chars at start of str
            Default: 3
        end_chars (Optional[int]): The number of visible chars at end of str
            Default: None
    Returns:
        str: The truncated string.
    """
    text = str(text)
    # backwards compatability
    if isinstance(start_chars, str) and isinstance(ellipsis, int):
        ellipsis, start_chars = start_chars, ellipsis
    if len(text) <= start_chars:
        return text
    str_start = text[:start_chars]
    str_end = text[-end_chars:] if end_chars else ''
    return str_start + ellipsis + str_end
