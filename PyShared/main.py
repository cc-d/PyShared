import random as ran
import typing
import common_types as TYPE
from .consts import ALPHANUMERIC_CHARS, ALPHANUMERIC_EXT_CHARS


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
    str_len = min_len if max_len is None else ran.randint(min_len, max_len)

    if as_generator:
        return (ran.choice(chars) for _ in range(str_len))
    return ''.join(ran.choice(chars) for _ in range(str_len))
