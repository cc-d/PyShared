import os
import random as ran
import re
import sys
import re
from subprocess import CompletedProcess
from unittest.mock import patch

import pytest as pt

from .pyshared import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS
from .pyshared.crypto import is_jwt
from .pyshared.env import typed_evar
from .pyshared.exceptions import NotPrintableError
from .pyshared.python import default_repr, ranstr, safe_repr, truncstr
from .pyshared.shell import runcmd
from .pyshared.terminal import get_terminal_width, print_columns, print_middle
from .pyshared.pytest import multiscope_fixture


##### consts.py #####
def test_consts():
    _asscii = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    _asscii = _asscii + '0123456789'
    assert set(ALPHANUMERIC_CHARS) == set(_asscii)
    assert set(ALPHANUMERIC_EXT_CHARS) - set(ALPHANUMERIC_CHARS)


##### crypto.py #####


def test_is_jwt_valid_valid():
    jwt = f'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2YWxpZCI6Imp3dCJ9.BJc7CfppzWBPxNVzVteymEl6Hs6rCyax9_OM7LM3cQA'
    assert is_jwt(jwt)


def test_is_jwt_valid_invalid():
    _inv = [
        'valid.part.number',
        'invalid.part.number.ohno',
        'invalid.',
        # valid but segments wrong
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJpYXQiOjE1ODUxMzUwNjJ9',
        # valid jwt but invalid base64
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VybmFtZSI6InRlc3QiLCJpYXQiOjE1ODUxMzUwNjJ9.ohno',
        # valid base64 but invalid jwt
        'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.ohno.ohno',
    ]
    for inv in _inv:
        assert not is_jwt(inv)


def test_is_jwt_bytes_valid():
    jwt = b'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ2YWxpZCI6Imp3dCJ9.BJc7CfppzWBPxNVzVteymEl6Hs6rCyax9_OM7LM3cQA'
    assert is_jwt(jwt)


##### terminal.py #####


def test_print_columns_with_different_iterables():
    iterable = ["a", "b", "c"]
    assert set(print_columns(iterable)[0]) == set("a  b  c")


def test_print_columns_with_custom_separator():
    iterable = ['a' * 10, 'b' * 10, 'c' * 10]
    separator = "|"
    with patch("builtins.print") as mock_print:
        print_columns(iterable, separator=separator, terminal_width=20)

        assert mock_print.call_count == 2
    print(mock_print.call_args_list, mock_print.call_count)


def test_noprint():
    with patch("builtins.print") as mock_print:
        print_middle("test")
        mock_print.assert_called_once()


def test_get_terminal_width_os_error():
    with patch('os.get_terminal_size', side_effect=OSError):
        width = get_terminal_width()
        assert width == 80  # Assuming 80 is the default width set


##### env.py #####
@pt.mark.parametrize(
    'evname, ev, default, vartype, expected',
    [
        # with default arg
        ('evname', '0', 0, None, 0),
        # this shouldnt ever happen but if it does, it should raise error
        (None, None, '20.1', int, ValueError),
        (None, None, 1, None, ValueError),
        (None, None, 1.0, None, ValueError),
        (None, None, '1', None, ValueError),
        (None, None, None, int, ValueError),
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
    ],
)
def test_typed_evar(evname, ev, default, vartype, expected):
    with patch('os.environ.get') as mock_get:
        mock_get.return_value = ev
        # determine if expected is an exception or not
        if isinstance(expected, type) and issubclass(expected, Exception):
            with pt.raises(Exception):
                typed_evar(evname, default, vartype)
        else:
            assert typed_evar(evname, default, vartype) == expected


##### exceptions.py #####


def test_NotPrintableError():
    class Dummy:
        d = 'dumb'

    np = NotPrintableError(Dummy(), Exception('repr'), Exception('str'))
    assert type(np.obj) == type(Dummy())


##### python.py #####
def test_ranstr_generator():
    _len = 10
    _gen = ranstr(_len, as_generator=True)
    assert type(_gen) == type((i for i in range(1)))


def test_runcmd_no_output():
    result = runcmd("echo hi", output=False)
    assert result is None


def test_default_repr_different_objects():
    assert "%d" % 10 == default_repr(10)
    assert "[]" == default_repr([])
    assert "{}" == default_repr({})
    assert "()" == default_repr(())
    assert "%s" % 10.0 == default_repr(10.0)
    assert repr('one1') == default_repr('one1')
    assert "{1,2,3}" == default_repr({1, 2, 3}).replace(" ", "")

    class TestObject:
        def __init__(self):
            self.a = 1
            self.b = 2
            self.c = 3

    obj = TestObject()
    assert '<TestObject a=1, b=2, c=3>' == default_repr(obj)


def test_safe_repr():
    assert safe_repr(123) == '123'


def test_safe_repr_except():
    class Dummy:
        def __repr__(self):
            raise Exception('test')

    safe = safe_repr(Dummy())
    safe = re.sub(r'ID: \d+', 'ID: 0', safe)
    safe_err = NotPrintableError(Dummy(), Exception('test'), Exception('test'))
    safe_err = re.sub(r'ID: \d+', 'ID: 0', safe_err.message)
    assert safe == safe_err


class TestObject:
    pass


def test_default_repr():
    obj = TestObject()
    assert "TestObject" in default_repr(obj)


def test_runcmd():
    result = runcmd("echo test", output=True)
    assert isinstance(result, CompletedProcess)
    assert result.stdout.strip() == "test"


class CustomSlotObject:
    __slots__ = ['a', 'b']

    def __init__(self):
        self.a = 1
        self.b = 2


def test_default_repr_no_private():
    obj = CustomSlotObject()
    repr_str = default_repr(obj)
    assert "<CustomSlotObject a=1, b=2>" == repr_str


def test_default_repr_eval_format():
    obj = CustomSlotObject()
    repr_str = default_repr(obj, use_eval_format=True)
    assert "CustomSlotObject(a=1, b=2)" == repr_str


def test_default_repr_None():
    assert default_repr(None) == 'None'


TESTSTR = 'a' * 100


def test_truncstr_defaults():
    assert truncstr(TESTSTR) == 'aaa...'


@pt.mark.parametrize(
    'tstr, start_chars, ellipsis, end_chars, expected',
    [
        (TESTSTR, 1, 'z', 1, 'aza'),
        (TESTSTR, 1, '.', None, 'a.'),
        (TESTSTR, '.', 5, 2, 'a' * 5 + '.aa'),
        (TESTSTR, 100, '...', None, TESTSTR),
        (TESTSTR, 0, '|', 50, '|' + TESTSTR[:-50]),
        ('abcdefghijklmnopqrstuvwxyz', 5, '', 5, 'abcdevwxyz'),
        (None, 1, '...', 1, 'N...e'),
    ],
)
def test_truncstr_args(tstr, start_chars, ellipsis, end_chars, expected):
    assert truncstr(tstr, start_chars, ellipsis, end_chars) == expected


@multiscope_fixture
def fix():
    return 1


def test_multiscope_fixture(fix, fix_function, fix_module, fix_session):
    assert fix == 1
    assert fix_function == 1
    assert fix_module == 1
    assert fix_session == 1
