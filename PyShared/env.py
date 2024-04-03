import os
from typing import Union as U, Optional as Opt, Any as A


def typed_evar(
    name: str, default: Opt[A] = None, vartype: U[type, A] = None
) -> A:
    """Return an environment variable with an assumed type. Type from
    the default value, if provided, will be prioritized, otherwise
    the type will be inferred in order of: bool, int, float, str.
    ~name (str): the environment variable name
    ?default (Any): the default value if the environment variable is not set
    ?vartype (type): override type assumption to attempt to cast to this type

    (CURDAY, 25) -> 25
    (CURDAY, 25.0) -> 25.0
    (CURDAY, '25.0') -> '25.0'
    (CURDAY, None) -> '25'
    (CURDAY, None, int) -> 25
    (CURDAY, None, float) -> 25.0
    (CURDAY, None, bool) -> True
    (CURDAY, None, Decimal) -> Decimal('25')

    """
    if name is None:
        raise ValueError('Environment variable name cannot be None')

    varval = os.environ.get(name)
    if varval is None:
        return default

    if vartype is not None:
        return vartype(varval)

    _true = ('1', 'true', 'yes', 'on')
    _false = ('0', 'false', 'no', 'off')

    deftype = type(default) if default is not None else None
    if deftype is not None:
        if deftype is bool:
            if varval.lower() in _true:
                return True
            elif varval.lower() in _false:
                return False
            raise ValueError('Invalid boolean value: %s' % varval)
        return deftype(varval)

    casevar = varval.casefold()

    # otherwise assume type using a few simple types
    if casevar in ('1', 'true', 'false', '0'):
        return True if casevar in _true else False
    elif varval.isdigit():
        return int(varval)
    elif '.' in varval:
        spval = varval.split('.')
        if len(spval) == 2:
            if spval[0].isdigit() and spval[1].isdigit():
                return float(varval)
            elif spval[0] == '' and spval[1].isdigit():
                return float(varval)

    return str(varval)
