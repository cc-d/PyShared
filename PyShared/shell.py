import os
import typing as TYPE
from subprocess import run as sp_run, CompletedProcess
from shlex import split as shx_split


def get_terminal_width(default: int = 80) -> int:
    """Gets current terminal width or default 80 if not detectable"""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return default


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


def print_middle(
    obj: TYPE.Any, char: str = '=', noprint: bool = False, *args, **kwargs
) -> str:
    """prints object str in middle of line of $chars based on terminal width
    passes *args/**kwargs to print()
    Args:
        obj (Any): The object whose string representation needs to be printed.
        char (str): Char used for line default '='
        noprint (bool) = False: If True, don't print, just return str
    """
    terminal_width = get_terminal_width()
    obj = str(obj)

    padding = (terminal_width - len(obj) - 2) // 2

    # not using fstring for backwards compatibility
    result = '%s %s %s' % (char * padding, obj, char * padding)

    if not noprint:
        print(result, *args, **kwargs)
    return result


def print_columns(
    iterable: TYPE.Iterable[str],
    separator: str = "  ",
    terminal_width: TYPE.Optional[int] = None,
) -> TYPE.List[str]:
    """Print a list of objects in columns based on the terminal width.
    Args:
        iterable (Iterable): The iterable to be printed.
        separator (str) = "  ": The separator to be used between columns.
        terminal_width (Optional[int]): The terminal width to be used.
    Returns:
        List[str]: The list of strings that were printed.
    """
    termwidth = terminal_width or get_terminal_width()

    objs = [str(obj) for obj in iterable]
    longest = max(len(obj) for obj in objs)

    printed = []

    curline = ""
    while objs:
        curobj = objs.pop(0)
        curobj += " " * (longest - len(curobj))
        curobj += separator

        if len(curline) + len(curobj) > termwidth:
            print(curline)
            printed.append(curline)
            curline = ""
        else:
            curline += curobj

    return printed


def typed_evar(name: str, default: TYPE.Optional[TYPE.Any] = None):
    """Return an environment variable with an assumed type. Type from
    the default value, if provided, will be prioritized, otherwise
    the type will be inferred in order of: bool, int, float, str.

    (CURDAY, 25) -> 25
    (CURDAY, 25.0) -> 25.0
    (CURDAY, '25.0') -> '25.0'
    (CURDAY, None) -> '25'

    Args:
        name (str): The name of the environment variable.
        default (Optional[Any]): The default value of the environment variable.
            Defaults to None.
    Returns:
        Any: The env var value with the assumed type.
    """
    varval = os.environ.get(name)
    if varval is None:
        return default

    # use default's type
    if default is not None:
        vartype = type(default)

        # bool gets special treatment
        if vartype is bool:
            if varval.lower() in ('1', 'true'):
                return True
            elif varval.lower() in ('0', 'false', '-1'):
                return False
            else:
                raise ValueError(
                    "Invalid boolean value for environment variable %s: %s"
                    % (name, varval)
                )
        try:
            return vartype(varval)
        except Exception:
            pass

    # otherwise assume type using a few simple types
    if varval.casefold() in ('true', 'false'):
        return varval.casefold() == 'true'

    for vartype in (int, float):
        try:
            return vartype(varval)
        except ValueError:
            continue

    return varval
