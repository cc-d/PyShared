import random as ran
from typing import Generator as Gen


class RanData:
    """class to make generating random data easier"""

    RANGE: tuple
    TYPES: dict = {
        'int': int,
        'float': float,
        'str': str,
        'bool': bool,
        'list': list,
        'dict': dict,
        'tuple': tuple,
        'set': set,
        'frozenset': frozenset,
        'bytes': bytes,
        'bytearray': bytearray,
        'generator': Gen,
        'range': range,
        'slice': slice,
        'memoryview': memoryview,
    }

    def __init__(self, range: tuple = (1, 1000)):
        self.RANGE = range

    @property
    def int(self) -> int:
        """Generate a random integer."""
        return ran.randint(*self.RANGE)

    @property
    def float(self) -> float:
        """Generate a random float."""
        return ran.uniform(*self.RANGE)

    @property
    def str(self) -> str:
        """Generate a random string."""
        return 'str' + str(self.int)

    @property
    def bool(self) -> bool:
        """Generate a random boolean."""
        return ran.choice([True, False])

    @property
    def list(self) -> list:
        """Generate a random list."""
        return [self.int, self.float, self.str, self.bool]

    @property
    def dict(self) -> dict:
        """Generate a random dictionary."""
        return {self.str: self.int, self.int: self.str, self.bool: self.float}

    @property
    def tuple(self) -> tuple:
        """Generate a random tuple."""
        return (self.int, self.float, self.str, self.bool)

    @property
    def set(self) -> set:
        """Generate a random set."""
        return {self.int, self.float, self.str, self.bool}

    @property
    def frozenset(self) -> frozenset:
        """Generate a random frozenset."""
        return frozenset({self.int, self.float, self.str, self.bool})

    @property
    def bytes(self) -> bytes:
        """Generate a random bytes object."""
        return bytes(self.int)

    @property
    def bytearray(self) -> bytearray:
        """Generate a random bytearray object."""
        return bytearray(self.int)

    @property
    def generator(self) -> Gen:
        """Generate a random generator."""
        return (i for i in range(self.int))

    @property
    def range(self) -> range:
        """Generate a random range object."""
        return range(self.int)

    @property
    def slice(self) -> slice:
        """Generate a random slice object."""
        return slice(self.int, self.int, self.int)

    @property
    def memoryview(self) -> memoryview:
        """Generate a random memoryview object."""
        return memoryview(self.bytes)

    def __getitem__(self, key: str):
        """Return the random data for the given type."""
        return getattr(self, key)
