import os
import typing as TYPE


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
