import os
import typing as TYPE


def get_terminal_width(default: int = 80) -> int:
    """Gets current terminal width or default 80 if not detectable"""
    try:
        return os.get_terminal_size().columns
    except OSError:
        return default


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
    if curline:
        print(curline)
        printed.append(curline)

    return printed
