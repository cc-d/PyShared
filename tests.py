import os
import re
from unittest.mock import patch
from .pyshared.env import typed_evar
from .pyshared.crypto import is_jwt
from .pyshared import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS
from .pyshared.exceptions import NotPrintableError
from .pyshared.python import ranstr, safe_repr, default_repr
from pyshared.shell import runcmd
from subprocess import CompletedProcess
from pyshared.terminal import get_terminal_width, print_middle, print_columns


def test_get_terminal_width():
    assert isinstance(get_terminal_width(), int)
    assert get_terminal_width(999999) == 999999


def test_print_middle():
    assert "- test -" in print_middle("test", char='-', noprint=True)


def test_print_columns():
    columns = print_columns(["one", "two", "three"], terminal_width=10)
    assert isinstance(columns, list)


def test_noprint():
    with patch("builtins.print") as mock_print:
        print_middle("test")
        mock_print.assert_called_once()


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


def test_consts():
    assert ALPHANUMERIC_CHARS.isalnum()
    not_in_alphanum = set(ALPHANUMERIC_EXT_CHARS) - set(ALPHANUMERIC_CHARS)
    assert not_in_alphanum == {'-', '_'}


def test_is_jwt_valid():
    valid_jwt = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c"
    assert is_jwt(valid_jwt) is True

    invalid_jwt = "invalid.jwt.token"
    assert is_jwt(invalid_jwt) is False


def test_is_jwt_bytes():
    valid_jwt_bytes = (
        b"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.e30.x0ZzqSb6pQ8rEwzvZEPmZw"
    )
    assert is_jwt(valid_jwt_bytes) is True

    invalid_jwt_bytes = b"invalid.jwt.bytes"
    assert is_jwt(invalid_jwt_bytes) is False


def test_is_jwt_invalid_parts():
    invalid_jwt_two_parts = "part1.part2"
    invalid_jwt_four_parts = "part1.part2.part3.part4"
    assert is_jwt(invalid_jwt_two_parts) is False
    assert is_jwt(invalid_jwt_four_parts) is False


def test_typed_evar():
    # int
    test_evar = ranstr(32)
    os.environ[test_evar] = "123"
    assert typed_evar(test_evar) == 123
    # str
    os.environ[test_evar] = "test"
    assert typed_evar(test_evar) == "test"

    # bool
    os.environ[test_evar] = "TRUE"
    assert typed_evar(test_evar) is True
    os.environ[test_evar] = "fAlSe"
    assert typed_evar(test_evar) is False
    os.environ[test_evar] = "1"
    assert typed_evar(test_evar) is 1
    os.environ[test_evar] = "0"
    assert typed_evar(test_evar) is 0

    # Float
    os.environ[test_evar] = "1.23"
    assert typed_evar(test_evar) == 1.23


def test_safe_repr():
    assert safe_repr(123) == '123'


class TestObject:
    pass


def test_default_repr():
    obj = TestObject()
    assert "TestObject" in default_repr(obj)
