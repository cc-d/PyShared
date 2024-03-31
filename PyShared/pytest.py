import pytest as pt
import inspect
from typing import Callable as Call

_SCOPES = ['function', 'module', 'session']


def multiscope_fixture(func: Call):
    """Decorator to create a fixture for each scope (function, module, session)
    following the naming convention: {func_name}_{scope} as well as ensuring
    the original functional fixture is available under the original name.

    ~func (Call): The function to be decorated as a fixture.
    -> Call: The original function decorated for function scope.
    """
    # Get the globals of the calling module, not this module
    caller_globals = inspect.currentframe().f_back.f_globals

    for sc in _SCOPES:
        decorated = pt.fixture(scope=sc)(func)
        caller_globals[f'{func.__name__}_{sc}'] = decorated

    # Update the function to be the one decorated for function scope
    func = caller_globals[f'{func.__name__}_function']
    return func
