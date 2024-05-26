import os
import os.path as op
import sys
import datetime as DT
from decimal import Decimal as D
from contextlib import contextmanager
from importlib import import_module, reload
from pathlib import Path
from random import choice, randint
from typing import (
    Generator as Gen,
    Iterable,
    Iterator,
    Optional as Opt,
    Union,
    Union as U,
    Any,
    List,
    Tuple,
    Dict,
)

from .consts import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS
from .exceptions import NotPrintableError


@contextmanager
def tmp_pythonpath(path: Union[str, Path], strict: bool = False):
    """Temporarily add a path to the Python path for this context.
    ~path: The path to add to the Python path.
    ~strict: If True, only the path will be in the Python path.
    """
    og_paths = sys.path.copy()
    if strict:
        sys.path = [str(path)]
    else:
        sys.path.insert(0, str(path))
    try:
        yield
    finally:
        sys.path.remove(str(path))
        curpaths = sys.path.copy()
        sys.path = og_paths
        for i, p in enumerate(curpaths):
            if p not in sys.path:
                sys.path.insert(i, p)


def ranstr(
    min_len: int = 16,
    max_len: Opt[int] = None,
    chars: Iterable = ALPHANUMERIC_CHARS,
    as_generator: bool = False,
) -> Union[Gen, str]:
    """Generates str with random chars between min and max length
    ~min_length (int) = 16: The length of the string.
    ~max_length (Optional[int]): The maximum length of the string.
         If None, min_length is used with no variance on ranstr len
    ~chars (Iterable = ALPHANUMERIC_CHARS): Characters used for random str
    ~as_generator (bool) = False: Return a generator instead of a string
    -> Generator | str: The random str or generator for random str
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
    ~use_eval_format (bool): If True, the repr will always be formatted as
        as "Name(attr=value)" instead of "<Name attr=value>" or the
        user-defined repr_format.
    ~obj (Any): The input Python object.

    ~attrs_join (str): The string to join the attributes with.
        Default: ", "
    ~attrs_format (str): The format string to use for each attribute.
        Default: "{attr_name}={attr_repr}"
    ~repr_format (str): The format string to use for the object repr.
        Default: "<{obj_name} {attributes}>"
    ~exclude_attrs (Optional[Iterable[str]]): A list names of attributes
        to exclude from the repr.
    -> str: The string representation of the object.
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
    ~text (str): The str to truncate.
    ~start_chars (int): The number of visible chars at start of str.
    ~ellipsis (str): The ellipsis string to use. Default is '...'.
    ~end_chars (Optional[int]): The number of visible chars at end of str. Default is None.
    -> str: The truncated string.
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


_TYPE_HTIME = Union[int, float, D, str]


class HumanTime:
    incs = ['ms', 's', 'm', 'h', 'd']
    active = {k: None for k in incs}

    def _populate(self, ms: _TYPE_HTIME) -> None:
        self.ms = D(str(ms)) if not isinstance(ms, D) else ms
        if self.ms < 10000:
            self.active['ms'] = self.ms.quantize(D('1.00'))

        self.s = self.ms / D('1000').quantize(D('1.00'))

        if self.s < 60 and self.s > 0.1:
            self.active['s'] = self.s.quantize(D('1.00'))

        self.m = self.s / D('60')

        if self.m < 60 and self.m > 0.1:
            self.active['m'] = self.m.quantize(D('1.00'))

        self.h = self.m / D('60')

        if self.h < 100 and self.h > 0.1:
            self.active['h'] = self.h.quantize(D('1.00'))

        self.d = self.h / D('24')

        if self.d > 1:
            self.active['d'] = self.d.quantize(D('1.00'))

    def __init__(self, ms: _TYPE_HTIME):

        if isinstance(ms, str):
            if ms.endswith('ms'):
                ms = ms.strip().rstrip('ms')
        else:
            ms = D(str(ms)) if not isinstance(ms, D) else ms

        self._populate(ms)

    @property
    def single_str(self) -> str:
        if self.ms == 0:
            return '0ms'

        fstr = ''
        for inc in self.incs:
            if self.active[inc] is not None:
                atxt = str(self.active[inc])
                if atxt.endswith('.00'):
                    atxt = atxt[:-3]
                fstr += f'{atxt}{inc} '

        return fstr.rstrip()

    def __str__(self):
        return self.single_str

    def __repr__(self):
        return self.single_str

    @property
    def last(self) -> str:
        return getattr(self, self.active)


def htime(ms: _TYPE_HTIME) -> str:
    """Converts any time git to human readable time (ms, s, m, h, d)
    ~ms: The time in milliseconds.
    -> str: The human readable time.
       HumanTime object is also returned for further use.
    """
    if isinstance(ms, str):
        ms = ms.strip().rstrip('ms')
    return HumanTime(ms)


_ULISTS = U[List, 'UniqueList']


class UniqueList(list):
    """A list that only allows unique values to be added."""

    def __init__(self, *args, **kwargs):
        items = set()
        for i in args:
            if hasattr(i, '__iter__'):
                items.update(i)
            else:
                items.add(i)
        super().__init__(items, **kwargs)

    def append(self, i: Any) -> bool:
        """Append an item to the list if it is not already in the list.
        ~i: The item to append.
        -> bool: True if the item was appended, False if not.
        """
        for item in self:
            if item.__class__ == i.__class__ and item == i:
                return False

        super().append(i)
        return True

    def extend(self, items: Iterable) -> int:
        """Extend the list with unique values.
        ~items: The items to extend the list with.
        -> int: The number of items that were appended.
        """
        appended = 0
        for i in items:
            if self.append(i):
                appended += 1
        return appended

    def __add__(self, other: _ULISTS) -> 'UniqueList':
        """Add two UniqueList objects together."""
        new_list = UniqueList()
        for i in self:
            new_list.append(i)
        for i in other:
            new_list.append(i)
        return new_list

    def __iadd__(self, other: _ULISTS) -> 'UniqueList':
        """Add another list to this list."""
        self.extend(other)
        return self

    def __repr__(self):
        return super().__repr__()

    def __str__(self):
        return super().__str__()

    def __getitem__(self, idx: int) -> Any:
        return super().__getitem__(idx)

    def __setitem__(self, idx: int, value: Any) -> bool:
        if value in self:
            return False
        super().__setitem__(idx, value)
        return True
