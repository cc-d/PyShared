import os
import os.path as op
import random as ran
import re
import sys
import re
from subprocess import CompletedProcess
from unittest.mock import patch, MagicMock

import pytest as pt


from pyshared import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS
from pyshared import RanData
from pyshared.crypto import is_jwt
from pyshared.env import typed_evar
from pyshared.exceptions import NotPrintableError
from pyshared.python import (
    default_repr,
    ranstr,
    safe_repr,
    truncstr,
    HumanTime as HTime,
    htime,
    tmp_pythonpath,
    UniqueList as UList,
)
from pyshared.shell import runcmd
from pyshared.terminal import get_terminal_width, print_columns, print_middle
from pyshared.pytest import multiscope_fixture
from pyshared import D


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
        # this shouldnt ever happen but if it does, it should raise error
        (None, None, '20.1', int, ValueError),
        (None, None, 1, None, ValueError),
        (None, None, 1.0, None, ValueError),
        (None, None, '1', None, ValueError),
        (None, None, None, int, ValueError),
        (None, None, None, float, ValueError),
        # assumed typing
        ('e', '0', 0, None, 0),
        ('e', '123.3', None, None, 123.3),
        ('e', '123.', None, None, '123.'),
        ('e', '0.0', None, None, 0.0),
        ('e', '0.', None, None, '0.'),
        ('e', '.0', None, None, 0.0),
        ('e', 'True', None, None, True),
        ('e', 'tRuE', None, None, True),
        ('e', 'false', None, None, False),
        ('e', 'fAlSe', None, None, False),
        ('e', '0', None, None, 0),
        ('e', '0', True, None, False),
        ('e', '0', False, None, False),
        ('e', '0', None, bool, True),
        ('e', '0', None, int, 0),
        ('e', '0', 1.0, float, 0.0),
        ('e', '0', None, float, 0.0),
        ('e', 'true', None, str, 'true'),
        ('e', 'tru', None, None, 'tru'),
        ('e', 'false', None, str, 'false'),
        ('e', 'test', True, None, ValueError),
        ('e', 'test', None, int, ValueError),
        ('e', 'test', 1, None, ValueError),
        ('e', 1.1, None, None, ValueError),
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


def test_randata():
    start = 0
    end = 100

    rd = RanData(range=(start, end))
    assert rd.RANGE == (start, end)
    assert all([start <= rd.int <= end for _ in range(end)])

    for k, v in rd.TYPES.items():
        print(k, v)
        assert isinstance(rd[k], v)


def test_no_eval_randata_getitem():
    """regression for potential security issue too"""
    rd = RanData()
    with patch('builtins.print') as mock_print:
        with pt.raises(AttributeError):
            rd['int and print(1)']
        mock_print.assert_not_called()

    # ensure it still works
    assert set(type(rd['int']) for _ in range(100)) == {int}


TESTPATH = ['/tmp/1', '/tmp/2']


@pt.mark.parametrize(
    'tmppath, curpath, expected, strict',
    [
        ('/tmp/3', TESTPATH, ['/tmp/3'] + TESTPATH, False),
        ('/tmp/1', TESTPATH, ['/tmp/1'] + TESTPATH, False),
        ('/tmp/1/2/3', TESTPATH, ['/tmp/1/2/3'] + TESTPATH, False),
        ('/tmp/3', TESTPATH, ['/tmp/3'], True),
        ('/tmp/1', TESTPATH, ['/tmp/1'], True),
        ('/tmp/1/2/3', TESTPATH, ['/tmp/1/2/3'], True),
        ('/tmp/1', TESTPATH, ['/tmp/1'] + TESTPATH, False),
    ],
)
def test_tmp_pythonpath(tmppath, curpath, expected, strict):
    with patch('sys.path', curpath):
        assert sys.path == curpath
        with tmp_pythonpath(tmppath, strict=strict):
            assert sys.path == expected
        assert sys.path == curpath


# Import the module/script where get_logger is defined

from pyshared.log import get_logger


def test_default_logger_singleton():
    """Test that the default logger returns the same instance on repeated calls."""
    logger1 = get_logger()
    logger2 = get_logger()
    assert logger1 is logger2, "Default logger should be a singleton"


def test_different_loggers():
    """Ensure that providing different names results in different logger instances."""
    logger1 = get_logger(name="logger1")
    logger2 = get_logger(name="logger2")
    assert (
        logger1 is not logger2
    ), "Different names should produce different loggers"
    assert logger1.name == "logger1"

    assert logger2.name == "logger2"


def test_log_file_output(tmp_path):
    """Test actual file output."""
    d = tmp_path / "sub"
    d.mkdir()
    log_file = d / "test2.log"

    logger = get_logger(name="outputTest", log_file=str(log_file))
    test_message = "This is a test message for file output."
    logger.info(test_message)

    # Verify the output to the file
    with open(log_file, 'r') as file:
        content = file.read()
        assert test_message in content


# htime


@pt.mark.parametrize(
    'ms, single_str',
    [
        (0, '0ms'),
        (1, '1ms'),
        (1000, '1s'),
        (998, '998ms'),
        (5900, ('5.90s', '5900ms')),
        (60000, '1m'),
        (3600000, '1h'),
    ],
)
def test_htime(ms, single_str):

    ht = HTime(ms)
    if isinstance(single_str, tuple):
        for s in single_str:
            assert s in str(ht)
    else:
        assert single_str in str(ht)


@pt.mark.parametrize(
    'ulmeth, argsreturn',
    [
        ('append', ((1,), (True,))),
        ('append', ((1, 1, 1, 1), (True, False, False, False))),
        (
            'append',
            ((1, '1', D('1'), 1.0, '1.0'), (True, True, True, True, True)),
        ),
        ('extend', ([1, 2, 3], 3)),
        ('extend', ([1 for _ in range(100)], 1)),
        ('extend', ([1, '1', D('1'), 1.0, '1.0'], 5)),
        ('__add__', (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6])),
        ('__add__', (([1, 2, 3], [1, 2, 3, 4]), [1, 2, 3, 4])),
        ('__add__', (([], []), [])),
        ('__add__', (([1, 2, 3], [], [0, 0, 0]), [1, 2, 3, 0])),
        ('__iadd__', (([1, 2, 3], [4, 5, 6]), [1, 2, 3, 4, 5, 6])),
        ('__iadd__', (([1, 2, 3], [1, 2, 3, 4]), [1, 2, 3, 4])),
        ('__iadd__', (([], []), [])),
        ('__iadd__', (([1, 2, 3], [], [0, 0, 0]), [1, 2, 3, 0])),
        ('__iadd__', (([1], []), [1])),
        ('__iadd__', (([], [], [], [4]), [4])),
        ('__repr__', (([1, 2, 3],), repr([1, 2, 3]))),
        ('__str__', (([1, 2, 3],), str([1, 2, 3]))),
        ('__len__', (([1, 2, 3],), 3)),
        ('__len__', (([],), 0)),
        ('__getitem__', (([1, 2, 3], 1), 2)),
        ('__getitem__', (([1, 2, 3], slice(1, 3)), [2, 3])),
        ('__getitem__', (([1, 2, 3], slice(1, 3, 2)), [2])),
        ('__setitem__', (([1, 2, 3], 1, 4), [1, 4, 3])),
        ('__setitem__', (([1, 1, 1], 1, 1, 1), [1])),
        ('__init__', ([1, 2, 3], [1, 2, 3])),
        ('__init__', ((1, 2, 3), [1, 2, 3])),
        ('__init__', ({1, 2, 3}, [1, 2, 3])),
    ],
)
def test_ulist_meths(ulmeth: str, argsreturn: tuple):
    ul = UList()
    if ulmeth == 'append':
        for a, r in zip(*argsreturn):
            meth = getattr(ul, ulmeth)
            mr = meth(a)
            assert mr == r
    elif ulmeth == 'extend':
        meth = getattr(ul, ulmeth)
        mr = meth(argsreturn[0])
        assert mr == argsreturn[1]
        assert len(ul) == argsreturn[1]
    elif ulmeth == '__add__':
        addlists = [list(a) for a in argsreturn[0]]
        newlist = UList()
        while addlists:
            newlist = newlist + addlists.pop(0)
        assert newlist == argsreturn[1]
    elif ulmeth == '__iadd__':
        addlists = [list(a) for a in argsreturn[0]]
        newlist = UList()
        while addlists:
            newlist += addlists.pop(0)
        assert newlist == argsreturn[1]
    elif ulmeth == '__repr__':
        nl = UList(argsreturn[0][0])
        assert repr(nl) == argsreturn[1]
    elif ulmeth == '__str__':
        nl = UList(argsreturn[0][0])
        assert str(nl) == argsreturn[1]
    elif ulmeth == '__getitem__':
        nl = UList(argsreturn[0][0])
        assert nl[argsreturn[0][1]] == argsreturn[1]
    elif ulmeth == '__setitem__':
        nl = UList(argsreturn[0][0])
        nl[argsreturn[0][1]] = argsreturn[0][2]
        assert nl == argsreturn[1]
    elif ulmeth == '__init__':
        nl = UList(argsreturn[0])
        assert nl == argsreturn[1]


ptopts = [
    "-vv",
    "-s",
    "--tb=short",
    "--color=yes",
    "--disable-warnings",
    '-k test_ulist',
]

if __name__ == '__main__':
    print('running tests')
    ulano = test_ulist_meths.__annotations__

    pt.main(ptopts)
