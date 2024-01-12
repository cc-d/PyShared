import os
import re
import sys
import pytest as pt
import random as ran
from unittest.mock import patch
from .pyshared.env import typed_evar
from .pyshared.crypto import is_jwt
from .pyshared import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS
from .pyshared.exceptions import NotPrintableError
from .pyshared.python import ranstr, safe_repr, default_repr
from pyshared.shell import runcmd
from subprocess import CompletedProcess
from pyshared.terminal import get_terminal_width, print_middle, print_columns


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
    with patch("pyshared.terminal.get_terminal_width") as mock_termwidth:
        mock_termwidth.return_value = 20
        with patch("builtins.print") as mock_print:
            print_columns(iterable, separator=separator)
            assert mock_print.call_count == 2


def test_noprint():
    with patch("builtins.print") as mock_print:
        print_middle("test")
        mock_print.assert_called_once()


##### python.py #####
def test_runcmd():
    result = runcmd("echo test", output=True)
    assert isinstance(result, CompletedProcess)
    assert result.stdout.strip() == "test"


def test_runcmd_no_output():
    result = runcmd("echo hi", output=False)
    assert result is None


def test_default_repr_different_objects():
    assert "int(10)" == default_repr(10)
    assert "[]" == default_repr([])
    assert "{}" == default_repr({})
    assert "()" == default_repr(())


def test_safe_repr():
    assert safe_repr(123) == '123'


class TestObject:
    pass


def test_default_repr():
    obj = TestObject()
    assert "TestObject" in default_repr(obj)


##### env.py #####
evname = ranstr(32)


def test_typed_evar_novar():
    # no evar set and default specified
    assert typed_evar(evname, default=123) == 123
    assert typed_evar(evname, default='123') == '123'
    assert typed_evar(evname, default=True) is True
    assert typed_evar(evname, default=False) is False
    assert typed_evar(evname, default=evname) == evname

    # no evar set and no default specified
    assert typed_evar(evname) is None


def test_typed_evar_var_floatint():
    # int
    ev = ranstr(32)
    val = '1234321'
    os.environ[ev] = val
    assert typed_evar(ev, default=1) == int(val)
    assert typed_evar(ev, default=1.0) == float(val)

    # no default int/float
    os.environ[ev] = '2.1'
    assert typed_evar(ev) == 2.1
    os.environ[ev] = '2'
    assert typed_evar(ev) == 2


def test_typed_evar_var_bool():
    # bool
    ev = ranstr(32)
    testvals = {
        ('1', True): True,
        ('0', False): False,
        ('true', True): True,
        ('false', False): False,
        ('TRUE', True): True,
        ('FALSE', False): False,
        ('tRuE', True): True,
        ('fAlSe', False): False,
        ('-1', False): False,
    }
    for val, expected in testvals.items():
        os.environ[ev] = val[0]
        assert typed_evar(ev, default=val[1]) == expected

    os.environ[ev] = 'invalid'
    with pt.raises(ValueError):
        typed_evar(ev, default=True)
